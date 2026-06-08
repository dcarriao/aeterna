# utils/usuarios.py
import sqlite3
import hashlib
import secrets
from datetime import datetime


class GerenciadorUsuarios:
    def __init__(self, arquivo_db="dados/cofre.db"):
        self.arquivo_db = arquivo_db
        self._criar_tabelas()

    def _criar_tabelas(self):
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
                data_nascimento DATE,
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

        # Tabela de preferências do usuário
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

        # Tabela de personalidade (assistente)
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

        # Tabela de planos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL DEFAULT 0,
                descricao TEXT,
                max_contatos INTEGER DEFAULT 5,
                max_prioridades INTEGER DEFAULT 3,
                max_mensagens_ia INTEGER DEFAULT 50,
                max_videos_total INTEGER DEFAULT 10,
                max_videos_por_categoria INTEGER DEFAULT 5,
                tem_agendamento INTEGER DEFAULT 0,
                tem_videos_ia INTEGER DEFAULT 0,
                ativo INTEGER DEFAULT 1
            )
        ''')

        # Inserir plano padrão se não existir
        cursor.execute("SELECT COUNT(*) FROM planos")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO planos (nome, preco, descricao, max_contatos, max_prioridades, max_mensagens_ia, max_videos_total, max_videos_por_categoria, tem_agendamento, tem_videos_ia)
                VALUES ('Gratuito', 0, 'Plano básico gratuito', 5, 3, 50, 10, 5, 1, 0)
            ''')

        conn.commit()
        conn.close()

    def _hash_senha(self, senha: str, salt: str = None) -> tuple:
        if salt is None:
            salt = secrets.token_hex(16)
        senha_com_salt = (senha + salt).encode()
        hash_obj = hashlib.sha256(senha_com_salt)
        return hash_obj.hexdigest(), salt

    def criar_usuario(self, nome: str, sobrenome: str, email: str, cpf: str, data_nascimento: str,
                      senha: str, telefone: str = '', whatsapp: str = '',
                      foto: str = '', redes: str = '') -> bool:
        try:
            if not cpf or len(cpf) != 11 or not cpf.isdigit():
                return "cpf_invalido"
            if not email or '@' not in email:
                return "email_invalido"
            if not senha or len(senha) < 6:
                return "senha_curta"

            hash_senha, salt = self._hash_senha(senha)

            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, sobrenome, email, cpf, data_nascimento, telefone, whatsapp, senha_hash, salt, foto, redes_sociais)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            nome, sobrenome, email.lower(), cpf, data_nascimento, telefone, whatsapp, hash_senha, salt, foto, redes))
            conn.commit()
            usuario_id = cursor.lastrowid

            # Criar preferências vazias
            cursor.execute('INSERT INTO preferencias_usuario (usuario_id) VALUES (?)', (usuario_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            if "cpf" in str(e).lower():
                return "cpf_existente"
            elif "email" in str(e).lower():
                return "email_existente"
            return False

    def criar_usuario_admin(self, nome: str, sobrenome: str, email: str, cpf: str, data_nascimento: str, senha: str):
        """Cria um usuário administrador"""
        try:
            hash_senha, salt = self._hash_senha(senha)

            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, sobrenome, email, cpf, data_nascimento, senha_hash, salt, tipo)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'admin')
            ''', (nome, sobrenome, email.lower(), cpf, data_nascimento, hash_senha, salt))
            conn.commit()
            usuario_id = cursor.lastrowid
            cursor.execute('INSERT INTO preferencias_usuario (usuario_id) VALUES (?)', (usuario_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def autenticar(self, email: str, senha: str) -> dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, sobrenome, email, cpf, data_nascimento, senha_hash, salt, tipo, telefone, whatsapp, plano_id 
            FROM usuarios WHERE email = ? AND ativo = 1
        ''', (email.lower(),))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            hash_calculado, _ = self._hash_senha(senha, usuario[7])
            if hash_calculado == usuario[6]:
                return {
                    "id": usuario[0],
                    "nome": usuario[1],
                    "sobrenome": usuario[2],
                    "nome_completo": f"{usuario[1]} {usuario[2]}",
                    "email": usuario[3],
                    "cpf": usuario[4],
                    "data_nascimento": usuario[5],
                    "tipo": usuario[8],
                    "telefone": usuario[9] or "",
                    "whatsapp": usuario[10] or "",
                    "plano_id": usuario[11]
                }
        return None

    def obter_usuario_por_id(self, usuario_id: int) -> dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, sobrenome, email, cpf, data_nascimento, telefone, whatsapp, tipo, plano_id 
            FROM usuarios WHERE id = ?
        ''', (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            return {
                "id": usuario[0],
                "nome": usuario[1],
                "sobrenome": usuario[2],
                "nome_completo": f"{usuario[1]} {usuario[2]}",
                "email": usuario[3],
                "cpf": usuario[4],
                "data_nascimento": usuario[5],
                "telefone": usuario[6] or "",
                "whatsapp": usuario[7] or "",
                "tipo": usuario[8],
                "plano_id": usuario[9]
            }
        return None

    def salvar_preferencias(self, usuario_id: int, preferencias: dict):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE preferencias_usuario SET 
                gostos_musica = ?,
                gostos_comida = ?,
                melhor_lembranca = ?,
                dia_mais_feliz = ?,
                dia_mais_triste = ?,
                personalidade_extra = ?
            WHERE usuario_id = ?
        ''', (
            preferencias.get('gostos_musica', ''),
            preferencias.get('gostos_comida', ''),
            preferencias.get('melhor_lembranca', ''),
            preferencias.get('dia_mais_feliz', ''),
            preferencias.get('dia_mais_triste', ''),
            preferencias.get('personalidade_extra', ''),
            usuario_id
        ))
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
        return None

    def atualizar_ultimo_acesso(self, usuario_id: int):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?', (usuario_id,))
        conn.commit()
        conn.close()

    def listar_usuarios(self) -> list:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, sobrenome, email, cpf, tipo, telefone, whatsapp, data_criacao, ultimo_acesso 
            FROM usuarios ORDER BY data_criacao DESC
        ''')
        usuarios = cursor.fetchall()
        conn.close()
        return [
            {
                "id": u[0],
                "nome": f"{u[1]} {u[2]}",
                "email": u[3],
                "cpf": u[4],
                "tipo": u[5],
                "telefone": u[6] or "",
                "whatsapp": u[7] or "",
                "data_criacao": u[8],
                "ultimo_acesso": u[9]
            }
            for u in usuarios
        ]

    def criar_usuario_admin_inicial(self):
        """Cria usuário admin inicial se não existir"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        conn.close()

        if count == 0:
            senha = self._gerar_senha_admin()
            self.criar_usuario_admin(
                nome="Administrador",
                sobrenome="aEterna",
                email="admin@aeterna.com",
                cpf="00000000000",
                data_nascimento="1970-01-01",
                senha=senha
            )
            print("✅ Usuário admin criado. Verifique o log para a senha.")

    def _gerar_senha_admin(self) -> str:
        """Retorna senha fixa para o admin"""
        return "admin123"