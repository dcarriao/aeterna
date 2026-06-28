import html
import streamlit as st
import os
import json
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
    if len(perguntas) < 4:
        raise ValueError("A IA não retornou perguntas suficientes para o Curador.")
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
    .main .block-container,
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 0.25rem !important;
        padding-bottom: 0.75rem !important;
        max-width: 980px !important;
        width: min(980px, calc(100vw - 260px)) !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    .ae-curador-mobile-wrap {
        max-width: 780px;
        margin: 0 auto;
    }
    .ae-curador-mobile-title {
        color: #2B1747;
        font-size: 1.78rem;
        line-height: 1.05;
        font-weight: 950;
        margin: 0 0 0.25rem;
        letter-spacing: -0.03em;
    }
    .ae-curador-mobile-subtitle {
        color: #6f6478;
        font-size: 0.92rem;
        margin: 0 0 0.85rem;
    }
    .ae-curador-card {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(212,168,79,0.24);
        border-radius: 22px;
        padding: 1rem;
        box-shadow: 0 12px 34px rgba(43,23,71,0.06);
        margin-bottom: 0.85rem;
    }
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
        margin: 0.35rem 0 0.1rem;
    }
    .ae-curador-chip {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.34rem 0.62rem;
        background: rgba(244,238,252,0.92);
        border: 1px solid rgba(193,177,231,0.72);
        color: #4f2476;
        font-size: 0.78rem;
        font-weight: 850;
    }
    .ae-curador-question {
        border: 1px solid rgba(193,177,231,0.72);
        border-radius: 18px;
        background: rgba(255,255,255,0.78);
        padding: 0.85rem;
        margin-bottom: 0.72rem;
    }
    .ae-curador-question strong {
        color: #2B1747;
        display: block;
        margin-bottom: 0.35rem;
    }
    .ae-curador-final-text {
        color: #2B1747;
        line-height: 1.58;
        font-size: 0.96rem;
        background: rgba(255,250,241,0.92);
        border: 1px solid rgba(212,168,79,0.26);
        border-radius: 18px;
        padding: 1rem;
    }
    .st-key-curador_aprofundar_btn button,
    .st-key-curador_salvar_final_btn button,
    .st-key-curador_salvar_direto_btn button {
        background: #2B1747 !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 950 !important;
        min-height: 3rem !important;
    }
    .st-key-curador_gerar_narrativa_btn button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 950 !important;
        min-height: 3rem !important;
    }
    .st-key-curador_nova_memoria_btn button,
    .st-key-curador_reanalisar_btn button {
        border-radius: 14px !important;
        font-weight: 900 !important;
        min-height: 2.7rem !important;
    }
    .ae-curador-mobile-wrap input,
    .ae-curador-mobile-wrap textarea {
        font-size: 16px !important;
    }
    @media (max-width: 768px) {
        .main .block-container,
        .block-container,
        [data-testid="stMainBlockContainer"] {
            width: 100% !important;
            max-width: 100% !important;
            padding: 0.55rem 1rem 5rem !important;
        }
        .ae-curador-card { padding: 0.85rem; border-radius: 18px; }
        .ae-curador-mobile-title { font-size: 1.48rem; }
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

    st.markdown('<div class="ae-curador-mobile-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="ae-curador-mobile-title">Nova memória</div>'
        '<div class="ae-curador-mobile-subtitle">Escreva primeiro. Depois aprofunde a história com perguntas adequadas ao contexto.</div>',
        unsafe_allow_html=True,
    )

    etapa = st.session_state.get(etapa_key, "form")

    if etapa == "salvo":
        st.success("Memória salva.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Criar outra memória", key="curador_nova_memoria_btn", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith(prefixo):
                        del st.session_state[key]
                st.rerun()
        with c2:
            if st.button("Ver em Minha História", key="curador_ver_historia_btn", use_container_width=True):
                st.session_state.pagina_atual = "minha_historia"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    with st.container():
        st.markdown('<div class="ae-curador-card">', unsafe_allow_html=True)
        titulo = st.text_input("Título", key=prefixo + "titulo", placeholder="Título")
        data_memoria = st.date_input(
            "Data da memória",
            key=prefixo + "data",
            value=None,
            format="DD/MM/YYYY",
        )
        categoria_visual = st.selectbox(
            "Categoria",
            ["Momentos", "Família", "Viagens", "Infância", "Trabalho", "Aprendizados", "Conquistas", "Outro"],
            key=prefixo + "categoria_visual",
        )
        compartilhar = st.toggle("Compartilhar com familiares", key=prefixo + "compartilhar", value=False)
        pessoas_relacionadas = st.multiselect(
            "Quem participou deste momento?",
            options=nomes_contatos,
            key=prefixo + "pessoas",
            placeholder="Adicionar pessoas",
        )
        conteudo = st.text_area(
            "O que aconteceu?",
            key=prefixo + "conteudo",
            placeholder="O que aconteceu?",
            height=170,
        )
        with st.expander("Adicionar foto ou vídeo", expanded=False):
            c_foto, c_video = st.columns(2)
            with c_foto:
                foto_memoria = st.file_uploader(
                    "Foto",
                    type=["png", "jpg", "jpeg", "webp"],
                    key=prefixo + "foto",
                )
            with c_video:
                video_memoria = st.file_uploader(
                    "Vídeo",
                    type=["mp4", "mov", "avi", "mkv"],
                    key=prefixo + "video",
                )
        c1, c2 = st.columns([1, 1])
        with c1:
            aprofundar = st.button("Aprofundar esta história", key="curador_aprofundar_btn", use_container_width=True)
        with c2:
            salvar_direto = st.button("Salvar memória", key="curador_salvar_direto_btn", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if aprofundar:
        if not titulo.strip() and not conteudo.strip():
            st.warning("Escreva um título ou uma memória antes de aprofundar.")
        elif not assistente:
            st.error("Curador indisponível no momento.")
        else:
            with st.spinner("Analisando a memória..."):
                try:
                    analise = _curador_analisar_memoria_com_ia(
                        assistente,
                        titulo,
                        conteudo,
                        data_memoria,
                        pessoas_relacionadas,
                        categoria_visual,
                    )
                    st.session_state[prefixo + "analise"] = analise
                    st.session_state[etapa_key] = "perguntas"
                    st.rerun()
                except Exception as exc:
                    print("Erro ao analisar memória com IA:", exc)
                    st.error("Não foi possível gerar perguntas contextualizadas agora.")

    if salvar_direto:
        if st.session_state.get(prefixo + "salvando"):
            st.warning("Esta memória já está sendo salva.")
        elif not conteudo.strip():
            st.warning("Escreva a memória antes de salvar.")
        else:
            st.session_state[prefixo + "salvando"] = True
            try:
                memoria_id = db.salvar_memoria(
                    usuario_id=usuario_id,
                    conteudo=conteudo.strip(),
                    titulo=titulo.strip() or "Memória sem título",
                    categoria=categoria_visual,
                    origem="curador",
                    data_evento=data_memoria.strftime("%Y-%m-%d") if data_memoria else None,
                    pessoas_relacionadas=", ".join(pessoas_relacionadas) if pessoas_relacionadas else None,
                    visibilidade="contatos" if compartilhar else "privado",
                    contatos_ids=[],
                )
                if foto_memoria:
                    upload_foto = storage.upload_streamlit_file("fotos", foto_memoria, usuario_id, "memorias")
                    foto_id = db.adicionar_foto_com_acesso(usuario_id, titulo.strip() or "Foto da memória", conteudo.strip()[:300], categoria_visual, upload_foto["url"], [], "contatos" if compartilhar else "privado")
                    db.associar_foto_memoria(memoria_id=memoria_id, foto_id=foto_id)
                if video_memoria:
                    upload_video = storage.upload_streamlit_file("videos", video_memoria, usuario_id, "memorias")
                    video_id = db.adicionar_video_com_acesso(usuario_id, titulo.strip() or "Vídeo da memória", ", ".join(pessoas_relacionadas), upload_video["url"], [], categoria_visual, "contatos" if compartilhar else "privado")
                    db.associar_video_memoria(memoria_id=memoria_id, video_id=video_id)
                st.session_state[prefixo + "memoria_id"] = memoria_id
                st.session_state[etapa_key] = "salvo"
                st.rerun()
            except Exception as exc:
                st.session_state[prefixo + "salvando"] = False
                print("Erro ao salvar memória:", exc)
                st.error("Não foi possível salvar a memória agora.")

    if etapa == "perguntas":
        analise = st.session_state.get(prefixo + "analise") or {}
        perguntas = analise.get("perguntas") or []
        st.markdown('<div class="ae-curador-card">', unsafe_allow_html=True)
        st.markdown('<div class="ae-curador-section-title">Aprofundar esta história</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="ae-curador-chip">Tipo: {html.escape(analise.get("tipo") or "Outro")}</span>',
            unsafe_allow_html=True,
        )
        if analise.get("evidencia_tipo"):
            st.caption(analise.get("evidencia_tipo"))
        respostas = {}
        for idx, pergunta in enumerate(perguntas, start=1):
            st.markdown(f'<div class="ae-curador-question"><strong>{idx}. {html.escape(pergunta)}</strong>', unsafe_allow_html=True)
            respostas[pergunta] = st.text_area(
                "Resposta opcional",
                key=f"{prefixo}resposta_{idx}",
                label_visibility="collapsed",
                placeholder="Responder ou deixar em branco para pular",
                height=92,
            )
            st.markdown('</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            gerar_narrativa = st.button("Gerar narrativa", key="curador_gerar_narrativa_btn", use_container_width=True)
        with c2:
            if st.button("Refazer perguntas", key="curador_reanalisar_btn", use_container_width=True):
                st.session_state.pop(prefixo + "analise", None)
                st.session_state[etapa_key] = "form"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if gerar_narrativa:
            if not assistente:
                st.error("Curador indisponível no momento.")
            else:
                with st.spinner("Gerando narrativa..."):
                    try:
                        narrativa = _curador_gerar_narrativa_com_ia(
                            assistente,
                            titulo,
                            conteudo,
                            data_memoria,
                            pessoas_relacionadas,
                            categoria_visual,
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

    if etapa == "final":
        analise = st.session_state.get(prefixo + "analise") or {}
        narrativa = st.session_state.get(prefixo + "narrativa") or {}
        respostas = st.session_state.get(prefixo + "respostas") or {}
        conteudo_salvo = _curador_montar_conteudo_salvo(narrativa, analise, respostas, conteudo)
        st.markdown('<div class="ae-curador-card">', unsafe_allow_html=True)
        st.markdown('<div class="ae-curador-section-title">Narrativa final</div>', unsafe_allow_html=True)
        narrativa_editada = st.text_area(
            "Revise antes de salvar",
            value=conteudo_salvo,
            key=prefixo + "narrativa_editada",
            height=320,
        )
        st.markdown('<div class="ae-curador-analysis">', unsafe_allow_html=True)
        st.markdown(f'<span class="ae-curador-chip">Tipo: {html.escape(analise.get("tipo") or "Outro")}</span>', unsafe_allow_html=True)
        for valor in (narrativa.get("valores_percebidos") or [])[:8]:
            st.markdown(f'<span class="ae-curador-chip">{html.escape(valor)}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        salvar_final = st.button("Salvar memória", key="curador_salvar_final_btn", use_container_width=True, disabled=bool(st.session_state.get(prefixo + "memoria_id")))
        st.markdown('</div>', unsafe_allow_html=True)

        if salvar_final:
            if st.session_state.get(prefixo + "memoria_id"):
                st.warning("Esta memória já foi salva.")
            else:
                try:
                    memoria_id = db.salvar_memoria(
                        usuario_id=usuario_id,
                        conteudo=narrativa_editada.strip(),
                        titulo=titulo.strip() or "Memória sem título",
                        categoria=analise.get("tipo") or categoria_visual or "Outro",
                        origem="curador",
                        data_evento=data_memoria.strftime("%Y-%m-%d") if data_memoria else None,
                        pessoas_relacionadas=", ".join(pessoas_relacionadas) if pessoas_relacionadas else None,
                        visibilidade="contatos" if compartilhar else "privado",
                        contatos_ids=[],
                    )
                    if foto_memoria:
                        upload_foto = storage.upload_streamlit_file("fotos", foto_memoria, usuario_id, "memorias")
                        foto_id = db.adicionar_foto_com_acesso(usuario_id, titulo.strip() or "Foto da memória", narrativa_editada.strip()[:300], analise.get("tipo") or categoria_visual, upload_foto["url"], [], "contatos" if compartilhar else "privado")
                        db.associar_foto_memoria(memoria_id=memoria_id, foto_id=foto_id)
                    if video_memoria:
                        upload_video = storage.upload_streamlit_file("videos", video_memoria, usuario_id, "memorias")
                        video_id = db.adicionar_video_com_acesso(usuario_id, titulo.strip() or "Vídeo da memória", ", ".join(pessoas_relacionadas), upload_video["url"], [], analise.get("tipo") or categoria_visual, "contatos" if compartilhar else "privado")
                        db.associar_video_memoria(memoria_id=memoria_id, video_id=video_id)
                    st.session_state[prefixo + "memoria_id"] = memoria_id
                    st.session_state[etapa_key] = "salvo"
                    st.rerun()
                except Exception as exc:
                    print("Erro ao salvar narrativa final:", exc)
                    st.error("Não foi possível salvar a memória agora.")

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
