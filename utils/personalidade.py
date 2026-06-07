# utils/personalidade.py
import streamlit as st

# Perguntas para capturar a personalidade
PERGUNTAS_PERSONALIDADE = {
    "apresentacao": "Como você se descreveria em poucas palavras?",
    "valores": "Quais são os valores mais importantes que você quer transmitir?",
    "conselho_geral": "Qual é o principal conselho que você daria para seus entes queridos?",
    "amor": "O que você mais quer que seus entes queridos saibam sobre o amor que sente por eles?",
    "forca": "O que você diria para dar força a alguém que está passando por um momento difícil?",
    "felicidade": "O que, na sua opinião, torna a vida verdadeiramente feliz?",
    "lembranca_feliz": "Qual é sua lembrança mais feliz com seus entes queridos?",
    "superacao": "Como você superou momentos difíceis na vida? O que aprendeu?",
    "legado": "Qual legado você quer deixar para o mundo?",
    "futuro": "O que você deseja para o futuro de quem você ama?"
}


def renderizar_captura_personalidade():
    """Renderiza o formulário de captura de personalidade"""
    st.markdown("### 🧠 Sobre você")

    respostas = {}

    for key, pergunta in PERGUNTAS_PERSONALIDADE.items():
        resposta = st.text_area(
            pergunta,
            key=f"pers_{key}",
            height=80,
            placeholder="Escreva sua resposta aqui..."
        )
        if resposta:
            respostas[key] = resposta

    return respostas