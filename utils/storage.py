import os
import mimetypes
import secrets
from datetime import datetime

import streamlit as st
from supabase import create_client
from storage3.types import FileOptions


def _get_secret(nome: str):
    return os.getenv(nome) or st.secrets.get(nome)


class StorageAeterna:
    def __init__(self):
        self.url = _get_secret("SUPABASE_URL")
        self.key = _get_secret("SUPABASE_SERVICE_KEY")
        self.client = create_client(self.url, self.key)

    def upload_streamlit_file(self, bucket: str, arquivo, usuario_id: int, pasta: str):
        extensao = arquivo.name.split(".")[-1].lower()

        nome_arquivo = "{}_{}.{}".format(
            datetime.now().strftime("%Y%m%d_%H%M%S"),
            secrets.token_hex(8),
            extensao
        )

        path = f"usuario_{usuario_id}/{pasta}/{nome_arquivo}"

        mime_type = (
            mimetypes.guess_type(arquivo.name)[0]
            or "application/octet-stream"
        )

        self.client.storage.from_(bucket).upload(
            path,
            arquivo.getvalue()
        )

        public_url = self.client.storage.from_(bucket).get_public_url(path)

        return {
            "path": path,
            "url": public_url
        }

