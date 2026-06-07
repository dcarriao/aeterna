# utils/banco.py
import sqlite3
import os
from typing import List, Dict, Optional


class BancoDados:
    def __init__(self, arquivo_db="dados/cofre.db"):
        os.makedirs(os.path.dirname(arquivo_db), exist_ok=True)
        self.arquivo_db = arquivo_db
        self._inicializar_banco()

    def _inicializar_banco(self):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS senhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                servico TEXT NOT NULL,
                usuario TEXT NOT NULL,
                senha_criptografada TEXT NOT NULL,
                url TEXT,
                notas TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                destinatario TEXT,
                caminho_arquivo TEXT,
                url_externa TEXT,
                notas TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT,
                whatsapp TEXT,
                papel TEXT,
                chave_acesso TEXT,
                mensagem_liberacao TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def adicionar_senha(self, servico: str, usuario: str, senha: str, url: str = "", notas: str = ""):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO senhas (servico, usuario, senha_criptografada, url, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', (servico, usuario, senha, url, notas))
        conn.commit()
        conn.close()

    def listar_senhas(self) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, servico, usuario, url, notas FROM senhas ORDER BY servico')
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "servico": row[1], "usuario": row[2], "url": row[3], "notas": row[4]} for row in rows]

    def obter_senha(self, id_senha: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM senhas WHERE id = ?', (id_senha,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "servico": row[1], "usuario": row[2], "senha_criptografada": row[3], "url": row[4],
                    "notas": row[5]}
        return None

    def deletar_senha(self, id_senha: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM senhas WHERE id = ?', (id_senha,))
        conn.commit()
        conn.close()

    def adicionar_video(self, titulo: str, destinatario: str, caminho_arquivo: str = "", url_externa: str = "",
                        notas: str = ""):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO videos (titulo, destinatario, caminho_arquivo, url_externa, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, destinatario, caminho_arquivo, url_externa, notas))
        conn.commit()
        conn.close()

    def listar_videos(self) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, titulo, destinatario, url_externa, notas FROM videos ORDER BY data_criacao DESC')
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "titulo": row[1], "destinatario": row[2], "url_externa": row[3], "notas": row[4]} for row
                in rows]

    def deletar_video(self, id_video: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM videos WHERE id = ?', (id_video,))
        conn.commit()
        conn.close()

    def adicionar_contato(self, nome: str, email: str, telefone: str = "", whatsapp: str = "", papel: str = "",
                          chave_acesso: str = ""):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contatos (nome, email, telefone, whatsapp, papel, chave_acesso)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, telefone, whatsapp, papel, chave_acesso))
        conn.commit()
        conn.close()

    def listar_contatos(self) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, email, telefone, whatsapp, papel FROM contatos ORDER BY nome')
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "nome": row[1], "email": row[2], "telefone": row[3], "whatsapp": row[4], "papel": row[5]}
                for row in rows]

    def deletar_contato(self, id_contato: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contatos WHERE id = ?', (id_contato,))
        conn.commit()
        conn.close()

    def salvar_config(self, chave: str, valor: str):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)', (chave, valor))
        conn.commit()
        conn.close()

    def obter_config(self, chave: str) -> Optional[str]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM configuracoes WHERE chave = ?', (chave,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None