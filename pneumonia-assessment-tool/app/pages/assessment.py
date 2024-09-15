import streamlit as st
from components import xray_upload, symptom_input

def app():
    st.title('Pneumonia Assessment')
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = xray_upload.upload_xray()
    
    with col2:
        symptoms = symptom_input.get_symptoms()
    
    if uploaded_file and symptoms:
        if st.button('Analyze'):
            # Here you would typically call your backend analysis function
            # For now, we'll just set a flag in the session state
            st.session_state['analysis_complete'] = True
            st.success('Analysis complete! View results in the Results page.')
    else:
        st.warning('Please upload an X-ray and enter symptoms to proceed.')