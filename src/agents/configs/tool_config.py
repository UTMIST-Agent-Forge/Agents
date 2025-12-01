from pydantic import BaseModel, ValidationError
from typing import Any, TypedDict, Optional, Callable

class ToolConfig(BaseModel):
    tool_name: str
    tool_description: str
    tool_args: dict[str, Any]
    tool_func: Callable[..., Any]