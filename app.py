import streamlit as st
from PIL import Image
import os
import html
import base64
import mimetypes
from datetime import datetime
import secrets
from utils.banco import BancoDados
from utils.usuarios import GerenciadorUsuarios
from utils.upload_video import GerenciadorVideos
from styles.theme import aplicar_tema
from components.chat_luto import render_chat_luto
from components.login_compacto import render_login_compacto
from components.dashboard_ui import (
    aplicar_css_dashboard,
    render_sidebar_premium,
    render_painel_inicial
)
from components.mobile_ui import aplicar_css_mobile
from datetime import date
from utils.logger import logger
from utils.storage import StorageAeterna
from utils.mercado_pago_service import MercadoPagoService
from utils.media import exibir_foto_segura, exibir_video_seguro

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
    page_title="aEterna - Memórias Vivas",
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
storage = StorageAeterna()
mp_service = MercadoPagoService()

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
if 'modo_visualizacao' not in st.session_state:
    st.session_state.modo_visualizacao = "minha_historia"
if 'historia_atual_usuario_id' not in st.session_state:
    st.session_state.historia_atual_usuario_id = None
if 'historia_atual_nome' not in st.session_state:
    st.session_state.historia_atual_nome = None
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "inicio"


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
        st.session_state.modo_acesso = "usuario"
        st.session_state.modo_visualizacao = "minha_historia"
        st.session_state.pagina_atual = "inicio"
        st.session_state.historia_atual_usuario_id = usuario["id"]
        st.session_state.historia_atual_nome = usuario["nome_completo"]
        st.session_state.historico_assistente = []

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
    st.session_state.modo_visualizacao = "minha_historia"
    st.session_state.pagina_atual = "inicio"
    st.session_state.historia_atual_usuario_id = None
    st.session_state.historia_atual_nome = None
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

    tab1, tab2, tab3 = st.tabs(["📖 Entrar na minha história", "👋👨‍👩‍👧 Conhecer a história de alguém", "📝 Criar Conta"])

    with tab1:
        st.markdown("### Continue construindo sua história")
        with st.form("login_form"):
            email = st.text_input("E-mail", key="login_email")
            senha = st.text_input("Senha", type="password", key="login_senha")
            submitted = st.form_submit_button("🌿 ENTRAR", width="stretch", type="primary")
            if submitted:
                if email and senha:
                    if fazer_login(email, senha):
                        st.success("✅ Login realizado!")
                        logger.info(f"LOGIN_USUARIO: {email}")
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha incorretos")

    with tab2:
        st.markdown("### Conhecer a história de alguém")
        with st.form("visitante_form"):
            nome_visitante = st.text_input("Seu nome", key="visitante_nome")
            email_falecido = st.text_input("E-mail da pessoa responsável pela história", key="visitante_email")
            chave = st.text_input("Chave de acesso", type="password", key="visitante_chave")
            submitted = st.form_submit_button("📖 ACESSAR HISTÓRIA", width="stretch", type="primary")
            if submitted:
                if nome_visitante and email_falecido and chave:
                    if fazer_login_visitante(nome_visitante, chave, email_falecido):
                        st.success(f"✅ Bem-vindo(a), {nome_visitante}!")
                        logger.info(
                            f"LOGIN_VISITANTE: {nome_visitante} acessou história de {email_falecido}"
                        )
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

            submitted = st.form_submit_button("📝 CRIAR CONTA", width="stretch", type="primary")

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
# MINHA HISTORIA
# ============================================================================

ROTULOS_VISIBILIDADE = {
    "privado": "🔒 Somente eu",
    "contatos": "👥 Todos os meus contatos",
    "seletivo": "✨ Pessoas selecionadas",
}


def render_editor_visibilidade(
        tipo_conteudo: str,
        conteudo: dict,
        usuario_id: int,
        contatos: list,
        key_contexto: str = "",
):
    sufixo_key = f"_{key_contexto}" if key_contexto else ""
    visibilidade_atual = conteudo.get("visibilidade") or "contatos"
    st.caption(ROTULOS_VISIBILIDADE.get(visibilidade_atual, "👥 Todos os meus contatos"))

    with st.expander("Alterar quem pode ver"):
        opcoes = list(ROTULOS_VISIBILIDADE.keys())
        visibilidade = st.radio(
            "Quem pode ver este conteúdo?",
            opcoes,
            index=opcoes.index(visibilidade_atual),
            format_func=lambda valor: ROTULOS_VISIBILIDADE[valor],
            key=f"vis_{tipo_conteudo}_{conteudo['id']}{sufixo_key}",
        )

        contatos_atuais = db.listar_contatos_permitidos_conteudo(
            tipo_conteudo,
            conteudo["id"],
            usuario_id,
        )
        mapa_contatos = {
            contato["nome_completo"]: contato["id"]
            for contato in contatos
        }
        selecionados_nomes = []
        if visibilidade == "seletivo":
            selecionados_nomes = st.multiselect(
                "Escolha os contatos",
                list(mapa_contatos.keys()),
                default=[
                    nome for nome, contato_id in mapa_contatos.items()
                    if contato_id in contatos_atuais
                ],
                key=f"contatos_vis_{tipo_conteudo}_{conteudo['id']}{sufixo_key}",
            )

        if st.button(
            "Salvar visibilidade",
            key=f"salvar_vis_{tipo_conteudo}_{conteudo['id']}{sufixo_key}",
            use_container_width=True,
        ):
            contatos_ids = [
                mapa_contatos[nome]
                for nome in selecionados_nomes
            ]
            if visibilidade == "seletivo" and not contatos_ids:
                st.warning("Selecione pelo menos um contato.")
            elif db.atualizar_visibilidade_conteudo(
                tipo_conteudo,
                conteudo["id"],
                usuario_id,
                visibilidade,
                contatos_ids,
            ):
                st.success("Visibilidade atualizada.")
                st.rerun()
            else:
                st.error("Não foi possível atualizar a visibilidade.")


def render_minha_historia():
    memorias = db.listar_memorias_usuario(st.session_state.usuario_atual["id"])
    usuario_id = st.session_state.usuario_atual["id"]

    col_header, col_acao = st.columns([0.82, 0.18], vertical_alignment="center")
    with col_header:
        st.markdown(
            """
            <div class="ae-story-top">
                <h2>📖 Minha História</h2>
                <p>As histórias que você escolheu preservar.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_acao:
        rotulo_cta = (
            "➕ Contar uma História"
            if memorias
            else "➕ Contar minha primeira história"
        )
        if st.button(
            rotulo_cta,
            key="minha_historia_contar_historia",
            use_container_width=False,
        ):
            navegar_para("assistente")
            st.rerun()

    st.markdown('<div class="ae-story-header-rule"></div>', unsafe_allow_html=True)

    if not memorias:
        st.markdown(
            """
            <div class="ae-empty-story">
                <h3>📖 Sua história começa com o primeiro capítulo.</h3>
                <p>Quando você registrar a primeira lembrança, ela aparecerá aqui como o primeiro capítulo da sua coleção viva.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    fotos_por_memoria = db.listar_fotos_por_memorias_usuario(usuario_id)
    videos_por_memoria = db.listar_videos_por_memorias_usuario(usuario_id)
    contatos = db.listar_contatos_usuario(usuario_id)
    contribuicoes_por_memoria = carregar_contribuicoes_aprovadas_memorias(
        usuario_id
    )

    def resumo_memoria(memoria: dict) -> str:
        conteudo = (memoria.get("conteudo") or "").strip()
        if not conteudo:
            return "Uma história preservada na sua coleção."
        return conteudo[:145].rsplit(" ", 1)[0] + ("..." if len(conteudo) > 145 else "")

    def imagem_local_para_data_uri(caminho: str) -> str:
        try:
            if not caminho or not os.path.exists(caminho):
                return ""
            mime_type = mimetypes.guess_type(caminho)[0] or "image/jpeg"
            with open(caminho, "rb") as arquivo:
                encoded = base64.b64encode(arquivo.read()).decode("ascii")
            return f"data:{mime_type};base64,{encoded}"
        except Exception as exc:
            print("Erro ao preparar miniatura local:", exc)
            return ""

    def media_card_memoria(memoria: dict, classe_base: str = "ae-story-media") -> str:
        fotos = fotos_por_memoria.get(memoria["id"], [])
        videos = videos_por_memoria.get(memoria["id"], [])

        if fotos:
            caminho_foto = (fotos[0].get("caminho") or "").strip()
            imagem_src = caminho_foto if caminho_foto.startswith(("http://", "https://")) else imagem_local_para_data_uri(caminho_foto)
            if imagem_src:
                imagem_segura = html.escape(imagem_src, quote=True)
                return (
                    f'<div class="{classe_base} {classe_base}-photo">'
                    f'<img src="{imagem_segura}" alt="Miniatura da história">'
                    "</div>"
                )

        if videos:
            return (
                f'<div class="{classe_base} {classe_base}-video">'
                "<span>🎥</span>"
                "<strong>Vídeo</strong>"
                "</div>"
            )

        return (
            f'<div class="{classe_base} {classe_base}-fallback">'
            "<span>📖</span>"
            "<strong>História</strong>"
            "</div>"
        )

    def indicadores_memoria(memoria: dict) -> str:
        indicadores = []
        visibilidade = (memoria.get("visibilidade") or "contatos").lower()
        if visibilidade == "privado":
            indicadores.append("🔒 Privada")
        elif visibilidade == "seletivo":
            indicadores.append("👥 Seletiva")
        else:
            indicadores.append("🤝 Compartilhada")

        total_contribuicoes = len(
            contribuicoes_por_memoria.get(memoria["id"], [])
        )
        if total_contribuicoes:
            indicadores.append(f"💬 {total_contribuicoes} contribuição")

        return "".join(
            f"<span>{html.escape(indicador)}</span>" for indicador in indicadores
        )

    def render_card_memoria(memoria: dict, categoria: str, mostrar_categoria: bool = False):
        data_evento = memoria.get("data_evento") or ""
        titulo = html.escape(memoria.get("titulo") or "História sem título")
        data_evento_segura = html.escape(str(data_evento))
        resumo_seguro = html.escape(resumo_memoria(memoria))
        categoria_segura = html.escape(categoria)
        categoria_html = (
            f'<div class="ae-card-label">{categoria_segura}</div>'
            if mostrar_categoria
            else ""
        )
        card_html = (
            '<div class="ae-story-card">'
            f"{media_card_memoria(memoria)}"
            '<div class="ae-story-body">'
            f"{categoria_html}"
            f"<h3>{titulo}</h3>"
            f'<span class="ae-story-date">{data_evento_segura}</span>'
            f"<p>{resumo_seguro}</p>"
            f'<div class="ae-story-indicators">{indicadores_memoria(memoria)}</div>'
            "</div>"
            "</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)

    def mini_card_memoria_html(memoria: dict) -> str:
        titulo = html.escape(memoria.get("titulo") or "História sem título")
        data_evento = html.escape(str(memoria.get("data_evento") or ""))
        return (
            '<div class="ae-collection-mini-card">'
            f'{media_card_memoria(memoria, "ae-collection-mini-media")}'
            '<div class="ae-collection-mini-body">'
            f"<strong>{titulo}</strong>"
            f"<span>{data_evento}</span>"
            "</div>"
            "</div>"
        )

    def render_colecao_box(categoria: str, itens: list):
        categoria_nome = nome_categoria(categoria)
        titulo = html.escape(categoria_nome)
        mini_cards_itens = [
            mini_card_memoria_html(memoria)
            for memoria in itens[:3]
        ]
        while len(mini_cards_itens) < 3:
            mini_cards_itens.append(
                '<div class="ae-collection-mini-card ae-collection-mini-card-empty">'
                '<div class="ae-collection-mini-media ae-collection-mini-media-fallback">'
                "<span>📖</span>"
                "</div>"
                '<div class="ae-collection-mini-body">'
                "<strong>Próxima história</strong>"
                "<span>Aguardando novo capítulo</span>"
                "</div>"
                "</div>"
            )
        mini_cards = "".join(mini_cards_itens)
        st.markdown(
            (
                '<div class="ae-collection-box">'
                '<div class="ae-collection-head">'
                f'<h3>{icone_categoria(categoria)} {titulo}</h3>'
                '<span>Ver todas ›</span>'
                "</div>"
                '<div class="ae-collection-mini-grid">'
                f"{mini_cards}"
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    def render_detalhes_memoria(memoria: dict, key_contexto: str):
        if memoria.get("data_evento"):
            st.markdown(f"**Data:** {memoria['data_evento']}")
        if memoria.get("local"):
            st.markdown(f"**Local:** {memoria['local']}")
        if memoria.get("pessoas_relacionadas"):
            st.markdown(f"**Pessoas:** {memoria['pessoas_relacionadas']}")

        st.markdown(memoria.get("conteudo", ""))
        render_editor_visibilidade(
            "memoria",
            memoria,
            usuario_id,
            contatos,
            key_contexto=key_contexto,
        )
        render_contribuicoes_aprovadas(
            contribuicoes_por_memoria.get(memoria["id"], [])
        )

        fotos = fotos_por_memoria.get(memoria["id"], [])
        if fotos:
            st.markdown("**📷 Fotos desta história**")
            for foto in fotos:
                exibir_foto_segura(
                    foto.get("caminho"),
                    caption=foto.get("titulo", ""),
                )

        videos = videos_por_memoria.get(memoria["id"], [])
        if videos:
            st.markdown("**🎥 Vídeos desta história**")
            for video in videos:
                exibir_video_seguro(
                    video.get("caminho"),
                    legenda=video.get("titulo", ""),
                )

    def render_acesso_historia(memoria: dict, key_contexto: str):
        with st.popover("Ler história", use_container_width=False):
            render_detalhes_memoria(memoria, key_contexto)

    def render_prateleira(
            itens: list,
            categoria_nome: str,
            contexto: str,
            quantidade_colunas: int = 4,
    ):
        for inicio in range(0, len(itens), quantidade_colunas):
            colunas = st.columns(quantidade_colunas)
            for indice, coluna in enumerate(colunas):
                posicao = inicio + indice
                if posicao >= len(itens):
                    continue
                memoria = itens[posicao]
                key_contexto = f"{contexto}_{posicao}_{memoria['id']}"
                with coluna:
                    render_card_memoria(memoria, categoria_nome)
                    render_acesso_historia(memoria, key_contexto)

    def nome_categoria(categoria: str) -> str:
        categoria_normalizada = (categoria or "livre").lower()
        return {
            "livre": "Histórias da Vida",
            "outras histórias": "Histórias da Vida",
            "outros": "Histórias da Vida",
        }.get(categoria_normalizada, (categoria or "Histórias da Vida").title())

    def icone_categoria(categoria: str) -> str:
        categoria_normalizada = (categoria or "").lower()
        return {
            "família": "❤️",
            "familia": "❤️",
            "viagens": "✈️",
            "carreira": "💼",
            "estudos": "🎓",
            "infância": "👶",
            "infancia": "👶",
            "conquista": "🏆",
            "conquistas": "🏆",
            "amor": "💕",
            "valores": "🌟",
            "livre": "📚",
        }.get(categoria_normalizada, "📚")

    st.markdown('<div class="ae-story-section-title">Continue sua história</div>', unsafe_allow_html=True)
    render_prateleira(
        memorias[:4],
        "Continue",
        contexto="continue",
        quantidade_colunas=4,
    )

    grupos = {}
    for memoria in memorias:
        categoria = memoria.get("categoria") or "livre"
        grupos.setdefault(categoria, []).append(memoria)

    st.markdown('<div class="ae-story-section-title ae-story-section-title-collections">Coleções</div>', unsafe_allow_html=True)
    grupos_ordenados = sorted(
        grupos.items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )
    for inicio in range(0, len(grupos_ordenados), 3):
        colunas_colecoes = st.columns(3)
        for indice, coluna in enumerate(colunas_colecoes):
            posicao = inicio + indice
            if posicao >= len(grupos_ordenados):
                continue
            categoria, itens = grupos_ordenados[posicao]
            with coluna:
                render_colecao_box(categoria, itens)


# ============================================================================
# EXPERIÊNCIA DO VISITANTE
# ============================================================================

def render_cabecalho_visitante(nome_pessoa: str, nome_visitante: str):
    nome_pessoa_seguro = html.escape(nome_pessoa or "esta pessoa")
    nome_visitante_seguro = html.escape(nome_visitante or "Visitante")

    st.markdown(
        f"""
        <style>
        .ae-visitor-hero {{
            background:
                radial-gradient(circle at 84% 18%, rgba(212,168,79,0.24), transparent 30%),
                linear-gradient(135deg, #2B1747 0%, #45265f 68%, #6a3d73 100%);
            color: white;
            border: 1px solid rgba(212,168,79,0.42);
            border-radius: 28px;
            padding: 1.7rem 1.9rem;
            margin-bottom: 1.15rem;
            box-shadow: 0 18px 50px rgba(43,23,71,0.18);
        }}
        .ae-visitor-hero h1 {{
            color: #f2d89b;
            margin: 0 0 0.45rem;
            font-size: 2rem;
        }}
        .ae-visitor-hero p {{
            color: rgba(255,255,255,0.9);
            margin: 0.25rem 0;
            line-height: 1.55;
        }}
        .ae-visitor-card {{
            background: rgba(255,255,255,0.94);
            border: 1px solid rgba(212,168,79,0.28);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 28px rgba(43,23,71,0.07);
            margin-bottom: 0.8rem;
        }}
        </style>
        <div class="ae-visitor-hero">
            <h1>📖 A história de {nome_pessoa_seguro}</h1>
            <p><strong>{nome_visitante_seguro}</strong>, conheça histórias, momentos, aprendizados e memórias que {nome_pessoa_seguro} decidiu preservar.</p>
            <p>Este é um espaço de memórias vivas, criado para aproximar pessoas e gerações.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sobre_visitante(nome_pessoa: str, memorias: list, preferencias: dict):
    st.markdown(f"## 👤 Sobre {nome_pessoa}")

    resumo = preferencias.get("personalidade_extra", "").strip()
    if not resumo:
        for memoria in memorias:
            conteudo = (memoria.get("conteudo") or "").strip()
            if conteudo:
                resumo = conteudo[:420] + ("…" if len(conteudo) > 420 else "")
                break

    col_foto, col_resumo = st.columns([0.32, 0.68])

    with col_foto:
        try:
            foto_perfil = db.obter_foto_usuario(st.session_state.falecido_id)
        except Exception as exc:
            print("Erro ao carregar foto da pessoa:", exc)
            foto_perfil = None

        if foto_perfil:
            exibir_foto_segura(
                foto_perfil,
                caption=nome_pessoa,
                width="stretch",
            )
        else:
            st.info("Ainda não há uma foto de perfil compartilhada.")

    with col_resumo:
        if resumo:
            st.markdown(
                f'<div class="ae-visitor-card">{html.escape(resumo)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info(
                f"{nome_pessoa} ainda não registrou um resumo pessoal. "
                "Explore as outras seções para conhecer as histórias compartilhadas."
            )

        col1, col2, col3 = st.columns(3)
        col1.metric("Histórias", len(memorias))
        col2.metric(
            "Fotos",
            len(st.session_state.get("fotos_visitante_cache", [])),
        )
        col3.metric(
            "Vídeos",
            len(st.session_state.get("videos_visitante_cache", [])),
        )


def render_contribuicoes_aprovadas(contribuicoes: list):
    if not contribuicoes:
        return

    st.markdown("---")
    st.markdown("#### 🤝 Lembranças compartilhadas")

    for contribuicao in contribuicoes:
        nome = html.escape(
            contribuicao.get("contribuidor_nome") or "Pessoa convidada"
        )
        texto = html.escape(contribuicao.get("texto") or "").replace("\n", "<br>")
        st.markdown(
            f"""
            <div class="ae-visitor-card" style="border-left:4px solid #D4A84F;">
                <strong style="color:#2B1747;">Lembrança compartilhada por {nome}</strong>
                {f'<div style="margin-top:0.45rem;color:#51455b;line-height:1.55;">{texto}</div>' if texto else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )
        arquivo_url = contribuicao.get("arquivo_url")
        arquivo_tipo = contribuicao.get("arquivo_tipo", "")
        if arquivo_url:
            if arquivo_tipo.startswith("image/"):
                exibir_foto_segura(
                    arquivo_url,
                    caption=contribuicao.get("arquivo_nome", ""),
                )
            elif arquivo_tipo.startswith("video/"):
                exibir_video_seguro(
                    arquivo_url,
                    legenda=contribuicao.get("arquivo_nome", ""),
                )


def carregar_contribuicoes_aprovadas_memorias(usuario_id: int) -> dict:
    listar = getattr(db, "listar_contribuicoes_aprovadas_memorias", None)
    if not callable(listar):
        print("listar_contribuicoes_aprovadas_memorias indisponível no runtime.")
        return {}

    try:
        return listar(usuario_id) or {}
    except AttributeError as exc:
        print("Erro de atributo ao listar contribuições aprovadas:", exc)
        return {}
    except Exception as exc:
        print("Erro ao listar contribuições aprovadas:", exc)
        return {}


def render_form_contribuicao_memoria(
        memoria: dict,
        usuario_dono_id: int,
        usuario_logado: dict,
):
    memoria_id = memoria.get("id")
    if not memoria_id:
        return

    with st.expander("🤝 Adicionar lembrança"):
        st.markdown("**Compartilhe uma lembrança sobre este momento**")
        st.caption(
            "Sua contribuição será enviada ao dono da história e só aparecerá após aprovação."
        )

        with st.form(
            f"form_contribuicao_memoria_{usuario_dono_id}_{memoria_id}",
            clear_on_submit=True,
        ):
            texto = st.text_area(
                "Sua lembrança",
                placeholder="Conte um detalhe, uma lembrança ou um complemento para esta história.",
                height=130,
            )
            arquivo = st.file_uploader(
                "Foto ou vídeo (opcional)",
                type=["jpg", "jpeg", "png", "webp", "mp4", "mov", "webm"],
                key=f"arquivo_contribuicao_{usuario_dono_id}_{memoria_id}",
            )
            enviar = st.form_submit_button(
                "Enviar contribuição",
                type="primary",
                use_container_width=True,
            )

        if enviar:
            texto_normalizado = (texto or "").strip()
            if not texto_normalizado and not arquivo:
                st.warning("Escreva uma lembrança ou envie uma foto/vídeo para contribuir.")
                return

            email = usuario_logado.get("email", "")
            if not db.pode_contribuir_memoria(email, usuario_dono_id, memoria_id):
                st.error("Seu acesso a esta memória não está mais disponível.")
                return

            arquivo_url = arquivo_nome = arquivo_tipo = storage_bucket = storage_path = None
            arquivo_tamanho = None
            tipo_contribuicao = "texto"
            if arquivo:
                extensao = arquivo.name.rsplit(".", 1)[-1].lower()
                fotos_validas = {"jpg", "jpeg", "png", "webp"}
                videos_validos = {"mp4", "mov", "webm"}
                arquivo_tamanho = arquivo.size
                if extensao in fotos_validas:
                    if arquivo_tamanho > 10 * 1024 * 1024:
                        st.warning("A foto deve ter no máximo 10 MB.")
                        return
                    storage_bucket = "fotos"
                    tipo_midia = "foto"
                elif extensao in videos_validos:
                    if arquivo_tamanho > 100 * 1024 * 1024:
                        st.warning("O vídeo deve ter no máximo 100 MB.")
                        return
                    storage_bucket = "videos"
                    tipo_midia = "video"
                else:
                    st.warning("Formato de arquivo não permitido.")
                    return

                try:
                    upload = storage.upload_contribuicao(
                        storage_bucket,
                        arquivo,
                        usuario_dono_id,
                        memoria_id,
                    )
                except Exception as exc:
                    print("Erro no upload da contribuição:", exc)
                    st.error("Não foi possível enviar esta mídia agora.")
                    return

                arquivo_url = upload["url"]
                storage_path = upload["path"]
                arquivo_nome = arquivo.name
                arquivo_tipo = arquivo.type or (
                    f"image/{extensao}" if tipo_midia == "foto" else f"video/{extensao}"
                )
                tipo_contribuicao = (
                    f"texto_{tipo_midia}" if texto_normalizado else tipo_midia
                )

            try:
                contribuicao_id = db.criar_contribuicao(
                    email_contribuidor=usuario_logado.get("email", ""),
                    nome_contribuidor=(
                        usuario_logado.get("nome_completo")
                        or usuario_logado.get("nome")
                        or "Pessoa convidada"
                    ),
                    usuario_dono_id=usuario_dono_id,
                    memoria_id=memoria_id,
                    texto=texto_normalizado,
                    tipo_contribuicao=tipo_contribuicao,
                    arquivo_url=arquivo_url,
                    arquivo_nome=arquivo_nome,
                    arquivo_tipo=arquivo_tipo,
                    arquivo_tamanho=arquivo_tamanho,
                    storage_bucket=storage_bucket,
                    storage_path=storage_path,
                )
            except Exception as exc:
                print("Erro ao enviar contribuição:", exc)
                if storage_bucket and storage_path:
                    try:
                        storage.remover_arquivo(storage_bucket, storage_path)
                    except Exception:
                        pass
                st.error("Não foi possível enviar sua contribuição agora.")
                return

            if contribuicao_id:
                st.success("Sua contribuição foi enviada para aprovação.")
            else:
                if storage_bucket and storage_path:
                    try:
                        storage.remover_arquivo(storage_bucket, storage_path)
                    except Exception:
                        pass
                st.error(
                    "Não foi possível enviar esta contribuição. "
                    "Verifique se seu acesso à história continua ativo."
                )


def render_historias_visitante(
        memorias: list,
        usuario_dono_id: int = None,
        usuario_logado: dict = None,
        permitir_contribuicao: bool = False,
):
    st.markdown("## 📖 Histórias compartilhadas")

    if not memorias:
        st.info("Ainda não há histórias registradas para explorar.")
        return

    contribuicoes_por_memoria = {}
    if usuario_dono_id:
        contribuicoes_por_memoria = carregar_contribuicoes_aprovadas_memorias(
            usuario_dono_id
        )

    for memoria in memorias:
        titulo = memoria.get("titulo") or "História sem título"
        categoria = memoria.get("categoria") or "História"

        with st.expander(f"📚 {titulo} · {categoria.title()}"):
            conteudo = memoria.get("conteudo") or ""
            if conteudo:
                st.markdown(conteudo)
            else:
                st.info("Esta história ainda não possui uma descrição.")

            render_contribuicoes_aprovadas(
                contribuicoes_por_memoria.get(memoria.get("id"), [])
            )

            if (
                permitir_contribuicao
                and usuario_dono_id
                and usuario_logado
            ):
                render_form_contribuicao_memoria(
                    memoria,
                    usuario_dono_id,
                    usuario_logado,
                )


def render_aprendizados_visitante(memorias: list, preferencias: dict):
    st.markdown("## 🌟 Aprendizados e valores")

    itens = []

    personalidade = preferencias.get("personalidade_extra", "").strip()
    if personalidade:
        itens.append(("Valores e jeito de ser", personalidade))

    melhor_lembranca = preferencias.get("melhor_lembranca", "").strip()
    if melhor_lembranca:
        itens.append(("Uma lembrança importante", melhor_lembranca))

    dia_feliz = preferencias.get("dia_mais_feliz", "").strip()
    if dia_feliz:
        itens.append(("Um momento marcante", dia_feliz))

    categorias_aprendizado = (
        "valor",
        "aprend",
        "conselho",
        "ensinamento",
        "superação",
    )
    for memoria in memorias:
        categoria = (memoria.get("categoria") or "").lower()
        if any(termo in categoria for termo in categorias_aprendizado):
            conteudo = (memoria.get("conteudo") or "").strip()
            if conteudo:
                itens.append(
                    (memoria.get("titulo") or "Aprendizado compartilhado", conteudo)
                )

    if not itens:
        st.info(
            "Ainda não há aprendizados ou valores destacados. "
            "O Explorador de Histórias pode ajudar a descobrir o conteúdo já registrado."
        )
        return

    for titulo, conteudo in itens:
        st.markdown(
            f"""
            <div class="ae-visitor-card">
                <strong style="color:#2B1747;">{html.escape(titulo)}</strong>
                <div style="margin-top:0.35rem;color:#51455b;line-height:1.55;">{html.escape(conteudo)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================================
# CURADOR / EXPLORADOR DE HISTÓRIAS
# ============================================================================

def render_assistente():
    render_chat_luto()


# ============================================================================
# VÍDEOS
# ============================================================================
def render_videos():
    st.markdown("<h3 style='color: #2E8B57;'>📹 Vídeos da Minha História</h3>", unsafe_allow_html=True)

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

            try:
                videos = db.listar_videos_usuario(st.session_state.usuario_atual['id'])
            except Exception as e:
                st.error("Não foi possível carregar os vídeos agora. Tente novamente em alguns instantes.")
                print("Erro ao listar vídeos:", e)
                return

            try:
                contatos = db.listar_contatos_usuario(
                    st.session_state.usuario_atual["id"]
                )
            except Exception as e:
                print("Erro ao listar contatos para vídeo:", e)
                contatos = []

            with st.form("form_adicionar_video", clear_on_submit=True):
                titulo = st.text_input("Título *")

                categoria = st.selectbox(
                    "Categoria",
                    [
                        "Momento importante",
                        "Para pessoa específica",
                        "Para data especial"
                    ]
                )

                st.markdown("**👥 Quem pode ver este vídeo?**")

                contatos_selecionados = []
                opcoes_contato = {}
                visibilidade_video = st.radio(
                    "Visibilidade",
                    ["privado", "contatos", "seletivo"],
                    format_func=lambda valor: ROTULOS_VISIBILIDADE[valor],
                    key="visibilidade_novo_video",
                )

                if not contatos:
                    if visibilidade_video == "seletivo":
                        st.warning("⚠️ Cadastre contatos para usar o compartilhamento seletivo")
                else:
                    opcoes_contato = {
                        c["nome_completo"]: c["id"]
                        for c in contatos
                    }

                    contatos_selecionados_nomes = (
                        st.multiselect(
                            "Selecione os contatos que terão acesso ao vídeo",
                            list(opcoes_contato.keys())
                        )
                        if visibilidade_video == "seletivo"
                        else []
                    )

                    contatos_selecionados = [
                        opcoes_contato[nome]
                        for nome in contatos_selecionados_nomes
                    ]

                if categoria == "Para pessoa específica" and contatos:
                    destinatario_nome = st.selectbox(
                        "Para quem é este vídeo?",
                        list(opcoes_contato.keys())
                    )
                    destinatario = destinatario_nome
                else:
                    destinatario = st.text_input(
                        "Para quem é este vídeo? (opcional)",
                        placeholder="Ex: Para minha família"
                    )

                memorias = db.listar_memorias_usuario(
                    st.session_state.usuario_atual["id"]
                )

                memoria_id = None

                if memorias:
                    opcoes_memoria = {
                        "Não associar a nenhuma memória": None
                    }

                    for m in memorias:
                        titulo_memoria = m.get("titulo") or "Memória sem título"
                        opcoes_memoria[titulo_memoria] = m["id"]

                    memoria_escolhida = st.selectbox(
                        "Associar este vídeo a uma memória? (opcional)",
                        list(opcoes_memoria.keys())
                    )

                    memoria_id = opcoes_memoria[memoria_escolhida]
                else:
                    st.info("Você ainda não tem memórias salvas para associar este vídeo.")

                arquivo_video = st.file_uploader(
                    "Arquivo de vídeo",
                    type=["mp4", "mov", "avi", "mkv"]
                )

                st.caption("📹 Formatos aceitos: MP4, MOV, AVI, MKV")

                salvar_video = st.form_submit_button(
                    "💾 Salvar",
                    type="primary",
                    width="stretch"
                )

                if salvar_video:
                    if not titulo or not arquivo_video:
                        st.error("❌ Preencha o título e selecione um vídeo")
                    elif visibilidade_video == "seletivo" and not contatos_selecionados:
                        st.error("Selecione pelo menos um contato.")
                    else:
                        try:
                            upload = storage.upload_streamlit_file(
                                bucket="videos",
                                arquivo=arquivo_video,
                                usuario_id=st.session_state.usuario_atual["id"],
                                pasta="memorias"
                            )

                            caminho = upload["url"]

                            video_id = db.adicionar_video_com_acesso(
                                usuario_id=st.session_state.usuario_atual["id"],
                                titulo=titulo,
                                destinatario=destinatario,
                                caminho_arquivo=caminho,
                                contatos_ids=contatos_selecionados,
                                categoria=categoria,
                                visibilidade=visibilidade_video,
                            )

                            if memoria_id:
                                db.associar_video_memoria(
                                    memoria_id=memoria_id,
                                    video_id=video_id
                                )

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
                try:
                    contatos_acesso = db.listar_contatos_por_video(video['id'])
                    nomes_acesso = [c['nome_completo'] for c in contatos_acesso]
                except Exception as e:
                    print("Erro ao listar contatos do vídeo:", e)
                    contatos_acesso = []
                    nomes_acesso = []

                with st.expander(f"🎬 {video['titulo']} - {video.get('categoria', 'geral')}"):
                    if video.get('destinatario'):
                        st.markdown(f"**👥 Para:** {video['destinatario']}")
                    st.markdown(
                        f"**🔓 Acesso para:** "
                        f"{', '.join(nomes_acesso) if video.get('visibilidade') == 'seletivo' and nomes_acesso else ROTULOS_VISIBILIDADE.get(video.get('visibilidade', 'contatos'), 'Todos os contatos')}")
                    exibir_video_seguro(video.get("caminho"))
                    render_editor_visibilidade(
                        "video",
                        video,
                        st.session_state.usuario_atual["id"],
                        db.listar_contatos_usuario(
                            st.session_state.usuario_atual["id"]
                        ),
                    )

                    if st.button(f"🗑️ Remover", key=f"del_video_{video['id']}"):
                        db.deletar_video(video['id'], st.session_state.usuario_atual['id'])
                        st.rerun()

def render_videos_visitante(contato_id=None, nome_pessoa=None):
    usuario = st.session_state.usuario_atual
    contato_id = contato_id or usuario["id"]
    nome_falecido = (
        nome_pessoa
        or usuario.get("nome_falecido")
        or "essa pessoa"
    )

    st.markdown(
        f"<h3 style='color: #2E8B57;'>🎥 Vídeos compartilhados por {nome_falecido}</h3>",
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

            exibir_video_seguro(video.get("caminho"))


# ============================================================================
# FOTOS
# ============================================================================

def render_fotos():
    st.markdown("<h3 style='color: #2E8B57;'>📷 Álbum de Memórias</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("📷 Adicionar foto", expanded=False):
            with st.form("form_adicionar_foto", clear_on_submit=True):
                titulo = st.text_input("Título *")

                categoria = st.selectbox(
                    "Categoria",
                    [
                        "Família",
                        "Filhos",
                        "Casamento",
                        "Viagens",
                        "Infância",
                        "Amigos",
                        "Momentos especiais",
                    ],
                )

                descricao = st.text_area(
                    "Descrição",
                    placeholder="Conte brevemente o que essa foto representa...",
                    height=100,
                )

                with st.expander("Curador: história por trás da foto", expanded=False):
                    st.markdown("Vamos registrar a história por trás desta foto.")
                    st.markdown(
                        """
                        - Quem aparece nesta foto?
                        - Onde ela foi tirada?
                        - Em que época foi?
                        - O que estava acontecendo?
                        - Por que ela é importante para você?
                        """
                    )

                st.markdown("**👥 Quem pode ver esta foto?**")

                contatos = db.listar_contatos_usuario(
                    st.session_state.usuario_atual["id"]
                )

                visibilidade_foto = st.radio(
                    "Visibilidade",
                    ["privado", "contatos", "seletivo"],
                    format_func=lambda valor: ROTULOS_VISIBILIDADE[valor],
                    key="visibilidade_nova_foto",
                )

                if not contatos:
                    if visibilidade_foto == "seletivo":
                        st.warning("Cadastre contatos para usar o compartilhamento seletivo.")
                    contatos_selecionados = []
                else:
                    opcoes_contato = {
                        c["nome_completo"]: c["id"]
                        for c in contatos
                    }

                    contatos_selecionados_nomes = (
                        st.multiselect(
                            "Selecione os contatos que terão acesso à foto",
                            list(opcoes_contato.keys()),
                        )
                        if visibilidade_foto == "seletivo"
                        else []
                    )

                    contatos_selecionados = [
                        opcoes_contato[nome]
                        for nome in contatos_selecionados_nomes
                    ]
                memorias = db.listar_memorias_usuario(
                    st.session_state.usuario_atual["id"]
                )

                memoria_id = None

                if memorias:
                    opcoes_memoria = {
                        "Não associar a nenhuma memória": None
                    }

                    for m in memorias:
                        titulo = m.get("titulo") or "Memória sem título"
                        opcoes_memoria[titulo] = m["id"]

                    memoria_escolhida = st.selectbox(
                        "Associar esta foto a uma memória? (opcional)",
                        list(opcoes_memoria.keys())
                    )

                    memoria_id = opcoes_memoria[memoria_escolhida]
                else:
                    st.info("Você ainda não tem memórias salvas para associar esta foto.")
                arquivo_foto = st.file_uploader(
                    "Arquivo de foto",
                    type=["png", "jpg", "jpeg", "webp"],
                )

                salvar = st.form_submit_button(
                    "💾 Salvar foto",
                    type="primary",
                    width="stretch",
                )

                if salvar:
                    if not titulo or not arquivo_foto:
                        st.error("Informe um título e selecione uma foto.")
                    elif visibilidade_foto == "seletivo" and not contatos_selecionados:
                        st.error("Selecione pelo menos um contato.")
                    else:
                        try:
                            upload = storage.upload_streamlit_file(
                                bucket="fotos",
                                arquivo=arquivo_foto,
                                usuario_id=st.session_state.usuario_atual["id"],
                                pasta="memorias"
                            )

                            caminho = upload["url"]

                            foto_id = db.adicionar_foto_com_acesso(
                                usuario_id=st.session_state.usuario_atual["id"],
                                titulo=titulo,
                                descricao=descricao,
                                categoria=categoria,
                                caminho_arquivo=caminho,
                                contatos_ids=contatos_selecionados,
                                visibilidade=visibilidade_foto,
                            )

                            if memoria_id:
                                db.associar_foto_memoria(
                                    memoria_id=memoria_id,
                                    foto_id=foto_id
                                )

                            st.success("Foto salva com sucesso.")
                            st.rerun()

                        except Exception as e:
                            st.error(f"Erro ao salvar foto: {e}")
                            print("ERRO AO SALVAR FOTO:", e)

    with col2:
        fotos = db.listar_fotos_usuario(
            st.session_state.usuario_atual["id"]
        )

        if not fotos:
            st.info("📭 Nenhuma foto cadastrada.")
        else:
            for foto in fotos:
                contatos_acesso = db.listar_contatos_por_foto(foto["id"])
                nomes_acesso = [
                    c["nome_completo"]
                    for c in contatos_acesso
                ]

                with st.expander(f"📷 {foto['titulo']} - {foto.get('categoria', '')}"):
                    if foto.get("descricao"):
                        st.markdown(foto["descricao"])

                    st.markdown(
                        "**Acesso para:** {}".format(
                            ", ".join(nomes_acesso)
                            if foto.get("visibilidade") == "seletivo" and nomes_acesso
                            else ROTULOS_VISIBILIDADE.get(
                                foto.get("visibilidade", "contatos"),
                                "Todos os contatos",
                            )
                        )
                    )

                    exibir_foto_segura(
                        foto.get("caminho"),
                        caption=foto.get("titulo", ""),
                    )
                    render_editor_visibilidade(
                        "foto",
                        foto,
                        st.session_state.usuario_atual["id"],
                        db.listar_contatos_usuario(
                            st.session_state.usuario_atual["id"]
                        ),
                    )

                    if st.button(
                        "🗑️ Remover",
                        key=f"del_foto_{foto['id']}",
                    ):
                        db.deletar_foto(
                            foto["id"],
                            st.session_state.usuario_atual["id"],
                        )
                        st.rerun()

def render_fotos_visitante(contato_id=None, nome_pessoa=None):
    usuario = st.session_state.usuario_atual
    contato_id = contato_id or usuario["id"]
    nome_falecido = (
        nome_pessoa
        or usuario.get("nome_falecido")
        or "essa pessoa"
    )

    st.markdown(
        f"<h3 style='color: #2E8B57;'>📷 Fotos compartilhadas por {nome_falecido}</h3>",
        unsafe_allow_html=True
    )

    fotos = db.listar_fotos_por_contato(contato_id)

    if not fotos:
        st.info("📭 Nenhuma foto foi liberada para você.")
        return

    for foto in fotos:
        with st.expander(f"📷 {foto['titulo']} - {foto.get('categoria', '')}"):
            if foto.get("descricao"):
                st.markdown(foto["descricao"])

            exibir_foto_segura(
                foto.get("caminho"),
                caption=foto.get("titulo", ""),
            )

# ============================================================================
# CONTATOS (COMPLETO)
# ============================================================================
def render_contatos():
    plano = db.obter_plano_usuario(st.session_state.usuario_atual['id'])
    contatos_atual = db.contar_contatos_usuario(st.session_state.usuario_atual['id'])
    max_contatos = plano.get("max_contatos", 10) if plano else 10
    prioridades_atual = db.contar_contatos_prioritarios(st.session_state.usuario_atual['id'])
    max_prioridades = plano.get("max_prioridades", 3) if plano else 3
    contatos = db.listar_contatos_usuario(st.session_state.usuario_atual['id'])

    st.markdown(
        """
        <div class="ae-people-hero">
            <div>
                <h2>👥 Pessoas Importantes</h2>
                <p>As pessoas que fazem parte da sua história.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("contato_salvo_msg"):
        st.success(st.session_state.contato_salvo_msg)
        st.code(st.session_state.contato_chave_msg)

        if st.button("Ocultar chave"):
            del st.session_state.contato_salvo_msg
            del st.session_state.contato_chave_msg
            st.rerun()

    with st.expander("➕ Adicionar Pessoa Importante", expanded=False):
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
                "Relação",
                ["", "Filho(a)", "Cônjuge", "Irmão(ã)", "Amigo(a)", "Advogado(a)", "Primo(a)", "Outro"]
            )

            data_nascimento = st.date_input(
                "Data de nascimento",
                value=date(1990, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

            is_prioridade = st.checkbox("Marcar como pessoa prioritária")

            acesso_central_luto = st.checkbox(
                "Permitir explorar histórias compartilhadas",
                value=False
            )

            salvar = st.form_submit_button(
                "💾 Salvar pessoa importante",
                type="primary",
                width="stretch"
            )

            if salvar:
                if not nome or not sobrenome:
                    st.error("❌ Nome e sobrenome são obrigatórios")
                elif not email and not whatsapp:
                    st.error("❌ Informe pelo menos um contato (e-mail ou WhatsApp)")
                elif is_prioridade and prioridades_atual >= max_prioridades:
                    st.warning(
                        f"⚠️ Você já tem {prioridades_atual} pessoas prioritárias. "
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

    try:
        memorias_usuario = db.listar_memorias_usuario(st.session_state.usuario_atual["id"])
    except Exception as exc:
        print("Erro ao carregar presenças nas histórias:", exc)
        memorias_usuario = []

    presencas = {}
    for contato in contatos:
        nome_contato = (contato.get("nome") or "").strip().lower()
        nome_completo = (contato.get("nome_completo") or "").strip().lower()
        if not nome_contato and not nome_completo:
            continue
        total = 0
        for memoria in memorias_usuario:
            texto_busca = " ".join([
                str(memoria.get("titulo") or ""),
                str(memoria.get("conteudo") or ""),
                str(memoria.get("pessoas_relacionadas") or ""),
            ]).lower()
            if nome_completo and nome_completo in texto_busca:
                total += 1
            elif nome_contato and nome_contato in texto_busca:
                total += 1
        if total:
            presencas[contato["id"]] = total

    def contexto_pessoa(contato: dict) -> str:
        if contato.get("acesso_central_luto"):
            return "Pode ver algumas das suas histórias"
        if contato.get("email"):
            return "Pode contribuir com suas histórias"
        if contato.get("whatsapp"):
            return "Recebe mensagens futuras"
        return "Faz parte da sua história"

    def indicadores_pessoa(contato: dict) -> str:
        itens = []
        if presencas.get(contato["id"]):
            itens.append(f"📖 {presencas[contato['id']]} histórias")
        if contato.get("acesso_central_luto"):
            itens.append("🔐 acesso ativo")
        if contato.get("is_prioridade"):
            itens.append("⭐ prioridade")
        if not itens:
            itens.append("🤝 pessoa importante")
        return "".join(f"<span>{html.escape(item)}</span>" for item in itens[:3])

    if not contatos:
        st.markdown(
            """
            <div class="ae-people-empty">
                <h3>👥 Sua história é construída com outras pessoas.</h3>
                <p>Adicione familiares, amigos ou pessoas importantes para compartilhar histórias e memórias.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("➕ Adicionar minha primeira pessoa", key="primeira_pessoa", use_container_width=False):
            st.info("Abra o bloco “Adicionar Pessoa Importante” acima para começar.")
        return

    ranking = sorted(
        (
            (contato, presencas.get(contato["id"], 0))
            for contato in contatos
            if presencas.get(contato["id"], 0)
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    if ranking:
        top_html = "".join(
            f"<span>{html.escape(contato.get('nome_completo') or contato.get('nome') or 'Pessoa')} apareceu em {total} histórias</span>"
            for contato, total in ranking[:3]
        )
        st.markdown(
            f"""
            <div class="ae-people-presentes">
                <strong>Pessoas mais presentes nas suas histórias</strong>
                <div>{top_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="ae-people-grid-title">Todas as pessoas importantes</div>', unsafe_allow_html=True)
    for inicio in range(0, len(contatos), 3):
        colunas = st.columns(3)
        for indice, coluna in enumerate(colunas):
            posicao = inicio + indice
            if posicao >= len(contatos):
                continue
            contato = contatos[posicao]
            nome_exibido = contato.get("nome_completo") or contato.get("nome") or "Pessoa"
            inicial = html.escape(nome_exibido[:1].upper() or "P")
            relacao = contato.get("parentesco") or "Relação importante"
            with coluna:
                st.markdown(
                    f"""
                    <div class="ae-important-person-card">
                        <div class="ae-important-avatar">{inicial}</div>
                        <h3>{html.escape(nome_exibido)} {'⭐' if contato.get('is_prioridade') else ''}</h3>
                        <strong>{html.escape(relacao)}</strong>
                        <p>{html.escape(contexto_pessoa(contato))}</p>
                        <div class="ae-important-indicators">{indicadores_pessoa(contato)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with st.expander(f"Ver relação de {nome_exibido}", expanded=False):
                    st.markdown(f"**Relação:** {html.escape(relacao)}")
                    st.markdown(f"**Histórias em que aparece:** {presencas.get(contato['id'], 0)}")
                    st.markdown(
                        "**Permissões atuais:** "
                        + (
                            "Pode explorar histórias compartilhadas"
                            if contato.get("acesso_central_luto")
                            else "Acesso direto não habilitado"
                        )
                    )
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
    st.markdown("<h3 style='color: #2E8B57;'>👤 Minha Essência</h3>", unsafe_allow_html=True)
    st.info(
        "Essas informações ajudam o Curador e o Explorador da aEterna "
        "a compreender melhor sua história, seus valores, gostos e lembranças importantes."
    )

    usuario_id = st.session_state.usuario_atual["id"]

    st.markdown("### 📷 Sua foto")

    foto_atual = db.obter_foto_usuario(usuario_id)

    exibir_foto_segura(
        foto_atual,
        caption="Sua foto atual",
        width=180,
    )

    with st.form("form_foto_perfil_usuario", clear_on_submit=True):
        foto_usuario = st.file_uploader(
            "Adicione uma foto sua ao seu perfil",
            type=["png", "jpg", "jpeg", "webp"]
        )

        salvar_foto = st.form_submit_button(
            "💾 Salvar foto",
            type="primary",
            width="stretch"
        )

        if salvar_foto:
            if not foto_usuario:
                st.error("Selecione uma foto.")
            else:
                try:
                    upload = storage.upload_streamlit_file(
                        bucket="perfis",
                        arquivo=foto_usuario,
                        usuario_id=usuario_id,
                        pasta="usuario"
                    )

                    caminho = upload["url"]

                    db.atualizar_foto_usuario(usuario_id, caminho)

                    st.success("Foto de perfil atualizada.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro ao salvar foto de perfil: {e}")

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

        st.markdown("**🌟 Como você gostaria de ser lembrado?**")
        personalidade_extra = st.text_area("Algo mais que você quer registrar sobre você?",
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
# PLANOS
# ============================================================================
def render_planos():
    st.markdown("<h3 style='color:#2E8B57;'>💎 Planos aEterna</h3>", unsafe_allow_html=True)

    st.markdown("""
    ### Preserve sua história para as próximas gerações
    Escolha o plano que combina melhor com a história que você deseja guardar.
    """)

    planos = [
        {
            "nome": "🌱 Essencial",
            "preco": 0,
            "descricao": "Comece a registrar sua história.",
            "visivel": True,
            "beneficios": ["20 histórias", "5 fotos", "2 vídeos", "1 mensagem para o futuro", "1 pessoa convidada", "Preservação por 2 anos"]
        },
        {
            "nome": "👨‍👩‍👧 Família",
            "preco": 12,
            "parcelado": "12x de R$ 14,99",
            "descricao": "Para preservar as principais memórias da família.",
            "recomendado": True,
            "visivel": True,
            "beneficios": ["60 histórias", "20 fotos", "10 vídeos", "5 pessoas convidadas", "5 mensagens para o futuro", "Preservação por 5 anos"]
        },
        {
            "nome": "❤️ História Completa",
            "preco": 189,
            "descricao": "Para construir uma história familiar mais completa.",
            "visivel": True,
            "beneficios": ["80 histórias", "30 fotos", "15 vídeos", "10 pessoas convidadas", "10 mensagens para o futuro", "Preservação por 8 anos"]
        },
        {
            "nome": "👑 Gerações",
            "preco": 299,
            "descricao": "Para famílias que querem preservar mais momentos.",
            "visivel": True,
            "beneficios": ["100 histórias", "50 fotos", "25 vídeos", "30 pessoas convidadas", "30 mensagens para o futuro", "Preservação por 15 anos"]
        },
        {
            "nome": "✨ Permanente",
            "preco": 1499,
            "descricao": "Para preservar sua história sem prazo definido.",
            "visivel": False,
            "beneficios": ["Tudo ilimitado", "Preservação contínua", "Atualizações futuras incluídas"]
        }
    ]

    planos_visiveis = [p for p in planos if p.get("visivel", True)]
    for linha in range(0, len(planos_visiveis), 2):
        cols = st.columns(2)

        for idx, plano in enumerate(planos_visiveis[linha:linha + 2]):
            i = linha + idx

            with cols[idx]:
                with st.container(border=True):
                    if plano.get("recomendado"):
                        st.markdown("### ⭐ RECOMENDADO")
                    st.markdown(f"## {plano['nome']}")
                    st.caption(plano["descricao"])

                    if plano["preco"] == 0:
                        st.markdown("### Gratuito")
                    else:
                        st.markdown(f"### {plano.get('parcelado', '')}")

                        st.caption(
                            f"ou R$ {plano['preco']:.2f} à vista".replace(".", ",")
                        )

                    for item in plano["beneficios"]:
                        st.markdown(f"✓ {item}")

                    if plano["preco"] > 0:
                        if st.button(f"Quero o plano {plano['nome']}", key=f"plano_{i}", width="stretch"):
                            db.registrar_interesse_plano(
                                st.session_state.usuario_atual["id"],
                                plano["nome"],
                                plano["preco"]
                            )

                            link_pagamento = mp_service.criar_checkout_plano(
                                usuario_id=st.session_state.usuario_atual["id"],
                                plano_nome=plano["nome"],
                                valor=plano["preco"]
                            )

                            if link_pagamento:
                                st.success("Checkout criado com sucesso.")
                                st.link_button(
                                    "💳 Prosseguir para pagamento",
                                    link_pagamento,
                                    width="stretch"
                                )
                            else:
                                st.error("Não foi possível gerar o link de pagamento.")


# ============================================================================
# LEMBRANÇAS PROGRAMADAS (AGENDAMENTOS)
# ============================================================================
def render_agendamentos():
    st.markdown(
        "<h3 style='color: #2E8B57;'>💌 Mensagens para o Futuro</h3>",
        unsafe_allow_html=True
    )

    st.info(
        "Deixe mensagens e vídeos para serem entregues em momentos importantes "
        "da vida das pessoas que você ama."
    )

    st.markdown("### 🎉 Datas que marcaram minha vida")

    with st.expander("➕ Cadastrar uma data importante", expanded=False):
        with st.form("form_data_importante", clear_on_submit=True):
            titulo_data = st.text_input(
                "Título da data",
                placeholder="Ex: Aniversário da filha, Aniversário de casamento, Férias..."
            )

            tipo_data = st.selectbox(
                "Tipo",
                [
                    "Aniversário",
                    "Casamento",
                    "Nascimento",
                    "Conquista",
                    "Viagem",
                    "Data familiar",
                    "Outra"
                ]
            )

            contatos = db.listar_contatos_usuario(
                st.session_state.usuario_atual["id"]
            )

            contato_id = None

            if contatos:
                opcoes_contato = {"Nenhum contato específico": None}

                for c in contatos:
                    opcoes_contato[c["nome_completo"]] = c["id"]

                contato_nome = st.selectbox(
                    "Relacionar a algum contato? (opcional)",
                    list(opcoes_contato.keys())
                )

                contato_id = opcoes_contato[contato_nome]

            data_evento = st.date_input(
                "Data",
                value=datetime.now().date()
            )

            recorrente = st.checkbox(
                "Repetir todos os anos",
                value=True
            )

            observacoes = st.text_area(
                "Observações",
                placeholder="Ex: nesta data quero lembrar de registrar algo especial..."
            )

            salvar_data = st.form_submit_button(
                "💾 Salvar data importante",
                type="primary",
                width="stretch"
            )

            if salvar_data:
                if not titulo_data:
                    st.error("Informe um título para a data.")
                else:
                    db.criar_data_importante(
                        usuario_id=st.session_state.usuario_atual["id"],
                        titulo=titulo_data,
                        data_evento=data_evento.strftime("%Y-%m-%d"),
                        tipo=tipo_data,
                        contato_id=contato_id,
                        recorrente=recorrente,
                        observacoes=observacoes
                    )

                    st.success("Data importante cadastrada.")
                    st.rerun()
    datas_importantes = db.listar_datas_importantes_usuario(
        st.session_state.usuario_atual["id"]
    )

    if datas_importantes:
        for data in datas_importantes:
            with st.expander(f"📌 {data['titulo']} - {data['data_evento']}"):
                if data.get("tipo"):
                    st.markdown(f"**Tipo:** {data['tipo']}")

                if data.get("contato_nome"):
                    st.markdown(f"**Contato relacionado:** {data['contato_nome']}")

                st.markdown(
                    f"**Recorrente:** {'Sim' if data.get('recorrente') else 'Não'}"
                )

                if data.get("observacoes"):
                    st.markdown(data["observacoes"])

                if st.button(
                        "🗑️ Remover data",
                        key=f"del_data_importante_{data['id']}"
                ):
                    db.deletar_data_importante(
                        data["id"],
                        st.session_state.usuario_atual["id"]
                    )
                    st.rerun()
    else:
        st.info("Você ainda não cadastrou datas importantes.")

    plano = db.obter_plano_usuario(st.session_state.usuario_atual['id'])

    if not plano.get("tem_agendamento", False):
        st.info("💡 Esta funcionalidade estará disponível em breve nos planos pagos!")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("➕ Criar nova mensagem para o futuro", expanded=False):
            contatos = db.listar_contatos_usuario(st.session_state.usuario_atual["id"])

            if not contatos:
                st.warning("⚠️ Cadastre um contato primeiro")
            else:
                with st.form("form_mensagem_futuro", clear_on_submit=True):
                    opcoes_contato = {c["nome_completo"]: c for c in contatos}

                    contato_selecionado_nome = st.selectbox(
                        "Para quem?",
                        list(opcoes_contato.keys())
                    )

                    contato_selecionado = opcoes_contato[contato_selecionado_nome]
                    contato_id = contato_selecionado["id"]

                    if not contato_selecionado.get("email"):
                        st.warning(
                            "⚠️ Este contato não tem e-mail cadastrado. "
                            "Adicione um e-mail para receber mensagens."
                        )

                    tipo = st.selectbox(
                        "Tipo de mensagem",
                        ["texto", "vídeo"]
                    )

                    col_d1, col_d2 = st.columns(2)

                    with col_d1:
                        data_envio = st.date_input(
                            "Data de envio",
                            min_value=datetime.now().date()
                        )

                    with col_d2:
                        data_termino = st.date_input(
                            "Data de término (opcional)",
                            value=None
                        )

                    forma_envio = st.selectbox(
                        "Como enviar?",
                        ["E-mail", "WhatsApp (em breve)"]
                    )

                    conteudo = ""
                    video_id = None
                    gerar_por_ia = 0

                    if tipo == "texto":
                        opcao_texto = st.radio(
                            "Como criar?",
                            ["Escrever manualmente", "Receber perguntas do Curador (em breve)"]
                        )

                        if opcao_texto == "Escrever manualmente":
                            conteudo = st.text_area(
                                "Digite sua mensagem:",
                                height=150
                            )
                        else:
                            st.info("Em breve, o Curador ajudará você com perguntas simples para organizar esta mensagem.")
                            conteudo = st.text_area(
                                "Digite sua mensagem:",
                                height=150
                            )
                            gerar_por_ia = 1

                    else:
                        videos = db.listar_videos_usuario(
                            st.session_state.usuario_atual["id"]
                        )

                        if videos:
                            opcoes_video = {
                                v["titulo"]: v["id"]
                                for v in videos
                            }

                            video_selecionado = st.selectbox(
                                "Selecione um vídeo",
                                list(opcoes_video.keys())
                            )

                            video_id = opcoes_video[video_selecionado]
                        else:
                            st.warning("⚠️ Você não tem vídeos cadastrados.")

                    ocasiao = st.selectbox(
                        "Ocasião",
                        [
                            "Aniversário",
                            "Natal",
                            "Ano Novo",
                            "Dia dos Pais",
                            "Dia das Mães",
                            "Aniversário de Casamento",
                            "Formatura",
                            "Nascimento de Filho(a)",
                            "Mensagem Personalizada"
                        ]
                    )

                    if ocasiao == "Mensagem Personalizada":
                        data_especial = st.text_input(
                            "Descreva a ocasião"
                        )
                    else:
                        data_especial = ocasiao

                    salvar_agendamento = st.form_submit_button(
                        "💾 Agendar mensagem",
                        type="primary",
                        width="stretch"
                    )

                    if salvar_agendamento:
                        if tipo == "texto" and not conteudo:
                            st.error("❌ Digite uma mensagem")
                        elif tipo == "vídeo" and not video_id:
                            st.error("❌ Selecione um vídeo")
                        elif forma_envio == "E-mail" and not contato_selecionado.get("email"):
                            st.error("❌ Este contato não tem e-mail cadastrado")
                        else:
                            mensagem_final = conteudo

                            if data_especial and tipo == "texto":
                                mensagem_final = f"✨ {data_especial} ✨\n\n{conteudo}"

                            db.criar_agendamento(
                                usuario_id=st.session_state.usuario_atual["id"],
                                contato_id=contato_id,
                                tipo=tipo,
                                data_envio=data_envio.strftime("%Y-%m-%d"),
                                data_termino=data_termino.strftime("%Y-%m-%d") if data_termino else "",
                                conteudo=mensagem_final,
                                video_id=video_id,
                                gerar_por_ia=gerar_por_ia
                            )

                            st.success(
                                f"✅ Mensagem agendada para {data_envio.strftime('%d/%m/%Y')}!"
                            )

                            if forma_envio == "E-mail":
                                st.info(
                                    f"📧 Será enviada por e-mail para {contato_selecionado['email']}"
                                )

                            st.rerun()

    with col2:
        agendamentos = db.listar_agendamentos_usuario(st.session_state.usuario_atual['id'])
        if not agendamentos:
            st.info("📭 Nenhuma mensagem para o futuro programada.")
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

                if st.button("💾 Salvar", key="salvar_senha", type="primary", width="stretch"):
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

                if st.button("💾 Salvar", key="salvar_doc", type="primary", width="stretch"):
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

                        if doc['nome_original'].lower().endswith(('.png', '.jpg', '.jpeg')):
                            exibir_foto_segura(
                                doc.get("caminho_arquivo"),
                                caption=doc.get("titulo", ""),
                                width=150,
                            )
                        elif doc['nome_original'].lower().endswith('.pdf'):
                            try:
                                caminho_documento = doc.get("caminho_arquivo") or ""
                                if caminho_documento and os.path.exists(caminho_documento):
                                    with open(caminho_documento, "rb") as f:
                                        st.download_button(
                                            "📄 Baixar PDF",
                                            f,
                                            file_name=doc['nome_original'],
                                        )
                                else:
                                    st.warning("📄 Este documento não está disponível neste ambiente.")
                            except Exception as exc:
                                print("Erro ao carregar documento:", exc)
                                st.warning("📄 Não foi possível carregar este documento agora.")

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
        <h3>📖 Histórias que atravessam gerações</h3>
        <p>Registre momentos, aprendizados e experiências importantes.</p>
    </div>
    <div class="info-card">
        <h3>📷 Álbum de Memórias</h3>
        <p>Guarde fotos e vídeos que contam quem você é.</p>
    </div>
    <div class="info-card">
        <h3>💌 Mensagens para o Futuro</h3>
        <p>Compartilhe palavras importantes em momentos especiais.</p>
    </div>
    <div class="info-card">
        <h3>👨‍👩‍👧‍👦 Pessoas Importantes</h3>
        <p>Conecte familiares e pessoas queridas à sua história.</p>
    </div>
    <div class="info-card">
        <h3>🔒 Segurança e Privacidade</h3>
        <p>Sua história protegida e sob seu controle.</p>
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
# REDE PRIVADA DE HISTÓRIAS
# ============================================================================
def selecionar_minha_historia():
    usuario = st.session_state.usuario_atual or {}
    st.session_state.modo_visualizacao = "minha_historia"
    st.session_state.historia_atual_usuario_id = usuario.get("id")
    st.session_state.historia_atual_nome = usuario.get("nome_completo")
    st.session_state.historico_assistente = []
    st.session_state.pop("assistente_obj", None)
    st.session_state.pop("assistente_modo", None)
    st.session_state.pop("assistente_usuario_id", None)
    st.session_state.pop("assistente_contato_id", None)


def selecionar_historia_compartilhada(historia: dict):
    st.session_state.modo_visualizacao = "historia_compartilhada"
    st.session_state.historia_atual_usuario_id = historia["usuario_id"]
    st.session_state.historia_atual_nome = historia.get("nome_completo")
    st.session_state.historico_assistente = []
    st.session_state.pop("assistente_obj", None)
    st.session_state.pop("assistente_modo", None)
    st.session_state.pop("assistente_usuario_id", None)
    st.session_state.pop("assistente_contato_id", None)


def formatar_novidades_historia(novidades: dict) -> str:
    partes = []
    memorias = int(novidades.get("memorias", 0) or 0)
    fotos = int(novidades.get("fotos", 0) or 0)
    videos = int(novidades.get("videos", 0) or 0)

    if memorias:
        partes.append(
            f"{memorias} nova história"
            if memorias == 1
            else f"{memorias} novas histórias"
        )
    if fotos:
        partes.append(
            f"{fotos} nova foto"
            if fotos == 1
            else f"{fotos} novas fotos"
        )
    if videos:
        partes.append(
            f"{videos} novo vídeo"
            if videos == 1
            else f"{videos} novos vídeos"
        )

    return " · ".join(partes) if partes else "Tudo visto"


def render_navegacao_historias(
        historias_compartilhadas: list,
        contribuicoes_pendentes: int = 0,
):
    with st.sidebar:
        st.markdown("---")
        st.markdown('<div class="ae-sidebar-section">Minha área</div>', unsafe_allow_html=True)

        if st.button(
            "📖 Minha História",
            key="navegar_minha_historia",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.modo_visualizacao == "minha_historia"
                else "secondary"
            ),
        ):
            selecionar_minha_historia()
            st.rerun()

        if contribuicoes_pendentes:
            st.caption(
                f"🤝 {contribuicoes_pendentes} "
                f"{'contribuição aguardando aprovação' if contribuicoes_pendentes == 1 else 'contribuições aguardando aprovação'}"
            )

        st.markdown(
            '<div class="ae-sidebar-section">Histórias compartilhadas comigo</div>',
            unsafe_allow_html=True,
        )

        if not historias_compartilhadas:
            st.caption("Nenhuma história foi compartilhada com você ainda.")
            return

        for historia in historias_compartilhadas:
            nome = historia.get("nome_completo") or historia.get("nome") or "Pessoa"
            novidades = historia.get("novidades") or {}
            total_novidades = int(novidades.get("total", 0) or 0)
            selecionada = (
                st.session_state.modo_visualizacao == "historia_compartilhada"
                and st.session_state.historia_atual_usuario_id == historia["usuario_id"]
            )

            if st.button(
                (
                    f"👤 História de {nome} · {total_novidades} "
                    f"{'novidade' if total_novidades == 1 else 'novidades'}"
                    if total_novidades
                    else f"👤 História de {nome}"
                ),
                key=f"navegar_historia_{historia['usuario_id']}",
                use_container_width=True,
                type="primary" if selecionada else "secondary",
            ):
                selecionar_historia_compartilhada(historia)
                st.rerun()

            st.caption(formatar_novidades_historia(novidades))


def render_assistente_historia_compartilhada(
        usuario_logado: dict,
        acesso: dict,
):
    usuario_original = st.session_state.usuario_atual
    falecido_id_original = st.session_state.falecido_id

    usuario_visitante = {
        "id": acesso["contato_id"],
        "usuario_id": acesso["usuario_id"],
        "nome": usuario_logado.get("nome", "Visitante"),
        "tipo": "visitante",
        "nome_falecido": acesso.get("nome_completo") or acesso.get("nome"),
        "email": usuario_logado.get("email", ""),
        "parentesco": acesso.get("parentesco", ""),
        "usuario_logado_compartilhado": True,
    }

    try:
        st.session_state.usuario_atual = usuario_visitante
        st.session_state.falecido_id = acesso["usuario_id"]
        render_assistente()
    finally:
        st.session_state.usuario_atual = usuario_original
        st.session_state.falecido_id = falecido_id_original


def render_visao_historia_compartilhada(
        acesso: dict,
        usuario_logado: dict,
):
    usuario_id = acesso["usuario_id"]
    contato_id = acesso["contato_id"]
    nome_pessoa = acesso.get("nome_completo") or acesso.get("nome") or "esta pessoa"
    nome_visitante = usuario_logado.get("nome") or "Visitante"

    memorias = db.listar_memorias_por_contato(contato_id)
    fotos = db.listar_fotos_por_contato(contato_id)
    videos = db.listar_videos_por_contato(contato_id)

    try:
        preferencias = db.obter_preferencias(usuario_id)
    except Exception as exc:
        print("Erro ao carregar preferências para história compartilhada:", exc)
        preferencias = {}

    st.session_state.videos_visitante_cache = videos
    st.session_state.fotos_visitante_cache = fotos

    falecido_id_original = st.session_state.falecido_id
    try:
        st.session_state.falecido_id = usuario_id
        render_cabecalho_visitante(nome_pessoa, nome_visitante)

        abas = [
            "👤 Sobre",
            f"📖 Histórias ({len(memorias)})",
            "🌟 Aprendizados",
            "🔎 Explorar História",
        ]

        if videos:
            abas.append(f"🎥 Vídeos compartilhados ({len(videos)})")
        if fotos:
            abas.append(f"📷 Fotos compartilhadas ({len(fotos)})")

        tabs = st.tabs(abas)

        with tabs[0]:
            render_sobre_visitante(nome_pessoa, memorias, preferencias)
        with tabs[1]:
            render_historias_visitante(
                memorias,
                usuario_dono_id=usuario_id,
                usuario_logado=usuario_logado,
                permitir_contribuicao=True,
            )
        with tabs[2]:
            render_aprendizados_visitante(memorias, preferencias)
        with tabs[3]:
            render_assistente_historia_compartilhada(usuario_logado, acesso)

        indice = 4
        if videos:
            with tabs[indice]:
                render_videos_visitante(
                    contato_id=contato_id,
                    nome_pessoa=nome_pessoa,
                )
            indice += 1
        if fotos:
            with tabs[indice]:
                render_fotos_visitante(
                    contato_id=contato_id,
                    nome_pessoa=nome_pessoa,
                )
    finally:
        st.session_state.falecido_id = falecido_id_original

    st.markdown("""
    <div class="footer-aeterna">
        <p>✨ aEterna — Memórias vivas para quem você ama ✨</p>
    </div>
    """, unsafe_allow_html=True)


def render_contribuicoes_pendentes(usuario_dono_id: int):
    st.markdown("## 🤝 Contribuições pendentes")
    st.caption(
        "Lembranças enviadas por pessoas autorizadas. "
        "A memória original não será alterada."
    )

    contribuicoes = db.listar_contribuicoes_pendentes(usuario_dono_id)
    if not contribuicoes:
        st.info("Nenhuma contribuição aguardando aprovação.")
        return

    for contribuicao in contribuicoes:
        nome = contribuicao.get("contribuidor_nome") or "Pessoa convidada"
        titulo = contribuicao.get("memoria_titulo") or "História sem título"
        criado_em = contribuicao.get("criado_em")
        data_texto = (
            criado_em.strftime("%d/%m/%Y às %H:%M")
            if hasattr(criado_em, "strftime")
            else str(criado_em or "")
        )

        with st.container():
            st.markdown(f"**{nome} enviou uma lembrança para:**")
            st.markdown(f"### {titulo}")
            if data_texto:
                st.caption(data_texto)
            if contribuicao.get("texto"):
                st.markdown(contribuicao["texto"])

            arquivo_url = contribuicao.get("arquivo_url")
            arquivo_tipo = contribuicao.get("arquivo_tipo", "")
            if arquivo_url:
                if arquivo_tipo.startswith("image/"):
                    exibir_foto_segura(
                        arquivo_url,
                        caption=contribuicao.get("arquivo_nome", ""),
                    )
                elif arquivo_tipo.startswith("video/"):
                    exibir_video_seguro(
                        arquivo_url,
                        legenda=contribuicao.get("arquivo_nome", ""),
                    )

            col_aprovar, col_rejeitar = st.columns(2)
            with col_aprovar:
                if st.button(
                    "✅ Aprovar",
                    key=f"aprovar_contribuicao_{contribuicao['id']}",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        aprovado = db.avaliar_contribuicao(
                            contribuicao["id"],
                            usuario_dono_id,
                            "aprovado",
                        )
                    except Exception as exc:
                        print("Erro ao aprovar contribuição:", exc)
                        st.error("Não foi possível aprovar esta contribuição agora.")
                    else:
                        if aprovado:
                            st.success("Contribuição aprovada.")
                            st.rerun()
                        else:
                            st.warning("Esta contribuição não está mais pendente.")

            with col_rejeitar:
                if st.button(
                    "Rejeitar",
                    key=f"rejeitar_contribuicao_{contribuicao['id']}",
                    use_container_width=True,
                ):
                    try:
                        rejeitado = db.avaliar_contribuicao(
                            contribuicao["id"],
                            usuario_dono_id,
                            "rejeitado",
                        )
                    except Exception as exc:
                        print("Erro ao rejeitar contribuição:", exc)
                        st.error("Não foi possível rejeitar esta contribuição agora.")
                    else:
                        if rejeitado:
                            st.success("Contribuição rejeitada.")
                            st.rerun()
                        else:
                            st.warning("Esta contribuição não está mais pendente.")


def navegar_para(pagina: str):
    st.session_state.pagina_atual = pagina
    selecionar_minha_historia()


def contar_historias_compartilhadas(historia: dict) -> int:
    try:
        return len(db.listar_memorias_por_contato(historia.get("contato_id")))
    except Exception as exc:
        print("Erro ao contar histórias compartilhadas:", exc)
        return 0


def resumo_novidades(novidades: dict) -> str:
    total = int((novidades or {}).get("total", 0) or 0)
    if not total:
        return "Sem novidades"
    return f"{total} {'novidade' if total == 1 else 'novidades'}"


def _botao_sidebar(label: str, pagina: str, badge: int = 0):
    texto = f"{label} ({badge})" if badge else label
    selecionado = st.session_state.get("pagina_atual") == pagina
    if st.sidebar.button(
        texto,
        key=f"nav_principal_{pagina}",
        use_container_width=True,
        type="primary" if selecionado else "secondary",
    ):
        navegar_para(pagina)
        st.rerun()


def render_sidebar_principal(
        nome_exibido: str,
        historias_compartilhadas: list,
        contribuicoes_pendentes: int,
        is_admin: bool = False,
):
    with st.sidebar:
        _botao_sidebar("🏠 Início", "inicio")
        _botao_sidebar("📖 Minha História", "minha_historia")
        _botao_sidebar("👥 Pessoas", "pessoas")
        _botao_sidebar(
            "🤝 Compartilhadas Comigo",
            "historias_compartilhadas",
            sum(int((h.get("novidades") or {}).get("total", 0) or 0) for h in historias_compartilhadas),
        )
        _botao_sidebar("🔔 Novidades", "novidades", contribuicoes_pendentes)
        _botao_sidebar("✨ Contribuições", "contribuicoes", contribuicoes_pendentes)

        with st.expander("🧩 Mais", expanded=False):
            for label, pagina in (
                ("Curador de Histórias", "assistente"),
                ("Fotos", "fotos"),
                ("Vídeos", "videos"),
                ("Quem Sou Eu", "quem_sou_eu"),
                ("Mensagens para o Futuro", "mensagens"),
                ("Cofre", "cofre"),
                ("Meu plano", "planos"),
            ):
                if st.button(
                    label,
                    key=f"nav_mais_{pagina}",
                    use_container_width=True,
                    type=(
                        "primary"
                        if st.session_state.get("pagina_atual") == pagina
                        else "secondary"
                    ),
                ):
                    navegar_para(pagina)
                    st.rerun()

            if is_admin and st.button(
                "Admin",
                key="nav_mais_admin",
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.get("pagina_atual") == "admin"
                    else "secondary"
                ),
            ):
                navegar_para("admin")
                st.rerun()

        st.markdown('<div class="ae-sidebar-divider"></div>', unsafe_allow_html=True)
        primeiro_nome = str(nome_exibido or "Você").split()[0]
        with st.expander(f"👤 {primeiro_nome}", expanded=False):
            st.caption("Plano Familiar")
            st.caption("R$ 19,90/mês ou R$ 199/ano")
            if st.button("Meu plano", key="perfil_meu_plano", use_container_width=True):
                navegar_para("planos")
                st.rerun()
            if st.button("Configurações", key="perfil_configuracoes", use_container_width=True):
                navegar_para("quem_sou_eu")
                st.rerun()
            if st.button("Sair", key="nav_sair", use_container_width=True):
                fazer_logout()


def render_inicio(
        nome_exibido: str,
        usuario_id: int,
        historias_compartilhadas: list,
        contribuicoes_pendentes: int,
        qtd_pessoas: int = 0,
):
    primeiro_nome = str(nome_exibido or "Olá").split()[0]

    try:
        memorias = db.listar_memorias_usuario(usuario_id)
    except Exception as exc:
        print("Erro ao carregar memórias recentes:", exc)
        memorias = []

    try:
        fotos_por_memoria = db.listar_fotos_por_memorias_usuario(usuario_id)
        videos_por_memoria = db.listar_videos_por_memorias_usuario(usuario_id)
    except Exception as exc:
        print("Erro ao carregar mídia da home:", exc)
        fotos_por_memoria = {}
        videos_por_memoria = {}

    try:
        contatos = db.listar_contatos_usuario(usuario_id)
    except Exception as exc:
        print("Erro ao carregar pessoas importantes:", exc)
        contatos = []

    novidades_historias = sum(
        int((historia.get("novidades") or {}).get("total", 0) or 0)
        for historia in historias_compartilhadas
    )
    total_novidades = novidades_historias + int(contribuicoes_pendentes or 0)

    def resumo_curto(texto: str, limite: int = 118) -> str:
        texto = (texto or "").strip()
        if not texto:
            return "Uma história preservada no seu espaço privado."
        if len(texto) <= limite:
            return texto
        return texto[:limite].rsplit(" ", 1)[0] + "..."

    def imagem_local_para_data_uri(caminho: str) -> str:
        try:
            if not caminho or not os.path.exists(caminho):
                return ""
            mime_type = mimetypes.guess_type(caminho)[0] or "image/jpeg"
            with open(caminho, "rb") as arquivo:
                encoded = base64.b64encode(arquivo.read()).decode("ascii")
            return f"data:{mime_type};base64,{encoded}"
        except Exception as exc:
            print("Erro ao preparar miniatura da home:", exc)
            return ""

    def media_home_memoria(memoria: dict) -> str:
        fotos = fotos_por_memoria.get(memoria["id"], [])
        videos = videos_por_memoria.get(memoria["id"], [])
        if fotos:
            caminho_foto = (fotos[0].get("caminho") or "").strip()
            imagem_src = (
                caminho_foto
                if caminho_foto.startswith(("http://", "https://"))
                else imagem_local_para_data_uri(caminho_foto)
            )
            if imagem_src:
                return (
                    '<div class="ae-live-story-media">'
                    f'<img src="{html.escape(imagem_src, quote=True)}" alt="Miniatura da história">'
                    "</div>"
                )
        if videos:
            return (
                '<div class="ae-live-story-media ae-live-story-media-video">'
                "<span>🎥</span><strong>Vídeo</strong>"
                "</div>"
            )
        return (
            '<div class="ae-live-story-media ae-live-story-media-fallback">'
            "<span>📖</span><strong>História</strong>"
            "</div>"
        )

    def card_historia_home(memoria: dict) -> str:
        titulo = html.escape(memoria.get("titulo") or "História sem título")
        data = html.escape(str(memoria.get("data_evento") or ""))
        resumo = html.escape(resumo_curto(memoria.get("conteudo") or ""))
        data_html = f'<span class="ae-live-story-date">{data}</span>' if data else ""
        return (
            '<div class="ae-live-story-card">'
            f"{media_home_memoria(memoria)}"
            '<div class="ae-live-story-body">'
            f"<h3>{titulo}</h3>"
            f"{data_html}"
            f"<p>{resumo}</p>"
            "</div>"
            "</div>"
        )

    def pessoa_card(contato: dict) -> str:
        nome = contato.get("nome_completo") or contato.get("nome") or "Pessoa"
        inicial = html.escape(nome[:1].upper() or "P")
        relacao = "Você compartilha histórias com ela"
        if contato.get("parentesco"):
            relacao = f"{contato['parentesco']} nas suas histórias"
        elif contato.get("acesso_central_luto"):
            relacao = "Pode ver algumas das suas histórias"
        return (
            '<div class="ae-live-person-card">'
            f'<div class="ae-live-avatar">{inicial}</div>'
            f'<strong>{html.escape(nome)}</strong>'
            f'<span>{html.escape(relacao)}</span>'
            "</div>"
        )

    def compartilhada_card(historia: dict) -> str:
        nome = historia.get("nome_completo") or historia.get("nome") or "Pessoa importante"
        novidades = historia.get("novidades") or {}
        detalhe = (
            formatar_novidades_historia(novidades)
            if int(novidades.get("total", 0) or 0)
            else "Compartilhou um espaço de histórias com você"
        )
        return (
            '<div class="ae-live-shared-card">'
            '<div class="ae-live-avatar ae-live-avatar-shared">🤝</div>'
            f'<strong>{html.escape(nome)}</strong>'
            f'<span>{html.escape(detalhe)}</span>'
            "</div>"
        )

    col_top_text, col_top_action = st.columns([0.78, 0.22], vertical_alignment="center")
    with col_top_text:
        st.markdown(
            f"""
            <div class="ae-live-home-top">
                <h1>Olá, {html.escape(primeiro_nome)}</h1>
                <p>Seu espaço privado para preservar e compartilhar histórias com quem realmente importa.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_top_action:
        if st.button("+ Contar uma História", key="home_contar_historia", type="primary", use_container_width=True):
            navegar_para("assistente")
            st.rerun()

    st.markdown('<div class="ae-live-home-rule"></div>', unsafe_allow_html=True)

    st.markdown('<div class="ae-live-section-title">Continue sua história</div>', unsafe_allow_html=True)
    if memorias:
        colunas_memorias = st.columns(4)
        for indice, memoria in enumerate(memorias[:4]):
            with colunas_memorias[indice]:
                st.markdown(card_historia_home(memoria), unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="ae-live-empty-card">
                <strong>Sua primeira história ainda está esperando.</strong>
                <span>Quando você contar uma história, ela aparecerá aqui.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if st.button("Ver minha história", key="home_ver_minha_historia", use_container_width=False):
        navegar_para("minha_historia")
        st.rerun()

    col_pessoas, col_compartilhadas = st.columns(2)
    with col_pessoas:
        st.markdown('<div class="ae-live-section-title">Pessoas importantes</div>', unsafe_allow_html=True)
        pessoas_html = "".join(
            pessoa_card(contato)
            for contato in contatos[:4]
        )
        if not pessoas_html:
            pessoas_html = (
                '<div class="ae-live-empty-card ae-live-empty-card-small">'
                "<strong>Suas pessoas importantes aparecerão aqui.</strong>"
                "<span>Adicione contatos para organizar com quem suas histórias serão compartilhadas.</span>"
                "</div>"
            )
        st.markdown(f'<div class="ae-live-people-grid">{pessoas_html}</div>', unsafe_allow_html=True)
        if st.button("Ver pessoas", key="home_ver_pessoas", use_container_width=False):
            navegar_para("pessoas")
            st.rerun()

    with col_compartilhadas:
        st.markdown('<div class="ae-live-section-title">Compartilhadas comigo</div>', unsafe_allow_html=True)
        if historias_compartilhadas:
            compartilhadas_html = "".join(
                compartilhada_card(historia)
                for historia in historias_compartilhadas[:2]
            )
        else:
            compartilhadas_html = (
                '<div class="ae-live-empty-card ae-live-empty-card-small">'
                "<strong>Nenhuma história foi compartilhada com você ainda.</strong>"
                "<span>Quando alguém importante compartilhar histórias com você, elas aparecerão aqui.</span>"
                "</div>"
            )
        st.markdown(f'<div class="ae-live-shared-grid">{compartilhadas_html}</div>', unsafe_allow_html=True)
        if st.button("Ver compartilhadas", key="home_ver_historias", use_container_width=False):
            navegar_para("historias_compartilhadas")
            st.rerun()

    itens_novidades = []
    for historia in historias_compartilhadas:
        novidades = historia.get("novidades") or {}
        if int(novidades.get("total", 0) or 0):
            nome = historia.get("nome_completo") or historia.get("nome") or "Pessoa"
            itens_novidades.append(
                f"{nome}: {formatar_novidades_historia(novidades)}"
            )
    if contribuicoes_pendentes:
        itens_novidades.append(
            f"{contribuicoes_pendentes} contribuição aguardando avaliação"
        )
    if memorias:
        itens_novidades.append(
            f"Você criou a história \"{memorias[0].get('titulo') or 'História sem título'}\""
        )

    st.markdown('<div class="ae-live-section-title">O que aconteceu recentemente</div>', unsafe_allow_html=True)
    if itens_novidades:
        novidades_html = "".join(
            f'<div class="ae-live-news-item">✨ {html.escape(item)}</div>'
            for item in itens_novidades[:3]
        )
    else:
        novidades_html = (
            '<div class="ae-live-news-item">Sem novidades por enquanto. Quando algo importante acontecer, aparece aqui.</div>'
        )
    st.markdown(f'<div class="ae-live-news-list">{novidades_html}</div>', unsafe_allow_html=True)
    if st.button("Ver novidades", key="home_ver_novidades", use_container_width=False):
        navegar_para("novidades")
        st.rerun()


def render_historias_compartilhadas_lista(historias_compartilhadas: list):
    st.markdown("## 👥 Histórias compartilhadas comigo")
    if not historias_compartilhadas:
        st.info("Nenhuma história foi compartilhada com você ainda.")
        return

    for historia in historias_compartilhadas:
        nome = historia.get("nome_completo") or historia.get("nome") or "Pessoa"
        novidades = historia.get("novidades") or {}
        total_historias = contar_historias_compartilhadas(historia)
        resumo = resumo_novidades(novidades)
        with st.container():
            st.markdown(
                f"""
                <div class="ae-shared-card">
                    <div class="ae-avatar">👤</div>
                    <div class="ae-shared-content">
                        <div class="ae-card-label">História compartilhada</div>
                        <h3>{html.escape(nome)}</h3>
                        <p>{total_historias} {'história compartilhada' if total_historias == 1 else 'histórias compartilhadas'}</p>
                        <span>{html.escape(resumo)}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Explorar histórias",
                key=f"abrir_historia_compartilhada_{historia['usuario_id']}",
                use_container_width=True,
            ):
                selecionar_historia_compartilhada(historia)
                st.session_state.pagina_atual = "historias_compartilhadas"
                st.rerun()


def render_novidades(
        historias_compartilhadas: list,
        contribuicoes_pendentes: int,
):
    st.markdown("## 🔔 Novidades")
    total_historias = sum(
        int((historia.get("novidades") or {}).get("total", 0) or 0)
        for historia in historias_compartilhadas
    )

    if not total_historias and not contribuicoes_pendentes:
        st.info("Sem novidades por enquanto. Quando alguém compartilhar um novo momento, ele aparecerá aqui.")
        return

    if total_historias:
        for historia in historias_compartilhadas:
            novidades = historia.get("novidades") or {}
            if int(novidades.get("total", 0) or 0):
                nome = historia.get("nome_completo") or historia.get("nome") or "Pessoa"
                detalhes = formatar_novidades_historia(novidades)
                st.markdown(
                    f"""
                    <div class="ae-activity-card">
                        <div class="ae-activity-icon">📖</div>
                        <div>
                            <div class="ae-card-label">Histórias compartilhadas</div>
                            <h3>{html.escape(nome)} adicionou novos momentos</h3>
                            <p>{html.escape(detalhes)}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Ver história",
                    key=f"novidade_historia_{historia['usuario_id']}",
                    use_container_width=True,
                ):
                    selecionar_historia_compartilhada(historia)
                    st.session_state.pagina_atual = "historias_compartilhadas"
                    st.rerun()

    if contribuicoes_pendentes:
        st.markdown(
            f"""
            <div class="ae-activity-card">
                <div class="ae-activity-icon">🤝</div>
                <div>
                    <div class="ae-card-label">Contribuições</div>
                    <h3>Há lembranças aguardando sua revisão</h3>
                    <p>{contribuicoes_pendentes} {'contribuição enviada por uma pessoa convidada' if contribuicoes_pendentes == 1 else 'contribuições enviadas por pessoas convidadas'}.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Avaliar", use_container_width=True):
            navegar_para("contribuicoes")
            st.rerun()


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
            nome_pessoa = st.session_state.usuario_atual.get(
                "nome_falecido",
                "esta pessoa",
            )

            videos_visitante = db.listar_videos_por_contato(
                st.session_state.usuario_atual["id"]
            )

            fotos_visitante = db.listar_fotos_por_contato(
                st.session_state.usuario_atual["id"]
            )

            memorias_visitante = db.listar_memorias_por_contato(
                st.session_state.usuario_atual["id"]
            )

            try:
                preferencias_visitante = db.obter_preferencias(
                    st.session_state.falecido_id
                )
            except Exception as exc:
                print("Erro ao carregar preferências para visitante:", exc)
                preferencias_visitante = {}

            st.session_state.videos_visitante_cache = videos_visitante
            st.session_state.fotos_visitante_cache = fotos_visitante

            render_sidebar_premium(
                nome_exibido=nome_exibido,
                qtd_videos=len(videos_visitante),
                qtd_contatos=0,
                qtd_cofre=0,
                qtd_memorias=len(memorias_visitante),
                is_admin=False,
                fazer_logout=fazer_logout
            )

            render_cabecalho_visitante(nome_pessoa, nome_exibido)

            abas = [
                "👤 Sobre",
                f"📖 Histórias ({len(memorias_visitante)})",
                "🌟 Aprendizados",
                "🔎 Explorar História",
            ]

            if videos_visitante:
                abas.append(f"🎥 Vídeos compartilhados ({len(videos_visitante)})")

            if fotos_visitante:
                abas.append(f"📷 Fotos compartilhadas ({len(fotos_visitante)})")

            tabs = st.tabs(abas)

            with tabs[0]:
                render_sobre_visitante(
                    nome_pessoa,
                    memorias_visitante,
                    preferencias_visitante,
                )

            with tabs[1]:
                render_historias_visitante(
                    memorias_visitante,
                    usuario_dono_id=st.session_state.falecido_id,
                )

            with tabs[2]:
                render_aprendizados_visitante(
                    memorias_visitante,
                    preferencias_visitante,
                )

            with tabs[3]:
                render_assistente()

            indice = 4

            if videos_visitante:
                with tabs[indice]:
                    render_videos_visitante()
                indice += 1

            if fotos_visitante:
                with tabs[indice]:
                    render_fotos_visitante()
                indice += 1

            st.markdown("""
            <div class="footer-aeterna">
                <p>✨ aEterna — Memórias vivas para quem você ama ✨</p>
            </div>
            """, unsafe_allow_html=True)

            return

        nome_exibido = st.session_state.usuario_atual.get(
            "nome_completo",
            "Usuário"
        )
        usuario_logado = st.session_state.usuario_atual

        try:
            contribuicoes_pendentes = db.contar_contribuicoes_pendentes(
                usuario_logado.get("id")
            )
        except Exception as exc:
            print("Erro ao contar contribuições pendentes:", exc)
            contribuicoes_pendentes = 0

        try:
            historias_compartilhadas = db.listar_historias_compartilhadas_comigo(
                usuario_logado.get("email", "")
            )
        except Exception as exc:
            print("Erro ao listar histórias compartilhadas:", exc)
            historias_compartilhadas = []

        acesso_historia_atual = None
        if st.session_state.modo_visualizacao == "historia_compartilhada":
            historia_usuario_id = st.session_state.historia_atual_usuario_id
            acesso_historia_atual = db.usuario_pode_acessar_historia(
                usuario_logado.get("email", ""),
                historia_usuario_id,
            )

            if not acesso_historia_atual:
                st.warning(
                    "Você não possui autorização para acessar esta história. "
                    "Voltamos para a sua área."
                )
                selecionar_minha_historia()
                st.rerun()

            try:
                db.registrar_acesso_historia(
                    usuario_logado.get("email", ""),
                    historia_usuario_id,
                )
            except Exception as exc:
                print("Erro ao registrar acesso à história:", exc)

        for historia in historias_compartilhadas:
            try:
                historia["novidades"] = db.contar_novidades_historia(
                    usuario_logado.get("email", ""),
                    historia["usuario_id"],
                )
            except Exception as exc:
                print("Erro ao contar novidades da história:", exc)
                historia["novidades"] = {
                    "memorias": 0,
                    "fotos": 0,
                    "videos": 0,
                    "total": 0,
                }

        is_admin = (
                st.session_state.usuario_atual.get("tipo") == "admin"
        )

        try:
            qtd_videos = len(db.listar_videos_usuario(usuario_logado["id"]))
        except Exception as exc:
            print("Erro ao contar vídeos:", exc)
            qtd_videos = 0

        try:
            qtd_contatos = len(db.listar_contatos_usuario(usuario_logado["id"]))
        except Exception as exc:
            print("Erro ao contar pessoas:", exc)
            qtd_contatos = 0

        try:
            qtd_memorias = len(db.listar_memorias_usuario(usuario_logado["id"]))
        except Exception as exc:
            print("Erro ao contar memórias:", exc)
            qtd_memorias = 0

        qtd_cofre = 0

        render_sidebar_premium(
            nome_exibido=nome_exibido,
            qtd_videos=qtd_videos,
            qtd_contatos=qtd_contatos,
            qtd_cofre=qtd_cofre,
            qtd_memorias=qtd_memorias,
            is_admin=is_admin,
            fazer_logout=fazer_logout
        )

        render_sidebar_principal(
            nome_exibido,
            historias_compartilhadas,
            contribuicoes_pendentes,
            is_admin=is_admin,
        )

        if st.session_state.modo_visualizacao == "historia_compartilhada":
            render_visao_historia_compartilhada(
                acesso_historia_atual,
                usuario_logado,
            )
            return

        pagina = st.session_state.get("pagina_atual", "inicio")

        if pagina == "inicio":
            render_inicio(
                nome_exibido,
                usuario_logado["id"],
                historias_compartilhadas,
                contribuicoes_pendentes,
                qtd_contatos,
            )
        elif pagina == "minha_historia":
            render_minha_historia()
        elif pagina == "historias_compartilhadas":
            render_historias_compartilhadas_lista(historias_compartilhadas)
        elif pagina == "novidades":
            render_novidades(historias_compartilhadas, contribuicoes_pendentes)
        elif pagina == "contribuicoes":
            render_contribuicoes_pendentes(usuario_logado["id"])
        elif pagina == "assistente":
            render_assistente()
        elif pagina == "videos":
            render_videos()
        elif pagina == "fotos":
            render_fotos()
        elif pagina == "pessoas":
            render_contatos()
        elif pagina == "quem_sou_eu":
            render_preferencias()
        elif pagina == "mensagens":
            render_agendamentos()
        elif pagina == "cofre":
            render_cofre()
        elif pagina == "planos":
            render_planos()
        elif pagina == "admin" and is_admin:
            render_admin_panel()
        else:
            st.session_state.pagina_atual = "inicio"
            render_inicio(
                nome_exibido,
                usuario_logado["id"],
                historias_compartilhadas,
                contribuicoes_pendentes,
                qtd_contatos,
            )

        st.markdown("""
        <div class="footer-aeterna">
            <p>✨ aEterna — Memórias vivas para quem você ama ✨</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
