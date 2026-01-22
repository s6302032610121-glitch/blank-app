import streamlit as st
from openai import OpenAI
import re

# Page config
st.set_page_config(
    page_title="ManusCode AI - Autonomous Code Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for "Manus-like" professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=IBM+Plex+Sans+Thai:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'IBM Plex Sans Thai', sans-serif;
    }

    .main {
        background-color: #ffffff;
    }

    .stChatFloatingInputContainer {
        bottom: 20px;
    }

    .stChatMessage {
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    /* Better scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #aaa;
    }

    .preview-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 15px;
        background: #f8f9fa;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e0e0e0;
        border-bottom: none;
    }

    .preview-window {
        border: 1px solid #e0e0e0;
        border-radius: 0 0 8px 8px;
        background-color: white;
        height: 700px;
        overflow: hidden;
    }

    .sidebar .stButton button {
        width: 100%;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #f0f2f6;
        border-bottom: 2px solid #2e7bcf;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.title("🤖 ManusCode AI")
    st.markdown("---")

    # Language Toggle
    lang = st.radio("Language / ภาษา", ["English", "ไทย"], horizontal=True)

    t = {
        "api_label": "OpenAI API Key" if lang == "English" else "รหัส API OpenAI",
        "model_label": "Model" if lang == "English" else "รุ่นโมเดล",
        "clear_btn": "Clear Chat History" if lang == "English" else "ล้างประวัติการสนทนา",
        "about_title": "About" if lang == "English" else "เกี่ยวกับ",
        "about_desc": "**ManusCode AI** is an autonomous AI agent designed to generate and preview code instantly." if lang == "English" else "**ManusCode AI** คือเอเจนท์ AI อัจฉริยะที่ออกแบบมาเพื่อสร้างและดูตัวอย่างโค้ดได้ทันที",
        "instr_title": "Instructions:" if lang == "English" else "วิธีใช้งาน:",
        "instr_1": "1. Enter your API Key." if lang == "English" else "1. ใส่รหัส API Key ของคุณ",
        "instr_2": "2. Describe the web component or app you want." if lang == "English" else "2. อธิบายส่วนประกอบหรือแอปที่ต้องการ",
        "instr_3": "3. The AI will generate the code and show a live preview." if lang == "English" else "3. AI จะสร้างโค้ดและแสดงตัวอย่างให้เห็นทันที",
        "chat_header": "💬 Chat" if lang == "English" else "💬 สนทนา",
        "preview_header": "🚀 Preview & Code" if lang == "English" else "🚀 ตัวอย่างและโค้ด",
        "tab_preview": "🌐 Live Preview" if lang == "English" else "🌐 แสดงตัวอย่าง",
        "tab_code": "💻 Source Code" if lang == "English" else "💻 ซอร์สโค้ด",
        "input_placeholder": "Describe the code you want to build..." if lang == "English" else "อธิบายโค้ดที่คุณต้องการสร้าง...",
        "no_code": "No code generated yet. Describe something to see the preview." if lang == "English" else "ยังไม่มีโค้ดถูกสร้าง อธิบายบางอย่างเพื่อดูตัวอย่าง",
        "error_api": "Please enter your OpenAI API key in the sidebar." if lang == "English" else "กรุณาใส่ OpenAI API key ในแถบด้านข้าง",
        "download_btn": "Download Code" if lang == "English" else "ดาวน์โหลดโค้ด"
    }

    api_key = st.text_input(t["api_label"], type="password", help="Enter your OpenAI API key.")
    model = st.selectbox(t["model_label"], ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)

    st.markdown("---")
    st.markdown(f"### {t['about_title']}")
    st.markdown(t['about_desc'])

    st.markdown(f"**{t['instr_title']}**")
    st.markdown(t['instr_1'])
    st.markdown(t['instr_2'])
    st.markdown(t['instr_3'])

    if st.button(t["clear_btn"]):
        st.session_state.messages = []
        st.session_state.current_code = ""
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_code" not in st.session_state:
    st.session_state.current_code = ""

# Main UI layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader(t["chat_header"])

    # Chat container
    chat_container = st.container(height=650)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input(t["input_placeholder"]):
        if not api_key:
            st.error(t["error_api"])
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            try:
                client = OpenAI(api_key=api_key)

                system_prompt = f"""You are ManusCode AI, an expert autonomous coding agent.
                Your goal is to help users build web applications and components.
                When asked to create something, provide the complete, standalone HTML/CSS/JS code in a single block using ```html ... ```.
                Include any necessary CDN links (Tailwind CSS, FontAwesome, Lucide, etc.) to make it look professional.
                Current Language: {lang}
                Always provide high-quality, modern, and responsive designs."""

                with chat_container:
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        full_response = ""

                        stream = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                *st.session_state.messages
                            ],
                            stream=True,
                        )

                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")

                        message_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

                # Extract code block
                html_match = re.search(r"```html\n(.*?)```", full_response, re.DOTALL)
                if html_match:
                    st.session_state.current_code = html_match.group(1)
                else:
                    any_code_match = re.search(r"```(?:\w+)?\n(.*?)```", full_response, re.DOTALL)
                    if any_code_match:
                        st.session_state.current_code = any_code_match.group(1)

                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.subheader(t["preview_header"])

    tab1, tab2 = st.tabs([t["tab_preview"], t["tab_code"]])

    with tab1:
        if st.session_state.current_code:
            st.markdown(f'<div class="preview-window">', unsafe_allow_html=True)
            st.components.v1.html(st.session_state.current_code, height=700, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(t["no_code"])

    with tab2:
        if st.session_state.current_code:
            st.code(st.session_state.current_code, language="html")
            st.download_button(
                label=t["download_btn"],
                data=st.session_state.current_code,
                file_name="manus_code.html",
                mime="text/html"
            )
        else:
            st.info(t["no_code"])
