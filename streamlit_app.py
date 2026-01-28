import streamlit as st

st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
    layout="centered",
)

st.title("🎈 Streamlit App Template")

# Welcome toast
if "toast_shown" not in st.session_state:
    st.toast("Welcome to your new Streamlit app! 🎈")
    st.session_state.toast_shown = True

# Sidebar for Getting Started
with st.sidebar:
    st.header("🚀 Getting Started")
    st.markdown("""
    This is a simple Streamlit app template for you to modify!

    ### How to run it locally

    1. **Install requirements**
       ```bash
       pip install -r requirements.txt
       ```
    2. **Run the app**
       ```bash
       streamlit run streamlit_app.py
       ```

    ### Documentation
    - [Streamlit Docs](https://docs.streamlit.io)
    - [Components](https://streamlit.io/components)
    - [Gallery](https://streamlit.io/gallery)
    """)

st.write(
    "Welcome! This template is ready for your customizations. Check the sidebar for tips on how to get started, or dive straight into the code to begin building your data app."
)

st.info("💡 **Pro tip:** You can find more inspiration and tutorials at [docs.streamlit.io](https://docs.streamlit.io/).", icon="ℹ️")
