# First
import streamlit as st

st.set_page_config(
    page_title="Exstreamly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Chatbot")

openai_api_key = st.text_input("Enter Your Key to Chat", key="chatbot_api_key", type="password")
st.page_link(page="pages/Subscribe.py", label=":red[Login for key!]")

