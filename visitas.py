# visitas.py
import sqlite3
from datetime import datetime


def registrar_visita():
    """Registra uma visita à landing page"""
    conn = sqlite3.connect("dados/visitas.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            pagina TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def obter_estatisticas_visitas():
    """Retorna estatísticas de visitas"""
    conn = sqlite3.connect("dados/visitas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM visitas")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitas WHERE data >= date('now', '-7 days')")
    ultima_semana = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitas WHERE data >= date('now', '-30 days')")
    ultimo_mes = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "ultima_semana": ultima_semana,
        "ultimo_mes": ultimo_mes
    }