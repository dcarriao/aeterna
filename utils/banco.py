# utils/banco.py
import os
import sqlite3
import psycopg2
import hashlib
import secrets
import streamlit as st
from typing import List, Dict, Optional


class BancoDados:
    def __init__(self, arquivo_db="dados/cofre.db"):
        self.database_url = None

        try:
            self.database_url = (
                    os.getenv("DATABASE_URL")
                    or st.secrets.get("DATABASE_URL")
            )
        except Exception:
            self.database_url = os.getenv("DATABASE_URL")

        self.usa_postgres = bool(self.database_url)

        if not self.usa_postgres:
            os.makedirs(os.path.dirname(arquivo_db), exist_ok=True)
            self.arquivo_db = arquivo_db
            self._inicializar_banco()
            self._migrar_documentos()
        else:
            print("USANDO POSTGRES:", self.usa_postgres)

    def conectar(self):
        if self.usa_postgres:
            return psycopg2.connect(self.database_url)

        return sqlite3.connect(self.arquivo_db)

    def _inicializar_banco(self):
        conn = self.conectar()
        cursor = conn.cursor()

        # Tabela de usuários
        self.executar(cursor, '''
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
        self.executar(cursor, '''
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
        self.executar(cursor, '''
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
        self.executar(cursor, '''
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
        self.executar(cursor, '''
            CREATE TABLE IF NOT EXISTS videos_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                contato_id INTEGER,
                FOREIGN KEY (video_id) REFERENCES videos(id),
                FOREIGN KEY (contato_id) REFERENCES contatos(id)
            )
        ''')

        # Tabela de contatos
        self.executar(cursor, '''
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
        self.executar(cursor, '''
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
        self.executar(cursor, '''
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
        self.executar(cursor, "SELECT COUNT(*) FROM planos")
        if cursor.fetchone()[0] == 0:
            self.executar(cursor, '''
                INSERT INTO planos (nome, preco, descricao, max_contatos, max_prioridades, max_mensagens_ia, max_videos_total, max_videos_por_categoria, tem_agendamento, tem_videos_ia)
                VALUES ('Gratuito', 0, 'Plano básico gratuito', 10, 3, 50, 10, 5, 1, 0)
            ''')

        # Tabela de configurações
        self.executar(cursor,'''
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de senhas
        self.executar(cursor,'''
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
        self.executar(cursor,'''
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
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
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
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'SELECT COUNT(*) FROM contatos WHERE usuario_id = ? AND is_prioridade = 1', (usuario_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def gerar_hash_senha(self, senha: str, salt: str = None):
        if salt is None:
            salt = secrets.token_hex(16)

        senha_hash = hashlib.sha256((senha + salt).encode("utf-8")).hexdigest()
        return senha_hash, salt

    def cadastrar_usuario(self, nome, sobrenome, email, cpf, data_nascimento, senha, telefone="", whatsapp=""):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, "SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
            if cursor.fetchone():
                return "cpf_existente"

            self.executar(cursor, "SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                return "email_existente"

            senha_hash, salt = self.gerar_hash_senha(senha)

            self.executar(cursor, """
                INSERT INTO usuarios (
                    nome, sobrenome, email, cpf, data_nascimento,
                    telefone, whatsapp, senha_hash, salt,
                    tipo, plano_id, ativo, data_criacao
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'usuario', 1, 1, CURRENT_TIMESTAMP)
                RETURNING id
            """, (
                nome, sobrenome, email, cpf, data_nascimento,
                telefone, whatsapp, senha_hash, salt
            ))

            usuario_id = cursor.fetchone()[0]

            self.executar(cursor, """
                INSERT INTO consentimentos (
                    usuario_id,
                    aceite_termos,
                    aceite_privacidade,
                    aceite_lgpd,
                    versao_termos,
                    versao_privacidade,
                    data_aceite
                )
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (
                usuario_id,
                1,
                1,
                1,
                "1.0",
                "1.0"
            ))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Erro ao cadastrar usuário:", e)
            return False

        finally:
            cursor.close()
            conn.close()

    def autenticar_usuario(self, email: str, senha: str):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT id, nome, sobrenome, email, cpf, senha_hash, salt, tipo, plano_id, ativo
                FROM usuarios
                WHERE email = %s
            """, (email,))

            row = cursor.fetchone()

            if not row:
                return None

            usuario_id, nome, sobrenome, email, cpf, senha_hash_db, salt, tipo, plano_id, ativo = row

            if not ativo:
                return None

            senha_hash, _ = self.gerar_hash_senha(senha, salt)

            if senha_hash != senha_hash_db:
                return None

            self.executar(cursor, """
                UPDATE usuarios
                SET ultimo_acesso = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (usuario_id,))
            conn.commit()

            return {
                "id": usuario_id,
                "nome": nome,
                "sobrenome": sobrenome,
                "email": email,
                "cpf": cpf,
                "tipo": tipo,
                "plano_id": plano_id,
                "ativo": ativo,
            }

        finally:
            cursor.close()
            conn.close()

    # ========================================================================
    # SENHAS
    # ========================================================================
    def adicionar_senha(self, usuario_id: int, servico: str, usuario: str, senha: str, url: str = "", notas: str = ""):
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
            INSERT INTO senhas (usuario_id, servico, usuario, senha_criptografada, url, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (usuario_id, servico, usuario, senha, url, notas))
        conn.commit()
        conn.close()

    def listar_senhas_usuario(self, usuario_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'SELECT id, servico, usuario, url, notas FROM senhas WHERE usuario_id = ? ORDER BY servico',
                       (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "servico": row[1], "usuario": row[2], "url": row[3], "notas": row[4]} for row in rows]

    def obter_senha(self, id_senha: int, usuario_id: int) -> Optional[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'SELECT * FROM senhas WHERE id = ? AND usuario_id = ?', (id_senha, usuario_id))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "servico": row[2], "usuario": row[3], "senha_criptografada": row[4], "url": row[5],
                    "notas": row[6]}
        return None

    def deletar_senha(self, id_senha: int, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'DELETE FROM senhas WHERE id = ? AND usuario_id = ?', (id_senha, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # VÍDEOS
    # ========================================================================
    def listar_videos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
            SELECT id, titulo, destinatario, caminho_arquivo, categoria,
                   data_criacao, visibilidade
            FROM videos WHERE usuario_id = ? ORDER BY data_criacao DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "titulo": r[1], "destinatario": r[2], "caminho": r[3],
                 "categoria": r[4] if len(r) > 4 else "geral", "data": r[5],
                 "visibilidade": r[6] or "contatos"} for r in rows]

    def adicionar_video(self, usuario_id: int, titulo: str, destinatario: str, caminho_arquivo: str,
                        categoria: str = "geral"):
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
            INSERT INTO videos (usuario_id, titulo, destinatario, caminho_arquivo, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, titulo, destinatario, caminho_arquivo, categoria))
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return video_id

    def adicionar_video_com_acesso(
            self,
            usuario_id: int,
            titulo: str,
            destinatario: str,
            caminho_arquivo: str,
            contatos_ids: List[int],
            categoria: str = "geral",
            visibilidade: str = "contatos",
    ):
        if visibilidade not in ("privado", "contatos", "seletivo"):
            raise ValueError("Visibilidade inválida.")
        contatos_ids = list(dict.fromkeys(contatos_ids or []))
        if visibilidade == "seletivo" and not contatos_ids:
            raise ValueError("Selecione pelo menos um contato.")

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if self.usa_postgres:
                self.executar(cursor, '''
                    INSERT INTO videos (
                        usuario_id,
                        titulo,
                        destinatario,
                        caminho_arquivo,
                        categoria,
                        visibilidade
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (
                    usuario_id,
                    titulo,
                    destinatario,
                    caminho_arquivo,
                    categoria,
                    visibilidade,
                ))

                video_id = cursor.fetchone()[0]

            else:
                self.executar(cursor, '''
                    INSERT INTO videos (
                        usuario_id,
                        titulo,
                        destinatario,
                        caminho_arquivo,
                        categoria
                    )
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    usuario_id,
                    titulo,
                    destinatario,
                    caminho_arquivo,
                    categoria
                ))

                video_id = cursor.lastrowid

            for contato_id in contatos_ids:
                self.executar(cursor, '''
                    INSERT INTO videos_acesso (
                        video_id,
                        contato_id
                    )
                    SELECT %s, c.id
                    FROM contatos c
                    WHERE c.id = %s AND c.usuario_id = %s
                ''', (
                    video_id,
                    contato_id,
                    usuario_id,
                ))
                self.executar(cursor, """
                    INSERT INTO conteudo_permissoes (
                        tipo_conteudo, conteudo_id, contato_id
                    )
                    SELECT 'video', %s, c.id
                    FROM contatos c
                    WHERE c.id = %s AND c.usuario_id = %s
                    ON CONFLICT DO NOTHING
                """, (video_id, contato_id, usuario_id))

            if visibilidade == "seletivo":
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM conteudo_permissoes
                    WHERE tipo_conteudo = 'video'
                      AND conteudo_id = %s
                """, (video_id,))
                if cursor.fetchone()[0] == 0:
                    raise ValueError("Nenhum contato válido foi selecionado.")

            conn.commit()
            return video_id

        except Exception as e:
            conn.rollback()
            print("Erro ao adicionar vídeo com acesso:", e)
            raise e

        finally:
            cursor.close()
            conn.close()

    def deletar_video(self, id_video: int, usuario_id: int) -> bool:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,"SELECT caminho_arquivo FROM videos WHERE id = ? AND usuario_id = ?", (id_video, usuario_id))
        row = cursor.fetchone()
        if row:
            if row[0] and os.path.exists(row[0]):
                try:
                    os.remove(row[0])
                except:
                    pass
            self.executar(cursor,"DELETE FROM videos WHERE id = ? AND usuario_id = ?", (id_video, usuario_id))
            self.executar(cursor, """
                DELETE FROM conteudo_permissoes
                WHERE tipo_conteudo = 'video' AND conteudo_id = ?
            """, (id_video,))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def listar_contatos_por_video(self, video_id: int) -> List[Dict]:
        """Lista contatos que têm acesso a um vídeo específico"""
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
            SELECT c.id, c.nome, c.sobrenome
            FROM contatos c
            JOIN videos_acesso va ON c.id = va.contato_id
            WHERE va.video_id = ?
        ''', (video_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "nome_completo": f"{r[1]} {r[2]}".strip()} for r in rows]

    def listar_videos_por_contato(self, contato_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT 
                v.id,
                v.titulo,
                v.destinatario,
                v.caminho_arquivo,
                v.categoria,
                v.data_criacao
            FROM videos v
            JOIN contatos c ON c.usuario_id = v.usuario_id
            WHERE c.id = %s
              AND COALESCE(c.acesso_central_luto, 0) = 1
              AND (
                    v.visibilidade = 'contatos'
                    OR (
                        v.visibilidade = 'seletivo'
                        AND EXISTS (
                            SELECT 1 FROM conteudo_permissoes cp
                            WHERE cp.tipo_conteudo = 'video'
                              AND cp.conteudo_id = v.id
                              AND cp.contato_id = c.id
                        )
                    )
              )
            ORDER BY v.data_criacao DESC
        """, (contato_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "titulo": r[1],
            "destinatario": r[2],
            "caminho": r[3],
            "categoria": r[4],
            "data": r[5],
        } for r in rows]

    # ========================================================================
    # FOTOS
    # ========================================================================

    def adicionar_foto_com_acesso(
            self,
            usuario_id: int,
            titulo: str,
            descricao: str,
            categoria: str,
            caminho_arquivo: str,
            contatos_ids: List[int],
            visibilidade: str = "contatos",
    ):
        if visibilidade not in ("privado", "contatos", "seletivo"):
            raise ValueError("Visibilidade inválida.")
        contatos_ids = list(dict.fromkeys(contatos_ids or []))
        if visibilidade == "seletivo" and not contatos_ids:
            raise ValueError("Selecione pelo menos um contato.")

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                INSERT INTO fotos (
                    usuario_id,
                    titulo,
                    descricao,
                    categoria,
                    caminho_arquivo,
                    visibilidade
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                usuario_id,
                titulo,
                descricao,
                categoria,
                caminho_arquivo,
                visibilidade,
            ))

            foto_id = cursor.fetchone()[0]

            for contato_id in contatos_ids:
                self.executar(cursor, """
                    INSERT INTO fotos_contatos (
                        foto_id,
                        contato_id
                    )
                    SELECT %s, c.id
                    FROM contatos c
                    WHERE c.id = %s AND c.usuario_id = %s
                """, (
                    foto_id,
                    contato_id,
                    usuario_id,
                ))
                self.executar(cursor, """
                    INSERT INTO conteudo_permissoes (
                        tipo_conteudo, conteudo_id, contato_id
                    )
                    SELECT 'foto', %s, c.id
                    FROM contatos c
                    WHERE c.id = %s AND c.usuario_id = %s
                    ON CONFLICT DO NOTHING
                """, (foto_id, contato_id, usuario_id))

            if visibilidade == "seletivo":
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM conteudo_permissoes
                    WHERE tipo_conteudo = 'foto'
                      AND conteudo_id = %s
                """, (foto_id,))
                if cursor.fetchone()[0] == 0:
                    raise ValueError("Nenhum contato válido foi selecionado.")

            conn.commit()
            return foto_id

        except Exception as e:
            conn.rollback()
            print("Erro ao adicionar foto com acesso:", e)
            raise e

        finally:
            cursor.close()
            conn.close()

    def listar_fotos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT id, titulo, descricao, categoria, caminho_arquivo,
                   data_criacao, visibilidade
            FROM fotos
            WHERE usuario_id = %s
            ORDER BY data_criacao DESC
        """, (usuario_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "titulo": r[1],
            "descricao": r[2] or "",
            "categoria": r[3] or "",
            "caminho": r[4],
            "data_criacao": r[5],
            "visibilidade": r[6] or "contatos",
        } for r in rows]

    def listar_fotos_por_contato(self, contato_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT
                f.id,
                f.titulo,
                f.descricao,
                f.categoria,
                f.caminho_arquivo,
                f.data_criacao
            FROM fotos f
            JOIN contatos c ON c.usuario_id = f.usuario_id
            WHERE c.id = %s
              AND COALESCE(c.acesso_central_luto, 0) = 1
              AND (
                    f.visibilidade = 'contatos'
                    OR (
                        f.visibilidade = 'seletivo'
                        AND EXISTS (
                            SELECT 1 FROM conteudo_permissoes cp
                            WHERE cp.tipo_conteudo = 'foto'
                              AND cp.conteudo_id = f.id
                              AND cp.contato_id = c.id
                        )
                    )
              )
            ORDER BY f.data_criacao DESC
        """, (contato_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "titulo": r[1],
            "descricao": r[2] or "",
            "categoria": r[3] or "",
            "caminho": r[4],
            "data_criacao": r[5],
        } for r in rows]

    def listar_contatos_por_foto(self, foto_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT c.id, c.nome, c.sobrenome
            FROM contatos c
            JOIN fotos_contatos fc ON c.id = fc.contato_id
            WHERE fc.foto_id = %s
        """, (foto_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "nome_completo": "{} {}".format(r[1], r[2] or "").strip()
        } for r in rows]

    def buscar_fotos_por_texto(
            self,
            usuario_id: int,
            texto: str
    ):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            termo = f"%{texto.lower()}%"

            self.executar(cursor, """
                SELECT
                    id,
                    titulo,
                    descricao,
                    categoria,
                    caminho_arquivo
                FROM fotos
                WHERE usuario_id = %s
                AND (
                    LOWER(titulo) LIKE %s
                    OR LOWER(COALESCE(descricao,'')) LIKE %s
                    OR LOWER(COALESCE(categoria,'')) LIKE %s
                )
                LIMIT 5
            """, (
                usuario_id,
                termo,
                termo,
                termo
            ))

            rows = cursor.fetchall()

            return [{
                "id": r[0],
                "titulo": r[1],
                "descricao": r[2] or "",
                "categoria": r[3] or "",
                "caminho": r[4]
            } for r in rows]

        finally:
            cursor.close()
            conn.close()

    def buscar_fotos_por_contato_e_texto(
            self,
            contato_id: int,
            texto: str,
    ) -> List[Dict]:
        if not contato_id or not texto:
            return []

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            termo = f"%{texto.lower()}%"

            self.executar(cursor, """
                SELECT DISTINCT
                    f.id,
                    f.titulo,
                    f.descricao,
                    f.categoria,
                    f.caminho_arquivo
                FROM fotos f
                JOIN contatos c ON c.usuario_id = f.usuario_id
                WHERE c.id = ?
                  AND COALESCE(c.acesso_central_luto, 0) = 1
                  AND (
                        f.visibilidade = 'contatos'
                        OR (
                            f.visibilidade = 'seletivo'
                            AND EXISTS (
                                SELECT 1 FROM conteudo_permissoes cp
                                WHERE cp.tipo_conteudo = 'foto'
                                  AND cp.conteudo_id = f.id
                                  AND cp.contato_id = c.id
                            )
                        )
                  )
                  AND (
                    LOWER(COALESCE(f.titulo, '')) LIKE ?
                    OR LOWER(COALESCE(f.descricao, '')) LIKE ?
                    OR LOWER(COALESCE(f.categoria, '')) LIKE ?
                  )
                LIMIT 5
            """, (
                contato_id,
                termo,
                termo,
                termo,
            ))

            rows = cursor.fetchall()
            return [{
                "id": row[0],
                "titulo": row[1] or "",
                "descricao": row[2] or "",
                "categoria": row[3] or "",
                "caminho": row[4],
            } for row in rows]
        finally:
            cursor.close()
            conn.close()

    def deletar_foto(self, foto_id: int, usuario_id: int) -> bool:
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT caminho_arquivo
                FROM fotos
                WHERE id = %s AND usuario_id = %s
            """, (foto_id, usuario_id))

            row = cursor.fetchone()

            if not row:
                return False

            caminho = row[0]

            self.executar(cursor, """
                DELETE FROM fotos_contatos
                WHERE foto_id = %s
            """, (foto_id,))
            self.executar(cursor, """
                DELETE FROM conteudo_permissoes
                WHERE tipo_conteudo = 'foto' AND conteudo_id = %s
            """, (foto_id,))

            self.executar(cursor, """
                DELETE FROM fotos
                WHERE id = %s AND usuario_id = %s
            """, (foto_id, usuario_id))

            conn.commit()

            if caminho and os.path.exists(caminho):
                try:
                    os.remove(caminho)
                except Exception:
                    pass

            return True

        except Exception as e:
            conn.rollback()
            print("Erro ao deletar foto:", e)
            raise e

        finally:
            cursor.close()
            conn.close()
    # ========================================================================
    # MEMORIAS E videos
    # ========================================================================

    def associar_video_memoria(self, memoria_id: int, video_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                INSERT INTO memoria_videos (memoria_id, video_id)
                VALUES (%s, %s)
            """, (memoria_id, video_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def listar_videos_memoria(self, memoria_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT v.id, v.titulo, v.destinatario, v.categoria, v.caminho_arquivo
            FROM videos v
            JOIN memoria_videos mv ON mv.video_id = v.id
            WHERE mv.memoria_id = %s
            ORDER BY v.data_criacao DESC
        """, (memoria_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "titulo": r[1],
            "destinatario": r[2] or "",
            "categoria": r[3] or "",
            "caminho": r[4],
        } for r in rows]

    # ========================================================================
    # MEMORIAS E FOTOS
    # ========================================================================

    def listar_memorias_usuario(self, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT id, titulo, conteudo, categoria, data_criacao
            FROM memorias
            WHERE usuario_id = %s
            ORDER BY data_criacao DESC
        """, (usuario_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "titulo": r[1] or "Memória sem título",
            "conteudo": r[2] or "",
            "categoria": r[3] or "",
            "data_criacao": r[4],
        } for r in rows]

    def associar_foto_memoria(self, memoria_id: int, foto_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                INSERT INTO memoria_fotos (memoria_id, foto_id)
                VALUES (%s, %s)
            """, (memoria_id, foto_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def listar_fotos_memoria(self, memoria_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT f.id, f.titulo, f.descricao, f.categoria, f.caminho_arquivo
            FROM fotos f
            JOIN memoria_fotos mf ON mf.foto_id = f.id
            WHERE mf.memoria_id = %s
            ORDER BY f.data_criacao DESC
        """, (memoria_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "titulo": r[1],
            "descricao": r[2] or "",
            "categoria": r[3] or "",
            "caminho": r[4],
        } for r in rows]

    # ========================================================================
    # CONTATOS
    # ========================================================================
    def adicionar_contato(self, usuario_id: int, nome: str, sobrenome: str, email: str,
                          telefone: str = "", whatsapp: str = "", parentesco: str = "",
                          data_nascimento: str = "", datas_especiais: str = "",
                          is_prioridade: int = 0, prioridade_order: int = 0,
                          acesso_central_luto: int = 0, chave_acesso: str = "",):
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
            INSERT INTO contatos (usuario_id, nome, sobrenome, email, telefone, whatsapp, parentesco, 
                                  data_nascimento, datas_especiais, is_prioridade, prioridade_order, 
                                  acesso_central_luto, chave_acesso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome, sobrenome, email, telefone, whatsapp, parentesco,
              data_nascimento, datas_especiais, is_prioridade, prioridade_order, acesso_central_luto, chave_acesso))
        conn.commit()
        conn.close()

    def listar_contatos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,'''
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
            "acesso_central_luto": r[11] or 0,
            "chave_acesso": r[12] or ""
        } for r in rows]

    def listar_memorias_por_contato(self, contato_id: int) -> List[Dict]:
        if not contato_id:
            return []

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    m.id, m.categoria, m.titulo, m.conteudo,
                    m.origem, m.data_criacao, m.local,
                    m.data_evento, m.pessoas_relacionadas
                FROM memorias m
                JOIN contatos c ON c.usuario_id = m.usuario_id
                WHERE c.id = %s
                  AND COALESCE(c.acesso_central_luto, 0) = 1
                  AND (
                        m.visibilidade = 'contatos'
                        OR (
                            m.visibilidade = 'seletivo'
                            AND EXISTS (
                                SELECT 1 FROM conteudo_permissoes cp
                                WHERE cp.tipo_conteudo = 'memoria'
                                  AND cp.conteudo_id = m.id
                                  AND cp.contato_id = c.id
                            )
                        )
                  )
                ORDER BY m.data_criacao DESC
            """, (contato_id,))
            return [{
                "id": row[0],
                "categoria": row[1] or "",
                "titulo": row[2] or "Memória sem título",
                "conteudo": row[3] or "",
                "origem": row[4] or "",
                "data_criacao": row[5],
                "local": row[6],
                "data_evento": row[7],
                "pessoas_relacionadas": row[8],
            } for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def atualizar_visibilidade_conteudo(
            self,
            tipo_conteudo: str,
            conteudo_id: int,
            usuario_dono_id: int,
            visibilidade: str,
            contatos_ids: List[int],
    ) -> bool:
        tabelas = {
            "memoria": "memorias",
            "foto": "fotos",
            "video": "videos",
        }
        tabela = tabelas.get(tipo_conteudo)
        if not tabela or visibilidade not in ("privado", "contatos", "seletivo"):
            return False
        contatos_ids = list(dict.fromkeys(contatos_ids or []))
        if visibilidade == "seletivo" and not contatos_ids:
            return False

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"""
                UPDATE {tabela}
                SET visibilidade = %s
                WHERE id = %s AND usuario_id = %s
                RETURNING id
                """,
                (visibilidade, conteudo_id, usuario_dono_id),
            )
            if not cursor.fetchone():
                conn.rollback()
                return False

            cursor.execute("""
                DELETE FROM conteudo_permissoes
                WHERE tipo_conteudo = %s AND conteudo_id = %s
            """, (tipo_conteudo, conteudo_id))
            if tipo_conteudo == "foto":
                cursor.execute(
                    "DELETE FROM fotos_contatos WHERE foto_id = %s",
                    (conteudo_id,),
                )
            elif tipo_conteudo == "video":
                cursor.execute(
                    "DELETE FROM videos_acesso WHERE video_id = %s",
                    (conteudo_id,),
                )

            if visibilidade == "seletivo":
                for contato_id in contatos_ids:
                    cursor.execute("""
                        INSERT INTO conteudo_permissoes (
                            tipo_conteudo, conteudo_id, contato_id
                        )
                        SELECT %s, %s, c.id
                        FROM contatos c
                        WHERE c.id = %s AND c.usuario_id = %s
                        ON CONFLICT DO NOTHING
                    """, (
                        tipo_conteudo,
                        conteudo_id,
                        contato_id,
                        usuario_dono_id,
                    ))
                    if tipo_conteudo == "foto":
                        cursor.execute("""
                            INSERT INTO fotos_contatos (foto_id, contato_id)
                            SELECT %s, c.id
                            FROM contatos c
                            WHERE c.id = %s AND c.usuario_id = %s
                        """, (conteudo_id, contato_id, usuario_dono_id))
                    elif tipo_conteudo == "video":
                        cursor.execute("""
                            INSERT INTO videos_acesso (video_id, contato_id)
                            SELECT %s, c.id
                            FROM contatos c
                            WHERE c.id = %s AND c.usuario_id = %s
                        """, (conteudo_id, contato_id, usuario_dono_id))

            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def listar_contatos_permitidos_conteudo(
            self,
            tipo_conteudo: str,
            conteudo_id: int,
            usuario_dono_id: int,
    ) -> List[int]:
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT cp.contato_id
                FROM conteudo_permissoes cp
                JOIN contatos c ON c.id = cp.contato_id
                WHERE cp.tipo_conteudo = %s
                  AND cp.conteudo_id = %s
                  AND c.usuario_id = %s
                ORDER BY cp.contato_id
            """, (tipo_conteudo, conteudo_id, usuario_dono_id))
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def listar_historias_compartilhadas_comigo(self, email: str) -> List[Dict]:
        email_normalizado = (email or "").strip().lower()
        if not email_normalizado:
            return []

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT
                    u.id,
                    u.nome,
                    u.sobrenome,
                    u.email,
                    c.id,
                    c.chave_acesso,
                    c.parentesco
                FROM contatos c
                JOIN usuarios u ON u.id = c.usuario_id
                WHERE LOWER(TRIM(c.email)) = ?
                  AND COALESCE(c.acesso_central_luto, 0) = 1
                  AND COALESCE(u.ativo, 1) = 1
                ORDER BY u.nome, u.sobrenome, c.id
            """, (email_normalizado,))

            rows = cursor.fetchall()
            historias = []
            usuarios_adicionados = set()

            for row in rows:
                usuario_id = row[0]
                if usuario_id in usuarios_adicionados:
                    continue

                usuarios_adicionados.add(usuario_id)
                historias.append({
                    "usuario_id": usuario_id,
                    "nome": row[1] or "",
                    "sobrenome": row[2] or "",
                    "nome_completo": f"{row[1] or ''} {row[2] or ''}".strip(),
                    "email": row[3] or "",
                    "contato_id": row[4],
                    "chave_acesso": row[5] or "",
                    "parentesco": row[6] or "",
                })

            return historias
        finally:
            cursor.close()
            conn.close()

    def usuario_pode_acessar_historia(
            self,
            email: str,
            usuario_id: int,
    ) -> Optional[Dict]:
        email_normalizado = (email or "").strip().lower()
        if not email_normalizado or not usuario_id:
            return None

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT
                    c.id,
                    c.parentesco,
                    c.chave_acesso,
                    u.id,
                    u.nome,
                    u.sobrenome,
                    u.email
                FROM contatos c
                JOIN usuarios u ON u.id = c.usuario_id
                WHERE LOWER(TRIM(c.email)) = ?
                  AND c.usuario_id = ?
                  AND COALESCE(c.acesso_central_luto, 0) = 1
                  AND COALESCE(u.ativo, 1) = 1
                ORDER BY c.id
                LIMIT 1
            """, (email_normalizado, usuario_id))

            row = cursor.fetchone()
            if not row:
                return None

            return {
                "contato_id": row[0],
                "parentesco": row[1] or "",
                "chave_acesso": row[2] or "",
                "usuario_id": row[3],
                "nome": row[4] or "",
                "sobrenome": row[5] or "",
                "nome_completo": f"{row[4] or ''} {row[5] or ''}".strip(),
                "email": row[6] or "",
            }
        finally:
            cursor.close()
            conn.close()

    def obter_usuario_por_id(self, usuario_id: int) -> Optional[Dict]:
        if not usuario_id:
            return None

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT id, nome, sobrenome, email, tipo, plano_id, ativo
                FROM usuarios
                WHERE id = ?
            """, (usuario_id,))

            row = cursor.fetchone()
            if not row:
                return None

            return {
                "id": row[0],
                "nome": row[1] or "",
                "sobrenome": row[2] or "",
                "nome_completo": f"{row[1] or ''} {row[2] or ''}".strip(),
                "email": row[3] or "",
                "tipo": row[4] or "usuario",
                "plano_id": row[5],
                "ativo": row[6] if row[6] is not None else 1,
            }
        finally:
            cursor.close()
            conn.close()

    def obter_ultimo_acesso_historia(
            self,
            email_visualizador: str,
            dono_historia_id: int,
    ):
        acesso = self.usuario_pode_acessar_historia(
            email_visualizador,
            dono_historia_id,
        )
        if not acesso:
            return None

        email_normalizado = (email_visualizador or "").strip().lower()
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT ultimo_acesso_em
                FROM historias_acessos
                WHERE usuario_visualizador_email = %s
                  AND dono_historia_id = %s
            """, (email_normalizado, dono_historia_id))

            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            cursor.close()
            conn.close()

    def registrar_acesso_historia(
            self,
            email_visualizador: str,
            dono_historia_id: int,
    ) -> bool:
        email_normalizado = (email_visualizador or "").strip().lower()
        if not email_normalizado or not dono_historia_id:
            return False

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO historias_acessos (
                    usuario_visualizador_email,
                    dono_historia_id,
                    ultimo_acesso_em
                )
                SELECT
                    %s,
                    c.usuario_id,
                    NOW()
                FROM contatos c
                WHERE LOWER(TRIM(c.email)) = %s
                  AND c.usuario_id = %s
                  AND COALESCE(c.acesso_central_luto, 0) = 1
                ORDER BY c.id
                LIMIT 1
                ON CONFLICT (
                    usuario_visualizador_email,
                    dono_historia_id
                )
                DO UPDATE SET ultimo_acesso_em = NOW()
                RETURNING id
            """, (
                email_normalizado,
                email_normalizado,
                dono_historia_id,
            ))

            row = cursor.fetchone()
            conn.commit()
            return bool(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def contar_novidades_historia(
            self,
            email_visualizador: str,
            dono_historia_id: int,
    ) -> Dict[str, int]:
        acesso = self.usuario_pode_acessar_historia(
            email_visualizador,
            dono_historia_id,
        )
        if not acesso:
            return {
                "memorias": 0,
                "fotos": 0,
                "videos": 0,
                "total": 0,
            }

        ultimo_acesso = self.obter_ultimo_acesso_historia(
            email_visualizador,
            dono_historia_id,
        )
        contato_id = acesso["contato_id"]

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if ultimo_acesso is None:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM memorias m
                    WHERE m.usuario_id = %s
                      AND (
                            m.visibilidade = 'contatos'
                            OR (
                                m.visibilidade = 'seletivo'
                                AND EXISTS (
                                    SELECT 1 FROM conteudo_permissoes cp
                                    WHERE cp.tipo_conteudo = 'memoria'
                                      AND cp.conteudo_id = m.id
                                      AND cp.contato_id = %s
                                )
                            )
                      )
                """, (dono_historia_id, contato_id))
                memorias = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(DISTINCT f.id)
                    FROM fotos f
                    WHERE f.usuario_id = %s
                      AND (
                            f.visibilidade = 'contatos'
                            OR (
                                f.visibilidade = 'seletivo'
                                AND EXISTS (
                                    SELECT 1 FROM conteudo_permissoes cp
                                    WHERE cp.tipo_conteudo = 'foto'
                                      AND cp.conteudo_id = f.id
                                      AND cp.contato_id = %s
                                )
                            )
                      )
                """, (dono_historia_id, contato_id))
                fotos = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(DISTINCT v.id)
                    FROM videos v
                    WHERE v.usuario_id = %s
                      AND (
                            v.visibilidade = 'contatos'
                            OR (
                                v.visibilidade = 'seletivo'
                                AND EXISTS (
                                    SELECT 1 FROM conteudo_permissoes cp
                                    WHERE cp.tipo_conteudo = 'video'
                                      AND cp.conteudo_id = v.id
                                      AND cp.contato_id = %s
                                )
                            )
                      )
                """, (dono_historia_id, contato_id))
                videos = cursor.fetchone()[0]
            else:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM memorias m
                    WHERE m.usuario_id = %s
                      AND m.data_criacao > %s
                      AND (
                            m.visibilidade = 'contatos'
                            OR (
                                m.visibilidade = 'seletivo'
                                AND EXISTS (
                                    SELECT 1 FROM conteudo_permissoes cp
                                    WHERE cp.tipo_conteudo = 'memoria'
                                      AND cp.conteudo_id = m.id
                                      AND cp.contato_id = %s
                                )
                            )
                      )
                """, (dono_historia_id, ultimo_acesso, contato_id))
                memorias = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(DISTINCT f.id)
                    FROM fotos f
                    WHERE f.usuario_id = %s
                      AND f.data_criacao > %s
                      AND (
                            f.visibilidade = 'contatos'
                            OR (
                                f.visibilidade = 'seletivo'
                                AND EXISTS (
                                    SELECT 1 FROM conteudo_permissoes cp
                                    WHERE cp.tipo_conteudo = 'foto'
                                      AND cp.conteudo_id = f.id
                                      AND cp.contato_id = %s
                                )
                            )
                      )
                """, (dono_historia_id, ultimo_acesso, contato_id))
                fotos = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(DISTINCT v.id)
                    FROM videos v
                    WHERE v.usuario_id = %s
                      AND v.data_criacao > %s
                      AND (
                            v.visibilidade = 'contatos'
                            OR (
                                v.visibilidade = 'seletivo'
                                AND EXISTS (
                                    SELECT 1 FROM conteudo_permissoes cp
                                    WHERE cp.tipo_conteudo = 'video'
                                      AND cp.conteudo_id = v.id
                                      AND cp.contato_id = %s
                                )
                            )
                      )
                """, (dono_historia_id, ultimo_acesso, contato_id))
                videos = cursor.fetchone()[0]

            memorias = int(memorias or 0)
            fotos = int(fotos or 0)
            videos = int(videos or 0)

            return {
                "memorias": memorias,
                "fotos": fotos,
                "videos": videos,
                "total": memorias + fotos + videos,
            }
        finally:
            cursor.close()
            conn.close()

    def criar_contribuicao(
            self,
            email_contribuidor: str,
            nome_contribuidor: str,
            usuario_dono_id: int,
            memoria_id: int,
            texto: str,
            tipo_contribuicao: str = "texto",
            arquivo_url: str = None,
            arquivo_nome: str = None,
            arquivo_tipo: str = None,
            arquivo_tamanho: int = None,
            storage_bucket: str = None,
            storage_path: str = None,
    ) -> Optional[int]:
        email_normalizado = (email_contribuidor or "").strip().lower()
        nome_normalizado = (nome_contribuidor or "").strip() or email_normalizado
        texto_normalizado = (texto or "").strip()

        if (
            not email_normalizado
            or not usuario_dono_id
            or not memoria_id
            or tipo_contribuicao not in (
                "texto", "foto", "video", "texto_foto", "texto_video"
            )
            or (not texto_normalizado and not arquivo_url)
        ):
            return None

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO contribuicoes (
                    usuario_dono_id,
                    usuario_contribuidor_email,
                    usuario_contribuidor_nome,
                    tipo_conteudo,
                    conteudo_id,
                    tipo_contribuicao,
                    texto,
                    arquivo_url,
                    arquivo_nome,
                    arquivo_tipo,
                    arquivo_tamanho,
                    storage_bucket,
                    storage_path,
                    status,
                    criado_em
                )
                SELECT
                    m.usuario_id,
                    %s,
                    %s,
                    'memoria',
                    m.id,
                    %s,
                    %s,
                    %s, %s, %s, %s, %s, %s,
                    'pendente',
                    NOW()
                FROM memorias m
                WHERE m.id = %s
                  AND m.usuario_id = %s
                  AND (
                        m.visibilidade = 'contatos'
                        OR (
                            m.visibilidade = 'seletivo'
                            AND EXISTS (
                                SELECT 1 FROM conteudo_permissoes cp
                                JOIN contatos c2 ON c2.id = cp.contato_id
                                WHERE cp.tipo_conteudo = 'memoria'
                                  AND cp.conteudo_id = m.id
                                  AND LOWER(TRIM(c2.email)) = %s
                            )
                        )
                  )
                  AND EXISTS (
                      SELECT 1
                      FROM contatos c
                      WHERE c.usuario_id = m.usuario_id
                        AND LOWER(TRIM(c.email)) = %s
                        AND COALESCE(c.acesso_central_luto, 0) = 1
                  )
                RETURNING id
            """, (
                email_normalizado,
                nome_normalizado,
                tipo_contribuicao,
                texto_normalizado,
                arquivo_url,
                arquivo_nome,
                arquivo_tipo,
                arquivo_tamanho,
                storage_bucket,
                storage_path,
                memoria_id,
                usuario_dono_id,
                email_normalizado,
                email_normalizado,
            ))

            row = cursor.fetchone()
            conn.commit()
            return row[0] if row else None
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def pode_contribuir_memoria(
            self,
            email_contribuidor: str,
            usuario_dono_id: int,
            memoria_id: int,
    ) -> bool:
        email = (email_contribuidor or "").strip().lower()
        if not email or not usuario_dono_id or not memoria_id:
            return False
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 1
                FROM memorias m
                JOIN contatos c ON c.usuario_id = m.usuario_id
                WHERE m.id = %s
                  AND m.usuario_id = %s
                  AND LOWER(TRIM(c.email)) = %s
                  AND COALESCE(c.acesso_central_luto, 0) = 1
                  AND (
                        m.visibilidade = 'contatos'
                        OR (
                            m.visibilidade = 'seletivo'
                            AND EXISTS (
                                SELECT 1 FROM conteudo_permissoes cp
                                WHERE cp.tipo_conteudo = 'memoria'
                                  AND cp.conteudo_id = m.id
                                  AND cp.contato_id = c.id
                            )
                        )
                  )
                LIMIT 1
            """, (memoria_id, usuario_dono_id, email))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    def criar_contribuicao_texto(
            self,
            email_contribuidor: str,
            nome_contribuidor: str,
            usuario_dono_id: int,
            memoria_id: int,
            texto: str,
    ) -> Optional[int]:
        return self.criar_contribuicao(
            email_contribuidor,
            nome_contribuidor,
            usuario_dono_id,
            memoria_id,
            texto,
            tipo_contribuicao="texto",
        )

    def contar_contribuicoes_pendentes(self, usuario_dono_id: int) -> int:
        if not usuario_dono_id:
            return 0

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM contribuicoes
                WHERE usuario_dono_id = %s
                  AND status = 'pendente'
            """, (usuario_dono_id,))
            return int(cursor.fetchone()[0] or 0)
        finally:
            cursor.close()
            conn.close()

    def listar_contribuicoes_pendentes(
            self,
            usuario_dono_id: int,
    ) -> List[Dict]:
        if not usuario_dono_id:
            return []

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    c.id,
                    c.usuario_contribuidor_nome,
                    c.usuario_contribuidor_email,
                    c.tipo_conteudo,
                    c.conteudo_id,
                    c.tipo_contribuicao,
                    c.texto,
                    c.arquivo_url,
                    c.arquivo_nome,
                    c.arquivo_tipo,
                    c.arquivo_tamanho,
                    c.storage_bucket,
                    c.storage_path,
                    c.criado_em,
                    m.titulo
                FROM contribuicoes c
                JOIN memorias m
                  ON c.tipo_conteudo = 'memoria'
                 AND m.id = c.conteudo_id
                 AND m.usuario_id = c.usuario_dono_id
                WHERE c.usuario_dono_id = %s
                  AND c.status = 'pendente'
                ORDER BY c.criado_em ASC
            """, (usuario_dono_id,))

            rows = cursor.fetchall()
            return [{
                "id": row[0],
                "contribuidor_nome": row[1] or row[2] or "Pessoa convidada",
                "contribuidor_email": row[2] or "",
                "tipo_conteudo": row[3],
                "conteudo_id": row[4],
                "tipo_contribuicao": row[5],
                "texto": row[6] or "",
                "arquivo_url": row[7],
                "arquivo_nome": row[8] or "",
                "arquivo_tipo": row[9] or "",
                "arquivo_tamanho": row[10] or 0,
                "storage_bucket": row[11] or "",
                "storage_path": row[12] or "",
                "criado_em": row[13],
                "memoria_titulo": row[14] or "História sem título",
            } for row in rows]
        finally:
            cursor.close()
            conn.close()

    def avaliar_contribuicao(
            self,
            contribuicao_id: int,
            usuario_dono_id: int,
            decisao: str,
    ) -> bool:
        if decisao not in ("aprovado", "rejeitado"):
            return False
        if not contribuicao_id or not usuario_dono_id:
            return False

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE contribuicoes
                SET
                    status = %s,
                    avaliado_em = NOW(),
                    avaliado_por = %s
                WHERE id = %s
                  AND usuario_dono_id = %s
                  AND status = 'pendente'
                RETURNING id
            """, (
                decisao,
                usuario_dono_id,
                contribuicao_id,
                usuario_dono_id,
            ))

            row = cursor.fetchone()
            conn.commit()
            return bool(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def listar_contribuicoes_aprovadas_memorias(
            self,
            usuario_dono_id: int,
    ) -> Dict[int, List[Dict]]:
        if not usuario_dono_id:
            return {}

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    c.id,
                    c.conteudo_id,
                    c.usuario_contribuidor_nome,
                    c.usuario_contribuidor_email,
                    c.texto,
                    c.arquivo_url,
                    c.arquivo_nome,
                    c.arquivo_tipo,
                    c.criado_em,
                    c.avaliado_em
                FROM contribuicoes c
                JOIN memorias m
                  ON m.id = c.conteudo_id
                 AND m.usuario_id = c.usuario_dono_id
                WHERE c.usuario_dono_id = %s
                  AND c.tipo_conteudo = 'memoria'
                  AND c.status = 'aprovado'
                ORDER BY c.criado_em ASC
            """, (usuario_dono_id,))

            resultado = {}
            for row in cursor.fetchall():
                memoria_id = row[1]
                resultado.setdefault(memoria_id, []).append({
                    "id": row[0],
                    "contribuidor_nome": row[2] or row[3] or "Pessoa convidada",
                    "contribuidor_email": row[3] or "",
                    "texto": row[4] or "",
                    "arquivo_url": row[5],
                    "arquivo_nome": row[6] or "",
                    "arquivo_tipo": row[7] or "",
                    "criado_em": row[8],
                    "avaliado_em": row[9],
                })

            return resultado
        finally:
            cursor.close()
            conn.close()

    def listar_memorias_usuario(self, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT id, categoria, titulo, conteudo, origem, data_criacao,
                   visibilidade, local, data_evento, pessoas_relacionadas
            FROM memorias
            WHERE usuario_id = ?
            ORDER BY data_criacao DESC
        """, (usuario_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "categoria": r[1],
            "titulo": r[2],
            "conteudo": r[3],
            "origem": r[4],
            "data_criacao": r[5],
            "visibilidade": r[6] or "contatos",
            "local": r[7],
            "data_evento": r[8],
            "pessoas_relacionadas": r[9],
        } for r in rows]

    def atualizar_foto_usuario(self, usuario_id: int, caminho_foto: str):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                UPDATE usuarios
                SET foto_perfil = %s
                WHERE id = %s
            """, (caminho_foto, usuario_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def atualizar_foto_contato(self, contato_id: int, usuario_id: int, caminho_foto: str):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                UPDATE contatos
                SET foto_perfil = %s
                WHERE id = %s
                  AND usuario_id = %s
            """, (caminho_foto, contato_id, usuario_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def salvar_memoria(
            self,
            usuario_id: int,
            conteudo: str,
            titulo: str = "Memória registrada com o Curador",
            categoria: str = "livre",
            origem: str = "curador",
            local: str = None,
            data_evento: str = None,
            pessoas_relacionadas: str = None,
            visibilidade: str = "contatos",
            contatos_ids: List[int] = None,
    ):
        if visibilidade not in ("privado", "contatos", "seletivo"):
            raise ValueError("Visibilidade inválida.")
        contatos_ids = list(dict.fromkeys(contatos_ids or []))
        if visibilidade == "seletivo" and not contatos_ids:
            raise ValueError("Selecione pelo menos um contato.")

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                INSERT INTO memorias (
                    usuario_id,
                    categoria,
                    titulo,
                    conteudo,
                    origem,
                    local,
                    data_evento,
                    pessoas_relacionadas
                    , visibilidade
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                usuario_id,
                categoria,
                titulo,
                conteudo,
                origem,
                local,
                data_evento,
                pessoas_relacionadas,
                visibilidade,
            ))

            memoria_id = cursor.fetchone()[0]
            if visibilidade == "seletivo":
                for contato_id in contatos_ids or []:
                    cursor.execute("""
                        INSERT INTO conteudo_permissoes (
                            tipo_conteudo, conteudo_id, contato_id
                        )
                        SELECT 'memoria', %s, c.id
                        FROM contatos c
                        WHERE c.id = %s AND c.usuario_id = %s
                        ON CONFLICT DO NOTHING
                    """, (memoria_id, contato_id, usuario_id))
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM conteudo_permissoes
                    WHERE tipo_conteudo = 'memoria'
                      AND conteudo_id = %s
                """, (memoria_id,))
                if cursor.fetchone()[0] == 0:
                    raise ValueError("Nenhum contato válido foi selecionado.")
            conn.commit()
            return memoria_id

        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def contar_contatos_usuario(self, usuario_id: int) -> int:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, 'SELECT COUNT(*) FROM contatos WHERE usuario_id = ?', (usuario_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def listar_fotos_por_memorias_usuario(self, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT
                    mf.memoria_id,
                    f.id,
                    f.titulo,
                    f.descricao,
                    f.categoria,
                    f.caminho_arquivo
                FROM memoria_fotos mf
                JOIN fotos f ON f.id = mf.foto_id
                WHERE f.usuario_id = %s
                ORDER BY f.data_criacao DESC
            """, (usuario_id,))

            rows = cursor.fetchall()

            fotos_por_memoria = {}

            for r in rows:
                memoria_id = r[0]
                fotos_por_memoria.setdefault(memoria_id, []).append({
                    "id": r[1],
                    "titulo": r[2],
                    "descricao": r[3] or "",
                    "categoria": r[4] or "",
                    "caminho": r[5],
                })

            return fotos_por_memoria

        finally:
            cursor.close()
            conn.close()

    def obter_foto_usuario(self, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT foto_perfil
                FROM usuarios
                WHERE id = %s
            """, (usuario_id,))

            row = cursor.fetchone()
            return row[0] if row and row[0] else None

        finally:
            cursor.close()
            conn.close()

    def criar_data_importante(
            self,
            usuario_id: int,
            titulo: str,
            data_evento: str,
            tipo: str = "",
            contato_id: int = None,
            recorrente: bool = True,
            observacoes: str = ""
    ):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                INSERT INTO datas_importantes (
                    usuario_id,
                    contato_id,
                    titulo,
                    data_evento,
                    tipo,
                    recorrente,
                    observacoes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                usuario_id,
                contato_id,
                titulo,
                data_evento,
                tipo,
                recorrente,
                observacoes
            ))

            data_id = cursor.fetchone()[0]
            conn.commit()
            return data_id

        finally:
            cursor.close()
            conn.close()

    def listar_datas_importantes_usuario(self, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT
                    d.id,
                    d.titulo,
                    d.data_evento,
                    d.tipo,
                    d.recorrente,
                    d.observacoes,
                    c.nome,
                    c.sobrenome
                FROM datas_importantes d
                LEFT JOIN contatos c ON c.id = d.contato_id
                WHERE d.usuario_id = %s
                ORDER BY d.data_evento
            """, (usuario_id,))

            rows = cursor.fetchall()

            return [{
                "id": r[0],
                "titulo": r[1],
                "data_evento": r[2],
                "tipo": r[3] or "",
                "recorrente": r[4],
                "observacoes": r[5] or "",
                "contato_nome": "{} {}".format(r[6] or "", r[7] or "").strip(),
            } for r in rows]

        finally:
            cursor.close()
            conn.close()

    def deletar_data_importante(self, data_id: int, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                DELETE FROM datas_importantes
                WHERE id = %s AND usuario_id = %s
            """, (data_id, usuario_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def registrar_interesse_plano(
            self,
            usuario_id: int,
            plano: str,
            valor: float
    ):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                INSERT INTO interesses_planos (
                    usuario_id,
                    plano,
                    valor
                )
                VALUES (%s, %s, %s)
            """, (
                usuario_id,
                plano,
                valor
            ))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def listar_videos_por_memorias_usuario(self, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT
                    mv.memoria_id,
                    v.id,
                    v.titulo,
                    v.destinatario,
                    v.categoria,
                    v.caminho_arquivo
                FROM memoria_videos mv
                JOIN videos v ON v.id = mv.video_id
                WHERE v.usuario_id = %s
                ORDER BY v.data_criacao DESC
            """, (usuario_id,))

            rows = cursor.fetchall()

            videos_por_memoria = {}

            for r in rows:
                memoria_id = r[0]
                videos_por_memoria.setdefault(memoria_id, []).append({
                    "id": r[1],
                    "titulo": r[2],
                    "destinatario": r[3] or "",
                    "categoria": r[4] or "",
                    "caminho": r[5],
                })

            return videos_por_memoria

        finally:
            cursor.close()
            conn.close()

    def obter_contato_por_chave(self, chave_acesso: str, email_falecido: str = None) -> Optional[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()
        if email_falecido:
            self.executar(cursor, '''
                SELECT c.id, c.nome, 
                c.sobrenome, 
                c.email, 
                c.telefone, 
                c.whatsapp, 
                c.acesso_central_luto, 
                u.id as usuario_id, 
                u.nome as falecido_nome, 
                c.parentesco
                FROM contatos c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.chave_acesso = ? AND u.email = ?
            ''', (chave_acesso, email_falecido))
        else:
            self.executar(cursor, '''
                SELECT c.id, 
                c.nome, 
                c.sobrenome, 
                c.email, 
                c.telefone, 
                c.whatsapp, 
                c.acesso_central_luto, 
                u.id as usuario_id, 
                u.nome as falecido_nome,
                c.parentesco
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
                "falecido_nome": row[8],
                "parentesco": row[9] or ""
            }
        return None

    def deletar_contato(self, id_contato: int, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor,"DELETE FROM contatos WHERE id = ? AND usuario_id = ?", (id_contato, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # AGENDAMENTOS (LEMBRANÇAS PROGRAMADAS)
    # ========================================================================
    def criar_agendamento(
            self,
            usuario_id: int,
            contato_id: int,
            tipo: str,
            data_envio: str,
            data_termino: str = "",
            conteudo: str = "",
            video_id: int = None,
            gerar_por_ia: int = 0
    ) -> int:
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            if not data_termino:
                data_termino = None
            self.executar(cursor, """
                INSERT INTO agendamentos (
                    usuario_id,
                    contato_id,
                    tipo,
                    data_envio,
                    data_termino,
                    conteudo,
                    video_id,
                    gerar_por_ia,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'agendado')
                RETURNING id
            """, (
                usuario_id,
                contato_id,
                tipo,
                data_envio,
                data_termino,
                conteudo,
                video_id,
                gerar_por_ia
            ))

            agendamento_id = cursor.fetchone()[0]
            conn.commit()
            return agendamento_id

        except Exception as e:
            conn.rollback()
            print("Erro ao criar agendamento:", e)
            raise e

        finally:
            cursor.close()
            conn.close()

    def listar_agendamentos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, """
            SELECT 
                a.id,
                a.tipo,
                a.data_envio,
                a.data_termino,
                a.conteudo,
                a.status,
                c.nome,
                c.sobrenome,
                c.email,
                a.video_id
            FROM agendamentos a
            JOIN contatos c ON a.contato_id = c.id
            WHERE a.usuario_id = %s
            ORDER BY a.data_envio
        """, (usuario_id,))

        rows = cursor.fetchall()
        conn.close()

        return [{
            "id": r[0],
            "tipo": r[1],
            "data_envio": r[2],
            "data_termino": r[3],
            "conteudo": r[4] or "",
            "status": r[5],
            "contato_nome": "{} {}".format(r[6], r[7] or "").strip(),
            "contato_email": r[8],
            "video_id": r[9],
        } for r in rows]

    def deletar_agendamento(self, id_agendamento: int, usuario_id: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                DELETE FROM agendamentos
                WHERE id = %s AND usuario_id = %s
            """, (id_agendamento, usuario_id))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def listar_agendamentos_pendentes(self) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                SELECT
                    a.id,
                    a.usuario_id,
                    a.contato_id,
                    a.tipo,
                    a.data_envio,
                    a.data_termino,
                    a.conteudo,
                    a.video_id,
                    a.gerar_por_ia,
                    a.status,
                    c.nome,
                    c.sobrenome,
                    c.email
                FROM agendamentos a
                JOIN contatos c ON c.id = a.contato_id
                WHERE a.status = %s
                  AND a.data_envio <= CURRENT_DATE
                ORDER BY a.data_envio ASC
            """, ("agendado",))

            rows = cursor.fetchall()

            return [{
                "id": r[0],
                "usuario_id": r[1],
                "contato_id": r[2],
                "tipo": r[3],
                "data_envio": r[4],
                "data_termino": r[5],
                "conteudo": r[6] or "",
                "video_id": r[7],
                "gerar_por_ia": r[8],
                "status": r[9],
                "contato_nome": "{} {}".format(r[10], r[11] or "").strip(),
                "contato_email": r[12],
            } for r in rows]

        finally:
            cursor.close()
            conn.close()

    def marcar_agendamento_enviado(self, id_agendamento: int):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                UPDATE agendamentos
                SET status = %s,
                    data_envio_real = CURRENT_TIMESTAMP
                WHERE id = %s
            """, ("enviado", id_agendamento))

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def marcar_agendamento_erro(self, id_agendamento: int, erro: str):
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            self.executar(cursor, """
                UPDATE agendamentos
                SET status = %s
                WHERE id = %s
            """, ("erro", id_agendamento))

            conn.commit()

            print("Erro no agendamento {}: {}".format(id_agendamento, erro))

        finally:
            cursor.close()
            conn.close()

    # ========================================================================
    # PREFERÊNCIAS (GOSTOS)
    # ========================================================================
    def salvar_preferencias(self, usuario_id: int, preferencias: dict):
        conn = self.conectar()
        cursor = conn.cursor()

        self.executar(cursor, 'SELECT COUNT(*) FROM preferencias_usuario WHERE usuario_id = ?', (usuario_id,))
        if cursor.fetchone()[0] == 0:
            self.executar(cursor, '''
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
            self.executar(cursor, '''
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
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, '''
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
        ''', '')
        conn.commit()
        conn.close()

    def obter_preferencias(self, usuario_id: int) -> dict:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, '''
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
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, '''
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
        conn = self.conectar()
        cursor = conn.cursor()

        # Criar tabela se não existir
        self.executar(cursor, '''
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

        self.executar(cursor, '''
            INSERT INTO documentos (usuario_id, tipo, titulo, descricao, caminho_arquivo, nome_original, tamanho)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, tipo, titulo, descricao, caminho_arquivo, nome_original, tamanho))

        conn.commit()
        conn.close()

    def listar_documentos_usuario(self, usuario_id: int) -> List[Dict]:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, '''
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
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, "DELETE FROM documentos WHERE id = ? AND usuario_id = ?", (id_documento, usuario_id))
        conn.commit()
        conn.close()

    # ========================================================================
    # CONFIGURAÇÕES
    # ========================================================================
    def salvar_config(self, chave: str, valor: str):
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, 'INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)', (chave, valor))
        conn.commit()
        conn.close()

    def executar(self, cursor, sql, params=()):
        if self.usa_postgres:
            sql = sql.replace("?", "%s")
        cursor.execute(sql, params)

    def obter_config(self, chave: str) -> Optional[str]:
        conn = self.conectar()
        cursor = conn.cursor()
        self.executar(cursor, 'SELECT valor FROM configuracoes WHERE chave = ?', (chave,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
