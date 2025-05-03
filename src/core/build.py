from langgraph.prebuilt import ToolExecutor
from langgraph.graph import Graph, END
from src.core.graph import Nodes, Edges

# Create the graph
graph = Graph()

# Add nodes
graph.add_node("code_executor", Nodes.code_executor)
graph.add_node("error_detector", Nodes.error_detector)
graph.add_node("bug_reporter", Nodes.bug_reporter)
graph.add_node("memory_manager", Nodes.memory_manager)
graph.add_node("code_healer", Nodes.code_healer)

# Set entry point
graph.set_entry_point("code_executor")

# Add edges
graph.add_edge("code_executor", "error_detector")
graph.add_edge("error_detector", "bug_reporter")
graph.add_edge("bug_reporter", "memory_manager")
graph.add_edge("memory_manager", "code_healer")
graph.add_edge("code_healer", "code_executor")

# Add conditional edges
graph.add_conditional_edges(
    "error_detector", lambda x: "bug_reporter" if x.error else END
)

# Compile the graph
graph = graph.compile()
