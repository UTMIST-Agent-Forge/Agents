from agents.models.node_model import Node
from agents.configs.llm_config import State
from agents.configs.tool_config import ToolConfig
from typing import Any
from collections.abc import Callable


class Tool_Node(Node):
    '''
    Node model for Tool nodes
    '''

    def __init__(
        self, 
        tool_description: str | None = None,
        tool_args: dict[str, Any] | None = None,
        tool_func: Callable[..., Any] | None = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.tool_description = tool_description
        self.tool_args = tool_args
        self.tool_func = tool_func

    def get_metadata(self) -> dict:
        '''
        Get metadata for node
        '''
        return ToolConfig(
            tool_description = self.tool_description,
            tool_args = self.tool_args,
            tool_func = self.tool_func
        )

    def execute(self, state: State) -> Any:
        '''
        Execute the node
        '''
        return self.tool_func(state)

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