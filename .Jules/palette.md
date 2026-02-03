# Palette's UX/Accessibility Journal

## 2025-05-14 - Session-Guarded Feedback
**Learning:** In Streamlit, interactive elements like toasts or balloons can be overwhelming if they trigger on every rerun (which happens on every user interaction). Guarding them with `st.session_state` ensures they only provide delight without becoming a nuisance.
**Action:** Always use a session state flag to trigger one-time feedback or welcome messages in Streamlit apps.

## 2025-05-14 - Documentation Link Accessibility
**Learning:** Raw URLs in the UI are difficult for screen readers to interpret and provide poor context.
**Action:** Always use descriptive text like "Streamlit Documentation" for links instead of displaying the raw URL.
