import streamlit as st
from pages import home, assessment, results, education

PAGES = {
    "Home": home,
    "Assessment": assessment,
    "Results": results,
    "Education": education
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()