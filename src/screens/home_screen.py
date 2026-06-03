import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
def home_screen():


    header_home()
    style_background_home()
    style_base_layout()


    # --- ADD THIS CUSTOM STYLING ---
    st.markdown("""
    <style>
    /* Modern card look for the columns */
    div[data-testid="column"] {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    div[data-testid="column"]:hover {
        transform: translateY(-10px);
        background-color: rgba(255, 255, 255, 0.08);
    }
    /* Enhance the buttons */
    div.stButton > button {
        border-radius: 50px !important;
        padding: 0 30px !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # -------------------------------

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()