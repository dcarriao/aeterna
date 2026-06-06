# utils/usuarios.py
import sqlite3
import hashlib
import secrets
from datetime import datetime


class GerenciadorUsuarios:
    def __init__(self, arquivo_db="dados/cofre.db"):
        self.arquivo_db = arquivo_db
        self._criar_tabela_usuario()

    def _criar_tabela_usuario(self):
        """Cria tabela de usuários com CPF, foto e redes sociais"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
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

        conn.commit()
        conn.close()

    def _hash_senha(self, senha: str, salt: str = None) -> tuple:
        """Gera hash da senha com salt"""
        if salt is None:
            salt = secrets.token_hex(16)

        senha_com_salt = (senha + salt).encode()
        hash_obj = hashlib.sha256(senha_com_salt)
        hash_senha = hash_obj.hexdigest()

        return hash_senha, salt

    def criar_usuario(self, nome: str, email: str, cpf: str, senha: str, tipo: str = 'usuario', foto: str = '',
                      redes: str = '') -> bool:
        """Cria um novo usuário com CPF"""
        try:
            hash_senha, salt = self._hash_senha(senha)

            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO usuarios (nome, email, cpf, senha_hash, salt, tipo, foto, redes_sociais)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email.lower(), cpf, hash_senha, salt, tipo, foto, redes))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            if "cpf" in str(e).lower():
                return "cpf_existente"
            return False

    def autenticar(self, email: str, senha: str) -> dict:
        """Autentica um usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, nome, email, cpf, senha_hash, salt, tipo, foto, redes_sociais
            FROM usuarios WHERE email = ? AND ativo = 1
        ''', (email.lower(),))

        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            hash_calculado, _ = self._hash_senha(senha, usuario[5])
            if hash_calculado == usuario[4]:
                self._atualizar_acesso(usuario[0])
                return {
                    "id": usuario[0],
                    "nome": usuario[1],
                    "email": usuario[2],
                    "cpf": usuario[3],
                    "tipo": usuario[6],
                    "foto": usuario[7] or "",
                    "redes_sociais": usuario[8] or "{}"
                }
        return None

    def _atualizar_acesso(self, usuario_id: int):
        """Atualiza data do último acesso"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (usuario_id,))
        conn.commit()
        conn.close()

    def listar_usuarios(self) -> list:
        """Lista todos os usuários"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nome, email, cpf, tipo, data_criacao, ultimo_acesso 
            FROM usuarios ORDER BY data_criacao DESC
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
                "data_criacao": u[5],
                "ultimo_acesso": u[6]
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
            self.criar_usuario("Admin", "admin@aeterna.com", "00000000000", "admin123", "admin")
            print("✅ Usuário admin criado: admin@aeterna.com / admin123 / CPF: 00000000000")