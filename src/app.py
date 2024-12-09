from typing import Any, Dict

import streamlit as st
from dotenv import load_dotenv

from components.input_form import input_form
from models.llm import LLM
from utils.app_session_manager import SessionManager
from utils.app_user_input_logic import input_additional_info, select_item
from utils.app_util import display_history, load_yaml, stream_graph

load_dotenv()

MODEL = "claude-3-5"  # specify "gpt-4o" or "claude-3-5"
THREAD_ID = "1"
PROMPT_PATH = "agent/prompt/prompt_templates.yaml"
TEMPERATURE = 1.0


def main() -> None:
    # ================
    # Page Config
    # ================
    st.set_page_config(
        page_title="Streamlit×LangGraph コピー生成",
        page_icon="🤖",
        initial_sidebar_state="auto",
    )
    st.title("Streamlit×LangGraph コピー生成")

    # ================
    # Init Actor
    # ================
    llm = LLM(MODEL, TEMPERATURE)
    prompt: Dict[str, Dict[str, str]] = load_yaml(PROMPT_PATH)

    # ================
    # Streamlit Session State
    # ================
    session_manager = SessionManager(llm=llm, prompt=prompt)
    agent = session_manager.get_agent()

    # ================
    # Input
    # ================
    product_info = input_form()

    # ================
    # Display
    # ================
    display_history(session_manager.get_messages())

    # ================
    # Core Algorithm
    # ================
    thread = {"configurable": {"thread_id": THREAD_ID}}
    initial_input = {
        "product_info": product_info,
        "iteration_count": 0,
        "is_finish": False,
        "display_message_dict": None,
        "messages": [],
        "additional_info_input": "",
    }

    while True:
        # 開始ノードの場合
        if agent.is_start_node(thread):
            # グラフの実行
            stream_graph(agent, initial_input, thread, session_manager)

        # 次のノードがある場合
        next_graph: tuple[str, ...] | Any = agent.get_next_node(thread)
        if next_graph:
            if next_graph[0] == agent.node.user_select_copy.name:
                select_item(
                    agent=agent,
                    thread=thread,
                    state_key="copies",
                    selectbox_message="お気に入りのキャッチコピーを選択してください",
                    state_update_key="selected_copy",
                    as_node=next_graph[0],
                )
            elif next_graph[0] == agent.node.user_input_additioal_info_copy.name:
                input_additional_info(
                    agent=agent,
                    thread=thread,
                    as_node=next_graph[0],
                )

            # グラフの実行
            stream_graph(agent, None, thread, session_manager)

        # 終了ノードの場合
        if agent.is_end_node(thread):
            selected_copy = agent.get_state_value(thread, "selected_copy")
            st.success(f'生成したコピー: {selected_copy["copy_text"]}')
            break


if __name__ == "__main__":
    main()
