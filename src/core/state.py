from pydantic import BaseModel
from typing import Callable

class State(BaseModel):
    function: Callable
    function_string: str
    arguments: list
    error: bool
    error_description: str = ""
    new_function_string: str = ""
    bug_report: str = ""
    memory_search_results: list = []
    memory_ids_to_update: list = []
