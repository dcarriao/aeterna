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
            CREATE TABLE IF NOT EXISTS contribuicoes (
                id BIGSERIAL PRIMARY KEY,
                usuario_dono_id BIGINT NOT NULL
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE,
                usuario_contribuidor_email TEXT NOT NULL,
                usuario_contribuidor_nome TEXT NOT NULL,
                tipo_conteudo TEXT NOT NULL,
                conteudo_id BIGINT NOT NULL,
                tipo_contribuicao TEXT NOT NULL,
                texto TEXT,
                arquivo_url TEXT,
                status TEXT NOT NULL DEFAULT 'pendente',
                criado_em TIMESTAMP WITHOUT TIME ZONE
                    NOT NULL DEFAULT NOW(),
                avaliado_em TIMESTAMP WITHOUT TIME ZONE,
                avaliado_por BIGINT REFERENCES usuarios(id),
                CONSTRAINT ck_contribuicoes_tipo_conteudo
                    CHECK (tipo_conteudo IN ('memoria', 'foto', 'video')),
                CONSTRAINT ck_contribuicoes_tipo_contribuicao
                    CHECK (tipo_contribuicao IN ('texto', 'foto', 'video')),
                CONSTRAINT ck_contribuicoes_status
                    CHECK (status IN ('pendente', 'aprovado', 'rejeitado')),
                CONSTRAINT ck_contribuicoes_texto_preenchido
                    CHECK (
                        tipo_contribuicao <> 'texto'
                        OR NULLIF(BTRIM(texto), '') IS NOT NULL
                    )
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_contribuicoes_dono_status
            ON contribuicoes(usuario_dono_id, status, criado_em DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_contribuicoes_conteudo
            ON contribuicoes(
                usuario_dono_id,
                tipo_conteudo,
                conteudo_id,
                status
            )
        """)

        conn.commit()
        print("Tabela contribuicoes criada/verificada no Supabase Postgres.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
