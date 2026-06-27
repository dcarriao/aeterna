import streamlit as st


def aplicar_css_mobile():
    st.markdown("""
<style>
@media (max-width: 768px) {
    :root {
        --ae-bg: #F9F7F3;
        --ae-card: #FFFFFF;
        --ae-text: #24125A;
        --ae-muted: #6E6478;
        --ae-gold: #D9A328;
        --ae-border: #E7DCC7;
    }

    html, body, .stApp {
        overflow-x: hidden !important;
        width: 100% !important;
        background: var(--ae-bg) !important;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 15% 0%, rgba(94,45,170,0.10), transparent 28%),
            radial-gradient(circle at 90% 5%, rgba(217,163,40,0.10), transparent 24%),
            linear-gradient(180deg, #F9F7F3 0%, #F4EFE7 100%) !important;
    }

    .block-container,
    [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        padding: 0.75rem 0.85rem 5.25rem !important;
        margin: 0 !important;
    }

    [data-testid="stHeader"] {
        display: block !important;
        visibility: visible !important;
        background: rgba(249,247,243,0.92) !important;
        backdrop-filter: blur(12px) !important;
        height: 3rem !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stHeaderActionElements"],
    [data-testid="stDeployButton"],
    #MainMenu,
    footer,
    .viewerBadge_container__1QSob {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    [data-testid="stSidebar"] {
        min-width: 82vw !important;
        max-width: 82vw !important;
        width: 82vw !important;
        background: linear-gradient(180deg, #160A4A 0%, #10052F 100%) !important;
        border-right: 1px solid rgba(217,163,40,0.28) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        width: 82vw !important;
        padding: 0.75rem !important;
    }

    [data-testid="stSidebar"] button {
        min-height: 2.75rem !important;
        border-radius: 14px !important;
        font-size: 0.95rem !important;
    }

    h1, h2, h3 {
        color: var(--ae-text) !important;
        letter-spacing: -0.025em !important;
    }

    h1 { font-size: 1.65rem !important; line-height: 1.12 !important; margin: 0.25rem 0 0.75rem !important; }
    h2 { font-size: 1.35rem !important; line-height: 1.18 !important; margin: 0.25rem 0 0.6rem !important; }
    h3 { font-size: 1.08rem !important; line-height: 1.22 !important; }

    p, li, label, small,
    .stMarkdown, .stMarkdown p,
    div[data-testid="stWidgetLabel"], div[data-testid="stWidgetLabel"] p {
        color: var(--ae-text) !important;
    }

    .stCaptionContainer, .stCaptionContainer p,
    .ae-small, .ae-muted {
        color: var(--ae-muted) !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 0.7rem !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.7rem !important;
    }

    .ae-dashboard-hero,
    .ae-home-hero,
    .ae-visitor-hero {
        border-radius: 22px !important;
        padding: 1.1rem !important;
        margin: 0.35rem 0 0.85rem !important;
        box-shadow: 0 14px 32px rgba(36,18,90,0.12) !important;
    }

    .ae-dashboard-hero h1,
    .ae-home-hero h1,
    .ae-visitor-hero h1 {
        color: #F2C572 !important;
        font-size: 1.45rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.45rem !important;
    }

    .ae-dashboard-hero p,
    .ae-home-hero p,
    .ae-visitor-hero p {
        color: rgba(255,255,255,0.88) !important;
        font-size: 0.9rem !important;
        line-height: 1.45 !important;
    }

    .ae-dashboard-grid,
    .ae-home-stats,
    .ae-live-news-list,
    .ae-live-people-grid,
    .ae-live-shared-grid,
    .ae-contrib-summary-grid,
    .ae-contrib-approved-grid,
    .ae-collection-mini-grid,
    .ae-card-grid-row {
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 0.75rem !important;
        min-height: auto !important;
    }

    .ae-dashboard-card,
    .ae-dashboard-next,
    .ae-home-panel,
    .ae-stat-card,
    .ae-live-story-card,
    .ae-live-person-card,
    .ae-live-shared-card,
    .ae-live-empty-card,
    .ae-live-news-item,
    .ae-story-card,
    .ae-collection-box,
    .ae-contrib-card,
    .ae-contrib-side-card,
    .ae-contrib-summary,
    .ae-contrib-approved-card,
    .ae-visitor-card {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        min-height: auto !important;
        height: auto !important;
        border-radius: 18px !important;
        padding: 0.9rem !important;
        margin: 0 0 0.7rem !important;
        background: rgba(255,255,255,0.96) !important;
        border: 1px solid rgba(231,220,199,0.95) !important;
        box-shadow: 0 10px 26px rgba(36,18,90,0.07) !important;
    }

    .ae-live-story-media,
    .ae-story-media,
    .ae-collection-mini-media {
        height: 130px !important;
        min-height: 130px !important;
        max-height: 130px !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    .ae-live-story-body,
    .ae-story-body {
        height: auto !important;
        min-height: auto !important;
        max-height: none !important;
        padding: 0.75rem 0 0 !important;
    }

    .ae-live-story-body h3,
    .ae-story-body h3 {
        font-size: 1rem !important;
        min-height: 0 !important;
        -webkit-line-clamp: 3 !important;
    }

    .ae-live-story-body p,
    .ae-story-body p {
        font-size: 0.86rem !important;
        line-height: 1.45 !important;
        -webkit-line-clamp: 4 !important;
        color: #3B3150 !important;
    }

    .ae-live-card-read-btn {
        width: 100% !important;
        min-height: 2.5rem !important;
        margin: 0.6rem 0 0 !important;
        border-radius: 12px !important;
        font-size: 0.9rem !important;
    }

    .ae-story-top,
    .ae-live-home-top,
    .ae-home-top,
    .ae-contrib-hero {
        display: block !important;
        min-height: auto !important;
        margin: 0.2rem 0 0.75rem !important;
    }

    .ae-story-top h2,
    .ae-live-home-top h1,
    .ae-home-top h1,
    .ae-contrib-hero h1 {
        font-size: 1.45rem !important;
        line-height: 1.12 !important;
        color: var(--ae-text) !important;
    }

    .ae-story-section-title,
    .ae-live-section-title,
    .ae-panel-title {
        font-size: 1.05rem !important;
        margin: 0.9rem 0 0.45rem !important;
        color: var(--ae-text) !important;
    }

    .st-key-home_contar_historia,
    [class*="st-key-minha_historia_contar_historia"] {
        justify-content: stretch !important;
    }

    .st-key-home_contar_historia button,
    [class*="st-key-minha_historia_contar_historia"] button,
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button,
    button[data-testid*="baseButton"] {
        width: 100% !important;
        min-height: 2.75rem !important;
        border-radius: 13px !important;
        font-size: 0.92rem !important;
        font-weight: 900 !important;
    }

    div[data-testid="stForm"],
    div[data-testid="stExpander"],
    details {
        border-radius: 18px !important;
        max-width: 100% !important;
    }

    input, textarea, select {
        font-size: 16px !important;
        color: #1b0f2e !important;
        background: #ffffff !important;
        border-radius: 12px !important;
    }

    textarea { min-height: 110px !important; }

    img, video {
        max-width: 100% !important;
        height: auto !important;
        border-radius: 14px !important;
    }

    .stTabs [role="tablist"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        gap: 0.25rem !important;
        padding-bottom: 0.35rem !important;
        scrollbar-width: none !important;
    }

    .stTabs [role="tablist"]::-webkit-scrollbar { display: none !important; }

    button[data-baseweb="tab"] {
        min-width: max-content !important;
        padding: 0.55rem 0.75rem !important;
        font-size: 0.86rem !important;
        border-radius: 999px !important;
    }

    .ae-curador-steps,
    .ae-curador-how-grid,
    .ae-curador-question-shell {
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 0.6rem !important;
    }

    .ae-curador-how-arrow { display: none !important; }

    .ae-curador-preview-media {
        height: 150px !important;
        border-radius: 16px !important;
    }

    .ae-contrib-card,
    .ae-contrib-approved-card,
    .ae-contrib-person-row {
        grid-template-columns: 44px 1fr !important;
    }

    .ae-contrib-card-head {
        display: block !important;
    }

    .ae-contrib-card-head em,
    .ae-contrib-approved-card span,
    .ae-contrib-person-row button {
        display: inline-flex !important;
        margin-top: 0.45rem !important;
    }
}
</style>
""", unsafe_allow_html=True)
