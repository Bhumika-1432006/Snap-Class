import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #18A4A9 !important;
                }

                # storing the id
                .stApp div[data-testid="stColumn"]{
                    background-color:#E4F4F4 !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }
        </style>

                """
            ,unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: #E4F4F4 !important;
                }

        </style>

                """
            ,unsafe_allow_html=True)




def style_base_layout():
# asdasd
    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap');

        :root {
            --color-primary: #18A4A9;
            --color-primary-dark: #0E7A7E;
            --color-secondary: #2B2D6E;
            --color-accent: #F5A623;
            --color-text: #1E2430;
            --color-text-muted: #52606D;
            --color-surface: rgba(255, 255, 255, 0.65);
            --color-surface-border: rgba(255, 255, 255, 0.9);
            --font-heading: 'Poppins', sans-serif;
            --font-body: 'Inter', sans-serif;
        }


          /* Hide Top Bar of streamlit */

            #MainMenu, footer, header {
               visibility: hidden;
            }

            .block-container {
                padding-top:1.5rem !important;
            }

            h1 {
                font-family: var(--font-heading, 'Poppins', sans-serif) !important;
                font-size: 2rem !important;
                font-weight: 700 !important;
                color: var(--color-secondary, #2B2D6E) !important;
            }

            h2 {
                font-family: var(--font-heading, 'Poppins', sans-serif) !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: var(--color-secondary, #2B2D6E) !important;
            }

            h3, h4, p {
                font-family: var(--font-body);
            }


            button{
                border-radius: 1.5rem !important;
                background-color: #18A4A9 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: #2B2D6E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"] {
                background-color: transparent !important;
                color: #18A4A9 !important;
                border: 0.5px solid #18A4A9 !important;
                border-radius: 50px !important;
                padding: 10px 20px !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform :scale(1.05)}

            /* --- Dark-mode safety net ---
               config.toml's [theme] base="light" is the primary fix, but
               native BaseWeb components (dialogs, the date_input calendar,
               selectbox/multiselect dropdowns) are portaled to <body>
               outside .stApp and have historically still picked up OS dark
               mode in some Streamlit versions. These selectors are
               intentionally unscoped (no .stApp prefix) since that's where
               BaseWeb actually mounts them, and force a light, on-brand
               surface with readable text regardless of the OS setting. */

            [data-testid="stDialog"],
            [data-testid="stDialog"] > div:first-child > div:first-child {
                background: #FFFFFF !important;
            }
            [data-testid="stDialog"] h1,
            [data-testid="stDialog"] h2,
            [data-testid="stDialog"] h3,
            [data-testid="stDialog"] label,
            [data-testid="stDialog"] p,
            [data-testid="stDialog"] span,
            [data-testid="stDialog"] div {
                color: var(--color-text, #1E2430) !important;
            }

            /* Selectbox / multiselect / date_input popovers */
            div[data-baseweb="popover"] {
                background: #FFFFFF !important;
            }
            div[data-baseweb="popover"] * {
                color: var(--color-text, #1E2430) !important;
            }
            div[data-baseweb="menu"],
            ul[role="listbox"] {
                background: #FFFFFF !important;
            }
            li[role="option"] {
                background: #FFFFFF !important;
                color: var(--color-text, #1E2430) !important;
            }
            li[role="option"]:hover,
            li[aria-selected="true"] {
                background: rgba(24, 164, 169, 0.12) !important;
            }

            /* Date range calendar popup */
            div[data-baseweb="calendar"] {
                background: #FFFFFF !important;
            }
            div[data-baseweb="calendar"] * {
                color: var(--color-text, #1E2430) !important;
            }
            div[data-baseweb="calendar"] button[aria-selected="true"],
            div[data-baseweb="calendar"] div[aria-selected="true"] {
                background: var(--color-primary, #18A4A9) !important;
                color: #FFFFFF !important;
            }
            div[data-baseweb="calendar"] button:hover {
                background: rgba(24, 164, 169, 0.15) !important;
            }
        </style>

                """
            ,unsafe_allow_html=True)
