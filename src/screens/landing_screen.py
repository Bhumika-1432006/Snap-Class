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
        /* Force full width and remove default shifting margins */
        .stApp { background: linear-gradient(135deg, #e0f2f7 0%, #d1eaf0 100%) !important; }
        
        [data-testid="stMainBlockContainer"] {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }

        /* Locked Grid - Immune to Refresh Glitches */
        .grid-row {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 40px !important;
            margin: 0 auto 60px auto !important;
            align-items: center !important;
            width: 100% !important;
        }
        
        .grid-item { width: 100% !important; }
        
        /* Button & UI elements */
        div.stButton > button:first-child {
            background-color: #18a4a9 !important; color: #ffffff !important; font-weight: 700 !important;
            border: none !important; border-radius: 50px !important; padding: 15px 50px !important;
            font-size: 1.4rem !important; box-shadow: 0 4px 15px rgba(24, 164, 169, 0.3);
        }

        .uniform-image-container { 
            width: 100% !important; height: 400px !important; border-radius: 25px; overflow: hidden; 
            background: #ffffff; box-shadow: 0 15px 30px rgba(0,0,0,0.08); 
            display: flex; align-items: center; justify-content: center;
        }
        .uniform-image-container img { width: 100% !important; height: 100% !important; object-fit: cover !important; }
        
        .text-block { 
            padding: 50px !important; border-radius: 25px; background: rgba(255, 255, 255, 0.5); 
            border: 1px solid rgba(255, 255, 255, 0.8);
        }
        
        h1 { font-size: 4.5rem; font-weight: 900; color: #0f172a; text-align: center; }
        h2 { color: #6A329F !important; font-size: 2.2rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>SNAPCLASS <span style='color:#18a4a9'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5rem; color: #334155;'>Intelligent Attendance Automation for Modern Classrooms.</p>", unsafe_allow_html=True)

    # Use an empty container to keep the button centered without columns that might shift
    st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)
    if st.button("Get Started"):
        st.session_state['login_type'] = 'home'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    steps = [
        ("Step 1: Student Registration", "Students register profiles using unique face embeddings and voice signatures for secure, AI-ready identity mapping.", "images/step1.png"),
        ("Step 2: Class Enrollment", "Students join any class instantly by using the teacher-provided subject code or scanning the class QR link.", "images/step2.png"),
        ("Step 3: Teacher Management", "Teachers register, create subjects, and generate unique codes to manage their classroom environment.", "images/step3.png"),
        ("Step 4: AI Attendance Marking", "Capture classroom photos and voice recordings for AI scanning to automatically mark attendance and download CSV files.", "images/step4.png")
    ]

    for i, (title, desc, img_path) in enumerate(steps):
        img_b64 = convert_local_file_to_base64(img_path)
        img_html = f'<div class="grid-item"><div class="uniform-image-container"><img src="data:image/png;base64,{img_b64}"></div></div>'
        text_html = f'<div class="grid-item"><div class="text-block"><h2>{title}</h2><p>{desc}</p></div></div>'
        
        if i % 2 == 0:
            st.markdown(f'<div class="grid-row">{img_html}{text_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="grid-row">{text_html}{img_html}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if not st.session_state['logged_in']:
        landing_screen()