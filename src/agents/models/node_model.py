from abc import ABC, abstractmethod
from typing import Any
from src.agents.config import State


class Node(ABC):
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

    @abstractmethod
    def update(self) -> None:
        '''
        Update the values within node
        '''

    @abstractmethod
    def get_metadata(self) -> dict:
        '''
        Get metadata for node
        '''

    @abstractmethod
    def execute(self, state: State) -> State:
        '''
        Execute the node
        '''

    @abstractmethod
    def error_handling(self, error: Any) -> Any | None:
        '''
        Handle errors
        '''

    @abstractmethod
    def save_to_memory(self, memory: Memory, state: State, save_long_term: bool) -> None:
        '''
        Save the state to memory
        '''
