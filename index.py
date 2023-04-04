import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.chains import LLMChain, HypotheticalDocumentEmbedder
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
import pinecone
import promptlayer

@st.cache_resource
def load_vector_store() -> Pinecone:
    print("Loading vector store...")
    # initialize pinecone
    pinecone.init(
        api_key="25db0a5b-ee2d-4d5e-86ba-5bce9cd90804",  # find at app.pinecone.io
        environment="us-east1-gcp"  # next to api key in console
    )
    base_embeddings = OpenAIEmbeddings()
    promptlayer.api_key = "pl_2b1769e7202b6a141d4491fca41e308a"
    llm = PromptLayerChatOpenAI(pl_tags=["chat-nice-st-embeddings"])
    prompt_template = """Please answer the user's question concisely using medical language. If in doubt mention multiple possible answers. Consider chat history if provided.
    {question}"""
    prompt = PromptTemplate(input_variables=["question"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    hydeembeddings = HypotheticalDocumentEmbedder(llm_chain=llm_chain, base_embeddings=base_embeddings)
    docsearch = Pinecone.from_existing_index(index_name="cks-summary-1500tiktoken", namespace="full-cks-1200", embedding = hydeembeddings)
    print("Loaded vector store")
    return docsearch