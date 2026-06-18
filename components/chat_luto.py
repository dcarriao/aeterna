import html
import streamlit as st
import os
from datetime import datetime

from utils.assistente_ia import AssistenteLuto
from utils.banco import BancoDados
from utils.upload_video import GerenciadorVideos
from utils.storage import StorageAeterna
from utils.media import exibir_foto_segura

storage = StorageAeterna()


def _extrair_palavras_relevantes(texto: str):
    ignorar = {
        "como", "foi", "essa", "esse", "isso", "sobre", "para", "pela",
        "pelo", "dele", "dela", "nossa", "nosso", "minha", "meu",
        "quero", "saber", "falar", "conte", "mais", "uma", "uns", "das",
        "dos", "que", "com", "por"
    }

    palavras = []

    for palavra in texto.lower().replace("?", "").replace(",", "").split():
        if len(palavra) >= 4 and palavra not in ignorar:
            palavras.append(palavra)

    return palavras

def _safe_text(value: str) -> str:
    return html.escape(str(value or "")).replace("\n", "<br>")


def render_chat_luto():
    _inicializar_chat()
    db = BancoDados()

    nome_referencia = _obter_nome_referencia()
    usuario = st.session_state.get("usuario_atual") or {}
    modo = "memorial" if usuario.get("tipo") == "visitante" else "legado"

    st.markdown("""
    <style>
    .ae-assistente-page h2,
    .ae-assistente-page p {
        color: #2b1747 !important;
    }

    .ae-simple-bubble-bot {
        background: #ffffff;
        color: #1b0f2e;
        padding: 14px 16px;
        border-radius: 18px;
        margin: 12px 0;
        max-width: 92%;
        border: 1px solid rgba(0,0,0,0.08);
        font-size: 0.95rem;
        line-height: 1.45;
    }

    .ae-simple-bubble-user {
        background: #2b1747;
        color: #ffffff;
        padding: 14px 16px;
        border-radius: 18px;
        margin: 12px 0 12px auto;
        max-width: 92%;
        font-size: 0.95rem;
        line-height: 1.45;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ae-assistente-page">', unsafe_allow_html=True)

    if modo == "memorial":
        nome_falecido = usuario.get("nome_falecido", "essa pessoa especial")

        st.markdown("## 💬 Converse com o Assistente de Histórias")
        st.info(
            f"Explore histórias, valores e momentos compartilhados por {nome_falecido}. "
            "O assistente usa apenas informações registradas, não inventa fatos "
            "e não fala como se fosse a pessoa."
        )

        st.markdown("""
                    ### 💬 Por onde começar?

                    • Quais histórias {nome_falecido} compartilhou comigo?
                    • Quais momentos importantes foram registrados?
                    • Quais fotos ou vídeos estão disponíveis?
                    • O que foi contado sobre família, viagens ou aprendizados?
                    • Existe alguma mensagem compartilhada comigo?
                    • Quais valores aparecem nessas histórias?
                    """.format(nome_falecido=nome_falecido))
        if not usuario.get("usuario_logado_compartilhado"):
            st.markdown("""
                        ---
                        ### ✨ Também quer preservar sua história?

                        Crie seu espaço na aEterna para registrar histórias, fotos, vídeos e momentos importantes da sua vida.
                        """)

            if st.button("✨ Criar minha história"):
                for key in [
                    "autenticado",
                    "usuario_atual",
                    "modo_acesso",
                    "falecido_id",
                    "historico_assistente",
                    "assistente_obj",
                    "assistente_modo",
                    "assistente_usuario_id",
                    "assistente_contato_id",
                ]:
                    if key in st.session_state:
                        del st.session_state[key]

                st.session_state.autenticado = False
                st.session_state.login_mode = "cadastro"
                st.rerun()
    else:
        st.markdown("## Assistente de Legado")
        st.markdown("""
            Este espaço existe para ajudar a construir e preservar o seu legado digital.
        
            Você pode conversar livremente sobre qualquer assunto que desejar.
        
            Também posso sugerir temas importantes para registrar histórias, valores, aprendizados, conselhos e lembranças que poderão ajudar sua família e pessoas queridas no futuro.
            """)
        st.markdown(
            """

            ### 💡 Sugestões de conversa
    
            • Minha infância
    
            • Minha família
    
            • Como conheci meu amor
    
            • Meus filhos
    
            • Minha carreira
    
            • Meus maiores aprendizados
    
            • Sonhos realizados
    
            • Momentos difíceis que superei
    
            • Conselhos para o futuro
    
            • Histórias engraçadas
            """
            )

    if st.session_state.get("ultimo_erro_openai"):
        st.error(f"Erro OpenAI: {st.session_state['ultimo_erro_openai']}")


    historico = st.session_state.get("historico_assistente", [])

    if not historico:
        historico = [{
            "tipo": "bot",
            "texto": (
                f"Olá. Este é um espaço para explorar histórias, valores, "
                f"aprendizados e momentos importantes de {nome_referencia}."
            )
        }]

    for i, msg in enumerate(historico):
        tipo = msg.get("tipo", "bot")
        texto_original = msg.get("texto", "")
        texto_html = html.escape(texto_original).replace("\n", "<br>")

        if tipo == "user":
            st.markdown(
                '<div class="ae-simple-bubble-user">{}</div>'.format(texto_html),
                unsafe_allow_html=True
            )

            if modo == "legado" and len(texto_original.strip()) > 20:
                chave_base = "memoria_{}_{}".format(i, abs(hash(texto_original)))

                if st.button(
                        "💾 Salvar como memória",
                        key="salvar_" + chave_base
                ):
                    sugestoes = st.session_state.assistente_obj.sugerir_metadados_memoria(
                        texto_original
                    )
                    st.session_state["sugestoes_" + chave_base] = sugestoes
                    st.session_state["texto_memoria_" + chave_base] = texto_original

                if "sugestoes_" + chave_base in st.session_state:
                    sugestoes = st.session_state["sugestoes_" + chave_base]

                    with st.form("form_" + chave_base):
                        st.markdown("#### 💡 Sugestões para organizar esta memória")

                        titulo = st.text_input(
                            "Título",
                            value=sugestoes.get("titulo", "")
                        )

                        categoria = st.text_input(
                            "Categoria",
                            value=sugestoes.get("categoria", "")
                        )

                        local = st.text_input(
                            "Local",
                            value=sugestoes.get("local", "")
                        )

                        data_evento = st.text_input(
                            "Data aproximada",
                            value=sugestoes.get("data_evento", ""),
                            placeholder="Ex: 2024-03-15, 2024, infância..."
                        )

                        pessoas_relacionadas = st.text_input(
                            "Pessoas relacionadas",
                            value=sugestoes.get("pessoas_relacionadas", "")
                        )

                        contatos = db.listar_contatos_usuario(
                            st.session_state.get("usuario_atual", {}).get("id")
                        )
                        visibilidade = st.radio(
                            "Quem pode ver esta memória?",
                            ["privado", "contatos", "seletivo"],
                            format_func=lambda valor: {
                                "privado": "🔒 Somente eu",
                                "contatos": "👥 Todos os meus contatos",
                                "seletivo": "✨ Escolher contatos específicos",
                            }[valor],
                            key="visibilidade_" + chave_base,
                        )
                        mapa_contatos = {
                            contato["nome_completo"]: contato["id"]
                            for contato in contatos
                        }
                        contatos_selecionados_nomes = (
                            st.multiselect(
                                "Contatos que poderão ver",
                                list(mapa_contatos.keys()),
                                key="contatos_" + chave_base,
                            )
                            if visibilidade == "seletivo"
                            else []
                        )
                        contatos_selecionados = [
                            mapa_contatos[nome]
                            for nome in contatos_selecionados_nomes
                        ]

                        foto_memoria = st.file_uploader(
                            "📷 Adicionar foto a esta memória (opcional)",
                            type=["png", "jpg", "jpeg", "webp"],
                            key="foto_" + chave_base
                        )

                        video_memoria = st.file_uploader(
                            "🎥 Adicionar vídeo a esta memória (opcional)",
                            type=["mp4", "mov", "avi", "mkv"],
                            key="video_" + chave_base
                        )

                        salvar_final = st.form_submit_button(
                            "✅ Salvar memória",
                            type="primary",
                            width="stretch"
                        )

                        if salvar_final:
                            usuario = st.session_state.get("usuario_atual")

                            if visibilidade == "seletivo" and not contatos_selecionados:
                                st.warning("Selecione pelo menos um contato.")
                                st.stop()

                            if data_evento:
                                try:
                                    datetime.strptime(data_evento, "%Y-%m-%d")
                                except:
                                    data_evento = None

                            memoria_id = db.salvar_memoria(
                                usuario_id=usuario["id"],
                                conteudo=st.session_state["texto_memoria_" + chave_base],
                                titulo=titulo or "Memória registrada via assistente",
                                categoria=categoria or "livre",
                                origem="assistente",
                                local=local or None,
                                data_evento=data_evento or None,
                                pessoas_relacionadas=pessoas_relacionadas or None,
                                visibilidade=visibilidade,
                                contatos_ids=contatos_selecionados,
                            )

                            if foto_memoria:
                                upload = storage.upload_streamlit_file(
                                    bucket="fotos",
                                    arquivo=foto_memoria,
                                    usuario_id=usuario["id"],
                                    pasta="memorias"
                                )

                                caminho_foto = upload["url"]

                                foto_id = db.adicionar_foto_com_acesso(
                                    usuario_id=usuario["id"],
                                    titulo=titulo or "Foto da memória",
                                    descricao=st.session_state["texto_memoria_" + chave_base][:300],
                                    categoria=categoria or "livre",
                                    caminho_arquivo=caminho_foto,
                                    contatos_ids=contatos_selecionados,
                                    visibilidade=visibilidade,
                                )

                                db.associar_foto_memoria(
                                    memoria_id=memoria_id,
                                    foto_id=foto_id
                                )
                            if video_memoria:
                                upload = storage.upload_streamlit_file(
                                    bucket="videos",
                                    arquivo=video_memoria,
                                    usuario_id=usuario["id"],
                                    pasta="memorias"
                                )

                                caminho_video = upload["url"]

                                video_id = db.adicionar_video_com_acesso(
                                    usuario_id=usuario["id"],
                                    titulo=titulo or "Vídeo da memória",
                                    destinatario=pessoas_relacionadas or "",
                                    caminho_arquivo=caminho_video,
                                    contatos_ids=contatos_selecionados,
                                    categoria=categoria or "livre",
                                    visibilidade=visibilidade,
                                )

                                db.associar_video_memoria(
                                    memoria_id=memoria_id,
                                    video_id=video_id
                                )

                            del st.session_state["sugestoes_" + chave_base]
                            del st.session_state["texto_memoria_" + chave_base]

                            st.success("Memória salva no legado.")
                            st.rerun()


        else:
            st.markdown(
                '<div class="ae-simple-bubble-bot">{}</div>'.format(texto_html),
                unsafe_allow_html=True
            )
            fotos = msg.get("fotos", [])

            if fotos:
                st.caption("📷 Fotos relacionadas")

                mostradas = set()

                for foto in fotos:
                    if foto["id"] in mostradas:
                        continue

                    mostradas.add(foto["id"])

                    exibir_foto_segura(
                        foto.get("caminho"),
                        caption=foto.get("titulo", "Foto relacionada"),
                    )

    with st.form("form_assistente_luto", clear_on_submit=True):
        mensagem = st.text_area(
            "Digite sua mensagem",
            placeholder="Escreva aqui...",
            height=120,
            key="mensagem_assistente_luto",
        )

        col_enviar, col_limpar = st.columns([0.65, 0.35])

        with col_enviar:
            enviar = st.form_submit_button(
                "Enviar",
                use_container_width=True,
                type="primary"
            )

        with col_limpar:
            limpar = st.form_submit_button(
                "Limpar",
                use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if limpar:
        st.session_state.historico_assistente = []
        st.rerun()

    if enviar and mensagem.strip():
        st.session_state.historico_assistente.append({
            "tipo": "user",
            "texto": mensagem.strip(),
        })

        try:

            usuario = st.session_state.get("usuario_atual") or {}

            contexto_adicional = ""

            if usuario.get("tipo") == "visitante":
                contexto_adicional = (
                    "A pessoa visitante autorizada se chama {}. "
                    "Ela está registrada como {} de {} e está explorando "
                    "as histórias compartilhadas."
                ).format(
                    usuario.get("nome", "Visitante"),
                    usuario.get("parentesco", "relação não informada"),
                    usuario.get("nome_falecido", "a pessoa responsável pela história")
                )

            resposta = st.session_state.assistente_obj.conversar(
                mensagem.strip(),
                contexto_adicional=contexto_adicional
            )
        except Exception as exc:
            resposta = (
                "Desculpe, tive uma dificuldade para responder agora. "
                "Tente novamente em alguns instantes."
            )
            st.error(f"Erro no assistente: {exc}")

        fotos_relacionadas = []

        usuario = st.session_state.get("usuario_atual") or {}

        if usuario.get("tipo") == "visitante":
            contato_id = usuario.get("id")

            palavras = _extrair_palavras_relevantes(mensagem.strip())

            for palavra in palavras:
                if not isinstance(palavra, str):
                    continue

                resultado = db.buscar_fotos_por_contato_e_texto(
                    contato_id,
                    palavra
                )

                fotos_relacionadas.extend(resultado)

        st.session_state.historico_assistente.append({
            "tipo": "bot",
            "texto": resposta,
            "fotos": fotos_relacionadas
        })

        st.rerun()


def _obter_nome_referencia() -> str:
    usuario = st.session_state.get("usuario_atual") or {}

    if usuario.get("tipo") == "visitante":
        return (
            usuario.get("nome_falecido")
            or usuario.get("falecido_nome")
            or "essa pessoa especial"
        )

    return usuario.get("nome_completo") or "seu legado"


def _inicializar_chat():
    if "historico_assistente" not in st.session_state:
        st.session_state.historico_assistente = []

    usuario = st.session_state.get("usuario_atual") or {}

    modo = "memorial" if usuario.get("tipo") == "visitante" else "legado"

    if modo == "memorial":
        usuario_id_referencia = usuario.get("usuario_id") or usuario.get("falecido_id")
    else:
        usuario_id_referencia = usuario.get("id")

    if (
        "assistente_obj" not in st.session_state
        or st.session_state.get("assistente_modo") != modo
        or st.session_state.get("assistente_usuario_id") != usuario_id_referencia
        or st.session_state.get("assistente_contato_id") != usuario.get("id")
    ):
        st.session_state.assistente_obj = AssistenteLuto(
            usuario_id_referencia,
            modo=modo,
            contato_id=usuario.get("id") if modo == "memorial" else None,
        )
        st.session_state.assistente_modo = modo
        st.session_state.assistente_usuario_id = usuario_id_referencia
        st.session_state.assistente_contato_id = (
            usuario.get("id") if modo == "memorial" else None
        )

    if not st.session_state.historico_assistente:
        if modo == "memorial":
            st.session_state.historico_assistente.append({
                "tipo": "bot",
                "texto": (
                    "Olá. Este é o Assistente de Histórias da aEterna.\n\n"
                    "Estou aqui para ajudar você a explorar histórias, fotos, "
                    "vídeos, valores e momentos compartilhados."
                )
            })
        else:
            st.session_state.historico_assistente.append({
                "tipo": "bot",
                "texto": (
                    "Olá. Este é o seu Assistente de Legado.\n\n"
                    "Estou aqui para ajudar a preservar histórias, valores, aprendizados e lembranças importantes da sua vida."
                )
            })
