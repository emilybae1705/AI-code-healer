from langgraph.graph import END
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from src.config import MODEL, CHROMA_PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME
from src.core.state import State
import inspect
import chromadb
import uuid
from typing import List, Dict, Any, Optional, Tuple


class Nodes:
    llm = ChatOpenAI(model=MODEL)  # gpt-4o-mini
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
    try:
        collection = client.get_collection(name=CHROMA_COLLECTION_NAME)
    except:
        collection = client.create_collection(name=CHROMA_COLLECTION_NAME)

    @staticmethod
    def code_executor(state: State) -> State:
        try:
            # Execute the function with the provided arguments
            result = state.function(*state.arguments)
            state.result = result
            state.error = False
            return state
        except Exception as e:
            state.error = True
            state.error_message = str(e)
            return state

    @staticmethod
    def error_detector(state: State) -> State:
        if state.error:
            state.error_type = type(state.error_message).__name__
            return state
        return state

    @staticmethod
    def bug_reporter(state: State) -> State:
        if state.error:
            state.bug_report = {
                "error_type": state.error_type,
                "error_message": state.error_message,
                "function_string": state.function_string,
                "arguments": str(state.arguments),
            }
        return state

    @staticmethod
    def memory_manager(state: State) -> State:
        # Store the bug report
        collection.add(
            documents=[str(state.bug_report)],
            metadatas=[{"error_type": state.error_type}],
            ids=[str(uuid.uuid4())],
        )

        # Query similar bug reports
        results = collection.query(query_texts=[str(state.bug_report)], n_results=5)
        state.similar_bugs = results
        return state

    @staticmethod
    def code_healer(state: State) -> State:
        # Implement code healing logic here
        # This is where you would use the similar bugs to suggest fixes
        return state

    @staticmethod
    def code_updater(state: State):
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
        new_function_string = Nodes.llm.invoke([message]).content.strip()

        print("\n⚠️ Buggy Function")
        print("-------------------\n")
        print(state.function_string)
        print("\n💠 Proposed Bug Fix")
        print("-------------------\n")
        print(new_function_string)

        state.new_function_string = new_function_string
        return state

    @staticmethod
    def code_patcher(state: State):
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

    @staticmethod
    def memory_searcher(state: State):
        """Find memories relevant to the current bug report"""
        prompt = ChatPromptTemplate.from_template(
            "You are tasked with archiving a bug report for a Python function that raised an error."
            "Bug Report: {bug_report}."
            "Your response must be a concise string including only crucial information on the bug report for future reference."
            "Format: # function_name ## error_description ### error_analysis"
        )

        message = HumanMessage(content=prompt.format(bug_report=state.bug_report))
        response = Nodes.llm.invoke([message]).content.strip()
        results = Nodes.collection.query(query_texts=[response])

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

    @staticmethod
    def memory_filter(state: State):
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

    @staticmethod
    def memory_generator(state: State):
        """Condenses bug report and generates relevant memories before storing in ChromaDB Vector Database"""
        prompt = ChatPromptTemplate.from_template(
            "You are tasked with archiving a bug report for a Python function that raised an error."
            "Bug Report: {bug_report}."
            "Your response must be a concise string including only crucial information on the bug report for future reference."
            "Format: # function_name ## error_description ### error_analysis"
        )

        message = HumanMessage(content=prompt.format(bug_report=state.bug_report))
        response = Nodes.llm.invoke([message]).content.strip()

        print("\n💾 Saving Bug Report to Memory")
        print("------------------------------\n")
        print(response)

        id = str(uuid.uuid4())
        Nodes.collection.add(
            ids=[id],
            documents=[response],
        )

        return state

    @staticmethod
    def memory_modifier(state: State):
        """Update relevant memories with new interaction information"""
        prompt = ChatPromptTemplate.from_template(
            "Update the following memories based on the new interaction:"
            "Current Bug Report: {bug_report}"
            "Prior Bug Report: {memory_to_update}"
            "Your response must be a concise but cumulative string including only crucial information\
            on the current and prior bug reports for future reference."
            "Format: # function_name ## error_description ### error_analysis"
        )
        memory_to_update_id = state.memory_ids_to_update.pop(0)
        state.memory_search_results.pop(0)
        results = Nodes.collection.get(ids=[memory_to_update_id])
        memory_to_update = results["documents"][0]
        message = HumanMessage(
            content=prompt.format(
                bug_report=state.bug_report,
                memory_to_update=memory_to_update,
            )
        )

        response = Nodes.llm.invoke([message]).content.strip()

        print("\nCurrent Bug Report")
        print("-------------------\n")
        print(memory_to_update)
        print("\nWill be replaced with")
        print("-------------------\n")
        print(response)

        Nodes.collection.update(
            ids=[memory_to_update_id],
            documents=[response],
        )

        return state


class Edges:
    @staticmethod
    def has_error(state: State) -> bool:
        return state.error

    @staticmethod
    def no_error(state: State) -> bool:
        return not state.error

    def error_router(state: State):
        if state.error:
            return "bug_reporter"
        else:
            return END

    def memory_filter_router(state: State):
        if state.memory_search_results:
            return "memory_filter"
        else:
            return "memory_generator"

    def memory_generation_router(state: State):
        if state.memory_ids_to_update:
            return "memory_modifier"
        else:
            return "memory_generator"

    def memory_update_router(state: State):
        if state.memory_ids_to_update:
            return "memory_modifier"
        else:
            return "code_updater"
