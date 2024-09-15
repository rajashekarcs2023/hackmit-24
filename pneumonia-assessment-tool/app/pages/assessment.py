import streamlit as st
from components.xray_upload import upload_xray
from components.symptom_input import get_symptoms
from iris_integration.vector_store import process_xray, process_symptoms, get_all_symptoms
from iris_integration.iris_connection import get_db_connection

def app():
    st.title("Pneumonia Assessment")

    # File uploader for X-ray image
    uploaded_file = upload_xray()
    
    # Symptom selection from the database
    engine = get_db_connection()
    all_symptoms = get_all_symptoms(engine)  # Fetch individual symptoms related to "Pneumonia"
    
    if all_symptoms:
        selected_symptoms = get_symptoms(all_symptoms)  # Display the distinct symptoms in the dropdown
    else:
        st.error("No symptoms data found in the database.")

    if st.button("Assess"):
        if uploaded_file is None:
            st.error("Please upload an X-ray image.")
        elif not selected_symptoms:
            st.error("Please select at least one symptom.")
        else:
            with st.spinner("Processing..."):
                # Process the uploaded X-ray
                xray_features = process_xray(uploaded_file)
                
                # Process the selected symptoms
                symptom_features = process_symptoms(selected_symptoms)
                
                # Store results in session state for the Results page
                st.session_state['xray_features'] = xray_features
                st.session_state['symptom_features'] = symptom_features
                st.session_state['selected_symptoms'] = selected_symptoms
                
                st.success("Assessment complete! Please go to the Results page.")
