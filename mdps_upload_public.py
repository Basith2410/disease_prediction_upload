import pickle
import streamlit as st
import pdfplumber
import re

# loading the saved models
diabetes_model = pickle.load(open('diabetes.sav', 'rb'))

# sidebar for navigation
with st.sidebar:
    selected = st.selectbox(
        'Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"]
    )

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    # Allow the user to upload a PDF report
    uploaded_file = st.file_uploader("Upload a PDF report", type=["pdf"])

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    # Code for Prediction
    diab_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Diabetes Test Result'):
        if uploaded_file is not None:
            pdf_text = ""
            with pdfplumber.load(uploaded_file) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text()
            extracted_values = re.findall(r'(\d+\.\d+)', pdf_text)
            if len(extracted_values) >= 8:
                Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age = extracted_values[
                                                                                                                  :8]

        diab_prediction = diabetes_model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

    st.success(diab_diagnosis)
