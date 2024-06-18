from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import get_session_history, print_msg, StreamingHandler, refresh_msg
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

st.set_page_config(page_title="ChatLlama", page_icon="🚀")
st.title("🚀 ChatLlama")

if "store" not in st.session_state:
    st.session_state["store"] = dict()

with st.sidebar:
    session_id = st.text_input("Session ID", placeholder="Enter Session ID")
    if st.button("reload"):
        refresh_msg(session_id)

# 현재 세션의 대화 기록 출력
print_msg(session_id)


if user_input := st.chat_input("메세지를 입력해주세요."):
    # 사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")

    # AI 답변
    with st.chat_message("assistant"):
        stream_handler = StreamingHandler(st.empty())
        # LLM 정의
        llm = HuggingFaceEndpoint(
            repo_id=os.environ["MODEL_ID"],
            max_new_tokens=2048,
            temperature=0.1,
            stop_sequences=[
                "<|eot_id|>"
            ],  # stop token을 넣어줘야 답변에서 해당 토큰이 포함되지 않음
        )
        model = ChatHuggingFace(llm=llm, streaming=True, callbacks=[stream_handler])

        # system, history, 그리고 사용자의 질문을 prompt 구성
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "질문에 짧고 간결하게 대답해주세요."),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
        )
        chain = prompt | model

        chain_with_memory = RunnableWithMessageHistory(
            chain,
            get_session_history,  # BaseChatMessageHistory 객체를 반환하는 callable 함수
            input_messages_key="question",
            history_messages_key="history",
        )

        chain_with_memory.invoke(
            {"question": user_input},
            # session id 설정
            config={"configurable": {"session_id": session_id}},
        )
        # st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))
