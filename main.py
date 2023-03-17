"""Python file to serve as the frontend"""
import streamlit as st
import os
from streamlit_chat import message
from streamlit.components.v1 import html
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

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

system_template="""Use the following pieces of context to answer the users question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the source of the document from which you got your answer.

Example of your response should be:

```
The answer is foo
SOURCES: xyz
```

Begin!
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
chain = VectorDBQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0), 
    chain_type="stuff", 
    vectorstore=docsearch,
    chain_type_kwargs=chain_type_kwargs
)

# From here down is all the StreamLit UI.
st.set_page_config(page_title="Ask NICE CKS!", page_icon=":brain:")
html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

with st.sidebar:
    st.markdown("""
    # About 
    \nAsk any Medical Question and get an explanation.
    \n For more detailed responses, ask specific and detailed questions
    \n\nDisclaimer: **Do not** use as a substitute for professional medical advice.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.64)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work?
    \nIt is trained on NICE CKS guidelines.
    \nSource - http://nice.org.uk/
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

if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []

def get_text():
    st.markdown("""
    ## Ask me anything!
    """)
    input_text = st.text_input("Refresh the page to reset the conversation...", disabled=False, placeholder="Start typing a medical question here and press enter ⏎")
    return input_text

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

user_input = get_text()

if len(st.session_state["generated"]) < 1:
    prev_a = [""]
else:
    prev_a = st.session_state["generated"][-1:]

if len(st.session_state["past"]) < 1:
    prev_q = [""]
else:
    prev_q = st.session_state["past"][-1:]

query = '\n'.join([f"Q: {prev_q[0]}\nA: {prev_a[0]}\nQ: {user_input}\nA: "])
if user_input:
    result = chain({"question": query}, return_only_outputs=True)
    output = f"Answer - {result['answer']} | Source - {result['sources']}"
    print(result)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
