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
    try:
        # Try to get the source code
        try:
            function_string = inspect.getsource(function)
        except (TypeError, OSError):
            # If we can't get the source code, just execute the function directly
            return function(*arguments)

        state = State(
            error=False,
            function=function,
            function_string=function_string,
            arguments=arguments,
        )

        return graph.invoke(state)
    except Exception as e:
        # If anything goes wrong, fall back to direct execution
        return function(*arguments)
