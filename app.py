import streamlit as st
from PIL import Image
import os
from datetime import datetime
import json
from utils.banco import BancoDados
from utils.criptografia import GerenciadorCriptografia
from utils.usuarios import GerenciadorUsuarios
from utils.upload_video import GerenciadorVideos


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

def encontrar_icone_aba():
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
    logo_paths = ["assets/logo.png", "assets/icon-512.png", "logo.png"]
    for path in logo_paths:
        if os.path.exists(path):
            try:
                return Image.open(path)
            except:
                continue
    return None


def remover_fundo_branco(imagem):
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
    st.markdown("""
    <style>
        /* Remover botão de deploy */
        .stDeployButton { display: none !important; }
        header[data-testid="stHeader"] { background: transparent !important; }
        .stApp > header { display: none !important; }

        /* Layout compacto */
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
        }

        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
        }

        /* FONTES MENORES */
        .main .block-container {
            font-size: 0.85rem;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 0.8rem;
            padding: 0.3rem 0.6rem;
        }

        .info-card h3 {
            font-size: 0.9rem;
        }

        .info-card p {
            font-size: 0.75rem;
        }

        /* Header com texto verde escuro */
        .aeterna-header {
            background: linear-gradient(135deg, #90EE90 0%, #2E8B57 50%, #1B5E20 100%);
            padding: 0.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .aeterna-header h2 {
            color: #1B5E20 !important;
            margin: 0;
        }

        .aeterna-header p {
            color: rgba(255,255,255,0.9) !important;
            margin: 0;
        }

        .info-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0faf0 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid #2E8B57;
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

        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #c8e6c8;
        }

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

        /* Melhorias para mobile - tela de cadastro */
        @media (max-width: 768px) {
            .stTextInput > div > div > input {
                font-size: 16px !important;
                padding: 12px !important;
                min-height: 48px !important;
            }

            .stButton > button {
                min-height: 48px !important;
                font-size: 16px !important;
            }

            .stMarkdown h3 {
                font-size: 1.3rem !important;
            }

            .stTextInput {
                margin-bottom: 15px !important;
            }

            .stTextArea textarea {
                font-size: 16px !important;
                min-height: 80px !important;
            }

            .block-container {
                padding-left: 15px !important;
                padding-right: 15px !important;
            }

            hr {
                margin: 20px 0 !important;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 8px !important;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 10px 16px !important;
                font-size: 14px !important;
            }
        }

        /* Cards mais limpos para mobile */
        .info-card {
            background: white !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin: 12px 0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        }

        .stTextInput > div > div > input {
            border: 1px solid #ddd !important;
            border-radius: 10px !important;
            background: white !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #2E8B57 !important;
            box-shadow: 0 0 0 2px rgba(46,139,87,0.1) !important;
        }

        .stTextArea textarea {
            border: 1px solid #ddd !important;
            border-radius: 10px !important;
        }

        .stTextArea textarea:focus {
            border-color: #2E8B57 !important;
        }

        /* Chat do assistente */
        .chat-message-user {
            background: #e8f5e9;
            padding: 12px;
            border-radius: 15px;
            margin: 8px 0;
            text-align: right;
        }

        .chat-message-assistant {
            background: #f0faf0;
            padding: 12px;
            border-radius: 15px;
            margin: 8px 0;
            border-left: 3px solid #2E8B57;
        }

        /* Mensagem diária */
        .daily-message {
            background: linear-gradient(135deg, #2E8B57 0%, #1B5E20 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-style: italic;
            margin: 20px 0;
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
gerente_videos = GerenciadorVideos()

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
if 'historico_assistente' not in st.session_state:
    st.session_state.historico_assistente = []


# ============================================================================
# FUNÇÕES DE AUTENTICAÇÃO
# ============================================================================
def fazer_login(email, senha):
    usuario = gerente_usuarios.autenticar(email, senha)
    if usuario:
        st.session_state.usuario_atual = usuario
        st.session_state.autenticado = True
        st.session_state.pagina = 'app'
        st.session_state.crypto = GerenciadorCriptografia(senha)
        return True
    return False


def fazer_logout():
    st.session_state.autenticado = False
    st.session_state.usuario_atual = None
    st.session_state.pagina = 'login'
    st.session_state.crypto = None
    st.session_state.historico_assistente = []
    st.rerun()


def fazer_cadastro(nome, email, cpf, senha, foto=None, redes=None):
    return gerente_usuarios.criar_usuario(nome, email, cpf, senha, 'usuario', foto or '', redes or '{}')


# ============================================================================
# TELA DE LOGIN E CADASTRO - VERSÃO OTIMIZADA PARA MOBILE
# ============================================================================
def render_login():
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    st.markdown('<div class="aeterna-header" style="padding: 0.8rem;">', unsafe_allow_html=True)
    if logo_sem_fundo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_sem_fundo, width=180)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 **ENTRAR**", "📝 **CRIAR CONTA**"])

    with tab1:
        st.markdown("### Bem-vindo de volta!")

        with st.form("login_form"):
            email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
            senha = st.text_input("Senha", type="password", placeholder="••••••••", key="login_senha")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🌿 ENTRAR", use_container_width=True, type="primary")

            if submitted:
                if email and senha:
                    if fazer_login(email, senha):
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha incorretos")
                else:
                    st.warning("⚠️ Preencha e-mail e senha")

        st.caption("💡 **Teste:** admin@aeterna.com / admin123")

    with tab2:
        st.markdown("### ✨ Crie sua conta")
        st.caption("⚠️ O CPF é obrigatório e será usado para validação futura")

        with st.form("cadastro_form"):
            st.markdown("**📝 Nome completo**")
            nome = st.text_input("Nome", placeholder="Ex: João Silva", key="cadastro_nome",
                                 label_visibility="collapsed")

            st.markdown("**📧 E-mail**")
            email = st.text_input("E-mail", placeholder="seu@email.com", key="cadastro_email",
                                  label_visibility="collapsed")

            st.markdown("**🆔 CPF (apenas números)**")
            cpf = st.text_input("CPF", placeholder="00000000000", key="cadastro_cpf", max_chars=11,
                                label_visibility="collapsed")

            st.markdown("**🔒 Senha**")
            senha = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres", key="cadastro_senha",
                                  label_visibility="collapsed")

            st.markdown("**🔒 Confirmar senha**")
            confirmar_senha = st.text_input("Confirmar", type="password", placeholder="Digite a senha novamente",
                                            key="cadastro_confirmar", label_visibility="collapsed")

            st.markdown("---")
            st.markdown("#### ✨ Opcional (pode pular)")

            st.markdown("**📷 Foto de perfil**")
            foto = st.file_uploader("Foto", type=["png", "jpg", "jpeg"], key="cadastro_foto",
                                    label_visibility="collapsed")

            st.markdown("**🌐 Redes sociais**")
            redes = st.text_area("Redes", placeholder="Instagram: @seuusuario\nLinkedIn: linkedin.com/in/seuusuario",
                                 key="cadastro_redes", label_visibility="collapsed", height=80)

            st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("📝 CRIAR CONTA", use_container_width=True, type="primary")

            if submitted:
                erros = []
                if not nome: erros.append("Nome")
                if not email: erros.append("E-mail")
                if not cpf: erros.append("CPF")
                if not senha: erros.append("Senha")

                if erros:
                    st.error(f"❌ Preencha os campos obrigatórios: {', '.join(erros)}")
                elif len(cpf) != 11 or not cpf.isdigit():
                    st.error("❌ CPF inválido. Digite apenas 11 números")
                elif senha != confirmar_senha:
                    st.error("❌ As senhas não coincidem")
                elif len(senha) < 6:
                    st.warning("⚠️ A senha deve ter pelo menos 6 caracteres")
                else:
                    resultado = fazer_cadastro(nome, email, cpf, senha)
                    if resultado == True:
                        st.success("✅ Conta criada com sucesso! Faça login para continuar.")
                        st.balloons()
                        st.rerun()
                    elif resultado == "cpf_existente":
                        st.error("❌ Este CPF já está cadastrado")
                    else:
                        st.error("❌ Este e-mail já está cadastrado")


# ============================================================================
# SIDEBAR
# ============================================================================
def render_sidebar():
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    with st.sidebar:
        if logo_sem_fundo:
            st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
            st.image(logo_sem_fundo, width=220)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"### ✨ Olá, **{st.session_state.usuario_atual['nome']}**!")
        st.caption(f"📧 {st.session_state.usuario_atual['email']}")

        if st.button("🚪 Sair", use_container_width=True):
            fazer_logout()

        st.markdown("---")
        st.markdown("### 📊 Seu Cofre")
        senhas = db.listar_senhas()
        videos = gerente_videos.listar_videos_usuario(st.session_state.usuario_atual['id'])
        contatos = db.listar_contatos()

        st.metric("🔐 Senhas", len(senhas))
        st.metric("📹 Vídeos", len(videos))
        st.metric("👥 Contatos", len(contatos))


# ============================================================================
# TELA PRINCIPAL
# ============================================================================
def render_app():
    st.markdown('<div class="aeterna-header">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Bem-vindo, {st.session_state.usuario_atual['nome']}!</h2>",
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">Gerencie seu legado digital com segurança</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Verificar se o usuário configurou o assistente
    from utils.assistente_ia import AssistenteLuto
    assistente_temp = AssistenteLuto(st.session_state.usuario_atual['id'])
    stats = assistente_temp.estatisticas()
    tem_assistente = stats.get("perguntas_respondidas", 0) > 0

    # Abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔐 Senhas",
        "📹 Vídeos",
        "👥 Contatos",
        "🤖 Assistente de Luto" + (" ✅" if tem_assistente else ""),
        "ℹ️ Sobre"
    ])

    with tab1:
        render_senhas()
    with tab2:
        render_videos()
    with tab3:
        render_contatos()
    with tab4:
        render_assistente()
    with tab5:
        render_sobre()


# ============================================================================
# SENHAS
# ============================================================================
def render_senhas():
    st.markdown("<h3 style='color: #2E8B57;'>🔐 Gerenciamento de Senhas</h3>", unsafe_allow_html=True)
    st.info(
        "💡 **Opcional:** Você pode usar o cofre para guardar suas senhas ou apenas para indicar onde elas estão. A escolha é sua.")

    col1, col2 = st.columns([2, 1])

    with col2:
        with st.expander("➕ Adicionar nova senha", expanded=False):
            servico = st.text_input("Serviço/App *", key="servico_input")
            usuario = st.text_input("Usuário/E-mail *", key="usuario_input")
            senha_original = st.text_input("Senha *", type="password", key="senha_input")
            url = st.text_input("URL", key="url_input")
            notas = st.text_area("Notas", key="notas_input", height=80,
                                 placeholder="Onde esta senha está salva? Observações importantes?")

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
    st.markdown("<h3 style='color: #2E8B57;'>📹 Mensagens em Vídeo</h3>", unsafe_allow_html=True)
    st.info("💡 Grave vídeos com suas palavras, conselhos e lembranças. Eles ficarão salvos em nosso servidor seguro.")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("🎥 Adicionar vídeo", expanded=False):
            titulo = st.text_input("Título *", key="titulo_video_input")
            destinatario = st.text_input("Para", key="destinatario_video", placeholder="Ex: Para minha filha Ana")
            arquivo_video = st.file_uploader("Arquivo de vídeo", type=["mp4", "mov", "avi", "mkv"], key="video_file")
            st.caption("📹 Formatos aceitos: MP4, MOV, AVI, MKV | Tamanho máximo: 200MB")

            if st.button("💾 Salvar", key="btn_salvar_video", type="primary", use_container_width=True):
                if titulo and arquivo_video:
                    caminho = gerente_videos.salvar_video(
                        arquivo_video,
                        st.session_state.usuario_atual['id'],
                        titulo,
                        destinatario
                    )
                    st.success(f"✅ {titulo} salvo com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Preencha o título e selecione um vídeo")

    with col2:
        videos = gerente_videos.listar_videos_usuario(st.session_state.usuario_atual['id'])

        if not videos:
            st.info("📭 Nenhum vídeo cadastrado")
        else:
            for video in videos:
                with st.expander(f"🎬 {video['titulo']}"):
                    if video['destinatario']:
                        st.markdown(f"**👥 Para:** {video['destinatario']}")
                    st.markdown(f"**📅 Data:** {video['data'][:19] if video['data'] else 'Não informada'}")
                    st.video(video['caminho'])
                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        if gerente_videos.deletar_video(video['id'], st.session_state.usuario_atual['id']):
                            st.rerun()


# ============================================================================
# CONTATOS
# ============================================================================
def render_contatos():
    st.markdown("<h3 style='color: #2E8B57;'>👥 Contatos de Confiança</h3>", unsafe_allow_html=True)
    st.info("💡 Indique até 3 pessoas que receberão seu legado. A ordem define a prioridade.")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Adicionar contato", expanded=False):
            nome_contato = st.text_input("Nome *", key="nome_contato_input")
            email_contato = st.text_input("E-mail *", key="email_contato_input")
            telefone_contato = st.text_input("Telefone", key="telefone_contato")
            papel_contato = st.selectbox("Papel",
                                         ["Filho(a)", "Cônjuge", "Irmão(ã)", "Amigo(a)", "Advogado(a)", "Outro"],
                                         key="papel_contato")
            prioridade = st.selectbox("Prioridade", [1, 2, 3], key="prioridade_contato")

            if st.button("💾 Salvar", key="btn_salvar_contato", type="primary", use_container_width=True):
                if nome_contato and email_contato:
                    db.adicionar_contato(nome_contato, email_contato, telefone_contato, papel_contato,
                                         f"Prioridade: {prioridade}")
                    st.success(f"✅ {nome_contato} adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Preencha nome e e-mail")

    with col2:
        contatos = db.listar_contatos()

        if not contatos:
            st.info("📭 Nenhum contato cadastrado")
        else:
            for i, contato in enumerate(contatos):
                st.markdown(f"""
                <div class="info-card" style="padding: 0.75rem;">
                    <strong>{i + 1}º - 👤 {contato['nome']}</strong><br>
                    📧 {contato['email']}<br>
                    🏷️ {contato['papel']}
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑️ Remover {contato['nome']}", key=f"del_contato_{contato['id']}"):
                    db.deletar_contato(contato['id'])
                    st.rerun()

        st.markdown("""
        <div class="info-card" style="padding: 0.75rem; font-size: 0.8rem; background: #fff3e0;">
            <strong>📌 Como funciona:</strong><br>
            A liberação será feita automaticamente via API de validação de CPF (em desenvolvimento).<br>
            Quando confirmado o falecimento, o primeiro contato da lista receberá todas as orientações.
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# ASSISTENTE DE LUTO
# ============================================================================
def render_assistente():
    from utils.assistente_ia import AssistenteLuto
    from utils.personalidade import renderizar_captura_personalidade, PERGUNTAS_PERSONALIDADE

    st.markdown("<h3 style='color: #2E8B57;'>🤖 Assistente de Luto</h3>", unsafe_allow_html=True)

    # Verificar se o assistente já foi configurado
    assistente = AssistenteLuto(st.session_state.usuario_atual['id'])
    stats = assistente.estatisticas()

    # Mensagem diária (se já configurado)
    if stats.get("perguntas_respondidas", 0) > 0:
        with st.expander("💝 Mensagem de Conforto do Dia", expanded=False):
            mensagem = assistente.gerar_mensagem_diaria()
            st.markdown(f'<div class="daily-message">{mensagem}</div>', unsafe_allow_html=True)

    if stats["perguntas_respondidas"] == 0:
        # Primeira vez: capturar personalidade
        st.info("✨ **Vamos te conhecer melhor!** ✨")
        st.markdown("""
        Responda às perguntas abaixo para que o Assistente de Luto possa 
        conversar com seus entes queridos como se fosse você.

        Não se preocupe, você pode editar suas respostas depois.
        """)

        respostas = renderizar_captura_personalidade()

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 Salvar Personalidade", type="primary", use_container_width=True):
                if any(respostas.values()):
                    assistente.capturar_personalidade(respostas)
                    st.success("✅ Personalidade salva com sucesso!")
                    st.rerun()
                else:
                    st.warning("⚠️ Responda pelo menos uma pergunta para continuar.")
    else:
        # Assistente já configurado
        st.success(f"✅ Assistente configurado com {stats['perguntas_respondidas']} respostas")

        # Abas: Conversar, Ajustes, Estatísticas
        tab1, tab2, tab3 = st.tabs(["💬 Conversar", "✏️ Ajustar Personalidade", "📊 Estatísticas"])

        with tab1:
            st.markdown("### 💬 Converse com seu ente querido")
            st.markdown("""
            Simule uma conversa com a pessoa que partiu. As respostas são geradas 
            baseadas na personalidade e memórias que ela deixou.
            """)

            # Inicializar histórico de conversa na sessão
            if "historico_assistente" not in st.session_state:
                st.session_state.historico_assistente = []

            # Exibir histórico
            for msg in st.session_state.historico_assistente:
                if msg["tipo"] == "usuario":
                    st.markdown(f'<div class="chat-message-user"><strong>Você:</strong><br>{msg["texto"]}</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="chat-message-assistant"><strong>🤖 Assistente:</strong><br>{msg["texto"]}</div>',
                        unsafe_allow_html=True)

            # Input de mensagem
            mensagem = st.text_area("Sua mensagem:", key="msg_assistente", height=100,
                                    placeholder="Escreva sua mensagem aqui...")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📨 Enviar", type="primary", use_container_width=True):
                    if mensagem:
                        st.session_state.historico_assistente.append({"tipo": "usuario", "texto": mensagem})

                        with st.spinner("✨ Pensando..."):
                            resposta = assistente.conversar(mensagem)

                        st.session_state.historico_assistente.append({"tipo": "assistente", "texto": resposta})
                        st.rerun()

            with col2:
                if st.button("🗑️ Limpar Conversa", use_container_width=True):
                    st.session_state.historico_assistente = []
                    st.rerun()

        with tab2:
            st.markdown("### ✏️ Ajustar Personalidade")
            st.markdown("Você pode editar suas respostas a qualquer momento.")

            # Carregar respostas atuais
            import sqlite3
            conn = sqlite3.connect("dados/cofre.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pergunta, resposta FROM personalidade 
                WHERE usuario_id = ? ORDER BY id
            ''', (st.session_state.usuario_atual['id'],))

            respostas_atuais = dict(cursor.fetchall())
            conn.close()

            respostas_editadas = {}

            for key, pergunta in PERGUNTAS_PERSONALIDADE.items():
                valor_atual = respostas_atuais.get(pergunta, "")
                nova_resposta = st.text_area(
                    pergunta,
                    value=valor_atual,
                    key=f"edit_{key}",
                    height=80
                )
                if nova_resposta != valor_atual:
                    respostas_editadas[pergunta] = nova_resposta

            if respostas_editadas:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
                        conn = sqlite3.connect("dados/cofre.db")
                        cursor = conn.cursor()
                        for pergunta, resposta in respostas_editadas.items():
                            cursor.execute('''
                                UPDATE personalidade SET resposta = ? 
                                WHERE usuario_id = ? AND pergunta = ?
                            ''', (resposta, st.session_state.usuario_atual['id'], pergunta))
                        conn.commit()
                        conn.close()

                        assistente._gerar_embedding_personalidade(respostas_editadas)
                        st.success("✅ Personalidade atualizada!")
                        st.rerun()
            else:
                st.info("Nenhuma alteração detectada. Edite alguma resposta para salvar.")

        with tab3:
            st.markdown("### 📊 Estatísticas do Assistente")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📝 Perguntas", stats.get("perguntas_respondidas", 0))
            with col2:
                st.metric("💾 Memórias", stats.get("memorias_armazenadas", 0))
            with col3:
                status_ia = "✅ Ativo" if stats.get("ia_disponivel", False) else "⚠️ Local"
                st.metric("🧠 IA", status_ia)

            st.markdown("---")
            st.markdown("#### 📌 Sobre o Assistente")
            st.markdown("""
            O Assistente de Luto utiliza:
            - **Embeddings semânticos** para entender o contexto
            - **Memórias vetorizadas** para buscas relevantes
            - **IA generativa** (Gemini) para respostas naturais

            Quanto mais informações você fornecer, mais personalizadas serão as respostas.
            """)

            if not stats.get("ia_disponivel", False):
                st.warning("""
                ⚠️ **IA Avançada não configurada**

                Para ativar respostas mais naturais, configure a API Key do Google Gemini:
                1. Acesse: https://aistudio.google.com/app/apikey
                2. Crie uma API key gratuita
                3. Adicione como segredo no Streamlit Cloud: `GEMINI_API_KEY`
                """)


# ============================================================================
# SOBRE
# ============================================================================
def render_sobre():
    st.markdown("<h3 style='color: #2E8B57;'>✨ Sobre o aEterna</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>🌿 O que é o aEterna?</h3>
        <p>O aEterna é uma plataforma de legado digital que permite você guardar suas senhas, 
        mensagens em vídeo e contatos de confiança em um único lugar seguro.</p>
        <p><strong>O cofre é opcional:</strong> Você pode usar apenas para indicar onde estão suas coisas, sem armazenar senhas.</p>
    </div>

    <div class="info-card">
        <h3>🤖 Assistente de Luto</h3>
        <p>Nossa tecnologia mais especial: uma IA treinada com sua personalidade, mensagens e memórias 
        para conversar com seus entes queridos e oferecer conforto após sua partida.</p>
        <p>💡 <strong>Como funciona:</strong> Você responde perguntas sobre sua vida, valores e conselhos. 
        O sistema aprende sua essência e pode interagir como você faria.</p>
    </div>

    <div class="info-card">
        <h3>🚀 Roadmap</h3>
        <p>✅ App funcional (senhas, vídeos, contatos)<br>
        ✅ Assistente de Luto (versão inicial)<br>
        🔄 App mobile (Android/iOS) - em desenvolvimento<br>
        🔄 API de validação de CPF - em desenvolvimento<br>
        🔄 Transcrição automática de vídeos - em breve<br>
        🔄 Mural da Memória - em planejamento</p>
    </div>

    <div class="info-card">
        <h3>💼 Para Investidores e Parceiros</h3>
        <p>Estamos abertos a:</p>
        <ul>
            <li>Investimento anjo</li>
            <li>Parcerias com planos funerários</li>
            <li>Parcerias com seguros de vida</li>
            <li>Licenciamento da tecnologia</li>
        </ul>
        <p>📧 Contato: <strong>parcerias@aeterenalegado.com.br</strong></p>
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

        # Rodapé SEM CRUZ
        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna - Seu legado, sua história, sua vida. ✨</p>
            <p style="font-size: 0.6rem;">Versão 2.0 | Com Assistente de Luto</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()