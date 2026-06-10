import streamlit as st
from utils.assistente_ia import AssistenteLuto

def render_chat_luto():
    nome_falecido = st.session_state.usuario_atual.get("nome_completo", "seu ente querido")

    if "historico_assistente" not in st.session_state:
        st.session_state.historico_assistente = []

    if "assistente_obj" not in st.session_state:
        st.session_state.assistente_obj = AssistenteLuto(st.session_state.falecido_id)

    if not st.session_state.historico_assistente:
        st.session_state.historico_assistente.append({
            "tipo": "bot",
            "texto": f"Olá. Este é um espaço de acolhimento baseado nas memórias de {nome_falecido}."
        })

    col_info, col_chat = st.columns([1.4, 1])

    with col_info:
        st.markdown("### Assistente de Luto")
        st.write("""
        Este espaço foi criado para apoiar conversas de memória, saudade e continuidade.
        Ele não substitui apoio psicológico, mas pode ajudar a preservar lembranças e mensagens.
        """)

    with col_chat:
        st.markdown(f"### Conversar com {nome_falecido}")

        st.markdown('<div class="chat-box">', unsafe_allow_html=True)

        for msg in st.session_state.historico_assistente:
            classe = "msg-user" if msg["tipo"] == "user" else "msg-bot"
            st.markdown(
                f'<div class="{classe}">{msg["texto"]}</div>',
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            mensagem = st.text_input(
                "Mensagem",
                placeholder="Digite sua mensagem...",
                label_visibility="collapsed"
            )
            enviar = st.form_submit_button("Enviar", use_container_width=True)

        if enviar and mensagem:
            st.session_state.historico_assistente.append({"tipo": "user", "texto": mensagem})
            resposta = st.session_state.assistente_obj.conversar(mensagem)
            st.session_state.historico_assistente.append({"tipo": "bot", "texto": resposta})
            st.rerun()