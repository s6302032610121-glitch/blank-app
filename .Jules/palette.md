## 2026-01-27 - [Streamlit Branding & Onboarding]
**Learning:** For minimal Streamlit apps, immediate branding via `st.set_page_config` and a welcoming `st.toast` (guarded by `st.session_state`) significantly improve the "first-run" experience. Adding an informative sidebar with descriptive links also enhances accessibility and discoverability.
**Action:** Always check for missing `st.set_page_config` in Streamlit apps and consider adding a session-state-aware welcome toast for new users.
