import streamlit as st

st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
)

if "app_just_started" not in st.session_state:
    st.session_state.app_just_started = True
    st.toast("Welcome to your new Streamlit app! 🎈", icon="🎈")

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [Streamlit Documentation](https://docs.streamlit.io/)."
)

with st.sidebar:
    st.title("🚀 Getting Started")
    st.markdown("""
### How to run it on your own machine

1. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```bash
   $ streamlit run streamlit_app.py
   ```
    """)
