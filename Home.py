"""Python file to serve as the frontend"""
import streamlit as st
import csv
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

st.set_page_config(page_title="Ask NICEly CKS!", page_icon=":brain:")

@st.cache_resource
def load_vectorstore(index_path):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        embedding_function=embeddings, 
        persist_directory=index_path
    )
    return vectorstore

docsearch = load_vectorstore("chroma")

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

user1="""Use the following pieces of medical content to answer the users question.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the sources in the contexts I provide from which you got your answer.

Example of your response should be:

```
The answer is foo
SOURCES: https://cks.nice.org.uk/xyz
```

"""
ass1="""Please provide me with the medical contexts. 😊"""
user2="""Contexts:
{summaries}

My question:
{question}"""
messages = [
    SystemMessagePromptTemplate.from_template("""Use the pieces of medical content as context to answer a medical question. 
    Be informal and fun with emojis but use medical terminology.
    The answer must be specific, elegant and should follow a logical flow.
    Answer using a combination of 3-5 paragraphs and bullet points to enable easy reading.
    Output in Markdown format"""),
    HumanMessagePromptTemplate.from_template(user1),
    AIMessagePromptTemplate.from_template(ass1),
    HumanMessagePromptTemplate.from_template(user2)
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
chain = RetrievalQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0, max_tokens=720), 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(),
    chain_type_kwargs=chain_type_kwargs
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
    """)
    st.markdown("""
    ### How does it work?
    \nIt is trained on NICE CKS guidelines as in https://cks.nice.org.uk
    \n*If the source is anything else other than NICE, then the answer could be wrong.*
    """)
    st.markdown("Wanna chat with NICE guidelines? Try [here](https://chatnice.streamlit.app)")
    st.markdown("""
    <a href = "mailto:fazeen.nasser@outlook.com?subject = Feedback&body = Message">Send Feedback</a>
    """,
    unsafe_allow_html=True,
    )
    st.markdown("""
    <a href="https://www.buymeacoffee.com/fazeen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 35px;width: 110px ;" ></a>
    """,
    unsafe_allow_html=True,
    )

st.markdown("""
## Ask me anything
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
        with open('logs.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_input, result['answer'], result['sources']])