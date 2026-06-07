#!/usr/bin/env python
# importar_dados.py - Script para importar dados do seu irmão
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def criar_conta_para_irmao():
    from utils.usuarios import GerenciadorUsuarios

    g = GerenciadorUsuarios()

    nome = input("Nome completo do seu irmão: ")
    email = input("E-mail para teste: ")
    senha = input("Senha para teste: ")
    cpf = input("CPF (11 números, use 00000000001 para teste): ")

    resultado = g.criar_usuario(nome, email, cpf, senha, 'usuario', '', '{}')

    if resultado:
        print(f"\n✅ Conta criada com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")

        # Buscar ID do usuário
        conn = sqlite3.connect("dados/cofre.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        usuario_id = cursor.fetchone()[0]
        conn.close()

        return usuario_id, email
    else:
        print("❌ Erro ao criar conta. E-mail ou CPF já existem?")
        return None, None


def importar_personalidade(usuario_id):
    from utils.assistente_ia import AssistenteLuto
    from utils.personalidade import PERGUNTAS_PERSONALIDADE

    print("\n" + "=" * 50)
    print("Vamos importar a personalidade do seu irmão")
    print("Responda como se fosse ELE respondendo")
    print("=" * 50 + "\n")

    respostas = {}

    for key, pergunta in PERGUNTAS_PERSONALIDADE.items():
        print(f"\n{pergunta}")
        resposta = input("> ")
        if resposta:
            respostas[key] = resposta

    if any(respostas.values()):
        assistente = AssistenteLuto(usuario_id)
        assistente.capturar_personalidade(respostas)
        print("\n✅ Personalidade importada com sucesso!")
        return True
    else:
        print("\n❌ Nenhuma resposta fornecida")
        return False


def importar_textos(usuario_id):
    from utils.assistente_ia import AssistenteLuto

    print("\n" + "=" * 50)
    print("Importar textos/mensagens do seu irmão")
    print("Cole cada mensagem em uma linha. Deixe em branco para terminar.")
    print("=" * 50 + "\n")

    textos = []
    print("Digite as mensagens (Enter em branco para terminar):")
    while True:
        linha = input("> ")
        if not linha:
            break
        if linha.strip():
            textos.append(linha.strip())

    if textos:
        assistente = AssistenteLuto(usuario_id)
        for texto in textos:
            assistente.adicionar_memoria(texto, "mensagem")
        print(f"\n✅ {len(textos)} textos importados com sucesso!")
    else:
        print("\n❌ Nenhum texto fornecido")


def main():
    import sqlite3

    print("=" * 50)
    print("🙏 IMPORTAR DADOS DO IRMÃO PARA O ASSISTENTE")
    print("=" * 50)
    print("\nEste script vai ajudar você a testar o Assistente de Luto")
    print("com os dados do seu irmão.\n")

    usuario_id, email = criar_conta_para_irmao()

    if usuario_id:
        importar_personalidade(usuario_id)
        importar_textos(usuario_id)

        print("\n" + "=" * 50)
        print("✅ IMPORTACAO CONCLUÍDA!")
        print("=" * 50)
        print(f"\nAgora acesse o app e faça login com:")
        print(f"   Email: {email}")
        print(f"\nVá na aba '🤖 Assistente de Luto' para conversar.")
    else:
        print("\n❌ Não foi possível criar a conta. Tente novamente.")


if __name__ == "__main__":
    main()