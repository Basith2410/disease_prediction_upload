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

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    # Allow the user to upload a PDF report
    uploaded_file = st.file_uploader("Upload a PDF report", type=["pdf"])

    # Initialize variables to store extracted values
    extracted_values = {'Pregnancies': '', 'Glucose': '', 'Blood Pressure': '', 'Skin Thickness': '',
                        'Insulin': '', 'BMI': '', 'Diabetes Pedigree Function': '', 'Age': ''}

    if uploaded_file is not None:
        pdf_text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text()
            extracted_values_list = re.findall(r'([^:]+)\s*:\s*([\d.]+)', pdf_text)
            st.write("Extracted Values:", extracted_values_list)  # Debugging line

            # Match extracted values to input fields
            for key, value in extracted_values_list:
                key = key.strip()
                if key in extracted_values:
                    extracted_values[key] = value
        except Exception as e:
            st.error(f"Error during PDF extraction: {e}")

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', value=extracted_values['Pregnancies'])

    with col2:
        Glucose = st.text_input('Glucose Level', value=extracted_values['Glucose'])

    with col3:
        BloodPressure = st.text_input('Blood Pressure', value=extracted_values['Blood Pressure'])

    # Add input fields for the remaining columns
    with col1:
        SkinThickness = st.text_input('Skin Thickness', value=extracted_values['Skin Thickness'])

    with col2:
        Insulin = st.text_input('Insulin Level', value=extracted_values['Insulin'])

    with col3:
        BMI = st.text_input('BMI', value=extracted_values['BMI'])

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', value=extracted_values['Diabetes Pedigree Function'])

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
