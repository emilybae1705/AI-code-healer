from dataclasses import dataclass
from typing import Any, List, Dict, Optional, Callable


@dataclass
class State:
    error: bool
    function: Callable
    function_string: str
    arguments: List[Any]
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    result: Optional[Any] = None
    bug_report: Optional[Dict[str, Any]] = None
    similar_bugs: Optional[List[Dict[str, Any]]] = None
