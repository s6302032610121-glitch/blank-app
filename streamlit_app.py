import streamlit as st

# Set page configuration
st.set_page_config(page_title="Streamlit App Template", page_icon="🎈")

# Initialize session state for toast notification
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

# Display toast notification once per session
if st.session_state.first_visit:
    st.toast("Welcome to your new Streamlit app! 🎈")
    st.session_state.first_visit = False

# Sidebar with "Getting Started" instructions
with st.sidebar:
    st.title("🚀 Getting Started")
    st.markdown("""
    ### How to run it on your own machine

    1. **Install requirements**
       ```bash
       pip install -r requirements.txt
       ```

    2. **Run the app**
       ```bash
       streamlit run streamlit_app.py
       ```
    """)
    st.divider()
    st.info("Edit `streamlit_app.py` to start building your own app!")

# Main content
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to the [Streamlit Documentation](https://docs.streamlit.io/)."
)
