import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home

def home_screen():
    st.markdown("""
        <style>
            /* Original Font Definitions preserved */
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
            
            .stApp {
                background: radial-gradient(circle at 100% 0%, #3d1b66, #210e3d, #140826) !important;
                background-attachment: fixed !important;
            }
            
            /* Enhanced Card Depth */
            .stApp div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.04) !important;
                backdrop-filter: blur(25px) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                padding: 3rem !important;
                border-radius: 2.5rem !important;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), inset 0 0 1px rgba(255,255,255,0.2) !important;
                transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-15px) scale(1.02) !important;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.25) !important;
            }
            
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                color: #ffffff !important;
                text-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }
            
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                color: #ffffff !important;
            }
            
            h3, h4, p, button {
                font-family: 'Outfit', sans-serif !important;
            }
            
            /* Premium Button Polish */
            button {
                background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
                border-radius: 1.5rem !important;
                padding: 12px 25px !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                transition: transform 0.3s ease !important;
            }
            
            button:hover {
                transform: scale(1.08) !important;
                filter: brightness(1.2) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    header_home()

    # Layout Spacing
    st.write("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.write("<br>", unsafe_allow_html=True) 
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()