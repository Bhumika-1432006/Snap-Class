import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    # Highly specific CSS block to override internal Streamlit styling
    st.markdown("""
    <style>
    /* 1. Force the Main App Container Background */
    div.stApp {
        background: radial-gradient(circle at 50% -20%, #1e293b 0%, #0f172a 80%) !important;
    }

    /* 2. Target the column containers more specifically to override base_layout */
    div[data-testid="column"] {
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
    
    div[data-testid="column"]:hover {
        transform: translateY(-15px) scale(1.02) !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* 3. Force Header Color Override */
    div[data-testid="column"] h2 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    /* 4. Force Button Styling */
    div[data-testid="column"] div.stButton > button {
        border-radius: 16px !important;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 40px !important;
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