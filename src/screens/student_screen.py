import streamlit as st
import time
import numpy as np
from PIL import Image
from src.ui.base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', icon=':material/add_circle:'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}
        stats_map[sid]['total'] +=1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {"total":0, "attended": 0})
        
        def unenroll_button(subject_id=sid, sub_name=sub['name']):
            if st.button("Unenroll from this course", 
                         key=f"unenroll_{subject_id}", 
                         type='tertiary', 
                         icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id, subject_id)
                st.toast(f'Unenrolled from {sub_name} successfully!')
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()

def student_screen():
    # Global styling to match the Home Page "Extravagant" Theme
    st.markdown("""
        <style>
            /* Hide top bar & import fonts */
            [data-testid="stHeader"] { display: none !important; }
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
            
            /* Radial Gradient background shared with Home */
            .stApp {
                background: radial-gradient(circle at 100% 0%, #3d1b66, #210e3d, #140826) !important;
                background-attachment: fixed !important;
            }
            
            /* Glassmorphism for containers/cards */
            div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"],
            div[data-testid="stHorizontalBlock"] {
                background: rgba(255, 255, 255, 0.05) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 2rem !important;
                padding: 1.5rem !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            }

            h1, h2, h3 {
                font-family: 'Climate Crisis', sans-serif !important;
                color: #ffffff !important;
            }
            p, button, div, span {
                font-family: 'Outfit', sans-serif !important;
            }
            
            /* Button styling */
            button {
                background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
                border-radius: 1.5rem !important;
                border: none !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    # Login screen layout
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID')
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner('AI is scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces > 1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized!')
    footer_dashboard()