import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from googletrans import Translator
import time

st.set_page_config(
    page_title="Exstreamly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("DiagnoHub")


on = st.toggle("ENG|TR")

information = """
    DiagnoHub is an innovative healthcare application designed to empower users 
    with accurate and personalized disease diagnosis. Using advanced machine learning
    algorithms, DiagnoHub analyzes the exhibited symptoms provided by the user to 
    generate potential diagnoses. Our user-friendly interface guides you through the
    symptom input process, helping you to provide relevant information for a more 
    accurate assessment. Whether you're experiencing minor discomfort or seeking 
    clarity on a more serious condition, DiagnoHub provides reliable insights to aid 
    in your healthcare journey. Take control of your health today with DiagnoHub.
"""
def translate(text, src_lang='en', dest_lang='tr'):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text

if on:
    information = translate(information)
else:
    information = information

def stream_data():
    for word in information.split(" "):
        yield word + " "
        time.sleep(0.03)

if st.button("Learn More", type="secondary"):
    st.write_stream(stream_data())

df = pd.read_csv("pages/disease.csv")
encoder = LabelEncoder()
df["prognosis"] = encoder.fit_transform(df["prognosis"])

x, y = df.drop("prognosis", axis = 1), df["prognosis"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

model = RandomForestClassifier(random_state=1, verbose=0)
model.fit(x_train, y_train)
#predictions = model.predict(x_test)
#accuracy = accuracy_score(y_test, predictions)

symptoms = x.columns.values

# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}

for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index":symptom_index,
    "predictions_classes":encoder.classes_
}

def predict_disease(symptoms): # strings with separated coma
    symptoms = symptoms.split(",")

    # creating input data for the models
    input_data = [0]*len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1

    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)

    return data_dict["predictions_classes"][model.predict(input_data)[0]]

with st.form("Symptoms", clear_on_submit=True):
    x = st.multiselect("Symptoms", symptom_index.keys())

    button = st.form_submit_button("Diagnose")
    if button:
        symptoms = ",".join(x)
        st.write(predict_disease(symptoms))



