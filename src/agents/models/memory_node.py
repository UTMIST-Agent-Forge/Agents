from src.agents.models.node_model import Node
from src.agents.configs.llm_config import State
from src.models.memory import Memory
from typing import Any, override

class MemoryNode(Node):
    '''
    Memory node for managing short-term and long-term memory operations
    '''

    def __init__(
        self,
        # Node base parameters
        start: bool,
        finish: bool,
        leader: bool,
        id: str,
        node_type: str,
        is_subgraph: bool,
        is_checkpoint: bool,
        is_streaming: bool,
        name: str,
        out_neighbours: list[str],
        self_connection: dict[str, Any] | list[Any] | str | int | float | bool | None,
        has_error_handlng: bool,
        layer: int,
        independent_memory: bool,
        # Memory-specific parameters
        checkpoints: dict[str, Any] | None = None,
        checkpoint_config: dict[str, Any] | None = None,
        subgraphs_list: list[str] | None = None,
        short_term_memory: dict[str, Any] | None = None,
        long_term_memory: Any | None = None,  # InStoreMemory object
        db_key: str | None = None,  # secret_str
        log_to_longterm_preference: dict[str, Any] | None = None,
        truncate_message_history_preference: dict[str, Any] | None = None
    ) -> None:
        '''
        Initialize Memory_Node with base Node parameters and memory-specific attributes
        '''
        super().__init__(
            start=start,
            finish=finish,
            leader=leader,
            id=id,
            node_type=node_type,
            is_subgraph=is_subgraph,
            is_checkpoint=is_checkpoint,
            is_streaming=is_streaming,
            name=name,
            out_neighbours=out_neighbours,
            self_connection=self_connection,
            has_error_handlng=has_error_handlng,
            layer=layer,
            independent_memory=independent_memory
        )
        self.checkpoints = checkpoints or {}
        self.checkpoint_config = checkpoint_config or {}
        self.subgraphs_list = subgraphs_list or []
        self.short_term_memory = short_term_memory or {}
        self.long_term_memory = long_term_memory
        self.db_key = db_key
        self.log_to_longterm_preference = log_to_longterm_preference or {}
        self.truncate_message_history_preference = truncate_message_history_preference or {}

    # Abstract method implementations from Node
    @override
    def update(self) -> None:
        '''
        Update the values within node
        '''
        pass

    @override
    def get_metadata(self) -> dict:
        '''
        Get metadata for node
        '''
        pass

    @override
    def execute(self, state: State) -> State:
        '''
        Execute the node
        '''
        pass

    @override
    def error_handling(self, error: Any) -> Any | None:
        '''
        Handle errors
        '''
        pass

    @override
    def save_to_memory(self, memory: Memory, state: State, save_long_term: bool) -> None:
        '''
        Save the state to memory
        '''
        pass

    # Memory-specific operations
    def write_to_long_term(self, key: str, schema: dict[str, Any]) -> None:
        '''
        Write data to long-term memory
        '''
        pass

    def read_from_long_term(self, key: str) -> None:
        '''
        Read data from long-term memory
        '''
        pass

    def semantic_search_from_long_term(self, key: str, query: str, k: int) -> None:
        '''
        Perform semantic search in long-term memory
        '''
        pass

    def trim(self, key: str, trim_kwargs: dict[str, Any]) -> None:
        '''
        Trim memory entries
        '''
        pass

    def delete(self, key: str) -> None:
        '''
        Delete memory entries
        '''
        pass

    def summarize(self, key: str) -> None:
        '''
        Summarize memory entries
        '''
        pass

    def write_to_short_term(self, key: str, text: str) -> None:
        '''
        Write data to short-term memory
        '''
        pass

    def inject_context(self, key: str, text: str) -> None:
        '''
        Inject context into memory
        '''
        pass
