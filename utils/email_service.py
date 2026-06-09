# utils/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from datetime import datetime


class EmailService:
    def __init__(self):
        # Carregar configurações dos secrets do Streamlit
        try:
            self.smtp_server = st.secrets.get("SMTP_SERVER", "smtppro.zoho.com")
            self.smtp_port = int(st.secrets.get("SMTP_PORT", 587))
            self.email_remetente = st.secrets.get("EMAIL_REMETENTE", "")
            self.email_senha = st.secrets.get("EMAIL_SENHA", "")

            # Debug (remove em produção)
            if self.email_remetente:
                print(f"✅ Email configurado: {self.email_remetente}")
            else:
                print("⚠️ Email não configurado nas secrets")
        except Exception as e:
            print(f"❌ Erro ao carregar secrets: {e}")
            self.email_remetente = ""
            self.email_senha = ""

    def enviar_mensagem(self, destinatario_email: str, nome_destinatario: str,
                        nome_remetente: str, mensagem: str, data_especial: str = ""):
        """Envia uma mensagem por e-mail usando SMTP do Zoho"""
        if not self.email_remetente or not self.email_senha:
            print("⚠️ Email não configurado. Configure as secrets no Streamlit Cloud.")
            print("   Adicione: EMAIL_REMETENTE, EMAIL_SENHA, SMTP_SERVER, SMTP_PORT")
            return False

        try:
            assunto = f"💚 Uma lembrança especial de {nome_remetente}"
            if data_especial:
                assunto = f"💚 {data_especial} - Uma lembrança de {nome_remetente}"

            corpo = f"""
            Olá {nome_destinatario},

            {mensagem}

            ---
            Esta é uma mensagem programada enviada pelo aEterna.
            {nome_remetente} deixou esta lembrança especialmente para você.

            💚 aEterna - Seu legado digital
            https://aeternalegado.com.br
            """

            msg = MIMEMultipart()
            msg['From'] = self.email_remetente
            msg['To'] = destinatario_email
            msg['Subject'] = assunto

            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

            # Conexão SMTP com Zoho
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_remetente, self.email_senha)
            server.send_message(msg)
            server.quit()

            print(f"✅ E-mail enviado para {destinatario_email}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {e}")
            return False