import functools
from typing import Any, Callable, Dict, List

import streamlit as st
import yaml

from agent.agent import Agent
from agent.state import DisplayMessageDict
from utils.app_session_manager import SessionManager


def load_yaml(yaml_path: str) -> dict[str, Any]:
    """yamlファイルの読み込み"""
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)


def with_spinner(message: str = "Processing..."):
    """
    Streamlitのspinnerをデコレータとして実装するデコレータファクトリ

    Args:
        message (str): スピナー表示時のメッセージ

    Returns:
        Callable: デコレータ関数

    Usage:
        @with_spinner("データを処理中...")
        def stream_graph(agent: Agent, input: Dict | None, thread: Dict) -> None:
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                return func(*args, **kwargs)

        return wrapper

    return decorator


@with_spinner("Processing...")
def stream_graph(
    agent: Agent,
    input: Dict | None,
    thread: Dict,
    session_manager: SessionManager,
) -> None:
    """
    グラフのストリーミングを行う
    """
    events = agent.graph.stream(input, thread, stream_mode="values")
    for event in events:  # event is state in each node.
        # _ = event  # Ensure complete event consumption from iterator
        # get synchronized result. You should not get state
        # from thread before update completely.
        if display_message_dict := event.get("display_message_dict"):
            # 表示
            _display_message(display_message_dict)
            # messageの保存
            session_manager.save_message_to_session_state(display_message_dict)


def display_history(messages) -> None:
    """
    メッセージ履歴を表示する
    """
    for block in messages:
        title, icon, message = block
        with st.expander(title, expanded=True, icon=icon):
            st.markdown(message)


def _display_message(display_message_dict: DisplayMessageDict) -> None:
    """
    メッセージを表示する
    """
    with st.expander(
        display_message_dict["title"],
        expanded=True,
        icon=display_message_dict["icon"],
    ) as st.session_state.status:
        st.markdown(display_message_dict["message_text"])


def find_item_by_title(result_node: List[Dict], title: str) -> dict | None:
    """
    指定されたタイトルに一致する辞書をリストから検索する
    """
    return next(
        (result for result in result_node if result.get("title") == title), None
    )
