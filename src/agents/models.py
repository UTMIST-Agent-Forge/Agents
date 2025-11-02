#TODO add docstrings

from typing import Any, TypedDict

from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import init_chat_model


class State(TypedDict):
    '''
    '''
    #TODO define state structure


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

    def __init__(self, id: str, model: str, config: dict[str, Any] | list[Any] | str | int | float | bool, structured_output: dict[str, Any] | list[Any] | str | int | float | bool | None, include_history: bool):
        '''
        '''
        self.id = id
        self.model = model 
        self.config = config
        self.structured_output = structured_output
        self.include_history = include_history
        #TODO add api key
        self.llm_model = init_chat_model(model=model, api_key="")

    def ainvoke(self, msgs: State) -> str:
        '''
        '''
        return self.llm_model.invoke(msgs.)

    def astream(self, msgs: State) -> Any:
        '''
        '''
        for chunk in self.llm_model.stream(
            {"messages": msgs.}
            stream_mode = "messages"
        ):
            yield chunk
        


class LLM_Node(Node):
    '''
    '''

    def __init__(self, id: str, model: str, provider: str, config: dict[str, Any] | list[Any] | str | int | float | bool, structured_output: dict[str, Any] | list[Any] | str | int | float | bool | None, include_history: bool, use_long_term_memory: bool, system_prompt: str, memory_type: str):
        '''
        '''
        super().__init__(start=False, finish=False, leader=False, id=id, node_type="LLM", is_subgraph=False, is_checkpoint=False, is_streaming=False, name="", out_neighbours=[], self_connection=None, has_error_handlng=False, layer=0, independent_memory=False)
        self.llm_object = LLM(id=id, model=model, config=config, structured_output=structured_output, include_history=include_history)
        self.use_long_term_memory = use_long_term_memory
        self.system_prompt = system_prompt
        self.memory_type = memory_type


# questions:
# why is provider necessary for LLM?
# why arent the params for LLM functions just state
# did i miss anything in the state object? 
# are we just having one catch-all state object?
# how to make vscode recognize dependencies?
# are invoke and stream supposed to be async functions?