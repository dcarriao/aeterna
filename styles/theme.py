import streamlit as st

def aplicar_tema():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }

    .ae-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.18);
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
    }

    .ae-subtitle {
        font-size: 20px;
        line-height: 1.55;
        opacity: 0.92;
        max-width: 720px;
    }

    .ae-login-card {
        max-width: 430px;
        margin: 0 auto;
        background: white;
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
        border: 1px solid #eadccc;
    }

    .msg-user {
        background: #4b256f;
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
        border: 1px solid #eee;
    }

    @media (max-width: 768px) {
        .ae-title { font-size: 34px; }
        .ae-hero { padding: 34px 24px; }
    }
    </style>
    """, unsafe_allow_html=True)