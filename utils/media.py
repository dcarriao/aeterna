import os

import streamlit as st


def exibir_video_seguro(caminho_video: str, legenda: str = "") -> bool:
    caminho_video = caminho_video or ""

    try:
        if caminho_video.startswith(("http://", "https://")):
            st.video(caminho_video)
            if legenda:
                st.caption(legenda)
            return True

        if caminho_video and os.path.exists(caminho_video):
            st.video(caminho_video)
            if legenda:
                st.caption(legenda)
            return True

        st.warning(
            "🎥 Este vídeo foi registrado antes da migração para o Storage "
            "e não está disponível neste ambiente."
        )
    except Exception as exc:
        print("Erro ao exibir vídeo:", exc)
        st.warning("🎥 Não foi possível carregar este vídeo agora.")

    return False


def exibir_foto_segura(
    caminho_foto: str,
    caption: str = "",
    width="stretch",
) -> bool:
    caminho_foto = caminho_foto or ""

    try:
        if caminho_foto.startswith(("http://", "https://")):
            st.image(caminho_foto, caption=caption, width=width)
            return True

        if caminho_foto and os.path.exists(caminho_foto):
            st.image(caminho_foto, caption=caption, width=width)
            return True

        st.warning(
            "📷 Esta foto foi registrada antes da migração para o Storage "
            "e não está disponível neste ambiente."
        )
    except Exception as exc:
        print("Erro ao exibir foto:", exc)
        st.warning("📷 Não foi possível carregar esta foto agora.")

    return False
