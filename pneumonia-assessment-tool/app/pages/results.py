# app/pages/results.py
import streamlit as st
from iris_integration.vector_store import search_similar_xrays, search_similar_symptoms

def app():
    st.title("Assessment Results")
    
    if 'xray_features' not in st.session_state or 'symptom_features' not in st.session_state:
        st.warning("No assessment results available. Please complete an assessment first.")
        return
    
    xray_features = st.session_state['xray_features']
    symptom_features = st.session_state['symptom_features']
    selected_symptoms = st.session_state['selected_symptoms']
    
    st.subheader("X-ray Analysis")
    similar_xrays = search_similar_xrays(xray_features)
    for i, (similarity, diagnosis) in enumerate(similar_xrays, 1):
        st.write(f"{i}. Similarity: {similarity:.2f}, Diagnosis: {diagnosis}")
    
    st.subheader("Symptom Analysis")
    st.write("Selected Symptoms:", ", ".join(selected_symptoms))
    similar_symptoms = search_similar_symptoms(symptom_features)
    for i, (similarity, condition) in enumerate(similar_symptoms, 1):
        st.write(f"{i}. Similarity: {similarity:.2f}, Condition: {condition}")
    
    st.subheader("Overall Assessment")
    # This is a simplified assessment. In a real-world scenario, you'd want a more sophisticated algorithm.
    xray_pneumonia_likelihood = sum(1 for _, diagnosis in similar_xrays if diagnosis == "pneumonia") / len(similar_xrays)
    symptom_pneumonia_likelihood = sum(1 for _, condition in similar_symptoms if condition == "pneumonia") / len(similar_symptoms)
    
    overall_likelihood = (xray_pneumonia_likelihood + symptom_pneumonia_likelihood) / 2
    
    st.write(f"Likelihood of Pneumonia: {overall_likelihood:.2%}")
    
    if overall_likelihood > 0.7:
        st.error("High likelihood of pneumonia. Please consult a healthcare professional immediately.")
    elif overall_likelihood > 0.4:
        st.warning("Moderate likelihood of pneumonia. Consider consulting a healthcare professional.")
    else:
        st.success("Low likelihood of pneumonia. Monitor your symptoms and consult a doctor if they worsen.")
    
    st.info("Remember: This assessment is not a diagnosis. Always consult with a qualified healthcare provider.")