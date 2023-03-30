import os

import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import config


@st.cache_data
def create_index():
    if os.getenv("TEST", None):
        print("Testing mode, skipping the creation of the index")
        return
    print("Checking if index exists...")
    if os.path.exists(config.INDEX_PATH) and os.path.isdir(config.INDEX_PATH) and os.listdir(config.INDEX_PATH):
        print("Index already exists, skipping the creation")
        return


@st.cache_resource
def load_vector_store() -> Chroma:
    print("Loading vector store...")
    docsearch = Chroma(persist_directory=config.INDEX_PATH, embedding_function=OpenAIEmbeddings())
    print("Loaded vector store")
    return docsearch