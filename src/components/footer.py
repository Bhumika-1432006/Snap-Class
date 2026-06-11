import streamlit as st


def footer_home():
    logo_url = "https://assets.streamlinehq.com/image/private/w_200,h_200,ar_1/f_auto/v1/icons/kawaii-emoji/-symbols/-symbols/u+1f171-em1eez07mrbn93sx69c6c.png?_a=DATAiZAAZAA0"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:white;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://assets.streamlinehq.com/image/private/w_200,h_200,ar_1/f_auto/v1/icons/kawaii-emoji/-symbols/-symbols/u+1f171-em1eez07mrbn93sx69c6c.png?_a=DATAiZAAZAA0"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:black;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)