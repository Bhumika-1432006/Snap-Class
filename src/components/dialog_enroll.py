import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    # Bind to session_state via key= so the value persists correctly across
    # reruns (e.g. when the Enroll button itself triggers a rerun) instead
    # of resetting to empty right when the button's logic reads it.
    if 'enroll_dialog_value' not in st.session_state:
        st.session_state['enroll_dialog_value'] = st.session_state.pop('enroll_code', '')

    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101', key='enroll_dialog_value')

    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                if check.data:
                    st.warning('You are already enrolled in this program')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.markdown("""
                        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px;">
                            <video src="https://assets-v2.lottiefiles.com/a/0fec3d74-5606-11ef-8b0e-4ff82aa28e0f/rvny7VRYdr.mp4"
                                   autoplay muted playsinline
                                   style="width:220px; height:220px; max-width:100%; object-fit:cover;"></video>
                            <p style="font-weight:700; font-size:1.1rem; margin:0;">Successfully enrolled! 🎉</p>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2.5)
                    st.rerun()
        else:
            st.warning('Please enter a subject code')
