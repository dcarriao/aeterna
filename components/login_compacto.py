import streamlit as st
import sqlite3
from pathlib import Path
from components.legal_texts import (
    TERMOS_USO,
    POLITICA_PRIVACIDADE,
    CONSENTIMENTO_LGPD,
)
from datetime import date


def _salvar_consentimento_usuario(email):
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "dados" / "cofre.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()

    if row:
        usuario_id = row[0]

        cursor.execute("""
            INSERT INTO consentimentos (
                usuario_id,
                aceite_termos,
                aceite_privacidade,
                aceite_lgpd,
                versao_termos,
                versao_privacidade
            )
            VALUES (?, 1, 1, 1, '1.0', '1.0')
        """, (usuario_id,))

        conn.commit()

    conn.close()


def _css_login_compacto():
    st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 20% 12%, rgba(74,38,110,0.36), transparent 28%),
        radial-gradient(circle at 82% 18%, rgba(212,175,55,0.18), transparent 26%),
        linear-gradient(180deg, #080014 0%, #120324 48%, #080014 100%);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.2rem !important;
}

.ae-login-header {
    text-align: center;
    margin-bottom: 0.45rem;
}

.ae-logo-text {
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 2.75rem;
    line-height: 1;
    font-style: italic;
    font-weight: 600;
    letter-spacing: -0.05em;
    color: #f2c572;
    text-shadow:
        0 6px 18px rgba(212,175,55,0.18),
        0 0 35px rgba(212,175,55,0.08);
}

.ae-logo-symbol {
    font-size: 2.15rem;
    font-style: normal;
    letter-spacing: -0.08em;
    margin-right: 0.18rem;
    color: #d4af37;
}

.ae-logo-subtitle {
    color: rgba(242,197,114,0.82);
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.18rem;
}

.ae-login-title {
    color: #ffffff;
}

.ae-login-subtitle {
    color: rgba(255,255,255,0.86);
}

.ae-login-mode-title {
    color: #1b0f2e;
}

div[data-testid="stForm"] label,
div[data-testid="stForm"] label p {
    color: #2b1845 !important;
}

.ae-login-footer {
    color: #6f6478;
    text-align: center;
    font-size: 0.82rem;
    margin-top: 0.85rem;
    padding-top: 0.85rem;
    border-top: 1px solid rgba(212,175,55,0.35);
}

.ae-login-secondary-block {
    margin-top: 0.85rem;
    padding: 0.82rem 1rem;
    border-radius: 20px 20px 0 0;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(212,175,55,0.20);
    border-bottom: 0;
}

.ae-login-secondary-title {
    color: #f2c572;
    text-align: center;
    font-weight: 900;
    font-size: 0.9rem;
    margin-bottom: 0.18rem;
}

.ae-login-secondary-text {
    color: rgba(255,255,255,0.84);
    text-align: center;
    font-size: 0.78rem;
    margin-bottom: 0.05rem;
}

div[data-testid="stForm"] {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(212,175,55,0.34);
    border-radius: 26px;
    padding: 1.25rem 1.45rem 1rem;
    box-shadow: 0 28px 90px rgba(0, 0, 0, 0.34);
}

div[data-testid="stForm"] label,
div[data-testid="stForm"] label p,
div[data-testid="stWidgetLabel"],
div[data-testid="stWidgetLabel"] p {
    color: #2b1845 !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stTextArea textarea {
    border-radius: 12px !important;
    color: #1b0f2e !important;
    background: #ffffff !important;
    border: 1px solid rgba(27, 15, 46, 0.35) !important;
}

input::placeholder,
textarea::placeholder {
    color: #8a7b95 !important;
    opacity: 1 !important;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] button,
button[data-testid*="baseButton"] {
    border-radius: 12px !important;
    font-weight: 900 !important;
    min-height: 2.65rem !important;
}

div[data-testid="stFormSubmitButton"] button,
button[data-testid="baseButton-primary"],
button[data-testid="stBaseButton-primary"],
div.stButton > button[kind="primary"],
button[kind="primary"] {
    background: linear-gradient(135deg, #f8dc92 0%, #d4af37 55%, #b77a46 100%) !important;
    color: #1b0f2e !important;
    border: none !important;
    font-weight: 900 !important;
    box-shadow: 0 8px 24px rgba(212,175,55,0.25) !important;
}

div.stButton > button,
button[data-testid="baseButton-secondary"],
button[data-testid="stBaseButton-secondary"],
button[kind="secondary"] {
    background: rgba(255,255,255,0.94) !important;
    color: #1b0f2e !important;
    border: 1px solid rgba(212,175,55,0.38) !important;
}

.ae-login-secondary-block + div button,
.ae-login-secondary-block + div [data-testid="baseButton-secondary"],
.ae-login-secondary-block + div [data-testid="stBaseButton-secondary"] {
    background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
    color: #1b0f2e !important;
    border: 0 !important;
}

@media (max-width: 768px) {
    .ae-login-title {
        color: #2b1747 !important;
        text-shadow: none !important;
    }

    .ae-login-subtitle {
        color: #4a3a66 !important;
        text-shadow: none !important;
    }
    
    .ae-login-secondary-title {
        color: #f2c572 !important;
    }
    
    .ae-login-secondary-text {
        color: rgba(255,255,255,0.92) !important;
    }
    
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] label p,
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] p {
        color: #2b1845 !important;
        opacity: 1 !important;
        font-weight: 800 !important;
    }
}
</style>
""", unsafe_allow_html=True)


def _set_mode(mode: str):
    st.session_state.login_mode = mode


def _render_logo():
    st.markdown("""
    <div class="ae-login-header">
        <div class="ae-logo-text"><span class="ae-logo-symbol">∞</span>aEterna</div>
        <div class="ae-logo-subtitle">Legados Digitais e Segurança Pós-Morte</div>
        <div class="ae-login-title">Bem-vindo à aEterna</div>
        <div class="ae-login-subtitle">
            Seu legado digital, suas mensagens e suas orientações em um espaço seguro.
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_login_principal(fazer_login):
    with st.form("login_form_compacto"):
        st.markdown('<div class="ae-login-mode-title">Acessar minha conta</div>', unsafe_allow_html=True)
        email = st.text_input("E-mail", key="login_email_compacto")
        senha = st.text_input("Senha", type="password", key="login_senha_compacto")
        submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")

        if submitted:
            if not email or not senha:
                st.error("Preencha e-mail e senha.")
            elif fazer_login(email, senha):
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

        st.markdown('<div class="ae-login-footer">Legados Digitais e Segurança Pós-Morte</div>', unsafe_allow_html=True)

    st.markdown('<div class="ae-login-secondary-block"><div class="ae-login-secondary-title">Novo por aqui?</div><div class="ae-login-secondary-text">Crie sua conta para começar seu legado digital.</div></div>', unsafe_allow_html=True)
    if st.button("Criar conta", use_container_width=True):
        _set_mode("cadastro")
        st.rerun()

    st.markdown('<div class="ae-login-secondary-block"><div class="ae-login-secondary-title">Recebeu uma chave?</div><div class="ae-login-secondary-text">Acesse um legado compartilhado com você.</div></div>', unsafe_allow_html=True)
    if st.button("Acessar legado com chave", use_container_width=True):
        _set_mode("visitante")
        st.rerun()


def _render_visitante(fazer_login_visitante):
    with st.form("visitante_form_compacto"):
        st.markdown('<div class="ae-login-mode-title">Acessar legado de alguém</div>', unsafe_allow_html=True)
        st.info("Use esta opção apenas se você recebeu uma chave de acesso autorizada.")
        nome_visitante = st.text_input("Seu nome", key="visitante_nome_compacto")
        email_falecido = st.text_input("E-mail da pessoa responsável pelo legado", key="visitante_email_compacto")
        chave = st.text_input("Chave de acesso", type="password", key="visitante_chave_compacto")
        submitted = st.form_submit_button("Acessar legado", use_container_width=True, type="primary")

        if submitted:
            if not nome_visitante or not email_falecido or not chave:
                st.error("Preencha todos os campos.")
            elif fazer_login_visitante(nome_visitante, chave, email_falecido):
                st.success(f"Bem-vindo(a), {nome_visitante}!")
                st.rerun()
            else:
                st.error("Credenciais inválidas.")

    if st.button("Voltar para login", use_container_width=True):
        _set_mode("login")
        st.rerun()


def _render_cadastro(fazer_cadastro):
    with st.form("cadastro_form_compacto"):
        st.markdown('<div class="ae-login-mode-title">Criar minha conta</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome *", key="cadastro_nome_compacto")
        with col2:
            sobrenome = st.text_input("Sobrenome *", key="cadastro_sobrenome_compacto")

        email = st.text_input("E-mail *", key="cadastro_email_compacto")
        cpf = st.text_input("CPF (11 números) *", key="cadastro_cpf_compacto", max_chars=11)
        data_nascimento = st.date_input("Data de nascimento *",
                                        key="cadastro_data_compacto",
                                        value=date(1990, 1, 1),
                                        min_value=date(1900, 1, 1),
                                        max_value=date.today(),
                                        format="DD/MM/YYYY")
        senha = st.text_input("Senha *", type="password", key="cadastro_senha_compacto")
        confirmar_senha = st.text_input("Confirmar senha *", type="password", key="cadastro_confirmar_compacto")

        with st.expander("Informações opcionais"):
            telefone = st.text_input("Telefone", key="cadastro_telefone_compacto")
            whatsapp = st.text_input("WhatsApp", key="cadastro_whatsapp_compacto")

        with st.expander("Termos de Uso"):
            st.markdown(TERMOS_USO)

        with st.expander("Política de Privacidade"):
            st.markdown(POLITICA_PRIVACIDADE)

        with st.expander("Consentimento LGPD"):
            st.markdown(CONSENTIMENTO_LGPD)

        aceite_termos = st.checkbox(
            "Li e aceito os Termos de Uso.",
            key="aceite_termos_cadastro"
        )

        aceite_privacidade = st.checkbox(
            "Li e aceito a Política de Privacidade.",
            key="aceite_privacidade_cadastro"
        )

        aceite_lgpd = st.checkbox(
            "Autorizo o tratamento dos meus dados pessoais conforme a LGPD.",
            key="aceite_lgpd_cadastro"
        )

        submitted = st.form_submit_button("Criar conta", use_container_width=True, type="primary")

        if submitted:
            if not nome or not sobrenome or not email or not cpf or not data_nascimento or not senha:
                st.error("Preencha todos os campos obrigatórios.")
            elif not aceite_termos or not aceite_privacidade or not aceite_lgpd:
                st.error(
                    "Para criar sua conta, é necessário aceitar os Termos de Uso, a Política de Privacidade e o Consentimento LGPD.")
            elif len(cpf) != 11 or not cpf.isdigit():
                st.error("CPF inválido.")
            elif senha != confirmar_senha:
                st.error("As senhas não coincidem.")
            elif len(senha) < 6:
                st.warning("A senha deve ter pelo menos 6 caracteres.")
            else:
                resultado = fazer_cadastro(nome, sobrenome, email, cpf, data_nascimento.strftime("%Y-%m-%d"), senha, telefone, whatsapp)
                if resultado is True:
                    _salvar_consentimento_usuario(email)
                    st.success("Conta criada! Faça login.")
                    _set_mode("login")
                    st.rerun()
                elif resultado == "cpf_existente":
                    st.error("Este CPF já está cadastrado.")
                else:
                    st.error("Este e-mail já está cadastrado.")

    if st.button("Voltar para login", use_container_width=True):
        _set_mode("login")
        st.rerun()


def render_login_compacto(
    carregar_logo=None,
    remover_fundo_branco=None,
    fazer_login=None,
    fazer_login_visitante=None,
    fazer_cadastro=None,
):
    _css_login_compacto()

    if "login_mode" not in st.session_state:
        st.session_state.login_mode = "login"

    _, center, _ = st.columns([1, 1.12, 1])

    with center:
        _render_logo()
        mode = st.session_state.login_mode

        if mode == "cadastro":
            _render_cadastro(fazer_cadastro)
        elif mode == "visitante":
            _render_visitante(fazer_login_visitante)
        else:
            _render_login_principal(fazer_login)
