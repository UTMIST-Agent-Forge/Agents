import pytest 
from langgraph.graph import StateGraph, START, END
from agents.models.edge_model import create_conditional_edges, create_parallel_edges
from agents.models.tool_node_model import Tool_Node
from agents.configs.llm_config import State, Message, Role


# random functions for testing
def f1(state: State) -> int:
    return {
        "messages" : state["messages"] + [Message(content="67", role=Role.ASSISTANT)] 
        if "messages" in state else 
        [Message(content="67", role=Role.ASSISTANT)]
    }


def f2(state: State) -> str:
    return "f1"


def f3(state: State) -> int:
    return {
        "other_state_attr" : state["other_state_attr"] + [Message(content="vincent", role=Role.ASSISTANT)] 
        if "other_state_attr" in state else 
        [Message(content="vincent", role=Role.ASSISTANT)]
    }


def graph_signature(g: StateGraph) -> dict[set, dict[str, str]]:
    '''
    Obtain graph signature (nodes and edges) from state graph
    '''
    edges = {}
    for src, dst in g.edges:
        edges.setdefault(src, set()).add(dst)

    return {
        "nodes": set(g.nodes.keys()),
        "edges": edges,
    }


def test_create_parallel_edge_mutation():
    ''' 
    Test that create_parallel_edge mutates the stategraph
    '''

    state_graph = StateGraph(State)
    state_graph.add_node("f1", f1)
    state_graph.add_edge("f1", END)
    state_graph.add_node("f3", f3)
    state_graph.add_edge("f3", END)

    create_parallel_edges(state_graph, START, ["f1", "f3"])

    compiled_graph = state_graph.compile()
    result = compiled_graph.invoke(State())
    assert result == {"messages" : [Message(content="67", role=Role.ASSISTANT)]}

    
def test_create_conditional_edges_mutation():
    ''' 
    Test that create_conditional_edges mutates the stategraph
    '''

    state_graph = StateGraph(State)
    state_graph.add_node("f1", f1)
    state_graph.add_edge("f1", END)

    # node params for routing node
    node_params = {
        "start": False,
        "finish": False,
        "leader": False,
        "id": "f2",
        "node_type": "tool_node",
        "is_subgraph": False,
        "is_checkpoint": False,
        "is_streaming": False,
        "name": "TestRoutingTool",
        "out_neighbours": [],
        "self_connection": {},
        "has_error_handling": False,
        "layer": 0,
        "independent_memory": False,
    }

    # routing node for conditional edge
    routing_node = Tool_Node(
        tool_description="tool that always routes to function f1, for testing",
        tool_args={},
        tool_func=f2,
        **node_params
    )
    
    create_conditional_edges(state_graph, START, routing_node)

    compiled_graph = state_graph.compile()
    result = compiled_graph.invoke(State())
    assert result == {"messages" : [Message(content="67", role=Role.ASSISTANT)]}