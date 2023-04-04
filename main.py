import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import chat
import index
import web


def init_session_state() -> None:
    if "human" not in st.session_state:
        st.session_state["human"] = []
    if "ai" not in st.session_state:
        st.session_state["ai"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "input_disabled" not in st.session_state:
        st.session_state["input_disabled"] = False


def check_input(container: DeltaGenerator, query: str) -> None:
    if not query:
        return

    print("-" * 24)
    print(f"Query: {query}")

    st.session_state["input"] = ""
    st.session_state.human.append(query)
    web.display_conversation(container)

    output = chat.get_response(query)
    print(f"Response: {output}")
    st.session_state["input_disabled"] = False
    st.session_state.ai.append(output)
    web.display_conversation(container)
    st.experimental_rerun()


if __name__ == '__main__':
    web.set_web()
    init_session_state()
    index.load_vector_store()
    conversation_container = st.empty()
    web.display_conversation(conversation_container)
    user_input = chat.get_input()
    st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Send")
    with col2:
        if st.button("Reset"):
            st.cache_resource.clear()
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()
    check_input(conversation_container, user_input)