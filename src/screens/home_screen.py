import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home

def home_screen():
    # Styled block with your original fonts and new purple theme
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');
            
            .stApp {
                background: linear-gradient(135deg, #2b1055 0%, #45217a 50%, #2b1055 100%) !important;
                background-attachment: fixed !important;
            }
            
            .stApp div[data-testid="stColumn"] {
                background-color: rgba(255, 255, 255, 0.05) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding: 2.5rem !important;
                border-radius: 2rem !important;
                text-align: center;
            }
            
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                color: white !important;
                font-size: 3.5rem !important;
            }
            
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                color: white !important;
                font-size: 2rem !important;
            }
            
            p, button {
                font-family: 'Outfit', sans-serif !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Render components
    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.write(" ") 
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()