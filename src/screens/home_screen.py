def home_screen():
    # Injecting the styling directly here for a fully self-contained home screen
    st.markdown("""
        <style>
            /* Deep purple background matching the reference */
            .stApp {
                background: linear-gradient(135deg, #2b1055 0%, #45217a 50%, #2b1055 100%) !important;
                background-attachment: fixed !important;
            }
            
            /* Glassmorphism card effect for columns */
            .stApp div[data-testid="stColumn"] {
                background-color: rgba(255, 255, 255, 0.05) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding: 2.5rem !important;
                border-radius: 2rem !important;
                text-align: center;
            }
            
            /* Ensure text inside these cards is white */
            h1, h2 {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Render components
    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        # Added a little extra top-margin via empty header for balance
        st.write(" ") 
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()