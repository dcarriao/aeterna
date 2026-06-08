# utils/migrar.py
import sqlite3
import os


def executar_migracao():
    """Adiciona colunas faltantes no banco de dados existente"""

    db_path = "dados/cofre.db"

    if not os.path.exists(db_path):
        print("Banco não encontrado")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar colunas da tabela contatos
    cursor.execute("PRAGMA table_info(contatos)")
    colunas = [col[1] for col in cursor.fetchall()]

    # Adicionar colunas que faltam (sem perder dados)
    if 'usuario_id' not in colunas:
        cursor.execute('ALTER TABLE contatos ADD COLUMN usuario_id INTEGER DEFAULT 1')
        print("✅ Coluna usuario_id adicionada")

    if 'chave_acesso' not in colunas:
        cursor.execute('ALTER TABLE contatos ADD COLUMN chave_acesso TEXT')
        print("✅ Coluna chave_acesso adicionada")

    if 'is_prioridade' not in colunas:
        cursor.execute('ALTER TABLE contatos ADD COLUMN is_prioridade INTEGER DEFAULT 0')
        print("✅ Coluna is_prioridade adicionada")

    # Verificar tabela videos
    cursor.execute("PRAGMA table_info(videos)")
    colunas_videos = [col[1] for col in cursor.fetchall()]

    if 'usuario_id' not in colunas_videos:
        cursor.execute('ALTER TABLE videos ADD COLUMN usuario_id INTEGER DEFAULT 1')
        print("✅ Coluna usuario_id adicionada em videos")

    conn.commit()
    conn.close()
    print("🎉 Migração concluída!")


if __name__ == "__main__":
    executar_migracao()