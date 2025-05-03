from src.core.state import State
from src.core.build import graph
import inspect


def execute_self_healing_code_system(function, arguments):
    """
    Execute a function with the self-healing code system.

    Args:
        function: The function to execute
        arguments: Arguments to pass to the function

    Returns:
        The result of the function execution after any necessary healing
    """
    state = State(
        error=False,
        function=function,
        function_string=inspect.getsource(function),
        arguments=arguments,
    )

    return graph.invoke(state)
