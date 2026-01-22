import streamlit as st
import streamlit.components.v1 as components
import os

# Set page configuration
st.set_page_config(
    page_title="StructureCAD | Professional Structural Engineering Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS to hide Streamlit header, footer, and adjust margins
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
    div[data-testid="stVerticalBlock"] > div:first-child {
        margin-top: -50px;
    }
    iframe {
        width: 100%;
        height: 100vh;
        border: none;
        overflow: hidden;
    }
    body {
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to load and render the index.html
def main():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Use a large height to avoid inner scrollbars if possible,
        # or handle scrolling within the iframe.
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.title("StructureCAD")
        st.info("Initializing application... Please wait.")
        st.warning("index.html not found. The core application file is being prepared.")

if __name__ == "__main__":
    main()
