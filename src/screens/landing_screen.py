import streamlit as st
import base64
import os

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="SnapClass AI")

def convert_local_file_to_base64(file_path):
    if not os.path.exists(file_path): return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def landing_screen():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #e0f2f7 0%, #d1eaf0 100%); color: #1e293b; }
        
        /* THE LOCKED LAYOUT: Prevents Streamlit from ever overriding this */
        .custom-row {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 40px !important;
            align-items: center !important;
            width: 100vw !important;
            max-width: 1400px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding: 20px 0 !important;
        }
        
        /* Explicit desktop override for column-like behavior */
        @media (min-width: 901px) {
            .item-box { flex: 1 1 50% !important; min-width: 400px !important; }
        }

        /* Mobile Breakpoint */
        @media (max-width: 900px) {
            .custom-row { flex-wrap: wrap !important; }
            h1 { font-size: 2.5rem !important; }
        }

        div.stButton > button:first-child {
            background-color: #18a4a9 !important; color: #ffffff !important; font-weight: 700 !important;
            border: none !important; border-radius: 50px !important; padding: 15px 50px !important;
            font-size: 1.4rem !important; box-shadow: 0 4px 15px rgba(24, 164, 169, 0.3);
        }

        .item-box { min-width: 300px; }
        .uniform-image-container { width: 100%; height: 400px; border-radius: 25px; overflow: hidden; background: #ffffff; box-shadow: 0 15px 30px rgba(0,0,0,0.08); margin: 0; display: flex; align-items: center; justify-content: center; }
        .uniform-image-container img { width: 100%; height: 100%; object-fit: cover; }
        .text-block { padding: 50px; border-radius: 25px; background: rgba(255, 255, 255, 0.5); border: 1px solid rgba(255, 255, 255, 0.8); }
        h2 { color: #6A329F !important; font-size: 2.2rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align: center; padding: 60px 0;"><h1>SNAPCLASS <span style="color:#18a4a9">AI</span></h1></div>', unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([2, 1, 2])
    with col_center:
        if st.button("Get Started", use_container_width=True):
            st.session_state['login_type'] = 'home'
            st.rerun()

    steps = [
        ("Step 1: Student Registration", "Students register profiles using unique face embeddings and voice signatures.", "images/step1.png"),
        ("Step 2: Class Enrollment", "Students join any class instantly by using the teacher-provided subject code.", "images/step2.png"),
        ("Step 3: Teacher Management", "Teachers register, create subjects, and generate unique codes.", "images/step3.png"),
        ("Step 4: AI Attendance Marking", "Capture classroom photos and voice recordings for AI scanning.", "images/step4.png")
    ]

    for i, (title, desc, img_path) in enumerate(steps):
        img_b64 = convert_local_file_to_base64(img_path)
        img_html = f'<div class="item-box"><div class="uniform-image-container"><img src="data:image/png;base64,{img_b64}"></div></div>'
        text_html = f'<div class="item-box"><div class="text-block"><h2>{title}</h2><p>{desc}</p></div></div>'
        
        st.markdown(f'<div class="custom-row">{"".join([img_html, text_html] if i % 2 == 0 else [text_html, img_html])}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if not st.session_state['logged_in']:
        landing_screen()