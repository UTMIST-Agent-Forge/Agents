from pydantic import BaseModel, ValidationError
from typing import Any, TypedDict, Optional, Callable
from enum import Enum
from uuid import UUID

class ToolCall(BaseModel):
    '''
    '''
    function: Callable
    function_name: str
    function_description: str
    args_schema: Optional[BaseModel]


class ToolCalls(BaseModel):
    '''
    '''
    tool_calls: list[ToolCall]
    
class StructuredOutput(BaseModel):
    '''
    '''
    schema: dict[str, Any]
    title: str
    description: str

    
    
class Role(Enum):
    '''
    '''
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    
class Message(BaseModel):
    '''
    '''
    content: str
    role: Role
    
class ChatHistory(BaseModel):
    '''
    '''
    messages: list[Message]
    profile_id: str
    user_id: UUID
    thread_id: str

class State(TypedDict):
    '''
    '''
    messages: list[Message]


class LLMConfig(BaseModel):
    model: str
    provider: str
    temperature: float
    max_tokens: int
    top_p: float
    stream: bool | None = None,
    stop: str | list[str] | None = None,
    structured_output: StructuredOutput | None = None,
    tool_calls: ToolCalls | None = None,