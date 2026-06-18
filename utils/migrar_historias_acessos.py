import os

import psycopg2
import streamlit as st


def obter_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    try:
        return st.secrets.get("DATABASE_URL", "")
    except Exception:
        return ""


def main():
    database_url = obter_database_url()
    if not database_url:
        raise RuntimeError("DATABASE_URL do Supabase não configurada.")

    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historias_acessos (
                id BIGSERIAL PRIMARY KEY,
                usuario_visualizador_email TEXT NOT NULL,
                dono_historia_id BIGINT NOT NULL
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE,
                ultimo_acesso_em TIMESTAMP WITHOUT TIME ZONE
                    NOT NULL DEFAULT NOW(),
                CONSTRAINT uq_historias_acessos_visualizador_dono
                    UNIQUE (usuario_visualizador_email, dono_historia_id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_historias_acessos_dono
            ON historias_acessos(dono_historia_id)
        """)

        conn.commit()
        print("Tabela historias_acessos criada/verificada no Supabase Postgres.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
