import pickle
import streamlit as st
import pdfplumber
import re

# Load the saved models
diabetes_model = pickle.load(open('diabetes.sav', 'rb'))

# Sidebar for navigation
with st.sidebar:
    selected = st.selectbox(
        'Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"]
    )

# Function to extract values from the report content
def extract_values(report_text):
    extracted_values = {'Pregnancies': '', 'Glucose': '', 'BloodPressure': '', 'SkinThickness': '',
                        'Insulin': '', 'BMI': '', 'DiabetesPedigreeFunction': '', 'Age': ''}
    matches = re.findall(r'([A-Za-z\s]+)\s*:\s*([\d.]+)', report_text)
    for key, value in matches:
        key = key.strip()
        if key in extracted_values:
            extracted_values[key] = value
    return extracted_values

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    # Allow the user to upload a PDF report
    uploaded_file = st.file_uploader("Upload a PDF report", type=["pdf"])

    # Initialize variables to store extracted values
    extracted_values = {'Pregnancies': '', 'Glucose': '', 'BloodPressure': '', 'SkinThickness': '',
                        'Insulin': '', 'BMI': '', 'DiabetesPedigreeFunction': '', 'Age': ''}

    if uploaded_file is not None:
        pdf_text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text()
            start_idx = pdf_text.find("Diabetes Test")
            end_idx = pdf_text.find("Age :")
            if start_idx != -1 and end_idx != -1:
                extracted_section = pdf_text[start_idx:end_idx]
                extracted_values = extract_values(extracted_section)
                st.write("Extracted Values:", extracted_values)  # Debugging line
        except Exception as e:
            st.error(f"Error during PDF extraction: {e}")

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Pregnancies', value=extracted_values['Pregnancies'])

    with col2:
        Glucose = st.text_input('Glucose Level', value=extracted_values['Glucose'])

    with col3:
        BloodPressure = st.text_input('Blood Pressure', value=extracted_values['BloodPressure'])

    # Add input fields for the remaining columns
    with col1:
        SkinThickness = st.text_input('Skin Thickness', value=extracted_values['SkinThickness'])

    with col2:
        Insulin = st.text_input('Insulin Level', value=extracted_values['Insulin'])

    with col3:
        BMI = st.text_input('BMI', value=extracted_values['BMI'])

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', value=extracted_values['DiabetesPedigreeFunction'])

    with col2:
        Age = st.text_input('Age of the Person', value=extracted_values['Age'])

    # Code for Prediction
    diab_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Diabetes Test Result'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

    st.success(diab_diagnosis)
