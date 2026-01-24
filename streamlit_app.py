import streamlit as st

# Add page configuration for better UX
st.set_page_config(
    page_title="Blank App Template",
    page_icon="🎈",
)

# Add a welcoming toast for delight
st.toast("Welcome to your new app! 🎈")

# Add a sidebar with Getting Started info
with st.sidebar:
    st.title("Getting Started")
    st.markdown("""
### How to run it

1. Install the requirements
   ```
   pip install -r requirements.txt
   ```

2. Run the app
   ```
   streamlit run streamlit_app.py
   ```
""")

st.title("🎈 My new app")

# Improve link accessibility
st.write(
    "Let's start building! For help and inspiration, head over to the [Streamlit Documentation](https://docs.streamlit.io/)."
)
