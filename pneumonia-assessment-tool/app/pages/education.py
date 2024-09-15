# app/pages/education.py
import streamlit as st

def app():
    st.title("Education: Understanding Pneumonia")
    
    st.write("""
    Pneumonia is an infection that inflames the air sacs in one or both lungs. 
    The air sacs may fill with fluid or pus, causing cough with phlegm or pus, 
    fever, chills, and difficulty breathing.
    """)
    
    st.subheader("Common Symptoms of Pneumonia")
    symptoms = [
        "Chest pain when breathing or coughing",
        "Confusion or changes in mental awareness (in adults age 65 and older)",
        "Cough, which may produce phlegm",
        "Fatigue",
        "Fever, sweating and shaking chills",
        "Lower than normal body temperature (in adults older than age 65 and people with weak immune systems)",
        "Nausea, vomiting or diarrhea",
        "Shortness of breath"
    ]
    for symptom in symptoms:
        st.write(f"- {symptom}")
    
    st.subheader("When to See a Doctor")
    st.write("""
    See your doctor if you have difficulty breathing, chest pain, persistent fever of 102 F (39 C) or higher, 
    or persistent cough, especially if you're coughing up pus.
    """)
    
    st.subheader("Prevention")
    preventions = [
        "Get vaccinated",
        "Practice good hygiene",
        "Don't smoke",
        "Keep your immune system strong"
    ]
    for prevention in preventions:
        st.write(f"- {prevention}")
    
    st.info("This information is for educational purposes only. Always consult with a qualified healthcare provider for medical advice.")