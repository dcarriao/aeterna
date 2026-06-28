import html
import json
import re
import streamlit as st
import os
from datetime import datetime

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


# ==========================================================================
# CURADOR INTELIGENTE - SITE ALINHADO AO MOBILE
# ==========================================================================
_TIPOS_CURADOR = [
    "Pessoa", "Evento familiar", "Viagem", "Infância", "Relacionamento",
    "Trabalho", "Conquista", "Mudança de vida", "Aprendizado", "Rotina",
    "Data comemorativa", "Outro",
]


def _curador_json_limpo(texto: str) -> dict:
    bruto = str(texto or "").strip()
    if not bruto:
        return {}
    bruto = re.sub(r"^```(?:json)?", "", bruto, flags=re.I).strip()
    bruto = re.sub(r"```$", "", bruto).strip()
    match = re.search(r"\{.*\}", bruto, flags=re.S)
    if match:
        bruto = match.group(0)
    try:
        return json.loads(bruto)
    except Exception:
        return {}


def _curador_lista(valor, limite=None):
    if isinstance(valor, list):
        itens = [str(v).strip() for v in valor if str(v).strip()]
    elif isinstance(valor, str):
        itens = [v.strip(" -•\t") for v in valor.split("\n") if v.strip(" -•\t")]
    else:
        itens = []
    vistos = []
    for item in itens:
        if item and item not in vistos:
            vistos.append(item)
    return vistos[:limite] if limite else vistos


def _curador_plano_fallback(titulo: str, conteudo: str, data_evento: str, pessoas: list, colecao: str) -> dict:
    base = f"{titulo} {conteudo} {colecao}".lower()
    if any(p in base for p in ["pai", "mãe", "mae", "avó", "avo", "avô", "tio", "tia", "filho", "filha"]):
        tipo = "Pessoa"
        perguntas = [
            "Como você descreveria essa pessoa?",
            "Qual característica dela você mais quer preservar?",
            "Existe uma lembrança que representa bem quem ela era?",
            "O que essa pessoa ensinou a você?",
            "O que você gostaria que sua família soubesse sobre ela?",
        ]
    elif any(p in base for p in ["viagem", "praia", "gramado", "hotel", "foz", "canyons", "passeio"]):
        tipo = "Viagem"
        perguntas = [
            "Como essa viagem começou?",
            "Quem estava com você?",
            "Qual momento dessa viagem ficou mais marcado?",
            "Houve algo inesperado ou engraçado?",
            "O que essa viagem representa para você hoje?",
        ]
    elif any(p in base for p in ["emprego", "trabalho", "empresa", "chefe", "carreira"]):
        tipo = "Trabalho"
        perguntas = [
            "Como surgiu essa oportunidade?",
            "Quais dificuldades você enfrentou nessa fase?",
            "Quem ajudou você nesse período?",
            "O que você aprendeu com essa experiência?",
            "Como isso mudou sua vida?",
        ]
    elif any(p in base for p in ["almoço", "almoco", "jantar", "domingo", "família", "familia", "aniversário", "aniversario"]):
        tipo = "Evento familiar"
        perguntas = [
            "Como esse encontro aconteceu?",
            "Quem estava presente?",
            "O que tornou esse momento especial?",
            "Houve alguma conversa marcante?",
            "Como você gostaria que sua família lembrasse desse dia?",
        ]
    else:
        tipo = "Outro"
        perguntas = [
            "O que aconteceu nesse momento?",
            "Quem estava envolvido?",
            "O que tornou essa lembrança importante?",
            "O que você aprendeu com essa experiência?",
        ]
    return {
        "tipo": tipo,
        "perguntas": perguntas[:7],
        "valores_percebidos": [],
        "pessoas_identificadas": pessoas or [],
        "locais_identificados": [],
        "datas_identificadas": [data_evento] if data_evento else [],
    }


def _curador_gerar_plano(assistente, titulo: str, conteudo: str, data_evento: str, pessoas: list, colecao: str) -> dict:
    contexto = (
        f"Título: {titulo or ''}\n"
        f"Texto inicial: {conteudo or ''}\n"
        f"Data informada: {data_evento or ''}\n"
        f"Pessoas informadas: {', '.join(pessoas or [])}\n"
        f"Coleção informada: {colecao or ''}"
    )
    prompt = f"""
Você é o Curador de Histórias da aEterna.
Analise a memória abaixo e responda APENAS em JSON válido.
Não mostre explicações fora do JSON.
Não invente fatos.
Se não houver evidência suficiente para classificar, use tipo "Outro".
Tipos permitidos: {', '.join(_TIPOS_CURADOR)}.
Gere entre 4 e 7 perguntas específicas para esse tipo de memória.
Não use perguntas incompatíveis com o contexto.
Não trate uma viagem ou almoço como se fosse sempre sobre uma pessoa.

Memória:
{contexto}

Formato obrigatório:
{{
  "tipo": "...",
  "perguntas": ["..."],
  "valores_percebidos": ["..."],
  "pessoas_identificadas": ["..."],
  "locais_identificados": ["..."],
  "datas_identificadas": ["..."]
}}
""".strip()
    try:
        dados = _curador_json_limpo(assistente.conversar(prompt))
    except Exception as exc:
        print("Erro ao gerar plano do Curador:", exc)
        dados = {}
    if not dados:
        dados = _curador_plano_fallback(titulo, conteudo, data_evento, pessoas, colecao)
    tipo = dados.get("tipo") if dados.get("tipo") in _TIPOS_CURADOR else "Outro"
    perguntas = _curador_lista(dados.get("perguntas"), 7)
    if len(perguntas) < 4:
        fallback = _curador_plano_fallback(titulo, conteudo, data_evento, pessoas, colecao)
        perguntas = fallback["perguntas"]
        if tipo == "Outro":
            tipo = fallback["tipo"]
    return {
        "tipo": tipo,
        "perguntas": perguntas[:7],
        "valores_percebidos": _curador_lista(dados.get("valores_percebidos"), 8),
        "pessoas_identificadas": _curador_lista(dados.get("pessoas_identificadas"), 10),
        "locais_identificados": _curador_lista(dados.get("locais_identificados"), 6),
        "datas_identificadas": _curador_lista(dados.get("datas_identificadas"), 6),
    }


def _curador_gerar_narrativa(assistente, titulo: str, conteudo: str, plano: dict, respostas: dict) -> dict:
    respostas_limpas = {p: r for p, r in respostas.items() if str(r or "").strip()}
    prompt = f"""
Você é o Curador de Histórias da aEterna.
Transforme as informações abaixo em uma narrativa final fluida e curta.
Use apenas informações fornecidas.
Não invente pessoas, datas, locais, sentimentos ou fatos.
Não concatene respostas soltas.
Depois gere análise objetiva.
Responda APENAS em JSON válido.

Título: {titulo or ''}
Texto inicial: {conteudo or ''}
Tipo identificado: {plano.get('tipo') or 'Outro'}
Perguntas e respostas: {json.dumps(respostas_limpas, ensure_ascii=False)}
Entidades já identificadas: {json.dumps(plano, ensure_ascii=False)}

Formato obrigatório:
{{
  "narrativa": "...",
  "valores_percebidos": ["..."],
  "pessoas_identificadas": ["..."],
  "locais_identificados": ["..."],
  "datas_identificadas": ["..."]
}}
""".strip()
    try:
        dados = _curador_json_limpo(assistente.conversar(prompt))
    except Exception as exc:
        print("Erro ao gerar narrativa do Curador:", exc)
        dados = {}
    narrativa = str(dados.get("narrativa") or conteudo or titulo or "").strip()
    return {
        "narrativa": narrativa,
        "valores_percebidos": _curador_lista(dados.get("valores_percebidos") or plano.get("valores_percebidos"), 8),
        "pessoas_identificadas": _curador_lista(dados.get("pessoas_identificadas") or plano.get("pessoas_identificadas"), 10),
        "locais_identificados": _curador_lista(dados.get("locais_identificados") or plano.get("locais_identificados"), 6),
        "datas_identificadas": _curador_lista(dados.get("datas_identificadas") or plano.get("datas_identificadas"), 6),
    }


def _curador_montar_conteudo_final(titulo: str, conteudo: str, plano: dict, respostas: dict, resultado: dict) -> str:
    partes = []
    narrativa = (resultado.get("narrativa") or conteudo or "").strip()
    if narrativa:
        partes.append(narrativa)
    partes.append("\n---\nAnálise da memória")
    partes.append(f"Tipo identificado: {plano.get('tipo') or 'Outro'}")
    for rotulo, chave in [
        ("Valores percebidos", "valores_percebidos"),
        ("Pessoas identificadas", "pessoas_identificadas"),
        ("Locais identificados", "locais_identificados"),
        ("Datas identificadas", "datas_identificadas"),
    ]:
        itens = resultado.get(chave) or plano.get(chave) or []
        if itens:
            partes.append(f"{rotulo}: {', '.join(itens)}")
    respostas_limpas = {p: r for p, r in respostas.items() if str(r or '').strip()}
    if respostas_limpas:
        partes.append("\nPerguntas do Curador")
        for pergunta, resposta in respostas_limpas.items():
            partes.append(f"- {pergunta}\n  Resposta: {str(resposta).strip()}")
    if conteudo and conteudo.strip() and conteudo.strip() not in narrativa:
        partes.append("\nTexto inicial informado")
        partes.append(conteudo.strip())
    return "\n".join(partes).strip()


def _render_curador_memoria_primeiro(db: BancoDados, usuario: dict, nome_referencia: str):
    st.markdown("""
    <style>
    .main .block-container, [data-testid="stMainBlockContainer"] {
        padding-top: 0.15rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-bottom: 0.6rem !important;
    }
    .ae-curador-hero { margin-top: -1.1rem; margin-bottom: .55rem; }
    .ae-curador-hero h1 { color:#21104a; font-size:1.55rem; line-height:1.05; margin:0; font-weight:950; }
    .ae-curador-hero p { color:#6d6380; margin:.15rem 0 0; font-size:.88rem; }
    .ae-curador-grid { display:grid; grid-template-columns: 1.05fr .95fr; gap:1.05rem; align-items:start; }
    .ae-curador-card { background:rgba(255,255,255,.55); border:1px solid rgba(222,202,166,.86); border-radius:18px; padding:.8rem; box-shadow:0 12px 30px rgba(43,23,71,.045); }
    .ae-curador-card h2, .ae-curador-card h3 { color:#21104a; margin:0 0 .55rem; }
    .ae-curador-meta { display:flex; flex-wrap:wrap; gap:.35rem; margin:.45rem 0; }
    .ae-curador-pill { display:inline-flex; align-items:center; border:1px solid rgba(212,168,79,.38); background:rgba(255,248,231,.78); color:#21104a; border-radius:999px; padding:.26rem .58rem; font-size:.78rem; font-weight:850; }
    .ae-curador-question { border:1px solid rgba(104,79,176,.24); border-radius:14px; background:rgba(255,255,255,.70); padding:.55rem .65rem; margin:.42rem 0; }
    .ae-curador-question strong { color:#21104a; display:block; margin-bottom:.28rem; }
    .ae-curador-note { color:#6d6380; font-size:.82rem; line-height:1.38; }
    .ae-curador-preview { border-left:3px solid #d4a84f; padding-left:.75rem; color:#2f2440; line-height:1.45; }
    .st-key-curador_gerar_plano button, .st-key-curador_salvar_final button, .st-key-curador_nova_memoria button {
        background:linear-gradient(135deg,#f8dc92,#d4af37 62%,#b77a46)!important; color:#1b0f2e!important; border:0!important; border-radius:12px!important; font-weight:900!important; min-height:2.5rem!important;
    }
    .st-key-curador_ver_historia button { background:rgba(255,255,255,.92)!important; color:#21104a!important; border:1px solid rgba(212,168,79,.40)!important; border-radius:12px!important; font-weight:900!important; }
    @media (max-width: 900px) {
        .ae-curador-grid { grid-template-columns:1fr; gap:.75rem; }
        .ae-curador-hero { margin-top:-.35rem; }
        .ae-curador-card { padding:.7rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    usuario_id = usuario.get("id")
    try:
        contatos = db.listar_contatos_usuario(usuario_id)
    except Exception as exc:
        print("Erro ao listar contatos do curador:", exc)
        contatos = []

    nomes_contatos = [c.get("nome_completo") for c in contatos if c.get("nome_completo")]
    colecoes = [
        ("livre", "Selecione uma coleção"), ("familia", "Família"),
        ("viagens", "Viagens"), ("infancia", "Infância"),
        ("carreira", "Carreira"), ("valores", "Valores"),
        ("amor", "Amor"), ("conquista", "Conquistas"),
    ]
    mapa_colecoes = {valor: rotulo for valor, rotulo in colecoes}

    st.markdown('<div class="ae-curador-hero"><h1>Curador de Histórias</h1><p>Registre uma memória. Depois o Curador identifica o contexto e faz perguntas adequadas.</p></div>', unsafe_allow_html=True)

    if st.session_state.get("curador_reset"):
        for key in list(st.session_state.keys()):
            if key.startswith("curador_") and key not in {"curador_reset"}:
                del st.session_state[key]
        st.session_state.pop("curador_reset", None)

    st.markdown('<div class="ae-curador-grid">', unsafe_allow_html=True)
    col_form, col_curador = st.columns([1.05, .95], gap="large")

    with col_form:
        st.markdown('<div class="ae-curador-card">', unsafe_allow_html=True)
        st.markdown("## Nova memória")
        media_cols = st.columns(2, gap="small")
        with media_cols[0]:
            foto_memoria = st.file_uploader("Foto (opcional)", type=["png", "jpg", "jpeg", "webp"], key="curador_memoria_foto")
        with media_cols[1]:
            video_memoria = st.file_uploader("Vídeo (opcional)", type=["mp4", "mov", "avi", "mkv"], key="curador_memoria_video")

        titulo = st.text_input("Título ou início da memória", key="curador_memoria_titulo", placeholder="Ex: Almoço com a tia Denir")
        conteudo = st.text_area("O que você já lembra?", key="curador_memoria_conteudo", height=118, placeholder="Escreva o que aconteceu, quem estava junto, onde foi ou por que isso importa...", max_chars=5000)
        meta_col1, meta_col2 = st.columns(2, gap="small")
        with meta_col1:
            data_valor = st.date_input("Data aproximada", value=None, format="DD/MM/YYYY", key="curador_memoria_data_input")
            data_aproximada = data_valor.strftime("%d/%m/%Y") if data_valor else ""
        with meta_col2:
            pessoas_relacionadas = st.multiselect("Pessoas relacionadas (opcional)", options=nomes_contatos, key="curador_memoria_pessoas", placeholder="Digite nomes e selecione")
        colecao_valor = st.selectbox("Coleção (opcional)", options=[item[0] for item in colecoes], format_func=lambda valor: mapa_colecoes.get(valor, valor), key="curador_memoria_colecao")

        gerar_disabled = not (titulo.strip() or conteudo.strip())
        if st.button("Gerar perguntas do Curador", key="curador_gerar_plano", type="primary", use_container_width=True, disabled=gerar_disabled):
            plano = _curador_gerar_plano(st.session_state.assistente_obj, titulo, conteudo, data_aproximada, pessoas_relacionadas, mapa_colecoes.get(colecao_valor, colecao_valor))
            st.session_state["curador_plano"] = plano
            st.session_state.pop("curador_resultado", None)
            st.session_state.pop("curador_memoria_salva_id", None)
            st.rerun()
        if gerar_disabled:
            st.caption("Informe pelo menos um título ou uma lembrança para o Curador analisar.")
        st.markdown('</div>', unsafe_allow_html=True)

    plano = st.session_state.get("curador_plano")
    respostas = {}

    with col_curador:
        st.markdown('<div class="ae-curador-card">', unsafe_allow_html=True)
        st.markdown("## Curadoria")
        if not plano:
            st.markdown('<div class="ae-curador-note">O Curador ainda não analisou esta memória. Ele só gera perguntas depois de entender o contexto informado.</div>', unsafe_allow_html=True)
        else:
            tipo = plano.get("tipo") or "Outro"
            st.markdown(f"<div class='ae-curador-pill'>Tipo identificado: {html.escape(tipo)}</div>", unsafe_allow_html=True)
            perguntas = plano.get("perguntas") or []
            for idx, pergunta in enumerate(perguntas):
                st.markdown(f"<div class='ae-curador-question'><strong>{idx+1}. {html.escape(pergunta)}</strong></div>", unsafe_allow_html=True)
                respostas[pergunta] = st.text_area("Responder ou pular", key=f"curador_resposta_{idx}", height=72, label_visibility="collapsed")

            if st.button("Gerar narrativa e salvar memória", key="curador_salvar_final", type="primary", use_container_width=True):
                if not (titulo.strip() or conteudo.strip()):
                    st.warning("Informe um título ou texto inicial antes de salvar.")
                else:
                    try:
                        resultado = _curador_gerar_narrativa(st.session_state.assistente_obj, titulo, conteudo, plano, respostas)
                        conteudo_final = _curador_montar_conteudo_final(titulo, conteudo, plano, respostas, resultado)
                        pessoas_final = plano.get("pessoas_identificadas") or pessoas_relacionadas
                        memoria_id = db.salvar_memoria(
                            usuario_id=usuario_id,
                            conteudo=conteudo_final,
                            titulo=titulo.strip() or "Memória sem título",
                            categoria=plano.get("tipo") or colecao_valor or "Outro",
                            origem="curador",
                            data_evento=_curador_normalizar_data(data_aproximada),
                            pessoas_relacionadas=", ".join(pessoas_final) if pessoas_final else None,
                            visibilidade="contatos",
                            contatos_ids=[],
                        )
                        if foto_memoria:
                            upload_foto = storage.upload_streamlit_file(bucket="fotos", arquivo=foto_memoria, usuario_id=usuario_id, pasta="memorias")
                            foto_id = db.adicionar_foto_com_acesso(usuario_id=usuario_id, titulo=titulo.strip() or "Foto da memória", descricao=conteudo_final[:300], categoria=plano.get("tipo") or colecao_valor or "Outro", caminho_arquivo=upload_foto["url"], contatos_ids=[], visibilidade="contatos")
                            db.associar_foto_memoria(memoria_id=memoria_id, foto_id=foto_id)
                        if video_memoria:
                            upload_video = storage.upload_streamlit_file(bucket="videos", arquivo=video_memoria, usuario_id=usuario_id, pasta="memorias")
                            video_id = db.adicionar_video_com_acesso(usuario_id=usuario_id, titulo=titulo.strip() or "Vídeo da memória", destinatario=", ".join(pessoas_relacionadas), caminho_arquivo=upload_video["url"], contatos_ids=[], categoria=plano.get("tipo") or colecao_valor or "Outro", visibilidade="contatos")
                            db.associar_video_memoria(memoria_id=memoria_id, video_id=video_id)
                        st.session_state["curador_memoria_salva_id"] = memoria_id
                        st.session_state["curador_resultado"] = resultado
                        st.success("Memória salva com narrativa e curadoria.")
                        st.rerun()
                    except Exception as exc:
                        print("Erro ao salvar memória curada:", exc)
                        st.error("Não foi possível salvar a memória agora.")
        st.markdown('</div>', unsafe_allow_html=True)

    resultado = st.session_state.get("curador_resultado")
    if resultado:
        st.markdown("### Narrativa final")
        st.markdown(f"<div class='ae-curador-card ae-curador-preview'>{_safe_text(resultado.get('narrativa') or '')}</div>", unsafe_allow_html=True)
        analise_html = []
        for rotulo, chave in [("Valores percebidos", "valores_percebidos"), ("Pessoas identificadas", "pessoas_identificadas"), ("Locais identificados", "locais_identificados"), ("Datas identificadas", "datas_identificadas")]:
            itens = resultado.get(chave) or plano.get(chave) or []
            if itens:
                analise_html.append(f"<div><strong>{html.escape(rotulo)}:</strong> {html.escape(', '.join(itens))}</div>")
        if analise_html:
            st.markdown("### Análise da memória")
            st.markdown("<div class='ae-curador-card'>" + "".join(analise_html) + "</div>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Ver em Minha História", key="curador_ver_historia", use_container_width=True):
                st.session_state.pagina_atual = "minha_historia"
                st.rerun()
        with b2:
            if st.button("Criar outra memória", key="curador_nova_memoria", use_container_width=True):
                st.session_state["curador_reset"] = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

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
