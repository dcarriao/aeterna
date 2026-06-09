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
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }

        .chat-header-name {
            font-weight: bold;
            font-size: 0.8rem;
        }

        .chat-body {
            height: 280px;
            overflow-y: auto;
            padding: 10px;
            background: #e5ddd5;
            display: flex;
            flex-direction: column;
        }

        .message-row {
            display: flex;
            margin-bottom: 8px;
            width: 100%;
        }

        .message-row.user {
            justify-content: flex-end;
        }

        .message-row.bot {
            justify-content: flex-start;
        }

        .message-bubble {
            max-width: 85%;
            padding: 6px 10px;
            border-radius: 15px;
            font-size: 0.75rem;
            word-wrap: break-word;
        }

        .message-bubble.user {
            background: #dcf8c5;
            color: #075e54;
            border-bottom-right-radius: 3px;
        }

        .message-bubble.bot {
            background: white;
            color: #1a1a1a;
            border-bottom-left-radius: 3px;
        }

        .chat-footer {
            padding: 8px;
            background: white;
            border-top: 1px solid #eee;
        }

        .chat-warning {
            background: #fff3cd;
            padding: 4px 8px;
            font-size: 0.6rem;
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
            .chat-body { height: 200px; }
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
# TELA DE LOGIN (SIMPLIFICADA)
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
    nome_falecido = st.session_state.usuario_atual.get('nome_completo', 'seu ente querido')

    if 'historico_assistente' not in st.session_state:
        st.session_state.historico_assistente = []

    if not st.session_state.historico_assistente:
        st.session_state.historico_assistente.append(
            {"tipo": "bot", "texto": f"Olá! Sou uma simulação baseada em como {nome_falecido} era. 💚"})

    if 'assistente_obj' not in st.session_state:
        st.session_state.assistente_obj = AssistenteLuto(st.session_state.falecido_id)

    col_conteudo, col_chat = st.columns([2, 1])

    with col_conteudo:
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 15px;">
            <h3 style="color: #2E8B57;">🤖 Sobre o Assistente de Luto</h3>
            <p>O assistente foi treinado com a personalidade de <strong>{nome_falecido}</strong>.</p>
            <p><strong>Dicas:</strong></p>
            <ul>
                <li>💬 Pergunte sobre lembranças felizes</li>
                <li>💬 Peça conselhos</li>
                <li>💬 Compartilhe como está se sentindo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        logo = carregar_logo()
        if logo:
            st.image(logo, width=180)
        st.caption("aEterna - Assistente de Luto com IA")

    with col_chat:
        st.markdown(f"""
        <div class="chat-widget">
            <div class="chat-header">
                <div class="chat-avatar">🤖</div>
                <div class="chat-header-name">Conversar com {nome_falecido}</div>
            </div>
            <div class="chat-body">
        """, unsafe_allow_html=True)

        for msg in st.session_state.historico_assistente:
            if msg["tipo"] == "user":
                st.markdown(
                    f'<div class="message-row user"><div class="message-bubble user">{msg["texto"]}</div></div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-row bot"><div class="message-bubble bot">{msg["texto"]}</div></div>',
                            unsafe_allow_html=True)

        st.markdown("""
            </div>
            <div class="chat-warning">💡 Conversa simulada por IA</div>
            <div class="chat-footer">
        """, unsafe_allow_html=True)

        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                mensagem = st.text_input("msg", key="nova_mensagem", placeholder="Digite sua mensagem...",
                                         label_visibility="collapsed")
            with col2:
                enviar = st.form_submit_button("📤", use_container_width=True)

        st.markdown('</div></div>', unsafe_allow_html=True)

        if enviar and mensagem:
            st.session_state.historico_assistente.append({"tipo": "user", "texto": mensagem})
            with st.spinner("..."):
                resposta = st.session_state.assistente_obj.conversar(mensagem)
            st.session_state.historico_assistente.append({"tipo": "bot", "texto": resposta})
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
            titulo = st.text_input("Título *", key="titulo_video")
            destinatario = st.text_input("Para quem?", key="destinatario_video", placeholder="Ex: Para minha filha Ana")
            arquivo_video = st.file_uploader("Arquivo de vídeo", type=["mp4", "mov", "avi", "mkv"], key="video_file")

            if st.button("💾 Salvar", key="salvar_video", type="primary", use_container_width=True):
                if titulo and arquivo_video:
                    caminho = gerente_videos.salvar_video(arquivo_video, st.session_state.usuario_atual['id'], titulo,
                                                          destinatario)
                    db.adicionar_video(st.session_state.usuario_atual['id'], titulo, destinatario, caminho)
                    st.success(f"✅ {titulo} salvo!")
                    st.rerun()
                else:
                    st.error("❌ Preencha o título e selecione um vídeo")

    with col2:
        videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
        if not videos:
            st.info("📭 Nenhum vídeo cadastrado")
        else:
            for video in videos:
                with st.expander(f"🎬 {video['titulo']}"):
                    if video['destinatario']:
                        st.markdown(f"**👥 Para:** {video['destinatario']}")
                    st.video(video['caminho'])
                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        db.deletar_video(video['id'], st.session_state.usuario_atual['id'])
                        st.rerun()


# ============================================================================
# CONTATOS
# ============================================================================
def render_contatos():
    st.markdown("<h3 style='color: #2E8B57;'>👥 Contatos de Confiança</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Adicionar contato", expanded=False):
            nome = st.text_input("Nome *", key="contato_nome")
            sobrenome = st.text_input("Sobrenome", key="contato_sobrenome")
            email = st.text_input("E-mail *", key="contato_email")
            whatsapp = st.text_input("WhatsApp", key="contato_whatsapp")
            is_prioridade = st.checkbox("Prioritário", key="contato_prioridade")

            if st.button("💾 Salvar", type="primary", use_container_width=True):
                if nome and email:
                    chave_acesso = secrets.token_hex(8)
                    db.adicionar_contato(
                        usuario_id=st.session_state.usuario_atual['id'],
                        nome=nome,
                        sobrenome=sobrenome or "",
                        email=email,
                        telefone="",
                        whatsapp=whatsapp or "",
                        parentesco="",
                        is_prioridade=1 if is_prioridade else 0,
                        chave_acesso=chave_acesso
                    )
                    st.success(f"✅ {nome} {sobrenome} adicionado!")
                    st.info(f"🔑 Chave: {chave_acesso}")
                    st.rerun()
                else:
                    st.error("❌ Preencha nome e e-mail")

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
                    if st.button(f"🗑️ Remover", key=f"del_contato_{contato['id']}"):
                        db.deletar_contato(contato['id'], st.session_state.usuario_atual['id'])
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
        <h3>📅 Mensagens Programadas</h3>
        <p>Programe mensagens para datas especiais.</p>
    </div>
    <div class="info-card">
        <h3>🔒 Segurança e LGPD</h3>
        <p>✅ Criptografia<br>✅ Seus dados, sua chave<br>✅ LGPD Compliant</p>
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

        nome_exibido = st.session_state.usuario_atual.get('nome_completo', 'Usuário')
        is_admin = st.session_state.usuario_atual.get('tipo') == 'admin'

        with st.sidebar:
            st.markdown(f"### ✨ Olá, {nome_exibido}!")
            if st.button("🚪 Sair", use_container_width=True):
                fazer_logout()
            st.markdown("---")
            st.markdown("### 📊 Seu Legado")
            st.metric("📹 Vídeos", len(db.listar_videos_usuario(st.session_state.usuario_atual['id'])))
            st.metric("👥 Contatos", len(db.listar_contatos_usuario(st.session_state.usuario_atual['id'])))

        if is_admin:
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 Assistente", "📹 Vídeos", "👥 Contatos", "ℹ️ Sobre", "👑 Admin"])
            with tab1:
                render_assistente()
            with tab2:
                render_videos()
            with tab3:
                render_contatos()
            with tab4:
                render_sobre()
            with tab5:
                render_admin_panel()
        else:
            tab1, tab2, tab3, tab4 = st.tabs(["🤖 Assistente", "📹 Vídeos", "👥 Contatos", "ℹ️ Sobre"])
            with tab1:
                render_assistente()
            with tab2:
                render_videos()
            with tab3:
                render_contatos()
            with tab4:
                render_sobre()

        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna - Assistente de Luto com IA ✨</p>
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


if __name__ == "__main__":
    main()