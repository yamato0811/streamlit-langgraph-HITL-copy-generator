from dataclasses import dataclass
from typing import Callable, Dict, Literal

from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate

from agent.output_structure import Copies, ReflectDetails
from agent.state import State
from models.llm import LLM
from utils.node_util import filter_key_from_list, get_output_format_instructions


@dataclass
class NodeType:
    name: str  # ノードの名前
    func: Callable  # ノードで実行する関数


class Node:
    def __init__(
        self,
        llm: LLM,
        prompt: Dict[str, Dict[str, str]],
    ) -> None:

        self.llm = llm
        self.prompt = prompt

        # ================
        # Define Node
        # ================
        self.generate_copy = NodeType("generate_copy", self._generate_copy)
        self.user_select_copy = NodeType("user_select_copy", self._user_input)
        self.reflect_copy = NodeType("reflect_copy", self._reflect_copy)
        self.user_input_additioal_info_copy = NodeType(
            "user_input_additioal_info_copy", self._user_input
        )
        self.end = NodeType("dummy_end", self._end_node)

    # ================
    # Node Functions
    # ================
    def _start_node(self, state: State):
        print("Node: start_node")

    def _generate_copy(self, state: State) -> State:
        print("Node: generate_copy")

        product_info = state["product_info"]

        # 初回コンテンツ生成
        if state["iteration_count"] == 0:
            system_prompt = SystemMessage(
                content=self.prompt["generate_copy"]["system"]
            )
            human_prompt = HumanMessagePromptTemplate.from_template(
                self.prompt["generate_copy"]["user_first"]
            ).format(
                product_info=product_info,
                output_format_instruction=get_output_format_instructions(Copies),
            )

            state["messages"] = [system_prompt, human_prompt]
        else:
            human_prompt = HumanMessagePromptTemplate.from_template(
                self.prompt["generate_copy"]["user_second"]
            ).format(
                product_info=product_info,
                additional_info=state["additional_info"],
                additional_info_input=state["additional_info_input"],
                output_format_instruction=get_output_format_instructions(Copies),
                state=state,
            )

        state["messages"].append(human_prompt)

        # invoke
        ai_message = self.llm((state["messages"]), Copies)
        state["messages"].append(AIMessage(ai_message.model_dump_json()))

        output_list = ai_message.model_dump()["copies"]

        # streamlit表示用のメッセージ
        message_text = ""
        for output in output_list:
            # avoid to break markdown format
            output["copy_text"] = output["copy_text"].replace("\n", "")
            # markdown改行のため空白スペースが2つ必要
            message_text += f"""
        **【{output["title"]}】**\u0020\u0020
        **キャッチコピー**：{output["copy_text"]}\u0020\u0020
        **理由**：{output["reason"]}
        """
        display_message_dict = {
            "title": f"**キャッチコピーの作成** {state['iteration_count'] + 1}回目",
            "icon": "📝",
            "message_text": message_text,
        }

        # 'reason'キーのみを削除した新しいリストを生成
        filtered_list = filter_key_from_list(output_list, "reason")

        # 状態の更新
        state["copies"] = filtered_list
        state["display_message_dict"] = display_message_dict

        return state

    def _reflect_copy(self, state: State) -> State:
        print("Node: reflect_copy")

        copies = state["copies"]

        human_prompt = HumanMessagePromptTemplate.from_template(
            self.prompt["reflect_copy"]["user"]
        ).format(
            copies=copies,
            output_format_instruction=get_output_format_instructions(ReflectDetails),
        )

        state["messages"].append(human_prompt)

        # invoke
        ai_message = self.llm((state["messages"]), ReflectDetails)
        state["messages"].append(AIMessage(ai_message.model_dump_json()))

        # 文字列をPythonの辞書に変換
        data = ai_message.model_dump()

        display_message_dict = {
            "title": f"**キャッチコピーの改善** {state['iteration_count'] + 1}回目",
            "icon": "🔄",
            "message_text": f"""
            **改善点**：{data["improvement_point"]}\u0020\u0020
            **必要な追加情報**：{data["additional_info"]}\u0020\u0020
            **理由**：{data["reason"]}
            """,
        }

        # 状態の更新
        state["additional_info"] = data["additional_info"]
        state["display_message_dict"] = display_message_dict

        # カウントアップ
        state["iteration_count"] += 1

        return state

    def _user_input(self, state: State):
        pass

    def _end_node(self, state: State):
        print("Node: end_node")
        return {"is_finish": True, "display_message_dict": None}

    # ================
    # Conditional Functions
    # ================
    def should_rethink(self, state: State) -> Literal["reflect", "end"]:
        if state["is_rethink"]:
            return "reflect"
        else:
            return "end"
