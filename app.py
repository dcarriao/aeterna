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
from utils.email_service import EmailService, processar_agendamentos
from styles.theme import aplicar_tema
from components.landing import render_landing
from components.chat_luto import render_chat_luto
from components.login_compacto import render_login_compacto
from components.dashboard_ui import (
    aplicar_css_dashboard,
    render_sidebar_premium,
    render_painel_inicial
)
from components.mobile_ui import aplicar_css_mobile
from datetime import date

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

aplicar_tema()


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

        /* Chat Widget */
        .chat-widget {
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            position: sticky;
            top: 20px;
        }

        .chat-header {
            background: #075e54;
            padding: 10px 12px;
            color: white;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chat-avatar {
            background: #128C7E;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }

        .chat-header-name {
            font-weight: bold;
            font-size: 0.85rem;
        }

        .chat-body {
            height: 320px;
            overflow-y: auto;
            padding: 12px;
            background: #e5ddd5;
            display: flex;
            flex-direction: column;
        }

        .message-row {
            display: flex;
            margin-bottom: 10px;
            width: 100%;
        }

        .message-row.user {
            justify-content: flex-end;
        }

        .message-row.bot {
            justify-content: flex-start;
        }

        .message-bubble {
            max-width: 80%;
            padding: 8px 12px;
            border-radius: 16px;
            font-size: 0.8rem;
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

        .chat-footer {
            padding: 10px;
            background: white;
            border-top: 1px solid #eee;
        }

        .chat-warning {
            background: #fff3cd;
            padding: 4px 8px;
            font-size: 0.65rem;
            color: #856404;
            text-align: center;
        }

        .stTextInput > div > div > input {
            color: #1a1a1a !important;
            background-color: #ffffff !important;
            border: 1px solid #c8e6c8 !important;
            border-radius: 10px !important;
            padding: 8px !important;
            font-size: 14px !important;
        }

        @media (max-width: 768px) {
            .chat-body { height: 250px; }
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
    usuario = db.autenticar_usuario(email, senha)

    if usuario:
        nome_completo = f"{usuario.get('nome', '')} {usuario.get('sobrenome', '')}".strip()

        usuario["nome_completo"] = nome_completo or usuario.get("nome", "Usuário")

        st.session_state.autenticado = True
        st.session_state.usuario_atual = usuario

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
            'usuario_id': contato['usuario_id'],  # <-- adicionar
            'nome': visitante_nome,
            'tipo': 'visitante',
            'nome_falecido': contato['falecido_nome'],
            'email': contato['email'],
            'whatsapp': contato['whatsapp'],
            'parentesco': contato.get('parentesco', '')
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


def fazer_cadastro(nome, sobrenome, email, cpf, data_nascimento, senha, telefone="", whatsapp=""):
    return db.cadastrar_usuario(
        nome,
        sobrenome,
        email,
        cpf,
        data_nascimento,
        senha,
        telefone,
        whatsapp
    )


# ============================================================================
# TELA DE LOGIN
# ============================================================================
def render_login():
    aplicar_css_dashboard()
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
            email = st.text_input("E-mail", key="login_email")
            senha = st.text_input("Senha", type="password", key="login_senha")
            submitted = st.form_submit_button("🌿 ENTRAR", use_container_width=True, type="primary")
            if submitted:
                if email and senha:
                    if fazer_login(email, senha):
                        st.success("✅ Login realizado!")
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha incorretos")

    with tab2:
        st.markdown("### Acessar legado de alguém especial")
        with st.form("visitante_form"):
            nome_visitante = st.text_input("Seu nome", key="visitante_nome")
            email_falecido = st.text_input("E-mail da pessoa falecida", key="visitante_email")
            chave = st.text_input("Chave de acesso", type="password", key="visitante_chave")
            submitted = st.form_submit_button("🕊️ ACESSAR LEGADO", use_container_width=True, type="primary")
            if submitted:
                if nome_visitante and email_falecido and chave:
                    if fazer_login_visitante(nome_visitante, chave, email_falecido):
                        st.success(f"✅ Bem-vindo(a), {nome_visitante}!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas")
        st.info("💡 Sem chave? Entre em contato com a família.")

    with tab3:
        st.markdown("### ✨ Crie sua conta")
        with st.form("cadastro_form"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome *", key="cadastro_nome")
            with col2:
                sobrenome = st.text_input("Sobrenome *", key="cadastro_sobrenome")

            email = st.text_input("E-mail *", key="cadastro_email")
            cpf = st.text_input("CPF (11 números) *", key="cadastro_cpf", max_chars=11)
            data_nascimento = st.date_input("Data de nascimento *", key="cadastro_data_nascimento", value=None)
            telefone = st.text_input("Telefone", key="cadastro_telefone")
            whatsapp = st.text_input("WhatsApp", key="cadastro_whatsapp")
            senha = st.text_input("Senha *", type="password", key="cadastro_senha")
            confirmar_senha = st.text_input("Confirmar senha *", type="password", key="cadastro_confirmar")

            submitted = st.form_submit_button("📝 CRIAR CONTA", use_container_width=True, type="primary")

            if submitted:
                if not nome or not sobrenome or not email or not cpf or not data_nascimento or not senha:
                    st.error("❌ Preencha todos os campos obrigatórios")
                elif len(cpf) != 11 or not cpf.isdigit():
                    st.error("❌ CPF inválido")
                elif senha != confirmar_senha:
                    st.error("❌ As senhas não coincidem")
                elif len(senha) < 6:
                    st.warning("⚠️ A senha deve ter pelo menos 6 caracteres")
                else:
                    resultado = fazer_cadastro(
                        nome, sobrenome, email, cpf,
                        data_nascimento.strftime("%Y-%m-%d"), senha, telefone, whatsapp
                    )
                    if resultado == True:
                        st.success("✅ Conta criada! Faça login.")
                        st.rerun()
                    elif resultado == "cpf_existente":
                        st.error("❌ Este CPF já está cadastrado")
                    else:
                        st.error("❌ Este e-mail já está cadastrado")


# ============================================================================
# ASSISTENTE DE LUTO (CHAT DENTRO DA CAIXA)
# ============================================================================
def render_assistente():
    render_chat_luto()

# ============================================================================
# VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h3 style='color: #2E8B57;'>📹 Mensagens em Vídeo</h3>", unsafe_allow_html=True)

    plano = db.obter_plano_usuario(st.session_state.usuario_atual['id'])
    videos_atual = len(db.listar_videos_usuario(st.session_state.usuario_atual['id']))
    max_videos = plano.get("max_videos_total", 10) if plano else 10

    st.info(f"📊 Você tem {videos_atual} de {max_videos} vídeos no seu plano.")

    if videos_atual >= max_videos:
        st.warning(f"⚠️ Você atingiu o limite de {max_videos} vídeos do seu plano.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("🎥 Adicionar vídeo", expanded=False):
            titulo = st.text_input("Título *", key="titulo_video")

            categoria = st.selectbox("Categoria",
                                     ["Mensagem após falecimento", "Para pessoa específica", "Para data especial"],
                                     key="categoria_video")

            # Seleção de contatos que terão acesso
            st.markdown("**👥 Quem pode ver este vídeo?**")

            contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])
            if not contatos:
                st.warning("⚠️ Cadastre contatos primeiro para definir quem pode ver o vídeo")
                contatos_selecionados = []
            else:
                opcoes_contato = {c['nome_completo']: c['id'] for c in contatos}
                contatos_selecionados_nomes = st.multiselect(
                    "Selecione os contatos que terão acesso ao vídeo",
                    list(opcoes_contato.keys()),
                    key="video_contatos_acesso"
                )
                contatos_selecionados = [opcoes_contato[nome] for nome in contatos_selecionados_nomes]

            # Destinatário específico (para categoria "Para pessoa específica")
            if categoria == "Para pessoa específica" and contatos:
                destinatario_nome = st.selectbox("Para quem é este vídeo?", list(opcoes_contato.keys()),
                                                 key="video_destinatario_especifico")
                destinatario = destinatario_nome
            else:
                destinatario = st.text_input("Para quem é este vídeo? (opcional)", key="destinatario_video",
                                             placeholder="Ex: Para minha família")

            arquivo_video = st.file_uploader("Arquivo de vídeo", type=["mp4", "mov", "avi", "mkv"], key="video_file")
            st.caption("📹 Formatos aceitos: MP4, MOV, AVI, MKV")

            if st.button("💾 Salvar", key="salvar_video", type="primary", use_container_width=True):

                if titulo and arquivo_video:

                    try:
                        caminho = gerente_videos.salvar_video(
                            arquivo_video,
                            st.session_state.usuario_atual['id'],
                            titulo,
                            destinatario,
                            categoria
                        )

                        print("VIDEO SALVO EM:", caminho)

                        video_id = db.adicionar_video_com_acesso(
                            usuario_id=st.session_state.usuario_atual['id'],
                            titulo=titulo,
                            destinatario=destinatario,
                            caminho_arquivo=caminho,
                            contatos_ids=contatos_selecionados,
                            categoria=categoria
                        )

                        print("VIDEO_ID:", video_id)

                        st.success(
                            f"✅ {titulo} salvo! "
                            f"{len(contatos_selecionados)} contato(s) terão acesso."
                        )

                        st.rerun()

                    except Exception as e:
                        print("ERRO AO SALVAR VIDEO:", e)
                        st.error(f"Erro ao salvar vídeo: {e}")

                else:
                    st.error("❌ Preencha o título e selecione um vídeo")

    with col2:
        videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
        if not videos:
            st.info("📭 Nenhum vídeo cadastrado")
        else:
            for video in videos:
                # Buscar contatos que têm acesso a este vídeo
                contatos_acesso = db.listar_contatos_por_video(video['id'])
                nomes_acesso = [c['nome_completo'] for c in contatos_acesso]

                with st.expander(f"🎬 {video['titulo']} - {video.get('categoria', 'geral')}"):
                    if video.get('destinatario'):
                        st.markdown(f"**👥 Para:** {video['destinatario']}")
                    st.markdown(
                        f"**🔓 Acesso para:** {', '.join(nomes_acesso) if nomes_acesso else 'Todos os contatos'}")
                    st.video(video['caminho'])

                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        db.deletar_video(video['id'], st.session_state.usuario_atual['id'])
                        st.rerun()

def render_videos_visitante():
    usuario = st.session_state.usuario_atual
    contato_id = usuario["id"]

    nome_falecido = st.session_state.usuario_atual.get(
        "nome_falecido",
        "essa pessoa"
    )

    st.markdown(
        f"<h3 style='color: #2E8B57;'>🕊️ Mensagens de {nome_falecido} para você</h3>",
        unsafe_allow_html=True
    )

    videos = db.listar_videos_por_contato(contato_id)

    if not videos:
        st.info("📭 Nenhum vídeo foi liberado para você.")
        return

    for video in videos:
        with st.expander(f"🎬 {video['titulo']}"):
            if video.get("destinatario"):
                st.markdown(f"**Para:** {video['destinatario']}")

            st.markdown(f"**Categoria:** {video.get('categoria', '')}")

            if video.get("caminho") and os.path.exists(video["caminho"]):
                st.video(video["caminho"])
            else:
                st.warning("Arquivo de vídeo indisponível neste ambiente.")

# ============================================================================
# CONTATOS (COMPLETO)
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

    if st.session_state.get("contato_salvo_msg"):
        st.success(st.session_state.contato_salvo_msg)
        st.code(st.session_state.contato_chave_msg)

        if st.button("Ocultar chave"):
            del st.session_state.contato_salvo_msg
            del st.session_state.contato_chave_msg
            st.rerun()

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Adicionar contato", expanded=False):

            with st.form("form_adicionar_contato", clear_on_submit=True):
                st.markdown("**📝 Nome completo ***")

                col_n1, col_n2 = st.columns(2)
                with col_n1:
                    nome = st.text_input("nome", placeholder="Nome", label_visibility="collapsed")
                with col_n2:
                    sobrenome = st.text_input("sobrenome", placeholder="Sobrenome", label_visibility="collapsed")

                st.markdown("**📧 Forma de contato ***")

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    email = st.text_input("email", placeholder="E-mail", label_visibility="collapsed")
                with col_c2:
                    whatsapp = st.text_input("whatsapp", placeholder="WhatsApp", label_visibility="collapsed")

                st.caption("⚠️ Pelo menos um contato (e-mail ou WhatsApp) é obrigatório")

                st.markdown("---")
                st.markdown("#### ✨ Informações adicionais (opcional)")

                parentesco = st.selectbox(
                    "Grau de parentesco",
                    ["", "Filho(a)", "Cônjuge", "Irmão(ã)", "Amigo(a)", "Advogado(a)", "Outro"]
                )

                data_nascimento = st.date_input(
                    "Data de nascimento",
                    value=date(1990, 1, 1),
                    min_value=date(1900, 1, 1),
                    max_value=date.today(),
                    format="DD/MM/YYYY"
                )

                is_prioridade = st.checkbox("Marcar como contato prioritário")

                acesso_central_luto = st.checkbox(
                    "Permitir acesso ao Assistente Memorial",
                    value=False
                )

                salvar = st.form_submit_button(
                    "💾 Salvar",
                    type="primary",
                    use_container_width=True
                )

                if salvar:
                    if not nome or not sobrenome:
                        st.error("❌ Nome e sobrenome são obrigatórios")
                    elif not email and not whatsapp:
                        st.error("❌ Informe pelo menos um contato (e-mail ou WhatsApp)")
                    elif is_prioridade and prioridades_atual >= max_prioridades:
                        st.warning(
                            f"⚠️ Você já tem {prioridades_atual} contatos prioritários. "
                            f"Limite: {max_prioridades}."
                        )
                    else:
                        chave_acesso = secrets.token_hex(8)

                        db.adicionar_contato(
                            usuario_id=st.session_state.usuario_atual["id"],
                            nome=nome,
                            sobrenome=sobrenome,
                            email=email,
                            telefone="",
                            whatsapp=whatsapp or "",
                            parentesco=parentesco,
                            data_nascimento=data_nascimento.strftime("%Y-%m-%d") if data_nascimento else "",
                            is_prioridade=1 if is_prioridade else 0,
                            prioridade_order=prioridades_atual + 1 if is_prioridade else 0,
                            acesso_central_luto=1 if acesso_central_luto else 0,
                            chave_acesso=chave_acesso,
                        )

                        st.session_state.contato_salvo_msg = f"✅ {nome} {sobrenome} adicionado!"
                        st.session_state.contato_chave_msg = f"🔑 Chave de acesso: {chave_acesso}"
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
                    if contato.get("chave_acesso"):
                        st.markdown("**Chave de acesso:**")
                        st.code(contato["chave_acesso"])
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
            st.success("✅ Preferências salvas!")
            st.rerun()


# ============================================================================
# LEMBRANÇAS PROGRAMADAS (AGENDAMENTOS)
# ============================================================================
def render_agendamentos():
    st.markdown("<h3 style='color: #2E8B57;'>📅 Lembranças Programadas</h3>", unsafe_allow_html=True)
    st.caption("Programe mensagens para serem enviadas em datas especiais.")

    # Processar agendamentos automaticamente
    enviados = processar_agendamentos()
    if enviados > 0:
        st.success(f"✨ {enviados} lembrança(s) programada(s) foram enviadas hoje!")

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
                opcoes_contato = {c['nome_completo']: c for c in contatos}
                contato_selecionado_nome = st.selectbox("Para quem?", list(opcoes_contato.keys()),
                                                        key="agendamento_contato")
                contato_selecionado = opcoes_contato[contato_selecionado_nome]
                contato_id = contato_selecionado['id']

                # Verificar se o contato tem e-mail
                if not contato_selecionado.get('email'):
                    st.warning("⚠️ Este contato não tem e-mail cadastrado. Adicione um e-mail para receber mensagens.")

                tipo = st.selectbox("Tipo de mensagem", ["texto", "vídeo"], key="agendamento_tipo")

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    data_envio = st.date_input("Data de envio", min_value=datetime.now().date(), key="agendamento_data")
                with col_d2:
                    data_termino = st.date_input("Data de término (opcional)", key="agendamento_termino", value=None)

                # Forma de envio
                forma_envio = st.selectbox("Como enviar?", ["E-mail", "WhatsApp (em breve)"], key="forma_envio")

                conteudo = ""
                video_id = None

                if tipo == "texto":
                    opcao_texto = st.radio("Como criar?", ["Escrever manualmente", "Gerar com IA (em breve)"],
                                           key="agendamento_opcao")
                    if opcao_texto == "Escrever manualmente":
                        conteudo = st.text_area("Digite sua mensagem:", height=150, key="agendamento_texto")
                    else:
                        st.info("🤖 Geração por IA disponível em breve!")
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

                # Data especial (opcional)
                data_especial = st.text_input("Data especial (opcional)", key="agendamento_data_especial",
                                              placeholder="Ex: Aniversário, Natal, Dia dos Pais...")

                if st.button("💾 Agendar", type="primary", use_container_width=True):
                    if tipo == "texto" and not conteudo:
                        st.error("❌ Digite uma mensagem")
                    elif not contato_selecionado.get('email') and forma_envio == "E-mail":
                        st.error("❌ Este contato não tem e-mail cadastrado")
                    else:
                        # Adicionar data especial ao conteúdo
                        mensagem_final = conteudo
                        if data_especial:
                            mensagem_final = f"✨ {data_especial} ✨\n\n{conteudo}"

                        db.criar_agendamento(
                            usuario_id=st.session_state.usuario_atual['id'],
                            contato_id=contato_id,
                            tipo=tipo,
                            data_envio=data_envio.strftime("%Y-%m-%d"),
                            data_termino=data_termino.strftime("%Y-%m-%d") if data_termino else "",
                            conteudo=mensagem_final,
                            video_id=video_id,
                            gerar_por_ia=1 if tipo == "texto" and opcao_texto == "Gerar com IA (em breve)" else 0
                        )
                        st.success(f"✅ Lembrança agendada para {data_envio.strftime('%d/%m/%Y')}!")
                        st.info(f"📧 Será enviada por e-mail para {contato_selecionado['email']}")
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

                    if agend['status'] == 'agendado':
                        if st.button(f"❌ Cancelar", key=f"del_agend_{agend['id']}"):
                            db.deletar_agendamento(agend['id'], st.session_state.usuario_atual['id'])
                            st.rerun()

# ============================================================================
# COFRE DIGITAL
# ============================================================================
def render_cofre():
    st.markdown("<h3 style='color: #2E8B57;'>📁 Cofre Digital</h3>", unsafe_allow_html=True)
    st.info("🔒 Todas as informações são criptografadas localmente.")

    tab_senhas, tab_documentos = st.tabs(["🔐 Senhas", "📄 Documentos"])

    with tab_senhas:
        st.markdown("#### 🔐 Suas Senhas")

        col1, col2 = st.columns([2, 1])

        with col2:
            with st.expander("➕ Adicionar senha", expanded=False):
                servico = st.text_input("Serviço/App *", key="servico_input")
                usuario_senha = st.text_input("Usuário/E-mail *", key="usuario_senha_input")
                senha_original = st.text_input("Senha *", type="password", key="senha_input")
                url = st.text_input("URL", key="url_input")
                notas = st.text_area("Notas", key="notas_input", height=80)

                if st.button("💾 Salvar", key="salvar_senha", type="primary", use_container_width=True):
                    if servico and usuario_senha and senha_original:
                        senha_cripto = st.session_state.crypto.criptografar(senha_original)
                        db.adicionar_senha(
                            usuario_id=st.session_state.usuario_atual['id'],
                            servico=servico,
                            usuario=usuario_senha,
                            senha=senha_cripto,
                            url=url,
                            notas=notas
                        )
                        st.success(f"✅ Senha de {servico} adicionada!")
                        st.rerun()

        with col1:
            senhas = db.listar_senhas_usuario(st.session_state.usuario_atual['id'])
            if not senhas:
                st.info("📭 Nenhuma senha cadastrada")
            else:
                for senha in senhas:
                    with st.expander(f"🔒 {senha['servico']}"):
                        st.markdown(f"**Usuário:** `{senha['usuario']}`")
                        if senha['url']:
                            st.markdown(f"**URL:** {senha['url']}")
                        if senha['notas']:
                            st.markdown(f"**Notas:** {senha['notas']}")

                        if st.button(f"🔓 Mostrar", key=f"ver_{senha['id']}"):
                            senha_completa = db.obter_senha(senha['id'], st.session_state.usuario_atual['id'])
                            if senha_completa:
                                senha_real = st.session_state.crypto.descriptografar(
                                    senha_completa['senha_criptografada'])
                                st.code(senha_real)
                        if st.button(f"🗑️ Excluir", key=f"del_{senha['id']}"):
                            db.deletar_senha(senha['id'], st.session_state.usuario_atual['id'])
                            st.rerun()

    with tab_documentos:
        st.markdown("#### 📄 Seus Documentos")

        tipos_documentos = ["RG", "CNH", "CPF", "Comprovante de Endereço", "Documento do Veículo", "Outro"]

        col1, col2 = st.columns([2, 1])

        with col2:
            with st.expander("➕ Adicionar documento", expanded=False):
                tipo_doc = st.selectbox("Tipo", tipos_documentos, key="tipo_documento")
                titulo_doc = st.text_input("Título", key="titulo_doc", placeholder=f"Ex: Minha {tipo_doc}")
                arquivo = st.file_uploader("Arquivo", type=["png", "jpg", "jpeg", "pdf"], key="arquivo_documento")
                descricao = st.text_area("Descrição", key="descricao_doc", height=80)

                titulo_final = titulo_doc if titulo_doc else f"{tipo_doc}"

                if st.button("💾 Salvar", key="salvar_doc", type="primary", use_container_width=True):
                    if arquivo:
                        docs_folder = f"documentos/usuario_{st.session_state.usuario_atual['id']}"
                        os.makedirs(docs_folder, exist_ok=True)

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        nome_arquivo = f"{timestamp}_{tipo_doc}_{arquivo.name}"
                        caminho_arquivo = os.path.join(docs_folder, nome_arquivo)

                        with open(caminho_arquivo, "wb") as f:
                            f.write(arquivo.getbuffer())

                        db.adicionar_documento(
                            usuario_id=st.session_state.usuario_atual['id'],
                            tipo=tipo_doc,
                            titulo=titulo_final,
                            descricao=descricao,
                            caminho_arquivo=caminho_arquivo,
                            nome_original=arquivo.name,
                            tamanho=arquivo.size
                        )
                        st.success(f"✅ {titulo_final} salvo!")
                        st.rerun()

        with col1:
            documentos = db.listar_documentos_usuario(st.session_state.usuario_atual['id'])
            if not documentos:
                st.info("📭 Nenhum documento cadastrado")
            else:
                for doc in documentos:
                    with st.expander(f"📄 {doc['titulo']}"):
                        st.markdown(f"**Tipo:** {doc['tipo']}")
                        if doc['descricao']:
                            st.markdown(f"**Descrição:** {doc['descricao']}")

                        if doc['caminho_arquivo'] and os.path.exists(doc['caminho_arquivo']):
                            if doc['nome_original'].lower().endswith(('.png', '.jpg', '.jpeg')):
                                st.image(doc['caminho_arquivo'], width=150)
                            elif doc['nome_original'].lower().endswith('.pdf'):
                                with open(doc['caminho_arquivo'], "rb") as f:
                                    st.download_button("📄 Baixar PDF", f, file_name=doc['nome_original'])

                        if st.button(f"🗑️ Excluir", key=f"del_doc_{doc['id']}"):
                            if doc['caminho_arquivo'] and os.path.exists(doc['caminho_arquivo']):
                                os.remove(doc['caminho_arquivo'])
                            db.deletar_documento(doc['id'], st.session_state.usuario_atual['id'])
                            st.rerun()


# ============================================================================
# SOBRE
# ============================================================================
def render_sobre():
    st.markdown("<h3 style='color: #2E8B57;'>✨ Sobre o aEterna</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <h3>🤖 Assistente de Luto com IA</h3>
        <p>Uma IA treinada com sua personalidade para conversar com seus entes queridos.</p>
    </div>
    <div class="info-card">
        <h3>📅 Lembranças Programadas</h3>
        <p>Programe mensagens para datas especiais.</p>
    </div>
    <div class="info-card">
        <h3>📁 Cofre Digital</h3>
        <p>Armazene senhas e documentos com criptografia.</p>
    </div>
    <div class="info-card">
        <h3>🔒 Segurança e LGPD</h3>
        <p>✅ Criptografia<br>✅ Seus dados, sua chave<br>✅ LGPD Compliant</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ADMIN PANEL
# ============================================================================
def render_admin_panel():
    st.markdown("<h2 style='color: #2E8B57;'>👑 Painel Administrativo</h2>", unsafe_allow_html=True)

    usuarios = gerente_usuarios.listar_usuarios()
    st.metric("👥 Total Usuários", len(usuarios))

    for usuario in usuarios:
        with st.expander(f"👤 {usuario['nome']}"):
            st.markdown(f"**Email:** {usuario['email']}")
            st.markdown(f"**CPF:** {usuario['cpf']}")
            st.markdown(f"**Tipo:** {usuario['tipo']}")


# ============================================================================
# MAIN
# ============================================================================
def main():
    inject_custom_css()

    if not st.session_state.autenticado:
        render_login_compacto(
            carregar_logo,
            remover_fundo_branco,
            fazer_login,
            fazer_login_visitante,
            fazer_cadastro
        )
    else:
        aplicar_css_mobile()
        aplicar_css_dashboard()

        if st.session_state.usuario_atual.get("tipo") == "visitante":
            nome_exibido = st.session_state.usuario_atual.get("nome", "Visitante")

            render_sidebar_premium(
                nome_exibido=nome_exibido,
                qtd_videos=0,
                qtd_contatos=0,
                qtd_cofre=0,
                qtd_memorias=0,
                is_admin=False,
                fazer_logout=fazer_logout
            )

            videos_visitante = db.listar_videos_por_contato(
                st.session_state.usuario_atual["id"]
            )

            qtd_videos = len(
                db.listar_videos_por_contato(
                    st.session_state.usuario_atual["id"]
                )
            )

            qtd_memorias = len(
                db.listar_memorias_usuario(
                    st.session_state.falecido_id
                )
            )

            qtd_contatos = len(
                db.listar_contatos_usuario(
                    st.session_state.falecido_id
                )
            )

            #qtd_documentos = len(
            #    db.listar_cofre_usuario(
            #        st.session_state.falecido_id
            #    )
            #)
            qtd_documentos = 0

            videos_visitante = db.listar_videos_por_contato(
                st.session_state.usuario_atual["id"]
            )

            abas = ["🕊️ Assistente Memorial"]

            if videos_visitante:
                abas.append(f"🎥 Mensagens ({len(videos_visitante)})")

            tabs = st.tabs(abas)

            with tabs[0]:
                render_assistente()

            indice = 1

            if videos_visitante:
                with tabs[indice]:
                    render_videos_visitante()
                indice += 1

            st.markdown("""
            <div class="footer-aeterna">
                <p>✨ aEterna - Assistente Memorial ✨</p>
            </div>
            """, unsafe_allow_html=True)

            return

        nome_exibido = st.session_state.usuario_atual.get(
            "nome_completo",
            "Usuário"
        )

        is_admin = (
                st.session_state.usuario_atual.get("tipo") == "admin"
        )

        #qtd_videos = len(
        #    db.listar_videos_usuario(
        #        st.session_state.usuario_atual["id"]
        #    )
        #)

        #qtd_contatos = len(
        #    db.listar_contatos_usuario(
        #        st.session_state.usuario_atual["id"]
        #    )
        #)

        qtd_videos = 0
        qtd_contatos = 0

        # Ajustaremos depois para dados reais
        qtd_cofre = 0
        qtd_memorias = 0

        render_sidebar_premium(
            nome_exibido=nome_exibido,
            qtd_videos=qtd_videos,
            qtd_contatos=qtd_contatos,
            qtd_cofre=qtd_cofre,
            qtd_memorias=qtd_memorias,
            is_admin=is_admin,
            fazer_logout=fazer_logout
        )

        if is_admin:
            tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "🏠 Painel",
                "💬 Assistente",
                "🎥 Vídeos",
                "👥 Família",
                "👤 Perfil",
                "📝 Lembranças",
                "🔒 Cofre",
                "👑 Admin"
            ])
            with tab0:
                render_painel_inicial(
                    nome_exibido,
                    qtd_videos,
                    qtd_contatos,
                    qtd_cofre,
                    qtd_memorias
                )
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
                render_cofre()
            with tab7:
                render_admin_panel()
        else:
            tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "🏠 Painel",
                "💬 Assistente",
                "🎥 Vídeos",
                "👥 Família",
                "👤 Perfil",
                "📝 Lembranças",
                "🔒 Cofre"
            ])
            with tab0:
                render_painel_inicial(
                    nome_exibido,
                    qtd_videos,
                    qtd_contatos,
                    qtd_cofre,
                    qtd_memorias
                )
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
                render_cofre()

        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna - Assistente de Luto com IA | Cofre Digital ✨</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()