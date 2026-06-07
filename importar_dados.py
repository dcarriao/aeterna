#!/usr/bin/env python
# importar_dados.py - Script para importar dados do seu irmão
import os
import sqlite3
import hashlib
import secrets
from datetime import datetime


def criar_tabelas_do_zero():
    """Recria as tabelas do zero com a estrutura correta"""

    # Fazer backup do banco antigo se existir
    if os.path.exists("dados/cofre.db"):
        backup = f"dados/cofre_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        os.rename("dados/cofre.db", backup)
        print(f"📁 Backup do banco antigo criado: {backup}")

    conn = sqlite3.connect("dados/cofre.db")
    cursor = conn.cursor()

    # Tabela de usuários (estrutura completa)
    cursor.execute('''
        CREATE TABLE usuarios (
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

    # Tabela de senhas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS senhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            titulo TEXT NOT NULL,
            destinatario TEXT,
            caminho_arquivo TEXT,
            url_externa TEXT,
            notas TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de contatos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            papel TEXT,
            mensagem_liberacao TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de personalidade
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personalidade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            pergunta TEXT,
            resposta TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    print("✅ Tabelas criadas com sucesso!")


def gerar_hash_senha(senha: str, salt: str = None) -> tuple:
    """Gera hash da senha com salt"""
    if salt is None:
        salt = secrets.token_hex(16)

    senha_com_salt = (senha + salt).encode()
    hash_obj = hashlib.sha256(senha_com_salt)
    hash_senha = hash_obj.hexdigest()

    return hash_senha, salt


def criar_conta(nome, email, cpf, senha):
    """Cria conta diretamente no banco de dados"""
    conn = sqlite3.connect("dados/cofre.db")
    cursor = conn.cursor()

    # Verificar se já existe
    cursor.execute("SELECT id FROM usuarios WHERE email = ? OR cpf = ?", (email, cpf))
    if cursor.fetchone():
        conn.close()
        return None, "E-mail ou CPF já cadastrado"

    senha_hash, salt = gerar_hash_senha(senha)

    try:
        cursor.execute('''
            INSERT INTO usuarios (nome, email, cpf, senha_hash, salt, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, cpf, senha_hash, salt, 'usuario'))

        conn.commit()
        usuario_id = cursor.lastrowid
        conn.close()
        return usuario_id, None
    except Exception as e:
        conn.close()
        return None, str(e)


def salvar_personalidade(usuario_id, perguntas_respostas):
    """Salva as respostas de personalidade"""
    conn = sqlite3.connect("dados/cofre.db")
    cursor = conn.cursor()

    for pergunta, resposta in perguntas_respostas.items():
        cursor.execute('''
            INSERT INTO personalidade (usuario_id, pergunta, resposta)
            VALUES (?, ?, ?)
        ''', (usuario_id, pergunta, resposta))

    conn.commit()
    conn.close()
    print(f"✅ {len(perguntas_respostas)} respostas de personalidade salvas")


def salvar_memorias(usuario_id, textos):
    """Salva memórias/textos do usuário"""
    memorias_file = f"dados/memorias_{usuario_id}.txt"
    with open(memorias_file, "w", encoding="utf-8") as f:
        f.write(f"# Memórias - Usuário {usuario_id}\n")
        f.write(f"# Data: {datetime.now()}\n\n")
        for i, texto in enumerate(textos, 1):
            f.write(f"{i}. {texto}\n")
        f.write(f"\n---\nTotal: {len(textos)} mensagens\n")

    print(f"✅ {len(textos)} textos salvos em {memorias_file}")


def main():
    print("=" * 50)
    print("🙏 IMPORTAR DADOS DO IRMÃO")
    print("=" * 50)

    # Criar pasta dados se não existir
    os.makedirs("dados", exist_ok=True)

    print("\n⏳ Preparando banco de dados...")
    criar_tabelas_do_zero()

    print("\n📝 DADOS DA CONTA")
    print("-" * 30)

    nome = input("Nome completo: ").strip()
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    cpf = input("CPF (11 números): ").strip()

    if not all([nome, email, senha, cpf]):
        print("❌ Todos os campos são obrigatórios!")
        return

    if len(cpf) != 11 or not cpf.isdigit():
        print("❌ CPF inválido! Use exatamente 11 números.")
        return

    print("\n⏳ Criando conta...")
    usuario_id, erro = criar_conta(nome, email, cpf, senha)

    if usuario_id:
        print(f"✅ Conta criada com sucesso! (ID: {usuario_id})")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
    else:
        print(f"❌ Erro: {erro}")
        return

    # Perguntas de personalidade
    print("\n" + "=" * 50)
    print("🧠 PERSONALIDADE")
    print("=" * 50)
    print("Responda como se fosse seu irmão falando:")
    print("(Digite 'pular' para pular uma pergunta)")
    print("-" * 30)

    perguntas = {
        "apresentacao": "1. Como você se descreveria em poucas palavras?",
        "valores": "2. Quais são os valores mais importantes para você?",
        "conselho_geral": "3. Qual o principal conselho que você daria?",
        "amor": "4. O que você quer que saibam sobre o seu amor?",
        "forca": "5. O que você diria para dar força?",
        "felicidade": "6. O que torna a vida feliz para você?",
        "lembranca_feliz": "7. Qual sua lembrança mais feliz?",
        "superacao": "8. Como você superou momentos difíceis?",
        "legado": "9. Qual legado você quer deixar?",
        "futuro": "10. O que você deseja para o futuro de quem ama?"
    }

    respostas = {}

    for key, pergunta in perguntas.items():
        print(f"\n{pergunta}")
        resposta = input("👉 ").strip()
        if resposta and resposta.lower() != 'pular':
            respostas[key] = resposta

    if respostas:
        salvar_personalidade(usuario_id, respostas)
    else:
        print("⚠️ Nenhuma resposta fornecida")

    # Textos/mensagens
    print("\n" + "=" * 50)
    print("📝 TEXTOS E MENSAGENS")
    print("=" * 50)
    print("Digite mensagens que seu irmão escreveu.")
    print("Digite uma por linha. Deixe em branco para terminar.")
    print("-" * 30)

    textos = []
    linha_num = 1
    while True:
        linha = input(f"{linha_num:2d} > ")
        if not linha.strip():
            break
        textos.append(linha.strip())
        linha_num += 1

    if textos:
        salvar_memorias(usuario_id, textos)
    else:
        print("⚠️ Nenhum texto fornecido")

    # Resumo final
    print("\n" + "=" * 50)
    print("✅ IMPORTAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print(f"\n📊 Resumo:")
    print(f"   Usuário ID: {usuario_id}")
    print(f"   Email: {email}")
    print(f"   Senha: {senha}")
    print(f"   Respostas: {len(respostas)}")
    print(f"   Mensagens: {len(textos)}")
    print(f"\n🌿 Agora:")
    print(f"   1. Execute: streamlit run app.py")
    print(f"   2. Faça login com: {email}")
    print(f"   3. Vá na aba '🤖 Assistente de Luto'")
    print("")


if __name__ == "__main__":
    main()