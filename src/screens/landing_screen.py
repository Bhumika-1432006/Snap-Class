import streamlit as st
import base64
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "images"))

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="SnapClass AI")

def convert_local_file_to_base64(file_path):
    if not os.path.exists(file_path): 
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def landing_screen():
    # --- CSS STYLES ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap');

        :root {
            --color-primary: #18A4A9;
            --color-primary-dark: #0E7A7E;
            --color-secondary: #2B2D6E;
            --color-accent: #F5A623;
            --color-text: #1E2430;
            --color-text-muted: #52606D;
            --color-surface: rgba(255, 255, 255, 0.65);
            --color-surface-border: rgba(255, 255, 255, 0.9);
            --font-heading: 'Poppins', sans-serif;
            --font-body: 'Inter', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #EAF7F8 0%, #DDEFF2 55%, #E9E4F5 100%) !important;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1300px !important;
            margin: 0 auto !important;
        }

        /* --- HERO --- */
        .hero-wrap {
            text-align: center;
            padding: 70px 0 20px 0;
            animation: fadeInUp 0.8s ease both;
        }
        .hero-wrap h1 {
            font-family: var(--font-heading) !important;
            font-size: 4.2rem !important;
            font-weight: 900 !important;
            color: var(--color-text) !important;
            letter-spacing: -1px;
            margin-bottom: 0 !important;
        }
        .hero-wrap h1 span {
            background: linear-gradient(120deg, var(--color-primary), var(--color-secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .hero-wrap p.tagline {
            font-family: var(--font-body) !important;
            font-size: 1.35rem !important;
            font-weight: 500 !important;
            color: var(--color-text-muted) !important;
            margin-top: 14px !important;
            text-align: center;
        }

        /* --- CENTERED BUTTON --- */
        div[data-testid="column"] {
            display: flex !important;
            justify-content: center !important;
        }

        div.stButton {
            display: flex;
            justify-content: center;
            margin: 22px 0 90px 0 !important;
        }

        div.stButton > button {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
            color: #ffffff !important;
            font-family: var(--font-heading) !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 14px 42px !important;
            font-size: 1.1rem !important;
            box-shadow: 0 8px 22px rgba(24, 164, 169, 0.35);
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 12px 28px rgba(24, 164, 169, 0.45);
            color: #ffffff !important;
        }
        div.stButton > button:active {
            transform: translateY(-1px) scale(0.99);
        }

        /* --- STEPS SECTION --- */
        .steps-heading {
            text-align: center;
            font-family: var(--font-heading);
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--color-secondary);
            opacity: 0.75;
            margin-bottom: 10px;
        }

        .grid-row {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 48px !important;
            margin: 0 auto 70px auto !important;
            align-items: center !important;
            width: 100% !important;
            padding-bottom: 55px;
            border-bottom: 1px solid rgba(43, 45, 110, 0.1);
            animation: fadeInUp 0.7s ease both;
        }
        .grid-row:last-of-type {
            border-bottom: none;
            margin-bottom: 20px !important;
        }

        .grid-item { width: 100% !important; }

        .uniform-image-container {
            width: 100% !important; height: 380px !important; border-radius: 24px; overflow: hidden;
            background: #ffffff; box-shadow: 0 12px 28px rgba(24, 164, 169, 0.12);
            display: flex; align-items: center; justify-content: center;
            transition: transform 0.35s ease, box-shadow 0.35s ease;
        }
        .uniform-image-container:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(24, 164, 169, 0.22);
        }
        .uniform-image-container img { width: 100% !important; height: 100% !important; object-fit: cover !important; }

        .text-block {
            padding: 46px !important; border-radius: 24px; background: var(--color-surface);
            border: 1px solid var(--color-surface-border);
            backdrop-filter: blur(6px);
            transition: transform 0.35s ease, box-shadow 0.35s ease;
            box-shadow: 0 4px 18px rgba(43, 45, 110, 0.05);
        }
        .text-block:hover {
            transform: translateY(-6px);
            box-shadow: 0 14px 30px rgba(43, 45, 110, 0.1);
        }

        .step-tag {
            display: inline-block;
            font-family: var(--font-heading);
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 1.5px;
            color: #ffffff;
            background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 14px;
        }

        h2 {
            font-family: var(--font-heading) !important;
            color: var(--color-text) !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            margin-bottom: 16px !important;
        }
        p {
            font-family: var(--font-body) !important;
            color: var(--color-text-muted) !important;
            font-size: 1.08rem !important;
            line-height: 1.75 !important;
            text-align: center;
        }
        .text-block p { text-align: left; }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(24px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- RESPONSIVE --- */
        @media (max-width: 900px) {
            .hero-wrap h1 { font-size: 2.8rem !important; }
            .hero-wrap p.tagline { font-size: 1.1rem !important; }
            .grid-row {
                grid-template-columns: 1fr !important;
                gap: 22px !important;
                margin-bottom: 45px !important;
                padding-bottom: 35px;
            }
            .uniform-image-container { height: 260px !important; order: -1; }
            .text-block { padding: 30px !important; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-wrap">
            <h1>SNAPCLASS <span>AI</span></h1>
            <p class="tagline">Intelligent Attendance Automation for Modern Classrooms.</p>
        </div>
    """, unsafe_allow_html=True)


    # --- CENTERED BUTTON ---
    col1, col2, col3 = st.columns([1.6, 1, 1])
    with col2:
        if st.button("Get Started"):
            st.session_state['login_type'] = 'home'
            st.rerun()

    # --- STEPS ---
    st.markdown('<p class="steps-heading">How It Works</p>', unsafe_allow_html=True)

    steps = [
        ("Step 1: Student Registration", "Students register profiles using unique face embeddings and voice signatures for secure, AI-ready identity mapping.", os.path.join(IMAGES_DIR, "step1.svg")),
        ("Step 2: Class Enrollment", "Students join any class instantly by using the teacher-provided subject code or scanning the class QR link.", os.path.join(IMAGES_DIR, "step2.svg")),
        ("Step 3: Teacher Management", "Teachers register, create subjects, and generate unique codes to manage their classroom environment.", os.path.join(IMAGES_DIR, "step3.svg")),
        ("Step 4: AI Attendance Marking", "Capture classroom photos and voice recordings for AI scanning to automatically mark attendance and download CSV files.", os.path.join(IMAGES_DIR, "step4.svg"))
    ]

    for i, (title, desc, img_path) in enumerate(steps):
        img_b64 = convert_local_file_to_base64(img_path)
        tag_html = f'<span class="step-tag">STEP {i + 1}</span>'
        img_html = f'<div class="grid-item"><div class="uniform-image-container"><img src="data:image/svg+xml;base64,{img_b64}"></div></div>'
        text_html = f'<div class="grid-item"><div class="text-block">{tag_html}<h2>{title}</h2><p>{desc}</p></div></div>'

        if i % 2 == 0:
            st.markdown(f'<div class="grid-row" style="animation-delay: {i * 0.05}s">{img_html}{text_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="grid-row" style="animation-delay: {i * 0.05}s">{text_html}{img_html}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if 'logged_in' not in st.session_state: 
        st.session_state['logged_in'] = False
    if not st.session_state['logged_in']:
        landing_screen()