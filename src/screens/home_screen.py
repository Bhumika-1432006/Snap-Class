import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home

def home_screen():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@300;400;600&display=swap');
            
            /* Extravagant Deep Purple Gradient */
            .stApp {
                background: radial-gradient(circle at top right, #4c1d95, #2e1065, #1e1b4b) !important;
                background-attachment: fixed !important;
            }
            
            /* Professional Glassmorphism Cards */
            .stApp div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.03) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding: 3rem !important;
                border-radius: 2.5rem !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
                transition: transform 0.4s ease, box-shadow 0.4s ease !important;
            }

            /* Hover Effect for Professional Polish */
            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }
            
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                color: #ffffff !important;
                letter-spacing: 2px !important;
                text-transform: uppercase;
            }
            
            button {
                background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
                font-weight: 600 !important;
                letter-spacing: 1px !important;
            }
            
            button:hover {
                filter: brightness(1.2) !important;
                transform: scale(1.05) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    header_home()

    # Add a slight top margin for spacing
    st.write("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=140)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        # Visual compensation for mascot size
        st.write("<br>", unsafe_allow_html=True) 
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=160)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()