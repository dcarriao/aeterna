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
        """Cria todas as tabelas necessárias"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT,
                whatsapp TEXT,
                senha_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                foto TEXT,
                redes_sociais TEXT,
                tipo TEXT DEFAULT 'usuario',
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP
            )
        ''')

        # Tabela de personalidade (para o assistente de luto)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalidade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                pergunta TEXT,
                resposta TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def _hash_senha(self, senha: str, salt: str = None) -> tuple:
        """Gera hash da senha com salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        senha_com_salt = (senha + salt).encode()
        hash_obj = hashlib.sha256(senha_com_salt)
        return hash_obj.hexdigest(), salt

    def criar_usuario(self, nome: str, email: str, cpf: str, senha: str, tipo: str = 'usuario',
                      telefone: str = '', whatsapp: str = '', foto: str = '', redes: str = ''):
        """Cria um novo usuário"""
        try:
            # Validar CPF
            if not cpf or len(cpf) != 11 or not cpf.isdigit():
                return "cpf_invalido"

            # Validar email
            if not email or '@' not in email:
                return "email_invalido"

            # Validar senha
            if not senha or len(senha) < 6:
                return "senha_curta"

            hash_senha, salt = self._hash_senha(senha)

            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, email, cpf, telefone, whatsapp, senha_hash, salt, tipo, foto, redes_sociais)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email.lower(), cpf, telefone, whatsapp, hash_senha, salt, tipo, foto, redes))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            if "cpf" in str(e).lower():
                return "cpf_existente"
            elif "email" in str(e).lower():
                return "email_existente"
            return False

    def autenticar(self, email: str, senha: str) -> dict:
        """Autentica um usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, nome, email, cpf, senha_hash, salt, tipo, telefone, whatsapp FROM usuarios WHERE email = ? AND ativo = 1',
            (email.lower(),))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            hash_calculado, _ = self._hash_senha(senha, usuario[5])
            if hash_calculado == usuario[4]:
                return {
                    "id": usuario[0],
                    "nome": usuario[1],
                    "email": usuario[2],
                    "cpf": usuario[3],
                    "tipo": usuario[6],
                    "telefone": usuario[7] or "",
                    "whatsapp": usuario[8] or ""
                }
        return None

    def obter_usuario_por_id(self, usuario_id: int) -> dict:
        """Obtém usuário pelo ID"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, email, cpf, telefone, whatsapp, tipo FROM usuarios WHERE id = ?',
                       (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            return {
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "cpf": usuario[3],
                "telefone": usuario[4] or "",
                "whatsapp": usuario[5] or "",
                "tipo": usuario[6]
            }
        return None

    def listar_usuarios(self) -> list:
        """Lista todos os usuários"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, email, cpf, tipo, telefone, whatsapp, data_criacao, ultimo_acesso 
            FROM usuarios 
            ORDER BY data_criacao DESC
        ''')
        usuarios = cursor.fetchall()
        conn.close()

        return [
            {
                "id": u[0],
                "nome": u[1],
                "email": u[2],
                "cpf": u[3],
                "tipo": u[4],
                "telefone": u[5] or "",
                "whatsapp": u[6] or "",
                "data_criacao": u[7],
                "ultimo_acesso": u[8]
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
            self.criar_usuario(
                nome="Administrador",
                email="admin@aeterna.com",
                cpf="00000000000",
                senha=self._gerar_senha_admin(),
                tipo="admin"
            )
            print("✅ Usuário admin criado. A senha será exibida apenas uma vez.")

    def _gerar_senha_admin(self) -> str:
        """Gera uma senha aleatória para o admin inicial"""
        import random
        import string
        senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        print(f"⚠️ SENHA ADMIN: {senha}")
        print("Guarde esta senha! Ela não será exibida novamente.")
        return senha

    def atualizar_ultimo_acesso(self, usuario_id: int):
        """Atualiza a data do último acesso do usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?', (usuario_id,))
        conn.commit()
        conn.close()