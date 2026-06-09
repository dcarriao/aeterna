# utils/banco.py
import sqlite3
import os
from typing import List, Dict, Optional


class BancoDados:
    def __init__(self, arquivo_db="dados/cofre.db"):
        os.makedirs(os.path.dirname(arquivo_db), exist_ok=True)
        self.arquivo_db = arquivo_db
        self._inicializar_banco()
        self._migrar_documentos()

    def _inicializar_banco(self):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                data_nascimento DATE NOT NULL,
                telefone TEXT,
                whatsapp TEXT,
                senha_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                foto TEXT,
                redes_sociais TEXT,
                tipo TEXT DEFAULT 'usuario',
                plano_id INTEGER DEFAULT 1,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP
            )
        ''')

        # Tabela de preferências do usuário (gostos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferencias_usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER UNIQUE,
                gostos_musica TEXT,
                gostos_comida TEXT,
                melhor_lembranca TEXT,
                dia_mais_feliz TEXT,
                dia_mais_triste TEXT,
                personalidade_extra TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        # Tabela de personalidade para assistente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalidade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                pergunta TEXT,
                resposta TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
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
                categoria TEXT DEFAULT 'geral',
                notas TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de acesso aos vídeos (quem pode ver)
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

        # Tabela de agendamentos (mensagens programadas)
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

        # Tabela de planos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL DEFAULT 0,
                descricao TEXT,
                max_contatos INTEGER DEFAULT 10,
                max_prioridades INTEGER DEFAULT 3,
                max_mensagens_ia INTEGER DEFAULT 50,
                max_videos_total INTEGER DEFAULT 10,
                max_videos_por_categoria INTEGER DEFAULT 5,
                tem_agendamento INTEGER DEFAULT 1,
                tem_videos_ia INTEGER DEFAULT 0,
                ativo INTEGER DEFAULT 1
            )
        ''')

        # Inserir plano padrão
        cursor.execute("SELECT COUNT(*) FROM planos")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO planos (nome, preco, descricao, max_contatos, max_prioridades, max_mensagens_ia, max_videos_total, max_videos_por_categoria, tem_agendamento, tem_videos_ia)
                VALUES ('Gratuito', 0, 'Plano básico gratuito', 10, 3, 50, 10, 5, 1, 0)
            ''')

        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

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
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # TABELA DE DOCUMENTOS (adicione esta parte)
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS documentos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario_id INTEGER,
                   tipo TEXT NOT NULL,
                   titulo TEXT NOT NULL,
                   descricao TEXT,
                   caminho_arquivo TEXT,
                   nome_original TEXT,
                   tamanho INTEGER,
                   data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
               )
        ''')

        conn.commit()
        conn.close()

    # ========================================================================
    # USUÁRIOS
    # ========================================================================
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
        return [{"id": r[0], "nome": r[1], "sobrenome": r[2], "nome_completo": f"{r[1]} {r[2]}".strip(),
                 "email": r[3], "telefone": r[4] or "", "whatsapp": r[5] or "", "parentesco": r[6] or "",
                 "is_prioridade": r[7]} for r in rows]

    def contar_contatos_prioritarios(self, usuario_id: int) -> int:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM contatos WHERE usuario_id = ? AND is_prioridade = 1', (usuario_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

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
        cursor.execute('''
            SELECT id, titulo, destinatario, caminho_arquivo, categoria, data_criacao 
            FROM videos WHERE usuario_id = ? ORDER BY data_criacao DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "titulo": r[1], "destinatario": r[2], "caminho": r[3],
                 "categoria": r[4] if len(r) > 4 else "geral", "data": r[5]} for r in rows]

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

    def adicionar_video_com_acesso(self, usuario_id: int, titulo: str, destinatario: str,
                                   caminho_arquivo: str, contatos_ids: List[int], categoria: str = "geral"):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO videos (usuario_id, titulo, destinatario, caminho_arquivo, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, titulo, destinatario, caminho_arquivo, categoria))
        video_id = cursor.lastrowid

        for contato_id in contatos_ids:
            try:
                cursor.execute('INSERT INTO videos_acesso (video_id, contato_id) VALUES (?, ?)', (video_id, contato_id))
            except:
                pass

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

    def listar_contatos_por_video(self, video_id: int) -> List[Dict]:
        """Lista contatos que têm acesso a um vídeo específico"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, c.nome, c.sobrenome
            FROM contatos c
            JOIN videos_acesso va ON c.id = va.contato_id
            WHERE va.video_id = ?
        ''', (video_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "nome_completo": f"{r[1]} {r[2]}".strip()} for r in rows]

    # ========================================================================
    # CONTATOS
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
                   data_nascimento, datas_especiais, is_prioridade, prioridade_order, acesso_central_luto, chave_acesso
            FROM contatos WHERE usuario_id = ? ORDER BY prioridade_order, nome
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0],
            "nome": r[1],
            "sobrenome": r[2] or "",
            "nome_completo": f"{r[1]} {r[2]}".strip(),
            "email": r[3],
            "telefone": r[4] or "",
            "whatsapp": r[5] or "",
            "parentesco": r[6] or "",
            "data_nascimento": r[7] or "",
            "datas_especiais": r[8] or "",
            "is_prioridade": r[9] or 0,
            "prioridade_order": r[10] or 0,
            "acesso_central_luto": r[11] or 0
        } for r in rows]

    def contar_contatos_usuario(self, usuario_id: int) -> int:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM contatos WHERE usuario_id = ?', (usuario_id,))
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
                "id": row[0], "nome": row[1], "sobrenome": row[2] or "", "email": row[3],
                "telefone": row[4] or "", "whatsapp": row[5] or "",
                "acesso_central_luto": row[6] or 0,
                "usuario_id": row[7],
                "falecido_nome": row[8]
            }
        return None

    def deletar_contato(self, id_contato: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = ? AND usuario_id = ?", (id_contato, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # AGENDAMENTOS (LEMBRANÇAS PROGRAMADAS)
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
            "contato_nome": f"{r[6]} {r[7]}".strip(), "contato_email": r[8]
        } for r in rows]

    def deletar_agendamento(self, id_agendamento: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ? AND usuario_id = ?", (id_agendamento, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # PREFERÊNCIAS (GOSTOS)
    # ========================================================================
    def salvar_preferencias(self, usuario_id: int, preferencias: dict):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM preferencias_usuario WHERE usuario_id = ?', (usuario_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO preferencias_usuario (usuario_id, gostos_musica, gostos_comida, melhor_lembranca, dia_mais_feliz, dia_mais_triste, personalidade_extra)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_id,
                  preferencias.get('gostos_musica', ''),
                  preferencias.get('gostos_comida', ''),
                  preferencias.get('melhor_lembranca', ''),
                  preferencias.get('dia_mais_feliz', ''),
                  preferencias.get('dia_mais_triste', ''),
                  preferencias.get('personalidade_extra', '')))
        else:
            cursor.execute('''
                UPDATE preferencias_usuario SET 
                    gostos_musica = ?,
                    gostos_comida = ?,
                    melhor_lembranca = ?,
                    dia_mais_feliz = ?,
                    dia_mais_triste = ?,
                    personalidade_extra = ?
                WHERE usuario_id = ?
            ''', (preferencias.get('gostos_musica', ''),
                  preferencias.get('gostos_comida', ''),
                  preferencias.get('melhor_lembranca', ''),
                  preferencias.get('dia_mais_feliz', ''),
                  preferencias.get('dia_mais_triste', ''),
                  preferencias.get('personalidade_extra', ''),
                  usuario_id))

        conn.commit()
        conn.close()

    def _migrar_documentos(self):
        """Adiciona tabela de documentos se não existir"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                tipo TEXT NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT,
                caminho_arquivo TEXT,
                nome_original TEXT,
                tamanho INTEGER,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def obter_preferencias(self, usuario_id: int) -> dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT gostos_musica, gostos_comida, melhor_lembranca, dia_mais_feliz, dia_mais_triste, personalidade_extra
            FROM preferencias_usuario WHERE usuario_id = ?
        ''', (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "gostos_musica": row[0] or "",
                "gostos_comida": row[1] or "",
                "melhor_lembranca": row[2] or "",
                "dia_mais_feliz": row[3] or "",
                "dia_mais_triste": row[4] or "",
                "personalidade_extra": row[5] or ""
            }
        return {}

    # ========================================================================
    # PLANOS
    # ========================================================================
    def obter_plano_usuario(self, usuario_id: int) -> dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, p.nome, p.preco, p.max_contatos, p.max_prioridades, p.max_mensagens_ia, 
                   p.max_videos_total, p.max_videos_por_categoria, p.tem_agendamento, p.tem_videos_ia
            FROM planos p
            JOIN usuarios u ON u.plano_id = p.id
            WHERE u.id = ?
        ''', (usuario_id,))
        plano = cursor.fetchone()
        conn.close()
        if plano:
            return {
                "id": plano[0],
                "nome": plano[1],
                "preco": plano[2],
                "max_contatos": plano[3],
                "max_prioridades": plano[4],
                "max_mensagens_ia": plano[5],
                "max_videos_total": plano[6],
                "max_videos_por_categoria": plano[7],
                "tem_agendamento": plano[8],
                "tem_videos_ia": plano[9]
            }
        return {
            "id": 1,
            "nome": "Gratuito",
            "preco": 0,
            "max_contatos": 10,
            "max_prioridades": 3,
            "max_mensagens_ia": 50,
            "max_videos_total": 10,
            "max_videos_por_categoria": 5,
            "tem_agendamento": 1,
            "tem_videos_ia": 0
        }

    # ========================================================================
    # DOCUMENTOS
    # ========================================================================
    def adicionar_documento(self, usuario_id: int, tipo: str, titulo: str, descricao: str,
                            caminho_arquivo: str, nome_original: str, tamanho: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        # Criar tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                tipo TEXT NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT,
                caminho_arquivo TEXT,
                nome_original TEXT,
                tamanho INTEGER,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        cursor.execute('''
            INSERT INTO documentos (usuario_id, tipo, titulo, descricao, caminho_arquivo, nome_original, tamanho)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, tipo, titulo, descricao, caminho_arquivo, nome_original, tamanho))

        conn.commit()
        conn.close()

    def listar_documentos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, tipo, titulo, descricao, caminho_arquivo, nome_original, tamanho, data_criacao
            FROM documentos WHERE usuario_id = ? ORDER BY data_criacao DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0],
            "tipo": r[1],
            "titulo": r[2],
            "descricao": r[3] or "",
            "caminho_arquivo": r[4],
            "nome_original": r[5],
            "tamanho": r[6],
            "data_criacao": r[7]
        } for r in rows]

    def deletar_documento(self, id_documento: int, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documentos WHERE id = ? AND usuario_id = ?", (id_documento, usuario_id))
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