# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 17:07:03 2023

@author: Mars
"""

import pickle
import streamlit as st
import pdfplumber
import re
from streamlit_option_menu import option_menu


# loading the saved models

diabetes_model = pickle.load(open('diabetes.sav', 'rb'))

heart_disease_model = pickle.load(open('heartdisease_model.sav', 'rb'))

parkinsons_model = pickle.load(open('parkinson_model.sav', 'rb'))


# sidebar for navigation
with st.sidebar:
    
    selected = option_menu('Multiple Disease Prediction System',
                          
                          ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Parkinsons Prediction'],
                          icons=['activity','heart','person'],
                          default_index=0)

# Function to extract value from the report content based on the keyword
def extract_value(report_text, keyword):
    pattern = re.compile(rf'{keyword}\s*:\s*([\d.]+)')
    match = pattern.search(report_text)
    if match:
        return match.group(1)
    return ''

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
            extracted_values['Pregnancies'] = extract_value(pdf_text, 'Pregnancies')
            extracted_values['Glucose'] = extract_value(pdf_text, 'Glucose')
            extracted_values['BloodPressure'] = extract_value(pdf_text, 'BloodPressure')
            extracted_values['SkinThickness'] = extract_value(pdf_text, 'SkinThickness')
            extracted_values['Insulin'] = extract_value(pdf_text, 'Insulin')
            extracted_values['BMI'] = extract_value(pdf_text, 'BMI')
            extracted_values['DiabetesPedigreeFunction'] = extract_value(pdf_text, 'DiabetesPedigreeFunction')
            extracted_values['Age'] = extract_value(pdf_text, 'Age')
            #st.write("Extracted Values:", extracted_values)  # Debugging line
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
    
# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):
    
    # page title
    st.title('Heart Disease Prediction using ML')

    # Allow the user to upload a PDF report
    uploaded_file = st.file_uploader("Upload a PDF report", type=["pdf"])

    # Initialize variables to store extracted values
    extracted_values = {'Age': '', 'Sex': '', 'Cp': '', 'Trestbps': '',
                        'Chol': '', 'Fbs': '', 'Restecg': '', 'Thalach': '',
                        'Exang': '', 'Oldpeak': '', 'Slope': '', 'Ca': '', 'thal': ''}

    if uploaded_file is not None:
        pdf_text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text()
            extracted_values['Age'] = extract_value(pdf_text, 'Age')
            extracted_values['Sex'] = extract_value(pdf_text, 'Sex')
            extracted_values['Cp'] = extract_value(pdf_text, 'Cp')
            extracted_values['Trestbps'] = extract_value(pdf_text, 'Trestbps')
            extracted_values['Chol'] = extract_value(pdf_text, 'Chol')
            extracted_values['Fbs'] = extract_value(pdf_text, 'Fbs')
            extracted_values['Restecg'] = extract_value(pdf_text, 'Restecg')
            extracted_values['Thalach'] = extract_value(pdf_text, 'Thalach')
            extracted_values['Exang'] = extract_value(pdf_text, 'Exang')
            extracted_values['Oldpeak'] = extract_value(pdf_text, 'Oldpeak')
            extracted_values['Slope'] = extract_value(pdf_text, 'Slope')
            extracted_values['Ca'] = extract_value(pdf_text, 'Ca')
            extracted_values['thal'] = extract_value(pdf_text, 'thal')
        except Exception as e:
            st.error(f"Error during PDF extraction: {e}")

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age', value=extracted_values['Age'])

    with col2:
        sex = st.text_input('Sex', value=extracted_values['Sex'])

    with col3:
        cp = st.text_input('Chest Pain types', value=extracted_values['Cp'])

    with col1:
        trestbps = st.text_input('Resting Blood Pressure', value=extracted_values['Trestbps'])

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl', value=extracted_values['Chol'])

    with col3:
        fbs = st.text_input('Fasting Blood Sugar', value=extracted_values['Fbs'])

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results', value=extracted_values['Restecg'])

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved', value=extracted_values['Thalach'])

    with col3:
        exang = st.text_input('Exercise Induced Angina', value=extracted_values['Exang'])

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise', value=extracted_values['Oldpeak'])

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment', value=extracted_values['Slope'])

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy', value=extracted_values['Ca'])

    with col1:
        thal = st.text_input('thal', value=extracted_values['thal'])

    # Code for Prediction
    heart_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Heart Disease Test Result'):
        heart_prediction = heart_disease_model.predict([[Age, Sex, Cp, Trestbps, Chol, Fbs, Restecg, Thalach,
                                                        Exang, Oldpeak, Slope, Ca, thal]])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)
