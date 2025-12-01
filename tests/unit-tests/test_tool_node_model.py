import pytest 
from agents.models.tool_node_model import Tool_Node
from agents.configs.llm_config import State


# random functions for testing
def f1(state: State) -> str:
    return "vincent"


def test_tool_node_init():
    ''' 
    Test that tool_node correctly initializes required attributes
    '''

    # node parameters for tool_node
    node_params = {
        "start": False,
        "finish": False,
        "leader": False,
        "id": "f1",
        "node_type": "tool_node",
        "is_subgraph": False,
        "is_checkpoint": False,
        "is_streaming": False,
        "name": "TestToolNodeTool",
        "out_neighbours": [],
        "self_connection": {},
        "has_error_handling": False,
        "layer": 0,
        "independent_memory": False,
    }

    node = Tool_Node(
        tool_description="A tool for testing ToolNode",
        tool_args={},
        tool_func=f1,
        **node_params
    )

    # check Tool_Node specific attributes
    assert node.tool_description == "A tool for testing ToolNode"
    assert node.tool_args == {}
    assert node.tool_func is f1

    # check Node parent attributes
    for key, value in node_params.items():
        assert getattr(node, key) == value


def test_tool_node_execute():
    ''' 
    Test that tool_node correctly executes tool function
    '''

    # node parameters for tool node
    node_params = {
        "start": False,
        "finish": False,
        "leader": False,
        "id": "f1",
        "node_type": "tool_node",
        "is_subgraph": False,
        "is_checkpoint": False,
        "is_streaming": False,
        "name": "TestToolNodeTool",
        "out_neighbours": [],
        "self_connection": {},
        "has_error_handling": False,
        "layer": 0,
        "independent_memory": False,
    }

    node = Tool_Node(
        tool_description="A tool for testing ToolNode",
        tool_args={},
        tool_func=f1,
        **node_params
    )

    assert node.execute(State()) == "vincent"