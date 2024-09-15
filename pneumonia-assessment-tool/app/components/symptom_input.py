import streamlit as st

def get_symptoms(available_symptoms):
    """
    Display a multi-select input for selecting symptoms from the available symptoms list.
    Allow users to input additional symptoms.
    """
    symptoms = st.multiselect(
        'Select your symptoms',
        available_symptoms,  # Pass the list of symptoms fetched from the database
        []
    )
    
    additional_symptoms = st.text_input('Any other symptoms? (comma-separated)')
    if additional_symptoms:
        symptoms.extend([s.strip() for s in additional_symptoms.split(',')])
    
    return symptoms
