import streamlit as st
import streamlit.components.v1 as components
import os

# Set page config
st.set_page_config(
    page_title="StructureCAD - Industrial Factory Designer",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS to hide streamlit elements and make iframe full screen
st.markdown("""
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
    """, unsafe_allow_html=True)

def main():
    # Load index.html
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Display the HTML content in a components.html call
        # Using height=1000 or similar, but the CSS above tries to make it full screen
        components.html(html_content, height=1200, scrolling=True)
    else:
        st.error("index.html not found. Please ensure the frontend build is complete.")

if __name__ == "__main__":
    main()
