import streamlit as st

def get_symptoms(available_symptoms):
    """
    Display a multi-select input for selecting symptoms from the available symptoms list.
    Allow users to input additional symptoms.
    """
    # Use the dynamically provided list of symptoms from the database
    symptoms = st.multiselect(
        'Select your symptoms',
        available_symptoms,
        []
    )
    
    # Allow the user to input any additional symptoms manually
    additional_symptoms = st.text_input('Any other symptoms? (comma-separated)')
    if additional_symptoms:
        symptoms.extend([s.strip() for s in additional_symptoms.split(',')])
    
    return symptoms
