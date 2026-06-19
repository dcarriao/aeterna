import streamlit as st


def aplicar_css_dashboard():
    st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 18% 10%, rgba(74,38,110,0.10), transparent 26%),
        radial-gradient(circle at 84% 18%, rgba(212,168,79,0.10), transparent 24%),
        linear-gradient(180deg, #F7F3EA 0%, #f5efe5 100%);
}

#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stDeployButton"],
[data-testid="stMainMenu"] {
    display: none !important;
    visibility: hidden !important;
}

.block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
    padding-bottom: 0.65rem !important;
    max-width: 1280px !important;
    width: min(1280px, calc(100vw - 285px)) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Sidebar premium */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 18% 8%, rgba(242,197,114,0.18), transparent 24%),
        linear-gradient(180deg, #140322 0%, #24113d 58%, #12021f 100%);
    border-right: 1px solid rgba(212,175,55,0.28);
    min-width: 190px !important;
    max-width: 220px !important;
    width: 200px !important;
}

[data-testid="stSidebar"] > div:first-child {
    width: 200px !important;
    padding-left: 0.6rem !important;
    padding-right: 0.6rem !important;
}

[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.88);
}

.ae-sidebar-brand {
    text-align: center;
    padding: 0.15rem 0 0.3rem;
    margin-bottom: 0.35rem;
    border-bottom: 1px solid rgba(212,175,55,0.22);
}

.ae-sidebar-logo {
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 2rem;
    font-style: italic;
    color: #f2c572;
    line-height: 1;
    letter-spacing: -0.05em;
}

.ae-sidebar-subtitle {
    color: rgba(242,197,114,0.72) !important;
    font-size: 0.54rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 0.26rem;
}

.ae-sidebar-user {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 18px;
    padding: 0.95rem;
    margin-bottom: 0.85rem;
}

.ae-sidebar-user-title {
    color: #f2c572 !important;
    font-weight: 900;
    font-size: 0.94rem;
    margin-bottom: 0.22rem;
}

.ae-sidebar-user-subtitle {
    color: rgba(255,255,255,0.68) !important;
    font-size: 0.76rem;
}

.ae-sidebar-section {
    color: #f2c572 !important;
    font-weight: 900;
    margin: 0.45rem 0 0.35rem;
    font-size: 0.78rem;
}

.ae-sidebar-stat {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.72rem 0.82rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.10);
    margin-bottom: 0.5rem;
}

.ae-sidebar-stat-label {
    color: rgba(255,255,255,0.78) !important;
    font-size: 0.8rem;
    font-weight: 800;
}

.ae-sidebar-stat-value {
    color: #f2c572 !important;
    font-size: 1.25rem;
    font-weight: 900;
}

.ae-sidebar-note {
    color: rgba(255,255,255,0.58) !important;
    font-size: 0.7rem;
    text-align: center;
    margin-top: 0.85rem;
    line-height: 1.35;
}

[data-testid="stSidebar"] div.stButton > button {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.90) !important;
    border: 1px solid rgba(212,175,55,0.22) !important;
    border-radius: 13px !important;
    font-weight: 900 !important;
    min-height: 2.15rem !important;
    padding: 0.28rem 0.45rem !important;
    font-size: 0.82rem !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
    color: #1b0f2e !important;
    border: 0 !important;
}

/* Tabs mais limpas e compactas */
div[data-testid="stTabs"] {
    margin-top: -0.6rem;
}

button[data-baseweb="tab"] {
    font-weight: 800 !important;
    color: #3b2454 !important;
    padding-top: 0.45rem !important;
    padding-bottom: 0.45rem !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #b77a46 !important;
    border-bottom-color: #b77a46 !important;
}

/* Painel inicial compacto */
.ae-dashboard-hero {
    background:
        radial-gradient(circle at 82% 18%, rgba(242,197,114,0.22), transparent 30%),
        linear-gradient(135deg, #1b0f2e 0%, #32184f 58%, #8a5a2b 100%);
    color: white;
    border-radius: 28px;
    padding: 1.55rem 1.75rem;
    box-shadow: 0 18px 55px rgba(27,15,46,0.16);
    border: 1px solid rgba(212,175,55,0.28);
    margin-bottom: 1rem;
}

.ae-dashboard-hero h1 {
    color: #f2c572;
    font-size: 1.75rem;
    margin: 0 0 0.35rem;
}

.ae-dashboard-hero p {
    color: rgba(255,255,255,0.82);
    font-size: 0.96rem;
    line-height: 1.5;
    max-width: 780px;
    margin: 0;
}

.ae-dashboard-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.85rem;
    margin-bottom: 1rem;
}

.ae-dashboard-card {
    background: rgba(255,255,255,0.96);
    border-radius: 20px;
    padding: 1rem;
    border: 1px solid rgba(212,175,55,0.20);
    box-shadow: 0 12px 34px rgba(27,15,46,0.08);
    min-height: 142px;
}

.ae-dashboard-card-icon {
    font-size: 1.35rem;
    margin-bottom: 0.45rem;
}

.ae-dashboard-card-label {
    color: #6f6478;
    font-size: 0.76rem;
    font-weight: 800;
}

.ae-dashboard-card-value {
    color: #1b0f2e;
    font-size: 1.85rem;
    font-weight: 900;
    line-height: 1.05;
    margin-top: 0.2rem;
}

.ae-dashboard-card-note {
    color: #9a8fa6;
    font-size: 0.7rem;
    margin-top: 0.3rem;
    line-height: 1.35;
}

.ae-dashboard-next {
    background: rgba(255,255,255,0.94);
    border-radius: 22px;
    padding: 1rem 1.2rem;
    border: 1px solid rgba(212,175,55,0.20);
    box-shadow: 0 12px 34px rgba(27,15,46,0.08);
}

.ae-dashboard-next h3 {
    color: #1b0f2e;
    margin: 0 0 0.55rem;
    font-size: 1.05rem;
}

.ae-dashboard-next ul {
    margin: 0 0 0 1.1rem;
    color: #5f536b;
    line-height: 1.65;
    font-size: 0.9rem;
}

.ae-home-hero {
    background:
        radial-gradient(circle at 82% 18%, rgba(242,197,114,0.24), transparent 30%),
        linear-gradient(135deg, #2B1747 0%, #3a1f5f 56%, #8a5a2b 100%);
    color: white;
    border-radius: 30px;
    padding: 1.75rem 1.9rem;
    box-shadow: 0 18px 55px rgba(43,23,71,0.15);
    border: 1px solid rgba(212,168,79,0.32);
    margin-bottom: 1rem;
}

.ae-home-top {
    min-height: 54px;
    margin-bottom: 0.15rem;
}

.ae-home-top h1 {
    color: #2B1747;
    margin: 0;
    font-size: 1.55rem;
    line-height: 1.1;
}

.ae-home-top p {
    color: #6f6478;
    margin: 0.15rem 0 0;
    font-size: 0.88rem;
}

.ae-top-action-spacer {
    height: 0.28rem;
}

.ae-home-stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.55rem;
    margin: 0.45rem 0 0.65rem;
}

.ae-stat-card {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(212,168,79,0.22);
    border-radius: 16px;
    padding: 0.62rem 0.75rem;
    box-shadow: 0 8px 22px rgba(43,23,71,0.06);
    min-height: 64px;
}

.ae-stat-card span {
    display: block;
    color: #6f6478;
    font-size: 0.78rem;
    font-weight: 800;
    line-height: 1.15;
}

.ae-stat-card strong {
    display: block;
    color: #2B1747;
    font-size: 1.6rem;
    line-height: 1.05;
    margin-top: 0.18rem;
}

.ae-home-panel {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(212,168,79,0.20);
    border-radius: 17px;
    padding: 0.7rem 0.85rem;
    box-shadow: 0 8px 22px rgba(43,23,71,0.06);
    min-height: 124px;
    margin-bottom: 0.35rem;
}

.ae-recent-panel {
    min-height: 96px;
}

.ae-panel-title {
    color: #2B1747;
    font-size: 0.92rem;
    font-weight: 900;
    margin-bottom: 0.35rem;
}

.ae-home-panel ul {
    margin: 0;
    padding-left: 1rem;
    color: #5F536B;
    font-size: 0.84rem;
    line-height: 1.55;
}

.ae-home-panel li {
    margin: 0.05rem 0;
}

.ae-live-home-top {
    min-height: 50px;
    margin-top: -2rem;
}

.ae-live-home-top h1 {
    color: #2B1747;
    font-size: 1.7rem;
    letter-spacing: -0.035em;
    margin: 0 0 0.28rem;
}

.ae-live-home-top p {
    color: #6F6478;
    font-size: 0.92rem;
    margin: 0;
}

.ae-live-home-rule {
    height: 1px;
    background: rgba(212,168,79,0.26);
    margin: 0.2rem 0 0.62rem;
}

.ae-live-section-title {
    color: #2B1747;
    font-size: 1.08rem;
    font-weight: 950;
    margin: 0.62rem 0 0.38rem;
}

.ae-live-story-card {
    height: 218px;
    overflow: hidden;
    border-radius: 16px;
    background: rgba(255,255,255,0.97);
    border: 1px solid rgba(212,168,79,0.22);
    box-shadow: 0 12px 28px rgba(43,23,71,0.07);
}

.ae-live-story-media {
    height: 88px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background:
        radial-gradient(circle at 72% 18%, rgba(212,168,79,0.26), transparent 32%),
        linear-gradient(135deg, rgba(43,23,71,0.94), rgba(85,54,110,0.86));
    color: white;
    text-align: center;
}

.ae-live-story-media img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.ae-live-story-media span {
    display: block;
    font-size: 1.45rem;
}

.ae-live-story-media strong {
    color: white;
    display: block;
    font-size: 0.68rem;
}

.ae-live-story-media-fallback {
    background:
        radial-gradient(circle at 80% 20%, rgba(212,168,79,0.30), transparent 34%),
        linear-gradient(135deg, #F7F3EA, #EFE3C8);
}

.ae-live-story-media-fallback span,
.ae-live-story-media-fallback strong {
    color: #2B1747;
}

.ae-live-story-body {
    padding: 0.7rem 0.82rem;
}

.ae-live-story-body h3 {
    color: #2B1747;
    font-size: 0.96rem;
    line-height: 1.18;
    margin: 0 0 0.22rem;
    min-height: 2.25em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.ae-live-story-date {
    color: #6F6478;
    display: block;
    font-size: 0.68rem;
    font-weight: 800;
    margin-bottom: 0.28rem;
}

.ae-live-story-body p {
    color: #2F2440;
    font-size: 0.78rem;
    line-height: 1.34;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.ae-live-people-grid,
.ae-live-shared-grid {
    display: grid;
    gap: 0.55rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    min-height: 206px;
}

.ae-live-person-card,
.ae-live-shared-card,
.ae-live-empty-card,
.ae-live-news-item {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(212,168,79,0.20);
    border-radius: 14px;
    box-shadow: 0 8px 22px rgba(43,23,71,0.05);
}

.ae-live-person-card,
.ae-live-shared-card {
    min-height: 100px;
    padding: 0.72rem;
}

.ae-live-avatar {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(212,168,79,0.28), rgba(43,23,71,0.10));
    color: #2B1747;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 950;
    margin-bottom: 0.44rem;
}

.ae-live-avatar-shared {
    font-size: 0.95rem;
}

.ae-live-person-card strong,
.ae-live-shared-card strong,
.ae-live-empty-card strong {
    color: #2B1747;
    display: block;
    font-size: 0.84rem;
    line-height: 1.18;
}

.ae-live-person-card span,
.ae-live-shared-card span,
.ae-live-empty-card span {
    color: #6F6478;
    display: block;
    font-size: 0.72rem;
    line-height: 1.32;
    margin-top: 0.24rem;
}

.ae-live-empty-card {
    padding: 0.78rem;
    min-height: 92px;
}

.ae-live-empty-card-small {
    min-height: 206px;
}

.ae-live-news-list {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.55rem;
    width: 100%;
}

.ae-live-news-item {
    color: #2F2440;
    font-size: 0.78rem;
    line-height: 1.34;
    padding: 0.68rem 0.78rem;
    min-height: 62px;
}

.st-key-home_contar_historia {
    display: flex;
    justify-content: flex-end;
}

.st-key-home_contar_historia button {
    width: 190px !important;
    min-height: 2.05rem !important;
    padding: 0.24rem 0.72rem !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}

.st-key-home_ver_minha_historia button,
.st-key-home_ver_pessoas button,
.st-key-home_ver_historias button,
.st-key-home_ver_novidades button {
    background: transparent !important;
    border: 0 !important;
    color: #2B1747 !important;
    padding: 0.1rem 0 !important;
    min-height: 1.35rem !important;
    font-size: 0.78rem !important;
    font-weight: 850 !important;
    box-shadow: none !important;
}

.st-key-home_ver_minha_historia button p::after,
.st-key-home_ver_pessoas button p::after,
.st-key-home_ver_historias button p::after,
.st-key-home_ver_novidades button p::after {
    content: " →";
}

.ae-sidebar-divider {
    height: 1px;
    background: rgba(212,175,55,0.18);
    margin: 0.55rem 0 0.4rem;
}

[data-testid="stSidebar"] details {
    margin-top: 0.25rem;
}

[data-testid="stSidebar"] details summary {
    font-size: 0.86rem !important;
    font-weight: 900 !important;
}

.ae-home-hero h1 {
    color: #F2C572;
    font-size: 2rem;
    margin: 0.2rem 0 0.45rem;
}

.ae-home-hero p {
    color: rgba(255,255,255,0.84);
    font-size: 1rem;
    line-height: 1.55;
    max-width: 820px;
    margin: 0;
}

.ae-kicker,
.ae-card-label {
    color: #B77A46;
    font-size: 0.76rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.ae-home-card,
.ae-memory-card,
.ae-activity-card,
.ae-shared-card,
.ae-mini-card {
    background: rgba(255,255,255,0.96);
    border-radius: 22px;
    padding: 1.15rem 1.25rem;
    border: 1px solid rgba(212,168,79,0.24);
    box-shadow: 0 12px 34px rgba(43,23,71,0.08);
    margin-bottom: 0.75rem;
}

.ae-home-card h2,
.ae-memory-card h3,
.ae-activity-card h3,
.ae-shared-card h3 {
    color: #2B1747;
    margin: 0.28rem 0 0.4rem;
}

.ae-home-card p {
    color: #5F536B;
    line-height: 1.55;
    margin: 0;
}

.ae-home-card-feature {
    min-height: 172px;
}

.ae-plan-card {
    background:
        radial-gradient(circle at 80% 18%, rgba(212,168,79,0.18), transparent 32%),
        rgba(255,255,255,0.97);
}

.ae-small {
    margin-top: 0.65rem !important;
    font-size: 0.86rem;
    color: #7A6D84 !important;
}

.ae-mini-card {
    padding: 0.85rem 1rem;
    border-radius: 18px;
}

.ae-mini-card strong {
    color: #2B1747;
    display: block;
    margin-bottom: 0.2rem;
}

.ae-mini-card span {
    color: #6f6478;
    font-size: 0.86rem;
}

.ae-activity-card,
.ae-shared-card,
.ae-person-card {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.ae-activity-icon,
.ae-avatar {
    width: 46px;
    height: 46px;
    min-width: 46px;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(212,168,79,0.24), rgba(43,23,71,0.08));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
}

.ae-activity-card p,
.ae-shared-card p,
.ae-shared-card span {
    color: #5F536B;
    margin: 0;
    line-height: 1.45;
}

.ae-people-summary {
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;
    margin: 0.2rem 0 0.65rem;
}

.ae-people-summary span {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(212,168,79,0.22);
    border-radius: 999px;
    color: #2B1747;
    font-size: 0.82rem;
    font-weight: 900;
    padding: 0.38rem 0.7rem;
}

.ae-person-card {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(212,168,79,0.20);
    border-radius: 18px;
    padding: 0.78rem 0.9rem;
    box-shadow: 0 8px 22px rgba(43,23,71,0.06);
    margin-bottom: 0.38rem;
}

.ae-person-card h3 {
    color: #2B1747;
    font-size: 1rem;
    margin: 0 0 0.16rem;
}

.ae-person-card p,
.ae-person-card span {
    color: #5F536B;
    margin: 0;
    font-size: 0.84rem;
    line-height: 1.35;
}

.ae-person-card span {
    color: #B77A46;
    font-weight: 900;
}

.ae-shared-card span {
    display: inline-block;
    margin-top: 0.45rem;
    color: #B77A46;
    font-weight: 900;
}

.ae-memory-card {
    padding: 0.9rem 1rem;
    margin-top: 0.55rem;
}

.ae-story-top {
    min-height: 46px;
    max-height: 62px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: transparent;
    border: 0;
    border-radius: 0;
    padding: 0;
    margin-top: -2.65rem;
    margin-bottom: 0;
    box-shadow: none;
}

.ae-story-top h2 {
    color: #2B1747;
    margin: 0 0 0.18rem;
    font-size: 1.62rem;
    letter-spacing: -0.035em;
}

.ae-story-top p {
    color: #6F6478;
    margin: 0;
    font-size: 0.84rem;
}

.ae-story-header-rule {
    height: 1px;
    background: rgba(212,168,79,0.26);
    margin: 0.1rem 0 0.44rem;
}

.ae-empty-story {
    background:
        radial-gradient(circle at top right, rgba(212,168,79,0.18), transparent 36%),
        rgba(255,255,255,0.96);
    border: 1px dashed rgba(212,168,79,0.45);
    border-radius: 22px;
    padding: 1.25rem 1.1rem;
    margin: 0.85rem 0;
    text-align: center;
    box-shadow: 0 12px 34px rgba(43,23,71,0.07);
}

.ae-empty-story h3 {
    color: #2B1747;
    margin: 0 0 0.35rem;
    font-size: 1.12rem;
}

.ae-empty-story p {
    color: #5F536B;
    margin: 0;
    font-size: 0.9rem;
}

.ae-story-section-title {
    color: #2B1747;
    font-size: 1.08rem;
    font-weight: 950;
    margin: 0.34rem 0 0.28rem;
}

.ae-story-shelf-title {
    color: #2B1747;
    font-size: 1rem;
    font-weight: 950;
    margin: 1.25rem 0 0.42rem;
}

.ae-story-card {
    height: 232px;
    width: 100%;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(212,168,79,0.24);
    border-radius: 16px;
    margin: 0.18rem 0 0;
    box-shadow: 0 12px 28px rgba(43,23,71,0.08);
}

.ae-story-media {
    height: 86px;
    width: 100%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(circle at 72% 18%, rgba(212,168,79,0.26), transparent 32%),
        linear-gradient(135deg, rgba(43,23,71,0.94), rgba(85,54,110,0.86));
    color: white;
}

.ae-story-media img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ae-story-media-photo-fallback {
    display: none;
    text-align: center;
}

.ae-story-media span {
    color: #F7F3EA;
    display: block;
    font-size: 1.65rem;
    margin-bottom: 0.16rem;
}

.ae-story-media strong {
    color: #F7F3EA;
    display: block;
    font-size: 0.8rem;
}

.ae-story-media-video {
    background:
        radial-gradient(circle at 75% 18%, rgba(212,168,79,0.32), transparent 34%),
        linear-gradient(135deg, #2B1747, #6D3E71);
    text-align: center;
}

.ae-story-media-fallback {
    background:
        radial-gradient(circle at 80% 20%, rgba(212,168,79,0.30), transparent 34%),
        linear-gradient(135deg, #F7F3EA, #EFE3C8);
    color: #2B1747;
    text-align: center;
}

.ae-story-media-fallback span,
.ae-story-media-fallback strong,
.ae-collection-mini-media-fallback span,
.ae-collection-mini-media-fallback strong {
    color: #2B1747;
}

.ae-story-body {
    min-height: 146px;
    padding: 0.58rem 0.76rem 0.55rem;
    display: flex;
    flex-direction: column;
}

.ae-story-card h3 {
    color: #2B1747;
    margin: 0 0 0.18rem;
    font-size: 0.9rem;
    line-height: 1.2;
    min-height: 2.36em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.ae-story-date {
    color: #6F6478;
    font-weight: 700;
    font-size: 0.68rem;
    min-height: 0.74rem;
}

.ae-story-card p {
    color: #2F2440;
    margin: 0.24rem 0 0;
    font-size: 0.76rem;
    line-height: 1.28;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.ae-story-indicators {
    display: flex;
    flex-wrap: wrap;
    gap: 0.28rem;
    margin-top: auto;
    padding-top: 0.28rem;
}

.ae-story-indicators span {
    color: #6F6478;
    background: rgba(247,243,234,0.92);
    border: 1px solid rgba(212,168,79,0.20);
    border-radius: 999px;
    padding: 0.1rem 0.32rem;
    font-size: 0.6rem;
    font-weight: 800;
}

div[data-testid="stPopover"] button {
    min-height: 1.72rem;
    padding: 0.14rem 0.48rem;
    border-color: rgba(212,168,79,0.35);
    color: #5F536B;
    background: rgba(255,255,255,0.72);
    font-size: 0.72rem;
}

div[data-testid="stPopover"] {
    margin-top: 0.12rem;
    margin-left: 0.6rem;
    position: relative;
    z-index: 3;
}

.st-key-minha_historia_contar_historia {
    display: flex;
    justify-content: flex-end;
}

.st-key-minha_historia_contar_historia button {
    width: 215px !important;
    min-height: 2.05rem !important;
    padding: 0.24rem 0.72rem !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}

.ae-story-section-title-collections {
    margin-top: 0.7rem;
}

.ae-collection-box {
    background: rgba(255,255,255,0.52);
    border: 1px solid rgba(212,168,79,0.22);
    border-radius: 16px;
    padding: 0.55rem;
    box-shadow: 0 12px 30px rgba(43,23,71,0.06);
    height: 214px;
    min-height: 214px;
    margin-bottom: 0.35rem;
    overflow: hidden;
}

.ae-collection-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.48rem;
}

.ae-collection-head h3 {
    color: #2B1747;
    font-size: 0.78rem;
    margin: 0;
}

.ae-collection-head span {
    color: #2B1747;
    font-size: 0.66rem;
    font-weight: 850;
    white-space: nowrap;
}

.ae-collection-mini-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.34rem;
    height: 162px;
    align-items: stretch;
}

.ae-collection-mini-card {
    background: rgba(255,255,255,0.95);
    border: 1px solid rgba(212,168,79,0.20);
    border-radius: 10px;
    overflow: hidden;
    height: 124px;
    min-height: 124px;
    box-shadow: 0 8px 18px rgba(43,23,71,0.06);
}

.ae-collection-mini-card-empty {
    opacity: 0.58;
    border-style: dashed;
}

.ae-collection-mini-media {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background:
        radial-gradient(circle at 75% 18%, rgba(212,168,79,0.26), transparent 34%),
        linear-gradient(135deg, #2B1747, #6D3E71);
    color: white;
    text-align: center;
}

.ae-collection-mini-media img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ae-collection-mini-media span {
    display: block;
    font-size: 1.05rem;
}

.ae-collection-mini-media strong {
    display: block;
    color: white;
    font-size: 0.58rem;
}

.ae-collection-mini-media-fallback {
    background:
        radial-gradient(circle at 80% 18%, rgba(212,168,79,0.30), transparent 34%),
        linear-gradient(135deg, #F7F3EA, #EFE3C8);
}

.ae-collection-mini-body {
    padding: 0.42rem 0.46rem;
}

.ae-collection-mini-body strong {
    color: #2B1747;
    display: block;
    font-size: 0.68rem;
    line-height: 1.18;
    min-height: 2.35em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.ae-collection-mini-body > span {
    color: #6F6478;
    display: block;
    font-size: 0.6rem;
    margin-top: 0.16rem;
}

.footer-aeterna {
    text-align: center;
    color: #8a7b95;
    font-size: 0.76rem;
    padding: 0.45rem 0 0;
}

@media (max-width: 1100px) {
    .block-container {
        width: auto !important;
        max-width: 100% !important;
        margin-left: 1rem !important;
        margin-right: 1rem !important;
        padding-left: 0.35rem !important;
        padding-right: 0.35rem !important;
    }

    .ae-dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 701px) {
    .element-container {
        margin-bottom: 0.28rem !important;
    }
}

@media (max-width: 700px) {
    .ae-dashboard-grid {
        grid-template-columns: 1fr;
    }

    .ae-dashboard-hero,
    .ae-home-hero {
        padding: 1.25rem;
        border-radius: 22px;
    }

    .ae-home-hero h1 {
        font-size: 1.55rem;
    }

    .ae-home-card,
    .ae-activity-card,
    .ae-shared-card {
        padding: 0.95rem;
        border-radius: 18px;
    }

    .ae-activity-card,
    .ae-shared-card {
        gap: 0.75rem;
    }

    [data-testid="stSidebar"] .ae-sidebar-brand {
        margin-bottom: 0.35rem;
        padding-bottom: 0.35rem;
    }

    [data-testid="stSidebar"] div.stButton > button {
        min-height: 2.35rem !important;
        padding: 0.35rem 0.55rem !important;
        font-size: 0.9rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


def render_sidebar_premium(
    nome_exibido,
    qtd_videos,
    qtd_contatos,
    qtd_cofre=0,
    qtd_memorias=0,
    is_admin=False,
    fazer_logout=None,
):
    with st.sidebar:
        with st.sidebar:
            st.markdown(
                '<div class="ae-sidebar-brand">',
                unsafe_allow_html=True
            )

            try:
                st.image(
                    "assets/logo-sidebar.png",
                    width=132
                )
            except Exception as exc:
                print("Erro ao carregar logo da sidebar:", exc)
                st.markdown(
                    '<div class="ae-sidebar-logo">aEterna</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        usuario = st.session_state.get("usuario_atual") or {}

        if usuario.get("tipo") == "visitante":
            nome_falecido = usuario.get("nome_falecido", "essa pessoa")

            st.markdown(f"### Histórias de {nome_falecido}")

            st.markdown("🔎 Explorar História")

            if qtd_videos > 0:
                st.markdown(f"🎥 Vídeos compartilhados: **{qtd_videos}**")

            if qtd_memorias > 0:
                st.markdown(f"💬 Histórias disponíveis: **{qtd_memorias}**")

            if qtd_cofre > 0:
                st.markdown(f"🔒 Itens liberados: **{qtd_cofre}**")

            st.markdown("---")
            return

        return


def render_painel_inicial(nome_exibido, qtd_videos, qtd_contatos, qtd_cofre=0, qtd_memorias=0):
    primeiro_nome = str(nome_exibido).split()[0] if nome_exibido else "Olá"

    hero_html = (
        f'<div class="ae-dashboard-hero">'
        f'<h1>Bem-vindo, {primeiro_nome}.</h1>'
        f'<p>Este é o espaço onde sua história ganha forma. '
        f'Aqui você registra memórias, fotos, vídeos, pessoas importantes e mensagens para o futuro..</p>'
        f'</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    cards_html = (
        '<div class="ae-dashboard-grid">'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">🎥</div><div class="ae-dashboard-card-label">Histórias registradas</div><div class="ae-dashboard-card-value">{qtd_videos}</div><div class="ae-dashboard-card-note">Mensagens em vídeo para o futuro.</div></div>'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">👥</div><div class="ae-dashboard-card-label">Contatos de confiança</div><div class="ae-dashboard-card-value">{qtd_contatos}</div><div class="ae-dashboard-card-note">Pessoas autorizadas a acessar sua história.</div></div>'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">🔒</div><div class="ae-dashboard-card-label">Fotos preservadas</div><div class="ae-dashboard-card-value">{qtd_cofre}</div><div class="ae-dashboard-card-note">Documentos e informações importantes.</div></div>'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">💬</div><div class="ae-dashboard-card-label">Pessoas importantes</div><div class="ae-dashboard-card-value">{qtd_memorias}</div><div class="ae-dashboard-card-note">Histórias, valores e ensinamentos.</div></div>'
        '</div>'
    )
    st.markdown(cards_html, unsafe_allow_html=True)

    next_html = (
        '<div class="ae-dashboard-next">'
        '<h3>Comece a construir sua história</h3>'
        '<ul>'
        '<li>Conte uma primeira história importante da sua vida.</li>'
        '<li>Adicione fotos que representem momentos especiais.</li>'
        '<li>Cadastre pessoas importantes para conectar à sua história.</li>'
        '<li>Registre datas que merecem ser lembradas.</li>'
        '<li>Use o Curador para organizar lembranças com perguntas simples.</li>'
        '</ul>'
        '</div>'
    )
    st.markdown(next_html, unsafe_allow_html=True)
