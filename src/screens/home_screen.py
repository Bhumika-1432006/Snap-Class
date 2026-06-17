import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Injecting unified styling
    st.markdown("""
        <style>
            /* Hide Streamlit components */
            [data-testid="stHeader"] { display: none !important; }
            
            /* Apply exact Landing Page background */
            .stApp { 
                background: linear-gradient(135deg, #e0f2f7 0%, #d1eaf0 100%) !important; 
            }
            
            /* Glassmorphism Card Style */
            div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.5) !important;
                backdrop-filter: blur(15px) !important;
                border: 1px solid rgba(255, 255, 255, 0.8) !important;
                border-radius: 2rem !important;
                padding: 3rem !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
                transition: transform 0.3s ease !important;
                text-align: center;
            }
            
            div[data-testid="stColumn"]:hover {
                transform: translateY(-10px);
            }
            
            /* Headers matching the violet brand color */
            h2 { color: #6A329F !important; font-weight: 800 !important; font-size: 2.2rem !important; }
        </style>
    """, unsafe_allow_html=True)

    # Note: Ensure style_background_home() does not override the .stApp background
    style_base_layout()
    header_home()

    st.write("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        # Images set to 350 for maximum impact
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=350)
        st.write("<br>", unsafe_allow_html=True)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        # Images set to 350 for maximum impact
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=350)
        st.write("<br>", unsafe_allow_html=True)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()