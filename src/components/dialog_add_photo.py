import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.markdown("""
        <style>
            .st-key-camera-snapshot-panel {
                background: #FFFFFF !important;
                border-radius: 20px !important;
                padding: 2rem !important;
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.12) !important;
                border: 1px solid var(--color-surface-border, rgba(255, 255, 255, 0.9)) !important;
                margin-bottom: 12px !important;
            }

            [data-testid="stCameraInputButton"] {
                background: linear-gradient(135deg, var(--color-primary, #18A4A9) 0%, var(--color-primary-dark, #0E7A7E) 100%) !important;
                color: #ffffff !important;
                font-family: var(--font-heading, 'Poppins', sans-serif) !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 50px !important;
                padding: 12px 30px !important;
                box-shadow: 0 8px 22px rgba(24, 164, 169, 0.35) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            }
            [data-testid="stCameraInputButton"]:hover {
                transform: translateY(-3px) scale(1.03);
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.45) !important;
                color: #ffffff !important;
            }
            [data-testid="stCameraInputButton"]:active {
                transform: translateY(-1px) scale(0.99);
            }
        </style>
    """, unsafe_allow_html=True)

    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'



    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        with st.container(key="camera-snapshot-panel"):
            c_left, c_center, c_right = st.columns([1, 6, 1])
            with c_center:
                cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured')
            st.rerun()


    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader( 'choose image files', type=['jpg', 'png', 'jpeg' ], accept_multiple_files=True, key='dialog_upload')

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            
            st.toast('Photo Uploaded Successfully')
            st.rerun()

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()