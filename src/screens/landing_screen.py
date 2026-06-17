import streamlit as st
import base64
import os

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="SnapClass AI")

def convert_local_file_to_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def landing_screen():
    # --- UNIFIED DARK THEME CSS ---
    st.markdown("""
        <style>
        /* Main background */
        .stApp { background-color: #020b0f; color: #e2e8f0; }
        
        /* Custom Cards */
        .glass-card {
            background: rgba(11, 56, 70, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(24, 164, 169, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            transition: transform 0.3s ease;
        }
        .glass-card:hover { transform: translateY(-5px); border-color: #18a4a9; }
        
        /* Interactive Image Container */
        .interactive-pic {
            width: 100%; border-radius: 20px; overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        /* Headings & Text */
        h1 { color: #ffffff !important; }
        h2 { color: #18a4a9 !important; font-weight: 700 !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    st.markdown("""
        <div style="text-align: center; padding: 60px 0;">
            <h1 style="font-size: 4rem; letter-spacing: -2px;">SNAPCLASS <span style="color:#18a4a9">AI</span></h1>
            <p style="font-size: 1.4rem; opacity: 0.8;">Revolutionizing attendance with biometric precision.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- CENTERED GET STARTED ---
    col_a, col_b, col_c = st.columns([3, 1, 3])
    with col_b:
        if st.button("Get Started", use_container_width=True):
            st.session_state['login_type'] = 'home'
            st.rerun()

    st.write("---")

    # --- CONTENT GRID ---
    steps = [
        ("Biometric Verification", "Advanced neural networks map facial features for near-instant, secure identification.", "images/step1.png"),
        ("Smart Data Intake", "Seamlessly integrate class rosters with automated scheduling and encrypted storage.", "images/step2.png"),
        ("Audit Integrity", "Built-in spoof detection ensures every attendance entry is verified and immutable.", "images/step3.png"),
        ("Insight Analytics", "Transform attendance raw data into actionable classroom engagement reports.", "images/step4.png")
    ]

    for i, (title, desc, img_path) in enumerate(steps):
        cols = st.columns([1, 1.2])
        img_b64 = convert_local_file_to_base64(img_path)
        
        # Build image component
        img_component = f'<div class="interactive-pic"><img src="data:image/png;base64,{img_b64}" style="width:100%"></div>' if img_b64 else "<div>Image Missing</div>"
        
        # Alternating Layout
        if i % 2 == 0:
            with cols[0]: st.markdown(img_component, unsafe_allow_html=True)
            with cols[1]: 
                st.markdown(f'<div class="glass-card"><h2>{title}</h2><p>{desc}</p></div>', unsafe_allow_html=True)
        else:
            with cols[0]: 
                st.markdown(f'<div class="glass-card"><h2>{title}</h2><p>{desc}</p></div>', unsafe_allow_html=True)
            with cols[1]: st.markdown(img_component, unsafe_allow_html=True)

    # --- MISSION STATEMENT ---
    st.markdown("""
        <div class="glass-card" style="border-left: 6px solid #18a4a9;">
            <h3>Our Mission</h3>
            <p>At SnapClass, we eliminate administrative friction. By replacing manual check-ins with AI-driven authentication, we restore valuable time back to the classroom environment.</p>
        </div>
    """, unsafe_allow_html=True)

# Run logic
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    landing_screen()