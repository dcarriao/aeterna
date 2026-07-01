import sys
sys.path.append('D:\\aeterna')
from utils.banco import BancoDados

def migrar():
    print("Iniciando migração de memoriais...")
    db = BancoDados()
    conn = db.conectar()
    cursor = conn.cursor()
    
    try:
        # 1. Criar tabela memoriais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memoriais (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                nome VARCHAR(255) NOT NULL,
                foto_perfil TEXT,
                data_nascimento DATE,
                data_falecimento DATE,
                parentesco VARCHAR(100),
                biografia TEXT,
                visibilidade VARCHAR(50) DEFAULT 'privado',
                conversa_curador TEXT,
                curador_etapa VARCHAR(50) DEFAULT 'form',
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabela memoriais criada ou já existente.")
        
        # 2. Adicionar memorial_id nas tabelas existentes se não houver
        colunas_adicionar = [
            ("memorias", "memorial_id"),
            ("fotos", "memorial_id"),
            ("videos", "memorial_id"),
            ("contatos", "memorial_id"),
            ("contribuicoes", "memorial_id")
        ]
        
        for tabela, coluna in colunas_adicionar:
            # Check if column exists
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='{tabela}' AND column_name='{coluna}'
            """)
            if not cursor.fetchone():
                cursor.execute(f"""
                    ALTER TABLE {tabela} 
                    ADD COLUMN {coluna} INTEGER REFERENCES memoriais(id) ON DELETE CASCADE
                """)
                print(f"Coluna {coluna} adicionada na tabela {tabela}.")
            else:
                print(f"Coluna {coluna} já existe na tabela {tabela}.")
                
        conn.commit()
        print("Migração de memoriais concluída com sucesso!")
    except Exception as e:
        conn.rollback()
        print("Erro durante migração:", e)
        raise e
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrar()
