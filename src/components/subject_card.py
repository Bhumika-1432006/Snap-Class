import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    st.markdown("""
        <style>
        .subject-card {
            background: #FFFFFF;
            border: 1px solid rgba(24, 164, 169, 0.15);
            border-left: 6px solid var(--color-primary, #18A4A9);
            border-radius: 20px;
            padding: 24px 26px;
            margin-bottom: 22px;
            box-shadow: 0 10px 24px rgba(24, 164, 169, 0.10);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeInUpCard 0.6s ease both;
        }
        .subject-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 16px 32px rgba(24, 164, 169, 0.18);
        }
        .subject-card h3 {
            margin: 0 0 8px 0 !important;
            color: var(--color-text, #1E2430) !important;
            font-family: var(--font-heading, 'Poppins', sans-serif) !important;
            font-size: 1.4rem !important;
        }
        .subject-card .meta {
            color: var(--color-text-muted, #52606D) !important;
            font-family: var(--font-body, 'Inter', sans-serif) !important;
            margin: 0 0 14px 0 !important;
            font-size: 0.95rem !important;
        }
        .subject-card .code-badge {
            background: rgba(24, 164, 169, 0.12);
            color: var(--color-primary-dark, #0E7A7E);
            padding: 3px 10px;
            border-radius: 8px;
            font-weight: 600;
        }
        .subject-card .stats-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        .subject-card .stat-pill {
            background: rgba(24, 164, 169, 0.08);
            padding: 6px 14px;
            border-radius: 14px;
            font-size: 0.9rem;
            font-family: var(--font-body, 'Inter', sans-serif);
            color: var(--color-text, #1E2430);
        }
        .subject-card .attendance-badge {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .subject-card .attendance-pct {
            font-family: var(--font-heading, 'Poppins', sans-serif);
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--color-primary-dark, #0E7A7E);
        }
        .subject-card .progress-track {
            width: 70px;
            height: 6px;
            border-radius: 4px;
            background: rgba(24, 164, 169, 0.15);
            overflow: hidden;
        }
        .subject-card .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--color-primary, #18A4A9), var(--color-primary-dark, #0E7A7E));
            border-radius: 4px;
        }
        @keyframes fadeInUpCard {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    total = 0
    attended = 0
    if stats:
        for icon, label, value in stats:
            if label.lower() == 'total':
                total = value
            elif label.lower() == 'attended':
                attended = value
    pct = int(round((attended / total) * 100)) if total else 0

    html = f"""
        <div class="subject-card">
            <h3>{name}</h3>
            <p class="meta">Code: <span class="code-badge">{code}</span> &nbsp;|&nbsp; Section: {section}</p>
    """

    if stats:
        html += '<div class="stats-row">'
        for icon, label, value in stats:
            html += f'<div class="stat-pill">{icon} <b>{value}</b> {label}</div>'
        html += f"""
            <div class="attendance-badge">
                <div class="progress-track"><div class="progress-fill" style="width:{pct}%;"></div></div>
                <span class="attendance-pct">{pct}%</span>
            </div>
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
