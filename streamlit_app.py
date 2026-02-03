import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
)

st.title("🎈 My new app")

st.write(
    "Let's start building! For help and inspiration, head over to the [Streamlit Documentation](https://docs.streamlit.io/)."
)

# Sidebar with Getting Started instructions from README
with st.sidebar:
    st.header("Getting Started")
    st.markdown("""
    To run this app on your own machine:
    1. **Install requirements**:
       ```bash
       pip install -r requirements.txt
       ```
    2. **Run the app**:
       ```bash
       streamlit run streamlit_app.py
       ```

    Happy coding!
    """)

# Welcome toast, only shown once per session
if "welcome_toast" not in st.session_state:
    st.toast("Welcome to your new Streamlit app! 🎈")
    st.session_state.welcome_toast = True
