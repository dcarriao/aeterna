import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dados" / "cofre.db"


def main():
    print(f"Banco: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consentimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            aceite_termos INTEGER DEFAULT 0,
            aceite_privacidade INTEGER DEFAULT 0,
            aceite_lgpd INTEGER DEFAULT 0,
            versao_termos TEXT DEFAULT '1.0',
            versao_privacidade TEXT DEFAULT '1.0',
            data_aceite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT,
            user_agent TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_consentimentos_usuario
        ON consentimentos(usuario_id)
    """)

    conn.commit()
    conn.close()

    print("Tabela consentimentos criada/verificada com sucesso.")


if __name__ == "__main__":
    main()