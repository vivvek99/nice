from copy import deepcopy
import streamlit as st
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.docstore.document import Document
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

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
        disabled=st.session_state.input_disabled,
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

@st.cache_resource
def get_chain():
    chain = load_qa_with_sources_chain(
        llm=PromptLayerChatOpenAI(
            pl_tags=["chat-nice-st"],
            temperature=0,
            model_name=config.MODEL_NAME,
            max_tokens=600,
            request_timeout=int(180)
        ),
        chain_type="stuff",
        memory=ConversationSummaryBufferMemory(
            llm=PromptLayerChatOpenAI(pl_tags=["chat-nice-st-memory"], model_name=config.MODEL_NAME, request_timeout=int(180)),
            max_token_limit=128,
            memory_key="chat_history",
            input_key="human_input"
        ),
        prompt=get_prompt()
    )
    return chain

def get_prompt() -> ChatPromptTemplate:
    with open(config.CHAT_SYS_PROMPT_PATH, "r") as f:
        systemplate = f.read()
    humtemplate = """Answer the following question. Be informal and fun, but use medical terminology. I shall give you the contexts and conversation history (if any). Ready?"""
    aitemplate = """Please provide me with the medical contexts and conversation history (if any). 😊"""
    with open(config.CHAT_HUM_PROMPT_PATH, "r") as f:
        humtemplate2 = f.read()
    system_message_prompt = SystemMessagePromptTemplate.from_template(systemplate)
    human_message_prompt = HumanMessagePromptTemplate.from_template(humtemplate)
    ai_message_prompt = AIMessagePromptTemplate.from_template(aitemplate)
    human_message_prompt2 = HumanMessagePromptTemplate.from_template(humtemplate2)
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt, ai_message_prompt, human_message_prompt2])
    return prompt

def get_documents(query: str) -> list[Document]:
    docsearch = get_docsearch()
    retriever = docsearch.as_retriever()
    if "ai" in st.session_state:
        last_resp = str(st.session_state["ai"][-1:])
        fquery = last_resp+query
    else:
        fquery = query
    return retriever.get_relevant_documents(fquery)

def get_docsearch() -> Chroma:
    if "docsearch" not in st.session_state:
        st.session_state["docsearch"] = load_vector_store()
    return st.session_state["docsearch"]