from cryptography.fernet import Fernet
import base64
import hashlib


class GerenciadorCriptografia:
    def __init__(self, senha_mestre: str):
        """Inicializa com uma senha mestre"""
        self.senha_mestre = senha_mestre
        self.chave = self._criar_chave_simples(senha_mestre)
        self.cipher = Fernet(self.chave)

    def _criar_chave_simples(self, senha: str) -> bytes:
        """Cria uma chave Fernet a partir de uma senha (simplificado para MVP)"""
        # Gera um hash da senha e converte para chave Fernet
        hash_senha = hashlib.sha256(senha.encode()).digest()
        # Fernet precisa de uma chave de 32 bytes em base64 URL-safe
        chave = base64.urlsafe_b64encode(hash_senha[:32])
        return chave

    def criptografar(self, texto: str) -> str:
        """Criptografa um texto"""
        if not texto:
            return ""
        texto_bytes = texto.encode('utf-8')
        criptografado = self.cipher.encrypt(texto_bytes)
        return base64.b64encode(criptografado).decode('utf-8')

    def descriptografar(self, texto_criptografado: str) -> str:
        """Descriptografa um texto"""
        if not texto_criptografado:
            return ""
        try:
            dados_bytes = base64.b64decode(texto_criptografado.encode('utf-8'))
            descriptografado = self.cipher.decrypt(dados_bytes)
            return descriptografado.decode('utf-8')
        except Exception as e:
            return "[Erro ao descriptografar]"


# Teste rápido (remova depois)
if __name__ == "__main__":
    crypto = GerenciadorCriptografia("minha_senha_123")

    # Testar criptografia
    original = "minha_senha_secreta"
    cripto = crypto.criptografar(original)
    print(f"Original: {original}")
    print(f"Criptografado: {cripto}")

    decripto = crypto.descriptografar(cripto)
    print(f"Descriptografado: {decripto}")

    assert original == decripto
    print("✅ Teste passou!")