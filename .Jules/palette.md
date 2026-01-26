## 2026-01-26 - [Streamlit One-time Toast Notification]
**Learning:** To prevent `st.toast` from appearing on every app re-run (which happens on every user interaction in Streamlit), it should be guarded by a `st.session_state` flag. This ensures the welcoming message only "pops" once per session, providing delight without becoming intrusive.
**Action:** Always use `if 'key' not in st.session_state: st.toast(...); st.session_state.key = True` for session-start notifications.
