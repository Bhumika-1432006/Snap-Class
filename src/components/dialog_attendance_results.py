import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

from src.screens.student_screen import _render_avatar

from src.database.db import create_attendance

def show_attendance_result(df, logs, key_prefix="default"):
    st.markdown("""
        <style>
        [data-testid="stDialog"] { background: #FFFFFF !important; border-radius: 16px !important; }
        [data-testid="stDataFrame"] { border-radius: 8px !important; overflow: hidden !important; }
        </style>
    """, unsafe_allow_html=True)

    # FEATURE 4: avatar + name strip above the review table. st.dataframe
    # can't render a live/autoplay <video> per cell, so this sits alongside
    # it rather than trying to embed avatars inside the dataframe itself.
    # Only appears when the caller's results include an 'Avatar' column --
    # today that's teacher_screen.py's face-analysis results; the voice
    # attendance flow (dialog_voice_attendance.py) doesn't set one yet.
    if 'Avatar' in df.columns and 'Name' in df.columns:
        chips = ''.join(
            f'<div style="display:flex;align-items:center;gap:6px;background:rgba(24,164,169,0.06);'
            f'padding:6px 12px;border-radius:20px;">'
            f'<span style="display:inline-flex;width:28px;height:28px;border-radius:50%;overflow:hidden;">'
            f'{_render_avatar(row["Avatar"], size_px=28)}</span>'
            f'<span style="font-family:Inter,sans-serif;font-size:0.82rem;color:#1E2430;">{row["Name"]}</span>'
            f'</div>'
            for _, row in df.iterrows()
        )
        st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;">{chips}</div>', unsafe_allow_html=True)

    st.write('Please review attendance before confirming.')
    # 'Avatar' is already shown via the chip strip above -- drop it here so
    # it doesn't also show up as a raw video/emoji URL string in the table.
    display_df = df.drop(columns=['Avatar']) if 'Avatar' in df.columns else df
    st.dataframe(display_df, hide_index=True, width='stretch')

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

