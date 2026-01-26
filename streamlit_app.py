import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StructureCAD AI - Structural Engineering Software",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit's default UI elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
            iframe {
                width: 100%;
                height: 100vh;
                border: none;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load the index.html file
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Render the HTML content
    components.html(html_content, height=2000, scrolling=True)
except FileNotFoundError:
    st.error("index.html not found. Please ensure it exists in the same directory.")
