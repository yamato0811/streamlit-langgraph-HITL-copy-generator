import streamlit as st

from agent.agent import Agent
from utils.app_util import find_item_by_title


def select_item(
    agent: Agent,
    thread: dict,
    state_key: str,
    selectbox_message: str,
    state_update_key: str,
    as_node: str,
) -> None:
    """
    項目選択関数

    Args:
        agent (Agent): エージェントオブジェクト
        thread (dict): 現在のスレッドの辞書
        state_key (str): ステートから取得する項目のキー
        selectbox_message (str): セレクトボックスのメッセージ
        state_update_key (str): ステートを更新する際のキー
        as_node (str): ステート更新ノード名
    """
    items = agent.get_state_value(thread, state_key)

    # セレクトボックスのオプション作成
    select_options = [item["title"] for item in items]
    select_options.append("再検討を依頼する")

    selected = st.selectbox(
        selectbox_message,
        select_options,
        key=f"{as_node}_select_{agent.get_state_value(thread, 'iteration_count')}",
    )

    if not st.button(
        "次へ",
        type="primary",
        key=f"{as_node}_button_{agent.get_state_value(thread, 'iteration_count')}",
    ):
        print("User Input Stop")
        st.stop()  # この時点で処理が停止

    print("Entered User Input: ", selected)

    if selected == "再検討を依頼する":
        agent.graph.update_state(
            thread,
            {
                state_update_key: None,
                "display_message_dict": None,
                "is_rethink": True,
            },
            as_node=as_node,
        )
    else:
        selected_item = find_item_by_title(items, selected)
        agent.graph.update_state(
            thread,
            {
                state_update_key: selected_item,
                "display_message_dict": None,
                "is_rethink": False,
            },
            as_node=as_node,
        )


def input_additional_info(agent: Agent, thread: dict, as_node: str) -> None:
    """
    追加情報入力関数。

    Args:
        agent (Agent): エージェントオブジェクト
        thread (dict): 現在のスレッドの辞書
        as_node (str): ステート更新ノード名
    """
    additional_info = agent.get_state_value(thread, "additional_info")

    # ユーザー情報入力
    additional_info_input = st.text_input(f"「{additional_info}」を入力してください")

    if not st.button(
        "次へ",
        type="primary",
        disabled=not bool(additional_info_input),
        key=as_node,
    ):
        print("User Input Stop")
        st.stop()  # この時点で処理が停止

    print("Entered User Input: ", additional_info_input)

    agent.graph.update_state(
        thread,
        {
            "additional_info_input": additional_info_input,
            "display_message_dict": None,
        },
        as_node=as_node,
    )
