import streamlit as st

def aplicar_tema():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,500&family=Inter:wght@400;600;700;800;900&display=swap');

    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }

    .ae-card {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(212,175,55,0.18);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 18px 45px rgba(72,44,21,0.08);
    }

    .ae-hero {
        background: linear-gradient(135deg, #26113f 0%, #4b256f 52%, #b77945 100%);
        border-radius: 32px;
        padding: 56px 46px;
        color: white;
        margin-bottom: 28px;
    }

    .ae-title {
        font-size: 48px;
        line-height: 1.05;
        font-weight: 800;
        margin-bottom: 18px;
        font-family: "Cormorant Garamond", Georgia, serif;
        letter-spacing: -0.04em;
    }

    .ae-subtitle {
        font-size: 20px;
        line-height: 1.55;
        opacity: 0.92;
        max-width: 720px;
        font-family: 'Inter', sans-serif;
    }

    .ae-login-card {
        max-width: 430px;
        margin: 0 auto;
        background: rgba(255,255,255,0.95);
        border: 1px solid rgba(212,175,55,0.18);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 60px rgba(38,17,63,0.18);
    }

    .chat-box {
        height: 520px;
        overflow-y: auto;
        background: #f7f1ea;
        border-radius: 24px;
        padding: 18px;
        border: 1px solid rgba(212,175,55,0.14);
    }

    .msg-user {
        background: linear-gradient(135deg, #4b256f, #26113f);
        color: white;
        padding: 12px 14px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 82%;
    }

    .msg-bot {
        background: white;
        color: #2b2233;
        padding: 12px 14px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 82%;
        border: 1px solid rgba(212,175,55,0.12);
    }

    .ae-section-title {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 2.15rem;
        line-height: 1.1;
        letter-spacing: -0.03em;
        color: #21104a;
        margin-bottom: 0.45rem;
    }

    .ae-premium-btn {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: 0 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }

    .ae-premium-btn:hover {
        box-shadow: 0 6px 20px rgba(212,175,55,0.35) !important;
        transform: translateY(-1px);
    }

    .ae-outline-btn {
        background: transparent !important;
        color: #4b256f !important;
        border: 1.5px solid rgba(212,175,55,0.38) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }

    .ae-outline-btn:hover {
        background: rgba(212,175,55,0.08) !important;
        border-color: #d4af37 !important;
    }

    @media (max-width: 768px) {
        .ae-title { font-size: 34px; }
        .ae-hero { padding: 34px 24px; }
        .ae-section-title { font-size: 1.65rem; }
    }
    </style>
    """, unsafe_allow_html=True)