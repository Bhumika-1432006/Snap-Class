import streamlit as st
import plotly.graph_objects as go
import dateutil.parser
import random
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students, create_student, get_student_subjects, get_student_attendance,
    unenroll_student_to_subject, update_student_avatar, get_students_in_subject,
    update_subject_note, create_dispute, get_disputes_for_student,
)
import time
from datetime import date, datetime, timedelta
from src.components.dialog_enroll import enroll_dialog

# Minimal monoline SVG icons for the stat cards -- stroke="currentColor" so
# each one picks up its color from the wrapping .icon-* span, no emoji.
_ICON_CALENDAR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
_ICON_CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="8 12 11 15 16 9"/></svg>'
_ICON_FLAME = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1 4-4 5-4 9a4 4 0 0 0 8 0c0-2-1-3-1-3s2 1 2 4a6 6 0 1 1-12 0c0-5 4-6 4-10z"/></svg>'

# --- FEATURE 4: avatar options -----------------------------------------
# `students.avatar` holds either a plain emoji (legacy/default) or one of
# these MP4 URLs. See _render_avatar() for how the two cases are told apart.
AVATAR_OPTIONS = [
    {"label": "Ghost", "url": "https://assets-v2.lottiefiles.com/a/4d43c0bc-1173-11ee-9cac-db1ea0a1c111/WXSK8aus2c.mp4"},
    {"label": "Bear", "url": "https://assets-v2.lottiefiles.com/a/7016fcb6-30c1-11f0-bcf8-57c4a2ec7739/dysehJREyh.mp4"},
    {"label": "Spinning Emoji", "url": "https://assets-v2.lottiefiles.com/a/b7caade6-1183-11ee-a621-3fa043c173ec/6sEBtMBdfv.mp4"},
    {"label": "Alien", "url": "https://assets-v2.lottiefiles.com/a/c87ed4c4-117d-11ee-a3e0-2b9a0269eb4d/Ssoh2HbFGO.mp4"},
    {"label": "Cool Fox", "url": "https://assets-v2.lottiefiles.com/a/d69c9ddc-1175-11ee-86e6-cf84c5dc742a/E6jG1eTIKz.mp4"},
    {"label": "Angry", "url": "https://assets-v2.lottiefiles.com/a/ad84cbc4-117d-11ee-b854-33f3503846bb/Q61WkCvobW.mp4"},
    {"label": "Bored Horse", "url": "https://assets-v2.lottiefiles.com/a/91d6c73b-0772-41f9-b0c5-e78f68dec48a/l86Srwxuy1.mp4"},
    {"label": "Crying", "url": "https://assets-v2.lottiefiles.com/a/f1f891fc-21e2-11ef-b4c0-9f416a581abe/JYAaIAVHD3.mp4"},
    {"label": "Skull", "url": "https://assets-v2.lottiefiles.com/a/7b658406-117a-11ee-9e8c-5b388298f159/CYfQ8Fy8Se.mp4"},
]
DEFAULT_AVATAR = "🙂"


def _render_avatar(avatar_value, size_px=48):
    if avatar_value and str(avatar_value).startswith("http"):
        return (
            f'<video src="{avatar_value}" autoplay loop muted playsinline '
            f'style="width:{size_px}px;height:{size_px}px;border-radius:50%;object-fit:cover;"></video>'
        )
    emoji = avatar_value or DEFAULT_AVATAR
    return f'<span style="font-size:{size_px * 0.7}px;line-height:1;">{emoji}</span>'


# --- FEATURE 1: slang streak tiers --------------------------------------
def _get_streak_tier(streak_days):
    if streak_days <= 0:
        return "🌱 Just Vibing"
    if streak_days < 5:
        return "🔥 Warming Up"
    if streak_days < 10:
        return "🔒 Locked In"
    if streak_days < 30:
        return "💀 No Chill"
    return "👑 Certified Menace"


# --- FEATURE 3: template roast bank --------------------------------------
_ROAST_TEMPLATES = [
    "{overall_pct}% attendance? Bold of you to assume {worst_subject} needed you.",
    "Your {streak}-day streak says main character. Your {worst_subject} attendance says extra.",
    "{best_subject} carried this whole GPA and you know it.",
    "You've shown up to {overall_pct}% of your life. Respectfully, that's a coin flip.",
    "{worst_subject} attendance so low it's basically a long-distance relationship at this point.",
    "Streak: {streak} days. Confidence: unmatched. Correlation: unclear.",
    "You're not 'busy', {worst_subject} just isn't the main quest right now.",
    "{overall_pct}% overall attendance -- statistically you're a background character in your own semester.",
    "{best_subject} really said 'I'll show up for you' and meant it.",
    "A {streak}-day streak is cute until {worst_subject} remembers you exist.",
    "You attend {best_subject} like it owes you money and {worst_subject} like it owes you nothing.",
    "{overall_pct}% attendance is giving 'I read the syllabus once for vibes'.",
    "Certified {streak}-day locked-in behavior, allegedly, according to everywhere except {worst_subject}.",
    "Some people have a favorite subject. You have {worst_subject}, which you actively avoid.",
    "At {overall_pct}% attendance you're basically a rumor in {worst_subject}.",
    "The {streak}-day streak is real. So is your absence record in {worst_subject}. Both can be true.",
    "You show up for {best_subject} like it's a situationship you're actually into.",
    "{overall_pct}% attendance: technically enrolled, spiritually elsewhere.",
    "{worst_subject} attendance lower than your screen time during {worst_subject}. Couldn't be a coincidence.",
    "Keep the {streak}-day streak going and maybe {worst_subject} will forgive you eventually.",
]


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
            /* The rule above forces font-family on every span/div app-wide,
               which clobbers Streamlit's Material Symbols icon font -- icon
               glyphs (popover chevrons, expander arrows) are rendered as
               text spans using ligature names like "expand_more" in that
               special font, so overriding it makes the browser show the
               literal ligature text instead of the icon. data-testid is the
               real, stable selector Streamlit emits for these spans
               (confirmed in its DynamicIcon component source -- the
               generated CSS classes are hashed per build and unusable as a
               selector). Must come after the rule it's correcting. */
            [data-testid="stIconMaterial"] {
                font-family: 'Material Symbols Rounded' !important;
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

            /* 4. Input and Selectbox, on-brand.
               Box styling lives on the wrapper div[data-baseweb="base-input"]
               (BaseWeb's real input container, confirmed via its source),
               not the bare <input> -- matches the fix applied in
               teacher_screen.py, where styling the inner <input> directly
               was found to overlap BaseWeb's endEnhancer icon slot (e.g. a
               password show/hide toggle). No password field exists on this
               screen today, but this keeps both screens' input theming
               consistent and avoids the same bug if one's ever added here. */
            div[data-baseweb="base-input"],
            div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                border: 1px solid rgba(24, 164, 169, 0.3) !important;
                border-radius: 10px !important;
            }
            .stTextInput input {
                background-color: transparent !important;
                border: none !important;
                color: var(--color-text) !important;
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
            @media (max-width: 768px) {
                .stat-grid { grid-template-columns: repeat(2, 1fr); }
            }
            @media (max-width: 480px) {
                .stat-grid { grid-template-columns: 1fr; }
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
            /* Tier name ("🔒 Locked In") is wider than the numeric values the
               rest of the stat cards show, so it gets its own smaller size. */
            .stat-card.streak .stat-value { font-size: 1.05rem; white-space: nowrap; }
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
            @media (max-width: 768px) {
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

            /* Private per-subject notes: pin indicator in the card header +
               the popover trigger/body, styled to match the card language
               instead of reading as a bolted-on widget. */
            .subject-card-pin {
                font-size: 0.85rem;
                margin-left: 6px;
                vertical-align: middle;
            }
            [class*="st-key-subject-card-"] [data-testid="stPopover"] {
                margin-top: 10px;
            }
            [class*="st-key-subject-card-"] [data-testid="stPopover"] button {
                background: rgba(24, 164, 169, 0.06) !important;
                color: var(--color-primary-dark) !important;
                border: 1px solid rgba(24, 164, 169, 0.2) !important;
                border-radius: 20px !important;
                box-shadow: none !important;
                font-family: var(--font-body) !important;
                font-weight: 600 !important;
                font-size: 0.78rem !important;
                padding: 5px 14px !important;
            }
            [class*="st-key-subject-card-"] [data-testid="stPopover"] button:hover {
                background: rgba(24, 164, 169, 0.12) !important;
                transform: none !important;
            }
            .subject-note-label {
                font-family: var(--font-body);
                font-size: 0.78rem;
                color: var(--color-text-muted);
                margin-bottom: 6px;
            }

            /* Attendance dispute history ("My Reported Issues") */
            .dispute-card {
                background: #FFFFFF;
                border-radius: 12px;
                border-left: 4px solid var(--color-accent);
                padding: 14px 18px;
                margin-bottom: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
            .dispute-card.resolved { border-left-color: #1F9D55; }
            .dispute-top {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
            }
            .dispute-subject {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.95rem;
                color: var(--color-text);
            }
            .dispute-date {
                font-family: var(--font-body);
                font-size: 0.74rem;
                color: var(--color-text-muted);
                margin-top: 1px;
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
            .dispute-message {
                font-family: var(--font-body);
                font-size: 0.85rem;
                color: var(--color-text);
                margin-top: 8px;
                line-height: 1.4;
            }
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

            /* FEATURE 1: red-flag tag on subject cards under 60% */
            .red-flag-tag {
                display: inline-block;
                margin-top: 8px;
                font-family: var(--font-body);
                font-weight: 700;
                font-size: 0.72rem;
                color: #C4453A;
                background: rgba(196, 69, 58, 0.10);
                padding: 3px 10px;
                border-radius: 20px;
            }

            /* FEATURE 2: ghosted-language copy + badge */
            .ghost-tag {
                display: block;
                margin-top: 6px;
                font-family: var(--font-body);
                font-size: 0.72rem;
                font-style: italic;
                color: var(--color-text-muted);
            }
            .ghoster-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.75rem;
                color: #52606D;
                background: rgba(82, 96, 109, 0.10);
                padding: 5px 14px;
                border-radius: 20px;
                margin: 4px 0 16px 0;
            }

            /* FEATURE 3: roast-of-the-day card, matches .stat-card language */
            .st-key-roast-card {
                background: #FFFFFF !important;
                border-radius: 14px !important;
                border-top: 3px solid var(--color-accent) !important;
                padding: 18px 20px !important;
                box-shadow: 0 6px 16px rgba(245, 166, 35, 0.10) !important;
                margin: 0 0 16px 0 !important;
                animation: fadeInUp 0.6s ease both;
            }
            .roast-label {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                color: #B8791A;
                margin-bottom: 8px;
            }
            .roast-text {
                font-family: var(--font-body);
                font-size: 1rem;
                font-weight: 500;
                color: var(--color-text);
                line-height: 1.5;
            }
            .st-key-roast-card div.stButton { justify-content: flex-start !important; margin-top: 12px !important; }
            .st-key-roast-card div.stButton > button {
                padding: 6px 18px !important;
                font-size: 0.82rem !important;
            }

            /* FEATURE 4: avatars + picker grid */
            .avatar-wrap {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                overflow: hidden;
                background: rgba(24, 164, 169, 0.08);
                flex-shrink: 0;
            }
            [class*="st-key-avatar-option-"] div.stButton { margin: 0 !important; }
            [class*="st-key-avatar-option-"] div.stButton > button {
                width: 100% !important;
                padding: 6px !important;
                font-size: 0.68rem !important;
                background: rgba(24, 164, 169, 0.05) !important;
                color: var(--color-text-muted) !important;
                border: 1px solid rgba(24, 164, 169, 0.2) !important;
                box-shadow: none !important;
            }
            .avatar-option-thumb { display: flex; justify-content: center; margin-bottom: 4px; }

            /* FEATURE 5: beef mode */
            .st-key-beef-card {
                background: #FFFFFF !important;
                border-radius: 16px !important;
                padding: 20px 22px !important;
                box-shadow: 0 8px 20px rgba(24, 164, 169, 0.10) !important;
                margin: 8px 0 16px 0 !important;
                animation: fadeInUp 0.6s ease both;
            }
            .beef-grid {
                display: grid;
                grid-template-columns: 1fr auto 1fr;
                gap: 16px;
                align-items: center;
                margin-top: 12px;
            }
            .beef-side { text-align: center; }
            .beef-avatar { display: flex; justify-content: center; margin-bottom: 8px; }
            .beef-name {
                font-family: var(--font-heading);
                font-weight: 700;
                font-size: 1rem;
                color: var(--color-text);
            }
            .beef-crown { font-size: 1.1rem; margin-left: 4px; }
            .beef-stat {
                font-family: var(--font-heading);
                font-weight: 800;
                font-size: 1.3rem;
                color: var(--color-primary-dark);
                margin-top: 6px;
            }
            .beef-stat-label {
                font-family: var(--font-body);
                font-size: 0.68rem;
                color: var(--color-text-muted);
            }
            .beef-vs {
                font-family: var(--font-heading);
                font-weight: 900;
                font-size: 1.1rem;
                color: var(--color-accent);
                text-align: center;
            }
            /* This 3-column grid (profile | VS | profile) had no mobile
               override at all -- on a narrow phone it would squeeze two
               full stat blocks and a divider into one cramped row. Stack
               instead, with VS becoming a horizontal divider between them. */
            @media (max-width: 640px) {
                .beef-grid { grid-template-columns: 1fr; }
                .beef-vs { padding: 4px 0; }
            }
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

        stat = subject_stats.setdefault(sid, {'total': 0, 'attended': 0, 'name': sname, 'week_attended': 0, 'month_absences': 0})
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
            else:
                # FEATURE 2: "ghosted" count -- absences this month, per subject.
                stat['month_absences'] += 1

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

    # FEATURE 2: "certified ghoster" badge -- overall attendance under 50%.
    # Self-facing only, same as the per-subject ghost tags.
    ghoster_html = (
        '<div class="ghoster-badge">👻 Certified Ghoster</div>'
        if stats['overall_pct'] is not None and stats['overall_pct'] < 50 else ''
    )

    with st.container(key="hero-card"):
        label_col, chart_col = st.columns([1, 2], vertical_alignment='center', gap='large')
        with label_col:
            st.markdown(f"""
                <div class="hero-label">Attendance Trend</div>
                <div class="hero-value">{overall_value}</div>
                <div class="hero-sub">{sub_caption}</div>
                {ghoster_html}
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

    # FEATURE 1: slang-named streak tiers instead of a raw number, with the
    # actual day count kept alongside it (in the caption line).
    streak_tier = _get_streak_tier(stats['streak'])
    streak_caption = f"{stats['streak']} days" if stats['streak'] else "Start today"

    # Built as a single unbroken line: a blank/whitespace-only line here would
    # split this into two Markdown blocks and the second half would render as
    # a raw code block instead of HTML (indented-code-block vs HTML-block rule).
    cards = (
        f'<div class="stat-card week"><div class="stat-top"><span class="stat-icon icon-teal">{_ICON_CALENDAR}</span><span class="stat-label">This Week</span></div><div class="stat-value">{week_value}</div><div class="stat-caption">{week_caption}</div></div>'
        f'<div class="stat-card month"><div class="stat-top"><span class="stat-icon icon-teal">{_ICON_CALENDAR}</span><span class="stat-label">This Month</span></div><div class="stat-value">{month_value}</div><div class="stat-caption">{month_caption}</div></div>'
        f'<div class="stat-card total"><div class="stat-top"><span class="stat-icon icon-indigo">{_ICON_CHECK}</span><span class="stat-label">Total Attended</span></div><div class="stat-value">{stats["total_attended"]}</div><div class="stat-caption">All time</div></div>'
        f'<div class="stat-card streak"><div class="stat-top"><span class="stat-icon icon-amber">{_ICON_FLAME}</span><span class="stat-label">Day Streak</span></div><div class="stat-value">{streak_tier}</div><div class="stat-caption">{streak_caption}</div></div>'
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


def _pick_roast(stats):
    template = random.choice(_ROAST_TEMPLATES)
    return template.format(
        overall_pct=stats['overall_pct'] if stats['overall_pct'] is not None else 0,
        streak=stats['streak'],
        best_subject=stats['best']['name'] if stats['best'] else 'that one class',
        worst_subject=stats['worst']['name'] if stats['worst'] else 'that one class',
    )


@st.fragment
def _render_roast_section(stats):
    if 'roast_pick' not in st.session_state:
        st.session_state.roast_pick = _pick_roast(stats)

    with st.container(key="roast-card"):
        st.markdown(f"""
            <div class="roast-label">🎤 Your Semester, Roasted</div>
            <div class="roast-text">{st.session_state.roast_pick}</div>
        """, unsafe_allow_html=True)
        # @st.fragment scopes this button's rerun to just this section --
        # not the whole dashboard -- so rerolling doesn't refetch subjects/
        # attendance from the DB. scope="fragment" makes the new pick show
        # up on this same click instead of one click behind.
        if st.button("🎲 Reroll", key="reroll_roast", type='tertiary'):
            st.session_state.roast_pick = _pick_roast(stats)
            st.rerun(scope="fragment")


def _render_subject_card(sub, subj_stats, student_id, note=''):
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
    month_absences = subj_stats.get('month_absences', 0)

    # FEATURE 1: red-flag tag for subjects under 60% attendance.
    red_flag_html = '<div class="red-flag-tag">🚩 Red Flag Behavior</div>' if total and pct < 60 else ''

    # FEATURE 2: "ghosted" copy for 3+ absences this month in this subject.
    # Self-facing only -- this whole screen only ever renders for the logged
    # in student themselves, never surfaced to teachers or classmates.
    ghost_html = (
        f'<div class="ghost-tag">You\'ve ghosted {sub["name"]} {month_absences} times this month 👻</div>'
        if month_absences >= 3 else ''
    )

    # Small pin indicator in the header if a note already exists, so it's
    # visible without opening the popover below.
    pin_html = '<span class="subject-card-pin">📌</span>' if note else ''

    # pct_class is baked into the container key (not just a markup class) so
    # the CSS can color this specific card's left-border accent -- see
    # `[class*="st-key-subject-card-mid-"]` etc. in set_global_styles().
    with st.container(key=f"subject-card-{pct_class}-{sid}"):
        st.markdown(f"""
            <div class="subject-card-top">
                <div>
                    <div class="subject-card-name">{sub['name']}{pin_html}</div>
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
            {red_flag_html}
            {ghost_html}
        """, unsafe_allow_html=True)

        note_popover_label = "📝 Notes for next class" + (" 📌" if note else "")
        with st.popover(note_popover_label, width='stretch'):
            st.markdown('<div class="subject-note-label">Private -- only you can see this.</div>', unsafe_allow_html=True)
            note_value = st.text_area(
                "Note", value=note, key=f"note_text_{sid}",
                placeholder="e.g. Bring lab report, sit near the front...",
                label_visibility="collapsed",
            )
            if st.button("Save", key=f"save_note_{sid}", type='primary'):
                update_subject_note(student_id, sid, note_value)
                st.toast("Note saved!")
                st.rerun()

        with st.popover("⚠️ Report an issue", width='stretch'):
            st.markdown('<div class="subject-note-label">Flag a class date where your attendance looks wrong.</div>', unsafe_allow_html=True)
            dispute_date = st.date_input("Class date", value=date.today(), max_value=date.today(), key=f"dispute_date_{sid}")
            dispute_message = st.text_area(
                "Message", key=f"dispute_msg_{sid}",
                placeholder="e.g. My attendance wasn't marked for this date but I was present",
                label_visibility="collapsed",
            )
            if st.button("Submit", key=f"dispute_submit_{sid}", type='primary'):
                if dispute_message.strip():
                    create_dispute(student_id, sid, dispute_date, dispute_message.strip())
                    st.toast("Issue reported -- your teacher will follow up.")
                    st.rerun()
                else:
                    st.warning("Please describe the issue before submitting.")

        if st.button("Unenroll", key=f"unenroll_{sid}", type='secondary'):
            unenroll_student_to_subject(student_id, sid)
            st.toast(f"Unenrolled from {sub['name']} successfully!")
            st.rerun()


def _render_avatar_picker(student_id):
    cols = st.columns(3)
    for i, opt in enumerate(AVATAR_OPTIONS):
        with cols[i % 3]:
            with st.container(key=f"avatar-option-{i}"):
                thumb_html = _render_avatar(opt['url'], size_px=60)
                st.markdown(f'<div class="avatar-option-thumb">{thumb_html}</div>', unsafe_allow_html=True)
                if st.button(opt['label'], key=f"avatar_pick_{i}"):
                    update_student_avatar(student_id, opt['url'])
                    st.session_state.student_data['avatar'] = opt['url']
                    st.toast(f"Avatar updated to {opt['label']}!")
                    st.rerun()

    st.divider()
    if st.button("🙂 Reset to default", key="avatar_reset", width='stretch'):
        update_student_avatar(student_id, DEFAULT_AVATAR)
        st.session_state.student_data['avatar'] = DEFAULT_AVATAR
        st.toast("Avatar reset!")
        st.rerun()


def _render_beef_mode(student_data, stats, subjects):
    if not subjects:
        return

    with st.container(key="beef-card"):
        st.markdown('<div class="section-header"><span class="section-dot"></span>Start Beef 🥊</div>', unsafe_allow_html=True)

        subject_options = {f"{n['subjects']['name']} - {n['subjects']['subject_code']}": n['subjects']['subject_id'] for n in subjects}
        picked_label = st.selectbox("Pick a class to start beef in", options=list(subject_options.keys()), key="beef_subject_select")
        picked_subject_id = subject_options[picked_label]

        roster = get_students_in_subject(picked_subject_id)
        opponents = {
            node['students']['name']: node['students']
            for node in roster
            if node.get('students') and node['students']['student_id'] != student_data['student_id']
        }

        if not opponents:
            st.info("No one else is enrolled in this class yet -- no beef to start.")
            return

        opponent_name = st.selectbox("Pick your opponent", options=list(opponents.keys()), key="beef_opponent_select")

        if st.button("🥊 Start Beef", key="beef_start_btn"):
            st.session_state.beef_opponent = opponents[opponent_name]

        opponent = st.session_state.get('beef_opponent')
        if opponent and opponent['name'] in opponents:
            opponent_logs = get_student_attendance(opponent['student_id'])
            opponent_stats = _compute_dashboard_stats(opponent_logs)

            my_streak = stats['streak']
            their_streak = opponent_stats['streak']
            my_crown = '👑' if my_streak > their_streak else ''
            their_crown = '👑' if their_streak > my_streak else ''

            my_avatar = _render_avatar(student_data.get('avatar'), size_px=56)
            their_avatar = _render_avatar(opponent.get('avatar'), size_px=56)

            st.markdown(f"""
                <div class="beef-grid">
                    <div class="beef-side">
                        <div class="beef-avatar">{my_avatar}</div>
                        <div class="beef-name">{student_data['name']} {my_crown}</div>
                        <div class="beef-stat">{my_streak}</div>
                        <div class="beef-stat-label">day streak</div>
                        <div class="beef-stat">{_fmt_pct(stats['overall_pct'])}</div>
                        <div class="beef-stat-label">overall attendance</div>
                    </div>
                    <div class="beef-vs">VS</div>
                    <div class="beef-side">
                        <div class="beef-avatar">{their_avatar}</div>
                        <div class="beef-name">{opponent['name']} {their_crown}</div>
                        <div class="beef-stat">{their_streak}</div>
                        <div class="beef-stat-label">day streak</div>
                        <div class="beef-stat">{_fmt_pct(opponent_stats['overall_pct'])}</div>
                        <div class="beef-stat-label">overall attendance</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("End beef", key="beef_end_btn", type='tertiary'):
                del st.session_state.beef_opponent
                st.rerun()


def _render_dispute_history(student_id):
    disputes = get_disputes_for_student(student_id)
    if not disputes:
        return

    open_count = sum(1 for d in disputes if d.get('status') != 'resolved')
    label = f"🚩 My Reported Issues ({open_count} open)" if open_count else "🚩 My Reported Issues"

    with st.expander(label):
        for d in disputes:
            is_resolved = d.get('status') == 'resolved'
            status_class = 'resolved' if is_resolved else 'open'
            status_label = '✅ Resolved' if is_resolved else '🟡 Open'
            subject_name = (d.get('subjects') or {}).get('name', 'Unknown subject')
            class_date = d.get('class_date', '—')
            reply = d.get('teacher_reply') or ''

            # Shown whenever a reply exists, regardless of open/resolved status.
            reply_html = (
                f'<div class="dispute-reply"><div class="dispute-reply-label">💬 Teacher\'s reply:</div>{reply}</div>'
                if reply else ''
            )

            st.markdown(f"""
                <div class="dispute-card {status_class}">
                    <div class="dispute-top">
                        <div>
                            <div class="dispute-subject">{subject_name}</div>
                            <div class="dispute-date">Class date: {class_date}</div>
                        </div>
                        <div class="dispute-badge {status_class}">{status_label}</div>
                    </div>
                    <div class="dispute-message">{d.get('student_message', '')}</div>
                    {reply_html}
                </div>
            """, unsafe_allow_html=True)


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
        # FEATURE 4: avatar next to the student's name in the dashboard hero row.
        avatar_html = _render_avatar(student_data.get('avatar'), size_px=42)
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <span class="avatar-wrap" style="width:42px;height:42px;">{avatar_html}</span>
                <span style="font-family:var(--font-heading); font-weight:700; font-size:1.3rem; color:var(--color-text);">Welcome, {student_data['name']}</span>
            </div>
        """, unsafe_allow_html=True)

        avatar_col, logout_col = st.columns(2)
        with avatar_col:
            with st.popover("🎭 Change avatar", width='stretch'):
                _render_avatar_picker(student_id)
        with logout_col:
            if st.button("Logout", type='secondary', key='logout_btn', width='stretch'):
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
    _render_roast_section(stats)

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
            subj_stats = stats['subject_stats'].get(sid, {'total': 0, 'attended': 0, 'week_attended': 0, 'month_absences': 0})
            # 'notes' lives on the subject_students row (sub_node), not on
            # the joined subjects row (sub) -- see get_student_subjects().
            note = sub_node.get('notes') or ''
            with grid_cols[i % 2]:
                _render_subject_card(sub, subj_stats, student_id, note=note)

    # Attendance dispute history -- the student's own reported issues + any teacher replies.
    _render_dispute_history(student_id)

    # FEATURE 5: opt-in streak comparison against a classmate in the same subject.
    _render_beef_mode(student_data, stats, subjects)

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
        img = np.array(Image.open(photo_source).convert('RGB'))
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
            new_name = st.text_input("Enter your name", placeholder='Enter your name')
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
