import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Injecting optimized styling for maximum visibility and brand color consistency
    st.markdown("""
        <style>
            /* Hide Streamlit components */
            [data-testid="stHeader"] { display: none !important; }
            
            /* Apply exact Landing Page background */
            .stApp { 
                background: linear-gradient(135deg, #e0f2f7 0%, #d1eaf0 100%) !important; 
            }
            
            /* High-Visibility Card Style */
            div[data-testid="stColumn"] {
                background: #FFFFFF !important; 
                border: 2px solid #6A329F !important; 
                border-radius: 2rem !important;
                padding: 3rem !important;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15) !important;
                transition: transform 0.3s ease !important;
                text-align: center;
            }
            
            div[data-testid="stColumn"]:hover {
                transform: translateY(-10px);
            }
            
            /* Update SNAPCLASS AI color to Violet */
            .snapclass-title {
                color: #6A329F !important;
                font-weight: 900 !important;
            }
            
            /* Ultra-readable Headers */
            h1 { color: #6A329F !important; font-weight: 900 !important; }
            h2 { 
                color: #6A329F !important; 
                font-weight: 900 !important; 
                font-size: 2.5rem !important; 
                margin-bottom: 20px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    style_base_layout()
    header_home()

    # Apply the brand color to the top title
    st.markdown("<h1 style='text-align: center;'>SNAPCLASS AI</h1>", unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=350)
        st.write("<br>", unsafe_allow_html=True)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=350)
        st.write("<br>", unsafe_allow_html=True)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()