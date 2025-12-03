from agents.models.node_model import Node
from langgraph.graph import StateGraph
from typing import Any
from agents.configs.llm_config import State


def create_parallel_edge(state_graph: StateGraph, start_node: str | Any, end_node: str | Any) -> None: #Any for START and END
    '''
    Create a parallel edge between two nodes in the state graph
    '''

    state_graph.add_edge(start_node, end_node) 


def create_conditional_edges(state_graph: StateGraph, start_node: str | Any, routing_node: Node) -> None:
    '''
    Create conditional edges between multiple nodes in the state graph
    '''

    state_graph.add_conditional_edges(start_node, routing_node.execute) #routing_node.execute should return which node to call next as a string