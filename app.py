
import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()


    # 1. Capture the code once
    join_code = st.query_params.get('join-code')
    if join_code:
        st.session_state.pending_join_code = join_code
        # Force switch to student if not already there
        if st.session_state.get('login_type') != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

    # 2. Logic to show dialog
    if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
        if 'pending_join_code' in st.session_state:
            # Call the dialog directly here
            auto_enroll_dialog(st.session_state.pending_join_code)
            # IMPORTANT: Delete the code after showing the dialog so it doesn't keep popping up
            del st.session_state.pending_join_code

    # 3. Route to screens
    if 'login_type' not in st.session_state: st.session_state['login_type'] = None
    
    match st.session_state['login_type']:
        case 'teacher': teacher_screen()
        case 'student': student_screen()
        case None: home_screen()
main()