import streamlit as st

def show_results(results):
    st.subheader('Analysis Results')
    
    st.write(f"Pneumonia Probability: {results['pneumonia_probability']:.2%}")
    
    st.progress(results['pneumonia_probability'])
    
    if results['pneumonia_probability'] > 0.7:
        st.error('High risk of pneumonia. Please consult a healthcare professional immediately.')
    elif results['pneumonia_probability'] > 0.4:
        st.warning('Moderate risk of pneumonia. Consider consulting a healthcare professional.')
    else:
        st.success('Low risk of pneumonia. Monitor your symptoms and consult a doctor if they worsen.')
    
    st.subheader('Similar X-rays')
    for xray in results['similar_xrays']:
        st.image(xray, width=200)
    
    st.subheader('Similar Symptom Patterns')
    st.write(', '.join(results['similar_symptoms']))
    
    st.info('Remember: This analysis is not a diagnosis. Always consult with a qualified healthcare provider.')
