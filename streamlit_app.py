import streamlit as st

with st.sidebar:
    st.header("Getting Started")
    st.markdown("To get started with this template:")

    st.subheader("1. Install requirements")
    st.code("pip install -r requirements.txt")

    st.subheader("2. Run the app")
    st.code("streamlit run streamlit_app.py")

    st.subheader("3. Modify code")
    st.markdown("Start editing `streamlit_app.py`!")

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
