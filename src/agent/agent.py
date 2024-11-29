from typing import Any, Dict, Union

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.memory import MemorySaver

from agent.graph import GraphBuilder
from agent.node import Node
from agent.state import State
from models.llm import LLM


class Agent:
    def __init__(
        self,
        llm: LLM,
        prompt: Dict[str, Dict[str, str]],
    ) -> None:
        # ================
        # Graph
        # ================
        graph_builder = GraphBuilder(State)

        # Create Node
        self.node = Node(llm, prompt)

        # Add nodes (generate copy)
        graph_builder.add_node(self.node.generate_copy)
        graph_builder.add_node(self.node.user_select_copy)
        graph_builder.add_node(self.node.reflect_copy)
        graph_builder.add_node(self.node.user_input_additioal_info_copy)
        graph_builder.add_node(self.node.end)

        # Add edges (generate copy)
        graph_builder.add_edge(self.node.generate_copy, self.node.user_select_copy)
        graph_builder.add_conditional_edges(
            self.node.user_select_copy,
            self.node.should_rethink,
            {
                "reflect": self.node.reflect_copy.name,
                "next_step": self.node.end.name,
            },
        )
        graph_builder.add_edge(
            self.node.reflect_copy, self.node.user_input_additioal_info_copy
        )
        graph_builder.add_edge(
            self.node.user_input_additioal_info_copy, self.node.generate_copy
        )

        # Set entry and finish point
        graph_builder.set_entry_point(self.node.generate_copy)
        graph_builder.set_finish_point(self.node.end)

        # Set up memory
        self.memory = MemorySaver()

        self.graph = graph_builder.work_flow.compile(
            checkpointer=self.memory,
            interrupt_before=[
                self.node.user_select_copy.name,
                self.node.user_input_additioal_info_copy.name,
            ],
        )

        # Mermaidコードをファイルに書き出し
        with open("graph.md", "w") as file:
            file.write(f"```mermaid\n{self.graph.get_graph().draw_mermaid()}```")

    # ================
    # Helper
    # ================
    def is_start_node(self, thread: dict) -> bool:
        return self.graph.get_state(thread).created_at is None

    def is_end_node(self, thread: dict) -> bool:
        return self.get_state_value(thread, "is_finish")

    def get_next_node(self, thread: dict) -> tuple[str, ...]:
        return self.graph.get_state(thread).next

    def get_state_value(
        self, thread: dict, name: str
    ) -> Union[dict[str, Any], Any, None]:
        state = self.graph.get_state(thread)
        if state and name in state.values:
            return state.values.get(name)
        return None
