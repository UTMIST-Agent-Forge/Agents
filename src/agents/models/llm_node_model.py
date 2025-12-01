from src.agents.models.node_model import Node
from typing import Any
from src.agents.configs.llm_config import State, StructuredOutput, ToolCalls, LLMConfig
from src.agents.services.llmNode.generateLLMResponse import generate_response

class LLM_Node(Node):
    '''
    Node model for LLM nodes
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
        tool_calls: ToolCalls | None = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stream = stream
        self.stop = stop
        self.structured_output = structured_output
        self.tool_calls = tool_calls

    def update(self) -> None:
        '''
        Update the values within node
        '''
        pass

    def get_metadata(self) -> dict:
        '''
        Get metadata for node
        '''
        return LLMConfig(
            model = self.model,
            provider = self.provider,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            stream = self.stream,
            stop = self.stop,
            structured_output = self.structured_output,
            tool_calls = self.tool_calls
        )

    def execute(self, state: State) -> Any:
        '''
        Execute the node
        '''
        config = LLMConfig(
            model = self.model,
            provider = self.provider,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            stream = self.stream,
            stop = self.stop,
            structured_output = self.structured_output,
            tool_calls = self.tool_calls
        )
        return generate_response(config, state)

    def error_handling(self, error: Any) -> Any | None:
        '''
        Handle errors
        '''
        pass

    def save_to_memory(self, memory, state: State, save_long_term: bool) -> None:
        '''
        Save the state to memory
        '''
        pass