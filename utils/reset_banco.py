# reset_banco.py
import os
import shutil
from datetime import datetime


def resetar_banco():
    """Reseta o banco de dados e a pasta de vídeos"""

    print("=" * 50)
    print("⚠️  ATENÇÃO: Isso vai apagar TODOS os dados!")
    print("=" * 50)

    confirm = input("Digite 'RESETAR' para confirmar: ")

    if confirm != "RESETAR":
        print("Operação cancelada.")
        return

    # Backup do banco antigo
    if os.path.exists("dados/cofre.db"):
        backup_name = f"dados/cofre_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy("dados/cofre.db", backup_name)
        print(f"✅ Backup criado: {backup_name}")

        # Remover banco antigo
        os.remove("dados/cofre.db")
        print("✅ Banco antigo removido")

    # Limpar pasta de vídeos
    if os.path.exists("videos"):
        shutil.rmtree("videos")
        print("✅ Pasta de vídeos removida")

    # Recriar pastas
    os.makedirs("dados", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    print("\n" + "=" * 50)
    print("✅ BANCO RESETADO COM SUCESSO!")
    print("=" * 50)
    print("\nO novo banco será criado automaticamente na primeira execução.")


if __name__ == "__main__":
    resetar_banco()