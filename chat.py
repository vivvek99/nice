from copy import deepcopy
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.docstore.document import Document
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

import config
from index import load_vector_store

import promptlayer
promptlayer.api_key = "pl_2b1769e7202b6a141d4491fca41e308a"


def clear_input() -> None:
    st.session_state["input"] = deepcopy(st.session_state["temp"])
    st.session_state["input_disabled"] = True
    st.session_state["temp"] = ""


def get_input() -> str:
    st.text_area(
        label="You: ",
        value="",
        placeholder=("Type here, send with Cmd+Enter"
                     if not st.session_state.input_disabled else "Getting response...\nRefresh the page if stuck for >10s"),
        label_visibility="hidden",
        key="temp",
        on_change=clear_input,
        # disabled=st.session_state.input_disabled,
    )
    return st.session_state["input"]


def get_response(query: str) -> str:
    try:
        chain = get_chain()
        response = chain({"input_documents": get_documents(query), "human_input": query}, return_only_outputs=True)
        return response.get("output_text").strip()
    except Exception as e:
        print(f"Get response error: {e}")
        return "Connection error. Please try again later."


def get_chain():
    if "chain" not in st.session_state:
        st.session_state["chain"] = load_qa_chain(
            llm=PromptLayerChatOpenAI(
                pl_tags=["chat-nice-st"],
                temperature=0,
                model_name=config.MODEL_NAME,
                max_tokens=512,
                request_timeout=int(180)
            ),
            chain_type="stuff",
            memory=get_memory(),
            prompt=get_prompt()
        )
    return st.session_state["chain"]

def get_memory() -> ConversationSummaryBufferMemory:
    if "memory" not in st.session_state:
        st.session_state["memory"] = new_memory()
    return st.session_state["memory"]


def new_memory() -> ConversationSummaryBufferMemory:
    llm = PromptLayerChatOpenAI(pl_tags=["chat-nice-st-memory"], model_name=config.MODEL_NAME, request_timeout=int(180))
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        input_key="human_input"
    )
    return memory

def get_prompt() -> PromptTemplate:
    with open(config.PROMPT_PATH, "r") as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"],
        template=template
    )
    return prompt


def get_documents(query: str) -> list[Document]:
    docsearch = get_docsearch()
    return docsearch.similarity_search(query)


def get_docsearch() -> Chroma:
    if "docsearch" not in st.session_state:
        st.session_state["docsearch"] = load_vector_store()
    return st.session_state["docsearch"]