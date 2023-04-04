import streamlit as st

def createPage():
        with open('./files/About.md', "r") as f:
              about = f.read()
        st.markdown(about)
        st.image('./files/hiw.png')
        st.markdown("Sneak Peak v2:<br>Try chatting with NICE guidelines -> [ChatNICE](https://chatnice.streamlit.app)",unsafe_allow_html=True)
        st.markdown("""<a href="https://www.buymeacoffee.com/fazeen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" alt="Buy Me A Coffee" style="height: 40px;width: 145px" ></a><br><br>
        [Source Code](https://github.com/faz-cxr/nice)<br><br>
        <a href = "mailto:fazeen.nasser@outlook.com?subject = Feedback&body = Message">Send Feedback</a><br>
        """,
        unsafe_allow_html=True,
        )
        return True