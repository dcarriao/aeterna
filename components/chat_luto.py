import html
import streamlit as st
from utils.assistente_ia import AssistenteLuto
from utils.banco import BancoDados


def _safe_text(value: str) -> str:
    return html.escape(str(value or "")).replace("\n", "<br>")


def render_chat_luto():
    _inicializar_chat()
    db = BancoDados()
    db.migrar_memoria()

    nome_referencia = _obter_nome_referencia()

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

    st.markdown("## Assistente de Legado")
    if st.session_state.get("ultimo_erro_openai"):
        st.error(f"Erro OpenAI: {st.session_state['ultimo_erro_openai']}")
    st.markdown(
        """
    Este espaço existe para ajudar a construir e preservar o seu legado digital.

    Você pode conversar livremente sobre qualquer assunto que desejar.

    Também posso sugerir temas importantes para registrar histórias, valores, aprendizados, conselhos e lembranças que poderão ajudar sua família e pessoas queridas no futuro.

    ### 💡 Sugestões de conversa

    • Minha infância

    • Minha família

    • Como conheci meu amor

    • Meus filhos

    • Minha carreira

    • Meus maiores aprendizados

    • Sonhos realizados

    • Momentos difíceis que superei

    • Conselhos para o futuro

    • Histórias engraçadas
    """
    )

    historico = st.session_state.get("historico_assistente", [])

    if not historico:
        historico = [{
            "tipo": "bot",
            "texto": f"Olá. Este é um espaço de criação de Histórias, valores e ensinamentos para o futuro de {nome_referencia}. Você pode falar sobre saudade, lembranças, conselhos ou momentos importantes."
        }]

    for msg in historico:
        tipo = msg.get("tipo", "bot")
        texto = html.escape(msg.get("texto", "")).replace("\n", "<br>")

        if tipo == "user":
            st.markdown(
                f'<div class="ae-simple-bubble-user">{texto}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="ae-simple-bubble-bot">{texto}</div>',
                unsafe_allow_html=True
            )
            if len(texto) > 80:
                if st.button(
                        "💾 Salvar como memória",
                        key="salvar_{hash(texto)}"
                ):
                    usuario = st.session_state.get("usuario_atual")
                    db.salvar_memoria(usuario["id"], texto)
                    st.success("Memória salva no legado.")

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
            resposta = st.session_state.assistente_obj.conversar(mensagem.strip())
        except Exception as exc:
            resposta = (
                "Desculpe, tive uma dificuldade para responder agora. "
                "Tente novamente em alguns instantes."
            )
            st.error(f"Erro no assistente: {exc}")

        st.session_state.historico_assistente.append({
            "tipo": "bot",
            "texto": resposta,
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

    return usuario.get("nome_completo") or "seu legado"


def _inicializar_chat():
    if "historico_assistente" not in st.session_state:
        st.session_state.historico_assistente = []

    if "assistente_obj" not in st.session_state:
        st.session_state.assistente_obj = AssistenteLuto(st.session_state.falecido_id)

    if not st.session_state.historico_assistente:
        nome = _obter_nome_referencia()
        st.session_state.historico_assistente.append({
            "tipo": "bot",
            "texto": (
                "Olá. Este é o seu Assistente de Legado.\n\n"
                "Estou aqui para ajudar a preservar histórias, valores, aprendizados e lembranças importantes da sua vida.\n\n"
                "Você pode conversar livremente sobre qualquer assunto ou utilizar as sugestões de temas para construir um legado mais rico para sua família e pessoas queridas."
            )
        })
