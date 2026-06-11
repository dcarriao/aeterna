import html
import streamlit as st
from utils.assistente_ia import AssistenteLuto


def _safe_text(value: str) -> str:
    return html.escape(str(value or "")).replace("\n", "<br>")


def aplicar_css_chat_luto():
    st.markdown("""
<style>
.ae-memory-card {
    background: linear-gradient(135deg, #1b0f2e 0%, #32184f 58%, #8a5a2b 100%);
    color: white;
    border-radius: 28px;
    padding: 28px;
    min-height: 560px;
    box-shadow: 0 22px 70px rgba(27, 15, 46, 0.22);
    border: 1px solid rgba(212, 175, 55, 0.28);
}
.ae-memory-card h2 {
    font-size: 1.9rem;
    margin-bottom: 0.8rem;
    color: #f2c572;
}
.ae-memory-card p {
    color: rgba(255,255,255,0.86);
    line-height: 1.65;
    font-size: 0.98rem;
}
.ae-memory-separator {
    height: 1px;
    background: linear-gradient(90deg, rgba(242,197,114,0.65), rgba(242,197,114,0.12));
    margin: 1.5rem 0 1.2rem;
}
.ae-memory-feature {
    display: grid;
    grid-template-columns: 54px 1fr;
    gap: 14px;
    align-items: center;
    margin: 15px 0;
}
.ae-memory-icon {
    width: 54px;
    height: 54px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    background: rgba(255,255,255,0.12);
    color: white;
    font-size: 1.35rem;
}
.ae-memory-feature strong {
    color: #f2c572;
    display: block;
    font-size: 1.02rem;
    margin-bottom: 2px;
}
.ae-memory-feature span {
    color: rgba(255,255,255,0.84);
    font-size: 0.92rem;
}
.ae-suggestion-box {
    margin-top: 1.7rem;
    padding: 18px;
    border-radius: 18px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(242,197,114,0.38);
}
.ae-suggestion-box strong {
    color: #f2c572;
}
.ae-suggestion-box ul {
    margin: 0.55rem 0 0 1.15rem;
    color: rgba(255,255,255,0.88);
}
.ae-chat-shell {
    background: #130322;
    border-radius: 28px;
    padding: 12px;
    border: 1px solid rgba(212,175,55,0.32);
    box-shadow: 0 22px 70px rgba(0,0,0,0.25);
    max-width: 520px;
    margin-left: auto;
}
.ae-chat-header {
    background: linear-gradient(135deg, #1b0f2e, #3b1d5c);
    border-radius: 22px 22px 0 0;
    color: white;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(212,175,55,0.28);
}
.ae-chat-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #f2c572, #b77a46);
    color: #1b0f2e;
    font-weight: 900;
    font-size: 1.15rem;
    flex: 0 0 auto;
}
.ae-chat-title {
    font-weight: 900;
    font-size: 0.96rem;
    line-height: 1.1;
}
.ae-chat-subtitle {
    color: rgba(255,255,255,0.64);
    font-size: 0.75rem;
    margin-top: 3px;
}
.ae-chat-body {
    height: 430px;
    overflow-y: auto;
    padding: 18px 14px;
    background:
        radial-gradient(circle at 15% 20%, rgba(242,197,114,0.10), transparent 25%),
        radial-gradient(circle at 90% 80%, rgba(74,38,110,0.16), transparent 28%),
        #efe5db;
}
.ae-message-row {
    display: flex;
    width: 100%;
    margin: 0 0 12px;
}
.ae-message-row.user { justify-content: flex-end; }
.ae-message-row.bot { justify-content: flex-start; }
.ae-message-bubble {
    max-width: 82%;
    padding: 11px 13px;
    border-radius: 18px;
    font-size: 0.91rem;
    line-height: 1.45;
    box-shadow: 0 5px 16px rgba(0,0,0,0.07);
    word-wrap: break-word;
}
.ae-message-bubble.user {
    background: linear-gradient(135deg, #4a266e, #2b1747);
    color: white;
    border-bottom-right-radius: 5px;
}
.ae-message-bubble.bot {
    background: white;
    color: #24182d;
    border-bottom-left-radius: 5px;
    border: 1px solid rgba(0,0,0,0.04);
}
.ae-chat-warning {
    background: #fff6dd;
    color: #6d4a14;
    font-size: 0.72rem;
    padding: 8px 12px;
    text-align: center;
    border-top: 1px solid #ead9b6;
}
.ae-input-label {
    color: #3b1d5c;
    font-size: 0.78rem;
    font-weight: 800;
    margin: 10px 0 4px;
}
div[data-testid="stForm"] {
    border: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}
@media (max-width: 900px) {
    .ae-memory-card { min-height: auto; margin-bottom: 1rem; }
    .ae-chat-shell { max-width: 100%; margin-left: 0; }
    .ae-chat-body { height: 360px; }
}
</style>
""", unsafe_allow_html=True)


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
                f"Olá. Este é um espaço de memória e acolhimento baseado no legado de {nome}. "
                "Você pode falar sobre saudade, lembranças, conselhos ou momentos importantes."
            )
        })


def _render_mensagens():
    partes = ['<div class="ae-chat-body" id="ae-chat-body">']

    for msg in st.session_state.historico_assistente:
        tipo = "user" if msg.get("tipo") == "user" else "bot"
        texto = _safe_text(msg.get("texto", ""))

        partes.append(
            f'<div class="ae-message-row {tipo}">'
            f'<div class="ae-message-bubble {tipo}">{texto}</div>'
            f'</div>'
        )

    partes.append("</div>")
    st.markdown("".join(partes), unsafe_allow_html=True)


def _render_card_esquerdo(nome_referencia: str):
    nome = _safe_text(nome_referencia)

    html_card = (
        '<div class="ae-memory-card">'
        '<h2>Assistente de Memória</h2>'
        '<p>Um espaço reservado para conversar com acolhimento sobre lembranças, saudade, ensinamentos e histórias ligadas a '
        f'<strong style="color:#f2c572;">{nome}</strong>.</p>'
        '<p>A proposta não é substituir uma pessoa nem apoio psicológico, mas ajudar a preservar presença, contexto, valores e memórias.</p>'
        '<div class="ae-memory-separator"></div>'
        '<div class="ae-memory-feature"><div class="ae-memory-icon">💬</div><div><strong>Conversa acolhedora</strong><span>Fale sobre saudade, emoções, lembranças e momentos importantes.</span></div></div>'
        '<div class="ae-memory-feature"><div class="ae-memory-icon">🕊️</div><div><strong>Memórias e saudade</strong><span>Reviva histórias, recordações e ensinamentos que marcaram sua vida.</span></div></div>'
        '<div class="ae-memory-feature"><div class="ae-memory-icon">✨</div><div><strong>Legado familiar</strong><span>Preserve valores, conselhos e caminhos que você deseja manter vivos.</span></div></div>'
        '<div class="ae-memory-feature"><div class="ae-memory-icon">🔒</div><div><strong>Uso privado</strong><span>Suas conversas são pessoais e devem ser tratadas com cuidado.</span></div></div>'
        '<div class="ae-suggestion-box"><strong>💡 Sugestões para começar:</strong>'
        '<ul>'
        '<li>Estou sentindo saudade hoje.</li>'
        '<li>Qual conselho combinaria com este momento?</li>'
        '<li>Me ajude a lembrar de uma história importante.</li>'
        '<li>Quero registrar uma mensagem para minha família.</li>'
        '</ul></div>'
        '</div>'
    )

    st.markdown(html_card, unsafe_allow_html=True)


def render_chat_luto():
    aplicar_css_chat_luto()
    _inicializar_chat()

    nome_referencia = _obter_nome_referencia()

    col_info, col_chat = st.columns([1.08, 0.92], gap="large")

    with col_info:
        _render_card_esquerdo(nome_referencia)

    with col_chat:
        st.markdown('<div class="ae-chat-shell">', unsafe_allow_html=True)

        st.markdown("""
<div class="ae-chat-header">
    <div class="ae-chat-avatar">💜</div>
    <div>
        <div class="ae-chat-title">Assistente aEterna</div>
        <div class="ae-chat-subtitle">Memória, legado e acolhimento</div>
    </div>
</div>
""", unsafe_allow_html=True)

        _render_mensagens()

        st.markdown(
            '<div class="ae-chat-warning">Este assistente não substitui psicólogo, terapeuta ou atendimento de emergência.</div>',
            unsafe_allow_html=True,
        )

        with st.form("form_assistente_luto", clear_on_submit=True):
            st.markdown('<div class="ae-input-label">Digite sua mensagem</div>', unsafe_allow_html=True)
            mensagem = st.text_area(
                "Mensagem",
                placeholder="Escreva aqui...",
                height=82,
                label_visibility="collapsed",
                key="mensagem_assistente_luto",
            )

            col_send, col_clear = st.columns([0.72, 0.28])

            with col_send:
                enviar = st.form_submit_button("Enviar mensagem", use_container_width=True, type="primary")

            with col_clear:
                limpar = st.form_submit_button("Limpar", use_container_width=True)

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
