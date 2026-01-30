## 2025-05-14 - [Streamlit Welcome Toast]
**Learning:** To implement non-intrusive UI feedback in Streamlit, use 'st.toast' guarded by 'st.session_state' logic to ensure the notification only appears once per session, avoiding repetitive popups on every script re-run.
**Action:** Always use session state to manage the lifecycle of transient UI elements like toasts or one-time instructions in Streamlit apps.
