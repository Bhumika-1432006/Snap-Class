import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home

def home_screen():
    st.markdown("""
        <style>
            /* --- HIDE TOP BAR --- */
            [data-testid="stHeader"] { display: none !important; }
            
            /* --- ORIGINAL FONT SETUP --- */
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 !important;
                margin-bottom:0rem !important;
                color: #1e3a5f !important;
            }
            
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
                color: #1e3a5f !important;
            }
            
            h3, h4, p {
                font-family: 'Outfit', sans-serif !important;    
                color: #333 !important;
            }

            /* --- DRAMATIC ANIMATED STRIATIONS --- */
            .stApp {
                background: linear-gradient(-45deg, #1d5863, #2a7380, #3a8a9a, #2a7380) !important;
                background-size: 400% 400% !important;
                animation: gradientShift 15s ease infinite !important;
                background-attachment: fixed !important;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* White Pop-out Cards */
            .stApp div[data-testid="stColumn"] {
                background: #ffffff !important;
                border-radius: 2.5rem !important;
                padding: 3rem !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
                transition: transform 0.3s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-5px);
            }
            
            /* --- BUTTONS --- */
            button {
                font-family: 'Outfit', sans-serif !important;
                background: #2a7380 !important;
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
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=180)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.write("<br>", unsafe_allow_html=True) 
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=200)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()