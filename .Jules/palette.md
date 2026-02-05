## 2026-02-05 - Improved Streamlit Onboarding
**Learning:** For minimal Streamlit apps, adding a "Getting Started" sidebar and a welcoming toast provides immediate guidance and delight without cluttering the main UI. Using `st.session_state` to guard `st.toast` prevents repetitive notifications on every re-run.
**Action:** Use a sidebar for onboarding instructions and `st.session_state` for one-time feedback in future Streamlit tasks.
