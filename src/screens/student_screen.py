import streamlit as st
import plotly.graph_objects as go
import dateutil.parser
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from datetime import date, datetime, timedelta
from src.components.dialog_enroll import enroll_dialog

# Minimal monoline SVG icons for the stat cards -- stroke="currentColor" so
# each one picks up its color from the wrapping .icon-* span, no emoji.
_ICON_CALENDAR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
_ICON_CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="8 12 11 15 16 9"/></svg>'
_ICON_FLAME = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1 4-4 5-4 9a4 4 0 0 0 8 0c0-2-1-3-1-3s2 1 2 4a6 6 0 1 1-12 0c0-5 4-6 4-10z"/></svg>'

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
            .stApp, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, div, p, span, label {
                color: var(--color-text) !important;
                font-family: var(--font-body) !important;
            }
            .stApp h1, .stApp h2, .stApp h3 {
                font-family: var(--font-heading) !important;
            }

            /* Same background gradient as landing/home for continuity */
            .stApp {
                background: linear-gradient(135deg, #EAF7F8 0%, #DDEFF2 55%, #E9E4F5 100%) !important;
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

            /* 3. Buttons: teal gradient pill for primary, outlined teal for secondary,
               muted outline for tertiary (Unenroll) so it doesn't compete visually */
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
                color: var(--color-primary-dark) !important;
                border: 2px solid var(--color-primary) !important;
                box-shadow: 0 4px 12px rgba(24, 164, 169, 0.12) !important;
            }
            div.stButton > button[kind="secondary"]:hover {
                background: rgba(24, 164, 169, 0.08) !important;
                box-shadow: 0 8px 18px rgba(24, 164, 169, 0.2) !important;
            }

            div.stButton > button[kind="tertiary"] {
                background: #FFFFFF !important;
                color: var(--color-text-muted) !important;
                border: 1px solid rgba(82, 96, 109, 0.35) !important;
                box-shadow: none !important;
                font-weight: 600 !important;
                padding: 8px 22px !important;
                font-size: 0.9rem !important;
            }
            div.stButton > button[kind="tertiary"]:hover {
                border-color: #B3261E !important;
                color: #B3261E !important;
                transform: none;
            }

            /* 4. Input and Selectbox, on-brand */
            .stTextInput input,
            div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                color: var(--color-text) !important;
                border: 1px solid rgba(24, 164, 169, 0.3) !important;
                border-radius: 10px !important;
            }
            .stTextInput input::placeholder {
                color: var(--color-text-muted) !important;
            }

            /* Card containers (login panel / registration), with fade-in on load */
            .st-key-login-panel, .st-key-registration-card {
                background: #FFFFFF !important;
                border-radius: 24px !important;
                padding: 3rem !important;
                box-shadow: 0 12px 28px rgba(24, 164, 169, 0.12) !important;
                margin-bottom: 28px !important;
                animation: fadeInUp 0.6s ease both;
            }
            .st-key-registration-card {
                border: 1px solid rgba(24, 164, 169, 0.25) !important;
            }
            .st-key-login-panel {
                border: 1px solid var(--color-surface-border) !important;
            }

            /* More breathing room around the whole view */
            .block-container {
                padding-top: 2.5rem !important;
                padding-bottom: 3rem !important;
            }
            @media (min-width: 1000px) {
                .block-container {
                    padding-left: 80px !important;
                    padding-right: 80px !important;
                }
            }

            .login-header {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
                margin-bottom: 4px;
            }
            .login-icon {
                font-size: 2.6rem;
                line-height: 1;
            }
            .login-title {
                font-family: var(--font-heading) !important;
                font-weight: 800 !important;
                font-size: 2.3rem !important;
                color: var(--color-text) !important;
                margin: 0 !important;
                text-align: center;
            }

            .subtitle-muted {
                color: var(--color-text-muted) !important;
                font-family: var(--font-body) !important;
                font-size: 1.05rem !important;
                text-align: center;
                margin: 0 0 20px 0 !important;
            }

            .step-strip {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 14px;
                flex-wrap: wrap;
                margin: 4px 0 28px 0;
            }
            .step-chip {
                display: flex;
                align-items: center;
                gap: 8px;
                background: rgba(24, 164, 169, 0.08);
                padding: 10px 18px;
                border-radius: 30px;
                font-family: var(--font-body);
                font-size: 0.92rem;
                color: var(--color-text);
            }
            .step-num {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 22px;
                height: 22px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
                color: #ffffff;
                font-weight: 700;
                font-size: 0.78rem;
                flex-shrink: 0;
            }
            .step-arrow {
                color: var(--color-text-muted);
                font-size: 1.2rem;
            }

            /* Camera widget's own shutter button lives outside div.stButton,
               so it needs its own selector to pick up the brand pill style */
            [data-testid="stCameraInputButton"] {
                background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
                color: #ffffff !important;
                font-family: var(--font-heading) !important;
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

            /* Dashboard: top stat cards, 4 across / 2x2 on narrow screens.
               Compact/dense by design -- this is the lightest-weight tier of card. */
            .stat-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
                margin: 8px 0 16px 0;
            }
            @media (max-width: 900px) {
                .stat-grid { grid-template-columns: repeat(2, 1fr); }
            }
            .stat-card {
                background: #FFFFFF;
                border-radius: 10px;
                border-top: 3px solid var(--color-primary);
                padding: 10px 14px 9px 14px;
                text-align: left;
                box-shadow: 0 4px 12px rgba(24, 164, 169, 0.07);
                transition: transform 0.25s ease, box-shadow 0.25s ease;
                animation: fadeInUp 0.6s ease both;
            }
            .stat-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 18px rgba(24, 164, 169, 0.13);
            }
            .stat-card.total { border-top-color: #4C4FD9; }
            .stat-card.streak { border-top-color: #F5A623; }
            .stat-top {
                display: flex;
                align-items: center;
                gap: 6px;
                margin-bottom: 4px;
            }
            .stat-icon { display: inline-flex; line-height: 0; }
            .icon-teal { color: var(--color-primary-dark); }
            .icon-indigo { color: #4C4FD9; }
            .icon-amber { color: #B8791A; }
            .stat-value {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.55rem;
                color: var(--color-primary-dark);
                line-height: 1.1;
            }
            .stat-label {
                font-family: var(--font-body);
                font-size: 0.72rem;
                color: var(--color-text-muted);
                font-weight: 600;
            }
            .stat-caption {
                font-family: var(--font-body);
                font-size: 0.68rem;
                color: var(--color-text-muted);
                margin-top: 2px;
            }

            /* Dashboard: best/needs-attention insight pair -- one visual tier up
               from the stat cards, but compact: a colored left border carries
               the accent instead of a full tinted background. */
            .insight-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                margin: 0 0 16px 0;
            }
            @media (max-width: 700px) {
                .insight-grid { grid-template-columns: 1fr; }
            }
            .insight-card {
                display: flex;
                align-items: center;
                gap: 12px;
                background: #FFFFFF;
                border-radius: 10px;
                border-left: 4px solid transparent;
                padding: 13px 18px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
                transition: transform 0.25s ease, box-shadow 0.25s ease;
                animation: fadeInUp 0.6s ease both;
            }
            .insight-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
            }
            .insight-card.best { border-left-color: #1F9D55; }
            .insight-card.worst { border-left-color: #B8791A; }
            .insight-icon { font-size: 1.35rem; flex-shrink: 0; }
            .insight-label {
                font-family: var(--font-heading);
                font-size: 0.68rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 700;
            }
            .insight-card.best .insight-label { color: #1F9D55; }
            .insight-card.worst .insight-label { color: #B8791A; }
            .insight-name {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 1rem;
                color: var(--color-text);
                margin-top: 1px;
            }
            .insight-detail {
                font-family: var(--font-body);
                font-size: 0.76rem;
                color: var(--color-text-muted);
                margin-top: 1px;
            }
            .insight-pct {
                margin-left: auto;
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.4rem;
                flex-shrink: 0;
            }
            .insight-card.best .insight-pct { color: #1F9D55; }
            .insight-card.worst .insight-pct { color: #B8791A; }


            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Dashboard: hero card -- top-of-page summary, one visual tier above
               everything else on the page (biggest shadow, biggest number). */
            .st-key-hero-card {
                background: #FFFFFF !important;
                border-radius: 20px !important;
                padding: 24px 28px !important;
                box-shadow: 0 14px 34px rgba(24, 164, 169, 0.14) !important;
                margin: 8px 0 16px 0 !important;
                animation: fadeInUp 0.6s ease both;
            }
            .hero-label {
                font-family: var(--font-heading);
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                font-weight: 700;
                color: var(--color-primary-dark);
                margin-bottom: 6px;
            }
            .hero-value {
                font-family: var(--font-heading);
                font-weight: 900;
                font-size: 3.2rem;
                line-height: 1;
                color: var(--color-text);
            }
            .hero-sub {
                font-family: var(--font-body);
                font-size: 0.85rem;
                color: var(--color-text-muted);
                margin-top: 8px;
            }

            /* Dashboard: subject cards, 2-column grid -- one card per subject.
               Card chrome (bg/shadow/left-border) lives on the *container*
               (keyed per-subject, with the performance tier baked into the
               key so the border color can vary per card) so the Unenroll
               button sits inside the same visual card as the stats above it,
               instead of floating outside it in a popover. */
            [class*="st-key-subject-card-"] {
                background: #FFFFFF !important;
                border-radius: 12px !important;
                border-left: 4px solid var(--color-primary) !important;
                padding: 16px 18px 12px 16px !important;
                box-shadow: 0 6px 16px rgba(24, 164, 169, 0.08) !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
                animation: fadeInUp 0.6s ease both;
                margin-bottom: 16px !important;
            }
            [class*="st-key-subject-card-"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 22px rgba(24, 164, 169, 0.13) !important;
            }
            [class*="st-key-subject-card-mid-"] { border-left-color: #F5A623 !important; }
            [class*="st-key-subject-card-poor-"] { border-left-color: #C4453A !important; }
            [class*="st-key-subject-card-"] div.stButton { justify-content: flex-end !important; margin-top: 8px !important; }
            [class*="st-key-subject-card-"] div.stButton > button {
                padding: 5px 16px !important;
                font-size: 0.78rem !important;
            }
            .subject-card-top {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 10px;
            }
            .subject-card-name {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.2rem;
                color: var(--color-text);
            }
            .subject-card-code {
                font-family: var(--font-body);
                font-size: 0.74rem;
                color: var(--color-text-muted);
                margin-top: 2px;
            }
            .subject-card-metrics {
                display: flex;
                align-items: baseline;
                justify-content: space-between;
                margin-top: 12px;
            }
            .subject-card-count {
                font-family: var(--font-heading);
                font-weight: 900;
                font-size: 2.4rem;
                line-height: 1;
                color: var(--color-text);
            }
            .subject-card-count-label {
                font-family: var(--font-body);
                font-size: 0.72rem;
                color: var(--color-text-muted);
                font-weight: 500;
            }
            .badge {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 0.95rem;
                padding: 4px 12px;
                border-radius: 20px;
            }
            .badge.good { background: rgba(24, 164, 169, 0.12); color: var(--color-primary-dark); }
            .badge.mid { background: rgba(245, 166, 35, 0.15); color: #B8791A; }
            .badge.poor { background: rgba(196, 69, 58, 0.12); color: #C4453A; }
            .subject-card-track {
                width: 100%;
                height: 8px;
                border-radius: 5px;
                background: rgba(30, 36, 48, 0.07);
                margin-top: 12px;
                overflow: hidden;
            }
            .subject-card-fill {
                height: 100%;
                border-radius: 5px;
                background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
            }
            .subject-card-fill.mid { background: linear-gradient(90deg, #F5A623, #B8791A); }
            .subject-card-fill.poor { background: linear-gradient(90deg, #E0685B, #C4453A); }
            .subject-card-change {
                font-family: var(--font-body);
                font-size: 0.75rem;
                color: var(--color-text-muted);
                margin-top: 8px;
            }
            .subject-card-change.positive { color: var(--color-primary-dark); font-weight: 600; }

            .section-header-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                margin: 6px 0 4px 0;
            }
            .section-header-row h2 { margin: 0 !important; }
            .section-header {
                display: flex;
                align-items: center;
                gap: 10px;
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.4rem;
                color: var(--color-text);
            }
            .section-dot {
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
                flex-shrink: 0;
            }
            .section-divider {
                height: 1px;
                background: rgba(30, 36, 48, 0.08);
                margin: 10px 0 18px 0;
            }
            .st-key-enroll-btn-wrap div.stButton { justify-content: flex-end !important; }
        </style>
    """, unsafe_allow_html=True)


def _parse_log_date(log):
    ts = log.get('timestamp')
    if not ts:
        return None
    try:
        dt = dateutil.parser.parse(ts)
    except (ValueError, TypeError):
        return None
    # Logs are written with datetime.now().strftime(...) -- a naive LOCAL
    # wall-clock string with no offset. Supabase's timestamptz column stores
    # that naive string as if it were UTC, so it round-trips back tagged
    # "+00:00" even though the digits are still local time. astimezone()
    # would treat that tag as real and shift the value again, double
    # counting the UTC offset. Stripping the (false) tzinfo instead recovers
    # the original local wall-clock value as written.
    dt = dt.replace(tzinfo=None)
    return dt.date()


def _compute_dashboard_stats(logs):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    month_start = today.replace(day=1)
    trend_start = today - timedelta(days=13)

    week_present = week_total = 0
    month_present = month_total = 0
    total_attended = 0
    total_logs = 0
    day_presence = {}
    day_present_count = {}
    day_total_count = {}
    subject_stats = {}

    for log in logs:
        is_present = bool(log.get('is_present'))
        sid = log.get('subject_id')
        sub = log.get('subjects') or {}
        sname = sub.get('name', 'Unknown')

        stat = subject_stats.setdefault(sid, {'total': 0, 'attended': 0, 'name': sname, 'week_attended': 0})
        stat['total'] += 1
        total_logs += 1
        if is_present:
            stat['attended'] += 1
            total_attended += 1

        log_date = _parse_log_date(log)
        if log_date is None:
            continue

        if week_start <= log_date <= week_end:
            week_total += 1
            if is_present:
                week_present += 1
                stat['week_attended'] += 1

        if month_start <= log_date <= today:
            month_total += 1
            if is_present:
                month_present += 1

        if trend_start <= log_date <= today:
            day_total_count[log_date] = day_total_count.get(log_date, 0) + 1
            if is_present:
                day_present_count[log_date] = day_present_count.get(log_date, 0) + 1

        if is_present:
            day_presence[log_date] = True
        else:
            day_presence.setdefault(log_date, False)

    week_pct = round((week_present / week_total) * 100) if week_total else None
    month_pct = round((month_present / month_total) * 100) if month_total else None
    overall_pct = round((total_attended / total_logs) * 100) if total_logs else None

    daily_series = []
    for i in range(14):
        d = trend_start + timedelta(days=i)
        d_total = day_total_count.get(d, 0)
        d_present = day_present_count.get(d, 0)
        pct = round((d_present / d_total) * 100) if d_total else 0
        daily_series.append({'date': d, 'pct': pct})

    streak = 0
    cursor = today
    if day_presence.get(cursor) is not True:
        cursor -= timedelta(days=1)
    while day_presence.get(cursor) is True:
        streak += 1
        cursor -= timedelta(days=1)

    best = worst = None
    for stat in subject_stats.values():
        if stat['total'] == 0:
            continue
        pct = round((stat['attended'] / stat['total']) * 100)
        entry = {'name': stat['name'], 'pct': pct, 'attended': stat['attended'], 'total': stat['total']}
        if best is None or pct > best['pct']:
            best = entry
        if worst is None or pct < worst['pct']:
            worst = entry

    return {
        'week_pct': week_pct,
        'week_present': week_present,
        'week_total': week_total,
        'month_pct': month_pct,
        'month_present': month_present,
        'month_total': month_total,
        'overall_pct': overall_pct,
        'total_attended': total_attended,
        'total_logs': total_logs,
        'streak': streak,
        'best': best,
        'worst': worst,
        'subject_stats': subject_stats,
        'daily_series': daily_series,
    }


def _fmt_pct(pct):
    return f"{pct}%" if pct is not None else "—"


def _render_hero_card(stats):
    overall_value = _fmt_pct(stats['overall_pct'])
    sub_caption = f"{stats['total_attended']}/{stats['total_logs']} classes, all time" if stats['total_logs'] else "No attendance recorded yet"

    with st.container(key="hero-card"):
        label_col, chart_col = st.columns([1, 2], vertical_alignment='center', gap='large')
        with label_col:
            st.markdown(f"""
                <div class="hero-label">Attendance Trend</div>
                <div class="hero-value">{overall_value}</div>
                <div class="hero-sub">{sub_caption}</div>
            """, unsafe_allow_html=True)
        with chart_col:
            day_labels = [d['date'].strftime('%b %d') for d in stats['daily_series']]
            pct_values = [d['pct'] for d in stats['daily_series']]
            bar_colors = ['#18A4A9' if p > 0 else '#E8F4F4' for p in pct_values]

            fig = go.Figure(
                data=[go.Bar(
                    x=day_labels,
                    y=pct_values,
                    marker_color=bar_colors,
                    marker_line_width=0,
                    hovertemplate='%{x}<br>%{y}%<extra></extra>',
                )]
            )
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                xaxis=dict(showgrid=False, showline=False, zeroline=False, title=None, tickfont=dict(size=10, color='#52606D')),
                yaxis=dict(showgrid=False, showline=False, zeroline=False, title=None, showticklabels=False, range=[0, 105]),
                font=dict(family='Inter, sans-serif', color='#1E2430'),
            )
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})


def _render_stat_cards(stats):
    week_value = _fmt_pct(stats['week_pct'])
    month_value = _fmt_pct(stats['month_pct'])
    week_caption = f"{stats['week_present']}/{stats['week_total']} classes" if stats['week_total'] else "No classes yet"
    month_caption = f"{stats['month_present']}/{stats['month_total']} classes" if stats['month_total'] else "No classes yet"
    streak_caption = "Keep it up!" if stats['streak'] else "Start today"

    # Built as a single unbroken line: a blank/whitespace-only line here would
    # split this into two Markdown blocks and the second half would render as
    # a raw code block instead of HTML (indented-code-block vs HTML-block rule).
    cards = (
        f'<div class="stat-card week"><div class="stat-top"><span class="stat-icon icon-teal">{_ICON_CALENDAR}</span><span class="stat-label">This Week</span></div><div class="stat-value">{week_value}</div><div class="stat-caption">{week_caption}</div></div>'
        f'<div class="stat-card month"><div class="stat-top"><span class="stat-icon icon-teal">{_ICON_CALENDAR}</span><span class="stat-label">This Month</span></div><div class="stat-value">{month_value}</div><div class="stat-caption">{month_caption}</div></div>'
        f'<div class="stat-card total"><div class="stat-top"><span class="stat-icon icon-indigo">{_ICON_CHECK}</span><span class="stat-label">Total Attended</span></div><div class="stat-value">{stats["total_attended"]}</div><div class="stat-caption">All time</div></div>'
        f'<div class="stat-card streak"><div class="stat-top"><span class="stat-icon icon-amber">{_ICON_FLAME}</span><span class="stat-label">Day Streak</span></div><div class="stat-value">{stats["streak"]}</div><div class="stat-caption">{streak_caption}</div></div>'
    )
    st.markdown(f'<div class="stat-grid">{cards}</div>', unsafe_allow_html=True)


def _render_insight_cards(stats):
    best = stats['best']
    worst = stats['worst']

    best_name = best['name'] if best else 'No data yet'
    best_pct = _fmt_pct(best['pct']) if best else '—'
    best_detail = f"{best['attended']}/{best['total']} classes attended" if best else 'Attend a class to see insights'

    worst_name = worst['name'] if worst else 'No data yet'
    worst_pct = _fmt_pct(worst['pct']) if worst else '—'
    worst_detail = f"{worst['attended']}/{worst['total']} classes attended" if worst else 'Attend a class to see insights'

    # Same single-line construction as _render_stat_cards, for the same reason.
    best_card = (
        f'<div class="insight-card best"><div class="insight-icon">🏆</div>'
        f'<div class="insight-body"><div class="insight-label">Best Subject</div>'
        f'<div class="insight-name">{best_name}</div><div class="insight-detail">{best_detail}</div></div>'
        f'<div class="insight-pct">{best_pct}</div></div>'
    )
    worst_card = (
        f'<div class="insight-card worst"><div class="insight-icon">⚠️</div>'
        f'<div class="insight-body"><div class="insight-label">Needs Attention</div>'
        f'<div class="insight-name">{worst_name}</div><div class="insight-detail">{worst_detail}</div></div>'
        f'<div class="insight-pct">{worst_pct}</div></div>'
    )
    st.markdown(f'<div class="insight-grid">{best_card}{worst_card}</div>', unsafe_allow_html=True)


def _render_subject_card(sub, subj_stats, student_id):
    sid = sub['subject_id']
    total = subj_stats.get('total', 0)
    attended = subj_stats.get('attended', 0)
    week_attended = subj_stats.get('week_attended', 0)
    pct = round((attended / total) * 100) if total else 0

    if pct >= 80:
        pct_class = "good"
    elif pct >= 50:
        pct_class = "mid"
    else:
        pct_class = "poor"

    change_text = f"+{week_attended} this week" if week_attended else "No classes this week"
    change_class = "positive" if week_attended else ""

    # pct_class is baked into the container key (not just a markup class) so
    # the CSS can color this specific card's left-border accent -- see
    # `[class*="st-key-subject-card-mid-"]` etc. in set_global_styles().
    with st.container(key=f"subject-card-{pct_class}-{sid}"):
        st.markdown(f"""
            <div class="subject-card-top">
                <div>
                    <div class="subject-card-name">{sub['name']}</div>
                    <div class="subject-card-code">{sub['subject_code']} &middot; Section {sub['section']}</div>
                </div>
                <div class="badge {pct_class}">{pct}%</div>
            </div>
            <div class="subject-card-metrics">
                <div>
                    <div class="subject-card-count">{attended}</div>
                    <div class="subject-card-count-label">classes attended</div>
                </div>
            </div>
            <div class="subject-card-track"><div class="subject-card-fill {pct_class}" style="width:{pct}%;"></div></div>
            <div class="subject-card-change {change_class}">{change_text}</div>
        """, unsafe_allow_html=True)
        if st.button("Unenroll", key=f"unenroll_{sid}", type='secondary'):
            unenroll_student_to_subject(student_id, sid)
            st.toast(f"Unenrolled from {sub['name']} successfully!")
            st.rerun()


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # QR/link enrollment: dialog_enroll.py pops 'enroll_code' on its first
    # render, so this only auto-opens once per pending code.
    if st.session_state.get('enroll_code'):
        enroll_dialog()

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary', key='logout_btn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    with st.spinner('Loading your dashboard..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats = _compute_dashboard_stats(logs)

    _render_hero_card(stats)
    _render_stat_cards(stats)
    _render_insight_cards(stats)

    header_col, button_col = st.columns([3, 1], vertical_alignment='center')
    with header_col:
        st.markdown('<div class="section-header"><span class="section-dot"></span>Your Enrolled Subjects</div>', unsafe_allow_html=True)
    with button_col:
        with st.container(key="enroll-btn-wrap"):
            if st.button('Enroll in Subject', type='primary'):
                enroll_dialog()
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if not subjects:
        st.info("You haven't enrolled in any subjects yet.")
    else:
        grid_cols = st.columns(2, gap='small')
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']
            subj_stats = stats['subject_stats'].get(sid, {'total': 0, 'attended': 0, 'week_attended': 0})
            with grid_cols[i % 2]:
                _render_subject_card(sub, subj_stats, student_id)

    footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()
    set_global_styles()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='back_btn'):
            st.session_state['login_type'] = 'home' # Change None to 'home'
            st.rerun()

    show_registration = False
    with st.container(key="login-panel"):
        st.markdown("""
            <div class="login-header">
                <div class="login-icon">🪪</div>
                <h1 class="login-title">Student Login</h1>
            </div>
            <p class="subtitle-muted">We'll recognize you instantly, or help you register in seconds.</p>
            <div class="step-strip">
                <div class="step-chip"><span class="step-num">1</span> Look at the camera</div>
                <span class="step-arrow">&rarr;</span>
                <div class="step-chip"><span class="step-num">2</span> We recognize you, or help you register</div>
            </div>
        """, unsafe_allow_html=True)

        photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner('AI is scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces > 1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True

    if show_registration:
        with st.container(key="registration-card"):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')
            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your voice for voice-only attendance")

            try:
                audio_data = st.audio_input('Record a short phrase (e.g., "I am present")')
            except Exception:
                st.error('Audio Input failed!')
                audio_data = None

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = get_voice_embedding(audio_data.read()) if audio_data else None
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Could not capture facial features.')
                else:
                    st.warning('Please enter your name!')

    footer_dashboard()
