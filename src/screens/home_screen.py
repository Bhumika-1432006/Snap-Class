import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Keep original logic
    header_home()
    style_background_home()
    style_base_layout()

    # Extraordinary Professional Glassmorphism Styling
    st.markdown("""
    <style>
    /* Global Page Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e293b 0%, #0f172a 80%);
        color: #f8fafc;
    }

    /* Extraordinary Glassmorphism Cards */
    .portal-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .portal-card:hover {
        transform: translateY(-15px) scale(1.02);
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Refined Typography */
    h2 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        margin-bottom: 25px !important;
        letter-spacing: -0.5px;
    }

    /* Premium Button Styling */
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
        # Wrap content in a div with the class 'portal-card'
        st.markdown('<div class="portal-card">', unsafe_allow_html=True)
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_student'):
            st.session_state['login_type']='student'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Wrap content in a div with the class 'portal-card'
        st.markdown('<div class="portal-card">', unsafe_allow_html=True)
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', key='btn_teacher'):
            st.session_state['login_type']='teacher'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    footer_home()