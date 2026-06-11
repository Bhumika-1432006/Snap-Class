import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def set_global_styles():
    st.markdown("""
        <style>
            /* 1. Global text remains your preferred purple */
            .stApp, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, div, p, span, label {
                color: #2E1A47 !important; 
            }

            /* 2. Dialog Box Background and Text Color */
            div[data-testid="stDialog"] > div:first-child > div:first-child {
                background-color: #F8F9FA !important; 
                border-radius: 15px !important;
                padding: 30px !important;
                border: 1px solid #E0E0E0 !important;
                max-width: 600px !important; 
                margin: 0 auto !important;
            }

            /* Force text inside the dialog to be a specific color */
            div[data-testid="stDialog"] * {
                color: #333333 !important; 
            }

            /* 3. Unenroll Button: Background White, Border Black, Text Left Unchanged */
            /* Removed 'color: #000000 !important' so it respects your theme/icon colors */
            div[data-testid="stButton"] button:has(span[aria-label*="delete"]) {
                background-color: #FFFFFF !important;
                border: 1px solid #000000 !important;
            }

            /* 4. Input and Selectbox styling */
            .stTextInput input, div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 1px solid #000000 !important;
            }
        </style>
    """, unsafe_allow_html=True)
def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary', key='logout_btn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        
        def unenroll_button(subject_id=sid, sub_name=sub['name']):
            if st.button("Unenroll", key=f"unenroll_{subject_id}", type='tertiary', icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id, subject_id)
                st.toast(f'Unenrolled from {sub_name} successfully!')
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()

def student_screen():
    set_global_styles()
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='back_btn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID')
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    show_registration = False
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
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True 

    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')
            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your voice for voice-only attendance")
            
            try:
                audio_data = st.audio_input('Record a short phrase (e.g., "I am present")')
            except Exception:
                st.error('Audio Input failed!')
                audio_data = None

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = get_voice_embedding(audio_data.read()) if audio_data else None
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Could not capture facial features.')
                else:
                    st.warning('Please enter your name!')
        
    footer_dashboard()