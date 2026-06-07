import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div class="header-container">
            <img src='{logo_url}' style='height:100px;' />
            <h1>SNAP<br/>CLASS</h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div class="header-dashboard">
            <img src='{logo_url}' style='height:85px;' />
            <h2>SNAP<br/>CLASS</h2>
        </div>
    """, unsafe_allow_html=True)