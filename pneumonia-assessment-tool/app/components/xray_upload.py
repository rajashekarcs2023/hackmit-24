import streamlit as st

def upload_xray():
    uploaded_file = st.file_uploader("Upload chest X-ray image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded X-ray', use_column_width=True)
    return uploaded_file