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

        # Tabela de senhas
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

        # Tabela de vídeos
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

        # Tabela de acesso aos vídeos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                contato_id INTEGER,
                FOREIGN KEY (video_id) REFERENCES videos(id),
                FOREIGN KEY (contato_id) REFERENCES contatos(id)
            )
        ''')

        # Tabela de contatos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT,
                whatsapp TEXT,
                parentesco TEXT,
                data_nascimento DATE,
                datas_especiais TEXT,
                is_prioridade INTEGER DEFAULT 0,
                prioridade_order INTEGER DEFAULT 0,
                acesso_central_luto INTEGER DEFAULT 0,
                chave_acesso TEXT,
                mensagem_liberacao TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        # Tabela de agendamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                contato_id INTEGER,
                tipo TEXT CHECK(tipo IN ('texto', 'video')),
                data_envio DATE,
                data_termino DATE,
                conteudo TEXT,
                video_id INTEGER,
                gerar_por_ia INTEGER DEFAULT 0,
                status TEXT DEFAULT 'agendado',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_envio_real TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (contato_id) REFERENCES contatos(id),
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        ''')

        # Tabela de configurações
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
    # OPERAÇÕES DE SENHAS
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
    # OPERAÇÕES DE VÍDEOS
    # ========================================================================
    def listar_videos_usuario(self, usuario_id: int) -> List[Dict]:
        """Lista todos os vídeos de um usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, titulo, destinatario, caminho_arquivo, categoria, data_criacao 
            FROM videos WHERE usuario_id = ? ORDER BY data_criacao DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "titulo": r[1], "destinatario": r[2], "caminho": r[3], "categoria": r[4], "data": r[5]} for
                r in rows]

    def adicionar_video_com_acesso(self, usuario_id: int, titulo: str, destinatario: str,
                                   caminho_arquivo: str, contatos_ids: List[int], categoria: str = "geral"):
        """Adiciona vídeo e define quais contatos podem acessar"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO videos (usuario_id, titulo, destinatario, caminho_arquivo, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, titulo, destinatario, caminho_arquivo, categoria))

        video_id = cursor.lastrowid

        for contato_id in contatos_ids:
            cursor.execute('INSERT INTO videos_acesso (video_id, contato_id) VALUES (?, ?)', (video_id, contato_id))

        conn.commit()
        conn.close()
        return video_id

    def listar_videos_por_contato(self, contato_id: int) -> List[Dict]:
        """Lista vídeos que um contato específico tem acesso"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, v.titulo, v.destinatario, v.caminho_arquivo, v.categoria
            FROM videos v
            JOIN videos_acesso va ON v.id = va.video_id
            WHERE va.contato_id = ?
        ''', (contato_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "titulo": r[1], "destinatario": r[2], "caminho": r[3], "categoria": r[4]} for r in rows]

    def deletar_video(self, id_video: int, usuario_id: int) -> bool:
        """Deleta um vídeo (apenas se for do usuário)"""
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

            cursor.execute("DELETE FROM videos_acesso WHERE video_id = ?", (id_video,))
            cursor.execute("DELETE FROM videos WHERE id = ? AND usuario_id = ?", (id_video, usuario_id))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    # ========================================================================
    # OPERAÇÕES DE CONTATOS
    # ========================================================================
    def adicionar_contato(self, usuario_id: int, nome: str, sobrenome: str, email: str,
                          telefone: str = "", whatsapp: str = "", parentesco: str = "",
                          data_nascimento: str = "", datas_especiais: str = "",
                          is_prioridade: int = 0, prioridade_order: int = 0,
                          acesso_central_luto: int = 0, chave_acesso: str = ""):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contatos (usuario_id, nome, sobrenome, email, telefone, whatsapp, parentesco, 
                                  data_nascimento, datas_especiais, is_prioridade, prioridade_order, 
                                  acesso_central_luto, chave_acesso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome, sobrenome, email, telefone, whatsapp, parentesco,
              data_nascimento, datas_especiais, is_prioridade, prioridade_order, acesso_central_luto, chave_acesso))
        conn.commit()
        conn.close()

    def listar_contatos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, sobrenome, email, telefone, whatsapp, parentesco, 
                   data_nascimento, datas_especiais, is_prioridade, prioridade_order, acesso_central_luto
            FROM contatos WHERE usuario_id = ? ORDER BY prioridade_order, nome
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], "nome": r[1], "sobrenome": r[2], "nome_completo": f"{r[1]} {r[2]}",
            "email": r[3], "telefone": r[4] or "", "whatsapp": r[5] or "", "parentesco": r[6] or "",
            "data_nascimento": r[7] or "", "datas_especiais": r[8] or "", "is_prioridade": r[9],
            "prioridade_order": r[10], "acesso_central_luto": r[11]
        } for r in rows]

    def listar_contatos_prioritarios(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, sobrenome, email, telefone, whatsapp, parentesco, is_prioridade
            FROM contatos 
            WHERE usuario_id = ? AND is_prioridade = 1
            ORDER BY prioridade_order
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "nome": r[1], "sobrenome": r[2], "nome_completo": f"{r[1]} {r[2]}",
                 "email": r[3], "telefone": r[4] or "", "whatsapp": r[5] or "", "parentesco": r[6] or "",
                 "is_prioridade": r[7]} for r in rows]

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
                SELECT c.id, c.nome, c.sobrenome, c.email, c.telefone, c.whatsapp, c.acesso_central_luto, u.id as usuario_id, u.nome as falecido_nome
                FROM contatos c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.chave_acesso = ? AND u.email = ?
            ''', (chave_acesso, email_falecido))
        else:
            cursor.execute('''
                SELECT c.id, c.nome, c.sobrenome, c.email, c.telefone, c.whatsapp, c.acesso_central_luto, u.id as usuario_id, u.nome as falecido_nome
                FROM contatos c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.chave_acesso = ?
            ''', (chave_acesso,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0], "nome": row[1], "sobrenome": row[2], "email": row[3],
                "telefone": row[4] or "", "whatsapp": row[5] or "",
                "acesso_central_luto": row[6], "usuario_id": row[7], "falecido_nome": row[8]
            }
        return None

    def deletar_contato(self, id_contato: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = ? AND usuario_id = ?", (id_contato, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # OPERAÇÕES DE AGENDAMENTOS
    # ========================================================================
    def criar_agendamento(self, usuario_id: int, contato_id: int, tipo: str, data_envio: str,
                          data_termino: str = "", conteudo: str = "", video_id: int = None,
                          gerar_por_ia: int = 0) -> int:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agendamentos (usuario_id, contato_id, tipo, data_envio, data_termino, 
                                      conteudo, video_id, gerar_por_ia, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'agendado')
        ''', (usuario_id, contato_id, tipo, data_envio, data_termino, conteudo, video_id, gerar_por_ia))
        conn.commit()
        agendamento_id = cursor.lastrowid
        conn.close()
        return agendamento_id

    def listar_agendamentos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.tipo, a.data_envio, a.data_termino, a.conteudo, a.status,
                   c.nome, c.sobrenome, c.email
            FROM agendamentos a
            JOIN contatos c ON a.contato_id = c.id
            WHERE a.usuario_id = ?
            ORDER BY a.data_envio
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], "tipo": r[1], "data_envio": r[2], "data_termino": r[3],
            "conteudo": r[4] or "", "status": r[5],
            "contato_nome": f"{r[6]} {r[7]}", "contato_email": r[8]
        } for r in rows]

    def deletar_agendamento(self, id_agendamento: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ? AND usuario_id = ?", (id_agendamento, usuario_id))
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