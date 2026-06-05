import streamlit as st
from PIL import Image
import os
from datetime import datetime
from utils.banco import BancoDados
from utils.criptografia import GerenciadorCriptografia


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

def encontrar_icone_aba():
    """Procura o ícone para a aba do navegador"""
    icones_possiveis = [
        "assets/favicon.ico",
        "assets/favicon-32.png",
        "assets/favicon-64.png",
        "assets/icon-192.png",
        "assets/logo.png",
        "logo.png"
    ]

    for icone in icones_possiveis:
        if os.path.exists(icone):
            return icone
    return "🌿"


icone_aba = encontrar_icone_aba()

st.set_page_config(
    page_title="aEterna - Seu Legado Digital",
    page_icon=icone_aba,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def carregar_logo():
    """Carrega a logo otimizada do aplicativo"""
    logo_paths = [
        "assets/logo.png",
        "assets/icon-512.png",
        "assets/icon-256.png",
        "logo.png"
    ]

    for path in logo_paths:
        if os.path.exists(path):
            try:
                return Image.open(path)
            except:
                continue
    return None


def remover_fundo_branco(imagem):
    """Remove fundo branco da imagem (torna transparente)"""
    if imagem is None:
        return None

    if imagem.mode != 'RGBA':
        imagem = imagem.convert('RGBA')

    dados = imagem.getdata()
    nova_lista = []
    for item in dados:
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            nova_lista.append((255, 255, 255, 0))
        else:
            nova_lista.append(item)

    imagem.putdata(nova_lista)
    return imagem


def inject_custom_css():
    """Injeta CSS personalizado - com remoção da faixa de deploy"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

        /* ========== REMOVER FAIXA DE DEPLOY E BOTÕES DO STREAMLIT ========== */
        /* Remove o botão Deploy e a faixa branca */
        .stDeployButton {
            display: none !important;
        }

        /* Remove a barra superior do Streamlit Cloud */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Remove o espaço reservado para o deploy */
        .stApp > header {
            display: none !important;
        }

        /* Ajusta o padding do topo para compensar a remoção */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 1rem;
        }

        /* Remove qualquer elemento indesejado */
        .stStatusWidget {
            display: none !important;
        }

        /* Ajusta o iframe de deploy */
        iframe {
            display: none !important;
        }

        /* Remove a faixa branca superior */
        .stAppViewContainer {
            padding-top: 0 !important;
        }

        /* ========== VARIÁVEIS DO TEMA VERDE ========== */
        :root {
            --aeterna-green-light: #90EE90;
            --aeterna-green-medium: #3CB371;
            --aeterna-green-primary: #2E8B57;
            --aeterna-green-dark: #1B5E20;
            --aeterna-green-deep: #0A2F1F;
        }

        /* Remove padding extra */
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
        }

        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
        }

        h1, h2, h3 {
            font-family: 'Playfair Display', serif !important;
        }

        /* ========== HEADER ========== */
        .aeterna-header {
            background: linear-gradient(135deg, var(--aeterna-green-light) 0%, var(--aeterna-green-primary) 50%, var(--aeterna-green-dark) 100%);
            padding: 0.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        /* ========== CARDS ========== */
        .info-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0faf0 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid var(--aeterna-green-primary);
            margin: 0.75rem 0;
            transition: transform 0.2s;
        }

        .info-card:hover {
            transform: translateY(-2px);
        }

        .info-card h3 {
            font-size: 1rem;
            margin-bottom: 0.5rem;
            color: var(--aeterna-green-dark);
        }

        .info-card p {
            font-size: 0.8rem;
            margin-bottom: 0.25rem;
        }

        .warning-card {
            background: linear-gradient(135deg, #fff3cd 0%, #ffe69b 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid #ffc107;
            margin: 0.75rem 0;
        }

        .success-card {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid var(--aeterna-green-primary);
            margin: 0.75rem 0;
        }

        /* ========== BOTÕES ========== */
        .stButton > button {
            background: linear-gradient(135deg, var(--aeterna-green-medium) 0%, var(--aeterna-green-dark) 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.4rem 0.8rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(46, 139, 87, 0.3);
        }

        /* ========== SIDEBAR ========== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e8f5e9 0%, #f0faf0 100%);
        }

        /* Container da logo na sidebar */
        .sidebar-logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0 15px 0;
            background: transparent;
        }

        /* Forçar tamanho e fundo transparente na sidebar */
        [data-testid="stSidebar"] img {
            max-width: 280px !important;
            width: 280px !important;
            margin: 0 auto;
            background: transparent !important;
        }

        /* Estilo do título na sidebar */
        [data-testid="stSidebar"] h3 {
            text-align: center;
            color: #2E8B57;
            margin-top: 0;
            font-size: 1.5rem;
        }

        /* ========== EXPANDER ========== */
        .streamlit-expanderHeader {
            background-color: #f0faf0;
            border-radius: 8px;
            font-weight: 500;
            color: var(--aeterna-green-dark);
        }

        /* ========== TABS ========== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 5px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 0.4rem 0.8rem;
            font-weight: 500;
            font-size: 0.85rem;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--aeterna-green-medium) 0%, var(--aeterna-green-dark) 100%);
            color: white;
        }

        /* ========== METRICAS ========== */
        [data-testid="stMetricValue"] {
            color: var(--aeterna-green-dark);
            font-size: 1.1rem;
        }

        /* ========== FOOTER ========== */
        .footer-aeterna {
            text-align: center;
            padding: 1rem;
            color: #808080;
            font-size: 0.7rem;
            border-top: 1px solid #d0e8d0;
            margin-top: 2rem;
        }

        /* ========== ANIMAÇÕES ========== */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .aeterna-header {
            animation: fadeIn 0.5s ease-out;
        }

        /* ========== SCROLLBAR ========== */
        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: #e8f5e9;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--aeterna-green-primary);
            border-radius: 10px;
        }

        /* ========== INPUTS ========== */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #c8e6c8;
            font-size: 0.85rem;
        }

        /* ========== REMOVER FUNDO BRANCO DAS IMAGENS ========== */
        img {
            background: transparent !important;
        }

        /* ========== CENTRALIZAR LOGO ========== */
        .stImage {
            display: flex;
            justify-content: center;
        }

        /* ========== AJUSTAR LARGURA DA SIDEBAR ========== */
        [data-testid="stSidebar"] {
            min-width: 300px;
        }
    </style>

    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#2E8B57">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="aEterna">

    <!-- Ícones para diferentes dispositivos -->
    <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
    <link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48.png">
    <link rel="icon" type="image/png" sizes="64x64" href="assets/favicon-64.png">
    <link rel="icon" type="image/png" sizes="96x96" href="assets/favicon-96.png">
    <link rel="icon" type="image/png" sizes="128x128" href="assets/favicon-128.png">
    <link rel="apple-touch-icon" sizes="152x152" href="assets/icon-152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/icon-192.png">
    """, unsafe_allow_html=True)


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================
db = BancoDados()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'senha_mestre' not in st.session_state:
    st.session_state.senha_mestre = ""
if 'crypto' not in st.session_state:
    st.session_state.crypto = None


# ============================================================================
# SIDEBAR
# ============================================================================
def render_sidebar():
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    with st.sidebar:
        if logo_sem_fundo:
            st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
            st.image(logo_sem_fundo, width=280)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; color: #2E8B57;'>✨ aEterna</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #3CB371; font-size: 0.8rem;'>Legado Digital Eterno</p>",
                    unsafe_allow_html=True)
        st.markdown("---")

        if not st.session_state.autenticado:
            st.markdown("### 🔐 Acesso")

            with st.form("login_form"):
                senha_digitada = st.text_input("Senha Mestra", type="password", placeholder="Digite sua senha...")
                submitted = st.form_submit_button("🌿 Abrir Cofre", use_container_width=True)

                if submitted:
                    if senha_digitada:
                        if senha_digitada == "admin123":
                            st.session_state.autenticado = True
                            st.session_state.senha_mestre = senha_digitada
                            st.session_state.crypto = GerenciadorCriptografia(senha_digitada)
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")
                    else:
                        st.warning("⚠️ Digite a senha")

            st.markdown("---")
            st.caption("💡 Teste: admin123")

        else:
            st.success(f"✅ Cofre aberto")
            st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

            if st.button("🔒 Fechar", use_container_width=True):
                st.session_state.autenticado = False
                st.session_state.senha_mestre = ""
                st.session_state.crypto = None
                st.rerun()

            st.markdown("---")
            st.markdown("### 📊 Estatísticas")

            senhas = db.listar_senhas()
            videos = db.listar_videos()
            contatos = db.listar_contatos()

            st.metric("🔐 Senhas", len(senhas))
            st.metric("📹 Vídeos", len(videos))
            st.metric("👥 Contatos", len(contatos))


# ============================================================================
# TELA INICIAL
# ============================================================================
def render_welcome():
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    st.markdown('<div class="aeterna-header">', unsafe_allow_html=True)
    if logo_sem_fundo:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(logo_sem_fundo, width=400)
    else:
        st.markdown("<h1 style='text-align: center; font-size: 6rem; margin: 0;'>🌿</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🔐 Senhas</h3>
            <p>Armazene senhas e acessos de forma segura e criptografada.</p>
            <p style="font-size: 0.7rem; color: #2E8B57;">✓ Criptografia E2E</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📹 Vídeos</h3>
            <p>Grave mensagens em vídeo para seus entes queridos.</p>
            <p style="font-size: 0.7rem; color: #2E8B57;">✓ Mensagens eternas</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>👥 Contatos</h3>
            <p>Indique quem terá acesso após sua partida.</p>
            <p style="font-size: 0.7rem; color: #2E8B57;">✓ Liberação segura</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("🔑 **Para testar**: Digite a senha `admin123` no menu lateral")

    st.markdown("""
    <div class="footer-aeterna">
        <p>✨ aEterna - Preserve sua história, eternize seu legado ✨</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SENHAS
# ============================================================================
def render_senhas():
    st.markdown("<h2 style='color: #2E8B57; font-size: 1.3rem;'>🔐 Gerenciamento de Senhas</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col2:
        with st.expander("➕ Adicionar nova senha", expanded=False):
            servico = st.text_input("Serviço/App *", key="servico_input")
            usuario = st.text_input("Usuário/E-mail *", key="usuario_input")
            senha_original = st.text_input("Senha *", type="password", key="senha_input")
            url = st.text_input("URL", key="url_input")
            notas = st.text_area("Notas", key="notas_input", height=80)

            if st.button("💾 Salvar", key="btn_salvar_senha", type="primary", use_container_width=True):
                if servico and usuario and senha_original:
                    senha_cripto = st.session_state.crypto.criptografar(senha_original)
                    db.adicionar_senha(servico, usuario, senha_cripto, url, notas)
                    st.success(f"✅ {servico} adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Preencha os campos obrigatórios")

    with col1:
        senhas = db.listar_senhas()

        if not senhas:
            st.info("📭 Nenhuma senha cadastrada")
        else:
            for senha in senhas:
                with st.expander(f"🔒 {senha['servico']}"):
                    st.markdown(f"**👤 Usuário:** `{senha['usuario']}`")
                    if senha['url']:
                        st.markdown(f"**🌐 URL:** {senha['url']}")
                    if senha['notas']:
                        st.markdown(f"**📝 Notas:** {senha['notas']}")

                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(f"🔓 Mostrar", key=f"ver_{senha['id']}"):
                            senha_completa = db.obter_senha(senha['id'])
                            if senha_completa:
                                senha_real = st.session_state.crypto.descriptografar(
                                    senha_completa['senha_criptografada'])
                                st.code(senha_real, language="text")
                    with col_btn2:
                        if st.button(f"🗑️ Excluir", key=f"del_{senha['id']}"):
                            db.deletar_senha(senha['id'])
                            st.rerun()


# ============================================================================
# VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h2 style='color: #2E8B57; font-size: 1.3rem;'>📹 Mensagens em Vídeo</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("🎥 Adicionar vídeo", expanded=False):
            titulo = st.text_input("Título *", key="titulo_video_input")
            destinatario = st.text_input("Para", key="destinatario_video")
            url_video = st.text_input("URL *", key="url_video_input", placeholder="https://youtube.com/...")
            notas_video = st.text_area("Notas", key="notas_video", height=60)

            if st.button("💾 Salvar", key="btn_salvar_video", type="primary", use_container_width=True):
                if titulo and url_video:
                    db.adicionar_video(titulo, destinatario, url_externa=url_video, notas=notas_video)
                    st.success(f"✅ {titulo} adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Preencha título e URL")

    with col2:
        videos = db.listar_videos()

        if not videos:
            st.info("📭 Nenhum vídeo cadastrado")
        else:
            for video in videos:
                with st.expander(f"🎬 {video['titulo']}"):
                    if video['destinatario']:
                        st.markdown(f"**👥 Para:** {video['destinatario']}")
                    if video['notas']:
                        st.markdown(f"**📝 Notas:** {video['notas']}")
                    if video['url_externa']:
                        st.video(video['url_externa'])
                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        db.deletar_video(video['id'])
                        st.rerun()


# ============================================================================
# CONTATOS
# ============================================================================
def render_contatos():
    st.markdown("<h2 style='color: #2E8B57; font-size: 1.3rem;'>👥 Contatos de Confiança</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Adicionar contato", expanded=False):
            nome_contato = st.text_input("Nome *", key="nome_contato_input")
            email_contato = st.text_input("E-mail *", key="email_contato_input")
            telefone_contato = st.text_input("Telefone", key="telefone_contato")
            papel_contato = st.selectbox("Papel",
                                         ["Filho(a)", "Cônjuge", "Irmão(ã)", "Amigo(a)", "Outro"],
                                         key="papel_contato")

            if st.button("💾 Salvar", key="btn_salvar_contato", type="primary", use_container_width=True):
                if nome_contato and email_contato:
                    db.adicionar_contato(nome_contato, email_contato, telefone_contato, papel_contato, "")
                    st.success(f"✅ {nome_contato} adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Preencha nome e e-mail")

    with col2:
        contatos = db.listar_contatos()

        if not contatos:
            st.info("📭 Nenhum contato cadastrado")
        else:
            for contato in contatos:
                st.markdown(f"""
                <div class="info-card" style="padding: 0.75rem;">
                    <strong>👤 {contato['nome']}</strong><br>
                    📧 {contato['email']}<br>
                    🏷️ {contato['papel']}
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑️ Remover {contato['nome']}", key=f"del_contato_{contato['id']}"):
                    db.deletar_contato(contato['id'])
                    st.rerun()

        st.markdown("""
        <div class="warning-card" style="padding: 0.75rem; font-size: 0.8rem;">
            <strong>⚠️ Liberação:</strong> 2 contatos precisam confirmar o falecimento
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
def render_configuracoes():
    st.markdown("<h2 style='color: #2E8B57; font-size: 1.3rem;'>⚙️ Configurações</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔄 Segurança")
        interval_days = st.slider("Dias para inatividade", 30, 365, 90, key="slider_inatividade")
        if st.button("💾 Salvar", key="btn_salvar_config"):
            db.salvar_config("prova_vida_dias", str(interval_days))
            st.success("✅ Salvo!")

    with col2:
        st.markdown("#### 📊 Sistema")
        senhas = db.listar_senhas()
        videos = db.listar_videos()
        contatos = db.listar_contatos()

        st.metric("Senhas", len(senhas))
        st.metric("Vídeos", len(videos))
        st.metric("Contatos", len(contatos))


# ============================================================================
# MAIN
# ============================================================================
def main():
    inject_custom_css()
    render_sidebar()

    if not st.session_state.autenticado:
        render_welcome()
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔐 Senhas", "📹 Vídeos", "👥 Contatos", "⚙️ Config"
        ])

        with tab1:
            render_senhas()
        with tab2:
            render_videos()
        with tab3:
            render_contatos()
        with tab4:
            render_configuracoes()

        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna - Legado Digital Eterno ✨</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()