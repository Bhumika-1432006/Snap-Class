import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Initialize standard components
    header_home()
    style_background_home()
    style_base_layout()

    # Layout: Use the custom render_portal function for structural consistency
    col1, col2 = st.columns(2, gap="large")

    def render_portal(title, image_url, button_text, key):
        st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
        st.header(title)
        
        # Fixed-height image container for perfect vertical alignment
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(image_url)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # The button is pushed to the bottom by the CSS .content-wrapper
        if st.button(button_text, type='primary', icon=':material/arrow_outward:', icon_position='right', key=key):
            st.session_state['login_type'] = 'student' if 'student' in key else 'teacher'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        render_portal("I'm Student", "https://i.ibb.co/844D9Lrt/mascot-student.png", "Student Portal", "btn_student")

    with col2:
        render_portal("I'm Teacher", "https://i.ibb.co/CsmQQV6X/mascot-prof.png", "Teacher Portal", "btn_teacher")

    # --- PROFESSIONAL DARK-THEME & ALIGNMENT CSS ---
    st.markdown("""
    <style>
    /* 1. Deep Midnight Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }

    /* 2. Card Styling */
    div[data-testid="column"] {
        background: #1e293b !important;
        padding: 40px !important;
        border-radius: 24px !important;
        border: 1px solid #334155 !important;
    }

    /* 3. The Alignment Fixes */
    .content-wrapper {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        height: 100% !important;
    }

    .img-container {
        height: 220px !important; /* Fixed height forces alignment */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 20px 0 !important;
    }

    .img-container img {
        max-height: 200px !important;
        width: auto !important;
    }

    /* 4. Button Alignment: Forces buttons to the bottom of the card */
    div.stButton {
        margin-top: auto !important;
        width: 100% !important;
    }
    
    div.stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
    }

    /* 5. Typography */
    h2 {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()