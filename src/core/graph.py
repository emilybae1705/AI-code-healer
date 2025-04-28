from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from config import MODEL, CHROMA_PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME
from state import State
import inspect
import chromadb
import uuid


class CodeHealerNodes:
    def __init__(self):
        self.graph = StateGraph(State)
        self.llm = ChatOpenAI(model=MODEL)  # gpt-4o-mini
        self.collection = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIRECTORY
        ).create_collection(name=CHROMA_COLLECTION_NAME)

    def code_executor(self, state: State):
        """Run User Code"""
        try:
            print("\nRunning Arbitrary Function")
            print("--------------------------\n")
            result = state.function(*state.arguments)
            print("\n✅ Arbitrary Function Ran Successfully")
            print(f"Result: {result}")
            print("-----------------------------------\n")
        except Exception as e:
            print(f"❌ Function Raised Error: {e}")
            state.error = True
            state.error_description = str(e)
        return state

    def code_updater(self, state: State):
        """Connects with OpenAI API to update user's buggy code"""
        prompt = ChatPromptTemplate.from_template(
            "You are tasked with fixing a Python function that raised an error."
            "Function: {function_string}"
            "Error: {error_description}"
            "You must provide a fix for the present error only."
            "The bug fix should handle the thrown error case gracefully by returning an error message."
            "Do not raise an error in your bug fix."
            "The function must use the exact same name and parameters."
            "Your response must contain only the function definition with no additional text."
            "Your response must not contain any additional formatting, such as code delimiters or language declarations."
        )
        message = HumanMessage(
            content=prompt.format(
                function_string=state.function_string,
                error_description=state.error_description,
            )
        )
        new_function_string = self.llm.invoke([message]).content.strip()

        print("\n⚠️ Buggy Function")
        print("-------------------\n")
        print(state.function_string)
        print("\n💠 Proposed Bug Fix")
        print("-------------------\n")
        print(new_function_string)

        state.new_function_string = new_function_string
        return state

    def code_patcher(self, state: State):
        """Verifies new function generated has the same signature as the original
        and updates state if no errors occur during validation process"""
        try:
            print("\n******************")
            print("\n♻️ Patching code...")

            original_sig = inspect.signature(state.function)
            original_args = len(original_sig.parameters)

            namespace = {}
            exec(state.new_function_string, namespace)

            func_name = state.function.__name__
            new_function = namespace[func_name]

            new_sig = inspect.signature(new_function)
            new_args = len(new_sig.parameters)

            if new_args != original_args:
                print(
                    f"Function expects {new_args} arguments, but original function had {original_args}"
                )
                return state

            state.function = new_function
            state.error = False
            result = state.function(*state.arguments)

            print("...patch complete!\n")
        except Exception as e:
            print(f"...patch failed: {e}")
            return False, str(e)

        print("******************\n")
        return state

    def bug_reporter(self, state: State):
        """Generates Bug Report"""
        prompt = ChatPromptTemplate.from_template(
            "You are tasked with generating a bug report for a Python function that raised an error."
            "Function: {function_string}"
            "Error: {error_description}"
            "Your response must be a comprehensive string including only crucial information on the bug report"
        )
        message = HumanMessage(
            content=prompt.format(
                function_string=state.function_string,
                error_description=state.error_description,
            )
        )
        bug_report = self.llm.invoke([message]).content.strip()

        print("\n📝 Generating Bug Report")
        print("------------------------\n")
        print(bug_report)

        state.bug_report = bug_report
        return state

    def memory_searcher(self, state: State):
        """Find memories relevant to the current bug report"""
        prompt = ChatPromptTemplate.from_template(
            "You are tasked with archiving a bug report for a Python function that raised an error."
            "Bug Report: {bug_report}."
            "Your response must be a concise string including only crucial information on the bug report for future reference."
            "Format: # function_name ## error_description ### error_analysis"
        )

        message = HumanMessage(content=prompt.format(bug_report=state.bug_report))
        response = self.llm.invoke([message]).content.strip()
        results = self.collection.query(query_texts=[response])

        print("\nSearching bug reports...")
        if results["ids"][0]:
            print(f"...{len(results['ids'][0])} found.\n")
            print(results)
            state.memory_search_results = [
                {
                    "id": results["ids"][0][idx],
                    "memory": results["documents"][0][idx],
                    "distance": results["distances"][0][idx],
                }
                for idx, id in enumerate(results["ids"][0])
            ]
        else:
            print("...none found.\n")

        return state

    def memory_filter(self, state: State):
        """Filters top 30% of results to ensure relevance of memories stays updated"""
        print("\nFiltering bug reports...")

        for memory in state.memory_search_results:
            if memory["distance"] < 0.3:
                state.memory_ids_to_update.append(memory["id"])

        if state.memory_ids_to_update:
            print(f"...{len(state.memory_ids_to_update)} selected.\n")
        else:
            print("...none selected.\n")

        return state

    def memory_generator(self, state: State):
        """Condenses bug report and generates relevant memories before storing in ChromaDB Vector Database"""
        prompt = ChatPromptTemplate.from_template(
            "You are tasked with archiving a bug report for a Python function that raised an error."
            "Bug Report: {bug_report}."
            "Your response must be a concise string including only crucial information on the bug report for future reference."
            "Format: # function_name ## error_description ### error_analysis"
        )

        message = HumanMessage(content=prompt.format(bug_report=state.bug_report))
        response = self.llm.invoke([message]).content.strip()

        print("\n💾 Saving Bug Report to Memory")
        print("------------------------------\n")
        print(response)

        id = str(uuid.uuid4())
        self.collection.add(
            ids=[id],
            documents=[response],
        )

        return state
