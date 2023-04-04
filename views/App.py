"""Python file to serve as the frontend"""
import streamlit as st
import csv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.chains import HypotheticalDocumentEmbedder

def createPage():
    @st.cache_resource
    def load_vectorstore():
        # initialize pinecone
        pinecone.init(
            api_key="25db0a5b-ee2d-4d5e-86ba-5bce9cd90804",  # find at app.pinecone.io
            environment="us-east1-gcp"  # next to api key in console
        )
        vectorstore = Pinecone.from_existing_index(
            index_name="cks-summary-1500tiktoken", 
            namespace="full-cks", 
            embedding = HypotheticalDocumentEmbedder.from_llm(
                llm=ChatOpenAI(), 
                base_embeddings=OpenAIEmbeddings(), 
                prompt_key="web_search")
            )
        return vectorstore

    docsearch = load_vectorstore()

    import promptlayer
    promptlayer.api_key = "pl_2b1769e7202b6a141d4491fca41e308a"

    from langchain.chains import RetrievalQAWithSourcesChain
    from langchain.chat_models import PromptLayerChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        AIMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    user1="""I will provide you with some contexts to help you answer a question. Be informal, friendly and fun, but use medical terminology. The answer must be elegant and must follow a logical flow. Explain the answer using a combination of 2-3 paragraphs and bullet points. Are you ready?
    """
    ass1="""Please provide me with the medical contexts. 😊"""
    user2="""Contexts:

    {summaries}

    My question:
    {question}"""
    messages = [
        SystemMessagePromptTemplate.from_template("""You are a helpful medical assistant that answers a doctor's questions. You will be given extracted parts of a long medical document to help answer questions. You can only answer the question if its related to the context. If you're unsure about the answer, simply state you haven't been fed with the appropriate NICE guidelines.
ALWAYS return a "SOURCES" part in your answer. The "SOURCES" part should be a reference to the sources in the documents provided from which you got your answer. If you're unsure about an answer, simply state so. Example of your response should be:
```
The answer is foo

SOURCES: 
- https://cks.nice.org.uk/xyz
```
"""),
        HumanMessagePromptTemplate.from_template(user1),
        AIMessagePromptTemplate.from_template(ass1),
        HumanMessagePromptTemplate.from_template(user2)
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        PromptLayerChatOpenAI(temperature=0, max_tokens=700, pl_tags=["cks-full-og"]), 
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 7}),
        chain_type_kwargs=chain_type_kwargs,
        max_tokens_limit=3000,
        reduce_k_below_max_tokens=True
    )

    # From here down is all the StreamLit UI.
    html_temp = """
                    <div style="background-color:{};padding:1px">
                    
                    </div>
                    """

    with st.sidebar:
        st.markdown("""
        ### About 
        \nAsk any medical question and get an explanation. You can even clear your MCQ doubts.
        \nPlease note that a detailed question will get a detailed answer and will take 10-15 seconds.
        \n\nDisclaimer: **DO NOT** use as a substitute for professional medical advice. This is meant for **EDUCATIONAL PURPOSES ONLY**.
        \n### How does it work?
        \nIt is trained on NICE CKS guidelines as in https://cks.nice.org.uk
        \n*If the source is anything else other than NICE, then the answer could be wrong.*
        """)
        st.markdown("""[Source Code](https://github.com/faz-cxr/nice)
        <a href = "mailto:fazeen.nasser@outlook.com?subject = Feedback&body = Message">Send Feedback</a><br>
        <a href="https://www.buymeacoffee.com/fazeen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 35px;width: 110px ;" ></a>
        """,
        unsafe_allow_html=True,
        )

    st.markdown("""
    ## Ask me anything
    Wanna chat with NICE guidelines? Try [here](https://chatnice.streamlit.app)
    """)
    user_input = st.text_area("..and I will answer  NICEly (in ~10sec)", disabled=False, placeholder="Start typing a medical question here and press Answer or Cmd/Ctrl+⏎")

    hide="""
    <style>
    footer{
        visibility: hidden;
        position: relative;
    }
    .viewerBadge_container__1QSob{
        visibility: hidden;
    }
    #MainMenu{
        visibility: hidden;
    }
    <style>
    """
    st.markdown(hide, unsafe_allow_html=True)

    if st.button("Answer") or user_input:
        with st.spinner('Thinking...'):
            result = chain({"question": user_input}, return_only_outputs=True)
            markdown_text = f"#### You asked:\n\n{user_input}\n\n#### My answer:\n\n{result['answer']}\n\n\n#### Sources:\n\n{result['sources']}"
            st.markdown(markdown_text)
            # with open('logs.csv', mode='a', newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerow([user_input, result['answer'], result['sources']])
    return True