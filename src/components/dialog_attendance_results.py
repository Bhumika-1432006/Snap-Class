import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


from src.database.db import create_attendance

def show_attendance_result(df, logs, key_prefix="default"):
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        # Added key with unique prefix
        if st.button('Discard', key=f"discard_{key_prefix}", width='stretch'):
            # Clear appropriate session state based on the prefix
            if key_prefix == "voice":
                st.session_state.voice_attendance_results = None
            else:
                st.session_state.face_attendance_results = None
            
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        # Added key with unique prefix
        if st.button('Confirm & Save', key=f"confirm_{key_prefix}", width='stretch', type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                
                # Clear appropriate session state based on the prefix
                if key_prefix == "voice":
                    st.session_state.voice_attendance_results = None
                else:
                    st.session_state.face_attendance_results = None
                    
                st.rerun()
            except Exception as e:
                st.error('Sync failed!')

                
@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)

