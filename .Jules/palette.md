## 2025-05-22 - Descriptive Documentation Links
**Learning:** Documentation links in the UI should use descriptive text instead of raw URLs to improve accessibility for screen readers and make the interface cleaner.
**Action:** Always replace raw URLs with meaningful link text (e.g., 'Streamlit Documentation' instead of 'docs.streamlit.io').

## 2025-05-22 - Non-intrusive Feedback in Streamlit
**Learning:** Using `st.toast` for welcoming users provides a delightful, non-intrusive feedback mechanism, but it should be guarded by `st.session_state` to ensure it only appears once per session.
**Action:** Implement `st.toast` with a session state check for one-time welcome messages.
