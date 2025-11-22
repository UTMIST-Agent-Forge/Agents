from src.agents.models.node_model import Node
from typing import Any
from src.agents.configs.llm_config import State, StructuredOutput, ToolCalls

class LLM_Node(Node):
    '''
    '''

    def __init__(
        self, 
        model: str | None = None,
        provider: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stream: bool | None = None,
        stop: str | list[str] | None = None,
        structured_output: StructuredOutput | None = None,
        tool_calls: ToolCalls | None = None
    ):
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stream = stream
        self.stop = stop
        self.structured_output = structured_output
        self.tool_calls = tool_calls

        