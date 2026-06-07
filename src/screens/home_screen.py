import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home

def home_screen():
    st.markdown("""
        <style>
            /* --- HIDE TOP BAR --- */
            [data-testid="stHeader"] {
                display: none !important;
            }

            /* Restoring your original font imports */
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
            
            /* Extravagant Radial Background */
            .stApp {
                background: radial-gradient(circle at top right, #4c1d95, #2e1065, #1e1b4b) !important;
                background-attachment: fixed !important;
            }
            
            /* Professional Glassmorphism Cards */
            .stApp div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.03) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding: 3rem !important;
                border-radius: 2.5rem !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
                transition: transform 0.4s ease, box-shadow 0.4s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5) !important;
            }
            
            /* Restoring your original font family settings */
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                color: white !important;
            }
            
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                color: white !important;
            }
            
            h3, h4, p {
                font-family: 'Outfit', sans-serif !important;
            }
            
            button {
                font-family: 'Outfit', sans-serif !important;
                background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
                border-radius: 1.5rem !important;
                border: none !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

    header_home()

    # Spacing for alignment
    st.write("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        # Increased mascot width
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=180)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        # Increased mascot width
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=200)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()