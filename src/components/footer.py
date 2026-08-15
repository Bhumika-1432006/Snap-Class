import streamlit as st


def footer_home():
    logo_url = "https://www.pngarts.com/files/3/Letter-B-PNG-High-Quality-Image.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center;">
            <p style="font-weight:bold; color:#2B2D6E; margin:0;"> Created with ❤️ by </p>
            <img src='{logo_url}' style='max-height:25px' />
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://www.pngarts.com/files/3/Letter-B-PNG-High-Quality-Image.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:var(--color-text, #1E2430);"> Created with ❤️ by </p>
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)