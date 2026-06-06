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

    # --- CHEERFUL & VIBRANT STYLING ---
    st.markdown("""
    <style>
    /* 1. Cheerful Sunset/Vibrant Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%) !important;
    }

    /* 2. Soft, Bouncy Cards */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 45px !important;
        border-radius: 50px !important;
        border: 4px solid rgba(255, 255, 255, 0.5) !important;
        text-align: center !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15) !important;
    }
    
    [data-testid="column"]:hover {
        transform: translateY(-20px) rotate(2deg) !important;
        background: #ffffff !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.25) !important;
    }

    /* 3. Playful Typography */
    h2 {
        color: #5D3FD3 !important;
        font-family: 'Comic Sans MS', 'Arial', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
    }

    /* 4. Energetic Buttons */
    div.stButton > button {
        border-radius: 30px !important;
        padding: 18px 40px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        background: #5D3FD3 !important;
        color: white !important;
        border: none !important;
        transition: 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #FF6A88 !important;
        transform: scale(1.08) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()