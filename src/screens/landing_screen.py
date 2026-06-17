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
    # --- CSS THEME: SOFT BLUE STRIATION & VIOLET HEADINGS (MOBILE FRIENDLY) ---
    st.markdown("""
        <style>
        .stApp { 
            background: linear-gradient(135deg, #e0f2f7 0%, #d1eaf0 100%); 
            color: #1e293b; 
        }
        
        /* Mobile Responsive Fixes */
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem !important; }
            .uniform-image-container { height: 250px !important; margin: 20px 0 !important; }
            .text-block { padding: 30px !important; margin: 10px 0 !important; }
            h2 { font-size: 1.6rem !important; }
        }
        
        /* Vibrant Teal Button Styling */
        div.stButton > button:first-child {
            background-color: #18a4a9 !important; 
            color: #ffffff !important; 
            font-weight: 700 !important;
            border: none !important; 
            border-radius: 50px !important; 
            padding: 15px 50px !important;
            font-size: 1.4rem !important; 
            box-shadow: 0 4px 15px rgba(24, 164, 169, 0.3);
            transition: transform 0.2s ease !important;
        }
        div.stButton > button:first-child:hover { 
            transform: scale(1.05) !important; 
            background-color: #148a8e !important; 
        }

        .uniform-image-container { 
            width: 100%; height: 400px; border-radius: 25px; overflow: hidden; 
            background: #ffffff; box-shadow: 0 15px 30px rgba(0,0,0,0.08); 
            margin: 40px 0; display: flex; align-items: center; justify-content: center;
        }
        .uniform-image-container img { width: 100%; height: 100%; object-fit: cover; }
        
        .text-block { 
            padding: 50px; border-radius: 25px; background: rgba(255, 255, 255, 0.5); 
            margin: 40px 0; border: 1px solid rgba(255, 255, 255, 0.8);
        }
        
        /* Violet Headings */
        h2 { color: #6A329F !important; font-size: 2.2rem !important; margin-bottom: 20px !important; }
        p { color: #475569 !important; font-size: 1.2rem !important; line-height: 1.8 !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    st.markdown("""
        <div style="text-align: center; padding: 60px 0 40px 0;">
            <h1 style="font-size: 4.5rem; font-weight: 900; color: #0f172a;">SNAPCLASS <span style="color:#18a4a9">AI</span></h1>
            <p style="font-size: 1.5rem; color: #334155; margin-top: 15px;">Intelligent Attendance Automation for Modern Classrooms.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- CENTERED TEAL BUTTON ---
    col_left, col_center, col_right = st.columns([2, 1, 2])
    with col_center:
        if st.button("Get Started", use_container_width=True):
            st.session_state['login_type'] = 'home'
            st.rerun()

    # --- CONTENT ROWS ---
    steps = [
        ("Step 1: Student Registration", "Students register profiles using unique face embeddings and voice signatures for secure, AI-ready identity mapping.", "images/step1.png"),
        ("Step 2: Class Enrollment", "Students join any class instantly by using the teacher-provided subject code or scanning the class QR link.", "images/step2.png"),
        ("Step 3: Teacher Management", "Teachers register, create subjects, and generate unique codes to manage their classroom environment.", "images/step3.png"),
        ("Step 4: AI Attendance Marking", "Capture classroom photos and voice recordings for AI scanning to automatically mark attendance and download CSV files.", "images/step4.png")
    ]

    for i, (title, desc, img_path) in enumerate(steps):
        img_b64 = convert_local_file_to_base64(img_path)
        img_html = f'<div class="uniform-image-container"><img src="data:image/png;base64,{img_b64}"></div>'
        text_html = f'<div class="text-block"><h2>{title}</h2><p>{desc}</p></div>'
        
        st.write("<br><br>", unsafe_allow_html=True) 
        c1, c2 = st.columns([1, 1], gap="large")
        if i % 2 == 0:
            with c1: st.markdown(img_html, unsafe_allow_html=True)
            with c2: st.markdown(text_html, unsafe_allow_html=True)
        else:
            with c1: st.markdown(text_html, unsafe_allow_html=True)
            with c2: st.markdown(img_html, unsafe_allow_html=True)

    # --- MISSION ---
    st.markdown("""
        <div style="margin: 80px 0; padding: 60px; background: rgba(255,255,255,0.4); border-radius: 30px; text-align: center; border: 1px solid rgba(255,255,255,0.6);">
            <h3 style="color: #6A329F; font-size: 1.8rem;">Our Mission</h3>
            <p style="max-width: 800px; margin: 20px auto; color: #1e293b; font-size: 1.2rem;">Making modern attendance easier and more efficient.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if not st.session_state['logged_in']:
        landing_screen()