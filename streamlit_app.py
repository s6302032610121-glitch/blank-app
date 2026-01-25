import streamlit as st

# 1. Set Page Configuration for a professional look
st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="🎈",
    layout="centered"
)

# 2. Add a welcoming toast notification (once per session)
if "welcome_toast" not in st.session_state:
    st.toast("Welcome to your new Streamlit app!", icon="🎈")
    st.session_state.welcome_toast = True

# 3. Use a Sidebar to declutter the main area and provide guidance
with st.sidebar:
    st.header("🚀 Getting Started")
    st.markdown("""
    To run this app on your local machine:
    1. **Install dependencies**:
       ```bash
       pip install -r requirements.txt
       ```
    2. **Run the app**:
       ```bash
       streamlit run streamlit_app.py
       ```
    """)
    st.divider()
    st.markdown("### 📚 Resources")
    st.page_link("https://docs.streamlit.io/", label="Streamlit Documentation", icon="📖")

# 4. Main content area
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, check out the resources in the sidebar."
)

st.success("Ready to go! Edit `streamlit_app.py` to start your project.")
