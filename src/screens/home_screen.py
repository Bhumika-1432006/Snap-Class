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

    # --- THE MOST EXTRAVAGANT STYLING YET ---
    st.markdown("""
    <style>
    /* 1. Animated Background Gradient */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #1e1b4b);
        background-size: 400% 400% !important;
        animation: gradient 15s ease infinite !important;
    }

    /* 2. Glass Cards with Animated Border Gradient */
    [data-testid="column"] {
        position: relative;
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        padding: 60px !important;
        border-radius: 40px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        text-align: center !important;
        transition: 0.6s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5) !important;
    }
    
    [data-testid="column"]:hover {
        transform: translateY(-25px) scale(1.06) !important;
        border: 2px solid rgba(59, 130, 246, 0.5) !important;
        box-shadow: 0 0 50px rgba(59, 130, 246, 0.3) !important;
    }

    /* 3. Text & Header Extravagance */
    h2 {
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 900 !important;
        margin-bottom: 30px !important;
    }

    /* 4. Liquid-Fill Button Effect */
    div.stButton > button {
        border-radius: 25px !important;
        padding: 20px 60px !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        border: none !important;
        transition: 0.4s !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    div.stButton > button:hover {
        transform: scale(1.1) !important;
        filter: hue-rotate(45deg);
        box-shadow: 0 0 40px rgba(124, 58, 237, 0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()