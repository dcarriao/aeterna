import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dados" / "cofre.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    categoria TEXT,
    titulo TEXT,
    conteudo TEXT NOT NULL,
    origem TEXT DEFAULT 'assistente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_memorias_usuario
ON memorias(usuario_id)
""")

conn.commit()
conn.close()

print("Tabela memorias criada com sucesso.")