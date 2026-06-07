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
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

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

        conn.commit()
        conn.close()

    def _hash_senha(self, senha: str, salt: str = None) -> tuple:
        if salt is None:
            salt = secrets.token_hex(16)
        senha_com_salt = (senha + salt).encode()
        hash_obj = hashlib.sha256(senha_com_salt)
        return hash_obj.hexdigest(), salt

    def criar_usuario(self, nome: str, email: str, cpf: str, senha: str, tipo: str = 'usuario',
                      telefone: str = '', whatsapp: str = '', foto: str = '', redes: str = '') -> bool:
        try:
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
            if "cpf" in str(e):
                return "cpf_existente"
            return False

    def autenticar(self, email: str, senha: str) -> dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, nome, email, cpf, senha_hash, salt, tipo, foto, redes_sociais FROM usuarios WHERE email = ? AND ativo = 1',
            (email.lower(),))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            hash_calculado, _ = self._hash_senha(senha, usuario[5])
            if hash_calculado == usuario[4]:
                return {"id": usuario[0], "nome": usuario[1], "email": usuario[2], "cpf": usuario[3],
                        "tipo": usuario[6], "foto": usuario[7] or "", "redes_sociais": usuario[8] or "{}"}
        return None

    def obter_usuario_por_id(self, usuario_id: int) -> dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, email, cpf, telefone, whatsapp, tipo FROM usuarios WHERE id = ?',
                       (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            return {"id": usuario[0], "nome": usuario[1], "email": usuario[2], "cpf": usuario[3],
                    "telefone": usuario[4], "whatsapp": usuario[5], "tipo": usuario[6]}
        return None

    def criar_usuario_admin_inicial(self):
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        conn.close()
        if count == 0:
            self.criar_usuario("Admin", "admin@aeterna.com", "00000000000", "admin123", "admin")
            print("✅ Usuário admin criado: admin@aeterna.com / admin123")