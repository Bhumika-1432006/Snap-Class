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

    # --- PROFESSIONAL DARK-TONED STYLING ---
    st.markdown("""
    <style>
    /* 1. Deep Midnight Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }

    /* 2. Sleek Dark Cards */
    div[data-testid="column"] {
        background: #1e293b !important;
        padding: 50px !important;
        border-radius: 24px !important;
        border: 1px solid #334155 !important;
        text-align: center !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
    }
    
    div[data-testid="column"]:hover {
        transform: translateY(-5px) !important;
        background: #334155 !important;
        border: 1px solid #475569 !important;
    }

    /* 3. Refined Typography */
    h2 {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 25px !important;
    }

    /* 4. Elegant Action Buttons */
    div.stButton > button {
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-weight: 500 !important;
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        transition: 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #2563eb !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()