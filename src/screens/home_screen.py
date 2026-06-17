import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    # Injecting optimized styling
    st.markdown("""
        <style>
            /* Hide Streamlit components */
            [data-testid="stHeader"] { display: none !important; }
            
            /* Apply exact Landing Page background */
            .stApp { 
                background: linear-gradient(135deg, #e0f2f7 0%, #d1eaf0 100%) !important; 
            }
            
            /* Reduced padding and size for smaller cards */
            div[data-testid="stColumn"] {
                background: #FFFFFF !important; 
                border: 2px solid #6A329F !important; 
                border-radius: 2rem !important;
                padding: 1.5rem !important; 
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
                text-align: center;
            }
            
            /* Headers matching the violet brand color */
            h2 { 
                color: #6A329F !important; 
                font-weight: 900 !important; 
                font-size: 1.8rem !important; 
                margin-bottom: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    style_base_layout()
    header_home()

    st.write("<br><br>", unsafe_allow_html=True)

    # Added spacer columns [1, 2, 2, 1] to make the two center cards smaller
    col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1])

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=250)
        st.write("<br>", unsafe_allow_html=True)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=250)
        st.write("<br>", unsafe_allow_html=True)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()

def footer_home():
    logo_url = "https://www.pngarts.com/files/3/Letter-B-PNG-High-Quality-Image.png"
    
    st.markdown(f"""
        <div style="margin-top:4rem; display:flex; gap:6px; justify-content:center; align-items:center;">
            <p style="font-weight:bold; color:#6A329F; margin:0;"> Created with ❤️ by </p>  
            <img src='{logo_url}' style='max-height:25px' />
        </div>
    """, unsafe_allow_html=True)