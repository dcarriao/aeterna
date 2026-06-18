import os
import psycopg2
import streamlit as st


def _database_url():
    return os.getenv("DATABASE_URL") or st.secrets.get("DATABASE_URL")


def main():
    conn = psycopg2.connect(_database_url())
    cursor = conn.cursor()
    try:
        for coluna, tipo in (
            ("arquivo_nome", "TEXT"),
            ("arquivo_tipo", "TEXT"),
            ("arquivo_tamanho", "BIGINT"),
            ("storage_bucket", "TEXT"),
            ("storage_path", "TEXT"),
        ):
            cursor.execute(
                f"ALTER TABLE contribuicoes ADD COLUMN IF NOT EXISTS {coluna} {tipo}"
            )

        cursor.execute("""
            ALTER TABLE contribuicoes
            DROP CONSTRAINT IF EXISTS ck_contribuicoes_tipo_contribuicao
        """)
        cursor.execute("""
            ALTER TABLE contribuicoes
            ADD CONSTRAINT ck_contribuicoes_tipo_contribuicao
            CHECK (
                tipo_contribuicao IN (
                    'texto', 'foto', 'video', 'texto_foto', 'texto_video'
                )
            )
        """)
        cursor.execute("""
            ALTER TABLE contribuicoes
            DROP CONSTRAINT IF EXISTS ck_contribuicoes_texto_preenchido
        """)
        cursor.execute("""
            ALTER TABLE contribuicoes
            DROP CONSTRAINT IF EXISTS ck_contribuicoes_conteudo_preenchido
        """)
        cursor.execute("""
            ALTER TABLE contribuicoes
            ADD CONSTRAINT ck_contribuicoes_conteudo_preenchido
            CHECK (
                NULLIF(BTRIM(COALESCE(texto, '')), '') IS NOT NULL
                OR NULLIF(BTRIM(COALESCE(arquivo_url, '')), '') IS NOT NULL
            )
        """)
        conn.commit()
        print("Contribuições com mídia migradas no Supabase Postgres.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
