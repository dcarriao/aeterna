# utils/banco.py - VERSÃO SIMPLIFICADA E COMPATÍVEL
import sqlite3
import os
from typing import List, Dict, Optional


class BancoDados:
    def __init__(self, arquivo_db="dados/cofre.db"):
        os.makedirs(os.path.dirname(arquivo_db), exist_ok=True)
        self.arquivo_db = arquivo_db
        self._inicializar_banco()
        self._migrar_contatos()

    def _migrar_contatos(self):
        """Adiciona colunas faltantes na tabela contatos"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(contatos)")
        colunas = [col[1] for col in cursor.fetchall()]

        # Colunas que deveriam existir
        colunas_necessarias = ['parentesco', 'data_nascimento', 'datas_especiais', 'acesso_central_luto', 'sobrenome']

        for coluna in colunas_necessarias:
            if coluna not in colunas:
                try:
                    if coluna == 'acesso_central_luto':
                        cursor.execute(f'ALTER TABLE contatos ADD COLUMN {coluna} INTEGER DEFAULT 0')
                    elif coluna == 'sobrenome':
                        cursor.execute(f'ALTER TABLE contatos ADD COLUMN {coluna} TEXT DEFAULT ""')
                    else:
                        cursor.execute(f'ALTER TABLE contatos ADD COLUMN {coluna} TEXT DEFAULT ""')
                    print(f"✅ Coluna '{coluna}' adicionada à tabela contatos")
                except Exception as e:
                    print(f"⚠️ Erro ao adicionar coluna {coluna}: {e}")

        conn.commit()
        conn.close()

    def _inicializar_banco(self):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS senhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
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
                usuario_id INTEGER,
                titulo TEXT NOT NULL,
                destinatario TEXT,
                caminho_arquivo TEXT,
                url_externa TEXT,
                categoria TEXT DEFAULT 'geral',
                notas TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT,
                whatsapp TEXT,
                parentesco TEXT,
                data_nascimento DATE,
                is_prioridade INTEGER DEFAULT 0,
                prioridade_order INTEGER DEFAULT 0,
                chave_acesso TEXT,
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

    # ========================================================================
    # SENHAS
    # ========================================================================
    def adicionar_senha(self, usuario_id: int, servico: str, usuario: str, senha: str, url: str = "", notas: str = ""):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO senhas (usuario_id, servico, usuario, senha_criptografada, url, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (usuario_id, servico, usuario, senha, url, notas))
        conn.commit()
        conn.close()

    def listar_senhas_usuario(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, servico, usuario, url, notas FROM senhas WHERE usuario_id = ? ORDER BY servico',
                       (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "servico": row[1], "usuario": row[2], "url": row[3], "notas": row[4]} for row in rows]

    def obter_senha(self, id_senha: int, usuario_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM senhas WHERE id = ? AND usuario_id = ?', (id_senha, usuario_id))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "servico": row[2], "usuario": row[3], "senha_criptografada": row[4], "url": row[5],
                    "notas": row[6]}
        return None

    def deletar_senha(self, id_senha: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM senhas WHERE id = ? AND usuario_id = ?', (id_senha, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # VÍDEOS
    # ========================================================================
    def listar_videos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT id, titulo, destinatario, caminho_arquivo, categoria, data_criacao 
                FROM videos WHERE usuario_id = ? ORDER BY data_criacao DESC
            ''', (usuario_id,))
            rows = cursor.fetchall()
            conn.close()
            return [{"id": r[0], "titulo": r[1], "destinatario": r[2], "caminho": r[3], "categoria": r[4], "data": r[5]}
                    for r in rows]
        except:
            conn.close()
            return []

    def adicionar_video(self, usuario_id: int, titulo: str, destinatario: str, caminho_arquivo: str,
                        categoria: str = "geral"):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO videos (usuario_id, titulo, destinatario, caminho_arquivo, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, titulo, destinatario, caminho_arquivo, categoria))
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return video_id

    def deletar_video(self, id_video: int, usuario_id: int) -> bool:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("SELECT caminho_arquivo FROM videos WHERE id = ? AND usuario_id = ?", (id_video, usuario_id))
        row = cursor.fetchone()
        if row:
            if row[0] and os.path.exists(row[0]):
                try:
                    os.remove(row[0])
                except:
                    pass
            cursor.execute("DELETE FROM videos WHERE id = ? AND usuario_id = ?", (id_video, usuario_id))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    # ========================================================================
    # CONTATOS
    # ========================================================================
    def adicionar_contato(self, usuario_id: int, nome: str, email: str, telefone: str = "", whatsapp: str = "",
                          parentesco: str = "", data_nascimento: str = "", is_prioridade: int = 0,
                          prioridade_order: int = 0, chave_acesso: str = ""):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contatos (usuario_id, nome, email, telefone, whatsapp, parentesco, data_nascimento, is_prioridade, prioridade_order, chave_acesso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome, email, telefone, whatsapp, parentesco, data_nascimento, is_prioridade, prioridade_order,
              chave_acesso))
        conn.commit()
        conn.close()

    def listar_contatos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, email, telefone, whatsapp, parentesco, data_nascimento, is_prioridade, prioridade_order
            FROM contatos WHERE usuario_id = ? ORDER BY prioridade_order, nome
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], "nome": r[1], "sobrenome": "", "nome_completo": r[1],
            "email": r[2], "telefone": r[3] or "", "whatsapp": r[4] or "", "parentesco": r[5] or "",
            "data_nascimento": r[6] or "", "is_prioridade": r[7], "prioridade_order": r[8],
            "acesso_central_luto": 0
        } for r in rows]

    def listar_contatos_prioritarios(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, email, telefone, whatsapp, parentesco, is_prioridade
            FROM contatos WHERE usuario_id = ? AND is_prioridade = 1 ORDER BY prioridade_order
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "nome": r[1], "sobrenome": "", "nome_completo": r[1],
                 "email": r[2], "telefone": r[3] or "", "whatsapp": r[4] or "", "parentesco": r[5] or "",
                 "is_prioridade": r[6]} for r in rows]

    def contar_contatos_usuario(self, usuario_id: int) -> int:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM contatos WHERE usuario_id = ?', (usuario_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def contar_contatos_prioritarios(self, usuario_id: int) -> int:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM contatos WHERE usuario_id = ? AND is_prioridade = 1', (usuario_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def obter_contato_por_chave(self, chave_acesso: str, email_falecido: str = None) -> Optional[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        if email_falecido:
            cursor.execute('''
                SELECT c.id, c.nome, c.email, u.id as usuario_id, u.nome as falecido_nome
                FROM contatos c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.chave_acesso = ? AND u.email = ?
            ''', (chave_acesso, email_falecido))
        else:
            cursor.execute('''
                SELECT c.id, c.nome, c.email, u.id as usuario_id, u.nome as falecido_nome
                FROM contatos c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.chave_acesso = ?
            ''', (chave_acesso,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0], "nome": row[1], "sobrenome": "", "email": row[2],
                "telefone": "", "whatsapp": "",
                "acesso_central_luto": 1, "usuario_id": row[3], "falecido_nome": row[4]
            }
        return None

    def deletar_contato(self, id_contato: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = ? AND usuario_id = ?", (id_contato, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # CONFIGURAÇÕES
    # ========================================================================
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