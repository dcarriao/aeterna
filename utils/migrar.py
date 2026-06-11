from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dados" / "cofre.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(usuarios)")
colunas = [col[1] for col in cursor.fetchall()]

if "data_nascimento" not in colunas:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN data_nascimento TEXT DEFAULT ''")
    print("Coluna data_nascimento criada.")
else:
    print("Coluna data_nascimento já existe.")

conn.commit()
conn.close()