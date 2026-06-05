import streamlit as st
from PIL import Image
import os
from datetime import datetime
from utils.banco import BancoDados
from utils.criptografia import GerenciadorCriptografia
from utils.usuarios import GerenciadorUsuarios


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

def encontrar_icone_aba():
    """Procura o ícone para a aba do navegador"""
    icones_possiveis = [
        "assets/favicon.ico",
        "assets/favicon-32.png",
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
    """Injeta CSS personalizado"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

        :root {
            --aeterna-green-light: #90EE90;
            --aeterna-green-medium: #3CB371;
            --aeterna-green-primary: #2E8B57;
            --aeterna-green-dark: #1B5E20;
        }

        /* Remove botão de deploy */
        .stDeployButton { display: none !important; }
        header[data-testid="stHeader"] { background: transparent !important; }
        .stApp > header { display: none !important; }

        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
        }

        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
        }

        .aeterna-header {
            background: linear-gradient(135deg, var(--aeterna-green-light) 0%, var(--aeterna-green-primary) 50%, var(--aeterna-green-dark) 100%);
            padding: 0.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .info-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0faf0 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid var(--aeterna-green-primary);
            margin: 0.75rem 0;
            transition: transform 0.2s;
        }

        .info-card:hover { transform: translateY(-2px); }

        .stButton > button {
            background: linear-gradient(135deg, #3CB371 0%, #1B5E20 100%);
            color: white;
            border: none;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(46, 139, 87, 0.3);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e8f5e9 0%, #f0faf0 100%);
        }

        .sidebar-logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0 15px 0;
        }

        [data-testid="stSidebar"] img {
            max-width: 280px !important;
            width: 280px !important;
            background: transparent !important;
        }

        .footer-aeterna {
            text-align: center;
            padding: 1rem;
            color: #808080;
            font-size: 0.7rem;
            border-top: 1px solid #d0e8d0;
            margin-top: 2rem;
        }

        img { background: transparent !important; }

        /* Estilo para formulários */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #c8e6c8;
        }

        /* Estilo para abas */
        .stTabs [data-baseweb="tab-list"] { gap: 5px; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 0.4rem 0.8rem;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3CB371 0%, #1B5E20 100%);
            color: white;
        }
    </style>

    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#2E8B57">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="aEterna">
    """, unsafe_allow_html=True)


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================
db = BancoDados()
gerente_usuarios = GerenciadorUsuarios()

# Criar usuário admin inicial
gerente_usuarios.criar_usuario_admin_inicial()

# Inicializar estado da sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_atual' not in st.session_state:
    st.session_state.usuario_atual = None
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'crypto' not in st.session_state:
    st.session_state.crypto = None


# ============================================================================
# FUNÇÕES DE AUTENTICAÇÃO
# ============================================================================
def fazer_login(email, senha):
    """Realiza login do usuário"""
    usuario = gerente_usuarios.autenticar(email, senha)
    if usuario:
        st.session_state.usuario_atual = usuario
        st.session_state.autenticado = True
        st.session_state.pagina = 'app'
        st.session_state.crypto = GerenciadorCriptografia(senha)
        return True
    return False


def fazer_logout():
    """Realiza logout do usuário"""
    st.session_state.autenticado = False
    st.session_state.usuario_atual = None
    st.session_state.pagina = 'login'
    st.session_state.crypto = None
    st.rerun()


def fazer_cadastro(nome, email, senha):
    """Cadastra novo usuário"""
    return gerente_usuarios.criar_usuario(nome, email, senha)


# ============================================================================
# TELA DE LOGIN
# ============================================================================
def render_login():
    """Renderiza tela de login e cadastro"""
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    st.markdown('<div class="aeterna-header">', unsafe_allow_html=True)
    if logo_sem_fundo:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(logo_sem_fundo, width=250)
    st.markdown('</div>', unsafe_allow_html=True)

    # Criar abas para login e cadastro
    tab_login, tab_cadastro = st.tabs(["🔐 Entrar", "📝 Criar Conta"])

    # ABA DE LOGIN
    with tab_login:
        st.markdown("### Bem-vindo de volta!")

        with st.form("login_form"):
            email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
            senha = st.text_input("Senha", type="password", placeholder="Sua senha", key="login_senha")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🌿 Entrar", use_container_width=True)

            if submitted:
                if email and senha:
                    if fazer_login(email, senha):
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha incorretos")
                else:
                    st.warning("⚠️ Preencha todos os campos")

        st.markdown("---")
        st.caption("💡 **Teste:** use admin@aeterna.com / admin123")

    # ABA DE CADASTRO
    with tab_cadastro:
        st.markdown("### Crie sua conta gratuita")
        st.caption("Comece a eternizar seu legado digital")

        with st.form("cadastro_form"):
            nome = st.text_input("Nome completo", placeholder="Seu nome", key="cadastro_nome")
            email = st.text_input("E-mail", placeholder="seu@email.com", key="cadastro_email")
            senha = st.text_input("Senha", type="password", placeholder="Crie uma senha", key="cadastro_senha")
            confirmar_senha = st.text_input("Confirmar senha", type="password", placeholder="Digite a senha novamente",
                                            key="cadastro_confirmar")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("📝 Criar Conta", use_container_width=True)

            if submitted:
                if not nome or not email or not senha:
                    st.error("❌ Preencha todos os campos")
                elif senha != confirmar_senha:
                    st.error("❌ As senhas não coincidem")
                elif len(senha) < 4:
                    st.warning("⚠️ A senha deve ter pelo menos 4 caracteres")
                else:
                    if fazer_cadastro(nome, email, senha):
                        st.success("✅ Conta criada com sucesso! Faça login para continuar.")
                        st.balloons()
                    else:
                        st.error("❌ Este e-mail já está cadastrado")


# ============================================================================
# SIDEBAR (APÓS LOGIN)
# ============================================================================
def render_sidebar():
    """Renderiza a sidebar com informações do usuário"""
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    with st.sidebar:
        if logo_sem_fundo:
            st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
            st.image(logo_sem_fundo, width=220)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"### ✨ Olá, **{st.session_state.usuario_atual['nome']}**!")
        st.caption(f"📧 {st.session_state.usuario_atual['email']}")

        if st.session_state.usuario_atual.get('tipo') == 'admin':
            st.caption("👑 Administrador")

        st.markdown("---")

        # Botão de logout
        if st.button("🚪 Sair", use_container_width=True):
            fazer_logout()

        st.markdown("---")

        # Estatísticas
        st.markdown("### 📊 Seu Cofre")
        senhas = db.listar_senhas()
        videos = db.listar_videos()
        contatos = db.listar_contatos()

        st.metric("🔐 Senhas", len(senhas))
        st.metric("📹 Vídeos", len(videos))
        st.metric("👥 Contatos", len(contatos))


# ============================================================================
# TELA PRINCIPAL DO APP
# ============================================================================
def render_app():
    """Renderiza o app principal após login"""
    st.markdown('<div class="aeterna-header">', unsafe_allow_html=True)
    st.markdown(
        f"<h2 style='text-align: center; color: white;'>Bem-vindo, {st.session_state.usuario_atual['nome']}!</h2>",
        unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; color: rgba(255,255,255,0.9);">Gerencie seu legado digital com segurança</p>',
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔐 Senhas", "📹 Vídeos", "👥 Contatos",
                                      "⚙️ Admin" if st.session_state.usuario_atual.get(
                                          'tipo') == 'admin' else "ℹ️ Sobre"])

    # TAB 1: SENHAS
    with tab1:
        render_senhas()

    # TAB 2: VÍDEOS
    with tab2:
        render_videos()

    # TAB 3: CONTATOS
    with tab3:
        render_contatos()

    # TAB 4: ADMIN ou SOBRE
    with tab4:
        if st.session_state.usuario_atual.get('tipo') == 'admin':
            render_admin()
        else:
            render_sobre()


# ============================================================================
# GERENCIAMENTO DE SENHAS
# ============================================================================
def render_senhas():
    st.markdown("<h2 style='color: #2E8B57;'>🔐 Gerenciamento de Senhas</h2>", unsafe_allow_html=True)

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
# GERENCIAMENTO DE VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h2 style='color: #2E8B57;'>📹 Mensagens em Vídeo</h2>", unsafe_allow_html=True)

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
# GERENCIAMENTO DE CONTATOS
# ============================================================================
def render_contatos():
    st.markdown("<h2 style='color: #2E8B57;'>👥 Contatos de Confiança</h2>", unsafe_allow_html=True)

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
# PAINEL ADMINISTRATIVO
# ============================================================================
def render_admin():
    st.markdown("<h2 style='color: #2E8B57;'>👑 Painel Administrativo</h2>", unsafe_allow_html=True)

    st.markdown("### 📋 Usuários Cadastrados")

    usuarios = gerente_usuarios.listar_usuarios()

    if not usuarios:
        st.info("Nenhum usuário cadastrado")
    else:
        for usuario in usuarios:
            with st.expander(f"👤 {usuario['nome']} - {usuario['email']}"):
                st.markdown(f"**ID:** {usuario['id']}")
                st.markdown(f"**Tipo:** {usuario['tipo']}")
                st.markdown(f"**Data de criação:** {usuario['data_criacao']}")
                st.markdown(f"**Último acesso:** {usuario['ultimo_acesso'] or 'Nunca'}")

    st.markdown("---")
    st.markdown("### 📊 Estatísticas do Sistema")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Usuários", len(usuarios))
    with col2:
        st.metric("Total Senhas", len(db.listar_senhas()))
    with col3:
        st.metric("Total Vídeos", len(db.listar_videos()))
    with col4:
        st.metric("Total Contatos", len(db.listar_contatos()))


# ============================================================================
# TELA SOBRE
# ============================================================================
def render_sobre():
    st.markdown("<h2 style='color: #2E8B57;'>ℹ️ Sobre o aEterna</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>✨ O que é o aEterna?</h3>
        <p>O aEterna é uma plataforma de legado digital que permite você guardar suas senhas, 
        mensagens em vídeo e contatos de confiança em um único lugar seguro.</p>
    </div>

    <div class="info-card">
        <h3>🔒 Segurança</h3>
        <p>Todas as suas senhas são criptografadas localmente antes de serem salvas. 
        Nem mesmo nós temos acesso aos seus dados.</p>
    </div>

    <div class="info-card">
        <h3>🚀 Futuro</h3>
        <p>Em breve: aplicativo mobile, assistente de luto com IA, verificação automática de falecimento e muito mais!</p>
    </div>

    <div class="info-card">
        <h3>📧 Contato</h3>
        <p>Dúvidas ou sugestões? Entre em contato: <strong>contato@aeterenalegado.com.br</strong></p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN
# ============================================================================
def main():
    inject_custom_css()

    if not st.session_state.autenticado:
        render_login()
    else:
        render_sidebar()
        render_app()


if __name__ == "__main__":
    main()