import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


from src.database.db import create_attendance

def show_attendance_result(df, logs, key_prefix="default"):
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, width='stretch')

    # --- CSV DOWNLOAD LOGIC ---
    # Create a clean version for Excel: remove emojis and force Time as text
    df_clean = df.copy()
    df_clean['Status'] = df_clean['Status'].replace({'✅ Present': 'Present', '❌ Absent': 'Absent'})
    
    if 'Time' in df_clean.columns:
        df_clean['Time'] = "'" + df_clean['Time'].astype(str)

    csv_data = df_clean.to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        label="Download Attendance CSV",
        data=csv_data,
        file_name=f"attendance_{key_prefix}.csv",
        mime="text/csv",
        key=f"download_{key_prefix}"
    )

    # --- ACTION BUTTONS ---
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', key=f"discard_{key_prefix}", width='stretch'):
            if key_prefix == "voice":
                st.session_state.voice_attendance_results = None
            else:
                st.session_state.face_attendance_results = None
            
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('Confirm & Save', key=f"confirm_{key_prefix}", width='stretch', type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                
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

