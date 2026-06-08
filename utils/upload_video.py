# utils/upload_video.py
import os
import json
from datetime import datetime


class GerenciadorVideos:
    def __init__(self, pasta_base="videos"):
        self.pasta_base = pasta_base
        os.makedirs(pasta_base, exist_ok=True)
        self._criar_metadata()

    def _criar_metadata(self):
        metadata_path = os.path.join(self.pasta_base, "metadata.json")
        if not os.path.exists(metadata_path):
            with open(metadata_path, "w") as f:
                json.dump({}, f)

    def _carregar_metadata(self):
        metadata_path = os.path.join(self.pasta_base, "metadata.json")
        with open(metadata_path, "r") as f:
            return json.load(f)

    def _salvar_metadata(self, metadata):
        metadata_path = os.path.join(self.pasta_base, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

    def salvar_video(self, arquivo, usuario_id, titulo, destinatario="", categoria="geral"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"usuario_{usuario_id}_{timestamp}.mp4"
        caminho = os.path.join(self.pasta_base, nome_arquivo)

        with open(caminho, "wb") as f:
            f.write(arquivo.getbuffer())

        metadata = self._carregar_metadata()
        metadata[nome_arquivo] = {
            "usuario_id": usuario_id,
            "titulo": titulo,
            "destinatario": destinatario,
            "categoria": categoria,
            "data_criacao": datetime.now().isoformat(),
            "tamanho": os.path.getsize(caminho)
        }
        self._salvar_metadata(metadata)
        return caminho

    def listar_videos_usuario(self, usuario_id):
        videos = []
        metadata = self._carregar_metadata()

        for arquivo, dados in metadata.items():
            if dados.get("usuario_id") == usuario_id:
                caminho = os.path.join(self.pasta_base, arquivo)
                if os.path.exists(caminho):
                    videos.append({
                        "id": arquivo,
                        "nome": arquivo,
                        "titulo": dados.get("titulo", ""),
                        "destinatario": dados.get("destinatario", ""),
                        "categoria": dados.get("categoria", "geral"),
                        "caminho": caminho,
                        "data": dados.get("data_criacao", ""),
                        "tamanho": dados.get("tamanho", 0)
                    })
        return sorted(videos, key=lambda x: x["data"], reverse=True)

    def deletar_video(self, video_id, usuario_id):
        metadata = self._carregar_metadata()

        if video_id in metadata and metadata[video_id]["usuario_id"] == usuario_id:
            caminho = os.path.join(self.pasta_base, video_id)
            if os.path.exists(caminho):
                os.remove(caminho)
            del metadata[video_id]
            self._salvar_metadata(metadata)
            return True
        return False

    def get_video_path(self, video_id, usuario_id):
        metadata = self._carregar_metadata()
        if video_id in metadata and metadata[video_id]["usuario_id"] == usuario_id:
            caminho = os.path.join(self.pasta_base, video_id)
            if os.path.exists(caminho):
                return caminho
        return None