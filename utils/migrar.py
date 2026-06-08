# utils/migrar.py
import sqlite3
import os


def executar_migracao():
    """Adiciona colunas faltantes no banco de dados existente"""

    db_path = "dados/cofre.db"

    if not os.path.exists(db_path):
        print("Banco não encontrado, será criado")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # TABELA USUARIOS
    cursor.execute("PRAGMA table_info(usuarios)")
    colunas = [col[1] for col in cursor.fetchall()]

    colunas_usuarios = ['sobrenome', 'telefone', 'whatsapp', 'foto', 'redes_sociais', 'plano_id', 'data_nascimento']
    for coluna in colunas_usuarios:
        if coluna not in colunas:
            try:
                if coluna == 'plano_id':
                    cursor.execute(f'ALTER TABLE usuarios ADD COLUMN {coluna} INTEGER DEFAULT 1')
                elif coluna == 'data_nascimento':
                    cursor.execute(f'ALTER TABLE usuarios ADD COLUMN {coluna} DATE')
                else:
                    cursor.execute(f'ALTER TABLE usuarios ADD COLUMN {coluna} TEXT DEFAULT ""')
                print(f"✅ Coluna '{coluna}' adicionada em usuarios")
            except:
                pass

    # TABELA VIDEOS
    cursor.execute("PRAGMA table_info(videos)")
    colunas = [col[1] for col in cursor.fetchall()]

    if 'usuario_id' not in colunas:
        try:
            cursor.execute('ALTER TABLE videos ADD COLUMN usuario_id INTEGER DEFAULT 1')
            print("✅ Coluna 'usuario_id' adicionada em videos")
        except:
            pass

    if 'categoria' not in colunas:
        try:
            cursor.execute('ALTER TABLE videos ADD COLUMN categoria TEXT DEFAULT "geral"')
            print("✅ Coluna 'categoria' adicionada em videos")
        except:
            pass

    # TABELA CONTATOS
    cursor.execute("PRAGMA table_info(contatos)")
    colunas = [col[1] for col in cursor.fetchall()]

    colunas_contatos = ['usuario_id', 'sobrenome', 'parentesco', 'data_nascimento', 'datas_especiais',
                        'is_prioridade', 'prioridade_order', 'acesso_central_luto', 'chave_acesso']

    for coluna in colunas_contatos:
        if coluna not in colunas:
            try:
                if coluna in ['is_prioridade', 'prioridade_order', 'acesso_central_luto']:
                    cursor.execute(f'ALTER TABLE contatos ADD COLUMN {coluna} INTEGER DEFAULT 0')
                elif coluna == 'usuario_id':
                    cursor.execute(f'ALTER TABLE contatos ADD COLUMN {coluna} INTEGER DEFAULT 1')
                else:
                    cursor.execute(f'ALTER TABLE contatos ADD COLUMN {coluna} TEXT DEFAULT ""')
                print(f"✅ Coluna '{coluna}' adicionada em contatos")
            except:
                pass

    # TABELA SENHAS
    cursor.execute("PRAGMA table_info(senhas)")
    colunas = [col[1] for col in cursor.fetchall()]

    if 'usuario_id' not in colunas:
        try:
            cursor.execute('ALTER TABLE senhas ADD COLUMN usuario_id INTEGER DEFAULT 1')
            print("✅ Coluna 'usuario_id' adicionada em senhas")
        except:
            pass

    conn.commit()
    conn.close()
    print("🎉 Migração concluída!")