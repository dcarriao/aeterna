import streamlit as st


def aplicar_css_dashboard():
    st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 18% 10%, rgba(74,38,110,0.10), transparent 26%),
        radial-gradient(circle at 84% 18%, rgba(212,175,55,0.08), transparent 24%),
        linear-gradient(180deg, #f7fbf5 0%, #eef8ef 100%);
}

.block-container {
    padding-top: 1.4rem !important;
    padding-bottom: 1.2rem !important;
    max-width: 1180px !important;
}

/* Sidebar premium */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 18% 8%, rgba(242,197,114,0.18), transparent 24%),
        linear-gradient(180deg, #140322 0%, #24113d 58%, #12021f 100%);
    border-right: 1px solid rgba(212,175,55,0.28);
}

[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.88);
}

.ae-sidebar-brand {
    text-align: center;
    padding: 0.4rem 0;
    margin-bottom: 0.8rem;
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
    margin: 0.85rem 0 0.6rem;
    font-size: 0.9rem;
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
    background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
    color: #1b0f2e !important;
    border: 0 !important;
    border-radius: 13px !important;
    font-weight: 900 !important;
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

.footer-aeterna {
    text-align: center;
    color: #8a7b95;
    font-size: 0.76rem;
    padding: 1.1rem 0 0.4rem;
}

@media (max-width: 1100px) {
    .ae-dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 700px) {
    .ae-dashboard-grid {
        grid-template-columns: 1fr;
    }

    .ae-dashboard-hero {
        padding: 1.25rem;
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

            st.image(
                "assets/logo-sidebar.png",
                width=180
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        if fazer_logout and st.button("🚪 Encerrar sessão", use_container_width=True):
            fazer_logout()

        st.markdown('<div class="ae-sidebar-section">Seu legado</div>', unsafe_allow_html=True)

        stats_html = (
            f'<div class="ae-sidebar-stat"><div class="ae-sidebar-stat-label">🎥 Vídeos</div><div class="ae-sidebar-stat-value">{qtd_videos}</div></div>'
            f'<div class="ae-sidebar-stat"><div class="ae-sidebar-stat-label">👥 Família</div><div class="ae-sidebar-stat-value">{qtd_contatos}</div></div>'
            f'<div class="ae-sidebar-stat"><div class="ae-sidebar-stat-label">🔒 Cofre</div><div class="ae-sidebar-stat-value">{qtd_cofre}</div></div>'
            f'<div class="ae-sidebar-stat"><div class="ae-sidebar-stat-label">💬 Memórias</div><div class="ae-sidebar-stat-value">{qtd_memorias}</div></div>'
        )
        st.markdown(stats_html, unsafe_allow_html=True)

        perfil = "Administrador" if is_admin else "Usuário"
        st.markdown(
            f'<div class="ae-sidebar-note">Perfil: {perfil}<br>aEterna Beta</div>',
            unsafe_allow_html=True,
        )


def render_painel_inicial(nome_exibido, qtd_videos, qtd_contatos, qtd_cofre=0, qtd_memorias=0):
    primeiro_nome = str(nome_exibido).split()[0] if nome_exibido else "Olá"

    hero_html = (
        f'<div class="ae-dashboard-hero">'
        f'<h1>Bem-vindo, {primeiro_nome}.</h1>'
        f'<p>Este é o painel do seu legado digital. Aqui você organiza vídeos, mensagens, '
        f'contatos de confiança, documentos importantes e memórias para quem você ama.</p>'
        f'</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    cards_html = (
        '<div class="ae-dashboard-grid">'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">🎥</div><div class="ae-dashboard-card-label">Vídeos registrados</div><div class="ae-dashboard-card-value">{qtd_videos}</div><div class="ae-dashboard-card-note">Mensagens em vídeo para o futuro.</div></div>'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">👥</div><div class="ae-dashboard-card-label">Contatos de confiança</div><div class="ae-dashboard-card-value">{qtd_contatos}</div><div class="ae-dashboard-card-note">Pessoas autorizadas a acessar seu legado.</div></div>'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">🔒</div><div class="ae-dashboard-card-label">Itens no cofre</div><div class="ae-dashboard-card-value">{qtd_cofre}</div><div class="ae-dashboard-card-note">Documentos e informações importantes.</div></div>'
        f'<div class="ae-dashboard-card"><div class="ae-dashboard-card-icon">💬</div><div class="ae-dashboard-card-label">Memórias registradas</div><div class="ae-dashboard-card-value">{qtd_memorias}</div><div class="ae-dashboard-card-note">Histórias, valores e ensinamentos.</div></div>'
        '</div>'
    )
    st.markdown(cards_html, unsafe_allow_html=True)

    next_html = (
        '<div class="ae-dashboard-next">'
        '<h3>Próximos passos recomendados</h3>'
        '<ul>'
        '<li>Grave uma primeira mensagem em vídeo para alguém especial.</li>'
        '<li>Cadastre pelo menos um contato de confiança.</li>'
        '<li>Adicione informações importantes ao cofre digital.</li>'
        '<li>Use o Assistente de Memória para registrar histórias e ensinamentos.</li>'
        '</ul>'
        '</div>'
    )
    st.markdown(next_html, unsafe_allow_html=True)
