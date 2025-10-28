from typing_extensions import TypedDict
from typing import Any


class node:
    '''
    '''

    def __init__(self, start: bool, finish: bool, leader: bool, id: str, node_type: str, is_subgraph: bool, is_checkpoint: bool, is_streaming: bool, state: TypedDict, name: str, out_neighbours: list[str], self_connection: dict[str, Any] | list[Any] | str | int | float | bool | None, has_error_handlng: bool, layer: int, independent_memory: bool) -> None:
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
        self.state = state
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