import streamlit as st
import base64
import os
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "images"))

def convert_local_file_to_base64(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def home_screen():
    # Injecting optimized styling for maximum visibility and brand color consistency
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap');

            :root {
                --color-primary: #18A4A9;
                --color-primary-dark: #0E7A7E;
                --color-secondary: #2B2D6E;
                --color-accent: #F5A623;
                --color-text: #1E2430;
                --color-text-muted: #52606D;
                --color-surface: rgba(255, 255, 255, 0.65);
                --color-surface-border: rgba(255, 255, 255, 0.9);
                --font-heading: 'Poppins', sans-serif;
                --font-body: 'Inter', sans-serif;
            }

            /* Hide Streamlit components */
            [data-testid="stHeader"] { display: none !important; }

            /* Apply the same background gradient as the landing page */
            .stApp {
                background: linear-gradient(135deg, #EAF7F8 0%, #DDEFF2 55%, #E9E4F5 100%) !important;
            }

            /* Role-card styling, scoped to the role-cards container only */
            .st-key-role-cards div[data-testid="stColumn"] {
                background: #FFFFFF !important;
                border: 1px solid var(--color-surface-border) !important;
                border-radius: 24px !important;
                padding: 2.75rem 2.5rem !important;
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.12) !important;
                transition: transform 0.35s ease, box-shadow 0.35s ease !important;
                text-align: center;
                animation: fadeInUp 0.7s ease both;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 22px !important;
            }

            .st-key-role-cards h2 {
                margin-bottom: 0 !important;
            }

            .role-desc {
                color: var(--color-text-muted) !important;
                font-size: 1.05rem !important;
                line-height: 1.6 !important;
                max-width: 380px;
                margin: 0 !important;
            }

            .st-key-role-cards div[data-testid="stColumn"]:nth-of-type(2) {
                animation-delay: 0.1s;
            }

            .st-key-role-cards div[data-testid="stColumn"]:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(24, 164, 169, 0.22) !important;
            }

            /* Update SNAPCLASS AI color to brand teal */
            .snapclass-title {
                color: var(--color-primary) !important;
                font-weight: 900 !important;
            }

            /* Ultra-readable headers */
            h1 {
                font-family: var(--font-heading) !important;
                color: var(--color-text) !important;
                font-weight: 900 !important;
            }
            h2 {
                font-family: var(--font-heading) !important;
                color: var(--color-secondary) !important;
                font-weight: 700 !important;
                font-size: 2.2rem !important;
                margin-bottom: 20px !important;
            }
            p, span, label {
                font-family: var(--font-body) !important;
            }

            /* Teal gradient pill buttons, matching the landing page CTA */
            div.stButton {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
            }
            div.stButton > button {
                background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
                color: #ffffff !important;
                font-family: var(--font-heading) !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 50px !important;
                padding: 14px 34px !important;
                font-size: 1.05rem !important;
                box-shadow: 0 8px 22px rgba(24, 164, 169, 0.35) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            }
            div.stButton > button:hover {
                transform: translateY(-3px) scale(1.03);
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.45) !important;
                color: #ffffff !important;
            }
            div.stButton > button:active {
                transform: translateY(-1px) scale(0.99);
            }

            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(24px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Role illustration containers */
            .role-image-container {
                width: 85%;
                max-width: 400px;
                aspect-ratio: 1 / 1;
                margin: 0 auto 14px auto;
                background: none;
                border: none;
                box-shadow: none;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .role-image-container img {
                width: 100%;
                height: 100%;
                object-fit: contain;
            }
        </style>
    """, unsafe_allow_html=True)

    style_base_layout()
    header_home()

    st.write("<br><br>", unsafe_allow_html=True)

    with st.container(key="role-cards"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.header("I'm Student")
            st.markdown('<p class="role-desc">Register and join your classes in seconds.</p>', unsafe_allow_html=True)
            student_img_b64 = convert_local_file_to_base64(os.path.join(IMAGES_DIR, "role_student.svg"))
            st.markdown(
                f'<div class="role-image-container"><img src="data:image/svg+xml;base64,{student_img_b64}"></div>',
                unsafe_allow_html=True
            )
            if st.button('Student Portal', type='primary'):
                st.session_state['login_type']='student'
                st.rerun()

        with col2:
            st.header("I'm Teacher")
            st.markdown('<p class="role-desc">Create classes and manage attendance effortlessly.</p>', unsafe_allow_html=True)
            teacher_img_b64 = convert_local_file_to_base64(os.path.join(IMAGES_DIR, "role_teacher.svg"))
            st.markdown(
                f'<div class="role-image-container"><img src="data:image/svg+xml;base64,{teacher_img_b64}"></div>',
                unsafe_allow_html=True
            )
            if st.button('Teacher Portal', type='primary'):
                st.session_state['login_type']='teacher'
                st.rerun()

    footer_home()
