from typing import Any, TypedDict
from langchain.messages import BaseMessage


class State(TypedDict):
    '''
    '''


class Memory:
    '''
    '''

    def __init__(self) -> None:
        pass


class Node:
    '''
    '''

    def __init__(self, start: bool, finish: bool, leader: bool, id: str, node_type: str, is_subgraph: bool, is_checkpoint: bool, is_streaming: bool, name: str, out_neighbours: list[str], self_connection: dict[str, Any] | list[Any] | str | int | float | bool | None, has_error_handlng: bool, layer: int, independent_memory: bool) -> None:
        '''
        '''
        self.start = start
        self.finish = finish
        self.leader = leader
        self.id = id
        self.node_type = node_type
        self.is_subgraph = is_subgraph
        self.is_checkpoint = is_checkpoint
        self.is_streaming = is_streaming
        self.name = name
        self.out_neighbours = out_neighbours
        self.self_connection = self_connection
        self.has_error_handlng = has_error_handlng
        self.layer = layer
        self.independent_memory = independent_memory

    def update() -> None:
        '''
        '''
        pass

    def get_metadata() -> dict:
        '''
        '''
        pass

    def execute(state: State) -> State:
        '''
        '''
        pass

    def error_handling(error: Any) -> Any | None:
        '''
        '''
        pass

    def save_to_memory(memory: Memory, state: TypedDict, save_long_term: bool) -> None:
        '''
        '''
        pass


class LLM:
    '''
    '''

    def __init__(self, id: str, model: str, provider: str, config: dict[str, Any] | list[Any] | str | int | float | bool, structured_output: dict[str, Any] | list[Any] | str | int | float | bool | None, include_history: bool):
        '''
        '''
        self.id = id
        self.model = model
        self.provider = provider
        self.config = config
        self.structured_output = structured_output
        self.include_history = include_history

    def ainvoke(msgs: State) -> str:
        '''
        '''

    def astream(msgs: State) -> Any:
        '''
        '''


class LLM_Node(Node):
    '''
    '''

    def __init__(self, id: str, model: str, provider: str, config: dict[str, Any] | list[Any] | str | int | float | bool, structured_output: dict[str, Any] | list[Any] | str | int | float | bool | None, include_history: bool, use_long_term_memory: bool, system_prompt: str, memory_type: str):
        '''
        '''
        super().__init__(start=False, finish=False, leader=False, id=id, node_type="LLM", is_subgraph=False, is_checkpoint=False, is_streaming=False, name="", out_neighbours=[], self_connection=None, has_error_handlng=False, layer=0, independent_memory=False)
        self.llm_object = LLM(id, model, provider, config, structured_output, include_history)
        self.use_long_term_memory = use_long_term_memory
        self.system_prompt = system_prompt
        self.memory_type = memory_type
