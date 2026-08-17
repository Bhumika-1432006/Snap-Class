import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.dialog_attendance_results import show_attendance_result, attendance_result_dialog
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects,
    get_attendance_for_teacher, get_all_students, get_disputes_for_teacher,
    reply_to_dispute, resolve_dispute,
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime
import dateutil.parser

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendance import voice_attendance_dialog

def set_global_styles():
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

            /* 1. Global text, on-brand instead of purple */
            .stApp, .stMarkdown, .stText, div, p, span, label {
                color: var(--color-text) !important;
                font-family: var(--font-body) !important;
            }
            /* Headings: Poppins bold indigo everywhere on this screen -- this
               rule loads after base_layout.py's h1/h2 rule (call order in
               teacher_screen() puts set_global_styles() last), so it wins
               the cascade and replaces the old comic-style display font. */
            .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
                font-family: var(--font-heading) !important;
                color: var(--color-secondary) !important;
                font-weight: 700 !important;
            }

            .stApp {
                background: linear-gradient(135deg, #EAF7F8 0%, #DDEFF2 55%, #E9E4F5 100%) !important;
            }

            .block-container {
                padding-left: 32px !important;
                padding-right: 32px !important;
                padding-bottom: 3rem !important;
            }

            /* 2. Dialog box, on-brand */
            div[data-testid="stDialog"] > div:first-child > div:first-child {
                background-color: #FFFFFF !important;
                border-radius: 20px !important;
                padding: 30px !important;
                border: 1px solid var(--color-surface-border) !important;
                box-shadow: 0 20px 45px rgba(24, 164, 169, 0.18) !important;
                max-width: 600px !important;
                margin: 0 auto !important;
            }
            div[data-testid="stDialog"] * {
                color: var(--color-text) !important;
            }

            /* 3. Inputs / selects: rounded, teal focus ring, no black border.
               FIX: box styling (bg/border/radius) now lives on the wrapper
               div[data-baseweb="base-input"] -- confirmed via Streamlit's
               own source (base-input.js: `"data-baseweb": ... || "base-input"`)
               -- instead of the bare <input>. BaseWeb lays the input and its
               endEnhancer slot (the password show/hide eye icon) out as flex
               children of that wrapper; skinning only the inner <input> gave
               it an independent box that visually overlapped the icon
               instead of sitting cleanly beside it. */
            div[data-baseweb="base-input"],
            div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                border: 1px solid rgba(24, 164, 169, 0.3) !important;
                border-radius: 10px !important;
            }
            .stTextInput input,
            .stDateInput input {
                background-color: transparent !important;
                border: none !important;
                color: var(--color-text) !important;
            }
            .stTextInput input::placeholder {
                color: var(--color-text-muted) !important;
            }
            .stTextInput:focus-within div[data-baseweb="base-input"],
            .stDateInput:focus-within div[data-baseweb="base-input"],
            div[data-baseweb="select"]:focus-within > div {
                border-color: var(--color-primary) !important;
                box-shadow: 0 0 0 3px rgba(24, 164, 169, 0.15) !important;
            }
            /* Password show/hide toggle: safety net, not a confirmed-needed
               fix. Live DOM inspection (Chrome DevTools Protocol, twice,
               across separate sessions) shows this button already renders a
               real inline <svg> eye icon -- buttonInnerText comes back
               empty, confirming nothing is visually rendered as text; the
               only "password" text found is the SVG's own <title>
               accessibility element, which browsers never render visually.
               Selectors below DO match the real button (its aria-label/
               title are literally "Show password text"), so naively adding
               an ::after emoji unconditionally would draw a SECOND icon
               next to the working SVG. :not(:has(svg)) keeps the fallback
               dormant unless a future Streamlit build ever drops the SVG
               and falls back to bare ligature text. */
            button[aria-label*="password" i]:not(:has(svg)),
            button[title*="password" i]:not(:has(svg)) {
                font-size: 0 !important;
            }
            button[aria-label*="password" i]:not(:has(svg))::after,
            button[title*="password" i]:not(:has(svg))::after {
                content: "👁️";
                font-size: 16px !important;
            }

            div[role="listbox"] {
                background-color: #FFFFFF !important;
            }
            div[role="listbox"] div[role="option"] {
                color: var(--color-text) !important;
                background-color: #FFFFFF !important;
            }

            /* 4. Buttons: teal gradient pill for primary, indigo outline for
               secondary, muted outline for tertiary. */
            div.stButton {
                display: flex !important;
                justify-content: center !important;
            }
            div.stButton > button {
                border-radius: 50px !important;
                padding: 12px 30px !important;
                font-family: var(--font-heading) !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                border: none !important;
                white-space: nowrap !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            }
            div.stButton > button:hover {
                transform: translateY(-3px) scale(1.03);
            }
            div.stButton > button:active {
                transform: translateY(-1px) scale(0.99);
            }

            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
                color: #ffffff !important;
                box-shadow: 0 8px 22px rgba(24, 164, 169, 0.35) !important;
            }
            div.stButton > button[kind="primary"]:hover {
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.45) !important;
                color: #ffffff !important;
            }

            div.stButton > button[kind="secondary"] {
                background: #FFFFFF !important;
                color: var(--color-secondary) !important;
                border: 2px solid var(--color-secondary) !important;
                box-shadow: 0 4px 12px rgba(43, 45, 110, 0.10) !important;
            }
            div.stButton > button[kind="secondary"]:hover {
                background: rgba(43, 45, 110, 0.06) !important;
                box-shadow: 0 8px 18px rgba(43, 45, 110, 0.16) !important;
                color: var(--color-secondary) !important;
            }

            div.stButton > button[kind="tertiary"] {
                background: #FFFFFF !important;
                color: var(--color-text-muted) !important;
                border: 1px solid rgba(82, 96, 109, 0.35) !important;
                box-shadow: none !important;
                font-weight: 600 !important;
            }
            div.stButton > button[kind="tertiary"]:hover {
                border-color: #B3261E !important;
                color: #B3261E !important;
                transform: none;
            }
            div.stButton > button:disabled {
                opacity: 0.45 !important;
                transform: none !important;
            }
            /* FIX: Streamlit renders a button's label and its keyboard-
               shortcut hint (st.button(..., shortcut=...)) as sibling flex
               children inside the button, wrapped in an element flagged
               data-has-shortcut="true" (confirmed via Streamlit's Button.js
               source). `white-space: nowrap` above is needed so pill-button
               labels never wrap mid-word, but it was inherited into that
               inner row too with no gap protecting the hint from the label,
               so on narrower buttons ("Login", stacked in a half-width
               column) they visually crammed together. Give the hint its own
               spacing and a distinct, muted, smaller treatment instead of
               competing with the label text. aria-label is the stable
               selector for the hint span itself (Streamlit renders it as
               aria-label="Shortcut <keys>").
            */
            div.stButton > button [data-has-shortcut] {
                display: inline-flex !important;
                align-items: center !important;
                gap: 8px !important;
            }
            div.stButton > button [aria-label^="Shortcut"] {
                flex-shrink: 0 !important;
                font-size: 0.7rem !important;
                font-weight: 600 !important;
                opacity: 0.75 !important;
                white-space: nowrap !important;
            }

            /* Solid-indigo variant, scoped via container key -- Streamlit only
               ships primary/secondary/tertiary kinds, and "Run Face Analysis"
               needs a 4th look (solid indigo) distinct from the outlined
               indigo secondary style used elsewhere on this screen. */
            .st-key-btn-face-analysis div.stButton > button {
                background: linear-gradient(135deg, #4C5FD5 0%, #4151B5 100%) !important;
                color: #ffffff !important;
                border: none !important;
                box-shadow: 0 8px 22px rgba(76, 95, 213, 0.30) !important;
            }
            .st-key-btn-face-analysis div.stButton > button:hover {
                box-shadow: 0 12px 28px rgba(76, 95, 213, 0.4) !important;
                color: #ffffff !important;
            }

            /* 5. Login / register card */
            .st-key-teacher-register-card {
                background: #FFFFFF !important;
                max-width: 480px !important;
                margin: 0 auto !important;
                border-radius: 20px !important;
                padding: 2.75rem !important;
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.14) !important;
                border: 1px solid var(--color-surface-border) !important;
                animation: fadeInUp 0.6s ease both;
            }
            /* Login card no longer gets max-width/auto-margin centering --
               it now lives inside the right column of the split layout
               below, which already constrains its width. */
            .st-key-teacher-login-card {
                background: #FFFFFF !important;
                border-radius: 20px !important;
                padding: 2.75rem !important;
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.14) !important;
                border: 1px solid var(--color-surface-border) !important;
                animation: fadeInUp 0.6s ease both;
                height: 100%;
                box-sizing: border-box;
            }
            .teacher-auth-title {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 1.9rem;
                color: var(--color-secondary);
                text-align: center;
                margin-bottom: 4px;
            }
            .teacher-auth-subtitle {
                font-family: var(--font-body);
                font-size: 0.95rem;
                color: var(--color-text-muted);
                text-align: center;
                margin-bottom: 22px;
            }

            /* 5b. Login split layout: left brand/stats panel */
            .st-key-teacher-login-left {
                background: linear-gradient(160deg, var(--color-primary) 0%, var(--color-primary-dark) 55%, var(--color-secondary) 100%) !important;
                border-radius: 20px !important;
                padding: 2.5rem 2.1rem !important;
                color: #ffffff !important;
                height: 100%;
                box-sizing: border-box;
                box-shadow: 0 16px 40px rgba(24, 164, 169, 0.25) !important;
                animation: fadeInUp 0.6s ease both;
            }
            .st-key-teacher-login-left * { color: #ffffff !important; }
            .login-left-eyebrow {
                font-family: var(--font-heading);
                font-size: 0.78rem;
                letter-spacing: 2px;
                text-transform: uppercase;
                opacity: 0.85;
                margin-bottom: 8px;
            }
            .login-left-title {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.8rem;
                line-height: 1.25;
                margin-bottom: 10px;
            }
            .login-left-sub {
                font-family: var(--font-body);
                font-size: 0.92rem;
                opacity: 0.9;
                margin-bottom: 26px;
                line-height: 1.5;
            }
            .login-stat-row {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-bottom: 22px;
            }
            @media (max-width: 480px) {
                .login-stat-row { grid-template-columns: 1fr; }
                /* Login/Register button pairs (Login + Register Instead,
                   Register now + Login Instead) sat side-by-side in
                   st.columns(2) with no narrow-screen handling, so each
                   column got too cramped to fit its own button -- especially
                   "Register Instead"/"Login Instead", which are longer than
                   "Login"/"Register now". Scoped via container(key=...)
                   wrappers so this doesn't touch any other st.columns(2)
                   row elsewhere on the page. */
                .st-key-login-action-buttons div[data-testid="stColumn"],
                .st-key-register-action-buttons div[data-testid="stColumn"] {
                    width: 100% !important;
                    flex: 1 1 100% !important;
                }
            }
            .login-stat-tile {
                background: rgba(255, 255, 255, 0.14);
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 12px;
                padding: 12px 8px;
                text-align: center;
            }
            .login-stat-value {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.3rem;
                line-height: 1.1;
            }
            .login-stat-label {
                font-family: var(--font-body);
                font-size: 0.66rem;
                opacity: 0.85;
                margin-top: 3px;
            }
            .login-mini-cards {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .login-mini-card {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 12px 14px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .login-mini-badge {
                width: 38px;
                height: 38px;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 0.85rem;
                flex-shrink: 0;
            }
            .login-mini-title {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.88rem;
            }
            .login-mini-detail {
                font-family: var(--font-body);
                font-size: 0.74rem;
                opacity: 0.85;
                margin-top: 2px;
            }

            /* 6. Nav tab bar -- replaces the black pill tab buttons */
            .st-key-teacher-nav-tabs {
                background: #FFFFFF !important;
                border-radius: 16px 16px 0 0 !important;
                box-shadow: 0 6px 18px rgba(24, 164, 169, 0.08) !important;
                padding: 6px 6px 0 6px !important;
                border-bottom: 1px solid rgba(30, 36, 48, 0.08) !important;
            }
            .st-key-teacher-nav-tabs div.stButton {
                margin: 0 !important;
            }
            .st-key-teacher-nav-tabs div.stButton > button {
                background: transparent !important;
                color: var(--color-text-muted) !important;
                border: none !important;
                border-radius: 10px 10px 0 0 !important;
                border-bottom: 3px solid transparent !important;
                box-shadow: none !important;
                padding: 14px 10px !important;
                width: 100% !important;
            }
            .st-key-teacher-nav-tabs div.stButton > button:hover {
                background: rgba(24, 164, 169, 0.06) !important;
                color: var(--color-text) !important;
                transform: none !important;
            }
            .st-key-teacher-nav-tabs div.stButton > button[kind="primary"] {
                background: #FFFFFF !important;
                color: var(--color-primary-dark) !important;
                border-bottom: 3px solid var(--color-primary) !important;
                box-shadow: 0 -2px 10px rgba(24, 164, 169, 0.08) !important;
            }

            /* 7. Take Attendance: hero subtitle + mini stat summary bar */
            .teacher-hero-sub {
                font-family: var(--font-body);
                font-size: 0.95rem;
                color: var(--color-text-muted);
                margin: -6px 0 18px 0;
            }
            .mini-stat-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 14px;
                margin: 4px 0 6px 0;
            }
            @media (max-width: 768px) {
                .mini-stat-grid { grid-template-columns: 1fr; }
            }
            .mini-stat-card {
                background: #FFFFFF;
                border-radius: 12px;
                border-top: 3px solid var(--color-primary);
                padding: 14px 16px;
                box-shadow: 0 4px 12px rgba(24, 164, 169, 0.07);
            }
            .mini-stat-value {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.4rem;
                color: var(--color-primary-dark);
                line-height: 1.1;
            }
            .mini-stat-label {
                font-family: var(--font-body);
                font-size: 0.75rem;
                color: var(--color-text-muted);
                font-weight: 600;
                margin-top: 3px;
            }

            /* 8. Manage Subjects: section header row + empty state.
               subject_card.py owns its own card styling -- this only tightens
               the gap between cards to match the page's 16px rhythm. */
            .section-header-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                margin: 4px 0 18px 0;
            }
            .section-header {
                display: flex;
                align-items: center;
                gap: 10px;
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 1.6rem;
                color: var(--color-secondary);
            }
            .section-dot {
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
                flex-shrink: 0;
            }
            .st-key-create-subject-btn div.stButton {
                justify-content: flex-end !important;
            }
            .subject-card {
                margin-bottom: 16px !important;
            }
            [class*="st-key-subjects-empty"] {
                text-align: center !important;
                padding: 60px 20px !important;
                background: #FFFFFF !important;
                border-radius: 20px !important;
                box-shadow: 0 8px 20px rgba(24, 164, 169, 0.08) !important;
                margin: 12px 0 !important;
            }
            .subjects-empty-icon { font-size: 3rem; margin-bottom: 12px; }
            .subjects-empty-title {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 1.3rem;
                color: var(--color-text);
                margin-bottom: 6px;
            }
            .subjects-empty-detail {
                font-family: var(--font-body);
                font-size: 0.9rem;
                color: var(--color-text-muted);
                margin-bottom: 20px;
            }

            /* 9. Attendance Records: filter row + white card table */
            .st-key-records-filter-row {
                background: #FFFFFF !important;
                border-radius: 14px !important;
                padding: 14px 18px 2px 18px !important;
                box-shadow: 0 4px 14px rgba(24, 164, 169, 0.06) !important;
                margin-bottom: 16px !important;
            }
            .records-table-card {
                background: #FFFFFF;
                border-radius: 16px;
                padding: 4px;
                box-shadow: 0 10px 26px rgba(24, 164, 169, 0.10);
                overflow: hidden;
                margin-top: 4px;
            }
            .records-table-scroll { overflow-x: auto; }
            table.records-table {
                width: 100%;
                border-collapse: collapse;
                font-family: var(--font-body);
                font-size: 0.9rem;
            }
            table.records-table thead th {
                background: #E4F4F4;
                color: var(--color-secondary);
                font-family: var(--font-heading);
                font-weight: 600;
                text-align: left;
                padding: 14px 18px;
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.4px;
            }
            table.records-table thead th:first-child { border-radius: 12px 0 0 0; }
            table.records-table thead th:last-child { border-radius: 0 12px 0 0; }
            table.records-table tbody td {
                padding: 12px 18px;
                color: var(--color-text);
                border-bottom: 1px solid rgba(30, 36, 48, 0.06);
            }
            table.records-table tbody tr:nth-child(even) { background: #F8FAFB; }
            table.records-table tbody tr:last-child td { border-bottom: none; }
            .status-pill {
                display: inline-block;
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.8rem;
                padding: 4px 12px;
                border-radius: 20px;
            }
            .status-pill.good { background: rgba(24, 164, 169, 0.12); color: var(--color-primary-dark); }
            .status-pill.mid { background: rgba(245, 166, 35, 0.15); color: #B8791A; }
            .status-pill.poor { background: rgba(196, 69, 58, 0.12); color: #C4453A; }

            /* Reported Issues tab: one card per dispute */
            [class*="st-key-dispute-entry-"] {
                background: #FFFFFF !important;
                border-radius: 12px !important;
                border-left: 4px solid #F5A623 !important;
                padding: 14px 18px !important;
                margin-bottom: 12px !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
            }
            [class*="st-key-dispute-entry-resolved-"] {
                border-left-color: #1F9D55 !important;
                opacity: 0.72;
            }
            .dispute-entry-top {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
            }
            .dispute-entry-student {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 1rem;
                color: var(--color-secondary);
            }
            .dispute-entry-meta {
                font-family: var(--font-body);
                font-size: 0.76rem;
                color: var(--color-text-muted);
                margin-top: 1px;
            }
            .dispute-entry-message {
                font-family: var(--font-body);
                font-size: 0.85rem;
                color: var(--color-text);
                margin-top: 8px;
                line-height: 1.4;
            }
            .dispute-badge {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.72rem;
                padding: 3px 12px;
                border-radius: 20px;
                white-space: nowrap;
            }
            .dispute-badge.open { background: rgba(245, 166, 35, 0.15); color: #B8791A; }
            .dispute-badge.resolved { background: rgba(31, 157, 85, 0.12); color: #1F9D55; }
            .dispute-reply {
                font-family: var(--font-body);
                font-size: 0.85rem;
                color: var(--color-text);
                margin-top: 8px;
                padding: 8px 12px;
                background: rgba(24, 164, 169, 0.07);
                border-radius: 8px;
                line-height: 1.4;
            }
            .dispute-reply-label {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.4px;
                color: var(--color-primary-dark);
                margin-bottom: 3px;
            }

            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    set_global_styles()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()




def _fmt_dt(ts, fmt='%b %d, %Y %I:%M %p'):
    if not ts:
        return None
    try:
        dt = dateutil.parser.parse(ts).replace(tzinfo=None)
    except (ValueError, TypeError):
        return None
    return dt.strftime(fmt)


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data['teacher_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()


    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    # Fetched once here so the open-count badge in the tab label and the tab
    # body itself (when active) share the same query instead of double-fetching.
    disputes = get_disputes_for_teacher(teacher_id)
    open_dispute_count = sum(1 for d in disputes if d.get('status') != 'resolved')
    issues_label = f"Reported Issues ({open_dispute_count})" if open_dispute_count else "Reported Issues"

    with st.container(key="teacher-nav-tabs"):
        tab1, tab2, tab3, tab4 = st.columns(4)

        with tab1:
            type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
            if st.button('Take Attendance',type=type1, width='stretch'):
                st.session_state.current_teacher_tab = 'take_attendance'
                st.rerun()

        with tab2:
            type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
            if st.button('Manage Subjects', type=type2, width='stretch'):
                st.session_state.current_teacher_tab = 'manage_subjects'
                st.rerun()

        with tab3:
            type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
            if st.button('Attendance Records',type=type3, width='stretch'):
                st.session_state.current_teacher_tab = 'attendance_records'
                st.rerun()

        with tab4:
            type4 = "primary" if st.session_state.current_teacher_tab == 'reported_issues' else "tertiary"
            if st.button(issues_label, type=type4, width='stretch'):
                st.session_state.current_teacher_tab = 'reported_issues'
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
    if st.session_state.current_teacher_tab == "reported_issues":
        teacher_tab_reported_issues(disputes)



    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    st.markdown("""
        <h2 style="margin-bottom:2px;">Take Attendance</h2>
        <p class="teacher-hero-sub">Select a subject and capture classroom photos</p>
    """, unsafe_allow_html=True)


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}
    subjects_by_id = {s['subject_id']: s for s in subjects}

    selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))
    selected_subject_id = subject_options[selected_subject_label]
    selected_subject = subjects_by_id[selected_subject_id]

    # Read-only summary bar -- reuses the already-imported get_attendance_for_teacher,
    # no new business logic, just an aggregate over data already fetched elsewhere.
    teacher_records = get_attendance_for_teacher(teacher_id)
    subject_records = [r for r in teacher_records if (r.get('subjects') or {}).get('subject_id') == selected_subject_id]
    if subject_records:
        present_count = sum(1 for r in subject_records if r.get('is_present'))
        attendance_rate = f"{round((present_count / len(subject_records)) * 100)}%"
        last_ts = max((r['timestamp'] for r in subject_records if r.get('timestamp')), default=None)
        last_attendance = _fmt_dt(last_ts, '%b %d, %Y') if last_ts else "—"
    else:
        attendance_rate = "—"
        last_attendance = "—"

    st.markdown(f"""
        <div class="mini-stat-grid">
            <div class="mini-stat-card"><div class="mini-stat-value">{selected_subject.get('total_students', 0)}</div><div class="mini-stat-label">Total Students</div></div>
            <div class="mini-stat-card"><div class="mini-stat-value">{last_attendance}</div><div class="mini-stat-label">Last Attendance</div></div>
            <div class="mini-stat-card"><div class="mini-stat-value">{attendance_rate}</div><div class="mini-stat-label">Attendance Rate</div></div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.session_state.attendance_images:
        st.subheader('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
        st.divider()

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button('Add Photos', type='primary', width='stretch'):
            add_photos_dialog()

    with c2:
        if st.button('Clear all photos', width='stretch', type='tertiary', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


    with c3:
        with st.container(key="btn-face-analysis"):
            if st.button('Run Face Analysis', width='stretch', type='secondary', disabled=not has_photos):
                with st.spinner('Deep scanning classroom photos...'):
                    all_detected_ids = {}

                    for idx, img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB'))
                        detected, _, _ = predict_attendance(img_np)

                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                    enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                    enrolled_students = enrolled_res.data

                    if not enrolled_students:
                        st.warning('No students enrolled in this course')
                    else:
                        results, attendance_to_log = [], []
                        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                        # Added human-readable fields
                        readable_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                        subject_name = selected_subject_label

                        for node in enrolled_students:
                            student = node['students']
                            sources = all_detected_ids.get(int(student['student_id']), [])
                            is_present = len(sources) > 0

                            results.append({
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Subject": subject_name,
                                "Time": readable_time,
                                "Source": ", ".join(sources) if is_present else "-",
                                "Status": "✅ Present" if is_present else "❌ Absent",
                                # FEATURE 4: 'students(*)' already selects every
                                # column including the new 'avatar' one -- no
                                # query change needed here, just carrying it
                                # through to the results table.
                                "Avatar": student.get('avatar', '🙂'),
                            })

                            attendance_to_log.append({
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })

                        # Save to state and refresh to trigger persistent display
                        st.session_state.face_attendance_results = (pd.DataFrame(results), attendance_to_log)
                        st.rerun()

    with c4:
        if st.button('Use Voice Attendance', type='secondary', width='stretch'):
            voice_attendance_dialog(selected_subject_id)

     # --- PERSISTENT FACE ATTENDANCE DISPLAY ---
    if 'face_attendance_results' in st.session_state and st.session_state.face_attendance_results is not None:
        st.divider()
        st.subheader("Face Attendance Results")
        df_face, logs_face = st.session_state.face_attendance_results

        # Pass a unique key here to avoid conflict
        show_attendance_result(df_face, logs_face, key_prefix="face")

        # Add a unique key here
        if st.button("Clear Face Results", key="clear_face_btn"):
            st.session_state.face_attendance_results = None
            st.rerun()

    # --- PERSISTENT VOICE ATTENDANCE DISPLAY ---
    if 'voice_attendance_results' in st.session_state and st.session_state.voice_attendance_results is not None:
        st.divider()
        st.subheader("Voice Attendance Results")

        # Pass a unique key here to avoid conflict
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs, key_prefix="voice")

        # Add a unique key here
        if st.button("Clear Voice Results", key="clear_voice_btn"):
            st.session_state.voice_attendance_results = None
            st.rerun()


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    header_col, button_col = st.columns([3, 1], vertical_alignment='center')
    with header_col:
        st.markdown('<div class="section-header"><span class="section-dot"></span>Manage Subjects</div>', unsafe_allow_html=True)
    with button_col:
        with st.container(key="create-subject-btn"):
            if st.button('Create New Subject', width='stretch', type='primary'):
                create_subject_dialog(teacher_id)

    st.markdown("<br>", unsafe_allow_html=True)

    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        # NOTE: previously `def share_btn` and the `subject_card(...)` call were
        # dedented outside this loop, so only the *last* subject in the list
        # ever rendered a card. Indenting them back inside the loop is a
        # rendering-scope fix (every subject now gets its own card), not a
        # business-logic change -- no data/query behavior is touched.
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_id']}"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        with st.container(key="subjects-empty"):
            st.markdown("""
                <div class="subjects-empty-icon">📚</div>
                <div class="subjects-empty-title">No subjects yet</div>
                <div class="subjects-empty-detail">Create your first subject to start taking attendance.</div>
            """, unsafe_allow_html=True)
            if st.button('Create your first subject', type='primary'):
                create_subject_dialog(teacher_id)


def teacher_tab_attendance_records():
    st.markdown('<div class="section-header"><span class="section-dot"></span>Attendance Records</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records yet.")
        return

    data = []

    for r in records:
        ts = r.get('timestamp')
        log_date = None
        if ts:
            try:
                log_date = dateutil.parser.parse(ts).replace(tzinfo=None).date()
            except (ValueError, TypeError):
                log_date = None

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "log_date": log_date,
            "Time": _fmt_dt(ts) or "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)
    df = df.dropna(subset=['log_date'])

    if df.empty:
        st.info("No attendance records yet.")
        return

    with st.container(key="records-filter-row"):
        filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])
        with filter_col1:
            subject_choices = ['All Subjects'] + sorted(df['Subject'].unique().tolist())
            selected_subject_filter = st.selectbox('Filter by Subject', options=subject_choices)
        with filter_col2:
            start_date = st.date_input('From', value=df['log_date'].min())
        with filter_col3:
            end_date = st.date_input('To', value=df['log_date'].max())

    filtered_df = df.copy()
    if selected_subject_filter != 'All Subjects':
        filtered_df = filtered_df[filtered_df['Subject'] == selected_subject_filter]
    filtered_df = filtered_df[(filtered_df['log_date'] >= start_date) & (filtered_df['log_date'] <= end_date)]

    if filtered_df.empty:
        st.info("No records match this filter.")
        return

    summary = (
        filtered_df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['pct'] = (summary['Present_Count'] / summary['Total_Count'] * 100).round().astype(int)

    def _status_class(pct):
        if pct >= 80:
            return 'good'
        if pct >= 50:
            return 'mid'
        return 'poor'

    display_df = summary.sort_values(by='ts_group', ascending=False)

    rows_html = ""
    for _, row in display_df.iterrows():
        status_class = _status_class(row['pct'])
        rows_html += (
            f"<tr><td>{row['Time']}</td><td>{row['Subject']}</td><td>{row['Subject Code']}</td>"
            f"<td><span class=\"status-pill {status_class}\">{row['Present_Count']}/{row['Total_Count']} Students</span></td></tr>"
        )

    st.markdown(f"""
        <div class="records-table-card">
            <div class="records-table-scroll">
                <table class="records-table">
                    <thead><tr><th>Time</th><th>Subject</th><th>Subject Code</th><th>Attendance Stats</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>
    """, unsafe_allow_html=True)


def _render_dispute_entry(d, resolved):
    dispute_id = d['dispute_id']
    student_name = (d.get('students') or {}).get('name', 'Unknown student')
    subject_name = (d.get('subjects') or {}).get('name', 'Unknown subject')
    class_date = d.get('class_date', '—')
    message = d.get('student_message', '')
    reply = d.get('teacher_reply') or ''
    status_class = 'resolved' if resolved else 'open'
    status_label = '✅ Resolved' if resolved else '🟡 Open'

    # 'resolved'/'open' baked into the container key (not just a markup
    # class) so the CSS can grey out resolved entries -- same pattern as
    # the subject cards' performance-tier-in-key trick in student_screen.py.
    with st.container(key=f"dispute-entry-{status_class}-{dispute_id}"):
        st.markdown(f"""
            <div class="dispute-entry-top">
                <div>
                    <div class="dispute-entry-student">{student_name}</div>
                    <div class="dispute-entry-meta">{subject_name} &middot; {class_date}</div>
                </div>
                <div class="dispute-badge {status_class}">{status_label}</div>
            </div>
            <div class="dispute-entry-message">{message}</div>
        """, unsafe_allow_html=True)

        if reply:
            st.markdown(
                f'<div class="dispute-reply"><div class="dispute-reply-label">Your reply</div>{reply}</div>',
                unsafe_allow_html=True,
            )

        # Reply is always available, even for resolved disputes -- previously
        # this was gated behind `if not resolved:` along with the resolve
        # button, which meant a dispute resolved before ever being replied
        # to could never receive a reply again (the whole input+button
        # block disappeared for good). Only "Mark as Resolved" itself should
        # be one-directional/gated.
        reply_col, send_col = st.columns([3, 1])
        with reply_col:
            new_reply = st.text_input(
                "Reply", value=reply, key=f"reply_input_{dispute_id}",
                label_visibility="collapsed", placeholder="Type a reply to the student...",
            )
        with send_col:
            if st.button("Send Reply", key=f"send_reply_{dispute_id}", width='stretch'):
                reply_to_dispute(dispute_id, new_reply)
                st.toast("Reply sent!")
                st.rerun()

        if not resolved:
            if st.button("✅ Mark as Resolved", key=f"resolve_{dispute_id}", type='secondary', width='stretch'):
                resolve_dispute(dispute_id)
                st.toast("Marked as resolved!")
                st.rerun()


def teacher_tab_reported_issues(disputes):
    st.markdown('<div class="section-header"><span class="section-dot"></span>Reported Issues</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not disputes:
        st.info("No reported issues yet.")
        return

    open_disputes = [d for d in disputes if d.get('status') != 'resolved']
    resolved_disputes = [d for d in disputes if d.get('status') == 'resolved']

    st.subheader(f"Open ({len(open_disputes)})")
    if not open_disputes:
        st.caption("No open issues -- you're all caught up.")
    for d in open_disputes:
        _render_dispute_entry(d, resolved=False)

    if resolved_disputes:
        st.subheader(f"Resolved ({len(resolved_disputes)})")
        for d in resolved_disputes:
            _render_dispute_entry(d, resolved=True)


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True


    return False


def _teacher_login_left_panel():
    # This screen only renders when 'teacher_data' isn't in session_state
    # (see teacher_screen()'s dispatch), so the "logged in" branch below is
    # defensive rather than reachable today -- kept anyway since the spec
    # calls for real data whenever a teacher_id is actually available,
    # rather than assuming this component is only ever used pre-login.
    is_logged_in = bool(st.session_state.get('teacher_data'))

    total_students = len(get_all_students())

    subjects = []
    if is_logged_in:
        teacher_id = st.session_state.teacher_data['teacher_id']
        subjects = get_teacher_subjects(teacher_id)
        total_subjects = len(subjects)
        records = get_attendance_for_teacher(teacher_id)
        total_classes = len(set(r['timestamp'] for r in records if r.get('timestamp')))
    else:
        total_subjects = "—"
        total_classes = "—"

    with st.container(key="teacher-login-left"):
        st.markdown(f"""
            <div class="login-left-eyebrow">SnapClass</div>
            <div class="login-left-title">AI-powered attendance,<br/>in seconds.</div>
            <div class="login-left-sub">Face and voice recognition mark attendance automatically — no roll call, no paperwork.</div>
            <div class="login-stat-row">
                <div class="login-stat-tile"><div class="login-stat-value">{total_students}</div><div class="login-stat-label">Students</div></div>
                <div class="login-stat-tile"><div class="login-stat-value">{total_subjects}</div><div class="login-stat-label">Subjects</div></div>
                <div class="login-stat-tile"><div class="login-stat-value">{total_classes}</div><div class="login-stat-label">Classes Held</div></div>
            </div>
        """, unsafe_allow_html=True)

        if is_logged_in and subjects:
            # "Top 2" by enrolled student count.
            top_subjects = sorted(subjects, key=lambda s: s.get('total_students', 0), reverse=True)[:2]
            cards_html = '<div class="login-mini-cards">'
            for sub in top_subjects:
                initials = ''.join(w[0] for w in sub['name'].split()[:2]).upper() or '??'
                cards_html += f"""
                    <div class="login-mini-card">
                        <div class="login-mini-badge">{initials}</div>
                        <div>
                            <div class="login-mini-title">{sub['name']}</div>
                            <div class="login-mini-detail">{sub.get('total_students', 0)} students &middot; {sub['subject_code']}</div>
                        </div>
                    </div>
                """
            cards_html += '</div>'
            st.markdown(cards_html, unsafe_allow_html=True)
        else:
            # Not logged in yet -- no real subjects to show, so this is a
            # feature highlight instead of fabricated placeholder stats.
            st.markdown("""
                <div class="login-mini-cards">
                    <div class="login-mini-card">
                        <div class="login-mini-badge">🙂</div>
                        <div>
                            <div class="login-mini-title">Face recognition check-in</div>
                            <div class="login-mini-detail">Marks attendance in under 4 seconds</div>
                        </div>
                    </div>
                    <div class="login-mini-card">
                        <div class="login-mini-badge">🎙️</div>
                        <div>
                            <div class="login-mini-title">Voice attendance</div>
                            <div class="login-mini-detail">Audio-based backup verification</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        # The line below was missing the correct indentation/logic flow
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = 'home'
            st.rerun()

    left_col, right_col = st.columns([4, 5], gap='large')

    with left_col:
        _teacher_login_left_panel()

    with right_col:
        with st.container(key="teacher-login-card"):
            st.markdown("""
                <div class="teacher-auth-title">Teacher Login</div>
                <div class="teacher-auth-subtitle">Sign in with your username and password</div>
            """, unsafe_allow_html=True)

            teacher_username = st.text_input("Enter username", placeholder='Enter username')

            teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

            st.divider()

            with st.container(key="login-action-buttons"):
                btnc1, btnc2 = st.columns(2)

                with btnc1:
                    if st.button('Login', shortcut='control+enter', width='stretch', type='primary'):
                        if login_teacher(teacher_username, teacher_pass):
                            st.toast("welcome back!", icon="👋")
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid username and password combo")

                with btnc2:
                    if st.button('Register Instead', type="secondary", width='stretch'):
                        st.session_state.teacher_login_type = 'register'

    footer_dashboard()



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()



    with st.container(key="teacher-register-card"):
        st.markdown("""
            <div class="teacher-auth-title">Register Teacher Profile</div>
            <div class="teacher-auth-subtitle">Create your teacher account to get started</div>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Enter username", placeholder='Enter username')

        teacher_name = st.text_input("Enter name", placeholder='Enter your name')

        teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

        teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")

        st.divider()

        with st.container(key="register-action-buttons"):
            btnc1, btnc2 = st.columns(2)

            with btnc1:
                if st.button('Register now', shortcut='control+enter', width='stretch', type='primary'):
                    success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                    if success:
                        st.success(message)
                        import time
                        time.sleep(2)
                        st.session_state.teacher_login_type = "login"
                        st.rerun()
                    else:
                        st.error(message)


            with btnc2:
                if st.button('Login Instead', type="secondary", width='stretch'):
                    st.session_state.teacher_login_type = 'login'

    footer_dashboard()
