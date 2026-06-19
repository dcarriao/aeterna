# utils/agendamentos.py
import streamlit as st
import sqlite3
from datetime import datetime, timedelta


class GerenciadorAgendamentos:
    def __init__(self, db):
        self.db = db

    def renderizar_formulario(self, usuario_id: int, plano: dict):
        """Renderiza o formulário para criar um novo agendamento (Lembrança Programada)"""
        st.markdown("### 📅 Lembrança Programada")
        st.markdown("Programe mensagens ou vídeos para serem enviados em datas especiais.")

        if not plano.get("tem_agendamento", False):
            st.info("💡 Esta funcionalidade estará disponível em breve! Faça upgrade para ter acesso.")
            return None

        # Selecionar contato
        contatos = self.db.listar_contatos_usuario(usuario_id)
        if not contatos:
            st.warning("⚠️ Você precisa cadastrar um contato primeiro.")
            return None

        opcoes_contato = {f"{c['nome_completo']} ({c['email']})": c['id'] for c in contatos}
        contato_selecionado = st.selectbox("Para quem?", list(opcoes_contato.keys()), key="agendamento_contato")
        contato_id = opcoes_contato[contato_selecionado]

        # Tipo de mensagem
        tipo = st.selectbox("Tipo de mensagem", ["texto", "vídeo"], key="agendamento_tipo")

        # Data de envio
        col1, col2 = st.columns(2)
        with col1:
            data_envio = st.date_input("Data de envio", min_value=datetime.now().date(), key="agendamento_data")
        with col2:
            data_termino = st.date_input("Data de término (opcional)", key="agendamento_termino", value=None)

        # Conteúdo
        conteudo = ""
        video_id = None

        if tipo == "texto":
            opcao_texto = st.radio("Como criar o texto?", ["Escrever manualmente", "Receber perguntas do Curador"],
                                   key="agendamento_opcao")

            if opcao_texto == "Escrever manualmente":
                conteudo = st.text_area("Digite sua mensagem:", height=150, key="agendamento_texto")
            else:
                if plano.get("tem_videos_ia", False):
                    st.info("Em breve, o Curador ajudará você com perguntas simples para organizar mensagens.")
                    conteudo = st.text_area("Ou digite manualmente:", height=150, key="agendamento_texto_ia")
                else:
                    st.info("O Curador estará disponível em planos pagos.")
                    conteudo = st.text_area("Digite sua mensagem:", height=150, key="agendamento_texto")
        else:
            # Vídeo - selecionar da biblioteca
            videos = self.db.listar_videos_usuario(usuario_id)
            if videos:
                opcoes_video = {v['titulo']: v['id'] for v in videos}
                video_selecionado = st.selectbox("Selecione um vídeo", list(opcoes_video.keys()),
                                                 key="agendamento_video")
                video_id = opcoes_video[video_selecionado]
            else:
                st.warning("⚠️ Você não tem vídeos cadastrados. Grave um vídeo primeiro.")
                return None

        if st.button("💾 Agendar Lembrança", type="primary", use_container_width=True):
            if tipo == "texto" and not conteudo:
                st.error("❌ Digite uma mensagem")
                return None

            agendamento_id = self.db.criar_agendamento(
                usuario_id=usuario_id,
                contato_id=contato_id,
                tipo=tipo,
                data_envio=data_envio.strftime("%Y-%m-%d"),
                data_termino=data_termino.strftime("%Y-%m-%d") if data_termino else "",
                conteudo=conteudo,
                video_id=video_id,
                gerar_por_ia=1 if tipo == "texto" and opcao_texto == "Receber perguntas do Curador" else 0
            )

            st.success(f"✅ Lembrança agendada para {data_envio.strftime('%d/%m/%Y')}!")
            return agendamento_id
        return None

    def renderizar_lista(self, usuario_id: int):
        """Renderiza a lista de agendamentos"""
        st.markdown("### 📅 Suas Lembranças Programadas")

        agendamentos = self.db.listar_agendamentos_usuario(usuario_id)

        if not agendamentos:
            st.info("📭 Nenhuma lembrança programada. Crie a primeira!")
            return

        for agend in agendamentos:
            with st.expander(f"📌 {agend['tipo'].upper()} para {agend['contato_nome']} - {agend['data_envio']}"):
                st.markdown(f"**Para:** {agend['contato_nome']} ({agend['contato_email']})")
                st.markdown(f"**Data de envio:** {agend['data_envio']}")
                if agend['data_termino']:
                    st.markdown(f"**Data de término:** {agend['data_termino']}")
                st.markdown(f"**Status:** {agend['status']}")
                if agend['conteudo']:
                    st.markdown(f"**Mensagem:** {agend['conteudo'][:200]}...")

                if st.button(f"🗑️ Cancelar", key=f"del_agend_{agend['id']}"):
                    self.db.deletar_agendamento(agend['id'], usuario_id)
                    st.rerun()
