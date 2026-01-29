import streamlit as st

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
)

# Show a welcome toast
if "welcome_toast_shown" not in st.session_state:
    st.toast("Welcome to your new Streamlit app! 🚀")
    st.session_state.welcome_toast_shown = True

# Add a "Getting Started" sidebar
with st.sidebar:
    st.header("Getting Started")
    st.markdown("""
    This is a blank template for your Streamlit app.

    ### Resources
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
    - [Gallery](https://streamlit.io/gallery)

    ### Next Steps
    1. Edit `streamlit_app.py`
    2. Add your data and logic
    3. Deploy to Streamlit Community Cloud
    """)

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
