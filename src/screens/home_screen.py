import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    def render_portal(title, image_url, button_text, key, extra_class=""):
        st.markdown(f'<div class="content-wrapper {extra_class}">', unsafe_allow_html=True)
        st.header(title)
        # Adding a specific class to the image container
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(image_url)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button(button_text, type='primary', icon=':material/arrow_outward:', icon_position='right', key=key):
            st.session_state['login_type'] = 'student' if 'student' in key else 'teacher'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        render_portal("I'm Student", "https://i.ibb.co/844D9Lrt/mascot-student.png", "Student Portal", "btn_student")

    with col2:
        # Added 'teacher-card' class here
        render_portal("I'm Teacher", "https://i.ibb.co/CsmQQV6X/mascot-prof.png", "Teacher Portal", "btn_teacher", "teacher-card")

    st.markdown("""
    <style>
    /* ... (Your existing styles remain the same) ... */
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
        justify-content: space-between !important;
        height: 100% !important;
        gap: 20px !important;
    }
    .content-wrapper img {
        width: 150px !important;
        height: 150px !important;
        object-fit: contain !important;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        background: #3b82f6 !important;
        color: white !important;
    }

    /* THE SPECIFIC FIX: Shift Teacher Image Down */
    .teacher-card .img-container {
        margin-top: 50px !important; /* Adjust this number to shift more/less */
    }
    </style>
    """, unsafe_allow_html=True)

    footer_home()