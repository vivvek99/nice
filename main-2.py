"""Python file to serve as the frontend"""
import streamlit as st
import os
from streamlit_chat import message
from streamlit.components.v1 import html
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

os.environ['OPENAI_API_KEY'] = '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'
embeddings = OpenAIEmbeddings()
docsearch = Chroma(persist_directory='chroma', embedding_function=embeddings)

from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

system_template="""Use the following pieces of medical context to answer the users question.
If you don't know the answer, just say that you don't know, Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the source of the document from which you got your answer.

Example of your response should be:

```
The answer is foo
SOURCES: https://cks.nice.org.uk/xyz
```

Begin!
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("Please answer medically and explain why:\n\n{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
chain = VectorDBQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0, max_tokens = 800), 
    chain_type="stuff", 
    vectorstore=docsearch,
    chain_type_kwargs=chain_type_kwargs
)

# From here down is all the StreamLit UI.
st.set_page_config(page_title="Ask NICEly CKS!", page_icon=":brain:")
html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

with st.sidebar:
    st.markdown("""
    # About 
    \nAsk any medical question and get an explanation. You can even clear your MCQ doubts.
    \nPlease note that a detailed question will get a detailed answer.
    \n\nDisclaimer: **DO NOT** use as a substitute for professional medical advice. This is meant for **EDUCATIONAL PURPOSES ONLY**.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.64)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work?
    \nIt is trained on NICE CKS guidelines.
    \nSource - https://cks.nice.org.uk
    \n\nIf the source is anything else other than NICE, then the answer could be wrong.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.64)"),unsafe_allow_html=True)
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
# Ask me anything
""")
user_input = st.text_area("..and I will answer  NICEly", disabled=False, placeholder="Start typing a medical question here and press enter Cmd/Ctrl+⏎")

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
    result = chain({"question": user_input}, return_only_outputs=True)
    markdown_text = f"#### Answer:\n\n{result['answer']}\n\n\n#### Sources:\n\n{result['sources']}"
    st.markdown(markdown_text)