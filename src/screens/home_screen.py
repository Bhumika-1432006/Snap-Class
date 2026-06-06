import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Original logic preserved
    header_home()
    style_background_home()
    style_base_layout()

    # Extraordinary Professional Glassmorphism Styling
    # This targets Streamlit's internal layout engines directly to ensure it applies
    st.markdown("""
    <style>
    /* 1. Force the App Background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% -20%, #1e293b 0%, #0f172a 80%) !important;
    }

    /* 2. Target columns to turn them into Glassmorphism cards */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        padding: 40px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        text-align: center !important;
        transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    }
    
    [data-testid="column"]:hover {
        transform: translateY(-15px) scale(1.02) !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* 3. Refined Typography */
    h2 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        margin-bottom: 25px !important;
        letter-spacing: -0.5px;
    }

    /* 4. Premium Button Styling */
    div.stButton > button {
        border-radius: 16px !important;
        padding: 15px 40px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.5) !important;
        filter: brightness(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

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

    footer_home()