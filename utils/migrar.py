# listar_banco.py

import sqlite3

with open("estrutura_banco.txt", "w", encoding="utf-8") as arq:

    conn = sqlite3.connect("D:/aeterna/dados/cofre.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """)

    tabelas = [row[0] for row in cursor.fetchall()]

    for tabela in tabelas:
        arq.write(f"\n=== {tabela} ===\n")

        cursor.execute(f"PRAGMA table_info({tabela})")

        for coluna in cursor.fetchall():
            arq.write(f"{coluna[1]} ({coluna[2]})\n")

    conn.close()

print("Arquivo estrutura_banco.txt criado.")

conn.close()
