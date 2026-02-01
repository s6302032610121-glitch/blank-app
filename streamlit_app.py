import streamlit as st

st.set_page_config(page_title="Streamlit App Template", page_icon="🎈")

# Welcoming toast
st.toast("Welcome to your new Streamlit app! 🚀")

# Sidebar for Getting Started
with st.sidebar:
    st.title("🚀 Getting Started")
    st.markdown("""
    This is a simple Streamlit app template for you to modify!

    ### How to run it locally

    1. **Install requirements:**
       ```bash
       pip install -r requirements.txt
       ```
    2. **Run the app:**
       ```bash
       streamlit run streamlit_app.py
       ```

    Check out the [Streamlit Documentation](https://docs.streamlit.io/) for more information.
    """)

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to the [Streamlit Documentation](https://docs.streamlit.io/)."
)
