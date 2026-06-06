import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    def render_portal(title, image_url, button_text, key, img_class=""):
        st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
        st.header(title)
        st.markdown(f'<div class="img-container {img_class}">', unsafe_allow_html=True)
        st.image(image_url)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button(button_text, type='primary', icon=':material/arrow_outward:', icon_position='right', key=key):
            st.session_state['login_type'] = 'student' if 'student' in key else 'teacher'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        render_portal("I'm Student", "https://i.ibb.co/844D9Lrt/mascot-student.png", "Student Portal", "btn_student", "student-img")

    with col2:
        # Teacher image class set to make it slightly larger than the previous version
        render_portal("I'm Teacher", "https://i.ibb.co/CsmQQV6X/mascot-prof.png", "Teacher Portal", "btn_teacher", "teacher-img")

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    div[data-testid="column"] {
        background: #1e293b !important;
        padding: 40px !important;
        border-radius: 24px !important;
        border: 1px solid #334155 !important;
    }

    .content-wrapper {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        height: 100% !important;
    }
    
    .img-container {
        height: 220px !important; 
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-end !important;
        margin-bottom: 20px !important;
    }
    
    /* Standard Student Image */
    .student-img img {
        width: 150px !important;
        object-fit: contain !important;
    }
    
    /* Teacher image scaled up to be larger */
    .teacher-img img {
        width: 190px !important; 
        object-fit: contain !important;
    }

    div.stButton {
        margin-top: auto !important;
        width: 100% !important;
    }
    
    div.stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
    }
    
    h2 {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()