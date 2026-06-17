import streamlit as st


def footer_home():
    logo_url = "https://www.pngarts.com/files/3/Letter-B-PNG-High-Quality-Image.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center;">
            <p style="font-weight:bold; color:#6A329F; margin:0;"> Created with ❤️ by </p>  
            <img src='{logo_url}' style='max-height:25px' />
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://www.pngarts.com/files/3/Letter-B-PNG-High-Quality-Image.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:black;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)