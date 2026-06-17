import streamlit as st

def landing_screen():
    st.title("Welcome to SnapClass! 👋")
    st.subheader("Attendance made simple with AI.")
    
    st.markdown("""
    ### How it works:
    1. **For Teachers:** Create subjects, share your unique code, and take attendance using Face or Voice recognition.
    2. **For Students:** Enroll in your classes using the code or QR link and get verified automatically!
    """)
    
    if st.button("Get Started", type="primary"):
        # We set this to 'home' so the app knows to move to the login selection
        st.session_state['login_type'] = 'home'
        st.rerun()