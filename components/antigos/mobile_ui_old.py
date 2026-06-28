import streamlit as st

def aplicar_css_mobile():
    st.markdown("""
<style>
@media (max-width: 768px) {
    input,
    textarea,
    select {
        color: #1b0f2e !important;
    }
    
    .stToolbar,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stHeaderActionElements"],
    header [title="View source"],
    header a[href*="github"],
    header a[href*="streamlit"],
    .viewerBadge_container__1QSob,
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
    }
    
    div[data-testid="stFormSubmitButton"] button[kind="secondary"] {
        background: rgba(255,255,255,0.95) !important;
        color: #1b0f2e !important;
        border: 1px solid rgba(212,175,55,0.38) !important;
    }
    
    input::placeholder,
    textarea::placeholder {
        color: #8a7b95 !important;
        opacity: 1 !important;
    }
    .block-container {
        padding-top: 0.65rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 18% 8%, rgba(74,38,110,0.10), transparent 26%),
            radial-gradient(circle at 82% 14%, rgba(212,175,55,0.08), transparent 24%),
            linear-gradient(180deg, #f7fbf5 0%, #eef8ef 100%) !important;
    }

    .footer-aeterna {
        font-size: 0.72rem !important;
        padding: 1rem 0 0.5rem !important;
    }

    div[data-testid="stTabs"] {
        margin-top: 0 !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        padding-bottom: 0.25rem !important;
        scrollbar-width: none !important;
    }

    div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
        display: none !important;
    }

    button[data-baseweb="tab"] {
        min-width: auto !important;
        padding: 0.55rem 0.75rem !important;
        font-size: 0.88rem !important;
        font-weight: 800 !important;
    }

    button[data-baseweb="tab"] p {
        font-size: 0.88rem !important;
        margin: 0 !important;
    }

    h1 {
        font-size: 1.65rem !important;
        line-height: 1.15 !important;
        color: #2b1747 !important;
        margin-bottom: 0.85rem !important;
    }

    h2 {
        font-size: 1.35rem !important;
        line-height: 1.18 !important;
        color: #2b1747 !important;
    }

    h3 {
        font-size: 1.05rem !important;
        color: #2b1747 !important;
    }

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stText,
    label,
    small,
    span,
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] p {
        color: #2b1747 !important;
    }

    .ae-dashboard-hero * {
        color: inherit !important;
    }
    
    .ae-chat-header * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] * {
        color: inherit !important;
    }

    .ae-memory-card p,
    .ae-memory-card span,
    .ae-dashboard-hero p {
        color: rgba(255,255,255,0.84) !important;
    }

    .ae-memory-card h2,
    .ae-dashboard-hero h1 {
        color: #f2c572 !important;
    }

    .ae-dashboard-hero {
        border-radius: 22px !important;
        padding: 1.15rem !important;
        margin-bottom: 0.9rem !important;
    }

    .ae-dashboard-hero h1 {
        font-size: 1.45rem !important;
    }

    .ae-dashboard-hero p {
        font-size: 0.88rem !important;
        line-height: 1.45 !important;
    }

    .ae-dashboard-grid {
        grid-template-columns: 1fr !important;
        gap: 0.75rem !important;
    }

    .ae-dashboard-card {
        min-height: auto !important;
        padding: 0.95rem !important;
        border-radius: 18px !important;
    }

    .ae-dashboard-card-value {
        font-size: 1.55rem !important;
    }

    .ae-dashboard-next {
        border-radius: 18px !important;
        padding: 0.95rem !important;
    }

    .ae-dashboard-next h3 {
        font-size: 1rem !important;
    }

    .ae-dashboard-next ul {
        font-size: 0.84rem !important;
        line-height: 1.55 !important;
    }

    div[data-testid="stForm"],
    div[data-testid="stExpander"] {
        border-radius: 18px !important;
    }

    input,
    textarea,
    select {
        font-size: 16px !important;
        color: #1b0f2e !important;
        background: #ffffff !important;
        border-radius: 12px !important;
    }

    textarea {
        min-height: 92px !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        background: #ffffff !important;
        border-radius: 12px !important;
    }

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button,
    button[data-testid*="baseButton"] {
        min-height: 2.75rem !important;
        border-radius: 12px !important;
        font-size: 0.92rem !important;
        font-weight: 900 !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.94) !important;
        border: 1px solid rgba(212,175,55,0.20) !important;
        border-radius: 16px !important;
        padding: 0.85rem !important;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: #2b1747 !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 16px !important;
        font-size: 0.9rem !important;
    }

    .ae-memory-card {
        display: none !important;
    }

    .ae-chat-shell {
        max-width: 100% !important;
        margin: 0 !important;
        border-radius: 22px !important;
        padding: 8px !important;
    }

    .ae-chat-header {
        border-radius: 18px 18px 0 0 !important;
        padding: 12px !important;
    }

    .ae-chat-shell {
        margin-top: 0.5rem !important;
    }
    
    .ae-chat-warning {
        display: none !important;
    }

    .ae-message-bubble {
        max-width: 88% !important;
        font-size: 0.86rem !important;
    }

    .ae-chat-warning {
        font-size: 0.66rem !important;
        padding: 7px 10px !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.75rem !important;
    }

    .viewerBadge_container__1QSob,
    #MainMenu,
    footer {
        visibility: hidden !important;
    }
    /* Oculta toolbar Streamlit Cloud / GitHub / Fork */
    [data-testid="stToolbar"],
    [data-testid="stHeaderActionElements"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"],
    [data-testid="stMainMenu"],
    .stToolbar,
    .stDeployButton,
    header button,
    header a,
    header [role="button"],
    iframe[title*="streamlit"],
    iframe[title*="GitHub"],
    iframe[title*="Fork"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
}
</style>
""", unsafe_allow_html=True)
