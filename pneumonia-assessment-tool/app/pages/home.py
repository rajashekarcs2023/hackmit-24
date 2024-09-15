import streamlit as st

def app():
    st.title('Welcome to the Pneumonia Assessment Tool')
    st.write("""
    This tool uses advanced AI techniques to assist in the assessment of pneumonia 
    based on chest X-rays and reported symptoms. Please note that this tool is for 
    educational purposes only and should not replace professional medical advice.
    """)
    
    st.subheader('How to use this tool:')
    st.write("""
    1. Navigate to the 'Assessment' page
    2. Upload a chest X-ray image
    3. Enter any symptoms you're experiencing
    4. Review the results and analysis
    5. Consult with a healthcare professional for accurate diagnosis
    """)
    
    st.info('Remember: This tool is not a substitute for professional medical diagnosis.')