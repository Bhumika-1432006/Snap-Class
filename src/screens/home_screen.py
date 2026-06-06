import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_student'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_teacher'):
            st.session_state['login_type']='teacher'
            st.rerun()

    # --- THE EXTRAVAGANT CSS INJECTION ---
    st.markdown("""
    <style>
    /* 1. Deep Space Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #0f172a 50%, #020617 100%) !important;
    }

    /* 2. Extravagant Glowing Glass Cards */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        padding: 50px !important;
        border-radius: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        text-align: center !important;
        transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 0 1px rgba(255,255,255,0.1) !important;
    }
    
    [data-testid="column"]:hover {
        transform: translateY(-20px) scale(1.05) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 30px 60px rgba(30, 58, 138, 0.6), inset 0 0 0 1px rgba(255,255,255,0.2) !important;
    }

    /* 3. Glowing Typography */
    [data-testid="column"] h2 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(255,255,255,0.3) !important;
    }

    /* 4. Neon-Border Button */
    div.stButton > button {
        border-radius: 20px !important;
        padding: 18px 50px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border: 2px solid rgba(59, 130, 246, 0.5) !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        color: white !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 5px 15px rgba(29, 78, 216, 0.4) !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.8) !important;
        transform: scale(1.05) !important;
        border-color: #60a5fa !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()