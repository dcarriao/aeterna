# utils/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import sqlite3
from datetime import datetime
import os


class EmailService:
    def __init__(self):
        # Carregar configurações dos secrets do Streamlit
        try:
            self.smtp_server = st.secrets.get("SMTP_SERVER", "smtppro.zoho.com")
            self.smtp_port = int(st.secrets.get("SMTP_PORT", 587))
            self.email_remetente = st.secrets.get("EMAIL_REMETENTE", "")
            self.email_senha = st.secrets.get("EMAIL_SENHA", "")
        except Exception:
            self.email_remetente = ""
            self.email_senha = ""

    def enviar_mensagem(self, destinatario_email: str, nome_destinatario: str,
                        nome_remetente: str, mensagem: str, data_especial: str = ""):
        """Envia uma mensagem por e-mail"""
        if not self.email_remetente or not self.email_senha:
            print("⚠️ Email não configurado")
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

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_remetente, self.email_senha)
            server.send_message(msg)
            server.quit()

            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False


def processar_agendamentos():
    """Verifica agendamentos pendentes e envia mensagens"""
    db_path = "dados/cofre.db"

    if not os.path.exists(db_path):
        return 0

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hoje = datetime.now().strftime("%Y-%m-%d")

    try:
        # Verificar se a tabela agendamentos existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agendamentos'")
        if not cursor.fetchone():
            conn.close()
            return 0

        cursor.execute('''
            SELECT a.id, a.usuario_id, a.contato_id, a.tipo, a.conteudo, a.video_id,
                   u.nome as remetente_nome, u.email as remetente_email,
                   c.nome as destinatario_nome, c.email as destinatario_email,
                   c.whatsapp as destinatario_whatsapp
            FROM agendamentos a
            JOIN usuarios u ON a.usuario_id = u.id
            JOIN contatos c ON a.contato_id = c.id
            WHERE a.status = 'agendado' AND a.data_envio <= ?
        ''', (hoje,))

        agendamentos = cursor.fetchall()

        if not agendamentos:
            conn.close()
            return 0

        email_service = EmailService()
        enviados = 0

        for agend in agendamentos:
            agend_id = agend[0]
            tipo = agend[3]
            conteudo = agend[4]
            remetente_nome = agend[6]
            destinatario_nome = agend[8]
            destinatario_email = agend[9]

            if tipo == 'texto' and conteudo and destinatario_email:
                if email_service.enviar_mensagem(
                        destinatario_email=destinatario_email,
                        nome_destinatario=destinatario_nome,
                        nome_remetente=remetente_nome,
                        mensagem=conteudo
                ):
                    cursor.execute('''
                        UPDATE agendamentos SET status = 'enviado', data_envio_real = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (agend_id,))
                    enviados += 1

        conn.commit()
    except Exception as e:
        print(f"Erro processando agendamentos: {e}")

    conn.close()
    return enviados