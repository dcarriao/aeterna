import os
import sys
from pathlib import Path

# Permite importar utils quando rodar o script pela raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.banco import BancoDados
from utils.email_service import EmailService


def main():
    db = BancoDados()
    email_service = EmailService()

    mensagens = db.listar_agendamentos_pendentes()

    print(f"Mensagens pendentes encontradas: {len(mensagens)}")

    for msg in mensagens:
        try:
            if not msg.get("contato_email"):
                raise Exception("Contato sem e-mail cadastrado.")

            assunto = "💌 Uma mensagem especial foi deixada para você"

            if msg["tipo"] == "texto":
                corpo = f"""
Olá, {msg['contato_nome']}.

Você recebeu uma mensagem especial pela aEterna:

{msg['conteudo']}

Com carinho,
aEterna
"""
            else:
                corpo = f"""
Olá, {msg['contato_nome']}.

Uma mensagem em vídeo foi liberada para você na aEterna.

Acesse sua área memorial para visualizar.

Com carinho,
aEterna
"""
            print("=" * 80)
            print("DESTINATÁRIO:", msg["contato_email"])
            print("CONTEÚDO:", msg["conteudo"])
            print("ENVIANDO MENSAGEM")
            print("PARA:", msg["contato_email"])
            print("CONTEÚDO:")
            print(msg["conteudo"])
            print("=" * 80)

            db.marcar_agendamento_enviado(msg["id"])
            print(f"Agendamento {msg['id']} enviado com sucesso.")

        except Exception as e:
            db.marcar_agendamento_erro(msg["id"], str(e))
            print(f"Erro no agendamento {msg['id']}: {e}")


if __name__ == "__main__":
    main()