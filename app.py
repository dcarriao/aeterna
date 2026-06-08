import streamlit as st
from PIL import Image
import os
from datetime import datetime
import json
import sqlite3
import secrets
from utils.banco import BancoDados
from utils.criptografia import GerenciadorCriptografia
from utils.usuarios import GerenciadorUsuarios
from utils.upload_video import GerenciadorVideos
from utils.assistente_ia import AssistenteLuto


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

def encontrar_icone_aba():
    icones_possiveis = ["assets/favicon.ico", "assets/favicon-32.png", "assets/icon-192.png", "assets/logo.png",
                        "logo.png"]
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

        /* Layout */
        .main .block-container { padding-top: 0.5rem; padding-bottom: 1rem; }
        .stApp { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%); }

        /* Header */
        .aeterna-header {
            background: linear-gradient(135deg, #90EE90 0%, #2E8B57 50%, #1B5E20 100%);
            padding: 0.8rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .aeterna-header h2 { color: #1B5E20 !important; margin: 0; }

        /* Cards */
        .info-card {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid #2E8B57;
            margin: 0.75rem 0;
        }

        /* Botões */
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

        /* Sidebar */
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #e8f5e9 0%, #f0faf0 100%); }
        .sidebar-logo-container { display: flex; justify-content: center; padding: 20px 0; }
        [data-testid="stSidebar"] img { max-width: 220px !important; background: transparent !important; }

        /* Footer */
        .footer-aeterna { text-align: center; padding: 1rem; color: #808080; font-size: 0.7rem; border-top: 1px solid #d0e8d0; margin-top: 2rem; }

        /* Chat */
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 15px;
            margin-bottom: 1rem;
        }
        .chat-message-user {
            background: #2E8B57;
            color: white;
            padding: 10px 15px;
            border-radius: 20px 20px 5px 20px;
            margin: 10px 0;
            text-align: right;
            max-width: 80%;
            float: right;
            clear: both;
        }
        .chat-message-assistant {
            background: white;
            color: #333;
            padding: 10px 15px;
            border-radius: 20px 20px 20px 5px;
            margin: 10px 0;
            text-align: left;
            max-width: 80%;
            float: left;
            clear: both;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .chat-name-assistant { font-size: 0.7rem; color: #2E8B57; margin-left: 10px; margin-bottom: 2px; }
        .chat-name-user { font-size: 0.7rem; color: #666; margin-right: 10px; text-align: right; }
        .chat-clearfix { clear: both; }

        .ia-warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.75rem;
            margin-bottom: 15px;
        }

        /* ========== CORREÇÃO DAS CORES DOS INPUTS ========== */
        .stTextInput > div > div > input {
            color: #1a1a1a !important;
            background-color: #ffffff !important;
            border: 1px solid #c8e6c8 !important;
            border-radius: 10px !important;
            padding: 12px !important;
            font-size: 16px !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: #888888 !important;
            opacity: 1 !important;
        }

        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: #1B5E20 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            margin-bottom: 5px !important;
        }

        .stTextArea textarea {
            color: #1a1a1a !important;
            background-color: #ffffff !important;
            border: 1px solid #c8e6c8 !important;
            border-radius: 10px !important;
            font-size: 16px !important;
        }

        .stTextArea textarea::placeholder {
            color: #888888 !important;
        }

        .stSelectbox > div > div {
            background-color: #ffffff !important;
            border: 1px solid #c8e6c8 !important;
            border-radius: 10px !important;
        }

        .stFileUploader > div > button {
            background-color: #f0faf0 !important;
            color: #2E8B57 !important;
            border: 1px solid #c8e6c8 !important;
        }

        .stMarkdown h3, .stMarkdown h4 {
            color: #1B5E20 !important;
        }

        hr {
            margin: 20px 0 !important;
            border-color: #d0e8d0 !important;
        }

        @media (max-width: 768px) {
            .chat-message-user, .chat-message-assistant { max-width: 95%; }
            .stTextInput > div > div > input { font-size: 16px !important; padding: 12px !important; }
            .stTextInput label, .stTextArea label { font-size: 0.85rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================
db = BancoDados()
gerente_usuarios = GerenciadorUsuarios()
gerente_videos = GerenciadorVideos()

gerente_usuarios.criar_usuario_admin_inicial()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_atual' not in st.session_state:
    st.session_state.usuario_atual = None
if 'modo_acesso' not in st.session_state:
    st.session_state.modo_acesso = None
if 'falecido_id' not in st.session_state:
    st.session_state.falecido_id = None
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
        st.session_state.modo_acesso = 'falecido'
        st.session_state.falecido_id = usuario['id']
        st.session_state.crypto = GerenciadorCriptografia(senha)
        return True
    return False


def fazer_login_visitante(visitante_nome, chave_acesso, falecido_email):
    conn = sqlite3.connect("dados/cofre.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM usuarios WHERE email = ?", (falecido_email,))
    falecido = cursor.fetchone()
    conn.close()

    if falecido:
        conn = sqlite3.connect("dados/cofre.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM contatos WHERE chave_acesso = ? AND email = ?", (chave_acesso, falecido_email))
        contato = cursor.fetchone()
        conn.close()

        if contato:
            st.session_state.autenticado = True
            st.session_state.modo_acesso = 'visitante'
            st.session_state.falecido_id = falecido[0]
            st.session_state.usuario_atual = {
                'id': None,
                'nome': visitante_nome,
                'tipo': 'visitante',
                'nome_falecido': falecido[1]
            }
            st.session_state.historico_assistente = []
            return True
    return False


def fazer_logout():
    st.session_state.autenticado = False
    st.session_state.usuario_atual = None
    st.session_state.modo_acesso = None
    st.session_state.falecido_id = None
    st.session_state.crypto = None
    st.session_state.historico_assistente = []
    st.rerun()


def fazer_cadastro(nome, email, cpf, senha, telefone="", whatsapp="", foto=None, redes=None):
    resultado = gerente_usuarios.criar_usuario(
        nome=nome,
        email=email,
        cpf=cpf,
        senha=senha,
        tipo='usuario',
        telefone=telefone or "",
        whatsapp=whatsapp or "",
        foto=foto or "",
        redes=redes or "{}"
    )
    return resultado


# ============================================================================
# TELA DE LOGIN
# ============================================================================
def render_login():
    logo = carregar_logo()
    logo_sem_fundo = remover_fundo_branco(logo) if logo else None

    st.markdown('<div class="aeterna-header">', unsafe_allow_html=True)
    if logo_sem_fundo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_sem_fundo, width=180)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔐 Acessar meu Legado", "👋 Acessar Legado de Alguém", "📝 Criar Conta"])

    with tab1:
        st.markdown("### Acesse seu cofre digital")
        with st.form("login_form"):
            st.markdown("**📧 E-mail**")
            email = st.text_input("email", placeholder="seu@email.com", key="login_email", label_visibility="collapsed")
            st.markdown("**🔒 Senha**")
            senha = st.text_input("senha", type="password", placeholder="Sua senha", key="login_senha",
                                  label_visibility="collapsed")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🌿 ENTRAR", use_container_width=True, type="primary")

            if submitted:
                if email and senha:
                    if fazer_login(email, senha):
                        st.success("✅ Login realizado!")
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha incorretos")
                else:
                    st.warning("⚠️ Preencha e-mail e senha")
        st.caption("💡 **Teste:** admin@aeterna.com / admin123")

    with tab2:
        st.markdown("### Acessar legado de alguém especial")
        with st.form("visitante_form"):
            st.markdown("**👤 Seu nome**")
            nome_visitante = st.text_input("nome", placeholder="Seu nome", key="visitante_nome",
                                           label_visibility="collapsed")
            st.markdown("**📧 E-mail da pessoa falecida**")
            email_falecido = st.text_input("email_falecido", placeholder="email@do.falecido.com", key="visitante_email",
                                           label_visibility="collapsed")
            st.markdown("**🔑 Chave de acesso**")
            chave = st.text_input("chave", placeholder="Chave enviada por e-mail", key="visitante_chave",
                                  label_visibility="collapsed", type="password")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🕊️ ACESSAR LEGADO", use_container_width=True, type="primary")

            if submitted:
                if nome_visitante and email_falecido and chave:
                    if fazer_login_visitante(nome_visitante, chave, email_falecido):
                        st.success(f"✅ Bem-vindo(a), {nome_visitante}!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas")
                else:
                    st.warning("⚠️ Preencha todos os campos")
        st.info("💡 Sem chave? Entre em contato com a família.")

    with tab3:
        st.markdown("### ✨ Crie sua conta")
        st.caption("⚠️ CPF é obrigatório")

        with st.form("cadastro_form"):
            st.markdown("**📝 Nome completo**")
            nome = st.text_input("nome", placeholder="Ex: João Silva", key="cadastro_nome",
                                 label_visibility="collapsed")

            st.markdown("**📧 E-mail**")
            email = st.text_input("email_cad", placeholder="seu@email.com", key="cadastro_email",
                                  label_visibility="collapsed")

            st.markdown("**🆔 CPF (apenas números)**")
            cpf = st.text_input("cpf", placeholder="00000000000", key="cadastro_cpf", max_chars=11,
                                label_visibility="collapsed")

            st.markdown("**📱 Telefone**")
            telefone = st.text_input("telefone", placeholder="(11) 99999-9999", key="cadastro_telefone",
                                     label_visibility="collapsed")

            st.markdown("**📱 WhatsApp**")
            whatsapp = st.text_input("whatsapp", placeholder="(11) 99999-9999", key="cadastro_whatsapp",
                                     label_visibility="collapsed")

            st.markdown("**🔒 Senha**")
            senha = st.text_input("senha_cad", type="password", placeholder="Mínimo 6 caracteres", key="cadastro_senha",
                                  label_visibility="collapsed")

            st.markdown("**🔒 Confirmar senha**")
            confirmar_senha = st.text_input("confirmar", type="password", placeholder="Digite a senha novamente",
                                            key="cadastro_confirmar", label_visibility="collapsed")

            st.markdown("---")
            st.markdown("#### ✨ Opcional (pode pular)")
            st.markdown("**📷 Foto de perfil**")
            foto = st.file_uploader("foto", type=["png", "jpg", "jpeg"], key="cadastro_foto",
                                    label_visibility="collapsed")
            st.markdown("**🌐 Redes sociais**")
            redes = st.text_area("redes", placeholder="Instagram: @seuusuario\nLinkedIn: linkedin.com/in/seuusuario",
                                 key="cadastro_redes", label_visibility="collapsed", height=80)

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
                    st.error(f"❌ Preencha: {', '.join(erros)}")
                elif len(cpf) != 11 or not cpf.isdigit():
                    st.error("❌ CPF inválido. Digite apenas 11 números")
                elif senha != confirmar_senha:
                    st.error("❌ As senhas não coincidem")
                elif len(senha) < 6:
                    st.warning("⚠️ A senha deve ter pelo menos 6 caracteres")
                else:
                    resultado = fazer_cadastro(nome, email, cpf, senha, telefone, whatsapp)
                    if resultado == True:
                        st.success("✅ Conta criada! Faça login.")
                        st.balloons()
                        st.rerun()
                    elif resultado == "cpf_existente":
                        st.error("❌ Este CPF já está cadastrado")
                    else:
                        st.error("❌ Este e-mail já está cadastrado")


# ============================================================================
# ASSISTENTE DE LUTO
# ============================================================================
def render_assistente():
    assistente = AssistenteLuto(st.session_state.falecido_id)

    # Buscar nome do falecido
    nome_falecido = "seu ente querido"
    conn = sqlite3.connect("dados/cofre.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (st.session_state.falecido_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        nome_falecido = row[0]

    st.markdown(f"<h3 style='color: #2E8B57;'>🤖 Conversando com {nome_falecido}</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ia-warning">
        💡 <strong>Importante:</strong> Esta é uma conversa gerada por IA baseada na personalidade de <strong>{nome_falecido}</strong>. 
        As respostas são simulações e podem não representar exatamente o que a pessoa pensava. Use com carinho.
    </div>
    """, unsafe_allow_html=True)

    if "historico_assistente" not in st.session_state:
        st.session_state.historico_assistente = []

    chat_container = st.container()

    with chat_container:
        st.markdown('<div class="chat-container" id="chat">', unsafe_allow_html=True)

        if not st.session_state.historico_assistente:
            msg_inicial = f"Olá! Esta é uma conversa simulada baseada em como {nome_falecido} era. Pode me perguntar qualquer coisa."
            st.markdown(f'<div class="chat-name-assistant">{nome_falecido}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-message-assistant">{msg_inicial}</div>', unsafe_allow_html=True)
            st.markdown('<div class="chat-clearfix"></div>', unsafe_allow_html=True)
            st.session_state.historico_assistente.append({"tipo": "assistente", "texto": msg_inicial})

        for msg in st.session_state.historico_assistente:
            if msg["tipo"] == "usuario":
                st.markdown(f'<div class="chat-name-user">Você</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-message-user">{msg["texto"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-name-assistant">{nome_falecido}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-message-assistant">{msg["texto"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="chat-clearfix"></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        mensagem = st.text_input("Sua mensagem:", key="msg_assistente",
                                 placeholder=f"Escreva sua mensagem para {nome_falecido}...",
                                 label_visibility="collapsed")
    with col2:
        enviar = st.button("📨 Enviar", key="btn_enviar", type="primary", use_container_width=True)

    if enviar and mensagem:
        st.session_state.historico_assistente.append({"tipo": "usuario", "texto": mensagem})
        with st.spinner(f"{nome_falecido} está pensando..."):
            resposta = assistente.conversar(mensagem)
        st.session_state.historico_assistente.append({"tipo": "assistente", "texto": resposta})
        st.rerun()


# ============================================================================
# VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h3 style='color: #2E8B57;'>📹 Mensagens em Vídeo</h3>", unsafe_allow_html=True)
    st.info("💡 Cada vídeo pode ser direcionado para uma pessoa específica.")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("🎥 Adicionar vídeo", expanded=False):
            titulo = st.text_input("Título *", key="titulo_video_input")
            destinatario = st.text_input("Para quem é este vídeo?", key="destinatario_video",
                                         placeholder="Ex: Para minha filha Ana")
            arquivo_video = st.file_uploader("Arquivo de vídeo", type=["mp4", "mov", "avi", "mkv"], key="video_file")
            st.caption("📹 Formatos aceitos: MP4, MOV, AVI, MKV")

            if st.button("💾 Salvar", key="btn_salvar_video", type="primary", use_container_width=True):
                if titulo and arquivo_video:
                    caminho = gerente_videos.salvar_video(
                        arquivo_video,
                        st.session_state.usuario_atual['id'],
                        titulo,
                        destinatario
                    )
                    st.success(f"✅ {titulo} salvo para {destinatario or 'todos'}")
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
                    st.video(video['caminho'])
                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        if gerente_videos.deletar_video(video['id'], st.session_state.usuario_atual['id']):
                            st.rerun()


# ============================================================================
# CONTATOS
# ============================================================================
def render_contatos_falecido():
    st.markdown("<h3 style='color: #2E8B57;'>👥 Contatos que receberão seu legado</h3>", unsafe_allow_html=True)
    st.info("💡 Adicione até 3 pessoas. Cada uma receberá uma chave de acesso.")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Adicionar contato", expanded=False):
            nome = st.text_input("Nome completo *", key="contato_nome")
            email = st.text_input("E-mail *", key="contato_email")
            telefone = st.text_input("Telefone", key="contato_telefone")
            whatsapp = st.text_input("WhatsApp", key="contato_whatsapp")
            prioridade = st.selectbox("Prioridade", [1, 2, 3], key="contato_prioridade")

            if st.button("💾 Salvar", type="primary", use_container_width=True):
                if nome and email:
                    chave_acesso = secrets.token_hex(8)
                    db.adicionar_contato(nome, email, telefone, whatsapp, f"Prioridade: {prioridade}", chave_acesso)
                    st.success(f"✅ {nome} adicionado!")
                    st.info(f"🔑 Chave de acesso para {nome}: `{chave_acesso}`")
                    st.warning(
                        "📌 Guarde esta chave e envie para a pessoa. Ela será necessária para acessar seu legado.")
                    st.rerun()
                else:
                    st.error("❌ Preencha nome e e-mail")

    with col2:
        contatos = db.listar_contatos()
        if not contatos:
            st.info("📭 Nenhum contato cadastrado.")
        else:
            for i, contato in enumerate(contatos):
                st.markdown(f"""
                <div class="info-card" style="padding: 0.75rem;">
                    <strong>{i + 1}º - 👤 {contato['nome']}</strong><br>
                    📧 {contato['email']}<br>
                    📱 {contato['telefone'] or 'Não informado'}<br>
                    🏷️ {contato['papel']}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ Remover {contato['nome']}", key=f"del_contato_{contato['id']}"):
                    db.deletar_contato(contato['id'])
                    st.rerun()


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
    </div>

    <div class="info-card">
        <h3>🔒 Segurança e LGPD</h3>
        <p>✅ Criptografia de ponta a ponta (Fernet + PBKDF2)<br>
        ✅ Seus dados, sua chave - nem nós acessamos<br>
        ✅ 100% compatível com a Lei Geral de Proteção de Dados<br>
        ✅ Você pode solicitar exclusão a qualquer momento</p>
    </div>

    <div class="info-card">
        <h3>🚀 Roadmap</h3>
        <p>✅ App funcional (senhas, vídeos, contatos, assistente IA)<br>
        🔄 App mobile (Android/iOS) - em desenvolvimento<br>
        🔄 API de validação de CPF - em desenvolvimento<br>
        🔄 Mural da Memória - em planejamento</p>
    </div>

    <div class="info-card">
        <h3>💼 Para Investidores e Parceiros</h3>
        <p>Estamos abertos a:</p>
        <ul>
            <li>💎 Investimento anjo</li>
            <li>🤝 Parcerias com planos funerários</li>
            <li>🏦 Parcerias com seguros de vida</li>
            <li>📜 Licenciamento da tecnologia</li>
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
        logo = carregar_logo()
        if logo:
            with st.sidebar:
                st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
                st.image(logo, width=180)
                st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.modo_acesso == 'falecido':
            with st.sidebar:
                st.markdown(f"### ✨ Olá, {st.session_state.usuario_atual['nome']}!")
                if st.button("🚪 Sair", use_container_width=True):
                    fazer_logout()
                st.markdown("---")
                st.markdown("### 📊 Seu Legado")
                videos = gerente_videos.listar_videos_usuario(st.session_state.usuario_atual['id'])
                contatos = db.listar_contatos()
                st.metric("📹 Vídeos", len(videos))
                st.metric("👥 Contatos", len(contatos))

            tab1, tab2, tab3, tab4 = st.tabs(["🤖 Assistente de Luto", "📹 Meus Vídeos", "👥 Meus Contatos", "ℹ️ Sobre"])
            with tab1:
                render_assistente()
            with tab2:
                render_videos()
            with tab3:
                render_contatos_falecido()
            with tab4:
                render_sobre()
        else:
            with st.sidebar:
                nome_falecido = st.session_state.usuario_atual.get('nome_falecido', 'seu ente querido')
                st.markdown(f"### 🕊️ Em memória de")
                st.markdown(f"### {nome_falecido}")
                if st.button("🚪 Sair", use_container_width=True):
                    fazer_logout()

            render_assistente()

            st.markdown("---")
            st.markdown("""
            <div class="info-card" style="text-align: center;">
                <h3>💚 Gostou da experiência?</h3>
                <p>Você também pode criar seu próprio legado digital e eternizar sua memória para quem você ama.</p>
            </div>
            """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📝 Criar minha conta aEterna", use_container_width=True, type="primary"):
                    st.session_state.autenticado = False
                    st.rerun()

        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna - Seu legado, sua história, sua vida. ✨</p>
            <p style="font-size: 0.6rem;">Versão 2.0 | Assistente de Luto com IA | LGPD Compliant</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()