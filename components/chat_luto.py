import html
import streamlit as st

from utils.assistente_ia import AssistenteLuto
from utils.banco import BancoDados


def _safe_text(value: str) -> str:
    return html.escape(str(value or "")).replace("\n", "<br>")


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
        nome_falecido = usuario.get("nome_falecido", "essa pessoa especial")
        nome_visitante = usuario.get("nome", "você")
        parentesco = usuario.get("parentesco", "")

        st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #2b1747 0%, #6f4e37 100%);
                        color: white;
                        padding: 32px;
                        border-radius: 24px;
                        margin-bottom: 24px;
                        box-shadow: 0 20px 60px rgba(43, 23, 71, 0.25);
                    ">
                        <h1 style="color: #f2c572; margin-bottom: 12px;">🕊️ Memorial de {nome_falecido}</h1>
                        <p style="font-size: 1.1rem; line-height: 1.6;">
                            {nome_visitante}, este é um espaço para conversar com o legado de {nome_falecido}.
                        </p>
                        <p style="font-size: 1rem; opacity: 0.92;">
                            O Assistente Memorial usa memórias, valores, histórias e mensagens registradas para acolher,
                            responder perguntas, ajudar em momentos de saudade e preservar a presença simbólica de quem foi importante.
                        </p>
                        <p style="font-size: 0.88rem; opacity: 0.78;">
                            Ele não substitui a pessoa, não inventa lembranças e não responde fora do que foi preservado.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
                    ### 💬 💬 Se não souber por onde começar...

                    • Estou com saudade.
                    • Quero lembrar momentos especiais.
                    • Preciso conversar um pouco.
                    • O que essa pessoa valorizava na vida?
                    • Existem mensagens ou conselhos registrados?
                    • Como ela enxergava a família e os relacionamentos?
                    • O que posso aprender com sua história?
                    • Quero compartilhar algo que aconteceu comigo hoje.
                    """)
        st.markdown("""
                    ---
                    ### ✨ Também quer criar seu próprio legado?

                    A aEterna permite que você preserve histórias, mensagens e orientações para pessoas que ama.
                    """)

        if st.button("✨ Criar meu próprio legado"):
            for key in [
                "autenticado",
                "usuario_atual",
                "modo_acesso",
                "falecido_id",
                "historico_assistente",
                "assistente_obj",
                "assistente_modo",
                "assistente_usuario_id",
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.autenticado = False
            st.session_state.login_mode = "cadastro"
            st.rerun()
    else:
        st.markdown("## Assistente de Legado")
        st.markdown("""
            Este espaço existe para ajudar a construir e preservar o seu legado digital.
        
            Você pode conversar livremente sobre qualquer assunto que desejar.
        
            Também posso sugerir temas importantes para registrar histórias, valores, aprendizados, conselhos e lembranças que poderão ajudar sua família e pessoas queridas no futuro.
            """)
        st.markdown(
            """

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

    if st.session_state.get("ultimo_erro_openai"):
        st.error(f"Erro OpenAI: {st.session_state['ultimo_erro_openai']}")


    historico = st.session_state.get("historico_assistente", [])

    if not historico:
        historico = [{
            "tipo": "bot",
            "texto": "Olá. Este é um espaço de criação de Histórias, valores e ensinamentos para o futuro de {nome_referencia}. Você pode falar sobre saudade, lembranças, conselhos ou momentos importantes."
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
                if st.button(
                        "💾 Salvar como memória",
                        key="salvar_memoria_user_{}_{}".format(i, abs(hash(texto_original)))
                ):
                    usuario = st.session_state.get("usuario_atual")
                    db.salvar_memoria(usuario["id"], texto_original)
                    st.success("Memória salva no legado.")

        else:
            st.markdown(
                '<div class="ae-simple-bubble-bot">{}</div>'.format(texto_html),
                unsafe_allow_html=True
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
                    "A pessoa que está acessando o memorial se chama {}. "
                    "Ela está registrada como {} de {}."
                ).format(
                    usuario.get("nome", "Visitante"),
                    usuario.get("parentesco", "relação não informada"),
                    usuario.get("nome_falecido", "a pessoa memorializada")
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
    ):
        st.session_state.assistente_obj = AssistenteLuto(
            usuario_id_referencia,
            modo=modo
        )
        st.session_state.assistente_modo = modo
        st.session_state.assistente_usuario_id = usuario_id_referencia

    if not st.session_state.historico_assistente:
        if modo == "memorial":
            st.session_state.historico_assistente.append({
                "tipo": "bot",
                "texto": (
                    "Olá. Este é o seu Assistente Memorial.\n\n"
                    "Estou aqui para ajudar você a se conectar com seu ente querido."
                )
            })
        else:
            st.session_state.historico_assistente.append({
                "tipo": "bot",
                "texto": (
                    "Olá. Este é o seu Assistente de Legado.\n\n"
                    "Estou aqui para ajudar a preservar histórias, valores, aprendizados e lembranças importantes da sua vida."
                )
            })
