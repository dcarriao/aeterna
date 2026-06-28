import html
import streamlit as st
import os
from datetime import datetime, date

from utils.assistente_ia import AssistenteLuto
from utils.banco import BancoDados
from utils.upload_video import GerenciadorVideos
from utils.storage import StorageAeterna
from utils.media import exibir_foto_segura

storage = StorageAeterna()


def _extrair_palavras_relevantes(texto: str):
    ignorar = {
        "como", "foi", "essa", "esse", "isso", "sobre", "para", "pela",
        "pelo", "dele", "dela", "nossa", "nosso", "minha", "meu",
        "quero", "saber", "falar", "conte", "mais", "uma", "uns", "das",
        "dos", "que", "com", "por"
    }

    palavras = []

    for palavra in texto.lower().replace("?", "").replace(",", "").split():
        if len(palavra) >= 4 and palavra not in ignorar:
            palavras.append(palavra)

    return palavras

def _safe_text(value: str) -> str:
    return html.escape(str(value or "")).replace("\n", "<br>")


def _curador_normalizar_data(valor: str) -> str | None:
    texto = str(valor or "").strip()
    if not texto:
        return None
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato).strftime("%Y-%m-%d")
        except Exception:
            continue
    return None


def _curador_preview_data(valor: str) -> str:
    texto = str(valor or "").strip()
    if not texto:
        return datetime.now().strftime("%d/%m/%Y") + " (aprox.)"
    data_normalizada = _curador_normalizar_data(texto)
    if data_normalizada:
        try:
            return datetime.strptime(data_normalizada, "%Y-%m-%d").strftime("%d/%m/%Y") + " (aprox.)"
        except Exception:
            return texto
    return texto


def _curador_trecho(texto: str, limite: int = 180) -> str:
    base = "Exemplo de como sua memória será exibida após salvar. Este é um trecho do texto que você escreveu."
    valor = " ".join(str(texto or "").split()).strip()
    if not valor:
        return base
    return valor if len(valor) <= limite else valor[:limite].rstrip() + "..."


def _curador_nome_arquivo(upload) -> str:
    return getattr(upload, "name", "") if upload else ""


def _render_curador_memoria_primeiro(db: BancoDados, usuario: dict, nome_referencia: str):
    st.markdown("""
    <style>
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 0.15rem !important;
        padding-bottom: 0.45rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 1460px !important;
        width: calc(100vw - 245px) !important;
        margin-left: 1.2rem !important;
        margin-right: 1rem !important;
    }
    .ae-curador-hero {
        margin-top: -0.35rem !important;
    }
    .ae-curador-hero h1 {
        margin-top: 0 !important;
    }
    .ae-curador-hero h1 {
        color: #21104a;
        font-size: 1.58rem;
        line-height: 1.02;
        margin: 0;
        font-weight: 900;
    }
    .ae-curador-hero p {
        color: #6d6380;
        margin: 0.12rem 0 0;
        font-size: 0.88rem;
    }
    .ae-curador-steps {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.45rem;
        margin: 0.55rem 0 0.65rem;
        padding: 0.24rem;
        border: 1px solid rgba(233, 222, 198, 0.95);
        border-radius: 16px;
        background: rgba(255,255,255,0.72);
    }
    .ae-curador-step {
        border-radius: 13px;
        min-height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        padding: 0.35rem 0.5rem;
        color: #47507a;
        font-weight: 700;
        text-align: center;
        font-size: 0.84rem;
    }
    .ae-curador-step.is-active {
        background: linear-gradient(180deg, rgba(255,250,241,.95), rgba(255,248,232,.92));
        border: 1px solid rgba(234, 181, 77, 0.55);
        color: #b36e16;
    }
    .ae-curador-preview-media {
        height: 96px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at top, rgba(255, 218, 153, .55), rgba(219, 205, 180, .28) 55%, rgba(250, 246, 239, .9));
        overflow: hidden;
        margin-bottom: 0.48rem;
        position: relative;
    }
    .ae-curador-preview-media .ae-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(43, 23, 71, 0.74);
        color: white;
        border-radius: 999px;
        padding: 0.2rem 0.48rem;
        font-size: 0.76rem;
        font-weight: 800;
    }
    .ae-curador-preview-media img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .ae-curador-hint {
        border-top: 1px solid rgba(233, 222, 198, 0.9);
        margin-top: 0.45rem;
        padding-top: 0.45rem;
        color: #6d6380;
        font-size: 0.79rem;
    }
    .ae-curador-tip {
        border: 1px solid rgba(233, 222, 198, 0.96);
        border-radius: 14px;
        padding: 0.5rem 0.62rem;
        color: #6d6380;
        background: rgba(255,255,255,.72);
        font-size: 0.81rem;
    }
    .ae-curador-how {
        margin-top: 0.58rem;
        background: rgba(255,255,255,.92);
        border: 1px solid rgba(233, 222, 198, 0.96);
        border-radius: 20px;
        box-shadow: 0 18px 40px rgba(64, 45, 19, 0.06);
        padding: 0.62rem 0.72rem;
    }
    .ae-curador-how h3 {
        color: #21104a;
        margin: 0 0 0.58rem;
        font-size: 0.92rem;
        font-weight: 900;
    }
    .ae-curador-how-grid {
        display: flex;
        align-items: flex-start;
        gap: 0;
    }
    .ae-curador-how-item {
        flex: 1;
        border: 1px solid rgba(233, 222, 198, 0.96);
        border-radius: 16px;
        background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(250,247,241,.96));
        padding: 0.55rem;
        min-height: 90px;
        font-size: 0.82rem;
        line-height: 1.36;
    }
    .ae-curador-how-item strong {
        display: block;
        color: #21104a;
        margin-bottom: 0.28rem;
    }
    .ae-curador-how-icon {
        font-size: 1.4rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .ae-curador-how-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 0.28rem;
        padding-top: 0.6rem;
        color: #b07a1d;
        font-size: 0.9rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    .ae-curador-question-shell {
        display: grid;
        gap: 0.4rem;
    }
    .ae-curador-question-pill {
        min-height: 2.06rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0.4rem 0.7rem;
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(249,245,255,.98), rgba(244,238,252,.98));
        color: #5c3d87;
        border: 1px solid rgba(193, 177, 231, 0.92);
        font-weight: 700;
        font-size: 0.84rem;
        line-height: 1.18;
    }
    .ae-curador-response {
        margin-top: 0.45rem;
        border: 1px solid rgba(192, 177, 230, 0.82);
        border-radius: 14px;
        background: linear-gradient(180deg, rgba(248,244,255,.98), rgba(241,236,252,.92));
        padding: 0.58rem;
    }
    .ae-curador-response strong {
        color: #21104a;
        display: block;
        margin-bottom: 0.24rem;
    }
    .st-key-curador_save_wrap button[kind="primary"],
    .st-key-curador_save_wrap button[kind="primary"]:hover,
    .st-key-curador_save_wrap button[kind="primary"]:focus,
    .st-key-curador_save_wrap button[kind="primary"]:active {
        background: linear-gradient(135deg, #d5a03c, #b77a46 72%, #8f5a35) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        min-height: 2.18rem !important;
    }
    [class*="st-key-curador_pergunta_pronta_"] button,
    [class*="st-key-curador_pergunta_pronta_"] button:hover,
    [class*="st-key-curador_pergunta_pronta_"] button:focus,
    [class*="st-key-curador_pergunta_pronta_"] button:active {
        background: linear-gradient(180deg, rgba(249,245,255,.98), rgba(244,238,252,.98)) !important;
        color: #5c3d87 !important;
        border: 1px solid rgba(193, 177, 231, 0.92) !important;
        box-shadow: none !important;
        min-height: 2.06rem !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        white-space: normal !important;
        line-height: 1.18 !important;
    }
    .st-key-curador_form_panel label,
    .st-key-curador_preview_panel label {
        color: #6d6380 !important;
        font-size: 0.83rem !important;
    }
    .st-key-curador_form_panel .stTextArea textarea {
        min-height: 128px !important;
    }
    .st-key-curador_form_panel [data-testid="stFileUploader"] section {
        min-height: 86px !important;
        padding-top: 0.35rem !important;
        padding-bottom: 0.3rem !important;
    }
    .st-key-curador_form_panel [data-testid="stFileUploader"] small {
        font-size: 0.74rem !important;
    }
    .st-key-curador_form_panel .stTextInput input,
    .st-key-curador_form_panel .stSelectbox select,
    .st-key-curador_form_panel .stMultiSelect,
    .st-key-curador_form_panel .stDateInput input {
        min-height: 2.35rem !important;
    }
    .st-key-curador_form_panel,
    .st-key-curador_preview_panel,
    .st-key-curador_explore_panel {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    .ae-curador-saved-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        background: rgba(242, 248, 232, 0.95);
        border: 1px solid rgba(72, 163, 109, 0.34);
        border-radius: 16px;
        padding: 0.72rem 0.9rem;
        margin: 0.5rem 0 0.7rem;
        color: #1f5b38;
        box-shadow: 0 10px 28px rgba(35, 88, 55, 0.06);
    }
    .ae-curador-saved-card strong {
        color: #1f5b38;
        display: block;
        margin-bottom: 0.1rem;
    }
    .ae-curador-saved-card span {
        color: #406b50;
        font-size: 0.84rem;
    }
    .st-key-curador_ver_historia_salva button {
        background: rgba(255,255,255,0.86) !important;
        color: #1f5b38 !important;
        border: 1px solid rgba(72,163,109,0.38) !important;
        border-radius: 10px !important;
        min-height: 2rem !important;
        font-weight: 900 !important;
    }
    @media (max-width: 900px) {
        .main .block-container,
        [data-testid="stMainBlockContainer"] {
            width: 100% !important;
            max-width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
        }
        .ae-curador-steps { grid-template-columns: 1fr 1fr; }
        .ae-curador-how-grid { display: grid; grid-template-columns: 1fr; gap: 0.5rem; }
        .ae-curador-how-arrow { display: none; }
        .ae-curador-saved-card { display: block; }
    }
    </style>
    """, unsafe_allow_html=True)

    usuario_id = usuario.get("id")
    contatos = []
    try:
        contatos = db.listar_contatos_usuario(usuario_id)
    except Exception as exc:
        print("Erro ao listar contatos do curador:", exc)

    nomes_contatos = [c.get("nome_completo") for c in contatos if c.get("nome_completo")]
    colecoes = [
        ("livre", "Selecione uma coleção"),
        ("familia", "Família"),
        ("viagens", "Viagens"),
        ("infancia", "Infância"),
        ("carreira", "Carreira"),
        ("valores", "Valores"),
        ("amor", "Amor"),
        ("conquista", "Conquistas"),
    ]
    mapa_colecoes = {valor: rotulo for valor, rotulo in colecoes}

    st.markdown(
        '<div class="ae-curador-hero">'
        '<h1>Curador de Histórias</h1>'
        '<p>Registre primeiro. O Curador ajuda depois.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="ae-curador-steps">'
        '<div class="ae-curador-step is-active">🖼️ 1. Adicionar mídia (opcional)</div>'
        '<div class="ae-curador-step">✏️ 2. Escrever contexto</div>'
        '<div class="ae-curador-step">✅ 3. Salvar memória</div>'
        '<div class="ae-curador-step">💬 4. Explorar com o Curador</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    memoria_salva_topo = st.session_state.get("curador_memoria_salva")
    if memoria_salva_topo:
        st.markdown(
            '<div class="ae-curador-saved-card">'
            '<div><strong>Memória salva.</strong><span>Escolha uma pergunta em “Aprofundar agora” ou abra a história na sua coleção.</span></div>'
            '</div>',
            unsafe_allow_html=True,
        )
        with st.container(key="curador_ver_historia_salva"):
            if st.button("Ver em Minha História", use_container_width=False):
                st.session_state.pagina_atual = "minha_historia"
                st.rerun()

    col_form, col_preview, col_explore = st.columns([1.25, 0.88, 0.72], gap="small")

    with col_form:
        st.markdown("### Nova memória")
        st.caption("Mídia (opcional)")
        media_cols = st.columns(2, gap="small")
        with media_cols[0]:
            foto_memoria = st.file_uploader(
                "Adicionar foto",
                type=["png", "jpg", "jpeg", "webp"],
                key="curador_memoria_foto",
                help="JPG, PNG até 10MB",
            )
        with media_cols[1]:
            video_memoria = st.file_uploader(
                "Adicionar vídeo",
                type=["mp4", "mov", "avi", "mkv"],
                key="curador_memoria_video",
                help="MP4 até 50MB",
            )

        titulo = st.text_input(
            "Título da memória",
            key="curador_memoria_titulo",
            placeholder="Dê um título para esta memória",
        )
        conteudo = st.text_area(
            "Conte esta história",
            key="curador_memoria_conteudo",
            height=128,
            placeholder="Escreva o que aconteceu, onde, com quem, detalhes marcantes...",
            max_chars=5000,
        )
        meta_col1, meta_col2 = st.columns(2, gap="small")
        with meta_col1:
            data_aproximada = st.date_input(
                "Data da memória",
                key="curador_memoria_data",
                value=None,
                format="DD/MM/YYYY",
            )
        with meta_col2:
            pessoas_relacionadas = st.multiselect(
                "Pessoas relacionadas (opcional)",
                options=nomes_contatos,
                key="curador_memoria_pessoas",
                placeholder="Digite nomes e selecione",
            )

        colecao_valor = st.selectbox(
            "Coleção (opcional)",
            options=[item[0] for item in colecoes],
            format_func=lambda valor: mapa_colecoes.get(valor, valor),
            key="curador_memoria_colecao",
        )

        rodape_col1, rodape_col2 = st.columns([0.65, 0.35], gap="small")
        with rodape_col1:
            st.markdown(
                "<div class='ae-curador-tip'><strong style='display:block;color:#b07a1d;margin-bottom:.2rem;'>Você pode salvar só com texto.</strong>Foto e vídeo são opcionais.</div>",
                unsafe_allow_html=True,
            )
        with rodape_col2:
            with st.container(key="curador_save_wrap"):
                salvar_memoria = st.button(
                    "Salvar memória",
                    key="curador_salvar_memoria_primeiro",
                    type="primary",
                    use_container_width=True,
                )

    preview_titulo = titulo.strip() or "Título da memória aparecerá aqui"
    preview_texto = _curador_trecho(conteudo)
    preview_data = _curador_preview_data(data_aproximada)
    preview_pessoas = ", ".join(pessoas_relacionadas) if pessoas_relacionadas else "Pessoas relacionadas"
    preview_colecao = mapa_colecoes.get(colecao_valor, "Coleção")
    media_total = int(bool(foto_memoria)) + int(bool(video_memoria))

    with col_preview:
        st.markdown("### Prévia da memória")
        if foto_memoria:
            st.image(foto_memoria, use_container_width=True)
        else:
            st.markdown(
                "<div class='ae-curador-preview-media'><div style='font-size:2.4rem;color:#a48b62;'>◌</div></div>",
                unsafe_allow_html=True,
            )
        st.markdown(
            f"<div style='display:flex;justify-content:flex-end;margin:.18rem 0 .08rem;'><span style='background:rgba(43,23,71,.74);color:white;border-radius:999px;padding:.16rem .44rem;font-size:.72rem;font-weight:800;'>{max(media_total, 1)}/3</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div style='color:#21104a;font-weight:900;font-size:.96rem;margin-bottom:.18rem;'>{html.escape(preview_titulo)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#6d6380;line-height:1.34;font-size:.83rem;'>{html.escape(preview_texto)}</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='ae-curador-hint'>"
            f"<div style='margin-bottom:.24rem;'>🗓️ {html.escape(preview_data)}</div>"
            f"<div style='margin-bottom:.24rem;'>👥 {html.escape(preview_pessoas)}</div>"
            f"<div>🗂️ {html.escape(preview_colecao)}</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='ae-curador-tip' style='margin-top:.42rem;'>A prévia é atualizada conforme você preenche os campos.</div>",
            unsafe_allow_html=True,
        )

    perguntas_curador = [
        ("👤", "Quem estava com você?"),
        ("⭐", "O que tornou esse momento especial?"),
        ("📷", "Existe outra foto desse dia?"),
        ("💜", "Como você se sentiu?"),
        ("🌱", "O que aprendeu nesse momento?"),
        ("🔗", "Há uma história relacionada?"),
    ]

    with col_explore:
        memoria_salva = st.session_state.get("curador_memoria_salva")
        st.markdown("### Aprofundar agora" if memoria_salva else "### Explorar depois de salvar")
        st.markdown(
            "<div style='color:#6d6380;line-height:1.36;font-size:.84rem;margin-bottom:.46rem;'>Depois de salvar sua memória, escolha uma pergunta para aprofundar a história.</div>" if memoria_salva else "<div style='color:#6d6380;line-height:1.36;font-size:.84rem;margin-bottom:.46rem;'>Depois de salvar sua memória, o Curador pode ajudar você a aprofundar e enriquecer os detalhes.</div>",
            unsafe_allow_html=True,
        )
        if not memoria_salva:
            st.markdown("<div class='ae-curador-question-shell'>", unsafe_allow_html=True)
            for icone, pergunta in perguntas_curador:
                st.markdown(
                    f"<div class='ae-curador-question-pill'>{icone} {html.escape(pergunta)}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            for indice, (icone, pergunta) in enumerate(perguntas_curador):
                if st.button(
                    f"{icone} {pergunta}",
                    key=f"curador_pergunta_pronta_{indice}",
                    use_container_width=True,
                ):
                    try:
                        contexto = (
                            f"Memória já registrada.\n"
                            f"Título: {memoria_salva.get('titulo') or ''}\n"
                            f"Texto: {memoria_salva.get('conteudo') or ''}\n"
                            f"Data: {memoria_salva.get('data_evento') or ''}\n"
                            f"Pessoas: {memoria_salva.get('pessoas_relacionadas') or ''}\n"
                            f"Categoria: {memoria_salva.get('categoria') or ''}\n"
                            f"Pergunta: {pergunta}\n"
                            "Responda em até 4 linhas, sem inventar fatos, com foco em aprofundar a memória."
                        )
                        resposta = st.session_state.assistente_obj.conversar(contexto)
                    except Exception as exc:
                        print("Erro ao explorar memória com o curador:", exc)
                        resposta = "Não foi possível gerar a sugestão agora. Tente novamente em alguns instantes."
                    st.session_state["curador_exploracao"] = {
                        "pergunta": pergunta,
                        "resposta": resposta,
                    }
                    st.rerun()
        exploracao = st.session_state.get("curador_exploracao")
        if exploracao:
            st.markdown(
                "<div class='ae-curador-response'>"
                f"<strong>{html.escape(exploracao.get('pergunta') or 'Resposta baseada na memória')}</strong>"
                f"<div style='color:#3b3150;line-height:1.42;font-size:.88rem;'>{_safe_text(exploracao.get('resposta') or '')}</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        st.markdown(
            "<div class='ae-curador-tip' style='margin-top:.52rem;'>O Curador não substitui a memória. Ele ajuda a aprofundar o que você registrou.</div>",
            unsafe_allow_html=True,
        )

    if salvar_memoria:
        if not conteudo.strip():
            st.warning("Escreva a história antes de salvar.")
        else:
            try:
                memoria_id = db.salvar_memoria(
                    usuario_id=usuario_id,
                    conteudo=conteudo.strip(),
                    titulo=titulo.strip(),
                    categoria=colecao_valor or "livre",
                    origem="curador",
                    data_evento=_curador_normalizar_data(data_aproximada),
                    pessoas_relacionadas=", ".join(pessoas_relacionadas) if pessoas_relacionadas else None,
                    visibilidade="contatos",
                    contatos_ids=[],
                )

                if foto_memoria:
                    upload_foto = storage.upload_streamlit_file(
                        bucket="fotos",
                        arquivo=foto_memoria,
                        usuario_id=usuario_id,
                        pasta="memorias",
                    )
                    foto_id = db.adicionar_foto_com_acesso(
                        usuario_id=usuario_id,
                        titulo=titulo.strip() or "Foto da memória",
                        descricao=conteudo.strip()[:300],
                        categoria=colecao_valor or "livre",
                        caminho_arquivo=upload_foto["url"],
                        contatos_ids=[],
                        visibilidade="contatos",
                    )
                    db.associar_foto_memoria(memoria_id=memoria_id, foto_id=foto_id)

                if video_memoria:
                    upload_video = storage.upload_streamlit_file(
                        bucket="videos",
                        arquivo=video_memoria,
                        usuario_id=usuario_id,
                        pasta="memorias",
                    )
                    video_id = db.adicionar_video_com_acesso(
                        usuario_id=usuario_id,
                        titulo=titulo.strip() or "Vídeo da memória",
                        destinatario=", ".join(pessoas_relacionadas),
                        caminho_arquivo=upload_video["url"],
                        contatos_ids=[],
                        categoria=colecao_valor or "livre",
                        visibilidade="contatos",
                    )
                    db.associar_video_memoria(memoria_id=memoria_id, video_id=video_id)

                st.session_state["curador_memoria_salva"] = {
                    "id": memoria_id,
                    "titulo": preview_titulo,
                    "conteudo": conteudo.strip(),
                    "data_evento": _curador_normalizar_data(data_aproximada) or data_aproximada,
                    "pessoas_relacionadas": ", ".join(pessoas_relacionadas),
                    "categoria": colecao_valor or "livre",
                }
                st.session_state.pop("curador_exploracao", None)
                st.rerun()
            except Exception as exc:
                print("Erro ao salvar memória no curador:", exc)
                st.error("Não foi possível salvar a memória agora. Tente novamente em alguns instantes.")

    st.markdown(
        "<div class='ae-curador-how'><h3>Como funciona</h3><div class='ae-curador-how-grid'>"
        "<div class='ae-curador-how-item'><span class='ae-curador-how-icon'>🖼️</span><strong>1. Registrar</strong>Adicione mídia (se tiver) e escreva o contexto da sua memória.</div>"
        "<div class='ae-curador-how-arrow'>→</div>"
        "<div class='ae-curador-how-item'><span class='ae-curador-how-icon'>☁️</span><strong>2. Salvar</strong>Salve sua memória com segurança. Você pode editar depois.</div>"
        "<div class='ae-curador-how-arrow'>→</div>"
        "<div class='ae-curador-how-item'><span class='ae-curador-how-icon'>💬</span><strong>3. Receber sugestões</strong>O Curador oferece perguntas que ajudam a trazer mais detalhes.</div>"
        "<div class='ae-curador-how-arrow'>→</div>"
        "<div class='ae-curador-how-item'><span class='ae-curador-how-icon'>💛</span><strong>4. Aprofundar a história</strong>Você decide o que responder e transforma lembranças em legado.</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )


def render_curador_memoria_primeiro():
    _inicializar_chat()
    db = BancoDados()
    usuario = st.session_state.get("usuario_atual") or {}
    nome_referencia = _obter_nome_referencia()
    _render_curador_memoria_primeiro(db, usuario, nome_referencia)


def render_chat_luto():
    _inicializar_chat()
    db = BancoDados()

    nome_referencia = _obter_nome_referencia()
    usuario = st.session_state.get("usuario_atual") or {}
    modo = "memorial" if usuario.get("tipo") == "visitante" else "legado"

    st.markdown("""
    <style>
    .ae-assistente-page h2,
    .ae-assistente-page p {
        color: #2b1747 !important;
    }

    .ae-simple-bubble-bot {
        background: #ffffff;
        color: #1b0f2e;
        padding: 14px 16px;
        border-radius: 18px;
        margin: 12px 0;
        max-width: 92%;
        border: 1px solid rgba(0,0,0,0.08);
        font-size: 0.95rem;
        line-height: 1.45;
    }

    .ae-simple-bubble-user {
        background: #2b1747;
        color: #ffffff;
        padding: 14px 16px;
        border-radius: 18px;
        margin: 12px 0 12px auto;
        max-width: 92%;
        font-size: 0.95rem;
        line-height: 1.45;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ae-assistente-page">', unsafe_allow_html=True)

    if modo == "memorial":
        nome_pessoa = usuario.get("nome_falecido", "esta pessoa")

        st.markdown("## 🔎 Explorar História")
        st.info(
            f"Explore histórias, memórias, fotos, vídeos "
            f"e aprendizados compartilhados por {nome_pessoa}. "
            "As respostas usam apenas informações registradas e autorizadas."
        )

        st.markdown("""
                    ### 💬 Por onde começar?

                    • Quais histórias {nome_pessoa} compartilhou comigo?
                    • Quais momentos importantes foram registrados?
                    • Quais fotos ou vídeos estão disponíveis?
                    • O que foi contado sobre família, viagens ou aprendizados?
                    • Existe alguma mensagem compartilhada comigo?
                    • Quais valores aparecem nessas histórias?
                    """.format(nome_pessoa=nome_pessoa))
        if not usuario.get("usuario_logado_compartilhado"):
            st.markdown("""
                        ---
                        ### ✨ Também quer preservar sua história?

                        Crie seu espaço na aEterna para registrar histórias, fotos, vídeos e momentos importantes da sua vida.
                        """)

            if st.button("✨ Criar minha história"):
                for key in [
                    "autenticado",
                    "usuario_atual",
                    "modo_acesso",
                    "falecido_id",
                    "historico_assistente",
                    "assistente_obj",
                    "assistente_modo",
                    "assistente_usuario_id",
                    "assistente_contato_id",
                ]:
                    if key in st.session_state:
                        del st.session_state[key]

                st.session_state.autenticado = False
                st.session_state.login_mode = "cadastro"
                st.rerun()
    else:
        _render_curador_memoria_primeiro(db, usuario, nome_referencia)
        return

    if st.session_state.get("ultimo_erro_openai"):
        st.error("Não foi possível continuar agora. Tente novamente em alguns instantes.")


    historico = st.session_state.get("historico_assistente", [])

    if not historico:
        historico = [{
            "tipo": "bot",
            "texto": (
                f"Olá. Este é um espaço para explorar histórias, valores, "
                f"aprendizados e momentos importantes de {nome_referencia}."
            )
        }]

    for i, msg in enumerate(historico):
        tipo = msg.get("tipo", "bot")
        texto_original = msg.get("texto", "")
        texto_html = html.escape(texto_original).replace("\n", "<br>")

        if tipo == "user":
            st.markdown(
                '<div class="ae-simple-bubble-user">{}</div>'.format(texto_html),
                unsafe_allow_html=True
            )

            if modo == "legado" and len(texto_original.strip()) > 20:
                chave_base = "memoria_{}_{}".format(i, abs(hash(texto_original)))

                if st.button(
                        "💾 Salvar como memória",
                        key="salvar_" + chave_base
                ):
                    sugestoes = st.session_state.assistente_obj.sugerir_metadados_memoria(
                        texto_original
                    )
                    st.session_state["sugestoes_" + chave_base] = sugestoes
                    st.session_state["texto_memoria_" + chave_base] = texto_original

                if "sugestoes_" + chave_base in st.session_state:
                    sugestoes = st.session_state["sugestoes_" + chave_base]

                    with st.form("form_" + chave_base):
                        st.markdown("#### 💡 Curador: organizar esta memória")

                        titulo = st.text_input(
                            "Título",
                            value=sugestoes.get("titulo", "")
                        )

                        categoria = st.text_input(
                            "Categoria",
                            value=sugestoes.get("categoria", "")
                        )

                        local = st.text_input(
                            "Local",
                            value=sugestoes.get("local", "")
                        )

                        data_evento = st.text_input(
                            "Data aproximada",
                            value=sugestoes.get("data_evento", ""),
                            placeholder="Ex: 2024-03-15, 2024, infância..."
                        )

                        pessoas_relacionadas = st.text_input(
                            "Pessoas relacionadas",
                            value=sugestoes.get("pessoas_relacionadas", "")
                        )

                        contatos = db.listar_contatos_usuario(
                            st.session_state.get("usuario_atual", {}).get("id")
                        )
                        visibilidade = st.radio(
                            "Quem pode ver esta memória?",
                            ["privado", "contatos", "seletivo"],
                            format_func=lambda valor: {
                                "privado": "🔒 Somente eu",
                                "contatos": "👥 Todos os meus contatos",
                                "seletivo": "✨ Escolher contatos específicos",
                            }[valor],
                            key="visibilidade_" + chave_base,
                        )
                        mapa_contatos = {
                            contato["nome_completo"]: contato["id"]
                            for contato in contatos
                        }
                        contatos_selecionados_nomes = (
                            st.multiselect(
                                "Contatos que poderão ver",
                                list(mapa_contatos.keys()),
                                key="contatos_" + chave_base,
                            )
                            if visibilidade == "seletivo"
                            else []
                        )
                        contatos_selecionados = [
                            mapa_contatos[nome]
                            for nome in contatos_selecionados_nomes
                        ]

                        foto_memoria = st.file_uploader(
                            "📷 Adicionar foto a esta memória (opcional)",
                            type=["png", "jpg", "jpeg", "webp"],
                            key="foto_" + chave_base
                        )

                        video_memoria = st.file_uploader(
                            "🎥 Adicionar vídeo a esta memória (opcional)",
                            type=["mp4", "mov", "avi", "mkv"],
                            key="video_" + chave_base
                        )

                        salvar_final = st.form_submit_button(
                            "✅ Salvar memória",
                            type="primary",
                            width="stretch"
                        )

                        if salvar_final:
                            usuario = st.session_state.get("usuario_atual")

                            if visibilidade == "seletivo" and not contatos_selecionados:
                                st.warning("Selecione pelo menos um contato.")
                                st.stop()

                            if data_evento:
                                try:
                                    datetime.strptime(data_evento, "%Y-%m-%d")
                                except:
                                    data_evento = None

                            memoria_id = db.salvar_memoria(
                                usuario_id=usuario["id"],
                                conteudo=st.session_state["texto_memoria_" + chave_base],
                                titulo=titulo or "",
                                categoria=categoria or "livre",
                                origem="curador",
                                local=local or None,
                                data_evento=data_evento or None,
                                pessoas_relacionadas=pessoas_relacionadas or None,
                                visibilidade=visibilidade,
                                contatos_ids=contatos_selecionados,
                            )

                            if foto_memoria:
                                upload = storage.upload_streamlit_file(
                                    bucket="fotos",
                                    arquivo=foto_memoria,
                                    usuario_id=usuario["id"],
                                    pasta="memorias"
                                )

                                caminho_foto = upload["url"]

                                foto_id = db.adicionar_foto_com_acesso(
                                    usuario_id=usuario["id"],
                                    titulo=titulo or "Foto da memória",
                                    descricao=st.session_state["texto_memoria_" + chave_base][:300],
                                    categoria=categoria or "livre",
                                    caminho_arquivo=caminho_foto,
                                    contatos_ids=contatos_selecionados,
                                    visibilidade=visibilidade,
                                )

                                db.associar_foto_memoria(
                                    memoria_id=memoria_id,
                                    foto_id=foto_id
                                )
                            if video_memoria:
                                upload = storage.upload_streamlit_file(
                                    bucket="videos",
                                    arquivo=video_memoria,
                                    usuario_id=usuario["id"],
                                    pasta="memorias"
                                )

                                caminho_video = upload["url"]

                                video_id = db.adicionar_video_com_acesso(
                                    usuario_id=usuario["id"],
                                    titulo=titulo or "Vídeo da memória",
                                    destinatario=pessoas_relacionadas or "",
                                    caminho_arquivo=caminho_video,
                                    contatos_ids=contatos_selecionados,
                                    categoria=categoria or "livre",
                                    visibilidade=visibilidade,
                                )

                                db.associar_video_memoria(
                                    memoria_id=memoria_id,
                                    video_id=video_id
                                )

                            del st.session_state["sugestoes_" + chave_base]
                            del st.session_state["texto_memoria_" + chave_base]

                            st.success("Memória salva na sua história.")
                            st.rerun()


        else:
            st.markdown(
                '<div class="ae-simple-bubble-bot">{}</div>'.format(texto_html),
                unsafe_allow_html=True
            )
            fotos = msg.get("fotos", [])

            if fotos:
                st.caption("📷 Fotos relacionadas")

                mostradas = set()

                for foto in fotos:
                    if foto["id"] in mostradas:
                        continue

                    mostradas.add(foto["id"])

                    exibir_foto_segura(
                        foto.get("caminho"),
                        caption=foto.get("titulo", "Foto relacionada"),
                    )

    with st.form("form_assistente_luto", clear_on_submit=True):
        mensagem = st.text_area(
            "Digite sua mensagem",
            placeholder="Escreva aqui...",
            height=120,
            key="mensagem_assistente_luto",
        )

        col_enviar, col_limpar = st.columns([0.65, 0.35])

        with col_enviar:
            enviar = st.form_submit_button(
                "Enviar",
                use_container_width=True,
                type="primary"
            )

        with col_limpar:
            limpar = st.form_submit_button(
                "Limpar",
                use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if limpar:
        st.session_state.historico_assistente = []
        st.rerun()

    if enviar and mensagem.strip():
        st.session_state.historico_assistente.append({
            "tipo": "user",
            "texto": mensagem.strip(),
        })

        try:

            usuario = st.session_state.get("usuario_atual") or {}

            contexto_adicional = ""

            if usuario.get("tipo") == "visitante":
                contexto_adicional = (
                    "A pessoa visitante autorizada se chama {}. "
                    "Ela está registrada como {} de {} e está explorando "
                    "as histórias compartilhadas."
                ).format(
                    usuario.get("nome", "Visitante"),
                    usuario.get("parentesco", "relação não informada"),
                    usuario.get("nome_falecido", "a pessoa responsável pela história")
                )

            resposta = st.session_state.assistente_obj.conversar(
                mensagem.strip(),
                contexto_adicional=contexto_adicional
            )
        except Exception as exc:
            resposta = (
                "Desculpe, tive uma dificuldade para responder agora. "
                "Tente novamente em alguns instantes."
            )
            st.error("Não foi possível continuar agora. Tente novamente em alguns instantes.")

        fotos_relacionadas = []

        usuario = st.session_state.get("usuario_atual") or {}

        if usuario.get("tipo") == "visitante":
            contato_id = usuario.get("id")

            palavras = _extrair_palavras_relevantes(mensagem.strip())

            for palavra in palavras:
                if not isinstance(palavra, str):
                    continue

                resultado = db.buscar_fotos_por_contato_e_texto(
                    contato_id,
                    palavra
                )

                fotos_relacionadas.extend(resultado)

        st.session_state.historico_assistente.append({
            "tipo": "bot",
            "texto": resposta,
            "fotos": fotos_relacionadas
        })

        st.rerun()


def _obter_nome_referencia() -> str:
    usuario = st.session_state.get("usuario_atual") or {}

    if usuario.get("tipo") == "visitante":
        return (
            usuario.get("nome_falecido")
            or usuario.get("falecido_nome")
            or "essa pessoa especial"
        )

    return usuario.get("nome_completo") or "sua história"


def _inicializar_chat():
    if "historico_assistente" not in st.session_state:
        st.session_state.historico_assistente = []

    usuario = st.session_state.get("usuario_atual") or {}

    modo = "memorial" if usuario.get("tipo") == "visitante" else "legado"

    if modo == "memorial":
        usuario_id_referencia = usuario.get("usuario_id") or usuario.get("falecido_id")
    else:
        usuario_id_referencia = usuario.get("id")

    if (
        "assistente_obj" not in st.session_state
        or st.session_state.get("assistente_modo") != modo
        or st.session_state.get("assistente_usuario_id") != usuario_id_referencia
        or st.session_state.get("assistente_contato_id") != usuario.get("id")
    ):
        st.session_state.assistente_obj = AssistenteLuto(
            usuario_id_referencia,
            modo=modo,
            contato_id=usuario.get("id") if modo == "memorial" else None,
        )
        st.session_state.assistente_modo = modo
        st.session_state.assistente_usuario_id = usuario_id_referencia
        st.session_state.assistente_contato_id = (
            usuario.get("id") if modo == "memorial" else None
        )

    if not st.session_state.historico_assistente:
        if modo == "memorial":
            st.session_state.historico_assistente.append({
                "tipo": "bot",
                "texto": (
                    "Olá. Vamos explorar esta história.\n\n"
                    "Posso ajudar você a descobrir histórias, fotos, vídeos, valores e momentos compartilhados."
                )
            })
        else:
            st.session_state.historico_assistente.append({
                "tipo": "bot",
                "texto": (
                    "Olá. Este é o Curador de Histórias.\n\n"
                    "Estou aqui para fazer perguntas simples e ajudar você a registrar histórias, valores, aprendizados e lembranças importantes da sua vida."
                )
            })
