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
        for tabela in ("memorias", "fotos", "videos"):
            cursor.execute(f"""
                ALTER TABLE {tabela}
                ADD COLUMN IF NOT EXISTS visibilidade TEXT
                    NOT NULL DEFAULT 'contatos'
            """)
            cursor.execute(f"""
                UPDATE {tabela}
                SET visibilidade = 'contatos'
                WHERE visibilidade IS NULL
                   OR visibilidade NOT IN ('privado', 'contatos', 'seletivo')
            """)
            cursor.execute(f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'ck_{tabela}_visibilidade'
                    ) THEN
                        ALTER TABLE {tabela}
                        ADD CONSTRAINT ck_{tabela}_visibilidade
                        CHECK (visibilidade IN ('privado', 'contatos', 'seletivo'));
                    END IF;
                END
                $$;
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conteudo_permissoes (
                id BIGSERIAL PRIMARY KEY,
                tipo_conteudo TEXT NOT NULL,
                conteudo_id BIGINT NOT NULL,
                contato_id BIGINT NOT NULL
                    REFERENCES contatos(id)
                    ON DELETE CASCADE,
                criado_em TIMESTAMP WITHOUT TIME ZONE
                    NOT NULL DEFAULT NOW(),
                CONSTRAINT ck_conteudo_permissoes_tipo
                    CHECK (tipo_conteudo IN ('memoria', 'foto', 'video')),
                CONSTRAINT uq_conteudo_permissoes
                    UNIQUE (tipo_conteudo, conteudo_id, contato_id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conteudo_permissoes_consulta
            ON conteudo_permissoes(tipo_conteudo, conteudo_id, contato_id)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aeterna_migrations (
                chave TEXT PRIMARY KEY,
                executada_em TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
            )
        """)
        cursor.execute("""
            SELECT 1 FROM aeterna_migrations
            WHERE chave = 'fase4_importar_permissoes_legadas'
        """)
        migracao_legada_executada = cursor.fetchone() is not None

        if not migracao_legada_executada:
            cursor.execute("""
                INSERT INTO conteudo_permissoes (
                    tipo_conteudo, conteudo_id, contato_id
                )
                SELECT 'foto', fc.foto_id, fc.contato_id
                FROM fotos_contatos fc
                ON CONFLICT DO NOTHING
            """)
            cursor.execute("""
                UPDATE fotos f
                SET visibilidade = 'seletivo'
                WHERE EXISTS (
                    SELECT 1 FROM fotos_contatos fc WHERE fc.foto_id = f.id
                )
            """)

            cursor.execute("""
                INSERT INTO conteudo_permissoes (
                    tipo_conteudo, conteudo_id, contato_id
                )
                SELECT 'video', va.video_id, va.contato_id
                FROM videos_acesso va
                ON CONFLICT DO NOTHING
            """)
            cursor.execute("""
                UPDATE videos v
                SET visibilidade = 'seletivo'
                WHERE EXISTS (
                    SELECT 1 FROM videos_acesso va WHERE va.video_id = v.id
                )
            """)
            cursor.execute("""
                INSERT INTO aeterna_migrations(chave)
                VALUES ('fase4_importar_permissoes_legadas')
                ON CONFLICT DO NOTHING
            """)

        conn.commit()
        print("Visibilidade de conteúdos criada/migrada no Supabase Postgres.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
