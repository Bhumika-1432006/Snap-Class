import streamlit as st
import base64
import os

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="SnapClass AI")

def convert_local_file_to_base64(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def landing_screen():
    # --- LIGHT THEME CSS ---
    st.markdown("""
        <style>
        /* Light Theme Palette */
        .stApp { background-color: #ffffff; color: #1e293b; }
        
        .uniform-image-container {
            width: 100%; height: 400px; /* Fixed height for uniformity */
            border-radius: 20px; overflow: hidden;
            display: flex; align-items: center; justify-content: center;
            background-color: #f1f5f9; /* Light gray background */
            margin: 40px 0; /* Extra space around images */
        }
        .uniform-image-container img {
            max-width: 100%; height: 100%; object-fit: cover;
        }
        
        .text-block { 
            padding: 40px; 
            border-radius: 20px; 
            background: #ffffff;
            margin: 40px 0;
        }
        h2 { color: #0f172a !important; font-size: 2.2rem !important; }
        p { color: #64748b !important; font-size: 1.2rem !important; line-height: 1.8 !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO ---
    st.markdown("""
        <div style="text-align: center; padding: 80px 0 60px 0;">
            <h1 style="font-size: 4.5rem; font-weight: 900; color: #0f172a;">SNAPCLASS <span style="color:#18a4a9">AI</span></h1>
            <p style="font-size: 1.5rem; color: #64748b; margin-top: 20px;">Intelligent Attendance Automation for Modern Classrooms.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- ACTION BUTTON ---
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state['login_type'] = 'home'
            st.rerun()

    # --- CONTENT ROWS ---
    steps = [
        ("Face & Voice Verification", "Leverage advanced biometric neural nets to verify student presence with sub-second latency.", "images/step1.png"),
        ("Smart Classroom Intake", "Ingest student rosters and schedule metadata through our centralized management portal.", "images/step2.png"),
        ("Real-time Attendance Audits", "Verify classroom integrity with automated spoof-detection and environment analysis.", "images/step3.png"),
        ("Predictive Classroom Insights", "Analyze engagement patterns and attendance trends through clean, secure telemetry metrics.", "images/step4.png")
    ]

    for i, (title, desc, img_path) in enumerate(steps):
        img_b64 = convert_local_file_to_base64(img_path)
        img_html = f'<div class="uniform-image-container"><img src="data:image/png;base64,{img_b64}"></div>'
        text_html = f'<div class="text-block"><h2>{title}</h2><p>{desc}</p></div>'
        
        # Increased gap between rows
        st.write("<br><br>", unsafe_allow_html=True) 
        
        c1, c2 = st.columns([1.2, 1])
        if i % 2 == 0:
            with c1: st.markdown(img_html, unsafe_allow_html=True)
            with c2: st.markdown(text_html, unsafe_allow_html=True)
        else:
            with c1: st.markdown(text_html, unsafe_allow_html=True)
            with c2: st.markdown(img_html, unsafe_allow_html=True)

    # --- MISSION ---
    st.markdown("""
        <div style="margin: 80px 0; padding: 60px; background: #f8fafc; border-radius: 30px; text-align: center;">
            <h3 style="color: #18a4a9;">Our Mission</h3>
            <p style="max-width: 800px; margin: 20px auto;">Bridging the gap between classroom efficiency and identity security. We don't just track attendance—we ensure verified, stress-free learning environments.</p>
        </div>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    landing_screen()