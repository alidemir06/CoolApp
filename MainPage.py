import streamlit as st



import streamlit as st

st.set_page_config(
    page_title="Exstreamly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.title("Main Page")

st.code("""
class Human:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def introduce(self):
        print(f"Hello, my name is {self.name}. I am {self.age} years old and I am {self.gender}.")

        # Create an instance of the Human class
human1 = Human("Ali", 21, "male")
human1.introduce()
""")