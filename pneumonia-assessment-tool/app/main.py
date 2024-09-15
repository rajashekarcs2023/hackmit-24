import streamlit as st
from iris_integration.iris_connection import initialize_database, load_xray_data, load_symptom_data
from pages import home,assessment,results,education

def main():
    # Initialize the database tables
    initialize_database()
    
    # Load X-ray data and symptom data into the database (Optional: only if needed)
    # Comment out the following lines if data is already loaded to avoid reloading.
    load_xray_data('data/chest_xray')
    load_symptom_data('data/dataset.csv')
    
    st.sidebar.title('Navigation')
    
    PAGES = {
        "Home": home,   # Example, update accordingly
        "Assessment": assessment,  # This will be your main assessment logic
        "Results": results,  # Results page
        "Education": education,  # Information page
    }
    
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()  # This renders the selected page

if __name__ == "__main__":
    main()
