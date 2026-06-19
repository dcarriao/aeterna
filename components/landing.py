import streamlit as st

def render_landing():
    st.markdown("""
    <section class="ae-hero">
        <div class="ae-title">Suas histórias, seus momentos e seus aprendizados com quem você ama.</div>
        <div class="ae-subtitle">
            A aEterna ajuda você a preservar memórias, orientações, vídeos, documentos
            e mensagens importantes para que sua história continue presente.
        </div>
    </section>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="ae-card">
            <h3>Mensagens para o futuro</h3>
            <p>Deixe vídeos, cartas e orientações para familiares e pessoas especiais.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="ae-card">
            <h3>Cofre digital</h3>
            <p>Organize informações importantes, contatos de confiança e documentos.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="ae-card">
            <h3>Curador de Histórias</h3>
            <p>Um espaço acolhedor para registrar memórias com perguntas simples.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Como funciona")
    st.write("""
    1. Você cria sua conta.
    2. Cadastra contatos de confiança.
    3. Registra mensagens, vídeos e orientações.
    4. Define quem poderá acessar cada conteúdo no momento certo.
    """)

    st.markdown("### Comece em beta")
    st.write("A versão beta está aberta para testes e melhorias antes do lançamento pago.")
