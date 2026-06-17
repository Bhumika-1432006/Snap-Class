
import streamlit as st

from src.screens.landing_screen import landing_screen
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
        st.session_state['login_type'] = 'landing'

    match st.session_state['login_type']:
        case 'landing':
            landing_screen()
        case 'home':
            home_screen()
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        


    join_code = st.query_params.get('join-code')
    if join_code:
        # Only switch state if not already in student mode to avoid unnecessary re-runs
        if st.session_state.get('login_type') != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        
        # Check if the dialog should be shown
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            # Use a session state flag to prevent the dialog from popping up repeatedly
            # if you've already handled the join code for this session.
            if st.session_state.get('show_enrollment', True):
                auto_enroll_dialog(join_code)
main()