import os
import streamlit as st
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="") -> None:
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


def print_msg(session_id: str):
    history = get_session_history(session_id)
    for message in history.messages:
        if isinstance(message, HumanMessage):
            role = "human"
        elif isinstance(message, AIMessage):
            role = "assistant"
        st.chat_message(role).write(message.content)


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, os.environ["REDIS_URL"])


def refresh_msg(session_id):
    get_session_history(session_id).clear()
