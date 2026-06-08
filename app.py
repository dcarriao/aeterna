import streamlit as st
from PIL import Image
import os
from datetime import datetime
import json
import sqlite3
import secrets
import pandas as pd
from utils.banco import BancoDados
from utils.criptografia import GerenciadorCriptografia
from utils.usuarios import GerenciadorUsuarios
from utils.upload_video import GerenciadorVideos
from utils.assistente_ia import AssistenteLuto
from utils.contatos import GerenciadorContatos
from utils.agendamentos import GerenciadorAgendamentos


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

        .chat-wrapper {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            height: 450px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .chat-message-user {
            background: #2E8B57;
            color: white;
            padding: 10px 15px;
            border-radius: 20px 20px 5px 20px;
            margin: 8px 0;
            text-align: right;
            max-width: 80%;
            align-self: flex-end;
            word-wrap: break-word;
        }
        .chat-message-bot {
            background: white;
            color: #333;
            padding: 10px 15px;
            border-radius: 20px 20px 20px 5px;
            margin: 8px 0;
            text-align: left;
            max-width: 80%;
            align-self: flex-start;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            word-wrap: break-word;
        }
        .chat-name-user {
            font-size: 0.7rem;
            color: #666;
            text-align: right;
            margin-bottom: -5px;
        }
        .chat-name-bot {
            font-size: 0.7rem;
            color: #2E8B57;
            text-align: left;
            margin-bottom: -5px;
            margin-left: 5px;
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
            .chat-message-user, .chat-message-bot { max-width: 95%; }
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
gerente_contatos = GerenciadorContatos(db)
gerente_agendamentos = GerenciadorAgendamentos(db)

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


def fazer_login_visitante(visitante_nome, chave_acesso, falecido_email):
    contato = db.obter_contato_por_chave(chave_acesso, falecido_email)

    if contato and contato.get('acesso_central_luto', 0):
        st.session_state.autenticado = True
        st.session_state.modo_acesso = 'visitante'
        st.session_state.falecido_id = contato['usuario_id']
        st.session_state.usuario_atual = {
            'id': contato['id'],
            'nome': visitante_nome,
            'tipo': 'visitante',
            'nome_falecido': contato['falecido_nome'],
            'email': contato['email'],
            'whatsapp': contato['whatsapp']
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
                        st.error("❌ Credenciais inválidas ou você não tem acesso à Central de Luto")
                else:
                    st.warning("⚠️ Preencha todos os campos")
        st.info("💡 Sem chave? Entre em contato com a família.")

    with tab3:
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
# ASSISTENTE DE LUTO - VERSÃO CHAT EXPANSÍVEL
# ============================================================================
def render_assistente():
    """Renderiza o assistente de luto no estilo chat expansível"""
    assistente = AssistenteLuto(st.session_state.falecido_id)

    nome_falecido = st.session_state.usuario_atual.get('nome_falecido', 'seu ente querido')
    if st.session_state.modo_acesso == 'falecido':
        nome_falecido = st.session_state.usuario_atual.get('nome_completo') or \
                        st.session_state.usuario_atual.get('nome') or \
                        "você"

    # Layout de duas colunas: chat (2/3) e informações (1/3)
    col_chat, col_info = st.columns([2, 1])

    with col_chat:
        # Cabeçalho do chat
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2E8B57 0%, #1B5E20 100%);
            padding: 12px;
            border-radius: 15px 15px 0 0;
            color: white;
            text-align: center;
            font-weight: bold;
        ">
            💬 Conversando com {nome_falecido}
        </div>
        """, unsafe_allow_html=True)

        # Aviso importante em um expander (só abre se clicar)
        with st.expander("⚠️ Sobre esta conversa (clique para ler)"):
            st.markdown(f"""
            💡 **Importante:** Esta é uma conversa gerada por IA baseada na personalidade de **{nome_falecido}**. 

            As respostas são simulações e podem não representar exatamente o que a pessoa pensava ou sentia. 

            **Use com carinho e parcimônia.** O objetivo é ajudar no processo de luto, não criar dependência.
            """)

        # Container do chat
        chat_container = st.container()

        with chat_container:
            # Inicializar histórico
            if "historico_assistente" not in st.session_state:
                st.session_state.historico_assistente = []

            # Mostrar mensagens do chat
            if not st.session_state.historico_assistente:
                msg_inicial = f"Olá! Sou uma simulação baseada em como {nome_falecido} era. Pode me perguntar qualquer coisa. 💚"
                st.session_state.historico_assistente.append({"tipo": "bot", "texto": msg_inicial})

            # Exibir mensagens como se fosse um chat
            for msg in st.session_state.historico_assistente:
                if msg["tipo"] == "usuario":
                    st.markdown(f'<div class="chat-name-user">Você</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-message-user">{msg["texto"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-name-bot">{nome_falecido}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-message-bot">{msg["texto"]}</div>', unsafe_allow_html=True)

        # Input de mensagem
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            mensagem = st.text_area("Sua mensagem:", key="msg_assistente",
                                    placeholder=f"Escreva sua mensagem para {nome_falecido}...",
                                    label_visibility="collapsed",
                                    height=80)
        with col_btn:
            enviar = st.button("📨 Enviar", key="btn_enviar", type="primary", use_container_width=True)

        if enviar and mensagem:
            st.session_state.historico_assistente.append({"tipo": "usuario", "texto": mensagem})
            with st.spinner(f"{nome_falecido} está pensando..."):
                resposta = assistente.conversar(mensagem)
            st.session_state.historico_assistente.append({"tipo": "bot", "texto": resposta})
            st.rerun()

        # Botão para limpar conversa
        if st.button("🗑️ Limpar conversa", key="clear_chat", use_container_width=True):
            st.session_state.historico_assistente = []
            st.rerun()

    with col_info:
        # Informações sobre o assistente
        st.markdown("""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #2E8B57;
        ">
            <h4 style="color: #2E8B57; margin-top: 0;">🤖 Sobre este assistente</h4>
            <p style="font-size: 0.8rem; margin-bottom: 8px;">O Assistente de Luto do aEterna foi treinado com:</p>
            <ul style="font-size: 0.75rem; padding-left: 20px;">
                <li>✅ Sua personalidade (respostas às perguntas)</li>
                <li>✅ Suas preferências (música, comida, lembranças)</li>
                <li>✅ Mensagens e textos que você deixou</li>
            </ul>
            <p style="font-size: 0.7rem; color: #666; margin-top: 10px;">💡 Quanto mais informações você fornecer, mais personalizadas serão as respostas.</p>
        </div>
        """, unsafe_allow_html=True)

        # Dicas de conversa
        with st.expander("💬 Dicas de conversa"):
            st.markdown("""
            - Pergunte sobre lembranças felizes
            - Peça conselhos para decisões importantes  
            - Conte sobre suas conquistas
            - Fale sobre momentos especiais que viveram juntos
            - Pergunte sobre músicas ou comidas favoritas
            """)

        # Estatísticas
        stats = assistente.estatisticas()
        st.markdown(f"""
        <div style="
            background: #e8f5e9;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
        ">
            <p style="margin: 0; font-size: 0.8rem;">📊</p>
            <p style="margin: 0; font-weight: bold;">{stats.get('perguntas_respondidas', 0)} perguntas respondidas</p>
            <p style="margin: 0; font-size: 0.7rem; color: #666;">sobre a personalidade</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h3 style='color: #2E8B57;'>📹 Mensagens em Vídeo</h3>", unsafe_allow_html=True)

    plano = gerente_usuarios.obter_plano_usuario(st.session_state.usuario_atual['id'])
    videos_atual = len(db.listar_videos_usuario(st.session_state.usuario_atual['id']))
    max_videos = plano.get("max_videos_total", 10) if plano else 10

    st.info(f"💡 Você tem {videos_atual} de {max_videos} vídeos disponíveis no seu plano.")

    if videos_atual >= max_videos:
        st.warning(f"⚠️ Você atingiu o limite de {max_videos} vídeos do seu plano. Para adicionar mais, faça upgrade.")
        return

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
                    opcoes_contato = {f"{c['nome_completo']} ({c['email']})": c['id'] for c in contatos}
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
                    contatos_ids = []
                    if categoria == "Para pessoa específica" and contatos:
                        contatos_ids = [contatos[0]['id']]

                    caminho = gerente_videos.salvar_video(
                        arquivo_video,
                        st.session_state.usuario_atual['id'],
                        titulo,
                        destinatario,
                        categoria
                    )

                    db.adicionar_video_com_acesso(
                        usuario_id=st.session_state.usuario_atual['id'],
                        titulo=titulo,
                        destinatario=destinatario,
                        caminho_arquivo=caminho,
                        contatos_ids=contatos_ids,
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
                    st.video(video['caminho'])
                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        if db.deletar_video(video['id'], st.session_state.usuario_atual['id']):
                            st.rerun()


# ============================================================================
# PREFERÊNCIAS DO USUÁRIO
# ============================================================================
def render_preferencias():
    st.markdown("<h3 style='color: #2E8B57;'>🧠 Sobre você</h3>", unsafe_allow_html=True)
    st.info("💡 Essas informações ajudam o Assistente de Luto a conversar como você.")

    preferencias = gerente_usuarios.obter_preferencias(st.session_state.usuario_atual['id'])

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
            gerente_usuarios.salvar_preferencias(st.session_state.usuario_atual['id'], novas_preferencias)
            st.success("✅ Preferências salvas! O assistente agora te conhece melhor.")
            st.rerun()


# ============================================================================
# CONTATOS
# ============================================================================
def render_contatos():
    st.markdown("<h3 style='color: #2E8B57;'>👥 Contatos de Confiança</h3>", unsafe_allow_html=True)

    plano = gerente_usuarios.obter_plano_usuario(st.session_state.usuario_atual['id'])
    contatos_atual = db.contar_contatos_usuario(st.session_state.usuario_atual['id'])
    max_contatos = plano.get("max_contatos", 5) if plano else 5

    st.info(f"💡 Você tem {contatos_atual} de {max_contatos} contatos no seu plano.")

    col1, col2 = st.columns([1, 2])

    with col1:
        gerente_contatos.renderizar_formulario_adicionar(
            st.session_state.usuario_atual['id'],
            plano
        )

    with col2:
        gerente_contatos.renderizar_lista_contatos(st.session_state.usuario_atual['id'])


# ============================================================================
# LEMBRANÇAS PROGRAMADAS
# ============================================================================
def render_agendamentos():
    st.markdown("<h3 style='color: #2E8B57;'>📅 Lembranças Programadas</h3>", unsafe_allow_html=True)
    st.caption("Programe mensagens ou vídeos para serem enviados em datas especiais.")

    plano = gerente_usuarios.obter_plano_usuario(st.session_state.usuario_atual['id'])

    col1, col2 = st.columns([1, 2])

    with col1:
        gerente_agendamentos.renderizar_formulario(
            st.session_state.usuario_atual['id'],
            plano
        )

    with col2:
        gerente_agendamentos.renderizar_lista(st.session_state.usuario_atual['id'])


# ============================================================================
# PAINEL ADMINISTRATIVO
# ============================================================================
def render_admin_panel():
    st.markdown("<h2 style='color: #2E8B57;'>👑 Painel Administrativo</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Estatísticas", "👥 Usuários", "📤 Exportar"])

    with tab1:
        st.markdown("### 📊 Estatísticas do Sistema")

        conn = sqlite3.connect("dados/cofre.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total_usuarios = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE data_criacao >= date('now', '-30 days')")
            novos_usuarios = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'admin'")
            total_admins = cursor.fetchone()[0]
        else:
            total_usuarios = 0
            novos_usuarios = 0
            total_admins = 0

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='senhas'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM senhas")
            total_senhas = cursor.fetchone()[0]
        else:
            total_senhas = 0

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='videos'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM videos")
            total_videos = cursor.fetchone()[0]
        else:
            total_videos = 0

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contatos'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM contatos")
            total_contatos = cursor.fetchone()[0]
        else:
            total_contatos = 0

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalidade'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(DISTINCT usuario_id) FROM personalidade")
            total_com_ia = cursor.fetchone()[0]
        else:
            total_com_ia = 0

        conn.close()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Usuários", total_usuarios, delta=f"+{novos_usuarios} últimos 30 dias")
        with col2:
            st.metric("🔐 Senhas", total_senhas)
        with col3:
            st.metric("📹 Vídeos", total_videos)
        with col4:
            st.metric("🤖 Assistente IA", total_com_ia)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Contatos", total_contatos)
        with col2:
            st.metric("👑 Admins", total_admins)

        st.markdown("---")
        st.markdown("### 📈 Gráfico de Usuários por Mês")

        conn = sqlite3.connect("dados/cofre.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            try:
                cursor.execute('''
                    SELECT strftime('%Y-%m', data_criacao) as mes, COUNT(*) 
                    FROM usuarios 
                    WHERE data_criacao >= date('now', '-6 months')
                    GROUP BY mes 
                    ORDER BY mes
                ''')
                dados_meses = cursor.fetchall()

                if dados_meses:
                    meses = [d[0] for d in dados_meses]
                    quantidades = [d[1] for d in dados_meses]
                    st.line_chart({"Usuários": quantidades}, x=meses)
                else:
                    st.info("Ainda não há dados suficientes para exibir o gráfico.")
            except Exception as e:
                st.info("Dados insuficientes para gerar o gráfico.")
        else:
            st.info("Nenhum usuário cadastrado ainda.")

        conn.close()

    with tab2:
        st.markdown("### 👥 Usuários Cadastrados")

        conn = sqlite3.connect("dados/cofre.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            cursor.execute('''
                SELECT id, nome, sobrenome, email, cpf, tipo, data_criacao, ultimo_acesso 
                FROM usuarios ORDER BY data_criacao DESC
            ''')
            usuarios = cursor.fetchall()

            if usuarios:
                for usuario in usuarios:
                    with st.expander(f"👤 {usuario[1]} {usuario[2]} ({usuario[5]})"):
                        st.markdown(f"**ID:** {usuario[0]}")
                        st.markdown(f"**Email:** {usuario[3]}")
                        st.markdown(f"**CPF:** {usuario[4]}")
                        st.markdown(f"**Tipo:** {usuario[5]}")
                        st.markdown(f"**Criado em:** {usuario[6]}")
                        st.markdown(f"**Último acesso:** {usuario[7] or 'Nunca'}")

                        if usuario[5] != 'admin':
                            if st.button(f"🗑️ Excluir {usuario[1]} {usuario[2]}", key=f"del_user_{usuario[0]}"):
                                conn2 = sqlite3.connect("dados/cofre.db")
                                cursor2 = conn2.cursor()
                                cursor2.execute("DELETE FROM usuarios WHERE id = ?", (usuario[0],))
                                conn2.commit()
                                conn2.close()
                                st.success(f"✅ Usuário {usuario[1]} {usuario[2]} excluído!")
                                st.rerun()
            else:
                st.info("Nenhum usuário cadastrado ainda.")
        else:
            st.info("Nenhum usuário cadastrado ainda.")

        conn.close()

    with tab3:
        st.markdown("### 📤 Exportar Dados")

        conn = sqlite3.connect("dados/cofre.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            cursor.execute('''
                SELECT id, nome, sobrenome, email, cpf, tipo, data_criacao, ultimo_acesso 
                FROM usuarios
            ''')
            usuarios = cursor.fetchall()

            if usuarios:
                df = pd.DataFrame(usuarios, columns=["ID", "Nome", "Sobrenome", "Email", "CPF", "Tipo", "Data Criação",
                                                     "Último Acesso"])
                csv = df.to_csv(index=False)

                st.download_button(
                    label="📥 Exportar Usuários (CSV)",
                    data=csv,
                    file_name="usuarios_aeterna.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nenhum usuário para exportar.")
        else:
            st.info("Nenhum usuário para exportar.")

        conn.close()

        st.markdown("---")
        st.markdown("### 🌐 Google Analytics")
        st.markdown("""
        Para estatísticas detalhadas de visitas (origem, localização, dispositivos), 
        configure o Google Analytics no seu site:

        1. Acesse [Google Analytics](https://analytics.google.com)
        2. Crie uma conta gratuita
        3. Adicione o código de rastreamento no `index.html`
        4. Em 24h você terá dados completos
        """)


# ============================================================================
# SOBRE
# ============================================================================
def render_sobre():
    st.markdown("<h3 style='color: #2E8B57;'>✨ Sobre o aEterna</h3>", unsafe_allow_html=True)

    plano = None
    if st.session_state.modo_acesso == 'falecido':
        plano = gerente_usuarios.obter_plano_usuario(st.session_state.usuario_atual['id'])

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
    """, unsafe_allow_html=True)

    if plano:
        st.markdown(f"""
        <div class="info-card">
            <h3>📊 Seu Plano Atual</h3>
            <p><strong>{plano.get('nome', 'Gratuito')}</strong></p>
            <p>💰 Preço: R$ {plano.get('preco', 0):.2f}/mês</p>
            <p>📞 Contatos: até {plano.get('max_contatos', 5)} pessoas<br>
            ⭐ Prioritários: até {plano.get('max_prioridades', 3)}<br>
            💬 Mensagens IA: {plano.get('max_mensagens_ia', 50)} por mês<br>
            📹 Vídeos totais: {plano.get('max_videos_total', 10)}<br>
            📅 Agendamentos: {'✅ Sim' if plano.get('tem_agendamento', 0) else '❌ Não'}<br>
            🎬 Vídeos com IA: {'✅ Sim' if plano.get('tem_videos_ia', 0) else '❌ Não'}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>💼 Para Investidores e Parceiros</h3>
        <p>📧 parcerias@aeterenalegado.com.br</p>
    </div>

    <div class="info-card">
        <h3>📱 Funcionalidades Futuras</h3>
        <p>✅ App mobile (Android/iOS)<br>
        ✅ Lembranças Programadas em datas especiais<br>
        ✅ Presentes e flores programados<br>
        ✅ Mural da memória<br>
        ✅ Testamento digital</p>
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
            is_admin = st.session_state.usuario_atual.get('tipo') == 'admin'
            nome_exibido = st.session_state.usuario_atual.get('nome_completo') or \
                           st.session_state.usuario_atual.get('nome') or \
                           "Usuário"

            with st.sidebar:
                st.markdown(f"### ✨ Olá, {nome_exibido}!")
                if st.button("🚪 Sair", use_container_width=True):
                    fazer_logout()
                st.markdown("---")
                st.markdown("### 📊 Seu Legado")
                videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
                contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])
                st.metric("📹 Vídeos", len(videos))
                st.metric("👥 Contatos", len(contatos))

            if is_admin:
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "🤖 Assistente", "📹 Vídeos", "👥 Contatos", "🧠 Preferências",
                    "📅 Lembranças", "👑 Admin", "ℹ️ Sobre"
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
                with tab7:
                    render_sobre()
            else:
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "🤖 Assistente", "📹 Vídeos", "👥 Contatos", "🧠 Preferências", "📅 Lembranças", "ℹ️ Sobre"
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
                    render_sobre()
        else:
            nome_falecido = st.session_state.usuario_atual.get('nome_falecido', 'seu ente querido')
            nome_visitante = st.session_state.usuario_atual.get('nome', 'Visitante')

            with st.sidebar:
                st.markdown(f"### 🕊️ Em memória de")
                st.markdown(f"### {nome_falecido}")
                st.markdown(f"**Seu nome:** {nome_visitante}")
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