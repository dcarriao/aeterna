import html
import streamlit as st
import os
import json
import re
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




def _curador_json_from_text(texto: str) -> dict:
    base = str(texto or "").strip()
    if not base:
        return {}
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", base, re.S)
    if match:
        base = match.group(1)
    else:
        start = base.find("{")
        end = base.rfind("}")
        if start >= 0 and end > start:
            base = base[start:end + 1]
    try:
        return json.loads(base)
    except Exception:
        return {}


def _curador_limpar_lista(valores, limite: int = 7) -> list:
    saida = []
    if isinstance(valores, str):
        valores = [valores]
    if not isinstance(valores, list):
        return []
    for valor in valores:
        texto = str(valor or "").strip()
        if texto and texto not in saida:
            saida.append(texto)
        if len(saida) >= limite:
            break
    return saida


def _curador_contexto_base(titulo: str, conteudo: str, data_memoria, pessoas: list, categoria: str) -> str:
    data_txt = ""
    if data_memoria:
        try:
            data_txt = data_memoria.strftime("%d/%m/%Y")
        except Exception:
            data_txt = str(data_memoria)
    partes = [
        f"Título: {titulo.strip()}",
        f"Texto inicial: {conteudo.strip()}",
        f"Data informada: {data_txt}",
        f"Pessoas selecionadas: {', '.join(pessoas) if pessoas else ''}",
        f"Categoria escolhida pelo usuário: {categoria or ''}",
    ]
    return "\n".join(partes)


def _curador_analisar_memoria_com_ia(assistente, titulo: str, conteudo: str, data_memoria, pessoas: list, categoria: str) -> dict:
    contexto = _curador_contexto_base(titulo, conteudo, data_memoria, pessoas, categoria)
    prompt = f"""
Você é o Curador de Histórias da aEterna.
Analise a memória abaixo e devolva SOMENTE JSON válido.
Não use markdown. Não explique. Não invente fatos.

Tipos permitidos:
Pessoa, Evento familiar, Viagem, Infância, Relacionamento, Trabalho, Conquista, Mudança de vida, Aprendizado, Rotina, Data comemorativa, Outro.

Regras:
- Identifique o tipo apenas se houver evidência no texto.
- Se não houver evidência suficiente, use "Outro".
- Gere entre 4 e 7 perguntas adequadas ao tipo identificado.
- As perguntas devem estimular lembranças, não coletar dados mecânicos.
- Nunca usar perguntas incompatíveis com o tipo.
- Não assumir que toda memória é sobre uma pessoa.

Memória:
{contexto}

JSON esperado:
{{
  "tipo": "Outro",
  "evidencia_tipo": "trecho ou motivo curto",
  "perguntas": ["pergunta 1", "pergunta 2", "pergunta 3", "pergunta 4"],
  "valores_possiveis": [],
  "pessoas_identificadas": [],
  "locais_identificados": [],
  "datas_identificadas": []
}}
""".strip()
    resposta = assistente.conversar(prompt)
    dados = _curador_json_from_text(resposta)
    perguntas = _curador_limpar_lista(dados.get("perguntas"), 7)
    
    # Robust fallback: if AI returned fewer than 3 questions, fill them with context-aware generic ones so we never crash!
    if len(perguntas) < 3:
        if not perguntas:
            perguntas = [
                "Quem estava com você nesse momento especial?",
                "O que tornou esse dia inesquecível ou diferente de outros?",
                "Quais sentimentos ou lembranças essa memória traz para você?",
                "Há algum outro detalhe ou foto que represente bem esse dia?"
            ]
        else:
            generics = [
                "Quem estava com você nesse momento especial?",
                "O que tornou esse dia inesquecível?",
                "Quais sentimentos ou lembranças essa memória traz?",
                "Há algum outro detalhe que queira registrar?"
            ]
            for g in generics:
                if g not in perguntas:
                    perguntas.append(g)
                if len(perguntas) >= 3:
                    break

    tipo = str(dados.get("tipo") or "Outro").strip()
    tipos_validos = {"Pessoa", "Evento familiar", "Viagem", "Infância", "Relacionamento", "Trabalho", "Conquista", "Mudança de vida", "Aprendizado", "Rotina", "Data comemorativa", "Outro"}
    if tipo not in tipos_validos:
        tipo = "Outro"
    return {
        "tipo": tipo,
        "evidencia_tipo": str(dados.get("evidencia_tipo") or "").strip(),
        "perguntas": perguntas,
        "valores_possiveis": _curador_limpar_lista(dados.get("valores_possiveis"), 8),
        "pessoas_identificadas": _curador_limpar_lista(dados.get("pessoas_identificadas"), 12),
        "locais_identificados": _curador_limpar_lista(dados.get("locais_identificados"), 8),
        "datas_identificadas": _curador_limpar_lista(dados.get("datas_identificadas"), 8),
    }


def _curador_gerar_narrativa_com_ia(assistente, titulo: str, conteudo: str, data_memoria, pessoas: list, categoria: str, analise: dict, respostas: dict) -> dict:
    contexto = _curador_contexto_base(titulo, conteudo, data_memoria, pessoas, categoria)
    qa = []
    for pergunta in analise.get("perguntas", []):
        resposta = str(respostas.get(pergunta) or "").strip()
        if resposta:
            qa.append({"pergunta": pergunta, "resposta": resposta})
    prompt = f"""
Você é o Curador de Histórias da aEterna.
Com base APENAS nas informações fornecidas, gere a narrativa final da memória.
Devolva SOMENTE JSON válido. Não use markdown. Não invente fatos. Não preencha lacunas.
A narrativa deve ser fluida, humana e legível. Não concatene respostas.

Memória original:
{contexto}

Tipo identificado: {analise.get('tipo') or 'Outro'}
Perguntas e respostas:
{json.dumps(qa, ensure_ascii=False)}

Entidades já identificadas:
{json.dumps({
    'valores': analise.get('valores_possiveis', []),
    'pessoas': analise.get('pessoas_identificadas', []),
    'locais': analise.get('locais_identificados', []),
    'datas': analise.get('datas_identificadas', []),
}, ensure_ascii=False)}

JSON esperado:
{{
  "narrativa": "texto final fluido",
  "valores_percebidos": [],
  "pessoas_identificadas": [],
  "locais_identificados": [],
  "datas_identificadas": [],
  "observacoes": []
}}
""".strip()
    resposta = assistente.conversar(prompt)
    dados = _curador_json_from_text(resposta)
    narrativa = str(dados.get("narrativa") or "").strip()
    if not narrativa:
        raise ValueError("A IA não retornou narrativa final.")
    return {
        "narrativa": narrativa,
        "valores_percebidos": _curador_limpar_lista(dados.get("valores_percebidos"), 10),
        "pessoas_identificadas": _curador_limpar_lista(dados.get("pessoas_identificadas"), 12),
        "locais_identificados": _curador_limpar_lista(dados.get("locais_identificados"), 8),
        "datas_identificadas": _curador_limpar_lista(dados.get("datas_identificadas"), 8),
        "observacoes": _curador_limpar_lista(dados.get("observacoes"), 6),
    }


def _curador_montar_conteudo_salvo(narrativa: dict, analise: dict, respostas: dict, texto_original: str) -> str:
    linhas = [narrativa.get("narrativa", "").strip()]
    linhas.append("\n---\n")
    linhas.append("### Análise da memória")
    linhas.append(f"**Tipo identificado:** {analise.get('tipo') or 'Outro'}")
    secoes = [
        ("Valores percebidos", narrativa.get("valores_percebidos") or analise.get("valores_possiveis") or []),
        ("Pessoas identificadas", narrativa.get("pessoas_identificadas") or analise.get("pessoas_identificadas") or []),
        ("Locais identificados", narrativa.get("locais_identificados") or analise.get("locais_identificados") or []),
        ("Datas identificadas", narrativa.get("datas_identificadas") or analise.get("datas_identificadas") or []),
    ]
    for titulo, itens in secoes:
        if itens:
            linhas.append(f"\n**{titulo}:**")
            for item in itens:
                linhas.append(f"- {item}")
    respostas_validas = [(p, str(respostas.get(p) or "").strip()) for p in analise.get("perguntas", []) if str(respostas.get(p) or "").strip()]
    if respostas_validas:
        linhas.append("\n### Respostas usadas pelo Curador")
        for pergunta, resposta in respostas_validas:
            linhas.append(f"**{pergunta}**")
            linhas.append(resposta)
    if texto_original.strip():
        linhas.append("\n### Registro original")
        linhas.append(texto_original.strip())
    return "\n\n".join(linhas).strip()


def _render_curador_memoria_primeiro(db: BancoDados, usuario: dict, nome_referencia: str):
    st.markdown("""
    <style>
    /* Hide Streamlit default header to eliminate huge top margin */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }

    /* Main Block Container - wide layout and pulled up */
    .main .block-container,
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 0.15rem !important;
        padding-bottom: 0.45rem !important;
        max-width: 1420px !important;
        width: min(1420px, calc(100vw - 250px)) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: -3.5rem !important; /* Pulls the entire page up */
    }

    /* Reduce vertical gaps between elements in the main columns */
    [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) [data-testid="stVerticalBlock"] {
        gap: 0.45rem !important;
    }

    /* Style the columns in desktop view as gorgeous, bordered cards */
    @media (min-width: 769px) {
        [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) > div[data-testid="stColumn"]:nth-child(1) {
            background: rgba(255, 255, 255, 0.78) !important;
            border: 1px solid rgba(212, 168, 79, 0.22) !important;
            border-radius: 20px !important;
            padding: 1rem !important;
            box-shadow: 0 10px 30px rgba(43,23,71,0.03) !important;
        }
        [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) > div[data-testid="stColumn"]:nth-child(2) {
            background: rgba(255, 255, 255, 0.72) !important;
            border: 1px solid rgba(212, 168, 79, 0.18) !important;
            border-radius: 20px !important;
            padding: 1rem !important;
            box-shadow: 0 10px 30px rgba(43,23,71,0.03) !important;
        }
        [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) > div[data-testid="stColumn"]:nth-child(3) {
            background: rgba(255, 255, 255, 0.82) !important;
            border: 1px solid rgba(193, 177, 231, 0.45) !important;
            border-radius: 20px !important;
            padding: 1rem !important;
            box-shadow: 0 10px 30px rgba(43,23,71,0.03) !important;
        }
    }

    /* Prevent preview images from expanding vertically and causing excessive scrolling */
    [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) div[data-testid="stColumn"]:nth-child(2) img {
        max-height: 130px !important;
        object-fit: cover !important;
        border-radius: 14px !important;
    }

    /* Steps Progress bar */
    .ae-curador-steps {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.45rem;
        margin: 0.2rem 0 0.45rem;
        padding: 0.24rem;
        border: 1px solid rgba(233, 222, 198, 0.6);
        border-radius: 16px;
        background: rgba(255,255,255,0.72);
    }
    .ae-curador-step {
        border-radius: 13px;
        min-height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        padding: 0.25rem 0.5rem;
        color: #47507a;
        font-weight: 700;
        text-align: center;
        font-size: 0.82rem;
    }
    .ae-curador-step.is-active {
        background: linear-gradient(180deg, rgba(255,250,241,.95), rgba(255,248,232,.92));
        border: 1px solid rgba(234, 181, 77, 0.55);
        color: #b36e16;
    }

    /* File Uploader styling - extremely compact */
    div[data-testid="stFileUploader"] section {
        background: rgba(239,231,214,0.4) !important;
        border: 1px dashed rgba(212,168,79,0.3) !important;
        border-radius: 10px !important;
        min-height: 48px !important;
        padding: 0.1rem 0.4rem !important;
    }
    div[data-testid="stFileUploader"] section div {
        font-size: 0.72rem !important;
    }

    /* Preview Card details */
    .ae-curador-preview-media {
        height: 96px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at top, rgba(255, 218, 153, .45), rgba(219, 205, 180, .2) 55%, rgba(250, 246, 239, .9));
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
        border-top: 1px solid rgba(233, 222, 198, 0.7);
        margin-top: 0.45rem;
        padding-top: 0.45rem;
        color: #6d6380;
        font-size: 0.79rem;
    }
    .ae-curador-tip {
        border: 1px solid rgba(233, 222, 198, 0.6);
        border-radius: 14px;
        padding: 0.5rem;
        color: #6d6380;
        background: rgba(255,255,255,.72);
        font-size: 0.78rem;
        margin-top: 0.4rem;
    }

    /* Question Pills in Column 3 */
    .ae-curador-question-shell {
        display: grid;
        gap: 0.4rem;
        margin-top: 0.5rem;
    }
    .ae-curador-question-pill {
        min-height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0.4rem 0.7rem;
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(249,245,255,.98), rgba(244,238,252,.98));
        color: #5c3d87;
        border: 1px solid rgba(193, 177, 231, 0.7);
        font-weight: 700;
        font-size: 0.8rem;
        line-height: 1.18;
    }

    /* Como funciona block at the bottom - extremely compact */
    .ae-curador-how {
        margin-top: 0.5rem !important;
        background: rgba(255,255,255,.92);
        border: 1px solid rgba(233, 222, 198, 0.7);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(64, 45, 19, 0.03);
        padding: 0.45rem 0.55rem !important;
    }
    .ae-curador-how h3 {
        color: #21104a;
        margin: 0 0 0.35rem !important;
        font-size: 0.88rem !important;
        font-weight: 900;
    }
    .ae-curador-how-grid {
        display: flex;
        align-items: flex-start;
        gap: 0;
    }
    .ae-curador-how-item {
        flex: 1;
        border: 1px solid rgba(233, 222, 198, 0.6);
        border-radius: 16px;
        background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(250,247,241,.96));
        padding: 0.4rem !important;
        min-height: 64px !important;
        font-size: 0.74rem !important;
        line-height: 1.36;
    }
    .ae-curador-how-item strong {
        display: block;
        color: #21104a;
        margin-bottom: 0.15rem !important;
    }
    .ae-curador-how-icon {
        font-size: 1.15rem !important;
        display: block;
        margin-bottom: 0.15rem !important;
    }
    .ae-curador-how-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 0.28rem;
        padding-top: 0.4rem !important;
        color: #b07a1d;
        font-size: 0.9rem;
        font-weight: 700;
        flex-shrink: 0;
    }

    /* Style overrides for details and chips */
    .ae-curador-section-title {
        color: #2B1747;
        font-weight: 950;
        font-size: 1.05rem;
        margin: 0 0 0.45rem;
    }
    .ae-curador-analysis {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.35rem 0 0.5rem;
    }
    .ae-curador-chip {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.28rem 0.58rem;
        background: rgba(244,238,252,0.92);
        border: 1px solid rgba(193,177,231,0.72);
        color: #4f2476;
        font-size: 0.76rem;
        font-weight: 850;
    }
    .ae-curador-question {
        border: 1px solid rgba(193,177,231,0.4);
        border-radius: 14px;
        background: rgba(255,255,255,0.75);
        padding: 0.45rem 0.55rem !important;
        margin-bottom: 0.42rem !important;
    }
    .ae-curador-question strong {
        color: #2B1747;
        display: block;
        margin-bottom: 0.2rem !important;
        font-size: 0.8rem;
    }

    /* Streamlit Button overrides inside curator */
    .st-key-curador_aprofundar_btn button,
    .st-key-curador_salvar_final_btn button,
    .st-key-curador_gerar_narrativa_btn button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 950 !important;
        min-height: 2.45rem !important;
    }
    .st-key-curador_salvar_direto_btn button {
        background: #2B1747 !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 950 !important;
        min-height: 2.45rem !important;
    }
    .st-key-curador_reanalisar_btn button,
    .st-key-curador_voltar_perguntas_btn button,
    .st-key-curador_nova_memoria_btn button,
    .st-key-curador_ver_historia_btn button {
        background: rgba(255,255,255,0.85) !important;
        color: #2B1747 !important;
        border: 1px solid rgba(43,23,71,0.22) !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        min-height: 2.45rem !important;
    }

    @media (max-width: 768px) {
        .ae-curador-steps {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        .ae-curador-how-grid {
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 0.5rem !important;
        }
        .ae-curador-how-arrow {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    usuario_id = usuario.get("id")
    if not usuario_id:
        st.error("Usuário não identificado.")
        return

    _inicializar_chat()
    assistente = st.session_state.get("assistente_obj")

    prefixo = "curador_site_mobile_"
    etapa_key = prefixo + "etapa"
    if etapa_key not in st.session_state:
        st.session_state[etapa_key] = "form"

    contatos = []
    try:
        contatos = db.listar_contatos_usuario(usuario_id) or []
    except Exception as exc:
        print("Erro ao listar contatos do curador:", exc)
    nomes_contatos = [c.get("nome_completo") for c in contatos if c.get("nome_completo")]

    etapa = st.session_state.get(etapa_key, "form")

    # Wizard Steps progress calculation
    step1_active = "is-active" if etapa == "form" else ""
    step2_active = "is-active" if etapa == "form" else ""
    step3_active = "is-active" if etapa == "salvo" else ""
    step4_active = "is-active" if etapa in ("perguntas", "final") else ""

    st.markdown(f"""
    <div class="ae-curador-steps">
        <div class="ae-curador-step {step1_active}">🖼️ 1. Adicionar mídia (opcional)</div>
        <div class="ae-curador-step {step2_active}">✏️ 2. Escrever contexto</div>
        <div class="ae-curador-step {step3_active}">✅ 3. Salvar memória</div>
        <div class="ae-curador-step {step4_active}">💬 4. Explorar com o Curador</div>
    </div>
    """, unsafe_allow_html=True)

    if etapa != "form" and etapa != "salvo":
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) > div[data-testid="stColumn"]:nth-child(1),
            [data-testid="stHorizontalBlock"]:has(.ae-curador-page-marker) > div[data-testid="stColumn"]:nth-child(2) {
                display: none !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<span class="ae-curador-page-marker"></span>', unsafe_allow_html=True)
    col_form, col_preview, col_explore = st.columns([1.25, 0.88, 0.87], gap="small")

    with col_form:
        st.markdown('<div class="ae-curador-section-title">✍️ Nova memória</div>', unsafe_allow_html=True)
        
        is_disabled = (etapa != "form")

        c_foto, c_video = st.columns(2, gap="small")
        with c_foto:
            foto_memoria = st.file_uploader(
                "Adicionar foto",
                type=["png", "jpg", "jpeg", "webp"],
                key=prefixo + "foto",
                disabled=is_disabled,
                help="JPG, PNG até 10MB"
            )
        with c_video:
            video_memoria = st.file_uploader(
                "Adicionar vídeo",
                type=["mp4", "mov", "avi", "mkv"],
                key=prefixo + "video",
                disabled=is_disabled,
                help="MP4 até 50MB"
            )

        # Store uploaded file objects in session_state before they are disabled and return None
        if etapa == "form":
            st.session_state[prefixo + "stored_foto"] = foto_memoria
            st.session_state[prefixo + "stored_video"] = video_memoria

        foto_memoria_val = st.session_state.get(prefixo + "stored_foto") or foto_memoria
        video_memoria_val = st.session_state.get(prefixo + "stored_video") or video_memoria

        st.text_input(
            "Título da memória",
            key=prefixo + "titulo",
            placeholder="Dê um título para esta memória",
            disabled=is_disabled
        )
        titulo_val = st.session_state.get(prefixo + "titulo", "").strip()

        c_date, c_cat = st.columns(2, gap="small")
        with c_date:
            st.text_input(
                "Data da memória",
                key=prefixo + "data_txt",
                placeholder="DD/MM/AAAA (ou aproximada)",
                disabled=is_disabled
            )
            data_memoria_txt_val = st.session_state.get(prefixo + "data_txt", "").strip()
            data_memoria_val = _curador_normalizar_data(data_memoria_txt_val)
        with c_cat:
            st.selectbox(
                "Categoria (opcional)",
                ["Momentos", "Família", "Viagens", "Infância", "Trabalho", "Aprendizados", "Conquistas", "Outro"],
                key=prefixo + "categoria_visual",
                disabled=is_disabled
            )
            categoria_visual_val = st.session_state.get(prefixo + "categoria_visual", "Outro")

        c_people, c_share = st.columns([1.3, 0.7], gap="small")
        with c_people:
            st.multiselect(
                "Pessoas relacionadas (opcional)",
                options=nomes_contatos,
                key=prefixo + "pessoas",
                placeholder="Digite nomes e selecione",
                disabled=is_disabled
            )
            pessoas_relacionadas_val = st.session_state.get(prefixo + "pessoas", [])
        with c_share:
            compartilhar_val = st.toggle(
                "Compartilhar",
                key=prefixo + "compartilhar",
                value=False,
                disabled=is_disabled
            )

        # Handle selective sharing dynamically
        contatos_selecionados_ids = []
        if compartilhar_val:
            opcoes_contato = {
                c["nome_completo"]: c["id"]
                for c in contatos if c.get("nome_completo")
            }
            if opcoes_contato:
                contatos_vis_nomes = st.multiselect(
                    "Compartilhar com pessoas específicas (opcional)",
                    options=list(opcoes_contato.keys()),
                    key=prefixo + "contatos_compartilhar",
                    disabled=is_disabled,
                    placeholder="Selecione contatos (vazio = compartilhar com todos)"
                )
                contatos_selecionados_ids = [opcoes_contato[n] for n in contatos_vis_nomes]
            else:
                st.caption("⚠️ Nenhum contato cadastrado.")

        st.text_area(
            "Conte esta história",
            key=prefixo + "conteudo",
            placeholder="Escreva o que aconteceu, onde, com quem, detalhes marcantes...",
            height=110,
            disabled=is_disabled
        )
        conteudo_val = st.session_state.get(prefixo + "conteudo", "").strip()

        st.markdown('<div style="margin-top: 0.8rem;"></div>', unsafe_allow_html=True)
        c_btn1, c_btn2 = st.columns(2, gap="small")
        with c_btn1:
            aprofundar = st.button(
                "✨ Aprofundar esta história",
                key="curador_aprofundar_btn",
                use_container_width=True,
                disabled=is_disabled
            )
        with c_btn2:
            salvar_direto = st.button(
                "💾 Salvar história",
                key="curador_salvar_direto_btn",
                use_container_width=True,
                disabled=is_disabled
            )

    # Column 2: Live Memory Preview
    with col_preview:
        st.markdown('<div class="ae-curador-section-title">👁️ Prévia da memória</div>', unsafe_allow_html=True)
        
        preview_titulo = st.session_state.get(prefixo + "titulo", "").strip() or "Título da memória aparecerá aqui"
        preview_texto = _curador_trecho(st.session_state.get(prefixo + "conteudo", ""))
        preview_data = _curador_preview_data(data_memoria_val) if data_memoria_val else (st.session_state.get(prefixo + "data_txt", "") or "Data da memória")
        
        sel_pessoas = st.session_state.get(prefixo + "pessoas", [])
        preview_pessoas = ", ".join(sel_pessoas) if sel_pessoas else "Pessoas relacionadas"
        sel_categoria = st.session_state.get(prefixo + "categoria_visual", "Outro")
        
        media_total = int(bool(foto_memoria)) + int(bool(video_memoria))
        
        if foto_memoria:
            st.image(foto_memoria, use_container_width=True)
        else:
            st.markdown(
                "<div class='ae-curador-preview-media'><div style='font-size:2.2rem;color:#a48b62;'>📖</div></div>",
                unsafe_allow_html=True,
            )
            
        st.markdown(
            f"<div style='display:flex;justify-content:flex-end;margin:.18rem 0 .08rem;'><span class='ae-badge' style='background:rgba(43,23,71,.74);color:white;border-radius:999px;padding:.16rem .44rem;font-size:.72rem;font-weight:800;'>{max(media_total, 1)}/3</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div style='color:#21104a;font-weight:900;font-size:.96rem;margin-bottom:.18rem;'>{html.escape(preview_titulo)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#6d6380;line-height:1.34;font-size:.83rem;'>{html.escape(preview_texto)}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='ae-curador-hint'>"
            f"<div style='margin-bottom:.24rem;'>🗓️ {html.escape(preview_data)}</div>"
            f"<div style='margin-bottom:.24rem;'>👥 {html.escape(preview_pessoas)}</div>"
            f"<div>🗂️ {html.escape(sel_categoria)}</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='ae-curador-tip'>A prévia é atualizada conforme você preenche os campos.</div>",
            unsafe_allow_html=True,
        )

    # Column 3: Curadoria Step
    with col_explore:
        if etapa == "form":
            st.markdown("### Explorar com o Curador")
            st.markdown(
                "<div style='color:#6d6380;line-height:1.36;font-size:.84rem;margin-bottom:.46rem;'>"
                "Após preencher sua memória ao lado, o Curador identificará o contexto e criará perguntas para aprofundar sua história."
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown("<div class='ae-curador-question-shell'>", unsafe_allow_html=True)
            default_pills = [
                ("👤", "Quem estava com você?"),
                ("⭐", "O que tornou esse momento especial?"),
                ("📷", "Existe outra foto desse dia?"),
                ("💜", "Como você se sentiu?"),
            ]
            for icone, pergunta in default_pills:
                st.markdown(
                    f"<div class='ae-curador-question-pill'>{icone} {html.escape(pergunta)}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='ae-curador-tip' style='margin-top:.52rem;'>O Curador não substitui a memória. Ele ajuda a aprofundar o que você registrou.</div>",
                unsafe_allow_html=True,
            )

            if aprofundar:
                if not titulo_val and not conteudo_val:
                    st.warning("Escreva um título ou uma memória antes de aprofundar.")
                elif not assistente:
                    st.error("Curador indisponível no momento.")
                else:
                    with st.spinner("Analisando a memória..."):
                        try:
                            analise = _curador_analisar_memoria_com_ia(
                                assistente,
                                titulo_val,
                                conteudo_val,
                                data_memoria_val,
                                pessoas_relacionadas_val,
                                categoria_visual_val,
                            )
                            st.session_state[prefixo + "analise"] = analise
                            st.session_state[etapa_key] = "perguntas"
                            st.rerun()
                        except Exception as exc:
                            print("Erro ao analisar memória com IA:", exc)
                            st.error("Não foi possível gerar perguntas contextualizadas agora.")

            if salvar_direto:
                if st.session_state.get(prefixo + "salvando_direto"):
                    st.warning("Esta memória já está sendo salva.")
                elif not conteudo_val:
                    st.warning("Escreva a memória antes de salvar.")
                else:
                    st.session_state[prefixo + "salvando_direto"] = True
                    try:
                        visibilidade_direto = "seletivo" if (compartilhar_val and contatos_selecionados_ids) else ("contatos" if compartilhar_val else "privado")
                        contatos_ids_direto = contatos_selecionados_ids if visibilidade_direto == "seletivo" else []
                        memoria_id = db.salvar_memoria(
                            usuario_id=usuario_id,
                            conteudo=conteudo_val,
                            titulo=titulo_val or "Memória sem título",
                            categoria=categoria_visual_val,
                            origem="curador",
                            data_evento=data_memoria_val if data_memoria_val else None,
                            pessoas_relacionadas=", ".join(pessoas_relacionadas_val) if pessoas_relacionadas_val else None,
                            visibilidade=visibilidade_direto,
                            contatos_ids=contatos_ids_direto,
                        )
                        if foto_memoria_val:
                            upload_foto = storage.upload_streamlit_file("fotos", foto_memoria_val, usuario_id, "memorias")
                            foto_id = db.adicionar_foto_com_acesso(usuario_id, titulo_val or "Foto da memória", conteudo_val[:300], categoria_visual_val, upload_foto["url"], contatos_ids_direto, visibilidade_direto)
                            db.associar_foto_memoria(memoria_id=memoria_id, foto_id=foto_id)
                        if video_memoria_val:
                            upload_video = storage.upload_streamlit_file("videos", video_memoria_val, usuario_id, "memorias")
                            video_id = db.adicionar_video_com_acesso(usuario_id, titulo_val or "Vídeo da memória", ", ".join(pessoas_relacionadas_val), upload_video["url"], contatos_ids_direto, categoria_visual_val, visibilidade_direto)
                            db.associar_video_memoria(memoria_id=memoria_id, video_id=video_id)
                        st.session_state[prefixo + "memoria_id"] = memoria_id
                        st.session_state[etapa_key] = "salvo"
                        st.rerun()
                    except Exception as exc:
                        st.session_state[prefixo + "salvando_direto"] = False
                        print("Erro ao salvar direto:", exc)
                        st.error("Não foi possível salvar a memória agora.")

        elif etapa == "perguntas":
            analise = st.session_state.get(prefixo + "analise") or {}
            perguntas = analise.get("perguntas") or []
            st.markdown('<div class="ae-curador-section-title">✨ Perguntas do Curador</div>', unsafe_allow_html=True)
            
            tipo_identificado = analise.get("tipo") or "Outro"
            evidencia = analise.get("evidencia_tipo") or ""
            
            st.markdown(
                f'<div class="ae-curador-analysis" style="margin-bottom: 0.15rem;">'
                f'<span class="ae-curador-chip">Contexto: {html.escape(tipo_identificado)}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if evidencia:
                st.caption(f"💡 {evidencia}")
            
            respostas = {}
            for idx, pergunta in enumerate(perguntas, start=1):
                st.markdown(f'<div class="ae-curador-question"><strong>{idx}. {html.escape(pergunta)}</strong>', unsafe_allow_html=True)
                respostas[pergunta] = st.text_area(
                    "Resposta opcional",
                    key=f"{prefixo}resposta_{idx}",
                    label_visibility="collapsed",
                    placeholder="Escreva sua resposta aqui ou deixe em branco para pular...",
                    height=68,
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2, gap="small")
            with c1:
                gerar_narrativa = st.button("✨ Gerar narrativa final", key="curador_gerar_narrativa_btn", use_container_width=True)
            with c2:
                if st.button("← Voltar / Refazer", key="curador_reanalisar_btn", use_container_width=True):
                    st.session_state.pop(prefixo + "analise", None)
                    st.session_state[etapa_key] = "form"
                    st.rerun()

            if gerar_narrativa:
                if not assistente:
                    st.error("Curador indisponível no momento.")
                else:
                    with st.spinner("Gerando narrativa..."):
                        try:
                            narrativa = _curador_gerar_narrativa_com_ia(
                                assistente,
                                titulo_val,
                                conteudo_val,
                                data_memoria_val,
                                pessoas_relacionadas_val,
                                categoria_visual_val,
                                analise,
                                respostas,
                            )
                            st.session_state[prefixo + "respostas"] = respostas
                            st.session_state[prefixo + "narrativa"] = narrativa
                            st.session_state[etapa_key] = "final"
                            st.rerun()
                        except Exception as exc:
                            print("Erro ao gerar narrativa:", exc)
                            st.error("Não foi possível gerar a narrativa agora.")

        elif etapa == "final":
            analise = st.session_state.get(prefixo + "analise") or {}
            narrativa = st.session_state.get(prefixo + "narrativa") or {}
            respostas = st.session_state.get(prefixo + "respostas") or {}
            conteudo_salvo = _curador_montar_conteudo_salvo(narrativa, analise, respostas, conteudo_val)
            
            st.markdown('<div class="ae-curador-section-title">📖 Narrativa final sugerida</div>', unsafe_allow_html=True)
            narrativa_editada = st.text_area(
                "Revise e edite a narrativa antes de salvar:",
                value=conteudo_salvo,
                key=prefixo + "narrativa_editada",
                height=260,
            )
            
            st.markdown('<div class="ae-curador-analysis">', unsafe_allow_html=True)
            st.markdown(f'<span class="ae-curador-chip">Tipo: {html.escape(analise.get("tipo") or "Outro")}</span>', unsafe_allow_html=True)
            for valor in (narrativa.get("valores_percebidos") or [])[:8]:
                st.markdown(f'<span class="ae-curador-chip">{html.escape(valor)}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2, gap="small")
            with c1:
                salvar_final = st.button("💾 Salvar em minha história", key="curador_salvar_final_btn", use_container_width=True)
            with c2:
                if st.button("← Voltar para perguntas", key="curador_voltar_perguntas_btn", use_container_width=True):
                    st.session_state[etapa_key] = "perguntas"
                    st.rerun()

            if salvar_final:
                if st.session_state.get(prefixo + "memoria_id"):
                    st.warning("Esta memória já foi salva.")
                else:
                    try:
                        visibilidade_final = "seletivo" if (compartilhar_val and contatos_selecionados_ids) else ("contatos" if compartilhar_val else "privado")
                        contatos_ids_final = contatos_selecionados_ids if visibilidade_final == "seletivo" else []
                        memoria_id = db.salvar_memoria(
                            usuario_id=usuario_id,
                            conteudo=narrativa_editada.strip(),
                            titulo=titulo_val or "Memória sem título",
                            categoria=analise.get("tipo") or categoria_visual_val or "Outro",
                            origem="curador",
                            data_evento=data_memoria_val if data_memoria_val else None,
                            pessoas_relacionadas=", ".join(pessoas_relacionadas_val) if pessoas_relacionadas_val else None,
                            visibilidade=visibilidade_final,
                            contatos_ids=contatos_ids_final,
                        )
                        if foto_memoria_val:
                            upload_foto = storage.upload_streamlit_file("fotos", foto_memoria_val, usuario_id, "memorias")
                            foto_id = db.adicionar_foto_com_acesso(usuario_id, titulo_val or "Foto da memória", narrativa_editada.strip()[:300], analise.get("tipo") or categoria_visual_val, upload_foto["url"], contatos_ids_final, visibilidade_final)
                            db.associar_foto_memoria(memoria_id=memoria_id, foto_id=foto_id)
                        if video_memoria_val:
                            upload_video = storage.upload_streamlit_file("videos", video_memoria_val, usuario_id, "memorias")
                            video_id = db.adicionar_video_com_acesso(usuario_id, titulo_val or "Vídeo da memória", ", ".join(pessoas_relacionadas_val), upload_video["url"], contatos_ids_final, analise.get("tipo") or categoria_visual_val, visibilidade_final)
                            db.associar_video_memoria(memoria_id=memoria_id, video_id=video_id)
                        st.session_state[prefixo + "memoria_id"] = memoria_id
                        st.session_state[etapa_key] = "salvo"
                        st.rerun()
                    except Exception as exc:
                        print("Erro ao salvar narrativa final:", exc)
                        st.error("Não foi possível salvar a memória agora.")

        elif etapa == "salvo":
            st.balloons()
            st.success("🎉 Memória salva com sucesso na sua coleção viva!")
            st.markdown("""
            <div class="ae-curador-instructions">
                <h3>O que você deseja fazer agora?</h3>
                <div class="ae-curador-inst-step">
                    <span class="ae-curador-inst-icon">✍️</span>
                    <div>
                        <strong>Registrar outra lembrança</strong>
                        <span>Selecione a opção de criar outra memória para continuar registrando novos momentos da sua jornada.</span>
                    </div>
                </div>
                <div class="ae-curador-inst-step">
                    <span class="ae-curador-inst-icon">📖</span>
                    <div>
                        <strong>Ver sua coleção viva</strong>
                        <span>Navegue para sua prateleira para ler, reviver e compartilhar suas memórias e legados salvos.</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2, gap="small")
            with c1:
                if st.button("✍️ Registrar outra memória", key="curador_nova_memoria_btn", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith(prefixo):
                            del st.session_state[key]
                    st.rerun()
            with c2:
                if st.button("📖 Ver Minha História", key="curador_ver_historia_btn", use_container_width=True):
                    st.session_state.pagina_atual = "minha_historia"
                    st.rerun()

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
