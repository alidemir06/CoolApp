import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Exstreamly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title(":red[About]")

information = """
Hey there! I'm **Ali Demir**, a first-year mechanical engineering student who's super
excited about space, rockets, and AI. I'm still learning, but I'm really into using 
machine learning to solve cool problems. I made this website to share my projects and
stuff with you. I'm all about exploring new ideas and trying out new things, and I hope
you'll join me on this adventure!

I'm still figuring things out, but I'm always eager to learn more and grow. Stick around,
and let's discover some awesome stuff together!
"""

def stream_data():
    for word in information.split(" "):
        yield word + " "
        time.sleep(0.03)
st.write_stream(stream_data())

st.page_link(page="pages/Subscribe.py", label=":red[Subscribe for more!]")
