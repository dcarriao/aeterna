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
import os
from reset_banco import resetar_banco


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
        .stDeployButton { display: none !important; }
        header[data-testid="stHeader"] { background: transparent !important; }
        .stApp > header { display: none !important; }

        .main .block-container { padding-top: 0.5rem; padding-bottom: 1rem; }
        .stApp { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%); }

        .aeterna-header {
            background: linear-gradient(135deg, #90EE90 0%, #2E8B57 50%, #1B5E20 100%);
            padding: 0.8rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .aeterna-header h2 { color: #1B5E20 !important; margin: 0; }

        .info-card {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid #2E8B57;
            margin: 0.75rem 0;
        }

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

        [data-testid="stSidebar"] { background: linear-gradient(180deg, #e8f5e9 0%, #f0faf0 100%); }
        .sidebar-logo-container { display: flex; justify-content: center; padding: 20px 0; }
        [data-testid="stSidebar"] img { max-width: 220px !important; background: transparent !important; }

        .footer-aeterna { text-align: center; padding: 1rem; color: #808080; font-size: 0.7rem; border-top: 1px solid #d0e8d0; margin-top: 2rem; }

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

# ============================================================================
# INICIALIZAÇÃO NORMAL
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
        gerente_usuarios.atualizar_ultimo_acesso(usuario['id'])
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


def fazer_cadastro(nome, sobrenome, email, cpf, data_nascimento, senha,
                   telefone="", whatsapp="", foto=None, redes=None):
    resultado = gerente_usuarios.criar_usuario(
        nome=nome,
        sobrenome=sobrenome,
        email=email,
        cpf=cpf,
        data_nascimento=data_nascimento,
        senha=senha,
        telefone=telefone,
        whatsapp=whatsapp,
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

    tab1, tab2 = st.tabs(["🔐 ENTRAR", "📝 CRIAR CONTA"])

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

    with tab2:
        st.markdown("### ✨ Crie sua conta")
        st.caption("⚠️ CPF e data de nascimento são obrigatórios")

        with st.form("cadastro_form"):
            st.markdown("**📝 Nome completo ***")
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("nome", placeholder="Nome", key="cadastro_nome", label_visibility="collapsed")
            with col2:
                sobrenome = st.text_input("sobrenome", placeholder="Sobrenome", key="cadastro_sobrenome",
                                          label_visibility="collapsed")

            st.markdown("**📧 E-mail ***")
            email = st.text_input("email_cad", placeholder="seu@email.com", key="cadastro_email",
                                  label_visibility="collapsed")

            st.markdown("**🆔 CPF (apenas números) ***")
            cpf = st.text_input("cpf", placeholder="00000000000", key="cadastro_cpf", max_chars=11,
                                label_visibility="collapsed")

            st.markdown("**🎂 Data de nascimento ***")
            data_nascimento = st.date_input("data_nascimento", key="cadastro_data_nascimento",
                                            label_visibility="collapsed", value=None)

            st.markdown("**📱 Telefone**")
            telefone = st.text_input("telefone", placeholder="(11) 99999-9999", key="cadastro_telefone",
                                     label_visibility="collapsed")

            st.markdown("**📱 WhatsApp**")
            whatsapp = st.text_input("whatsapp", placeholder="(11) 99999-9999", key="cadastro_whatsapp",
                                     label_visibility="collapsed")

            st.markdown("**🔒 Senha ***")
            senha = st.text_input("senha_cad", type="password", placeholder="Mínimo 6 caracteres", key="cadastro_senha",
                                  label_visibility="collapsed")

            st.markdown("**🔒 Confirmar senha ***")
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
                if not sobrenome: erros.append("Sobrenome")
                if not email: erros.append("E-mail")
                if not cpf: erros.append("CPF")
                if not data_nascimento: erros.append("Data de nascimento")
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
                    resultado = fazer_cadastro(
                        nome=nome,
                        sobrenome=sobrenome,
                        email=email,
                        cpf=cpf,
                        data_nascimento=data_nascimento.strftime("%Y-%m-%d"),
                        senha=senha,
                        telefone=telefone,
                        whatsapp=whatsapp
                    )
                    if resultado == True:
                        st.success("✅ Conta criada! Faça login.")
                        st.balloons()
                        st.rerun()
                    elif resultado == "cpf_existente":
                        st.error("❌ Este CPF já está cadastrado")
                    elif resultado == "email_existente":
                        st.error("❌ Este e-mail já está cadastrado")
                    else:
                        st.error("❌ Erro ao criar conta. Verifique os dados.")


# ============================================================================
# ASSISTENTE DE LUTO
# ============================================================================
def render_assistente():
    """Renderiza o assistente de luto como um chat funcional"""

    # Verificar se o assistente já foi criado
    if 'assistente_obj' not in st.session_state:
        st.session_state.assistente_obj = AssistenteLuto(st.session_state.falecido_id)

    assistente = st.session_state.assistente_obj
    nome_falecido = st.session_state.usuario_atual.get('nome_completo', 'seu ente querido')

    # CSS para o chat
    st.markdown("""
    <style>
        .chat-container {
            background: #e5ddd5;
            border-radius: 12px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            margin-bottom: 15px;
        }

        .message-row {
            display: flex;
            margin-bottom: 12px;
        }

        .message-row.user {
            justify-content: flex-end;
        }

        .message-row.bot {
            justify-content: flex-start;
        }

        .message-bubble {
            max-width: 70%;
            padding: 10px 14px;
            border-radius: 18px;
            font-size: 0.85rem;
            word-wrap: break-word;
        }

        .message-bubble.user {
            background: #dcf8c5;
            color: #075e54;
            border-bottom-right-radius: 4px;
        }

        .message-bubble.bot {
            background: white;
            color: #1a1a1a;
            border-bottom-left-radius: 4px;
            box-shadow: 0 1px 1px rgba(0,0,0,0.05);
        }

        .chat-warning {
            background: #fff3cd;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.7rem;
            color: #856404;
            margin-bottom: 15px;
            text-align: center;
        }

        .chat-input-area {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }

        /* Esconder o botão de submit padrão do Streamlit */
        .stButton button[key="btn_enviar"] {
            background-color: #128C7E;
        }
    </style>
    """, unsafe_allow_html=True)

    # Aviso
    st.markdown(f"""
    <div class="chat-warning">
        💡 Esta é uma conversa gerada por IA baseada na personalidade de <strong>{nome_falecido}</strong>. 
        As respostas são simulações. Use com carinho.
    </div>
    """, unsafe_allow_html=True)

    # Inicializar histórico no session state se não existir
    if 'historico_assistente' not in st.session_state:
        st.session_state.historico_assistente = []

    if not st.session_state.historico_assistente:
        msg_inicial = f"Olá! Sou uma simulação baseada em como {nome_falecido} era. Pode me perguntar qualquer coisa. 💚"
        st.session_state.historico_assistente.append({"tipo": "bot", "texto": msg_inicial})

    # Exibir mensagens
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.historico_assistente:
        if msg["tipo"] == "user":
            st.markdown(f"""
            <div class="message-row user">
                <div class="message-bubble user">
                    {msg["texto"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-row bot">
                <div class="message-bubble bot">
                    <strong>{nome_falecido}:</strong><br>{msg["texto"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Usar um formulário para evitar reload completo
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            mensagem = st.text_input("msg", key="nova_mensagem",
                                     placeholder="Digite sua mensagem...",
                                     label_visibility="collapsed")

        with col2:
            enviar = st.form_submit_button("📤 Enviar", use_container_width=True)

        with col3:
            limpar = st.form_submit_button("🗑️ Limpar", use_container_width=True)

        if enviar and mensagem:
            # Adicionar mensagem do usuário
            st.session_state.historico_assistente.append({"tipo": "user", "texto": mensagem})

            # Gerar resposta da IA
            with st.spinner(f"{nome_falecido} está pensando..."):
                resposta = assistente.conversar(mensagem)
            st.session_state.historico_assistente.append({"tipo": "bot", "texto": resposta})

            st.rerun()

        if limpar:
            st.session_state.historico_assistente = []
            st.rerun()

# ============================================================================
# VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h3 style='color: #2E8B57;'>📹 Mensagens em Vídeo</h3>", unsafe_allow_html=True)
    st.info("💡 Cada vídeo pode ser direcionado para uma pessoa específica.")

    plano = db.obter_plano_usuario(st.session_state.usuario_atual['id'])
    videos_atual = len(db.listar_videos_usuario(st.session_state.usuario_atual['id']))
    max_videos = plano.get("max_videos_total", 10) if plano else 10

    st.info(f"📊 Você tem {videos_atual} de {max_videos} vídeos no seu plano.")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("🎥 Adicionar vídeo", expanded=False):
            titulo = st.text_input("Título *", key="titulo_video_input")

            categoria = st.selectbox("Categoria",
                                     ["Mensagem após falecimento", "Para pessoa específica", "Para data especial"],
                                     key="categoria_video")

            if categoria == "Para pessoa específica":
                contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])
                if contatos:
                    opcoes_contato = {c['nome_completo']: c['id'] for c in contatos}
                    contato_selecionado = st.selectbox("Selecione a pessoa", list(opcoes_contato.keys()),
                                                       key="video_contato")
                    destinatario = contato_selecionado
                else:
                    st.warning("⚠️ Cadastre um contato primeiro")
                    destinatario = ""
            else:
                destinatario = st.text_input("Para quem é este vídeo?", key="destinatario_video",
                                             placeholder="Ex: Para minha família")

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
                    db.adicionar_video(
                        usuario_id=st.session_state.usuario_atual['id'],
                        titulo=titulo,
                        destinatario=destinatario,
                        caminho_arquivo=caminho,
                        categoria=categoria
                    )
                    st.success(f"✅ {titulo} salvo com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Preencha o título e selecione um vídeo")

    with col2:
        videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
        if not videos:
            st.info("📭 Nenhum vídeo cadastrado")
        else:
            for video in videos:
                with st.expander(f"🎬 {video['titulo']} - {video['categoria']}"):
                    if video['destinatario']:
                        st.markdown(f"**👥 Para:** {video['destinatario']}")
                    if video['caminho'] and os.path.exists(video['caminho']):
                        st.video(video['caminho'])
                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        db.deletar_video(video['id'], st.session_state.usuario_atual['id'])
                        st.rerun()


# ============================================================================
# CONTATOS
# ============================================================================
def render_contatos():
    st.markdown("<h3 style='color: #2E8B57;'>👥 Contatos de Confiança</h3>", unsafe_allow_html=True)

    plano = db.obter_plano_usuario(st.session_state.usuario_atual['id'])
    contatos_atual = db.contar_contatos_usuario(st.session_state.usuario_atual['id'])
    max_contatos = plano.get("max_contatos", 10) if plano else 10
    prioridades_atual = db.contar_contatos_prioritarios(st.session_state.usuario_atual['id'])
    max_prioridades = plano.get("max_prioridades", 3) if plano else 3

    st.info(
        f"📊 Você tem {contatos_atual} de {max_contatos} contatos | Prioritários: {prioridades_atual} de {max_prioridades}")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Adicionar contato", expanded=False):
            st.markdown("**📝 Nome completo ***")
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                nome = st.text_input("nome", placeholder="Nome", key="contato_nome", label_visibility="collapsed")
            with col_n2:
                sobrenome = st.text_input("sobrenome", placeholder="Sobrenome", key="contato_sobrenome",
                                          label_visibility="collapsed")

            st.markdown("**📧 Forma de contato ***")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                email = st.text_input("email", placeholder="E-mail", key="contato_email", label_visibility="collapsed")
            with col_c2:
                whatsapp = st.text_input("whatsapp", placeholder="WhatsApp", key="contato_whatsapp",
                                         label_visibility="collapsed")

            st.caption("⚠️ Pelo menos um contato (e-mail ou WhatsApp) é obrigatório")

            st.markdown("---")
            st.markdown("#### ✨ Informações adicionais (opcional)")

            parentesco = st.selectbox("Grau de parentesco",
                                      ["", "Filho(a)", "Cônjuge", "Irmão(ã)", "Amigo(a)", "Advogado(a)", "Outro"],
                                      key="contato_parentesco")

            data_nascimento = st.date_input("Data de nascimento", key="contato_data_nascimento", value=None)

            is_prioridade = st.checkbox("Marcar como contato prioritário", key="contato_prioridade")

            if is_prioridade and prioridades_atual >= max_prioridades:
                st.warning(
                    f"⚠️ Você já tem {prioridades_atual} contatos prioritários. Limite do plano: {max_prioridades}.")
                is_prioridade = False

            if st.button("💾 Salvar", type="primary", use_container_width=True):
                if not nome or not sobrenome:
                    st.error("❌ Nome e sobrenome são obrigatórios")
                elif not email and not whatsapp:
                    st.error("❌ Informe pelo menos um contato (e-mail ou WhatsApp)")
                else:
                    chave_acesso = secrets.token_hex(8)
                    db.adicionar_contato(
                        usuario_id=st.session_state.usuario_atual['id'],
                        nome=nome,
                        sobrenome=sobrenome,
                        email=email,
                        telefone="",
                        whatsapp=whatsapp or "",
                        parentesco=parentesco,
                        data_nascimento=data_nascimento.strftime("%Y-%m-%d") if data_nascimento else "",
                        is_prioridade=1 if is_prioridade else 0,
                        prioridade_order=prioridades_atual + 1 if is_prioridade else 0,
                        chave_acesso=chave_acesso
                    )
                    st.success(f"✅ {nome} {sobrenome} adicionado!")
                    st.info(f"🔑 Chave de acesso: `{chave_acesso}`")
                    st.rerun()

    with col2:
        contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])
        if not contatos:
            st.info("📭 Nenhum contato cadastrado")
        else:
            for contato in contatos:
                with st.expander(f"👤 {contato['nome_completo']} {'⭐' if contato['is_prioridade'] else ''}"):
                    st.markdown(f"**Email:** {contato['email']}")
                    if contato.get('whatsapp'):
                        st.markdown(f"**WhatsApp:** {contato['whatsapp']}")
                    if contato.get('parentesco'):
                        st.markdown(f"**Parentesco:** {contato['parentesco']}")
                    if contato.get('data_nascimento'):
                        st.markdown(f"**Data nascimento:** {contato['data_nascimento']}")
                    st.markdown(f"**Prioritário:** {'✅ Sim' if contato.get('is_prioridade') else '❌ Não'}")

                    if st.button(f"🗑️ Remover", key=f"del_contato_{contato['id']}"):
                        db.deletar_contato(contato['id'], st.session_state.usuario_atual['id'])
                        st.rerun()


# ============================================================================
# PREFERÊNCIAS (GOSTOS)
# ============================================================================
def render_preferencias():
    st.markdown("<h3 style='color: #2E8B57;'>🧠 Sobre você</h3>", unsafe_allow_html=True)
    st.info("💡 Essas informações ajudam o Assistente de Luto a conversar como você.")

    preferencias = db.obter_preferencias(st.session_state.usuario_atual['id'])

    with st.form("preferencias_form"):
        st.markdown("**🎵 Música favorita**")
        gostos_musica = st.text_area("Quais seus gêneros/artistas favoritos?",
                                     value=preferencias.get('gostos_musica', ''),
                                     height=60, key="pref_musica")

        st.markdown("**🍽️ Comida favorita**")
        gostos_comida = st.text_area("Quais seus pratos/restaurantes favoritos?",
                                     value=preferencias.get('gostos_comida', ''),
                                     height=60, key="pref_comida")

        st.markdown("**💭 Melhor lembrança**")
        melhor_lembranca = st.text_area("Qual sua memória mais feliz?",
                                        value=preferencias.get('melhor_lembranca', ''),
                                        height=80, key="pref_lembranca")

        st.markdown("**😊 Dia mais feliz**")
        dia_mais_feliz = st.text_area("Descreva o dia mais feliz da sua vida",
                                      value=preferencias.get('dia_mais_feliz', ''),
                                      height=80, key="pref_feliz")

        st.markdown("**😔 Dia mais triste**")
        dia_mais_triste = st.text_area("Como você superou momentos difíceis?",
                                       value=preferencias.get('dia_mais_triste', ''),
                                       height=80, key="pref_triste")

        st.markdown("**💬 Personalidade extra**")
        personalidade_extra = st.text_area("Algo mais que você quer que o assistente saiba sobre você?",
                                           value=preferencias.get('personalidade_extra', ''),
                                           height=100, key="pref_extra")

        if st.form_submit_button("💾 Salvar Preferências", type="primary"):
            novas_preferencias = {
                "gostos_musica": gostos_musica,
                "gostos_comida": gostos_comida,
                "melhor_lembranca": melhor_lembranca,
                "dia_mais_feliz": dia_mais_feliz,
                "dia_mais_triste": dia_mais_triste,
                "personalidade_extra": personalidade_extra
            }
            db.salvar_preferencias(st.session_state.usuario_atual['id'], novas_preferencias)
            st.success("✅ Preferências salvas! O assistente agora te conhece melhor.")
            st.rerun()


# ============================================================================
# AGENDAMENTOS (LEMBRANÇAS PROGRAMADAS)
# ============================================================================
def render_agendamentos():
    st.markdown("<h3 style='color: #2E8B57;'>📅 Lembranças Programadas</h3>", unsafe_allow_html=True)
    st.caption("Programe mensagens ou vídeos para serem enviados em datas especiais.")

    plano = db.obter_plano_usuario(st.session_state.usuario_atual['id'])

    if not plano.get("tem_agendamento", False):
        st.info("💡 Esta funcionalidade estará disponível em breve nos planos pagos!")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Criar nova lembrança", expanded=False):
            contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])
            if not contatos:
                st.warning("⚠️ Cadastre um contato primeiro")
            else:
                opcoes_contato = {c['nome_completo']: c['id'] for c in contatos}
                contato_selecionado = st.selectbox("Para quem?", list(opcoes_contato.keys()), key="agendamento_contato")
                contato_id = opcoes_contato[contato_selecionado]

                tipo = st.selectbox("Tipo de mensagem", ["texto", "vídeo"], key="agendamento_tipo")

                data_envio = st.date_input("Data de envio", min_value=datetime.now().date(), key="agendamento_data")
                data_termino = st.date_input("Data de término (opcional)", key="agendamento_termino", value=None)

                conteudo = ""
                if tipo == "texto":
                    opcao_texto = st.radio("Como criar?", ["Escrever manualmente", "Gerar com IA"],
                                           key="agendamento_opcao")
                    if opcao_texto == "Escrever manualmente":
                        conteudo = st.text_area("Digite sua mensagem:", height=150, key="agendamento_texto")
                    else:
                        st.info("🤖 Em breve: IA generativa para criar mensagens personalizadas")
                        conteudo = st.text_area("Digite sua mensagem:", height=150, key="agendamento_texto_ia")
                else:
                    videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
                    if videos:
                        opcoes_video = {v['titulo']: v['id'] for v in videos}
                        video_selecionado = st.selectbox("Selecione um vídeo", list(opcoes_video.keys()),
                                                         key="agendamento_video")
                        video_id = opcoes_video[video_selecionado]
                    else:
                        st.warning("⚠️ Você não tem vídeos cadastrados.")
                        return

                if st.button("💾 Agendar", type="primary", use_container_width=True):
                    if tipo == "texto" and not conteudo:
                        st.error("❌ Digite uma mensagem")
                    else:
                        db.criar_agendamento(
                            usuario_id=st.session_state.usuario_atual['id'],
                            contato_id=contato_id,
                            tipo=tipo,
                            data_envio=data_envio.strftime("%Y-%m-%d"),
                            data_termino=data_termino.strftime("%Y-%m-%d") if data_termino else "",
                            conteudo=conteudo,
                            video_id=video_id if tipo == "vídeo" else None
                        )
                        st.success(f"✅ Lembrança agendada para {data_envio.strftime('%d/%m/%Y')}!")
                        st.rerun()

    with col2:
        agendamentos = db.listar_agendamentos_usuario(st.session_state.usuario_atual['id'])
        if not agendamentos:
            st.info("📭 Nenhuma lembrança programada")
        else:
            for agend in agendamentos:
                with st.expander(f"📌 {agend['tipo'].upper()} para {agend['contato_nome']} - {agend['data_envio']}"):
                    st.markdown(f"**Para:** {agend['contato_nome']} ({agend['contato_email']})")
                    st.markdown(f"**Data de envio:** {agend['data_envio']}")
                    if agend['data_termino']:
                        st.markdown(f"**Data de término:** {agend['data_termino']}")
                    st.markdown(f"**Status:** {agend['status']}")
                    if agend['conteudo']:
                        st.markdown(f"**Mensagem:** {agend['conteudo'][:200]}...")

                    if st.button(f"🗑️ Cancelar", key=f"del_agend_{agend['id']}"):
                        db.deletar_agendamento(agend['id'], st.session_state.usuario_atual['id'])
                        st.rerun()


# ============================================================================
# PAINEL ADMIN
# ============================================================================
def render_admin_panel():
    st.markdown("<h2 style='color: #2E8B57;'>👑 Painel Administrativo</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Estatísticas", "👥 Usuários"])

    with tab1:
        st.markdown("### 📊 Estatísticas do Sistema")

        usuarios = gerente_usuarios.listar_usuarios()
        senhas = db.listar_senhas_usuario(st.session_state.usuario_atual['id'])
        videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
        contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Usuários", len(usuarios))
        with col2:
            st.metric("🔐 Senhas", len(senhas))
        with col3:
            st.metric("📹 Vídeos", len(videos))
        with col4:
            st.metric("👥 Contatos", len(contatos))

    with tab2:
        st.markdown("### 👥 Usuários Cadastrados")

        if not usuarios:
            st.info("Nenhum usuário cadastrado ainda.")
        else:
            for usuario in usuarios:
                with st.expander(f"👤 {usuario['nome']}"):
                    st.markdown(f"**Email:** {usuario['email']}")
                    st.markdown(f"**CPF:** {usuario['cpf']}")
                    st.markdown(f"**Tipo:** {usuario['tipo']}")
                    st.markdown(f"**Criado em:** {usuario['data_criacao']}")


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
        <p>Uma IA treinada com sua personalidade para conversar com seus entes queridos e oferecer conforto.</p>
    </div>

    <div class="info-card">
        <h3>📅 Lembranças Programadas</h3>
        <p>Programe mensagens e vídeos para serem enviados em datas especiais como aniversários, Natal e outras ocasiões importantes.</p>
    </div>

    <div class="info-card">
        <h3>🔒 Segurança e LGPD</h3>
        <p>✅ Criptografia de ponta a ponta<br>
        ✅ Seus dados, sua chave - nem nós acessamos<br>
        ✅ 100% compatível com a LGPD</p>
    </div>

    <div class="info-card">
        <h3>💼 Para Investidores e Parceiros</h3>
        <p>📧 parcerias@aeterenalegado.com.br</p>
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

        is_admin = st.session_state.usuario_atual.get('tipo') == 'admin'
        nome_exibido = st.session_state.usuario_atual.get('nome_completo', 'Usuário')

        with st.sidebar:
            st.markdown(f"### ✨ Olá, {nome_exibido}!")
            if st.button("🚪 Sair", use_container_width=True):
                fazer_logout()
            st.markdown("---")
            st.markdown("### 📊 Seu Legado")
            st.metric("📹 Vídeos", len(db.listar_videos_usuario(st.session_state.usuario_atual['id'])))
            st.metric("👥 Contatos", len(db.listar_contatos_usuario(st.session_state.usuario_atual['id'])))

        if is_admin:
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "🤖 Assistente", "📹 Vídeos", "👥 Contatos", "🧠 Perfil", "📅 Lembranças", "👑 Admin"
            ])
            with tab1:
                render_assistente()
            with tab2:
                render_videos()
            with tab3:
                render_contatos()
            with tab4:
                render_preferencias()
            with tab5:
                render_agendamentos()
            with tab6:
                render_admin_panel()
        else:
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🤖 Assistente", "📹 Vídeos", "👥 Contatos", "🧠 Perfil", "📅 Lembranças"
            ])
            with tab1:
                render_assistente()
            with tab2:
                render_videos()
            with tab3:
                render_contatos()
            with tab4:
                render_preferencias()
            with tab5:
                render_agendamentos()

        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna - Seu legado, sua história, sua vida. ✨</p>
            <p style="font-size: 0.6rem;">Versão 2.0 | Assistente de Luto | Lembranças Programadas | LGPD Compliant</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
