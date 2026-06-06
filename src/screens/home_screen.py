import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Initialize standard components
    header_home()
    style_background_home()
    style_base_layout()

    # Content Area
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_student'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_teacher'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # --- EXTRAVAGANT NEUMORPHIC STYLING ---
    st.markdown("""
    <style>
    /* 1. Deep Vibrant Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #4c1d95 0%, #db2777 100%) !important;
    }

    /* 2. Neumorphic Floating Cards */
    div[data-testid="column"] {
        background: #ffffff !important;
        padding: 50px !important;
        border-radius: 40px !important;
        border: none !important;
        text-align: center !important;
        transition: all 0.5s ease !important;
        /* The signature soft-shadow look */
        box-shadow: 20px 20px 60px #3b0764, -20px -20px 60px #9d174d !important;
    }
    
    div[data-testid="column"]:hover {
        transform: translateY(-10px) !important;
        box-shadow: 30px 30px 80px #3b0764, -30px -30px 80px #9d174d !important;
    }

    /* 3. Typography */
    h2 {
        color: #1e293b !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-weight: 800 !important;
        margin-bottom: 25px !important;
    }

    /* 4. Sleek Action Buttons */
    div.stButton > button {
        border-radius: 20px !important;
        padding: 15px 40px !important;
        font-weight: 700 !important;
        background: #db2777 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(219, 39, 119, 0.3) !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        background: #be185d !important;
        transform: scale(1.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()