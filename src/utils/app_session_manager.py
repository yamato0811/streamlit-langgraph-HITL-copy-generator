from dataclasses import dataclass, field
from typing import List

import streamlit as st

from agent.agent import Agent
from models.llm import LLM


@dataclass
class SessionManager:
    """セッションの設定と状態を管理するデータクラス"""

    llm: LLM
    prompt: dict
    messages: List = field(default_factory=list)
    is_start: bool = False

    def __post_init__(self):
        """
        セッション状態の初期化（存在しない場合のみ）
        """
        if "agent" not in st.session_state:
            st.session_state.agent = Agent(self.llm, self.prompt)
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "is_start" not in st.session_state:
            st.session_state.is_start = False

    def get_agent(self) -> Agent:
        """Agentのインスタンスを取得"""
        return st.session_state.agent

    def get_messages(self) -> List:
        """メッセージリストを取得"""
        return st.session_state.messages
