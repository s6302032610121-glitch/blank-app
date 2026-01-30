import streamlit as st

# Step 1: Set page configuration
st.set_page_config(page_title="Streamlit App Template", page_icon="🎈")

# Step 3: Implement a welcome toast (only once per session)
if "welcomed" not in st.session_state:
    st.toast("Welcome to your new app! 🎈")
    st.session_state.welcomed = True

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Step 2: Add a 'Getting Started' sidebar
with st.sidebar:
    st.title("Getting Started")
    st.info("Welcome! This blank template is ready for your customizations.")

    st.markdown("### 📚 Resources")
    st.markdown("""
    - [Streamlit Documentation](https://docs.streamlit.io)
    - [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
    - [Community Forum](https://discuss.streamlit.io)
    """)

    if st.button("Say Hello"):
        st.toast("Hello! Happy coding! 🚀")
