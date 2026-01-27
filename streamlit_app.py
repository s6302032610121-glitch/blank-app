import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
    layout="centered"
)

# Welcome toast (one-time per session)
if "welcome_shown" not in st.session_state:
    st.toast("Welcome to your new Streamlit app! 🎈")
    st.session_state.welcome_shown = True

# Sidebar for better organization and helpful info
with st.sidebar:
    st.title("About")
    st.info(
        "This is a simple Streamlit app template. "
        "Use the links below to learn more about Streamlit."
    )
    st.markdown("### Resources")
    st.markdown("- [Streamlit Documentation](https://docs.streamlit.io/)")
    st.markdown("- [Streamlit Community Cloud](https://streamlit.io/cloud)")
    st.markdown("- [Streamlit Components](https://streamlit.io/components)")

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, check out the "
    "[Streamlit Documentation](https://docs.streamlit.io/)."
)
