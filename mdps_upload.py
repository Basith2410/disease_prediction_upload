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
    extracted_values = [''] * 8

    if uploaded_file is not None:
        pdf_text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:  # Corrected line
                for page in pdf.pages:
                    pdf_text += page.extract_text()
            extracted_values = re.findall(r'(\d+\.\d+)', pdf_text)
            st.write("Extracted Values:", extracted_values)  # Debugging line
        except Exception as e:
            st.error(f"Error during PDF extraction: {e}")

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', value=extracted_values[0])

    with col2:
        Glucose = st.text_input('Glucose Level', value=extracted_values[1])

    with col3:
        BloodPressure = st.text_input('Blood Pressure', value=extracted_values[2])

    with col1:
        SkinThickness = st.text_input('Skin Thickness', value=extracted_values[3])

    with col2:
        Insulin = st.text_input('Insulin', value=extracted_values[4])

    with col3:
        BMI = st.text_input('BMI', value=extracted_values[5])

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', value=extracted_values[6])

    with col2:
        Age = st.text_input('Age', value=extracted_values[7])

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


