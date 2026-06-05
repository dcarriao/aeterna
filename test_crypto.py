# test_crypto.py
from utils.criptografia import GerenciadorCriptografia


def testar_criptografia():
    print("Testando criptografia...")

    # Criar instância
    crypto = GerenciadorCriptografia("senha_teste_123")

    # Dados para testar
    senhas_teste = [
        "MinhaSenha123",
        "outra_senha_com!@#$",
        "senha_muito_longa_com_muitos_caracteres" * 10,
        ""
    ]

    for senha in senhas_teste:
        print(f"\nTestando: '{senha}'")

        # Criptografar
        criptografada = crypto.criptografar(senha)
        print(f"Criptografado: {criptografada[:50]}...")

        # Descriptografar
        descriptografada = crypto.descriptografar(criptografada)
        print(f"Descriptografado: '{descriptografada}'")

        # Verificar
        if senha == descriptografada:
            print("✅ OK")
        else:
            print(f"❌ ERRO! Original: '{senha}', Decripto: '{descriptografada}'")
            return False

    print("\n🎉 Todos os testes passaram!")
    return True


if __name__ == "__main__":
    testar_criptografia()