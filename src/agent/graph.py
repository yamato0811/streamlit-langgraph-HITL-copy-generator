from typing import Any, Callable, Dict, Union

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from agent.node import NodeType
from agent.state import State


class GraphBuilder:
    def __init__(self, state: State) -> None:
        self.work_flow: StateGraph = StateGraph(state)

    def add_node(self, node: NodeType) -> None:
        self.work_flow.add_node(node.name, node.func)

    def add_edge(self, from_node: NodeType, to_node: NodeType) -> None:
        self.work_flow.add_edge(from_node.name, to_node.name)

    def set_finish_point(self, end_node: NodeType) -> None:
        self.work_flow.set_finish_point(end_node.name)

    def set_entry_point(self, node: NodeType) -> None:
        self.work_flow.set_entry_point(node.name)

    def add_conditional_edges(
        self,
        from_node: NodeType,
        condition_func: Callable,
        path_map: Dict[str, Union[str, Any]],
    ) -> None:
        self.work_flow.add_conditional_edges(from_node.name, condition_func, path_map)

    def compile_flow(self) -> CompiledStateGraph:
        return self.work_flow.compile()
