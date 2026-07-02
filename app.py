import streamlit as st
from PIL import Image
import os
import html
import base64
import mimetypes
import re
import unicodedata
from datetime import datetime
import secrets
from utils.banco import BancoDados
from utils.usuarios import GerenciadorUsuarios
from utils.upload_video import GerenciadorVideos
from styles.theme import aplicar_tema
from components.chat_luto import render_chat_luto, render_curador_memoria_primeiro
from components.memorial import render_memoriais_lista, render_criar_memorial, render_pagina_memorial, render_curador_perfil
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
from utils.email_service import EmailService

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
    filtro_cat = st.session_state.get("_ae_filtro_categoria")

    expanded_key = None
    expanded_memoria = None

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

        estilo = "height:86px;max-height:86px;min-height:86px;overflow:hidden;position:relative;"

        imagem_extra = ""
        if fotos:
            caminho_foto = (fotos[0].get("caminho") or "").strip()
            imagem_src = caminho_foto if caminho_foto.startswith(("http://", "https://")) else imagem_local_para_data_uri(caminho_foto)
            if imagem_src:
                imagem_segura = html.escape(imagem_src, quote=True)
                imagem_extra = (
                    f'<img src="{imagem_segura}" alt="" '
                    'style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;">'
                )

        if videos and not imagem_extra:
            return (
                f'<div class="{classe_base} {classe_base}-video" style="{estilo}">'
                "<span>🎥</span>"
                "<strong>Vídeo</strong>"
                "</div>"
            )

        return (
            f'<div class="{classe_base} {classe_base}-fallback" style="{estilo}">'
            "<span>📖</span>"
            "<strong>História</strong>"
            f"{imagem_extra}"
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

    def render_card_memoria(memoria: dict, categoria: str, mostrar_categoria: bool = False, idx: int = None, contexto: str = None) -> str:
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
        return card_html

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

    def render_colecao_box_html(categoria: str, itens: list) -> str:
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
        return (
            '<div class="ae-collection-box">'
            '<div class="ae-collection-head">'
            f'<h3>{icone_categoria(categoria)} {titulo}</h3>'
            "</div>"
            '<div class="ae-collection-mini-grid">'
            f"{mini_cards}"
            "</div>"
            "</div>"
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

    def render_prateleira(
            itens: list,
            categoria_nome: str,
            contexto: str,
            quantidade_colunas: int = 4,
    ):
        expanded_key = None
        expanded_mem = None

        for row_start in range(0, len(itens), quantidade_colunas):
            row_items = itens[row_start:row_start + quantidade_colunas]
            cards_html = []
            btn_keys = []
            for j, memoria in enumerate(row_items):
                posicao = row_start + j
                key_contexto = f"{contexto}_{posicao}_{memoria['id']}"
                btn_keys.append(key_contexto)
                cards_html.append(render_card_memoria(memoria, categoria_nome))
                show_key = f"_show_{key_contexto}"
                if st.session_state.get(show_key, False):
                    expanded_key = key_contexto
                    expanded_mem = memoria
            cells = "".join(f"<div>{c}</div>" for c in cards_html)
            cells += "<div></div>" * (quantidade_colunas - len(row_items))
            st.markdown(
                '<style>'
                '.ae-story-card{display:flex!important;flex-direction:column!important;height:270px!important;max-height:270px!important;min-height:270px!important;}'
                '.ae-story-media{height:86px!important;max-height:86px!important;min-height:86px!important;flex-shrink:0!important;}'
                '.ae-story-body{height:146px!important;max-height:146px!important;min-height:146px!important;flex-shrink:0!important;}'
                '</style>'
                + f'<div class="ae-card-grid-row" style="display:grid;grid-template-columns:repeat({quantidade_colunas},1fr);gap:0.5rem;">{cells}</div>',
                unsafe_allow_html=True,
            )
            btn_cols = st.columns(quantidade_colunas, gap="small")
            for col_idx, col in enumerate(btn_cols):
                if col_idx < len(row_items):
                    key_ctx = btn_keys[col_idx]
                    show_key = f"_show_{key_ctx}"
                    with col:
                        if st.button("📖 Ler história", key=f"_ler_{key_ctx}"):
                            st.session_state[show_key] = True
                            st.rerun()
        return expanded_key, expanded_mem

    def nome_categoria(categoria: str) -> str:
        categoria_normalizada = normalizar_categoria_colecao(categoria)
        return {
            "livre": "Histórias da Vida",
            "outras histórias": "Histórias da Vida",
            "outros": "Histórias da Vida",
            "familia": "Família",
            "viagens": "Viagens",
            "infancia": "Infância",
        }.get(categoria_normalizada, (categoria or "Histórias da Vida").title())

    def icone_categoria(categoria: str) -> str:
        categoria_normalizada = normalizar_categoria_colecao(categoria)
        return {
            "familia": "❤️",
            "viagens": "✈️",
            "carreira": "💼",
            "estudos": "🎓",
            "infancia": "👶",
            "conquista": "🏆",
            "conquistas": "🏆",
            "amor": "💕",
            "valores": "🌟",
            "livre": "📚",
        }.get(categoria_normalizada, "📚")

    def normalizar_categoria_colecao(categoria: str) -> str:
        texto = unicodedata.normalize("NFD", str(categoria or "livre").strip().lower())
        texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
        texto = re.sub(r"\s+", " ", texto)
        mapa = {
            "familia": "familia",
            "família": "familia",
            "viagem": "viagens",
            "viagens": "viagens",
            "infancia": "infancia",
            "infância": "infancia",
            "historia": "livre",
            "historias": "livre",
            "histórias": "livre",
            "outras historias": "livre",
            "outras histórias": "livre",
        }
        return mapa.get(texto, texto or "livre")

    for idx, mem in enumerate(memorias[:4]):
        key_ctx = f"continue_{idx}_{mem['id']}"
        if st.session_state.get(f"_show_{key_ctx}", False):
            expanded_key = key_ctx
            expanded_memoria = mem
            break

    if expanded_memoria and expanded_key:
        st.divider()
        render_detalhes_memoria(expanded_memoria, expanded_key)
        close_key = f"_close_{expanded_key}"
        if st.button("✕ Fechar", key=close_key):
            st.session_state[f"_show_{expanded_key}"] = False
            st.rerun()
        st.divider()

    grupos = {}
    for memoria in memorias:
        categoria = normalizar_categoria_colecao(memoria.get("categoria") or "livre")
        grupos.setdefault(categoria, []).append(memoria)

    if filtro_cat and filtro_cat in grupos:
        # ── Vista filtrada por categoria ──────────────────────────────
        categoria_nome_filtro = nome_categoria(filtro_cat)
        if st.button("← Voltar às coleções", key="filtro_voltar"):
            del st.session_state["_ae_filtro_categoria"]
            st.rerun()
        st.markdown(
            f'<div class="ae-story-section-title">{icone_categoria(filtro_cat)} {categoria_nome_filtro}</div>',
            unsafe_allow_html=True,
        )
        exp_key_filtro, exp_mem_filtro = render_prateleira(grupos[filtro_cat], categoria_nome_filtro, contexto="filtro", quantidade_colunas=4)
        if exp_mem_filtro and exp_key_filtro:
            st.divider()
            render_detalhes_memoria(exp_mem_filtro, exp_key_filtro)
            close_key = f"_close_{exp_key_filtro}"
            if st.button("✕ Fechar", key=close_key):
                st.session_state[f"_show_{exp_key_filtro}"] = False
                st.rerun()
    else:
        # ── Vista normal: Continue + Coleções ─────────────────────────
        st.markdown('<div class="ae-story-section-title">Continue sua história</div>', unsafe_allow_html=True)
        exp_key_cont, exp_mem_cont = render_prateleira(
            memorias[:4],
            "Continue",
            contexto="continue",
            quantidade_colunas=4,
        )
        st.markdown('<div class="ae-story-section-title ae-story-section-title-collections">Coleções</div>', unsafe_allow_html=True)
        grupos_ordenados = sorted(
            grupos.items(),
            key=lambda item: len(item[1]),
            reverse=True,
        )
        for inicio in range(0, len(grupos_ordenados), 3):
            row_items = grupos_ordenados[inicio:inicio + 3]
            cols = st.columns(3)
            for col_idx, (cat, itens) in enumerate(row_items):
                with cols[col_idx]:
                    box_html = render_colecao_box_html(cat, itens)
                    st.markdown(box_html, unsafe_allow_html=True)
                    if st.button("Ver todas ›", key=f"colecao_btn_{cat}"):
                        st.session_state["_ae_filtro_categoria"] = cat
                        st.rerun()


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
    usuario = st.session_state.get("usuario_atual") or {}
    if usuario.get("tipo") == "visitante":
        render_chat_luto()
        return
    render_curador_memoria_primeiro()


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

PALAVRAS_IGNORADAS_PESSOAS = {
    "familia", "família", "viagem", "viagens", "canyons", "canyon", "gauchos", "gaúchos",
    "sao paulo", "são paulo", "joao pessoa", "joão pessoa", "gramado", "natal", "carnaval",
    "segunda", "domingo", "janeiro", "fevereiro", "marco", "março", "abril", "maio",
    "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    "historia", "história", "historias", "histórias", "memoria", "memória", "memorias",
    "memórias", "primeiro", "primeira", "vida", "emprego", "fortaleza", "canoas",
    "cambara", "cambará", "sul", "alegre", "rio", "grande", "brasil", "portugal",
    "argentina", "uruguai", "paris", "lisboa",
    "ela", "ele", "eles", "elas", "eu", "nos", "nós", "voce", "você", "voces", "vocês",
    "meu", "minha", "meus", "minhas", "seu", "sua", "seus", "suas", "nosso", "nossa",
    "sao", "são", "santa", "santo", "paulo", "cambará do sul", "canela", "porto",
    "porto alegre", "rio grande do sul", "fotos", "videos", "vídeos", "foi", "fomos",
    "era", "estava", "estavam", "tinha", "fizemos", "conhecemos", "visitamos",
}

PALAVRAS_IGNORADAS_EXIBICAO = [
    "Família", "Viagem", "Canyons", "São Paulo", "João Pessoa", "Gramado", "Natal",
    "Carnaval", "Segunda", "Domingo", "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def normalizar_nome_pessoa(valor: str) -> str:
    texto = unicodedata.normalize("NFD", str(valor or ""))
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    texto = re.sub(r"\s+", " ", texto.lower()).strip()
    return texto


def textos_memoria_para_sugestao(memoria: dict) -> str:
    campos = [
        memoria.get("titulo"),
        memoria.get("conteudo"),
        memoria.get("pessoas_relacionadas"),
        memoria.get("local"),
        memoria.get("resumo"),
        memoria.get("descricao"),
        memoria.get("transcricao"),
    ]
    return " ".join(str(campo or "") for campo in campos)


def extrair_pessoas_encontradas(memorias: list, contatos: list, ignoradas_usuario: set = None) -> list:
    nomes_contatos = set()
    for contato in contatos:
        for campo in ("nome_completo", "nome"):
            nome = normalizar_nome_pessoa(contato.get(campo))
            if nome:
                nomes_contatos.add(nome)

    ignoradas = {normalizar_nome_pessoa(item) for item in PALAVRAS_IGNORADAS_PESSOAS}
    ignoradas_usuario = {normalizar_nome_pessoa(item) for item in (ignoradas_usuario or set())}
    contexto_pessoal = {
        "filha", "filho", "irma", "irmao", "mae", "pai",
        "esposa", "marido", "sobrinha", "sobrinho", "prima", "primo", "amiga",
        "amigo", "avo", "tia", "tio", "cunhada", "cunhado",
        "neta", "neto", "namorada", "namorado", "companheira", "companheiro",
    }
    bloqueios_exatos = {
        "cambara do sul", "cambará do sul", "sao paulo foi", "são paulo foi",
        "alegre do rio grande", "alice ela", "alice joao pessoa", "alice joão pessoa",
        "canyons gauchos", "canyons gaúchos",
    }
    possessivos = {"meu", "minha", "meus", "minhas", "seu", "sua", "seus", "suas", "nosso", "nossa"}
    conectores = {"de", "da", "do", "das", "dos", "e"}
    sugestoes = {}

    def candidato_valido(candidato: str) -> bool:
        candidato_norm = normalizar_nome_pessoa(candidato)
        palavras_nome = [p for p in candidato_norm.split() if p not in conectores]
        if not candidato_norm or candidato_norm in ignoradas or candidato_norm in ignoradas_usuario:
            return False
        if candidato_norm in bloqueios_exatos:
            return False
        if candidato_norm in nomes_contatos or any(candidato_norm == nome.split()[0] for nome in nomes_contatos if nome):
            return False
        if any(parte in ignoradas or parte in contexto_pessoal for parte in palavras_nome):
            return False
        if len(palavras_nome) > 2:
            return False
        if len(palavras_nome) == 1 and len(palavras_nome[0]) < 3:
            return False
        return bool(re.match(r"^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]", candidato))

    def registrar_candidato(candidato: str, memoria: dict, score: int, forte: bool = False):
        candidato = re.sub(r"\s+", " ", candidato).strip()
        if not candidato_valido(candidato):
            return
        chave = normalizar_nome_pessoa(candidato)
        registro = sugestoes.setdefault(
            chave,
            {
                "nome": candidato,
                "memorias_ids": set(),
                "historias": [],
                "score": 0,
                "forte": False,
                "ocorrencias": 0,
            },
        )
        registro["memorias_ids"].add(memoria.get("id"))
        registro["historias"].append(memoria.get("titulo") or "História sem título")
        registro["score"] += score
        registro["forte"] = registro["forte"] or forte
        registro["ocorrencias"] += 1

    for memoria in memorias:
        texto = textos_memoria_para_sugestao(memoria)
        tokens = re.findall(r"\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]?[^\W\d_]{2,}\b", texto, flags=re.UNICODE)

        for indice, token in enumerate(tokens[:-1]):
            token_norm = normalizar_nome_pessoa(token)
            if token_norm not in contexto_pessoal:
                continue

            nome = tokens[indice + 1]
            if re.match(r"^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]", nome):
                anterior = normalizar_nome_pessoa(tokens[indice - 1]) if indice > 0 else ""
                score = 20
                forte = False
                if anterior in possessivos:
                    score = 200
                    forte = True
                registrar_candidato(nome, memoria, score, forte=forte)

        for candidato in re.findall(r"\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][^\W\d_]{2,}\b", texto, flags=re.UNICODE):
            registrar_candidato(candidato, memoria, 10, forte=False)

    resultado = []
    for item in sugestoes.values():
        item["quantidade"] = len(item["memorias_ids"])
        item["historias"] = list(dict.fromkeys(item["historias"]))[:5]
        item["nome_normalizado"] = normalizar_nome_pessoa(item["nome"])
        item["origem"] = ", ".join(item["historias"][:3])
        if item["forte"] or item["score"] >= 60:
            resultado.append(item)

    return sorted(resultado, key=lambda sugestao: (-sugestao["score"], -sugestao["quantidade"], sugestao["nome"]))[:8]


def render_perfil_pessoa_vivo(contato: dict, contatos: list, usuario_id: int):
    def texto_limpo(valor, padrao: str = "") -> str:
        return str(valor or padrao or "").strip()

    def data_curta(valor) -> str:
        if not valor:
            return ""
        texto = str(valor)[:10]
        for formato in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(texto, formato).strftime("%d/%m/%Y")
            except ValueError:
                continue
        return texto

    def ano_de(valor) -> str:
        if not valor:
            return ""
        match = re.search(r"(19|20)\d{2}", str(valor)[:10])
        return match.group(0) if match else ""

    def normalizar(valor: str) -> str:
        return normalizar_nome_pessoa(valor)

    def imagem_src(caminho: str) -> str:
        caminho = texto_limpo(caminho)
        if not caminho:
            return ""
        if caminho.startswith(("http://", "https://", "data:")):
            return caminho
        if os.path.exists(caminho):
            tipo, _ = mimetypes.guess_type(caminho)
            tipo = tipo or "image/jpeg"
            try:
                with open(caminho, "rb") as arquivo:
                    return f"data:{tipo};base64,{base64.b64encode(arquivo.read()).decode('utf-8')}"
            except Exception as exc:
                print("Erro ao preparar imagem do perfil vivo:", exc)
        return ""

    def resumo(texto: str, limite: int = 120) -> str:
        texto = re.sub(r"\s+", " ", texto_limpo(texto))
        return texto if len(texto) <= limite else texto[:limite].rstrip() + "..."

    nome_exibido = (
        texto_limpo(contato.get("nome_completo"))
        or f"{texto_limpo(contato.get('nome'))} {texto_limpo(contato.get('sobrenome'))}".strip()
        or "Pessoa importante"
    )
    primeiro_nome = texto_limpo(contato.get("nome")) or nome_exibido.split()[0]
    relacao = texto_limpo(contato.get("parentesco"), "Pessoa importante")
    nascimento = data_curta(contato.get("data_nascimento"))
    foto_src = imagem_src(contato.get("foto_perfil") or contato.get("foto") or "")
    inicial = html.escape(nome_exibido[:1].upper() or "P")

    termos_busca = {
        normalizar(nome_exibido),
        normalizar(primeiro_nome),
        normalizar(f"{texto_limpo(contato.get('nome'))} {texto_limpo(contato.get('sobrenome'))}".strip()),
    }
    termos_busca = {termo for termo in termos_busca if len(termo) >= 3}

    try:
        memorias = db.listar_memorias_usuario(usuario_id) or []
    except Exception as exc:
        print("Erro ao carregar histórias do perfil da pessoa:", exc)
        memorias = []

    def memoria_tem_pessoa(memoria: dict) -> bool:
        texto = normalizar(" ".join([
            texto_limpo(memoria.get("titulo")),
            texto_limpo(memoria.get("conteudo")),
            texto_limpo(memoria.get("pessoas_relacionadas")),
        ]))
        return any(termo and termo in texto for termo in termos_busca)

    memorias_relacionadas = [memoria for memoria in memorias if memoria_tem_pessoa(memoria)]
    ids_memorias = {memoria.get("id") for memoria in memorias_relacionadas if memoria.get("id")}

    try:
        fotos_por_memoria = db.listar_fotos_por_memorias_usuario(usuario_id) or {}
    except Exception as exc:
        print("Erro ao carregar fotos do perfil da pessoa:", exc)
        fotos_por_memoria = {}

    try:
        videos_por_memoria = db.listar_videos_por_memorias_usuario(usuario_id) or {}
    except Exception as exc:
        print("Erro ao carregar vídeos do perfil da pessoa:", exc)
        videos_por_memoria = {}

    contribuicoes_por_memoria = carregar_contribuicoes_aprovadas_memorias(usuario_id)
    nome_norm = normalizar(nome_exibido)
    email_norm = texto_limpo(contato.get("email")).lower()
    contribuicoes_relacionadas = []
    for memoria_id, contribuicoes in contribuicoes_por_memoria.items():
        for contribuicao in contribuicoes:
            contrib_nome_norm = normalizar(contribuicao.get("contribuidor_nome") or "")
            contrib_email_norm = texto_limpo(contribuicao.get("contribuidor_email")).lower()
            mesma_pessoa = (
                (nome_norm and (nome_norm in contrib_nome_norm or contrib_nome_norm in nome_norm))
                or (email_norm and email_norm == contrib_email_norm)
            )
            if mesma_pessoa or memoria_id in ids_memorias:
                item = dict(contribuicao)
                item["memoria_id"] = memoria_id
                contribuicoes_relacionadas.append(item)

    categorias = []
    for memoria in memorias_relacionadas:
        categoria = texto_limpo(memoria.get("categoria"))
        if categoria and categoria not in categorias:
            categorias.append(categoria)
    tags = [("❤️", relacao)] if relacao else []
    mapa_categorias = {
        "familia": "❤️",
        "viagens": "✈️",
        "viagem": "✈️",
        "trabalho": "💼",
        "fe": "✝️",
        "historias da vida": "📖",
    }
    for categoria in categorias[:4]:
        tags.append((mapa_categorias.get(normalizar(categoria), "🏷️"), categoria))

    def chips_html() -> str:
        if not tags:
            return '<span class="ae-person-profile-chip">🏷️ Pessoa importante</span>'
        return "".join(
            f'<span class="ae-person-profile-chip">{icone} {html.escape(label)}</span>'
            for icone, label in tags[:5]
        )

    def memoria_thumb(memoria: dict) -> str:
        for foto in fotos_por_memoria.get(memoria.get("id"), []):
            src = imagem_src(foto.get("caminho"))
            if src:
                alt = html.escape(foto.get("titulo") or memoria.get("titulo") or "História")
                return f'<img src="{html.escape(src)}" alt="{alt}">'
        return '<div class="ae-person-story-fallback">📖</div>'

    def avatar_html(pessoa: dict, classe: str = "ae-person-profile-avatar") -> str:
        nome = texto_limpo(pessoa.get("nome_completo")) or texto_limpo(pessoa.get("nome")) or "Pessoa"
        src = imagem_src(pessoa.get("foto_perfil") or "")
        if src:
            return f'<img class="{classe}" src="{html.escape(src)}" alt="{html.escape(nome)}">'
        return f'<div class="{classe}">{html.escape(nome[:1].upper() or "P")}</div>'

    def story_card_html(memoria: dict, compacto: bool = False) -> str:
        titulo = html.escape(texto_limpo(memoria.get("titulo"), "História sem título"))
        data = data_curta(memoria.get("data_evento") or memoria.get("data_criacao"))
        pessoas = texto_limpo(memoria.get("pessoas_relacionadas"))
        qtd_pessoas = len([p for p in re.split(r"[,;]", pessoas) if p.strip()]) if pessoas else 1
        classe = "ae-person-story-card ae-person-story-card-compact" if compacto else "ae-person-story-card"
        data_html = html.escape(data) if data else "data não informada"
        return (
            f'<div class="{classe}">'
            f'<div class="ae-person-story-media">{memoria_thumb(memoria)}</div>'
            f'<div class="ae-person-story-body">'
            f'<strong>{titulo}</strong>'
            f'<span>Atualizada em {data_html}</span>'
            f'<em>👥 {qtd_pessoas}</em>'
            f'</div>'
            f'</div>'
        )

    def montar_eventos() -> list:
        eventos = []
        if nascimento:
            eventos.append({
                "ano": ano_de(contato.get("data_nascimento")) or nascimento[-4:],
                "titulo": "Nascimento",
                "descricao": f"{nome_exibido} nasceu em {nascimento}.",
                "icone": "👤",
                "imagem": foto_src,
            })
        for memoria in memorias_relacionadas[:6]:
            data_evento = memoria.get("data_evento") or memoria.get("data_criacao")
            fotos_memoria = fotos_por_memoria.get(memoria.get("id")) or []
            eventos.append({
                "ano": ano_de(data_evento) or "História",
                "titulo": texto_limpo(memoria.get("titulo"), "Aparição em história"),
                "descricao": resumo(memoria.get("conteudo"), 96),
                "icone": "📖",
                "imagem": imagem_src(fotos_memoria[0].get("caminho", "")) if fotos_memoria else "",
            })
        for contribuicao in contribuicoes_relacionadas[:3]:
            eventos.append({
                "ano": ano_de(contribuicao.get("criado_em")) or "Agora",
                "titulo": "Contribuição",
                "descricao": resumo(contribuicao.get("texto") or "Contribuição enviada para uma história.", 96),
                "icone": "🤝",
                "imagem": imagem_src(contribuicao.get("arquivo_url") or ""),
            })
        return eventos[:8]

    eventos = montar_eventos()
    relacoes_familia = {
        "mae", "mãe", "pai", "filho(a)", "filha", "filho", "conjuge", "cônjuge",
        "irmao(a)", "irmão(ã)", "irma", "irmã", "irmao", "irmão", "avo", "avó", "avô",
        "neto(a)", "neto", "neta",
    }
    familiares = [
        pessoa for pessoa in contatos
        if pessoa.get("id") != contato.get("id")
        and normalizar(texto_limpo(pessoa.get("parentesco"))) in {normalizar(r) for r in relacoes_familia}
    ][:5]

    if st.button("← Voltar para Pessoas", key="voltar_lista_pessoas", use_container_width=False):
        st.session_state.pop("perfil_pessoa_id", None)
        st.session_state.pop("perfil_pessoa_tab", None)
        st.rerun()

    with st.container(key="ae_person_profile_hero"):
        foto_col, dados_col, acoes_col = st.columns([0.15, 0.62, 0.23], vertical_alignment="top")
        with foto_col:
            if foto_src:
                st.markdown(
                    f'<div class="ae-person-profile-photo"><img src="{html.escape(foto_src)}" alt="{html.escape(nome_exibido)}"></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="ae-person-profile-photo"><div>{inicial}</div></div>',
                    unsafe_allow_html=True,
                )
        with dados_col:
            fatos_html = "".join([
                f'<span>🗓️ {html.escape(nascimento)}</span>' if nascimento else "",
                f'<span>📍 {html.escape(texto_limpo(contato.get("local")))}</span>' if texto_limpo(contato.get("local")) else "",
                f'<span>♡ {html.escape(relacao)}</span>',
            ])
            st.markdown(
                f'<div class="ae-person-profile-main"><h1>{html.escape(primeiro_nome)} <span>✹</span></h1>'
                f'<p>{html.escape(texto_limpo(contato.get("observacoes"), "Pessoa importante dentro da sua história."))}</p>'
                f'<div class="ae-person-profile-facts">{fatos_html}</div>'
                f'<div class="ae-person-profile-chips">{chips_html()}<span class="ae-person-profile-chip ae-plus">＋</span></div></div>',
                unsafe_allow_html=True,
            )
        with acoes_col:
            st.markdown(
                '<div class="ae-person-profile-actions"><span>✎ Editar perfil</span><span>⋮</span></div>',
                unsafe_allow_html=True,
            )

    abas = [
        ("visao", "▦ Visão Geral"),
        ("historias", "📖 Histórias"),
        ("linha", "☷ Linha do Tempo"),
        ("midia", "▧ Fotos e Vídeos"),
        ("contribuicoes", "♙ Contribuições"),
        ("destaques", "♕ Momentos em Destaque"),
    ]
    aba_atual = st.session_state.get("perfil_pessoa_tab", "visao")
    with st.container(key="ae_person_profile_tabs"):
        aba_cols = st.columns(len(abas))
        for indice, (chave, label) in enumerate(abas):
            with aba_cols[indice]:
                texto_aba = f"● {label}" if chave == aba_atual else label
                if st.button(texto_aba, key=f"perfil_pessoa_tab_{chave}", use_container_width=True):
                    st.session_state.perfil_pessoa_tab = chave
                    st.rerun()
    st.markdown(f"<div class='ae-person-profile-tabs-marker is-{html.escape(aba_atual)}'></div>", unsafe_allow_html=True)

    def render_linha_tempo(limitado: bool = False):
        itens = eventos[:3] if limitado else eventos
        if not itens:
            st.markdown("<div class='ae-person-empty-card'>Ainda não há eventos reais ligados a esta pessoa.</div>", unsafe_allow_html=True)
            return
        html_eventos = []
        for evento in itens:
            imagem = f'<img src="{html.escape(evento["imagem"])}" alt="{html.escape(evento["titulo"])}">' if evento.get("imagem") else ""
            html_eventos.append(
                f'<div class="ae-person-timeline-item">'
                f'<div class="ae-person-timeline-icon">{html.escape(evento.get("icone") or "•")}</div>'
                f'<div>'
                f'<strong>{html.escape(str(evento.get("ano") or ""))}</strong>'
                f'<h4>{html.escape(evento.get("titulo") or "")}</h4>'
                f'<p>{html.escape(evento.get("descricao") or "")}</p>'
                f'</div>'
                f'{imagem}'
                f'</div>'
            )
        st.markdown("".join(html_eventos), unsafe_allow_html=True)

    def render_familia():
        if not familiares:
            st.markdown("<div class='ae-person-empty-card'>Nenhuma relação familiar cadastrada ainda.</div>", unsafe_allow_html=True)
            return
        cols = st.columns(min(5, len(familiares)))
        for idx, pessoa in enumerate(familiares):
            nome = texto_limpo(pessoa.get("nome")) or texto_limpo(pessoa.get("nome_completo"), "Pessoa")
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="ae-person-family-avatar">
                        {avatar_html(pessoa, "ae-person-family-photo")}
                        <strong>{html.escape(nome)}</strong>
                        <span>{html.escape(texto_limpo(pessoa.get("parentesco"), "Relação"))}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Abrir", key=f"abrir_familiar_{pessoa.get('id')}", use_container_width=True):
                    st.session_state.perfil_pessoa_id = pessoa.get("id")
                    st.session_state.perfil_pessoa_tab = "visao"
                    st.rerun()

    def render_contribuicoes_lista(limitado: bool = False):
        itens = contribuicoes_relacionadas[:4] if limitado else contribuicoes_relacionadas
        if not itens:
            st.markdown("<div class='ae-person-empty-card'>Ainda não há contribuições reais associadas a esta pessoa.</div>", unsafe_allow_html=True)
            return
        linhas = []
        for item in itens:
            nome = html.escape(texto_limpo(item.get("contribuidor_nome"), nome_exibido))
            data = data_curta(item.get("criado_em"))
            texto = html.escape(resumo(item.get("texto") or item.get("arquivo_nome") or "Contribuição enviada.", 78))
            linhas.append(
                f'<div class="ae-person-contrib-row">'
                f'<div>{html.escape((nome or "P")[:1].upper())}</div>'
                f'<p><strong>{nome}</strong><br>{texto}</p>'
                f'<span>{html.escape(data)}</span>'
                f'</div>'
            )
        st.markdown("".join(linhas), unsafe_allow_html=True)

    def render_historias_grid(limitado: bool = False):
        itens = memorias_relacionadas[:3] if limitado else memorias_relacionadas
        if not itens:
            st.markdown("<div class='ae-person-empty-card'>Nenhuma história real encontrada para esta pessoa.</div>", unsafe_allow_html=True)
            return
        st.markdown(
            f"<div class='ae-person-stories-grid'>{''.join(story_card_html(memoria, compacto=limitado) for memoria in itens)}</div>",
            unsafe_allow_html=True,
        )

    def render_midia():
        fotos = []
        videos = []
        for memoria_id in ids_memorias:
            fotos.extend(fotos_por_memoria.get(memoria_id, []))
            videos.extend(videos_por_memoria.get(memoria_id, []))
        filtro = st.radio(
            "Filtrar mídia",
            ["Todos", "Fotos", "Vídeos"],
            horizontal=True,
            key=f"perfil_midia_filtro_{contato.get('id')}",
            label_visibility="collapsed",
        )
        cards = []
        if filtro in ("Todos", "Fotos"):
            for foto in fotos:
                src = imagem_src(foto.get("caminho"))
                if src:
                    cards.append(f"<div class='ae-person-media-card'><img src='{html.escape(src)}'><strong>{html.escape(texto_limpo(foto.get('titulo'), 'Foto'))}</strong></div>")
        if filtro in ("Todos", "Vídeos"):
            for video in videos:
                cards.append(f"<div class='ae-person-media-card ae-video'><div>▶</div><strong>{html.escape(texto_limpo(video.get('titulo'), 'Vídeo'))}</strong></div>")
        if not cards:
            st.markdown("<div class='ae-person-empty-card'>Nenhuma foto ou vídeo associado a esta pessoa.</div>", unsafe_allow_html=True)
            return
        st.markdown(f"<div class='ae-person-media-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)

    aba_atual = st.session_state.get("perfil_pessoa_tab", "visao")
    if aba_atual == "visao":
        col_sobre, col_linha, col_lateral = st.columns([0.22, 0.43, 0.35])
        with col_sobre:
            with st.container(key="ae_person_panel_sobre"):
                st.markdown(
                    f"""
                    <h3>Sobre {html.escape(primeiro_nome)}</h3>
                    <p>{html.escape(texto_limpo(contato.get("observacoes"), "Nenhuma descrição adicionada ainda."))}</p>
                    <div class="ae-person-added-by">
                        <span>{html.escape(st.session_state.usuario_atual.get("nome", "Você")[:1].upper())}</span>
                        <div>Adicionado por você<br>{html.escape(data_curta(contato.get("criado_em")) or "data não informada")}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with col_linha:
            with st.container(key="ae_person_panel_linha"):
                st.markdown("<div class='ae-person-panel-title'><h3>Linha do Tempo</h3><span>Ver tudo</span></div>", unsafe_allow_html=True)
                render_linha_tempo(limitado=True)
        with col_lateral:
            with st.container(key="ae_person_panel_familia"):
                st.markdown("<div class='ae-person-panel-title'><h3>Família</h3><span>Ver árvore completa</span></div>", unsafe_allow_html=True)
                render_familia()
            with st.container(key="ae_person_panel_contribs"):
                st.markdown("<div class='ae-person-panel-title'><h3>Contribuições recentes</h3><span>Ver todas</span></div>", unsafe_allow_html=True)
                render_contribuicoes_lista(limitado=True)

        col_hist, col_dest = st.columns([0.62, 0.38])
        with col_hist:
            with st.container(key="ae_person_panel_historias"):
                st.markdown(f"<div class='ae-person-panel-title'><h3>Histórias de {html.escape(primeiro_nome)}</h3><span>Ver todas</span></div>", unsafe_allow_html=True)
                render_historias_grid(limitado=True)
        with col_dest:
            with st.container(key="ae_person_panel_destaques"):
                st.markdown("<div class='ae-person-panel-title'><h3>Momentos em destaque</h3><span>Ver todos</span></div>", unsafe_allow_html=True)
                render_historias_grid(limitado=True)
    elif aba_atual == "historias":
        st.markdown(f"<div class='ae-person-panel'><h3>Histórias de {html.escape(primeiro_nome)}</h3>", unsafe_allow_html=True)
        render_historias_grid()
        st.markdown("</div>", unsafe_allow_html=True)
    elif aba_atual == "linha":
        st.markdown("<div class='ae-person-panel'><h3>Linha do Tempo</h3>", unsafe_allow_html=True)
        render_linha_tempo()
        st.markdown("</div>", unsafe_allow_html=True)
    elif aba_atual == "midia":
        st.markdown("<div class='ae-person-panel'><h3>Fotos e Vídeos</h3>", unsafe_allow_html=True)
        render_midia()
        st.markdown("</div>", unsafe_allow_html=True)
    elif aba_atual == "contribuicoes":
        st.markdown("<div class='ae-person-panel'><h3>Contribuições</h3>", unsafe_allow_html=True)
        render_contribuicoes_lista()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='ae-person-panel'><h3>Momentos em Destaque</h3>", unsafe_allow_html=True)
        render_historias_grid()
        st.markdown("</div>", unsafe_allow_html=True)


def render_contatos():
    usuario_id = st.session_state.usuario_atual['id']
    plano = db.obter_plano_usuario(usuario_id)
    contatos_atual = db.contar_contatos_usuario(usuario_id)
    max_contatos = plano.get("max_contatos", 10) if plano else 10
    prioridades_atual = db.contar_contatos_prioritarios(usuario_id)
    max_prioridades = plano.get("max_prioridades", 3) if plano else 3
    contatos = db.listar_contatos_usuario(usuario_id)

    perfil_pessoa_id = st.session_state.get("perfil_pessoa_id")
    if perfil_pessoa_id:
        contato_perfil = next(
            (contato for contato in contatos if str(contato.get("id")) == str(perfil_pessoa_id)),
            None,
        )
        if contato_perfil:
            render_perfil_pessoa_vivo(contato_perfil, contatos, usuario_id)
            return
        st.session_state.pop("perfil_pessoa_id", None)

    cab_col, acao_col = st.columns([0.72, 0.28], vertical_alignment="center")
    with cab_col:
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
    with acao_col:
        if st.button("＋ Adicionar Pessoa", key="abrir_adicionar_pessoa_topo", type="primary", use_container_width=True):
            st.session_state.pop("contato_prefill_nome", None)
            st.session_state.pop("contato_prefill_sobrenome", None)
            st.session_state.pop("contato_prefill_normalizado", None)
            st.session_state.pop("contato_prefill_origem", None)
            st.session_state.pop("contato_nome_cadastro", None)
            st.session_state.pop("contato_sobrenome_cadastro", None)
            st.session_state.pop("contato_email_cadastro", None)
            st.session_state.pop("contato_whatsapp_cadastro", None)
            st.session_state.abrir_form_contato = True
            st.rerun()

    if st.session_state.get("contato_salvo_msg"):
        st.success(st.session_state.contato_salvo_msg)
        st.code(st.session_state.contato_chave_msg)

        if st.button("Ocultar chave"):
            del st.session_state.contato_salvo_msg
            del st.session_state.contato_chave_msg
            st.rerun()

    contato_prefill_nome = st.session_state.get("contato_prefill_nome", "")
    contato_prefill_sobrenome = st.session_state.get("contato_prefill_sobrenome", "")
    contato_origem_sugestao = st.session_state.get("contato_prefill_origem") == "sugestao"
    if st.session_state.pop("contato_aplicar_prefill", False):
        st.session_state.contato_nome_cadastro = contato_prefill_nome
        st.session_state.contato_sobrenome_cadastro = contato_prefill_sobrenome
        st.session_state.contato_email_cadastro = ""
        st.session_state.contato_whatsapp_cadastro = ""

    if st.session_state.get("abrir_form_contato"):
        st.markdown('<div class="ae-inline-person-form">', unsafe_allow_html=True)
        with st.form("form_adicionar_contato", clear_on_submit=True):
            st.markdown("**📝 Nome completo ***")

            col_n1, col_n2 = st.columns(2)
            with col_n1:
                nome = st.text_input("nome", placeholder="Nome", label_visibility="collapsed", key="contato_nome_cadastro")
            with col_n2:
                sobrenome = st.text_input("sobrenome", placeholder="Sobrenome", label_visibility="collapsed", key="contato_sobrenome_cadastro")

            st.markdown("**📧 Forma de contato ***")

            col_c1, col_c2 = st.columns(2)
            with col_c1:
                email = st.text_input("email", placeholder="E-mail", label_visibility="collapsed", key="contato_email_cadastro")
            with col_c2:
                whatsapp = st.text_input("whatsapp", placeholder="WhatsApp", label_visibility="collapsed", key="contato_whatsapp_cadastro")

            if contato_origem_sugestao:
                st.caption("Sugestão encontrada nas histórias. E-mail e WhatsApp são opcionais; nenhum acesso será liberado agora.")
            else:
                st.caption("⚠️ Pelo menos um contato (e-mail ou WhatsApp) é obrigatório")

            st.markdown("---")
            st.markdown("#### ✨ Informações adicionais (opcional)")

            parentesco = st.selectbox(
                "Relação",
                [
                    "",
                    "Mãe",
                    "Pai",
                    "Filho(a)",
                    "Cônjuge",
                    "Irmão(ã)",
                    "Avó",
                    "Avô",
                    "Neto(a)",
                    "Tio(a)",
                    "Sobrinho(a)",
                    "Primo(a)",
                    "Amigo(a)",
                    "Advogado(a)",
                    "Outro",
                ]
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
                elif not email and not whatsapp and not contato_origem_sugestao:
                    st.error("❌ Informe pelo menos um contato (e-mail ou WhatsApp)")
                elif is_prioridade and prioridades_atual >= max_prioridades:
                    st.warning(
                        f"⚠️ Você já tem {prioridades_atual} pessoas prioritárias. "
                        f"Limite: {max_prioridades}."
                    )
                else:
                    chave_acesso = "" if contato_origem_sugestao else secrets.token_hex(8)

                    contato_id_criado = db.adicionar_contato(
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
                        acesso_central_luto=0 if contato_origem_sugestao else (1 if acesso_central_luto else 0),
                        chave_acesso=chave_acesso,
                    )

                    if email:
                        nome_usuario = (
                            f"{st.session_state.usuario_atual.get('nome', '')} "
                            f"{st.session_state.usuario_atual.get('sobrenome', '')}"
                        ).strip() or "Alguém"
                        convite_enviado = EmailService().enviar_convite_pessoa_importante(
                            destinatario_email=email,
                            nome_destinatario=f"{nome} {sobrenome}".strip(),
                            nome_usuario=nome_usuario,
                        )
                        db.registrar_convite_pessoa(
                            usuario_id=usuario_id,
                            contato_id=contato_id_criado,
                            nome_destinatario=f"{nome} {sobrenome}".strip(),
                            email_destinatario=email,
                            status="enviado" if convite_enviado else "aguardando_configuracao",
                        )

                    st.session_state.contato_salvo_msg = f"✅ {nome} {sobrenome} adicionado!"
                    st.session_state.contato_chave_msg = (
                        "Nenhum acesso foi liberado automaticamente."
                        if contato_origem_sugestao
                        else f"🔑 Chave de acesso: {chave_acesso}"
                    )
                    if contato_origem_sugestao:
                        db.atualizar_status_pessoa_sugerida(
                            usuario_id,
                            st.session_state.get("contato_prefill_normalizado")
                            or normalizar_nome_pessoa(f"{nome} {sobrenome}"),
                            "aceita",
                            nome_sugerido=f"{nome} {sobrenome}".strip(),
                        )
                    st.session_state.pop("contato_prefill_nome", None)
                    st.session_state.pop("contato_prefill_sobrenome", None)
                    st.session_state.pop("contato_prefill_normalizado", None)
                    st.session_state.pop("contato_prefill_origem", None)
                    st.session_state.pop("abrir_form_contato", None)
                    st.session_state.pop("contato_nome_cadastro", None)
                    st.session_state.pop("contato_sobrenome_cadastro", None)
                    st.session_state.pop("contato_email_cadastro", None)
                    st.session_state.pop("contato_whatsapp_cadastro", None)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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

    sugestoes_detectadas = extrair_pessoas_encontradas(memorias_usuario, contatos)
    sugestoes_detectadas_norm = {
        sugestao.get("nome_normalizado") or normalizar_nome_pessoa(sugestao.get("nome", ""))
        for sugestao in sugestoes_detectadas
    }
    try:
        db.sincronizar_pessoas_sugeridas(usuario_id, sugestoes_detectadas)
        sugestoes_pessoas = [
            sugestao
            for sugestao in db.listar_pessoas_sugeridas_pendentes(usuario_id, limite=12)
            if (sugestao.get("nome_normalizado") or normalizar_nome_pessoa(sugestao.get("nome", "")))
               in sugestoes_detectadas_norm
        ][:4]
    except Exception as exc:
        print("Erro ao sincronizar sugestões de pessoas:", exc)
        sugestoes_pessoas = sugestoes_detectadas[:4]

    def abrir_formulario_pessoa_sugerida(
            nome_sugerido: str,
            nome_normalizado: str,
    ):
        partes_nome = str(nome_sugerido or "Pessoa").split()
        st.session_state.contato_prefill_nome = partes_nome[0] if partes_nome else str(nome_sugerido or "Pessoa")
        st.session_state.contato_prefill_sobrenome = " ".join(partes_nome[1:])
        st.session_state.contato_prefill_normalizado = nome_normalizado
        st.session_state.contato_prefill_origem = "sugestao"
        st.session_state.contato_aplicar_prefill = True
        st.session_state.abrir_form_contato = True
        st.session_state.pop("contato_nome_cadastro", None)
        st.session_state.pop("contato_sobrenome_cadastro", None)
        st.session_state.pop("contato_email_cadastro", None)
        st.session_state.pop("contato_whatsapp_cadastro", None)

    ranking = sorted(
        (
            (contato, presencas.get(contato["id"], 0))
            for contato in contatos
            if presencas.get(contato["id"], 0)
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    if ranking or sugestoes_pessoas:
        with st.container(key="ae_people_presentes_panel"):
            st.markdown(
                """
                <div class="ae-people-presentes-head">
                    <strong>Pessoas mais presentes nas suas histórias</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
            chips_cols = st.columns([1.42, 1.42, 1, 1, 1, 1, 1.2], gap="small")
            for indice, (contato, total) in enumerate(ranking[:2]):
                nome_chip = contato.get("nome") or contato.get("nome_completo") or "Pessoa"
                with chips_cols[indice]:
                    st.markdown(
                        f"<div class='ae-person-chip ae-person-chip-static'>👥 {html.escape(nome_chip)} • {total} histórias</div>",
                        unsafe_allow_html=True,
                    )
            if sugestoes_pessoas:
                for indice, sugestao in enumerate(sugestoes_pessoas[:4]):
                    nome_sugerido = sugestao.get("nome", "Pessoa")
                    nome_normalizado = sugestao.get("nome_normalizado") or normalizar_nome_pessoa(nome_sugerido)
                    with chips_cols[indice + 2]:
                        st.button(
                            f"⭐ {nome_sugerido}",
                            key=f"add_sugestao_{nome_normalizado}",
                            help="Adicionar como Pessoa Importante",
                            use_container_width=True,
                            on_click=abrir_formulario_pessoa_sugerida,
                            args=(
                                nome_sugerido,
                                nome_normalizado,
                            ),
                        )
            st.markdown(
                '<p class="ae-people-suggestion-note">⭐ Sugestões encontradas automaticamente nas suas histórias. Clique no nome para adicionar.</p>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="ae-people-grid-heading"><div>Sua rede de pessoas</div><span>Ver todas ›</span></div>',
        unsafe_allow_html=True,
    )
    for inicio in range(0, len(contatos), 5):
        colunas = st.columns(5)
        for indice, coluna in enumerate(colunas):
            posicao = inicio + indice
            if posicao >= len(contatos):
                continue
            contato = contatos[posicao]
            nome_exibido = contato.get("nome_completo") or contato.get("nome") or "Pessoa"
            inicial = html.escape(nome_exibido[:1].upper() or "P")
            relacao = contato.get("parentesco") or "Relação importante"
            historias_contato = presencas.get(contato["id"], 0)
            indicadores_card = []
            indicadores_card.append(f"👥 {historias_contato} histórias")
            if contato.get("acesso_central_luto"):
                indicadores_card.append("🔓 acesso ativo")
            elif contato.get("email"):
                indicadores_card.append("✉ convidada")
            if contato.get("is_prioridade"):
                indicadores_card.append("⭐ prioridade")
            indicadores_html = "".join(f"<span>{html.escape(item)}</span>" for item in indicadores_card[:3])
            with coluna:
                st.markdown(
                    f"""
                    <div class="ae-important-person-card">
                        <div class="ae-card-menu">⋮</div>
                        <div class="ae-important-avatar">{inicial}</div>
                        <h3>{html.escape(nome_exibido)}</h3>
                        <strong>{html.escape(relacao)}</strong>
                        <div class="ae-card-divider"></div>
                        <p>Presente em {historias_contato} histórias</p>
                        <div class="ae-important-indicators">{indicadores_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Ver perfil", key=f"abrir_perfil_pessoa_{contato.get('id')}", use_container_width=True):
                    st.session_state.perfil_pessoa_id = contato.get("id")
                    st.session_state.perfil_pessoa_tab = "visao"
                    st.rerun()
    try:
        convites = db.listar_convites_pessoas(usuario_id, limite=4)
    except Exception as exc:
        print("Erro ao listar convites de pessoas:", exc)
        convites = []

    if convites:
        itens_convite = []
        for convite in convites:
            nome_convite = html.escape(convite.get("nome") or "Pessoa")
            inicial_convite = html.escape((convite.get("nome") or "P")[:1].upper())
            status_convite = convite.get("status") or "enviado"
            status_label = "Enviado" if status_convite == "enviado" else "Aguardando cadastro"
            data_envio = str(convite.get("criado_em") or "")[:10]
            itens_convite.append(
                f"""
                <div class="ae-invite-row">
                    <div class="ae-invite-avatar">{inicial_convite}</div>
                    <div>
                        <strong>{nome_convite}</strong>
                        <span>Convite enviado em {html.escape(data_envio)}</span>
                    </div>
                    <em>{html.escape(status_label)}</em>
                    <b>⋮</b>
                </div>
                """
            )

        st.markdown(
            f"""
            <div class="ae-invites-panel">
                <div class="ae-people-grid-heading"><div>Convites enviados</div><span>Ver todos ›</span></div>
                <div class="ae-invites-grid">{''.join(itens_convite)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


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
    import base64 as _b64
    try:
        with open("assets/correcttree.png", "rb") as _f:
            _tree_src = "data:image/png;base64," + _b64.b64encode(_f.read()).decode()
    except Exception:
        _tree_src = ""

    qtd_memorias = st.session_state.get("_ae_qtd_memorias", 0)
    qtd_cofre    = st.session_state.get("_ae_qtd_cofre",    0)
    qtd_contatos = st.session_state.get("_ae_qtd_contatos", 0)

    lim_memorias = 10
    lim_medias   = 20
    lim_contribs = 5

    mem_pct     = min(100, int(qtd_memorias / lim_memorias * 100)) if lim_memorias > 0 else 0
    media_pct   = min(100, int(qtd_cofre    / lim_medias   * 100)) if lim_medias   > 0 else 0
    contrib_pct = min(100, int(qtd_contatos / lim_contribs * 100)) if lim_contribs > 0 else 0

    mem_danger     = " ae-bar-danger" if mem_pct     >= 90 else ""
    media_danger   = " ae-bar-danger" if media_pct   >= 90 else ""
    contrib_danger = " ae-bar-danger" if contrib_pct >= 90 else ""

    st.markdown(f"""
<style>
.ae-plans-page {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-family: 'Inter', sans-serif;
    width: 100%;
    max-width: 1140px;
    box-sizing: border-box;
}}
.ae-hero-container {{
    height: 100px;
    background: #FFFFFF;
    border: 1px solid #E8DCC6;
    border-radius: 20px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
}}
.ae-hero-icon {{
    width: 56px;
    height: 56px;
    min-width: 56px;
    background: #F8F5EE;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}}
.ae-hero-text {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding-top: 2px;
}}
.ae-hero-title {{
    font-size: 20px;
    font-weight: 700;
    color: #24125A;
    line-height: 26px;
    margin: 0 0 4px 0;
}}
.ae-hero-subtitle {{
    font-size: 13px;
    font-weight: 400;
    color: #555555;
    line-height: 18px;
    margin: 0;
}}
.ae-hero-btn {{
    height: 40px;
    width: 170px;
    min-width: 170px;
    background: #5A2BB5;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    align-self: center;
    flex-shrink: 0;
    transition: background 0.2s;
}}
.ae-hero-btn:hover {{ background: #4A22A4; }}
.ae-hero-tree {{
    width: 200px;
    height: 72px;
    min-width: 200px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    align-self: center;
    flex-shrink: 0;
    overflow: hidden;
}}
.ae-status-container {{
    height: 272px;
    display: flex;
    gap: 24px;
    box-sizing: border-box;
}}
.ae-free-usage-card {{
    width: 430px;
    min-width: 430px;
    height: 272px;
    background: #FFFFFF;
    border: 1px solid #E8DCC6;
    border-radius: 20px;
    padding: 24px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}}
.ae-fuc-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}}
.ae-fuc-title {{
    font-size: 16px;
    font-weight: 700;
    color: #24125A;
}}
.ae-fuc-badge {{
    background: #F0EBF8;
    color: #5A2BB5;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}}
.ae-fuc-subtitle {{
    font-size: 13px;
    color: #666666;
    margin-bottom: 10px;
    font-weight: 400;
}}
.ae-fuc-metric {{
    margin-bottom: 9px;
}}
.ae-fuc-metric-row {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
}}
.ae-fuc-metric-name {{
    font-size: 13px;
    color: #555555;
    font-weight: 400;
}}
.ae-fuc-metric-count {{
    font-size: 13px;
    color: #24125A;
    font-weight: 600;
}}
.ae-bar-track {{
    height: 6px;
    background: #EDE8F5;
    border-radius: 999px;
    overflow: hidden;
}}
.ae-bar-fill {{
    height: 100%;
    background: #5A2BB5;
    border-radius: 999px;
}}
.ae-bar-danger {{
    background: #E05858 !important;
}}
.ae-fuc-footer {{
    margin-top: auto;
    padding-top: 12px;
    border-top: 1px solid #F0EBF8;
    font-size: 12px;
    color: #888888;
    text-align: center;
}}
.ae-limit-card {{
    flex: 1;
    height: 272px;
    background: #FFFFFF;
    border: 1px solid #E8DCC6;
    border-radius: 20px;
    padding: 24px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.ae-limit-card-inner {{
    height: 152px;
    width: 100%;
    background: #F3EDF8;
    border-radius: 16px;
    padding: 14px 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}
.ae-limit-lock {{
    font-size: 26px;
    margin-bottom: 6px;
    line-height: 1;
}}
.ae-limit-title {{
    font-size: 15px;
    font-weight: 700;
    color: #24125A;
    font-family: 'Inter', sans-serif;
    margin: 0 0 5px 0;
    line-height: 1.3;
}}
.ae-limit-text {{
    font-size: 13px;
    font-weight: 400;
    color: #555555;
    font-family: 'Inter', sans-serif;
    margin: 0 0 10px 0;
    line-height: 1.4;
}}
.ae-limit-btn {{
    height: 36px;
    width: 180px;
    background: #5A2BB5;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    transition: background 0.2s;
}}
.ae-limit-btn:hover {{ background: #4A22A4; }}
.ae-pricing-container {{
    height: 362px;
    background: #FFFFFF;
    border: 1px solid #E8DCC6;
    border-radius: 20px;
    padding: 16px 18px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}
.ae-pricing-header {{
    height: 38px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 8px;
    flex-shrink: 0;
}}
.ae-pricing-title {{
    font-size: 16px;
    font-weight: 700;
    color: #24125A;
    margin: 0 0 2px 0;
    font-family: 'Inter', sans-serif;
}}
.ae-pricing-subtitle {{
    font-size: 12px;
    font-weight: 400;
    color: #666666;
    margin: 0;
    font-family: 'Inter', sans-serif;
}}
.ae-plans-row {{
    display: flex;
    gap: 14px;
    flex: 1;
    align-items: stretch;
    overflow: hidden;
}}
.ae-plan-free, .ae-plan-legacy {{
    flex: 1;
    min-width: 0;
    height: 100%;
    background: #FFFFFF;
    border: 1px solid #E8DCC6;
    border-radius: 16px;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    font-family: 'Inter', sans-serif;
}}
.ae-plan-family {{
    flex: 1;
    min-width: 0;
    height: 100%;
    background: #FFFFFF;
    border: 2px solid #8D5AE8;
    border-radius: 16px;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    font-family: 'Inter', sans-serif;
    position: relative;
    margin-top: 0;
}}
.ae-plan-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 30px;
    width: 115px;
    background: #D9A328;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
    border-radius: 999px;
    margin-bottom: 8px;
    font-family: 'Inter', sans-serif;
}}
.ae-plan-name {{
    font-size: 16px;
    font-weight: 700;
    color: #24125A;
    margin: 0 0 2px 0;
}}
.ae-plan-desc {{
    font-size: 12px;
    font-weight: 400;
    color: #666666;
    margin: 0 0 6px 0;
    line-height: 1.3;
}}
.ae-plan-price {{
    font-size: 20px;
    font-weight: 700;
    color: #24125A;
    margin: 0 0 8px 0;
    line-height: 1.2;
}}
.ae-plan-price-free {{
    font-size: 20px;
}}
.ae-plan-features {{
    list-style: none;
    margin: 0 0 auto 0;
    padding: 0;
    flex: 1;
}}
.ae-plan-features li {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-size: 12px;
    font-weight: 400;
    color: #555555;
    margin-bottom: 4px;
    line-height: 1.3;
}}
.ae-check-free {{
    width: 18px;
    height: 18px;
    min-width: 18px;
    border-radius: 50%;
    background: #E8F5E9;
    color: #2E7D32;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
}}
.ae-check-family {{
    width: 18px;
    height: 18px;
    min-width: 18px;
    border-radius: 50%;
    background: #EDE8F8;
    color: #5A2BB5;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
}}
.ae-check-legacy {{
    width: 18px;
    height: 18px;
    min-width: 18px;
    border-radius: 50%;
    background: #FDF5E0;
    color: #B87A00;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
}}
.ae-plan-btn-current {{
    height: 36px;
    width: 100%;
    background: #F0EBF8;
    color: #5A2BB5;
    border: 1px solid #D0C0F0;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: default;
    margin-top: 12px;
}}
.ae-plan-btn-family {{
    height: 36px;
    width: 100%;
    background: #5A2BB5;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    margin-top: 12px;
    transition: background 0.2s;
}}
.ae-plan-btn-family:hover {{ background: #4A22A4; }}
.ae-plan-btn-legacy {{
    height: 36px;
    width: 100%;
    background: #D9A328;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    margin-top: 12px;
    transition: background 0.2s;
}}
.ae-plan-btn-legacy:hover {{ background: #B87A00; }}
.ae-security-container {{
    height: 54px;
    background: #FFFFFF;
    border: 1px solid #E8DCC6;
    border-radius: 16px;
    padding: 0 24px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.ae-security-icon {{
    font-size: 22px;
    flex-shrink: 0;
}}
.ae-security-text {{
    font-size: 14px;
    font-weight: 400;
    color: #555555;
    font-family: 'Inter', sans-serif;
    flex: 1;
}}
.ae-security-link {{
    font-size: 14px;
    font-weight: 600;
    color: #5A2BB5;
    font-family: 'Inter', sans-serif;
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
}}
.ae-security-link:hover {{ text-decoration: underline; }}
</style>
<div class="ae-plans-page">
<div class="ae-hero-container">
<div class="ae-hero-icon">❤️</div>
<div class="ae-hero-text">
<p class="ae-hero-title">Preserve tudo para sua família</p>
<p class="ae-hero-subtitle">Suas histórias merecem durar para sempre.</p>
</div>
<button class="ae-hero-btn" onclick="document.querySelector('.ae-pricing-container').scrollIntoView({{behavior:'smooth'}})">Conhecer planos</button>
<div class="ae-hero-tree"><img src="{_tree_src}" alt="árvore" style="height:72px;width:auto;object-fit:contain;display:block;"/></div>
</div>
<div class="ae-status-container">
<div class="ae-free-usage-card">
<div class="ae-fuc-header">
<span class="ae-fuc-title">Uso atual</span>
<span class="ae-fuc-badge">Plano Gratuito</span>
</div>
<p class="ae-fuc-subtitle">Acompanhe o que você já preservou.</p>
<div class="ae-fuc-metric">
<div class="ae-fuc-metric-row">
<span class="ae-fuc-metric-name">Memórias</span>
<span class="ae-fuc-metric-count">{qtd_memorias} / {lim_memorias}</span>
</div>
<div class="ae-bar-track"><div class="ae-bar-fill{mem_danger}" style="width:{mem_pct}%"></div></div>
</div>
<div class="ae-fuc-metric">
<div class="ae-fuc-metric-row">
<span class="ae-fuc-metric-name">Fotos e vídeos</span>
<span class="ae-fuc-metric-count">{qtd_cofre} / {lim_medias}</span>
</div>
<div class="ae-bar-track"><div class="ae-bar-fill{media_danger}" style="width:{media_pct}%"></div></div>
</div>
<div class="ae-fuc-metric">
<div class="ae-fuc-metric-row">
<span class="ae-fuc-metric-name">Contribuições</span>
<span class="ae-fuc-metric-count">{qtd_contatos} / {lim_contribs}</span>
</div>
<div class="ae-bar-track"><div class="ae-bar-fill{contrib_danger}" style="width:{contrib_pct}%"></div></div>
</div>
<div class="ae-fuc-footer">Faça upgrade para remover todos os limites</div>
</div>
<div class="ae-limit-card">
<div class="ae-limit-card-inner">
<div class="ae-limit-lock">🔒</div>
<p class="ae-limit-title">Você chegou ao limite<br>do plano gratuito.</p>
<p class="ae-limit-text">Continue preservando as histórias<br>da sua família.</p>
<button class="ae-limit-btn" onclick="document.querySelector('.ae-pricing-container').scrollIntoView({{behavior:'smooth'}})">Ver planos</button>
</div>
</div>
</div>
<div class="ae-pricing-container">
<div class="ae-pricing-header">
<p class="ae-pricing-title">Escolha o plano ideal para sua família</p>
<p class="ae-pricing-subtitle">Selecione o plano que melhor se adapta às suas necessidades</p>
</div>
<div class="ae-plans-row">
<div class="ae-plan-free">
<p class="ae-plan-name">Gratuito</p>
<p class="ae-plan-desc">Para começar a preservar sua história</p>
<p class="ae-plan-price ae-plan-price-free">Grátis</p>
<ul class="ae-plan-features">
<li><span class="ae-check-free">✓</span>Até 10 memórias</li>
<li><span class="ae-check-free">✓</span>Até 20 fotos e vídeos</li>
<li><span class="ae-check-free">✓</span>Até 5 contribuições</li>
</ul>
<button class="ae-plan-btn-current" disabled>Plano atual</button>
</div>
<div class="ae-plan-family">
<span class="ae-plan-badge">Mais Popular</span>
<p class="ae-plan-name">Familiar</p>
<p class="ae-plan-desc">Para preservar todas as memórias da família</p>
<p class="ae-plan-price">R$ 14,90<span style="font-size:14px;font-weight:400;color:#666">/mês</span></p>
<ul class="ae-plan-features">
<li><span class="ae-check-family">✓</span>Memórias ilimitadas</li>
<li><span class="ae-check-family">✓</span>Fotos e vídeos ilimitados</li>
<li><span class="ae-check-family">✓</span>Contribuições ilimitadas</li>
<li><span class="ae-check-family">✓</span>Colaboração familiar</li>
<li><span class="ae-check-family">✓</span>Curador de histórias</li>
</ul>
<button class="ae-plan-btn-family">Assinar Plano Familiar</button>
</div>
<div class="ae-plan-legacy">
<p class="ae-plan-name">Legado</p>
<p class="ae-plan-desc">Para preservar sua história para gerações</p>
<p class="ae-plan-price">R$ 29,90<span style="font-size:14px;font-weight:400;color:#666">/mês</span></p>
<ul class="ae-plan-features">
<li><span class="ae-check-legacy">✓</span>Memórias ilimitadas</li>
<li><span class="ae-check-legacy">✓</span>Armazenamento permanente</li>
<li><span class="ae-check-legacy">✓</span>Histórico completo</li>
<li><span class="ae-check-legacy">✓</span>Prioridade no suporte</li>
</ul>
<button class="ae-plan-btn-legacy">Assinar Plano Legado</button>
</div>
</div>
</div>
<div class="ae-security-container">
<span class="ae-security-icon">🔒</span>
<span class="ae-security-text">Seus dados são protegidos com criptografia de ponta. Cancele a qualquer momento, sem multa.</span>
<a class="ae-security-link" href="#">Saiba mais sobre segurança</a>
</div>
</div>
""", unsafe_allow_html=True)
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
    CARD = "background:rgba(255,255,255,.94);border:1px solid rgba(222,202,166,.8);border-radius:18px;box-shadow:0 18px 44px rgba(70,46,20,.08);"

    def formatar_data(valor) -> str:
        if not valor:
            return ""
        if hasattr(valor, "strftime"):
            return valor.strftime("%d/%m/%Y")
        return str(valor)[:10]

    def iniciais(nome: str) -> str:
        partes = [p for p in str(nome or "Pessoa").split() if p]
        if len(partes) >= 2:
            return (partes[0][:1] + partes[-1][:1]).upper()
        return (partes[0][:1] if partes else "P").upper()

    def texto_curto(valor: str, limite: int = 150) -> str:
        texto = re.sub(r"\s+", " ", str(valor or "")).strip()
        return texto if len(texto) <= limite else texto[:limite].rstrip() + "..."

    def tipo_label(contribuicao: dict) -> str:
        arquivo_tipo = contribuicao.get("arquivo_tipo") or ""
        texto = bool(contribuicao.get("texto"))
        if arquivo_tipo.startswith("image/") and texto:
            return "Texto + foto"
        if arquivo_tipo.startswith("video/") and texto:
            return "Texto + vídeo"
        if arquivo_tipo.startswith("image/"):
            return "Foto"
        if arquivo_tipo.startswith("video/"):
            return "Vídeo"
        return "Texto"

    pendentes = db.listar_contribuicoes_pendentes(usuario_dono_id)
    listar_todas = getattr(db, "listar_contribuicoes_usuario", None)
    todas = listar_todas(usuario_dono_id) if callable(listar_todas) else pendentes
    aprovadas = [c for c in todas if c.get("status") == "aprovado"]
    rejeitadas = [c for c in todas if c.get("status") == "rejeitado"]
    pessoas = {c.get("contribuidor_email") or c.get("contribuidor_nome") for c in todas if c.get("contribuidor_nome") or c.get("contribuidor_email")}

    st.markdown(
        '<div class="ae-contrib-hero" style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;margin:.55rem 0 .65rem;">'
        '<div><h1 style="color:#21104a;font-size:2.05rem;line-height:1;margin:0 0 .22rem;font-weight:900;">✦ Contribuições</h1>'
        '<p style="color:#6d6380;font-size:.92rem;margin:0;">Lembranças, fotos e vídeos enviados por pessoas importantes para enriquecer suas histórias.</p></div>'
        '<span style="border:1.5px solid rgba(104,79,176,.55);border-radius:11px;color:#21104a;font-weight:900;padding:.58rem 1rem;background:rgba(255,255,255,.55);white-space:nowrap;">↗ Ver histórico completo</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="ae-contrib-summary" style="{CARD}padding:.8rem 1rem .9rem;margin-bottom:.7rem;">'
        '<h3 style="color:#21104a;margin:0 0 .55rem;font-size:1.08rem;font-weight:900;">Resumo das contribuições</h3>'
        '<div class="ae-contrib-summary-grid" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;">'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:.7rem;border-radius:11px;min-height:34px;font-weight:900;border:1.5px solid #daa742;background:rgba(255,248,231,.72);"><strong style="color:#21104a;font-size:1.12rem;">{len(pendentes)}</strong><span style="color:#21104a;font-size:.82rem;">Aguardando aprovação</span></div>'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:.7rem;border-radius:11px;min-height:34px;font-weight:900;border:1.5px solid #48a36d;background:rgba(236,252,242,.72);"><strong style="color:#21104a;font-size:1.12rem;">{len(aprovadas)}</strong><span style="color:#21104a;font-size:.82rem;">Aprovadas</span></div>'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:.7rem;border-radius:11px;min-height:34px;font-weight:900;border:1.5px solid #e98b8b;background:rgba(255,240,240,.72);"><strong style="color:#21104a;font-size:1.12rem;">{len(rejeitadas)}</strong><span style="color:#21104a;font-size:.82rem;">Rejeitadas</span></div>'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:.7rem;border-radius:11px;min-height:34px;font-weight:900;border:1.5px solid #9b86d5;background:rgba(247,243,255,.72);"><strong style="color:#21104a;font-size:1.12rem;">{len(pessoas)}</strong><span style="color:#21104a;font-size:.82rem;">Pessoas contribuíram</span></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    main_col, side_col = st.columns([0.64, 0.36], gap="medium")

    with main_col:
        st.markdown(
            '<div class="ae-contrib-section-title" style="margin:.15rem 0 .35rem;"><h2 style="color:#21104a;font-size:1.22rem;margin:0;font-weight:900;">Aguardando sua aprovação</h2>'
            '<p style="color:#6d6380;margin:.08rem 0 0;font-size:.9rem;">Nada entra na sua história sem sua autorização.</p></div>',
            unsafe_allow_html=True,
        )
        if not pendentes:
            st.markdown(
                '<div class="ae-contrib-empty" style="border:1px dashed rgba(104,79,176,.28);background:rgba(255,255,255,.55);border-radius:14px;color:#6d6380;padding:.75rem .9rem;font-size:.9rem;">'
                '<strong style="color:#21104a;display:block;margin-bottom:.18rem;">Nenhuma contribuição aguardando aprovação.</strong>'
                '<span>Quando alguém enviar uma lembrança, foto ou vídeo para enriquecer suas histórias, ela aparecerá aqui.</span></div>',
                unsafe_allow_html=True,
            )

    with side_col:
        fluxo = [
            ("1", "Receber", "Contato envia texto, foto ou vídeo."),
            ("2", "Revisar", "Você vê o conteúdo antes de publicar."),
            ("3", "Aprovar", "A contribuição entra na história."),
            ("4", "Rejeitar", "Nada aparece para visitantes."),
        ]
        fluxo_html = "".join(
            f'<div class="ae-contrib-flow-row" style="display:grid;grid-template-columns:32px 1fr;gap:.55rem;align-items:center;margin:.48rem 0;">'
            f'<span style="width:28px;height:28px;border-radius:999px;display:grid;place-items:center;background:#dfa93d;color:white;font-weight:900;font-size:.86rem;">{n}</span>'
            f'<p style="color:#6d6380;margin:0;line-height:1.18;font-size:.88rem;"><strong style="display:block;color:#21104a;">{html.escape(titulo)}</strong>{html.escape(desc)}</p></div>'
            for n, titulo, desc in fluxo
        )
        contagem = {}
        for c in todas:
            nome = c.get("contribuidor_nome") or "Pessoa convidada"
            contagem[nome] = contagem.get(nome, 0) + 1
        recentes_html = "".join(
            f'<div class="ae-contrib-person-row" style="display:grid;grid-template-columns:46px 1fr auto;gap:.65rem;align-items:center;padding:.55rem 0;">'
            f'<div style="width:42px;height:42px;border-radius:999px;display:grid;place-items:center;color:#21104a;background:linear-gradient(135deg,#efe6dc,#d7c9ec);font-weight:900;">{html.escape(iniciais(nome))}</div>'
            f'<p style="margin:0;color:#6d6380;line-height:1.25;"><strong style="display:block;color:#21104a;">{html.escape(nome)}</strong>{qtd} {"contribuição" if qtd == 1 else "contribuições"}</p>'
            '<button style="border:1px solid rgba(218,167,66,.42);border-radius:9px;background:rgba(255,248,231,.75);color:#21104a;font-weight:800;padding:.45rem .7rem;">Ver perfil</button></div>'
            for nome, qtd in list(sorted(contagem.items(), key=lambda item: item[1], reverse=True))[:3]
        ) or '<div class="ae-contrib-empty-small" style="border:1px dashed rgba(104,79,176,.28);background:rgba(255,255,255,.55);border-radius:14px;color:#6d6380;padding:.75rem .9rem;font-size:.9rem;">Nenhum contribuidor recente.</div>'
        st.markdown(
            f'<div class="ae-contrib-side-card" style="{CARD}padding:.75rem .9rem;margin:0 0 .55rem;"><h3 style="color:#21104a;margin:0 0 .45rem;font-size:1.08rem;font-weight:900;">Fluxo de aprovação</h3>{fluxo_html}</div>'
            f'<div class="ae-contrib-side-card" style="{CARD}padding:.75rem .9rem;margin:0 0 .55rem;"><h3 style="color:#21104a;margin:0 0 .45rem;font-size:1.08rem;font-weight:900;">Contribuidores recentes</h3>{recentes_html}</div>',
            unsafe_allow_html=True,
        )

    for contribuicao in pendentes:
        nome = contribuicao.get("contribuidor_nome") or "Pessoa convidada"
        titulo = contribuicao.get("memoria_titulo") or "História sem título"
        texto = texto_curto(contribuicao.get("texto") or contribuicao.get("arquivo_nome") or "Contribuição enviada.")
        media_chips = ""
        arquivo_tipo = contribuicao.get("arquivo_tipo") or ""
        if arquivo_tipo.startswith("image/"):
            media_chips = '<span style="display:block;width:62px;height:28px;border-radius:6px;background:linear-gradient(135deg,#d8af5d,#ead8b8);"></span><span style="display:block;width:62px;height:28px;border-radius:6px;background:linear-gradient(135deg,#b8d7bd,#e6f2e6);"></span>'
        elif arquivo_tipo.startswith("video/"):
            media_chips = '<span style="display:block;width:62px;height:28px;border-radius:6px;background:linear-gradient(135deg,#a8c9d8,#e8f3f7);"></span><span style="display:block;width:62px;height:28px;border-radius:6px;background:linear-gradient(135deg,#d8af5d,#ead8b8);"></span>'
        else:
            media_chips = '<span style="display:block;width:62px;height:28px;border-radius:6px;background:linear-gradient(135deg,#d8af5d,#ead8b8);"></span>'

        st.markdown(
            f'<div class="ae-contrib-card" style="{CARD}display:grid;grid-template-columns:54px 1fr;gap:.85rem;padding:1rem;margin:.65rem 0 .25rem;">'
            f'<div class="ae-contrib-avatar" style="width:48px;height:48px;border-radius:999px;display:grid;place-items:center;color:#21104a;background:linear-gradient(135deg,#efe6dc,#d7c9ec);font-weight:900;font-size:1.05rem;">{html.escape(iniciais(nome))}</div>'
            f'<div class="ae-contrib-card-body"><div class="ae-contrib-card-head" style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;margin-bottom:.45rem;"><div><strong style="color:#21104a;font-size:1.05rem;">{html.escape(nome)}</strong><p style="color:#6d6380;margin:0;font-size:.82rem;">{html.escape(tipo_label(contribuicao))} enviada em {html.escape(formatar_data(contribuicao.get("criado_em")))}</p></div><em style="border:1px solid rgba(218,167,66,.55);border-radius:999px;color:#21104a;background:rgba(255,248,231,.75);font-style:normal;font-weight:800;padding:.35rem .75rem;white-space:nowrap;">{html.escape(tipo_label(contribuicao))}</em></div>'
            f'<span style="color:#6d6380;margin:0;font-size:.82rem;">Para a história</span><h3 style="color:#21104a;margin:.05rem 0 .35rem;font-size:1.18rem;">{html.escape(titulo)}</h3>'
            f'<div class="ae-contrib-message" style="border:1px solid rgba(218,167,66,.35);border-radius:12px;padding:.7rem .85rem;background:rgba(255,250,241,.75);margin-bottom:.5rem;"><strong style="color:#21104a;">Eu lembro desse dia</strong><p style="color:#3b3150;margin:.25rem 0 0;line-height:1.45;">{html.escape(texto)}</p></div>'
            f'<small style="color:#6d6380;margin:0;font-size:.82rem;">Mídias enviadas</small><div class="ae-contrib-media-row" style="display:flex;gap:.5rem;margin-top:.35rem;">{media_chips}</div></div></div>',
            unsafe_allow_html=True,
        )
        col_ver, col_space, col_rejeitar, col_aprovar = st.columns([0.18, 0.46, 0.18, 0.18])
        with col_ver:
            st.button("Ver história", key=f"ver_historia_contribuicao_{contribuicao['id']}", use_container_width=True)
        with col_rejeitar:
            if st.button("Rejeitar", key=f"rejeitar_contribuicao_{contribuicao['id']}", use_container_width=True):
                try:
                    rejeitado = db.avaliar_contribuicao(contribuicao["id"], usuario_dono_id, "rejeitado")
                except Exception as exc:
                    print("Erro ao rejeitar contribuição:", exc)
                    st.error("Não foi possível rejeitar esta contribuição agora.")
                else:
                    st.success("Contribuição rejeitada.") if rejeitado else st.warning("Esta contribuição não está mais pendente.")
                    st.rerun()
        with col_aprovar:
            if st.button("Aprovar", key=f"aprovar_contribuicao_{contribuicao['id']}", type="primary", use_container_width=True):
                try:
                    aprovado = db.avaliar_contribuicao(contribuicao["id"], usuario_dono_id, "aprovado")
                except Exception as exc:
                    print("Erro ao aprovar contribuição:", exc)
                    st.error("Não foi possível aprovar esta contribuição agora.")
                else:
                    st.success("Contribuição aprovada.") if aprovado else st.warning("Esta contribuição não está mais pendente.")
                    st.rerun()

    st.markdown('<h2 class="ae-contrib-approved-title" style="color:#21104a;font-size:1.45rem;margin:1rem 0 .45rem;font-weight:900;">Aprovadas recentemente</h2>', unsafe_allow_html=True)
    aprovadas_html = ""
    for c in aprovadas[:3]:
        aprovadas_html += (
            f'<div class="ae-contrib-approved-card" style="{CARD}display:grid;grid-template-columns:48px 1fr auto;align-items:center;gap:.8rem;padding:.75rem;">'
            f'<div style="width:48px;height:48px;border-radius:999px;display:grid;place-items:center;color:#21104a;background:linear-gradient(135deg,#efe6dc,#d7c9ec);font-weight:900;">{html.escape(iniciais(c.get("contribuidor_nome")))}</div>'
            f'<p style="margin:0;color:#6d6380;line-height:1.25;"><strong style="color:#21104a;display:block;">{html.escape(c.get("contribuidor_nome") or "Pessoa convidada")}</strong>{html.escape(c.get("memoria_titulo") or "História sem título")}</p>'
            '<span style="background:rgba(222,247,229,.9);color:#167044;border:1px solid rgba(72,163,109,.3);border-radius:9px;padding:.45rem .75rem;font-weight:800;">Aprovada</span></div>'
        )
    if not aprovadas_html:
        aprovadas_html = '<div class="ae-contrib-empty-small" style="border:1px dashed rgba(104,79,176,.28);background:rgba(255,255,255,.55);border-radius:14px;color:#6d6380;padding:1rem;">Nenhuma contribuição aprovada recentemente.</div>'
    st.markdown(f'<div class="ae-contrib-approved-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.85rem;margin-bottom:.75rem;">{aprovadas_html}</div>', unsafe_allow_html=True)


def navegar_para(pagina: str):
    st.session_state.pagina_atual = pagina
    if pagina == "pessoas":
        st.session_state.pop("abrir_form_contato", None)
        st.session_state.pop("contato_prefill_nome", None)
        st.session_state.pop("contato_prefill_sobrenome", None)
        st.session_state.pop("contato_prefill_normalizado", None)
        st.session_state.pop("contato_prefill_origem", None)
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
        _botao_sidebar("🤍 Memorial", "memorial_lista")
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

        # ── PLAN_STATUS_CARD ─────────────────────────────────────────────
        _psc_qtd_memorias = st.session_state.get("_ae_qtd_memorias", 0)
        _psc_qtd_cofre    = st.session_state.get("_ae_qtd_cofre",    0)
        _psc_qtd_contatos = st.session_state.get("_ae_qtd_contatos", 0)
        
        _psc_nome_plano = "Gratuito"
        _psc_lim_memorias = 10
        _psc_lim_medias   = 20
        _psc_lim_contribs = 5
        try:
            plano_db = db.obter_plano_usuario(st.session_state.usuario_atual['id'])
            if plano_db:
                _psc_nome_plano = plano_db.get("nome", "Gratuito")
                if _psc_nome_plano != "Gratuito":
                    _psc_lim_memorias = 1000
                    _psc_lim_medias = plano_db.get("max_videos_total", 100) or 100
                    _psc_lim_contribs = plano_db.get("max_contatos", 50) or 50
        except Exception as exc:
            print("Erro ao obter limites do plano para a sidebar:", exc)

        _psc_mem_pct     = min(100, int(_psc_qtd_memorias / _psc_lim_memorias * 100)) if _psc_lim_memorias > 0 else 0
        _psc_media_pct   = min(100, int(_psc_qtd_cofre    / _psc_lim_medias   * 100)) if _psc_lim_medias   > 0 else 0
        _psc_contrib_pct = min(100, int(_psc_qtd_contatos / _psc_lim_contribs * 100)) if _psc_lim_contribs > 0 else 0
        _psc_mem_danger     = " ae-psc-bar-danger" if _psc_mem_pct     >= 90 else ""
        _psc_media_danger   = " ae-psc-bar-danger" if _psc_media_pct   >= 90 else ""
        _psc_contrib_danger = " ae-psc-bar-danger" if _psc_contrib_pct >= 90 else ""
        st.markdown("""<style>
.ae-psc {
    background:
        radial-gradient(circle at 88% 12%, rgba(242,197,114,0.16), transparent 34%),
        linear-gradient(180deg, rgba(255,255,255,0.085), rgba(255,255,255,0.045)) !important;
    border: 1px solid rgba(212,175,55,0.42) !important;
    border-radius: 16px !important;
    padding: 11px 11px 9px !important;
    margin: 4px 0 2px 0 !important;
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box !important;
    box-shadow: 0 12px 28px rgba(0,0,0,0.18) !important;
}
.ae-psc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 6px;
}
.ae-psc-label {
    color: #FFFFFF !important;
    font-size: 10px !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    line-height: 1.15;
}
.ae-psc-badge {
    background: rgba(242,197,114,0.16) !important;
    color: #F2C572 !important;
    border: 1px solid rgba(242,197,114,0.42) !important;
    font-size: 8px !important;
    font-weight: 900 !important;
    padding: 2px 6px !important;
    border-radius: 999px !important;
    white-space: nowrap;
}
.ae-psc-limit-note {
    background: rgba(242,197,114,0.10) !important;
    border: 1px solid rgba(242,197,114,0.26) !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,0.86) !important;
    font-size: 9px !important;
    line-height: 1.30 !important;
    padding: 5px 7px !important;
    margin: 0 0 6px 0 !important;
}
.ae-psc-limit-note strong { color: #F2C572 !important; }
.ae-psc-metric { margin-bottom: 6px !important; }
.ae-psc-metric:last-child { margin-bottom: 0 !important; }
.ae-psc-metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
}
.ae-psc-metric-name {
    color: rgba(255,255,255,0.78) !important;
    font-size: 10px !important;
    font-weight: 800 !important;
}
.ae-psc-metric-count {
    color: #FFFFFF !important;
    font-size: 9px !important;
    font-weight: 900 !important;
}
.ae-psc-bar-track {
    height: 3px !important;
    background: rgba(255,255,255,0.16) !important;
    border-radius: 999px !important;
    overflow: hidden !important;
}
.ae-psc-bar-fill {
    height: 100% !important;
    background: linear-gradient(90deg, #F8DC92, #D4AF37, #B77A46) !important;
    border-radius: 999px !important;
}
.ae-psc-bar-danger { background: linear-gradient(90deg, #f2c572, #e05858) !important; }
.ae-psc-divider {
    border: none !important;
    border-top: 1px solid rgba(212,175,55,0.22) !important;
    margin: 8px 0 6px 0 !important;
}
section[data-testid="stSidebar"] .ae-psc-btn-wrap {
    margin: 0 0 4px 0 !important;
}
[data-testid="stSidebar"] div[class*="st-key-psc_conhecer_premium"] button,
[data-testid="stSidebar"] div[class*="psc_conhecer_premium"] button,
[data-testid="stSidebar"] button[key="psc_conhecer_premium"],
div[class*="st-key-psc_conhecer_premium"] button {
    background: linear-gradient(135deg, #F8DC92 0%, #D4AF37 58%, #B77A46 100%) !important;
    color: #1B0F2E !important;
    border: 0 !important;
    border-radius: 12px !important;
    font-size: 11px !important;
    font-weight: 950 !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 32px !important;
    width: 100% !important;
    padding: 0 8px !important;
    box-shadow: 0 8px 18px rgba(212,175,55,0.20) !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] div[class*="st-key-psc_conhecer_premium"] button:hover,
[data-testid="stSidebar"] div[class*="psc_conhecer_premium"] button:hover,
[data-testid="stSidebar"] button[key="psc_conhecer_premium"]:hover,
div[class*="st-key-psc_conhecer_premium"] button:hover {
    background: linear-gradient(135deg, #FFF0BF 0%, #F2C572 42%, #D4AF37 100%) !important;
    color: #1B0F2E !important;
    border: 0 !important;
}
</style>
""", unsafe_allow_html=True)
        if _psc_nome_plano != "Gratuito":
            _psc_cta_texto = "Gerenciar plano"
            _psc_nota = "Você possui acesso total aos recursos da plataforma aEterna."
        else:
            _psc_acima_limite = _psc_qtd_memorias >= _psc_lim_memorias
            _psc_cta_texto = "Atualizar plano" if _psc_acima_limite else "Ver planos Premium"
            _psc_nota = (
                "<strong>Limite atingido.</strong> Atualize para continuar preservando novas memórias."
                if _psc_acima_limite
                else "Planos pagos liberam mais memórias, mídias e contribuições."
            )
        st.markdown(f"""<div class="ae-psc"><div class="ae-psc-header"><span class="ae-psc-label">Seu Plano</span><span class="ae-psc-badge">{_psc_nome_plano}</span></div><div class="ae-psc-limit-note">{_psc_nota}</div><div class="ae-psc-metric"><div class="ae-psc-metric-row"><span class="ae-psc-metric-name">Memórias</span><span class="ae-psc-metric-count">{_psc_qtd_memorias} / {_psc_lim_memorias}</span></div><div class="ae-psc-bar-track"><div class="ae-psc-bar-fill{_psc_mem_danger}" style="width:{_psc_mem_pct}%"></div></div></div><div class="ae-psc-metric"><div class="ae-psc-metric-row"><span class="ae-psc-metric-name">Fotos e vídeos</span><span class="ae-psc-metric-count">{_psc_qtd_cofre} / {_psc_lim_medias}</span></div><div class="ae-psc-bar-track"><div class="ae-psc-bar-fill{_psc_media_danger}" style="width:{_psc_media_pct}%"></div></div></div><div class="ae-psc-metric"><div class="ae-psc-metric-row"><span class="ae-psc-metric-name">Contribuições</span><span class="ae-psc-metric-count">{_psc_qtd_contatos} / {_psc_lim_contribs}</span></div><div class="ae-psc-bar-track"><div class="ae-psc-bar-fill{_psc_contrib_danger}" style="width:{_psc_contrib_pct}%"></div></div></div><hr class="ae-psc-divider"/></div>""", unsafe_allow_html=True)
        st.markdown('<div class="ae-psc-btn-wrap">', unsafe_allow_html=True)
        if st.button(_psc_cta_texto, key="psc_conhecer_premium", use_container_width=True):
            navegar_para("planos")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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

    def card_historia_home(memoria: dict, idx: int = None, contexto: str = None) -> str:
        titulo = html.escape(memoria.get("titulo") or "História sem título")
        data = html.escape(str(memoria.get("data_evento") or ""))
        resumo = html.escape(resumo_curto(memoria.get("conteudo") or ""))
        data_html = f'<span class="ae-live-story-date">{data}</span>' if data else ""
        button_html = ""
        if idx is not None and contexto is not None:
            btn_key = f"{contexto}_{idx}_{memoria['id']}"
            button_html = f'<a href="?ler={btn_key}" class="ae-live-card-read-btn">📖 Ler história</a>'
        return (
            '<div class="ae-live-story-card">'
            f"{media_home_memoria(memoria)}"
            '<div class="ae-live-story-body">'
            f"<h3>{titulo}</h3>"
            f"{data_html}"
            f"<p>{resumo}</p>"
            "</div>"
            f"{button_html}"
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
        if st.button("+ Contar uma História", key="home_contar_historia", use_container_width=True):
            navegar_para("assistente")
            st.rerun()

    st.markdown('<div class="ae-live-home-rule"></div>', unsafe_allow_html=True)

    st.markdown('<div class="ae-live-section-title">Continue sua história</div>', unsafe_allow_html=True)
    if memorias:
        home_ler_param = st.query_params.get("ler", "")
        if home_ler_param and home_ler_param.startswith("home_"):
            parts = home_ler_param.split("_", 2)
            if len(parts) == 3:
                mem_id = parts[2]
                for m in memorias:
                    if str(m["id"]) == mem_id:
                        st.session_state[f"_show_{home_ler_param}"] = True
                        break
            st.query_params.clear()
        cards_home = []
        expanded_home_key = None
        expanded_home_mem = None
        for i, memoria in enumerate(memorias[:4]):
            key_contexto = f"home_{i}_{memoria['id']}"
            cards_home.append(card_historia_home(memoria, idx=i, contexto="home"))
            if st.session_state.get(f"_show_{key_contexto}", False):
                expanded_home_key = key_contexto
                expanded_home_mem = memoria
        st.markdown(
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.5rem;">'
            + "".join(f"<div>{c}</div>" for c in cards_home)
            + "</div>",
            unsafe_allow_html=True,
        )
        if expanded_home_mem and expanded_home_key:
            st.divider()
            if expanded_home_mem.get("data_evento"):
                st.markdown(f"**Data:** {expanded_home_mem['data_evento']}")
            if expanded_home_mem.get("local"):
                st.markdown(f"**Local:** {expanded_home_mem['local']}")
            if expanded_home_mem.get("pessoas_relacionadas"):
                st.markdown(f"**Pessoas:** {expanded_home_mem['pessoas_relacionadas']}")
            st.markdown(expanded_home_mem.get("conteudo", ""))
            close_key = f"_close_{expanded_home_key}"
            if st.button("✕ Fechar", key=close_key):
                st.session_state[f"_show_{expanded_home_key}"] = False
                st.rerun()
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


def render_explorar_historia_compartilhada(
        grupo: dict,
        memoria: dict,
        imagem_local_para_data_uri,
        data_curta,
):
    acesso = grupo.get("acesso") or {}
    memorias = grupo.get("memorias") or []
    nome_pessoa = acesso.get("nome_completo") or acesso.get("nome") or "Pessoa"
    memoria_id = memoria.get("id")
    titulo = memoria.get("titulo") or "História sem título"
    conteudo = memoria.get("conteudo") or "Esta história ainda não possui descrição registrada."
    data_evento = str(memoria.get("data_evento") or memoria.get("data_criacao") or "")[:10]
    local = memoria.get("local") or "Local não informado"
    categoria = memoria.get("categoria") or "História"
    pessoas_texto = memoria.get("pessoas_relacionadas") or ""
    pessoas = [p.strip() for p in re.split(r"[,;]", pessoas_texto) if p.strip()]
    if not pessoas and nome_pessoa:
        pessoas = [nome_pessoa]

    try:
        fotos_por_memoria = db.listar_fotos_por_memorias_usuario(acesso.get("usuario_id")) or {}
    except Exception as exc:
        print("Erro ao carregar fotos da história explorada:", exc)
        fotos_por_memoria = {}
    try:
        videos_por_memoria = db.listar_videos_por_memorias_usuario(acesso.get("usuario_id")) or {}
    except Exception as exc:
        print("Erro ao carregar vídeos da história explorada:", exc)
        videos_por_memoria = {}
    contribuicoes = carregar_contribuicoes_aprovadas_memorias(acesso.get("usuario_id")).get(memoria_id, [])

    fotos_memoria = fotos_por_memoria.get(memoria_id, [])
    videos_memoria = videos_por_memoria.get(memoria_id, [])
    capa = ""
    if fotos_memoria:
        capa = imagem_local_para_data_uri(fotos_memoria[0].get("caminho") or fotos_memoria[0].get("caminho_arquivo") or "")
    capa_html = f'<img src="{html.escape(capa, quote=True)}" alt="Imagem da história">' if capa else '<div>📖</div>'

    def texto_curto(valor: str, limite: int = 150) -> str:
        texto = re.sub(r"\s+", " ", str(valor or "")).strip()
        return texto if len(texto) <= limite else texto[:limite].rstrip() + "..."

    def story_thumb(mem: dict) -> str:
        fotos = fotos_por_memoria.get(mem.get("id"), [])
        if fotos:
            src = imagem_local_para_data_uri(fotos[0].get("caminho") or fotos[0].get("caminho_arquivo") or "")
            if src:
                return f'<img src="{html.escape(src, quote=True)}" alt="História relacionada">'
        return '<span>📖</span>'

    pessoas_norm = {normalizar_nome_pessoa(p) for p in pessoas if p}
    relacionadas = []
    for outra in memorias:
        if outra.get("id") == memoria_id:
            continue
        pontos = 0
        texto_outra = normalizar_nome_pessoa(" ".join([
            outra.get("titulo") or "",
            outra.get("conteudo") or "",
            outra.get("pessoas_relacionadas") or "",
        ]))
        if any(p and p in texto_outra for p in pessoas_norm):
            pontos += 5
        if outra.get("categoria") and outra.get("categoria") == memoria.get("categoria"):
            pontos += 3
        if outra.get("local") and memoria.get("local") and outra.get("local") == memoria.get("local"):
            pontos += 2
        if pontos:
            relacionadas.append((pontos, outra))
    relacionadas = [item[1] for item in sorted(relacionadas, key=lambda item: item[0], reverse=True)[:3]]

    if st.button("← Voltar para explorar", key="voltar_lista_explorar_compartilhada", use_container_width=False):
        st.session_state.pop("historia_compartilhada_explorada_id", None)
        st.rerun()

    header_cols = st.columns([0.74, 0.26], vertical_alignment="center")
    with header_cols[0]:
        st.markdown(
            f'<div class="ae-explore-title"><h1>{html.escape(titulo)}</h1><p>{html.escape(texto_curto(conteudo, 86))}</p></div>',
            unsafe_allow_html=True,
        )
    with header_cols[1]:
        st.markdown('<div class="ae-explore-open-full">↗ Abrir história completa</div>', unsafe_allow_html=True)

    main_cols = st.columns([0.72, 0.28], gap="medium")
    with main_cols[0]:
        st.markdown(
            '<div class="ae-explore-main-card">'
            f'<div class="ae-explore-meta"><span>🗓️ {html.escape(data_evento or "Data não informada")}</span><span>📍 {html.escape(local)}</span></div>'
            f'<div class="ae-explore-story-grid"><div class="ae-explore-cover">{capa_html}</div>'
            f'<div class="ae-explore-story-text"><p>{html.escape(conteudo)}</p>'
            f'<blockquote>A vida é feita de escolhas e de amor.<br>Escolha sempre o que te aproxima de quem importa.</blockquote></div></div>'
            '<div class="ae-explore-sources">'
            f'<span>Fontes desta história:</span><b>{html.escape(categoria)}</b><b>{len(fotos_memoria)} fotos</b><b>{len(contribuicoes)} contribuições</b>'
            f'<em>Criada por: {html.escape(nome_pessoa)}</em><em>Última atualização: {html.escape(str(memoria.get("data_criacao") or "")[:10])}</em>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    with main_cols[1]:
        perguntas = [
            "Quem estava presente?",
            "Por que este momento foi importante?",
            f"Quais histórias envolvem {html.escape(pessoas[0]) if pessoas else 'esta pessoa'}?",
            "Existe outra memória parecida?",
        ]
        perguntas_html = "".join(f'<div class="ae-explore-question">💬 {pergunta}</div>' for pergunta in perguntas)
        resposta = (
            f"Nesta história aparecem {', '.join(pessoas[:4])}. "
            f"O contexto registrado indica: {texto_curto(conteudo, 120)}"
        )
        st.markdown(
            '<div class="ae-explore-side-card"><h3>Explorar esta história</h3>'
            '<p>Pergunte sobre o que já foi registrado. O explorador não inventa fatos.</p>'
            f'{perguntas_html}'
            f'<div class="ae-explore-answer"><strong>Resposta baseada nas histórias</strong><p>{html.escape(resposta)}</p>'
            f'<b>Fontes usadas:</b><ul><li>{html.escape(titulo)}</li><li>{html.escape(categoria)}</li></ul></div></div>',
            unsafe_allow_html=True,
        )

    pessoas_cards = []
    for pessoa in pessoas[:4]:
        inicial = html.escape(pessoa[:1].upper())
        pessoas_cards.append(
            f'<div class="ae-explore-person"><div>{inicial}</div><strong>{html.escape(pessoa)}</strong><span>pessoa relacionada</span><button>Ver perfil</button></div>'
        )
    pessoas_cards.append(f'<div class="ae-explore-person is-more"><div>👥</div><strong>Ver todas as pessoas</strong><span>{len(pessoas)} pessoas</span></div>')
    st.markdown(
        '<div class="ae-explore-section"><h3>Pessoas relacionadas</h3>'
        f'<div class="ae-explore-people-grid">{"".join(pessoas_cards)}</div></div>',
        unsafe_allow_html=True,
    )

    lower_cols = st.columns([0.52, 0.48], gap="medium")
    with lower_cols[0]:
        itens = []
        if fotos_memoria:
            for foto in fotos_memoria[:2]:
                itens.append(("Foto da história", foto.get("titulo") or "Foto registrada", foto.get("descricao") or "Mídia vinculada a esta memória."))
        for contrib in contribuicoes[:3]:
            itens.append(("Contribuição", contrib.get("contribuidor_nome") or "Pessoa convidada", contrib.get("texto") or contrib.get("arquivo_nome") or "Contribuição registrada."))
        if not itens:
            itens.append(("Registro principal", data_evento or "Data não informada", texto_curto(conteudo, 120)))
        linhas = "".join(
            f'<div class="ae-explore-contrib"><span></span><strong>{html.escape(a)}</strong><p>{html.escape(texto_curto(b, 48))}</p><em>{html.escape(texto_curto(c, 90))}</em><button>Ver detalhes</button></div>'
            for a, b, c in itens[:3]
        )
        st.markdown(
            '<div class="ae-explore-section"><h3>Contribuições e momentos registrados</h3>'
            f'<div class="ae-explore-timeline">{linhas}</div></div>',
            unsafe_allow_html=True,
        )
    with lower_cols[1]:
        cards = []
        for rel in relacionadas:
            cards.append(
                f'<div class="ae-explore-related-card"><div class="ae-explore-related-cover">{story_thumb(rel)}</div>'
                f'<strong>{html.escape(rel.get("titulo") or "História sem título")}</strong>'
                f'<span>{html.escape(rel.get("categoria") or "mesma história")}</span>'
                f'<em>{html.escape(str(rel.get("data_evento") or rel.get("data_criacao") or "")[:10])}</em></div>'
            )
        if not cards:
            cards.append('<div class="ae-explore-related-empty">Nenhuma história relacionada encontrada.</div>')
        st.markdown(
            '<div class="ae-explore-section"><div class="ae-explore-section-head"><h3>Histórias relacionadas</h3><span>Ver todas</span></div>'
            f'<div class="ae-explore-related-grid">{"".join(cards)}</div></div>',
            unsafe_allow_html=True,
        )


def render_historias_compartilhadas_lista(historias_compartilhadas: list):
    st.markdown(
        """
        <div class="ae-shared-hero">
            <div>
                <h1>🤝 Compartilhadas Comigo</h1>
                <p>Histórias que pessoas importantes decidiram compartilhar com você.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not historias_compartilhadas:
        st.markdown(
            """
            <div class="ae-shared-empty">
                <strong>Nenhuma história foi compartilhada com você ainda.</strong>
                <span>Quando uma pessoa importante liberar histórias para você, elas aparecerão aqui.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    def data_curta(valor) -> str:
        if not valor:
            return "Atualizada recentemente"
        texto = str(valor)
        if " " in texto:
            texto = texto.split(" ", 1)[0]
        return f"Atualizada em {texto[:10]}"

    def inicial_nome(nome: str) -> str:
        partes = [parte for parte in str(nome or "Pessoa").split() if parte]
        if len(partes) >= 2:
            return (partes[0][:1] + partes[-1][:1]).upper()
        return (partes[0][:2] if partes else "P").upper()

    def imagem_local_para_data_uri(caminho: str) -> str:
        try:
            if not caminho:
                return ""
            if caminho.startswith(("http://", "https://")):
                return caminho
            if not os.path.exists(caminho):
                return ""
            mime_type = mimetypes.guess_type(caminho)[0] or "image/jpeg"
            with open(caminho, "rb") as arquivo:
                encoded = base64.b64encode(arquivo.read()).decode("ascii")
            return f"data:{mime_type};base64,{encoded}"
        except Exception as exc:
            print("Erro ao preparar imagem compartilhada:", exc)
            return ""

    grupos = []
    for acesso in historias_compartilhadas:
        memorias = db.listar_memorias_por_contato(acesso.get("contato_id"))
        fotos = db.listar_fotos_por_contato(acesso.get("contato_id"))
        videos = db.listar_videos_por_contato(acesso.get("contato_id"))
        grupos.append({
            "acesso": acesso,
            "memorias": memorias,
            "fotos": fotos,
            "videos": videos,
            "total": len(memorias),
        })

    historia_explorada_id = st.session_state.get("historia_compartilhada_explorada_id")
    if historia_explorada_id:
        for grupo in grupos:
            memoria_encontrada = next(
                (memoria for memoria in grupo["memorias"] if str(memoria.get("id")) == str(historia_explorada_id)),
                None,
            )
            if memoria_encontrada:
                render_explorar_historia_compartilhada(grupo, memoria_encontrada, imagem_local_para_data_uri, data_curta)
                return
        st.session_state.pop("historia_compartilhada_explorada_id", None)

    filtro_usuario_id = st.session_state.get("compartilhadas_filtro_usuario_id")
    grupos_filtrados = [
        grupo for grupo in grupos
        if not filtro_usuario_id or grupo["acesso"].get("usuario_id") == filtro_usuario_id
    ]

    header_col, news_col = st.columns([0.62, 0.38], gap="large")

    with header_col:
        with st.container(key="ae_shared_people_panel"):
            st.markdown("<h3>Pessoas que compartilham comigo</h3>", unsafe_allow_html=True)
            pessoa_cols = st.columns([1, 1, 1, 1, 1, 0.34], gap="small")
            for indice, grupo in enumerate(grupos[:5]):
                acesso = grupo["acesso"]
                nome = acesso.get("nome_completo") or acesso.get("nome") or "Pessoa"
                total = grupo["total"]
                selecionada = acesso.get("usuario_id") == filtro_usuario_id
                with pessoa_cols[indice]:
                    st.markdown(
                        f"""
                        <div class="ae-shared-person-pill {'is-active' if selecionada else ''}">
                            <div class="ae-shared-person-avatar">{html.escape(inicial_nome(nome))}</div>
                            <strong>{html.escape(nome.split()[0] if nome else 'Pessoa')}</strong>
                            <span>{total} {'história' if total == 1 else 'histórias'}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "Selecionar",
                        key=f"filtrar_compartilhada_{acesso.get('usuario_id')}",
                        use_container_width=True,
                    ):
                        st.session_state.compartilhadas_filtro_usuario_id = acesso.get("usuario_id")
                        st.rerun()
            with pessoa_cols[-1]:
                if filtro_usuario_id:
                    if st.button("Todas", key="limpar_filtro_compartilhadas", use_container_width=True):
                        st.session_state.pop("compartilhadas_filtro_usuario_id", None)
                        st.rerun()

    with news_col:
        itens_novidade = []
        for grupo in grupos:
            acesso = grupo["acesso"]
            nome = acesso.get("nome_completo") or acesso.get("nome") or "Pessoa"
            novidades = acesso.get("novidades") or {}
            resumo = resumo_novidades(novidades)
            if resumo and resumo != "Tudo visto":
                itens_novidade.append((nome, resumo))
        if not itens_novidade:
            itens_novidade = [
                (
                    grupo["acesso"].get("nome_completo") or grupo["acesso"].get("nome") or "Pessoa",
                    f"{grupo['total']} histórias disponíveis",
                )
                for grupo in grupos[:4]
            ]
        novidades_html = "".join(
            f"""
            <div class="ae-shared-news-item">
                <div class="ae-shared-news-icon">📖</div>
                <p><strong>{html.escape(nome)}</strong> · {html.escape(texto)}</p>
            </div>
            """
            for nome, texto in itens_novidade[:4]
        )
        st.markdown(
            f"""
            <div class="ae-shared-news-panel">
                <h3>Novidades nas histórias compartilhadas</h3>
                {novidades_html}
                <strong>Ver todas as novidades ›</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if filtro_usuario_id:
        st.markdown(
            '<div class="ae-shared-filter-note">Filtro ativo. Mostrando histórias da pessoa selecionada.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<h2 class="ae-shared-section-title">Histórias compartilhadas por essas pessoas</h2>',
        unsafe_allow_html=True,
    )

    for grupo in grupos_filtrados:
        acesso = grupo["acesso"]
        memorias = grupo["memorias"]
        fotos = grupo["fotos"]
        nome = acesso.get("nome_completo") or acesso.get("nome") or "Pessoa"
        total_historias = grupo["total"]
        desde = "data não informada"
        if memorias:
            desde = str(memorias[-1].get("data_criacao") or "")[:10] or desde

        row_cols = st.columns([0.27, 0.52, 0.21], gap="small")
        with row_cols[0]:
            st.markdown(
                f"""
                <div class="ae-shared-owner">
                    <div class="ae-shared-owner-avatar">{html.escape(inicial_nome(nome))}</div>
                    <div>
                        <h3>{html.escape(nome)}</h3>
                        <p>Compartilha com você desde {html.escape(desde)}</p>
                        <span>👥 {total_historias} {'história' if total_historias == 1 else 'histórias'}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with row_cols[1]:
            story_cols = st.columns(3, gap="small")
            for indice in range(3):
                memoria = memorias[indice] if indice < len(memorias) else None
                with story_cols[indice]:
                    if memoria:
                        foto = fotos[indice] if indice < len(fotos) else None
                        img_src = imagem_local_para_data_uri((foto or {}).get("caminho") or (foto or {}).get("caminho_arquivo") or "")
                        media_html = (
                            f'<img src="{html.escape(img_src, quote=True)}" alt="Capa da história">'
                            if img_src
                            else '<span>📖</span>'
                        )
                        st.markdown(
                            f'<div class="ae-shared-story-mini"><div class="ae-shared-story-cover">{media_html}</div>'
                            f'<strong>{html.escape(memoria.get("titulo") or "História sem título")}</strong>'
                            f'<span>{html.escape(data_curta(memoria.get("data_criacao")))}</span></div>',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            "Explorar",
                            key=f"explorar_memoria_compartilhada_{acesso.get('usuario_id')}_{memoria.get('id')}",
                            use_container_width=True,
                        ):
                            st.session_state.historia_compartilhada_explorada_id = memoria.get("id")
                            st.rerun()
                    else:
                        st.markdown(
                            """
                            <div class="ae-shared-story-mini is-empty">
                                <div class="ae-shared-story-cover"><span>📖</span></div>
                                <strong>Próxima história</strong>
                                <span>Aguardando compartilhamento</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        with row_cols[2]:
            st.markdown(
                f"""
                <div class="ae-shared-open-card">
                    <div>📖</div>
                    <strong>Ver todas as {total_historias} histórias de {html.escape(nome.split()[0] if nome else 'Pessoa')}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Explorar história",
                key=f"abrir_historia_compartilhada_{acesso['usuario_id']}",
                use_container_width=True,
            ):
                selecionar_historia_compartilhada(acesso)
                st.session_state.pagina_atual = "historias_compartilhadas"
                st.rerun()


def render_novidades(
        historias_compartilhadas: list,
        contribuicoes_pendentes: int,
):
    st.markdown(
        """
        <div class="ae-news-hero">
            <div>
                <h1>🔔 Novidades</h1>
                <p>Acompanhe tudo o que aconteceu nas histórias que importam para você.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filtro = st.session_state.get("novidades_filtro", "todas")
    filtro_cols = st.columns([0.9, 1.35, 1.65, 1.25, 4], gap="small")
    for indice, (chave, rotulo) in enumerate([
        ("todas", "▦ Todas"),
        ("minhas", "📖 Minhas histórias"),
        ("compartilhadas", "♡ Compartilhadas comigo"),
        ("contribuicoes", "☆ Contribuições"),
    ]):
        with filtro_cols[indice]:
            if st.button(
                rotulo,
                key=f"novidades_filtro_{chave}",
                type="primary" if filtro == chave else "secondary",
                use_container_width=True,
            ):
                st.session_state.novidades_filtro = chave
                st.rerun()

    def inicial_nome(nome: str) -> str:
        partes = [parte for parte in str(nome or "Pessoa").split() if parte]
        if len(partes) >= 2:
            return (partes[0][:1] + partes[-1][:1]).upper()
        return (partes[0][:2] if partes else "P").upper()

    def imagem_src(caminho: str) -> str:
        try:
            if not caminho:
                return ""
            if caminho.startswith(("http://", "https://")):
                return caminho
            if not os.path.exists(caminho):
                return ""
            mime_type = mimetypes.guess_type(caminho)[0] or "image/jpeg"
            with open(caminho, "rb") as arquivo:
                encoded = base64.b64encode(arquivo.read()).decode("ascii")
            return f"data:{mime_type};base64,{encoded}"
        except Exception as exc:
            print("Erro ao preparar imagem de novidade:", exc)
            return ""

    def texto_relativo(valor) -> str:
        if not valor:
            return "recentemente"
        try:
            data = datetime.fromisoformat(str(valor).replace("Z", "+00:00")) if isinstance(valor, str) else valor
            agora = datetime.now(data.tzinfo) if getattr(data, "tzinfo", None) else datetime.now()
            delta = agora - data
            if delta.days <= 0:
                horas = max(1, int(delta.total_seconds() // 3600))
                return f"há {horas} hora" if horas == 1 else f"há {horas} horas"
            return "há 1 dia" if delta.days == 1 else f"há {delta.days} dias"
        except Exception:
            return str(valor)[:10]

    def grupo_data(valor) -> str:
        try:
            data = datetime.fromisoformat(str(valor).replace("Z", "+00:00")) if isinstance(valor, str) else valor
            hoje = (datetime.now(data.tzinfo).date() if getattr(data, "tzinfo", None) else datetime.now().date())
            dias = (hoje - data.date()).days
            if dias <= 0:
                return "Hoje"
            if dias == 1:
                return "Ontem"
            if dias <= 7:
                return "Esta semana"
            return "Semana passada"
        except Exception:
            return "Recentes"

    eventos = []
    totais = {"historias": 0, "lembrancas": 0, "comentarios": 0, "convites": int(contribuicoes_pendentes or 0), "mencoes": 0}
    atividades_por_pessoa = {}
    destaques = []

    for historia in historias_compartilhadas:
        nome = historia.get("nome_completo") or historia.get("nome") or "Pessoa"
        novidades = historia.get("novidades") or {}
        total = int(novidades.get("total", 0) or 0)
        if not total:
            continue
        memorias = db.listar_memorias_por_contato(historia.get("contato_id"))
        fotos = db.listar_fotos_por_contato(historia.get("contato_id"))
        memoria = memorias[0] if memorias else {}
        titulo = memoria.get("titulo") or "história compartilhada"
        data_evento = memoria.get("data_criacao")
        fotos_count = int(novidades.get("fotos", 0) or 0)
        texto = (
            f"{nome} adicionou {fotos_count} {'nova foto' if fotos_count == 1 else 'novas fotos'} em"
            if fotos_count
            else f"{nome} compartilhou uma nova história"
        )
        eventos.append({
            "tipo": "foto" if fotos_count else "historia",
            "origem": "compartilhadas",
            "pessoa": nome,
            "titulo": titulo,
            "texto": texto,
            "tempo": texto_relativo(data_evento),
            "grupo": grupo_data(data_evento),
            "data": data_evento or datetime.now(),
            "trecho": memoria.get("conteudo") or "",
            "fotos": fotos[:4],
            "historia": historia,
        })
        totais["historias"] += total
        totais["lembrancas"] += int(novidades.get("memorias", 0) or 0)
        atividades_por_pessoa[nome] = atividades_por_pessoa.get(nome, 0) + total
        if memoria:
            destaques.append({"titulo": titulo, "motivo": "Atualizada hoje", "foto": fotos[0] if fotos else {}})

    try:
        contribuicoes = db.listar_contribuicoes_pendentes(st.session_state.usuario_atual["id"])
    except Exception as exc:
        print("Erro ao listar contribuições para novidades:", exc)
        contribuicoes = []

    for contribuicao in contribuicoes:
        nome = contribuicao.get("contribuidor_nome") or "Pessoa convidada"
        titulo = contribuicao.get("memoria_titulo") or "história"
        criado_em = contribuicao.get("criado_em")
        eventos.append({
            "tipo": "convite",
            "origem": "contribuicoes",
            "pessoa": nome,
            "titulo": titulo,
            "texto": f"{nome} enviou uma contribuição em",
            "tempo": texto_relativo(criado_em),
            "grupo": grupo_data(criado_em),
            "data": criado_em or datetime.now(),
            "trecho": contribuicao.get("texto") or "Contribuição aguardando aprovação.",
            "fotos": [],
            "contribuicao": contribuicao,
        })
        atividades_por_pessoa[nome] = atividades_por_pessoa.get(nome, 0) + 1

    if filtro == "compartilhadas":
        eventos = [evento for evento in eventos if evento["origem"] == "compartilhadas"]
    elif filtro == "contribuicoes":
        eventos = [evento for evento in eventos if evento["origem"] == "contribuicoes"]
    elif filtro == "minhas":
        eventos = []

    eventos.sort(key=lambda item: str(item.get("data") or ""), reverse=True)
    main_col, side_col = st.columns([0.68, 0.32], gap="large")

    with main_col:
        if not eventos:
            st.markdown(
                '<div class="ae-news-empty"><strong>Sem novidades por enquanto.</strong><span>Quando algo importante acontecer nas suas histórias, aparecerá aqui.</span></div>',
                unsafe_allow_html=True,
            )
        grupo_atual = None
        for indice, evento in enumerate(eventos[:12]):
            if evento["grupo"] != grupo_atual:
                grupo_atual = evento["grupo"]
                st.markdown(f'<h3 class="ae-news-date">{html.escape(grupo_atual)}</h3>', unsafe_allow_html=True)
            fotos_html = ""
            for foto in evento.get("fotos", [])[:3]:
                src = imagem_src(foto.get("caminho") or foto.get("caminho_arquivo") or "")
                if src:
                    fotos_html += f'<img src="{html.escape(src, quote=True)}" alt="Miniatura">'
            if len(evento.get("fotos", [])) > 3:
                fotos_html += f'<span class="ae-news-more">+{len(evento.get("fotos", [])) - 3}</span>'
            midia_html = f'<div class="ae-news-media">{fotos_html}</div>' if fotos_html else ""
            trecho_html = f'<div class="ae-news-quote">{html.escape(evento.get("trecho") or "")[:160]}</div>' if evento.get("trecho") else ""
            icone = {"foto": "🖼️", "historia": "📖", "convite": "👥"}.get(evento["tipo"], "⭐")
            st.markdown(
                f"""
                <div class="ae-news-event">
                    <div class="ae-news-timeline-icon">{icone}</div>
                    <div class="ae-news-avatar">{html.escape(inicial_nome(evento['pessoa']))}</div>
                    <div class="ae-news-event-body">
                        <h3>{html.escape(evento['texto'])} <strong>“{html.escape(evento['titulo'])}”</strong></h3>
                        <span>{html.escape(evento['tempo'])}</span>
                        {trecho_html}
                        {midia_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if evento["origem"] == "compartilhadas":
                if st.button("Explorar história", key=f"news_open_shared_{indice}_{evento['historia']['usuario_id']}", use_container_width=False):
                    selecionar_historia_compartilhada(evento["historia"])
                    st.session_state.pagina_atual = "historias_compartilhadas"
                    st.rerun()
            elif evento["origem"] == "contribuicoes":
                if st.button("Avaliar contribuição", key=f"news_open_contrib_{evento['contribuicao']['id']}", use_container_width=False):
                    navegar_para("contribuicoes")
                    st.rerun()

        if len(eventos) > 12:
            st.button("Carregar mais novidades ↓", key="news_load_more", use_container_width=True)

    with side_col:
        resumo_html = "".join(
            f'<div class="ae-news-summary-row"><span>{icone}</span><p>{label}</p><strong>{valor}</strong></div>'
            for icone, label, valor in (
                ("🖼️", "Histórias atualizadas", totais["historias"]),
                ("✏️", "Lembranças escritas", totais["lembrancas"]),
                ("💬", "Comentários", totais["comentarios"]),
                ("👥", "Convites / Participações", totais["convites"]),
                ("⭐", "Menções", totais["mencoes"]),
            )
        )
        st.markdown(f'<div class="ae-news-side-card"><h3>Resumo rápido</h3>{resumo_html}</div>', unsafe_allow_html=True)

        ranking_html = "".join(
            f'<div class="ae-news-person-row"><div class="ae-news-person-avatar">{html.escape(inicial_nome(nome))}</div><div><strong>{html.escape(nome)}</strong><span>{total} atividades</span></div></div>'
            for nome, total in sorted(atividades_por_pessoa.items(), key=lambda item: item[1], reverse=True)[:5]
        ) or '<div class="ae-news-muted">Sem atividades por pessoa ainda.</div>'
        st.markdown(f'<div class="ae-news-side-card"><h3>Atividades por pessoa</h3>{ranking_html}<b>Ver todas as pessoas ›</b></div>', unsafe_allow_html=True)

        destaques_html = ""
        for destaque in destaques[:5]:
            src = imagem_src((destaque.get("foto") or {}).get("caminho") or (destaque.get("foto") or {}).get("caminho_arquivo") or "")
            thumb = f'<img src="{html.escape(src, quote=True)}" alt="Destaque">' if src else "<span>📖</span>"
            destaques_html += f'<div class="ae-news-highlight-row"><div>{thumb}</div><p><strong>{html.escape(destaque["titulo"])}</strong><span>{html.escape(destaque["motivo"])}</span></p></div>'
        destaques_html = destaques_html or '<div class="ae-news-muted">Sem histórias em destaque ainda.</div>'
        st.markdown(f'<div class="ae-news-side-card"><h3>Histórias em destaque</h3>{destaques_html}<b>Ver todas as histórias ›</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="ae-news-brand-card"><div>♡</div><p>“Cada novidade é um novo capítulo da nossa história juntos.”</p><strong>aEterna</strong></div>', unsafe_allow_html=True)


# ============================================================================
# MAIN
# ============================================================================
def main():
    # Clear Streamlit cache programmatically
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
    except Exception:
        pass
    
    # Cache buster to force Streamlit to bust cache and reload components
    print("RELOADING AETERNA CORE SYSTEM...")
    inject_custom_css()

    # Intercept Memorial Invitations
    convite_token = st.query_params.get("convite") or st.query_params.get("token")
    if convite_token:
        from components.memorial import render_aceite_convite
        render_aceite_convite(convite_token)
        return

    # Intercept Password Recovery redefinition link
    recuperar_param = st.query_params.get("recuperar")
    if recuperar_param:
        from components.login_compacto import render_redefinicao_senha
        render_redefinicao_senha(recuperar_param)
        return

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

        # Armazena métricas em session_state para uso em render_planos()
        st.session_state["_ae_qtd_memorias"] = qtd_memorias
        st.session_state["_ae_qtd_cofre"]    = qtd_cofre
        st.session_state["_ae_qtd_contatos"] = qtd_contatos
        st.session_state["_ae_qtd_videos"]   = qtd_videos

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
        elif pagina == "memorial_lista":
            render_memoriais_lista()
        elif pagina == "memorial_criar":
            render_criar_memorial()
        elif pagina.startswith("memorial_ver_"):
            memorial_id = int(pagina.split("_")[-1])
            render_pagina_memorial(memorial_id)
        elif pagina.startswith("memorial_curador_"):
            memorial_id = int(pagina.split("_")[-1])
            render_curador_perfil(memorial_id)
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
