import streamlit as st

import qrcode
import io
import base64
import json
import html
from urllib.parse import quote


@st.dialog(" ")
def share_subject_dialog(subject_name, subject_code):
    base_url = "https://snap-class--main.streamlit.app"
    enrollment_url = f"{base_url}/?enroll={subject_code}"

    qr_img = qrcode.make(enrollment_url)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    whatsapp_text = quote(f"Join {subject_name} on SnapClass: {enrollment_url}")
    whatsapp_url = f"https://wa.me/?text={whatsapp_text}"

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&family=Inter:wght@400;500;600&display=swap');

            div[data-testid="stDialog"] > div:first-child > div:first-child {
                border-top: 4px solid #18A4A9 !important;
            }
            .share-title {
                font-family: 'Poppins', sans-serif;
                font-weight: 700;
                font-size: 1.3rem;
                color: #2B2D6E;
                margin-bottom: 14px;
            }
            .share-col-heading {
                font-family: 'Poppins', sans-serif;
                font-weight: 700;
                font-size: 1rem;
                color: #2B2D6E;
                margin-bottom: 10px;
            }
            .share-url-box {
                background: #E4F4F4;
                border: 1px solid rgba(24, 164, 169, 0.35);
                border-radius: 8px;
                padding: 12px 14px;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
                font-size: 0.82rem;
                color: #1E2430;
                word-break: break-all;
                margin-bottom: 14px;
                width: 100%;
                box-sizing: border-box;
                cursor: pointer;
            }
            .copy-link-btn, .whatsapp-btn {
                display: block;
                width: 100%;
                box-sizing: border-box;
                text-align: center;
                font-family: 'Poppins', sans-serif;
                font-weight: 700;
                font-size: 0.92rem;
                border-radius: 50px;
                padding: 12px 20px;
                margin-bottom: 10px;
                text-decoration: none !important;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .copy-link-btn {
                background: linear-gradient(135deg, #18A4A9 0%, #0E7A7E 100%);
                color: #ffffff !important;
                border: none;
                box-shadow: 0 8px 20px rgba(24, 164, 169, 0.3);
            }
            .copy-link-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(24, 164, 169, 0.4); }
            .whatsapp-btn {
                background: #ffffff;
                color: #2B2D6E !important;
                border: 2px solid #2B2D6E;
                box-shadow: none;
            }
            .whatsapp-btn:hover { background: rgba(43, 45, 110, 0.06); transform: translateY(-2px); }
            .qr-wrap {
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(24, 164, 169, 0.12);
                padding: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .qr-wrap img { width: 100%; max-width: 220px; border-radius: 6px; display: block; }
            .qr-caption {
                text-align: center;
                font-family: 'Inter', sans-serif;
                font-size: 0.8rem;
                color: #52606D;
                margin-top: 10px;
            }
        </style>
        <div class="share-title">Share Class Link</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="share-col-heading">Copy Link</div>', unsafe_allow_html=True)
        st.markdown(
            f'<input class="share-url-box" type="text" readonly value="{html.escape(enrollment_url)}" onclick="this.select();" />',
            unsafe_allow_html=True,
        )

        copy_btn_html = f"""
            <button class="copy-link-btn" onclick='
                var text = {json.dumps(enrollment_url)};
                var btn = this;
                function showOk() {{ btn.innerText = "Copied!"; setTimeout(function(){{ btn.innerText = "Copy to Clipboard"; }}, 1500); }}
                function showFail() {{ btn.innerText = "Failed \\u2014 tap the link box above to select it"; setTimeout(function(){{ btn.innerText = "Copy to Clipboard"; }}, 2500); }}
                if (navigator.clipboard && window.isSecureContext) {{
                    navigator.clipboard.writeText(text).then(showOk, function(err) {{ console.error("clipboard.writeText failed:", err); showFail(); }});
                }} else {{
                    try {{
                        var ta = document.createElement("textarea");
                        ta.value = text;
                        ta.style.position = "fixed";
                        ta.style.opacity = "0";
                        document.body.appendChild(ta);
                        ta.focus();
                        ta.select();
                        var copied = document.execCommand("copy");
                        document.body.removeChild(ta);
                        if (copied) {{ showOk(); }} else {{ console.error("execCommand copy returned false"); showFail(); }}
                    }} catch (e) {{
                        console.error("copy fallback threw:", e);
                        showFail();
                    }}
                }}
            '>Copy to Clipboard</button>
        """
        st.markdown(copy_btn_html, unsafe_allow_html=True)

        st.markdown(
            f'<a class="whatsapp-btn" href="{whatsapp_url}" target="_blank" rel="noopener noreferrer">📲 WhatsApp</a>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown('<div class="share-col-heading">Scan to Join</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="qr-wrap"><img src="data:image/png;base64,{qr_b64}" /></div>
            <div class="qr-caption">Scan to enroll instantly</div>
        """, unsafe_allow_html=True)
