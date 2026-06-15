import os
import sys
from pathlib import Path
from utils.logger import logger

# Permite importar utils quando rodar o script pela raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.banco import BancoDados
from utils.email_service import EmailService


def main():
    db = BancoDados()
    email_service = EmailService()

    mensagens = db.listar_agendamentos_pendentes()

    logger.info(f"Mensagens pendentes encontradas: {len(mensagens)}")

    for msg in mensagens:
        try:
            if not msg.get("contato_email"):
                raise Exception("Contato sem e-mail cadastrado.")

            if msg["tipo"] == "texto":
                sucesso = email_service.enviar_mensagem(
                    destinatario_email=msg["contato_email"],
                    nome_destinatario=msg["contato_nome"],
                    nome_remetente="aEterna",
                    mensagem=msg["conteudo"],
                    data_especial=""
                )
            else:
                sucesso = email_service.enviar_mensagem(
                    destinatario_email=msg["contato_email"],
                    nome_destinatario=msg["contato_nome"],
                    nome_remetente="aEterna",
                    mensagem=(
                        "Uma mensagem em vídeo foi liberada para você na aEterna.\n\n"
                        "Acesse sua área memorial para visualizar."
                    ),
                    data_especial=""
                )

            if not sucesso:
                raise Exception("Falha ao enviar e-mail pelo EmailService.")

            db.marcar_agendamento_enviado(msg["id"])
            logger.info(f"Agendamento {msg['id']} enviado com sucesso.")

        except Exception as e:
            db.marcar_agendamento_erro(msg["id"], str(e))
            logger.error(f"Erro no agendamento {msg['id']}: {e}")


if __name__ == "__main__":
    main()