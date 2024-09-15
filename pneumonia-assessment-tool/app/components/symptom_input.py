import streamlit as st

def get_symptoms():
    symptoms = st.multiselect(
        'Select your symptoms',
        ['Cough', 'Fever', 'Shortness of breath', 'Chest pain', 'Fatigue', 'Confusion',
         'Nausea', 'Vomiting', 'Diarrhea', 'Rapid heartbeat', 'Difficulty swallowing'],
        []
    )
    
    additional_symptoms = st.text_input('Any other symptoms? (comma-separated)')
    if additional_symptoms:
        symptoms.extend([s.strip() for s in additional_symptoms.split(',')])
    
    return symptoms