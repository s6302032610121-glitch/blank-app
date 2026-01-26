import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
    layout="centered"
)

# Toast Notification (appears once per session)
if "toast_shown" not in st.session_state:
    st.toast("Welcome to your new Streamlit app! 🎈")
    st.session_state.toast_shown = True

# Sidebar for instructions
with st.sidebar:
    st.header("Getting Started")
    st.markdown("""
### How to run it

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
    st.info("Edit `streamlit_app.py` to customize this app.")

# Main content
st.title("🎈 Streamlit App Template")
st.write(
    "Let's start building! Explore the sidebar for setup instructions and head over to [docs.streamlit.io](https://docs.streamlit.io/) for help and inspiration."
)
