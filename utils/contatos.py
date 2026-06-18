# utils/contatos.py
import streamlit as st
import sqlite3
from datetime import date


class GerenciadorContatos:
    def __init__(self, db):
        self.db = db

    def renderizar_formulario_adicionar(self, usuario_id: int, plano: dict):
        """Renderiza o formulário para adicionar contato"""
        st.markdown("### 👤 Adicionar Contato")

        # Campos obrigatórios
        st.markdown("**📝 Nome e Sobrenome ***")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", key="contato_nome", placeholder="Ex: João", label_visibility="collapsed")
        with col2:
            sobrenome = st.text_input("Sobrenome", key="contato_sobrenome", placeholder="Ex: Silva",
                                      label_visibility="collapsed")

        st.markdown("**📧 Forma de contato ***")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("E-mail", key="contato_email", placeholder="email@exemplo.com",
                                  label_visibility="collapsed")
        with col2:
            whatsapp = st.text_input("WhatsApp", key="contato_whatsapp", placeholder="(11) 99999-9999",
                                     label_visibility="collapsed")

        st.caption("⚠️ Pelo menos um contato (e-mail ou WhatsApp) é obrigatório")

        # Campos opcionais
        st.markdown("---")
        st.markdown("#### ✨ Informações adicionais (opcional)")

        col1, col2 = st.columns(2)
        with col1:
            parentesco = st.text_input("Grau de parentesco", key="contato_parentesco",
                                       placeholder="Ex: Filho, Esposa, Amigo")
            data_nascimento = st.date_input(
                                "Data de nascimento",
                                value=date(1990, 1, 1),
                                min_value=date(1900, 1, 1),
                                max_value=date.today(),
                                format="DD/MM/YYYY",
                                key="contato_data_nascimento"
                            )
        with col2:
            acesso_central_luto = st.checkbox("Dar acesso ao Assistente de Histórias", key="contato_acesso_luto")
            prioridade = st.checkbox("Marcar como contato prioritário", key="contato_prioridade")

        # Datas especiais (JSON)
        st.markdown("**📅 Datas especiais**")
        st.caption("Datas que você quer lembrar (ex: aniversário, Natal, etc.)")
        datas_especiais = st.text_area("Datas (uma por linha, formato: DD/MM - Descrição)",
                                       key="contato_datas", height=80,
                                       placeholder="15/05 - Aniversário\n25/12 - Natal\n10/10 - Dia do Amigo")

        # Verificar limites do plano
        contatos_atual = self.db.contar_contatos_usuario(usuario_id)
        max_contatos = plano.get("max_contatos", 5)

        if contatos_atual >= max_contatos:
            st.warning(
                f"⚠️ Você atingiu o limite de {max_contatos} contatos do seu plano. Para adicionar mais, faça upgrade.")
            return None

        if prioridade:
            prioridades_atual = self.db.contar_contatos_prioritarios(usuario_id)
            max_prioridades = plano.get("max_prioridades", 3)
            if prioridades_atual >= max_prioridades:
                st.warning(
                    f"⚠️ Você já tem {prioridades_atual} contatos prioritários. O limite do seu plano é {max_prioridades}.")
                return None

        if st.button("💾 Salvar Contato", type="primary", use_container_width=True):
            if not nome or not sobrenome:
                st.error("❌ Nome e sobrenome são obrigatórios")
                return None
            if not email and not whatsapp:
                st.error("❌ Informe pelo menos um contato (e-mail ou WhatsApp)")
                return None

            import secrets
            chave_acesso = secrets.token_hex(8)

            # Processar datas especiais
            datas_json = {}
            if datas_especiais:
                for linha in datas_especiais.split('\n'):
                    if linha.strip():
                        partes = linha.split('-', 1)
                        if len(partes) == 2:
                            datas_json[partes[0].strip()] = partes[1].strip()

            import json
            datas_str = json.dumps(datas_json) if datas_json else ""

            self.db.adicionar_contato(
                usuario_id=usuario_id,
                nome=nome,
                sobrenome=sobrenome,
                email=email or "",
                telefone="",  # telefone fixo (opcional)
                whatsapp=whatsapp or "",
                parentesco=parentesco or "",
                data_nascimento=data_nascimento.strftime("%Y-%m-%d") if data_nascimento else "",
                datas_especiais=datas_str,
                is_prioridade=1 if prioridade else 0,
                prioridade_order=prioridades_atual + 1 if prioridade else 0,
                acesso_central_luto=1 if acesso_central_luto else 0,
                chave_acesso=chave_acesso
            )

            st.success(f"✅ {nome} {sobrenome} adicionado com sucesso!")
            st.info(f"🔑 Chave de acesso: `{chave_acesso}`")
            st.warning("📌 Guarde esta chave e envie para a pessoa.")
            return True
        return None

    def renderizar_lista_contatos(self, usuario_id: int):
        """Renderiza a lista de contatos"""
        st.markdown("### 👥 Seus Contatos")

        contatos = self.db.listar_contatos_usuario(usuario_id)

        if not contatos:
            st.info("📭 Nenhum contato cadastrado ainda. Adicione pessoas de confiança.")
            return

        # Separar prioritários e não prioritários
        prioritarios = [c for c in contatos if c.get("is_prioridade")]
        nao_prioritarios = [c for c in contatos if not c.get("is_prioridade")]

        if prioritarios:
            st.markdown("#### ⭐ Contatos Prioritários")
            for i, contato in enumerate(prioritarios, 1):
                with st.expander(f"{i}º - 👤 {contato['nome_completo']}"):
                    st.markdown(f"**📧 Email:** {contato['email']}")
                    st.markdown(f"**📱 WhatsApp:** {contato['whatsapp'] or 'Não informado'}")
                    st.markdown(f"**👨‍👩‍👧 Parentesco:** {contato['parentesco'] or 'Não informado'}")
                    st.markdown(
                        f"**🔓 Acesso às histórias:** {'✅ Sim' if contato.get('acesso_central_luto') else '❌ Não'}")
                    if contato.get('data_nascimento'):
                        st.markdown(f"**🎂 Data de nascimento:** {contato['data_nascimento']}")

                    if st.button(f"🗑️ Remover", key=f"del_contato_{contato['id']}"):
                        self.db.deletar_contato(contato['id'], usuario_id)
                        st.rerun()

        if nao_prioritarios:
            st.markdown("#### 📌 Outros Contatos")
            for contato in nao_prioritarios:
                with st.expander(f"👤 {contato['nome_completo']}"):
                    st.markdown(f"**📧 Email:** {contato['email']}")
                    st.markdown(f"**📱 WhatsApp:** {contato['whatsapp'] or 'Não informado'}")
                    st.markdown(f"**👨‍👩‍👧 Parentesco:** {contato['parentesco'] or 'Não informado'}")
                    if contato.get('data_nascimento'):
                        st.markdown(f"**🎂 Data de nascimento:** {contato['data_nascimento']}")

                    if st.button(f"🗑️ Remover", key=f"del_contato_{contato['id']}"):
                        self.db.deletar_contato(contato['id'], usuario_id)
                        st.rerun()
