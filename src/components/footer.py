import streamlit as st


def footer_home():
    logo_url = "https://png.pngtree.com/png-vector/20250321/ourmid/pngtree-colorful-and-vibrant-brush-strokes-forming-the-letter-b-with-splashes-png-image_15843522.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:white;"> Created with ❤️ by</p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)

# since we hvae two different styles in footer that is in home and differnt in dashboard 


def footer_dashboard():
    logo_url = "https://png.pngtree.com/png-vector/20250321/ourmid/pngtree-colorful-and-vibrant-brush-strokes-forming-the-letter-b-with-splashes-png-image_15843522.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:black;"> Created with ❤️ by</p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)