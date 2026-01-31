import streamlit as st

st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
)

if "welcome_toast" not in st.session_state:
    st.toast("Welcome to your new Streamlit app!", icon="🎈")
    st.session_state.welcome_toast = True

st.title("🎈 My new app")

with st.sidebar:
    st.header("Getting Started")
    st.markdown("""
    Welcome to your new app! Here are some next steps:
    1.  **Modify this page**: Edit `streamlit_app.py` to change the content.
    2.  **Add dependencies**: Add any required Python packages to `requirements.txt`.
    3.  **Deploy**: Connect your GitHub repo to [Streamlit Community Cloud](https://share.streamlit.io).
    """)
    st.divider()
    st.write("Need help? Check out the [Streamlit Documentation](https://docs.streamlit.io/).")

st.write(
    "Let's start building! For help and inspiration, head over to the [Streamlit Documentation](https://docs.streamlit.io/)."
)
