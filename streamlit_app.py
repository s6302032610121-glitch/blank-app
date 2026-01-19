import streamlit as st
import streamlit.components.v1 as components
import os

# Set page config for a true app-like experience
st.set_page_config(
    page_title="StructureCAD - Professional Engineering Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Advanced CSS to hide Streamlit UI and make the component full-screen
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    .stApp {
        overflow: hidden;
    }
    iframe {
        height: 100vh;
        width: 100vw;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            # Inject a small script to handle potential window size issues
            components.html(html_content, height=1200, scrolling=False)
    else:
        st.error("Error: index.html not found. Please ensure the file is in the root directory.")

if __name__ == "__main__":
    main()
