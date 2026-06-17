import streamlit as st
import base64

# Ensure this function is available in your scope
def convert_local_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def landing_screen():
    # --- 1. GLOBAL STYLES & HERO HEADER ---
    st.markdown("""
        <style>
        .interactive-pic-container {
            width: 100%; border-radius: 24px; overflow: hidden; background-color: #0b3846; 
            padding: 10px; margin-top: 15px; border: 1px solid rgba(24, 164, 169, 0.1);
            transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;
        }
        .interactive-pic-container:hover {
            transform: translateY(-8px) scale(1.01); background-color: #0d4354; border-color: rgba(24, 164, 169, 0.4);
            box-shadow: 0 20px 38px rgba(2, 11, 15, 0.6), 0 15px 12px rgba(24, 164, 169, 0.15) !important;
        }
        .interactive-pic-container img {
            width: 100%; height: auto; max-height: 480px; object-fit: contain; 
            filter: contrast(1.02); transition: transform 0.35s ease;
        }
        .interactive-pic-container:hover img { transform: scale(1.015); }
        </style>

        <div style="text-align: center; padding: 45px 0 25px 0; margin-bottom: 20px;">
            <h1 style="font-size: 3.8rem; font-weight: 900; margin: 0; letter-spacing: -1.5px;
                       background: linear-gradient(135deg, #ffffff 30%, #18a4a9 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                SNAPCLASS AI
            </h1>
            <p style="font-size: 1.2rem; color: #cbd5e1; margin-top: 10px; font-weight: 500; letter-spacing: 0.5px; opacity: 0.85;">
                Intelligent Attendance Automation & Classroom Verification Infrastructure
            </p>
            <div style="width: 80px; height: 4px; background: #18a4a9; margin: 25px auto 0 auto; border-radius: 2px; opacity: 0.7;"></div>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. GET STARTED BUTTON ---
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Get Started", use_container_width=True):
            st.session_state['login_type'] = 'home'
            st.rerun()

    st.write("")

    # --- 3. DYNAMIC CONTENT ROWS ---
    # Define your content structure
    rows = [
        ("Face & Voice Verification", "Leverage advanced biometric neural nets to verify student presence with sub-second latency. Our system maps facial vectors and voice signatures with absolute precision.", "D:/Snap-class/images/step1.png"),
        ("Smart Classroom Intake", "Ingest student rosters and schedule metadata through our centralized management portal. The system handles automated check-ins while ensuring strict data privacy.", "D:/Snap-class/images/step2.png"),
        ("Real-time Attendance Audits", "Verify classroom integrity with automated spoof-detection and environment analysis. Ensure every check-in is cryptographically verified to the specific device.", "D:/Snap-class/images/step3.png"),
        ("Predictive Classroom Insights", "Analyze engagement patterns and attendance trends through clean, secure telemetry metrics. Unlock strategic educational insights without compromising student identities.", "D:/Snap-class/images/step4.png")
    ]

    for i, (title, desc, img_path) in enumerate(rows):
        st.write("---")
        c1, c2 = st.columns([1.1, 0.9]) if i % 2 == 0 else st.columns([0.9, 1.1])
        
        # Logic for alternating image/text position
        if i % 2 == 0:
            with c1:
                st.markdown(f'<div class="interactive-pic-container"><img src="data:image/png;base64,{convert_local_file_to_base64(img_path)}"></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div style="margin-top: 85px; padding-left: 20px;"><h2 style="font-weight: 800; color: #ffffff;">{title}</h2><p style="color: #ffffff; line-height: 1.7;">{desc}</p></div>', unsafe_allow_html=True)
        else:
            with c1:
                st.markdown(f'<div style="margin-top: 85px; padding-right: 20px;"><h2 style="font-weight: 800; color: #ffffff;">{title}</h2><p style="color: #ffffff; line-height: 1.7;">{desc}</p></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="interactive-pic-container"><img src="data:image/png;base64,{convert_local_file_to_base64(img_path)}"></div>', unsafe_allow_html=True)

    # --- 4. FOOTER MISSION BOX ---
    st.markdown("""
        <div style="margin-top: 45px; background: rgba(255, 255, 255, 0.08); padding: 25px; border-radius: 18px; border-left: 5px solid #18a4a9; backdrop-filter: blur(10px);">
            <p style="margin: 0; color: #ffffff; line-height: 1.7; font-size: 1rem;">
                <b style="color: #18a4a9; text-transform: uppercase; letter-spacing: 0.5px;">SnapClass Mission:</b> 
                We bridge the gap between classroom efficiency and identity security. We don't just track attendance—we ensure verified, stress-free learning environments.
            </p>
        </div>
    """, unsafe_allow_html=True)