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
    # --- ENHANCED CSS INJECTION ---
    st.markdown("""
        <style>
        .interactive-pic-container {
            width: 100%; border-radius: 30px; overflow: hidden; 
            background: linear-gradient(145deg, #0d4354, #0b3846);
            padding: 12px; margin-top: 15px; 
            border: 1px solid rgba(24, 164, 169, 0.2);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
            cursor: pointer;
        }
        .interactive-pic-container:hover {
            transform: translateY(-12px) scale(1.02); 
            box-shadow: 0 25px 50px -12px rgba(24, 164, 169, 0.3);
            border-color: rgba(24, 164, 169, 0.6);
        }
        .interactive-pic-container img {
            width: 100%; height: auto; border-radius: 20px;
            filter: brightness(1.05) contrast(1.1);
        }
        .text-block { 
            margin-top: 60px; padding: 40px; 
            background: rgba(255, 255, 255, 0.03);
            border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        .text-block:hover { background: rgba(255, 255, 255, 0.06); }
        h2 { margin-bottom: 20px !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO HEADER ---
    st.markdown("""
        <div style="text-align: center; padding: 60px 0 40px 0;">
            <h1 style="font-size: 4.5rem; font-weight: 900; margin: 0; letter-spacing: -2px;
                       background: linear-gradient(to right, #ffffff, #18a4a9);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                SNAPCLASS AI
            </h1>
            <p style="font-size: 1.4rem; color: #94a3b8; margin-top: 15px; font-weight: 400;">
                Advanced Attendance Automation & Biometric Verification
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- ACTION BUTTON ---
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Get Started Now", use_container_width=True):
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
        st.write("<br>", unsafe_allow_html=True)
        img_b64 = convert_local_file_to_base64(img_path)
        img_html = f'<div class="interactive-pic-container"><img src="data:image/png;base64,{img_b64}"></div>'
        text_html = f'<div class="text-block"><h2>{title}</h2><p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.8;">{desc}</p></div>'
        
        c1, c2 = st.columns([1.1, 0.9])
        if i % 2 == 0:
            with c1: st.markdown(img_html, unsafe_allow_html=True)
            with c2: st.markdown(text_html, unsafe_allow_html=True)
        else:
            with c1: st.markdown(text_html, unsafe_allow_html=True)
            with c2: st.markdown(img_html, unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("""
        <div style="margin-top: 80px; padding: 40px; background: linear-gradient(135deg, rgba(24, 164, 169, 0.1), rgba(0,0,0,0)); 
                    border-radius: 24px; border: 1px solid rgba(24, 164, 169, 0.2);">
            <p style="margin: 0; color: #ffffff; line-height: 1.7; font-size: 1.1rem; text-align: center;">
                <b style="color: #18a4a9;">MISSION:</b> Bridging the gap between classroom efficiency and identity security.
            </p>
        </div>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    landing_screen()