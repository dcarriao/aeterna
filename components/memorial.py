import streamlit as st
import html
import json
import os
from datetime import datetime, date
from openai import OpenAI
from utils.banco import BancoDados
from utils.storage import StorageAeterna
from utils.media import exibir_foto_segura

storage = StorageAeterna()
db = BancoDados()

def _get_openai_client():
    api_key = db._get_secret("OPENAI_API_KEY") if hasattr(db, "_get_secret") else os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def render_criar_memorial():
    st.markdown("""
    <style>
    .main .block-container,
    .block-container,
    [data-testid="stMainBlockContainer"] {
        max-width: 900px !important;
        width: min(900px, calc(100vw - 250px)) !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    .ae-memorial-header {
        color: #2B1747;
        font-weight: 950;
        font-size: 1.58rem;
        margin-bottom: 0.15rem;
    }
    .ae-memorial-subheader {
        color: #6F6478;
        font-size: 0.86rem;
        margin-bottom: 1.15rem;
    }
    .stButton>button {
        border-radius: 14px !important;
        font-weight: 950 !important;
        min-height: 2.5rem !important;
    }
    .st-key-memorial_finish_btn button {
        background: #2B1747 !important;
        color: white !important;
        border: none !important;
    }
    .st-key-memorial_curador_btn button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ae-memorial-header">🤍 Novo Memorial</div>', unsafe_allow_html=True)
    st.markdown('<div class="ae-memorial-subheader">Preencha o perfil da pessoa para preservar seu legado e memórias para sempre.</div>', unsafe_allow_html=True)

    usuario_id = st.session_state.usuario_atual["id"]
    contatos = []
    try:
        contatos = db.listar_contatos_usuario(usuario_id) or []
    except Exception as exc:
        print("Erro ao listar contatos:", exc)
    nomes_contatos = [c.get("nome_completo") for c in contatos if c.get("nome_completo")]

    with st.form("form_criar_memorial"):
        nome = st.text_input("Nome completo do homenageado *", placeholder="Ex: Maria de Souza Silva")
        
        c_dates = st.columns(2, gap="small")
        with c_dates[0]:
            data_nascimento = st.date_input("Data de nascimento", value=None, format="DD/MM/YYYY")
        with c_dates[1]:
            data_falecimento = st.date_input("Data de falecimento", value=None, format="DD/MM/YYYY")
            
        c_rel_vis = st.columns(2, gap="small")
        with c_rel_vis[0]:
            parentesco = st.selectbox("Relação com você", ["Pai", "Mãe", "Avô", "Avó", "Irmão", "Irmã", "Tio", "Tia", "Cônjuge", "Amigo(a)", "Outro"])
        with c_rel_vis[1]:
            visibilidade = st.selectbox("Configuração de privacidade", ["privado", "contatos"], format_func=lambda x: "Privado (só eu vejo)" if x == "privado" else "Compartilhado com meus contatos")
            
        biografia = st.text_area("Breve biografia ou introdução", placeholder="Fale um pouco sobre quem foi essa pessoa especial, seus principais valores ou uma mensagem de saudade...", height=110)
        
        foto_perfil = st.file_uploader("Foto principal (opcional)", type=["png", "jpg", "jpeg", "webp"])
        
        convidados = st.multiselect("Convidados para contribuir (opcional)", options=nomes_contatos, placeholder="Escolha contatos que podem contribuir com histórias e fotos")
        
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        c_btns = st.columns(2, gap="small")
        with c_btns[0]:
            finalizar = st.form_submit_button("💾 Finalizar criação do Memorial", use_container_width=True)
        with c_btns[1]:
            continuar_curador = st.form_submit_button("✨ Continuar com o Curador de Perfil", use_container_width=True)

    if finalizar or continuar_curador:
        if not nome.strip():
            st.error("❌ O nome do homenageado é obrigatório.")
        else:
            try:
                foto_url = ""
                if foto_perfil:
                    upload = storage.upload_streamlit_file("fotos", foto_perfil, usuario_id, "memoriais")
                    foto_url = upload["url"]
                
                nasc_str = data_nascimento.strftime("%Y-%m-%d") if data_nascimento else None
                fal_str = data_falecimento.strftime("%Y-%m-%d") if data_falecimento else None
                
                memorial_id = db.criar_memorial(
                    usuario_id=usuario_id,
                    nome=nome.strip(),
                    foto_perfil=foto_url,
                    data_nascimento=nasc_str,
                    data_falecimento=fal_str,
                    parentesco=parentesco,
                    biografia=biografia.strip(),
                    visibilidade=visibilidade
                )
                
                # Link selected contacts to the memorial
                opcoes_contato = {c["nome_completo"]: c["id"] for c in contatos if c.get("nome_completo")}
                convites_pessoas = convidados
                for nome_c in convites_pessoas:
                    contato_id = opcoes_contato.get(nome_c)
                    if contato_id:
                        # We can link the contact to this memorial by updating it
                        db.executar(db.conectar(), "UPDATE contatos SET memorial_id = %s WHERE id = %s", (memorial_id, contato_id))
                
                st.success("✅ Memorial criado com sucesso!")
                
                if continuar_curador:
                    st.session_state.pagina_atual = f"memorial_curador_{memorial_id}"
                else:
                    st.session_state.pagina_atual = f"memorial_ver_{memorial_id}"
                st.rerun()
            except Exception as e:
                print("Erro ao criar memorial:", e)
                st.error("Não foi possível criar o memorial no momento.")

def render_memoriais_lista():
    st.markdown("""
    <style>
    .ae-memorial-header {
        color: #2B1747;
        font-weight: 950;
        font-size: 1.58rem;
        margin-bottom: 0.15rem;
    }
    .ae-memorial-subheader {
        color: #6F6478;
        font-size: 0.86rem;
        margin-bottom: 1.15rem;
    }
    .ae-memorial-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.15rem;
        margin-top: 0.85rem;
    }
    .ae-memorial-card {
        background: #FFFFFF;
        border: 1.5px solid rgba(212, 168, 79, 0.22);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 10px 30px rgba(43,23,71,0.03);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .ae-memorial-card-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #D4AF37;
        margin-bottom: 0.55rem;
    }
    .ae-memorial-card-img-placeholder {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #F4EEFC;
        border: 2px solid #C1B1E7;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        margin-bottom: 0.55rem;
    }
    .ae-memorial-card-nome {
        color: #2B1747;
        font-weight: 900;
        font-size: 1.05rem;
        margin-bottom: 0.15rem;
    }
    .ae-memorial-card-rel {
        color: #B77A46;
        font-weight: 800;
        font-size: 0.78rem;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .ae-memorial-card-dates {
        color: #6F6478;
        font-size: 0.74rem;
        margin-bottom: 0.85rem;
    }
    .stButton>button {
        border-radius: 12px !important;
        font-size: 0.82rem !important;
        min-height: 2.15rem !important;
    }
    .ae-btn-gold button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
        font-weight: 900 !important;
    }
    .ae-btn-purple button {
        background: #2B1747 !important;
        color: white !important;
        border: none !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ae-memorial-header">🤍 Memorial de Legados</div>', unsafe_allow_html=True)
    st.markdown('<div class="ae-memorial-subheader">Preserve e honre a história de pessoas amadas que já partiram, compartilhando lembranças eternas.</div>', unsafe_allow_html=True)

    usuario_id = st.session_state.usuario_atual["id"]
    
    st.markdown('<div class="ae-btn-gold">', unsafe_allow_html=True)
    if st.button("➕ Criar Memorial", key="btn_goto_criar_memorial"):
        st.session_state.pagina_atual = "memorial_criar"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    try:
        memoriais = db.listar_memoriais_usuario(usuario_id) or []
    except Exception as e:
        print("Erro ao listar memoriais:", e)
        memoriais = []

    if not memoriais:
        st.info("💡 Você ainda não possui nenhum memorial criado. Clique acima para começar a preservar um lindo legado.")
        return

    st.markdown('<div class="ae-memorial-grid">', unsafe_allow_html=True)
    for m in memoriais:
        st.markdown(f'<div class="ae-memorial-card">', unsafe_allow_html=True)
        if m["foto_perfil"]:
            st.markdown(f'<img src="{m["foto_perfil"]}" class="ae-memorial-card-img" />', unsafe_allow_html=True)
        else:
            st.markdown('<div class="ae-memorial-card-img-placeholder">👤</div>', unsafe_allow_html=True)
            
        st.markdown(f'<div class="ae-memorial-card-nome">{html.escape(m["nome"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ae-memorial-card-rel">{html.escape(m["parentesco"] or "Homenageado(a)")}</div>', unsafe_allow_html=True)
        
        nasc = datetime.strptime(str(m["data_nascimento"]), "%Y-%m-%d").strftime("%d/%m/%Y") if m["data_nascimento"] else "N/A"
        fal = datetime.strptime(str(m["data_falecimento"]), "%Y-%m-%d").strftime("%d/%m/%Y") if m["data_falecimento"] else "N/A"
        st.markdown(f'<div class="ae-memorial-card-dates">🌟 {nasc}  ✝️ {fal}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="ae-btn-purple" style="width:100%;">', unsafe_allow_html=True)
        if st.button("📖 Abrir Memorial", key=f"btn_abrir_mem_{m['id']}", use_container_width=True):
            st.session_state.pagina_atual = f"memorial_ver_{m['id']}"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="ae-btn-gold" style="width:100%; margin-top:0.35rem;">', unsafe_allow_html=True)
        if st.button("✨ Curador de Perfil", key=f"btn_curador_mem_{m['id']}", use_container_width=True):
            st.session_state.pagina_atual = f"memorial_curador_{m['id']}"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_curador_perfil(memorial_id):
    st.markdown("""
    <style>
    .main .block-container,
    .block-container,
    [data-testid="stMainBlockContainer"] {
        max-width: 1000px !important;
        width: min(1000px, calc(100vw - 250px)) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: -3.5rem !important;
    }
    .ae-curador-header {
        color: #2B1747;
        font-weight: 950;
        font-size: 1.48rem;
        margin-bottom: 0.15rem;
    }
    .ae-curador-subheader {
        color: #6F6478;
        font-size: 0.84rem;
        margin-bottom: 1.15rem;
    }
    .ae-chat-container {
        border: 1px solid rgba(193, 177, 231, 0.45);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.78);
        padding: 1rem;
        min-height: 380px;
        box-shadow: 0 10px 30px rgba(43,23,71,0.03);
        margin-bottom: 0.85rem;
    }
    .ae-chat-bubble-assistant {
        background: #F4EEFC;
        border: 1px solid rgba(193, 177, 231, 0.4);
        border-radius: 14px;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.58rem;
        color: #2B1747;
        max-width: 85%;
        text-align: left;
    }
    .ae-chat-bubble-user {
        background: #2B1747;
        border-radius: 14px;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.58rem;
        color: white !important;
        max-width: 85%;
        margin-left: auto;
        text-align: right;
    }
    .ae-chat-bubble-user * {
        color: white !important;
    }
    .stButton>button {
        border-radius: 14px !important;
        font-weight: 950 !important;
        min-height: 2.45rem !important;
    }
    .st-key-curador_perfil_enviar button {
        background: linear-gradient(135deg, #f8dc92, #d4af37 62%, #b77a46) !important;
        color: #1b0f2e !important;
        border: none !important;
    }
    .st-key-curador_perfil_interromper button,
    .st-key-curador_perfil_voltar button {
        background: rgba(255,255,255,0.85) !important;
        color: #2B1747 !important;
        border: 1px solid rgba(43,23,71,0.22) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    memorial = db.obter_memorial(memorial_id)
    if not memorial:
        st.error("Memorial não encontrado.")
        return

    st.markdown(f'<div class="ae-curador-header">✨ Curador de Perfil: {html.escape(memorial["nome"])}</div>', unsafe_allow_html=True)
    st.markdown('<div class="ae-curador-subheader">Converse com o Curador para resgatar ricas lembranças e construir o perfil biográfico do homenageado.</div>', unsafe_allow_html=True)

    # Initialize or load conversation history
    conversa = []
    if memorial["conversa_curador"]:
        try:
            conversa = json.loads(memorial["conversa_curador"])
        except Exception:
            conversa = []

    # If empty, start with the first assistant question
    if not conversa:
        conversa.append({
            "role": "assistant",
            "content": f"Olá! Eu sou o Curador de Perfil da aEterna. Estou aqui para ajudar você a registrar e eternizar as mais belas memórias de {memorial['nome']}. Para começarmos, você poderia me contar um pouco sobre a personalidade de {memorial['nome']}? O que mais definia seu jeito de ser?"
        })
        db.atualizar_conversa_curador_memorial(memorial_id, json.dumps(conversa), "conversa")

    # Display Chat Bubble History
    st.markdown('<div class="ae-chat-container">', unsafe_allow_html=True)
    for msg in conversa:
        classe = "ae-chat-bubble-assistant" if msg["role"] == "assistant" else "ae-chat-bubble-user"
        st.markdown(f'<div class="{classe}">{html.escape(msg["content"])}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # User input
    with st.form("form_curador_perfil_input", clear_on_submit=True):
        user_response = st.text_input("Sua resposta para o Curador", placeholder="Escreva aqui...")
        c_btns = st.columns([0.7, 0.3], gap="small")
        with c_btns[0]:
            enviar = st.form_submit_button("✨ Enviar resposta", use_container_width=True)
        with c_btns[1]:
            interromper = st.form_submit_button("🛑 Interromper e salvar", use_container_width=True)

    # Back button
    if st.button("← Voltar para a lista", key="curador_perfil_voltar"):
        st.session_state.pagina_atual = "memorial_lista"
        st.rerun()

    if enviar and user_response.strip():
        # Append user message
        conversa.append({"role": "user", "content": user_response.strip()})
        db.atualizar_conversa_curador_memorial(memorial_id, json.dumps(conversa), "conversa")
        st.rerun()

    if len(conversa) > 0 and conversa[-1]["role"] == "user":
        # Generate the next AI question based on conversation history
        with st.spinner("O Curador está refletindo..."):
            client = _get_openai_client()
            if client:
                try:
                    system_prompt = f"""
Você é o Curador de Perfil do Memorial da aEterna.
Seu objetivo é ajudar o responsável pelo memorial de {memorial['nome']} (relação: {memorial['parentesco']}) a recordar e registrar informações valiosas sobre a vida dessa pessoa.

Exemplos de temas que você deve explorar de forma natural e empática ao longo da conversa:
- personalidade, valores, infância, família, amizades, profissão, hobbies, gostos, sonhos, conquistas, dificuldades, histórias marcantes, conselhos que costumava dar, frases que costumava repetir, momentos importantes, viagens, tradições familiares, características marcantes.

Regras importantes:
1. Você NÃO fala como se fosse {memorial['nome']}. Você conversa COM o responsável pelo memorial sobre ela.
2. Seja extremamente empático, respeitoso e acolhedor (utilize linguagem compatível com memória, legado, histórias e saudade).
3. Conduza uma conversa natural. Faça APENAS UMA pergunta de cada vez, baseando-se no contexto das respostas anteriores fornecidas pelo usuário. Não use um questionário fixo.
4. Escreva respostas curtas, afetuosas e focadas (máximo 4-5 linhas).
                    """.strip()
                    
                    messages = [{"role": "system", "content": system_prompt}]
                    for msg in conversa:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                        
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        max_tokens=250,
                        temperature=0.7
                    )
                    
                    ai_text = response.choices[0].message.content.strip()
                    conversa.append({"role": "assistant", "content": ai_text})
                    db.atualizar_conversa_curador_memorial(memorial_id, json.dumps(conversa), "conversa")
                    st.rerun()
                except Exception as exc:
                    print("Erro no Curador de Perfil:", exc)
                    st.error("Não foi possível conectar com o Curador no momento.")
            else:
                st.error("Serviço de IA temporariamente indisponível.")

    if interromper:
        st.success("✅ Progresso da conversa salvo com sucesso!")
        st.session_state.pagina_atual = f"memorial_ver_{memorial_id}"
        st.rerun()

def render_pagina_memorial(memorial_id):
    st.markdown("""
    <style>
    .ae-memorial-banner {
        background: radial-gradient(circle at 18% 8%, rgba(242,197,114,0.14), transparent 24%),
                    linear-gradient(135deg, #140322 0%, #2b1747 100%);
        border: 1px solid rgba(212,175,55,0.35);
        border-radius: 28px;
        padding: 1.5rem;
        margin-bottom: 1.15rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        color: white !important;
        box-shadow: 0 14px 34px rgba(0,0,0,0.15);
    }
    .ae-memorial-banner * {
        color: white !important;
    }
    .ae-memorial-banner-img {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #f2c572;
    }
    .ae-memorial-banner-img-placeholder {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        border: 3px solid rgba(255,255,255,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
    }
    .ae-memorial-banner-nome {
        font-family: "Cormorant Garamond", Georgia, serif;
        font-size: 2.2rem;
        color: #f2c572 !important;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.35rem;
    }
    .ae-memorial-banner-info {
        font-size: 0.82rem;
        color: rgba(255,255,255,0.72) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: nowrap;
        background-color: rgba(255, 255, 255, 0.4) !important;
        border: 1px solid rgba(212, 168, 79, 0.15) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0 16px !important;
        font-size: 0.84rem !important;
        font-weight: 800 !important;
        color: #6F6478 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        border-color: rgba(212, 168, 79, 0.28) !important;
        color: #2B1747 !important;
    }
    .ae-timeline-item {
        background: white;
        border-left: 3px solid #D4AF37;
        padding-left: 0.85rem;
        margin-bottom: 0.85rem;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    .ae-card-header {
        font-weight: 900;
        color: #2B1747;
    }
    </style>
    """, unsafe_allow_html=True)

    memorial = db.obter_memorial(memorial_id)
    if not memorial:
        st.error("Memorial não encontrado.")
        return

    usuario_id = st.session_state.usuario_atual["id"]
    is_owner = (memorial["usuario_id"] == usuario_id)

    # 1. Header Banner
    st.markdown('<div class="ae-memorial-banner">', unsafe_allow_html=True)
    if memorial["foto_perfil"]:
        st.markdown(f'<img src="{memorial["foto_perfil"]}" class="ae-memorial-banner-img" />', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ae-memorial-banner-img-placeholder">👤</div>', unsafe_allow_html=True)
        
    st.markdown('<div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ae-memorial-banner-nome">{html.escape(memorial["nome"])}</div>', unsafe_allow_html=True)
    
    nasc = datetime.strptime(str(memorial["data_nascimento"]), "%Y-%m-%d").strftime("%d/%m/%Y") if memorial["data_nascimento"] else "N/A"
    fal = datetime.strptime(str(memorial["data_falecimento"]), "%Y-%m-%d").strftime("%d/%m/%Y") if memorial["data_falecimento"] else "N/A"
    st.markdown(f'<div class="ae-memorial-banner-info">🌟 {nasc}  ✝️ {fal}  &nbsp;|&nbsp;  Relação: {html.escape(memorial["parentesco"] or "Homenageado(a)")}</div>', unsafe_allow_html=True)
    if memorial["biografia"]:
        st.markdown(f'<div style="font-size:0.86rem; margin-top:0.45rem; line-height:1.4; font-style:italic;">"{html.escape(memorial["biografia"])}"</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Main Page Navigation and Tabs
    tab_timeline, tab_stories, tab_photos, tab_videos, tab_people, tab_curador, tab_contribs = st.tabs([
        "📅 Linha do Tempo",
        "📖 Histórias",
        "📷 Fotos",
        "🎥 Vídeos",
        "👥 Pessoas Relacionadas",
        "✨ Conversar com o Memorial",
        "📥 Contribuições"
    ])

    # Fetch contents
    memorias_list = db.listar_memorias_memorial(memorial_id) or []
    fotos_list = db.listar_fotos_memorial(memorial_id) or []
    videos_list = db.listar_videos_memorial(memorial_id) or []
    contatos_list = db.listar_contatos_memorial(memorial_id) or []

    # Tab 1: Timeline
    with tab_timeline:
        st.markdown("### 📅 Linha do Tempo")
        all_events = []
        for m in memorias_list:
            if m["data_evento"]:
                all_events.append({"tipo": "historia", "titulo": m["titulo"], "data": m["data_evento"], "conteudo": m["conteudo"]})
                
        all_events = sorted(all_events, key=lambda x: x["data"], reverse=True)
        
        if not all_events:
            st.info("Nenhum evento com data aproximada cadastrado na linha do tempo ainda.")
        else:
            for item in all_events:
                dt_f = datetime.strptime(str(item["data"]), "%Y-%m-%d").strftime("%d/%m/%Y")
                st.markdown(f"""
                <div class="ae-timeline-item">
                    <div style="font-size:0.75rem; color:#B77A46; font-weight:800;">{dt_f}</div>
                    <div class="ae-card-header">{html.escape(item["titulo"])}</div>
                    <div style="font-size:0.84rem; color:#6F6478; margin-top:0.15rem;">{html.escape(item["conteudo"][:250])}...</div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 2: Stories / Memories
    with tab_stories:
        st.markdown("### 📖 Histórias & Lembranças")
        if is_owner:
            with st.expander("✍️ Adicionar nova história"):
                with st.form("form_add_memoria_memorial"):
                    t_title = st.text_input("Título")
                    t_content = st.text_area("O que aconteceu? *")
                    t_date = st.date_input("Data (opcional)", value=None)
                    t_cat = st.selectbox("Categoria", ["Momentos", "Família", "Viagens", "Infância", "Trabalho", "Outro"])
                    t_submit = st.form_submit_button("Salvar na História")
                    
                if t_submit and t_content.strip():
                    try:
                        db.salvar_memoria(
                            usuario_id=usuario_id,
                            conteudo=t_content.strip(),
                            titulo=t_title.strip() or "Memória sem título",
                            categoria=t_cat,
                            origem="memorial",
                            data_evento=t_date.strftime("%Y-%m-%d") if t_date else None,
                            visibilidade="contatos",
                            memorial_id=memorial_id
                        )
                        st.success("História salva com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")
                        
        if not memorias_list:
            st.info("Nenhuma história registrada neste memorial ainda.")
        else:
            for m in memorias_list:
                with st.expander(m["titulo"]):
                    st.write(m["conteudo"])
                    if m["data_evento"]:
                        dt_f = datetime.strptime(str(m["data_evento"]), "%Y-%m-%d").strftime("%d/%m/%Y")
                        st.caption(f"🗓️ Data do momento: {dt_f} &nbsp;|&nbsp; Categoria: {m['categoria']}")

    # Tab 3: Photos
    with tab_photos:
        st.markdown("### 📷 Álbum de Fotos")
        if is_owner:
            with st.expander("📷 Adicionar foto"):
                with st.form("form_add_foto_memorial"):
                    f_title = st.text_input("Título da foto")
                    f_desc = st.text_input("Descrição")
                    f_file = st.file_uploader("Arquivo de imagem *", type=["png", "jpg", "jpeg", "webp"])
                    f_submit = st.form_submit_button("Adicionar ao Álbum")
                    
                if f_submit and f_file:
                    try:
                        upload = storage.upload_streamlit_file("fotos", f_file, usuario_id, "memoriais")
                        db.adicionar_foto_com_acesso(
                            usuario_id=usuario_id,
                            titulo=f_title.strip() or "Foto",
                            descricao=f_desc.strip(),
                            categoria="Outro",
                            caminho_arquivo=upload["url"],
                            contatos_ids=[],
                            visibilidade="contatos",
                            memorial_id=memorial_id
                        )
                        st.success("Foto adicionada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar foto: {e}")
                        
        if not fotos_list:
            st.info("Nenhuma foto cadastrada no álbum ainda.")
        else:
            c_cols = st.columns(3)
            for idx, foto in enumerate(fotos_list):
                with c_cols[idx % 3]:
                    exibir_foto_segura(foto["caminho_arquivo"], caption=foto["titulo"])
                    if foto["descricao"]:
                        st.caption(foto["descricao"])

    # Tab 4: Videos
    with tab_videos:
        st.markdown("### 🎥 Vídeos")
        if is_owner:
            with st.expander("🎥 Adicionar vídeo"):
                with st.form("form_add_video_memorial"):
                    v_title = st.text_input("Título do vídeo")
                    v_file = st.file_uploader("Arquivo de vídeo *", type=["mp4", "mov", "avi", "mkv"])
                    v_submit = st.form_submit_button("Adicionar Vídeo")
                    
                if v_submit and v_file:
                    try:
                        upload = storage.upload_streamlit_file("videos", v_file, usuario_id, "memoriais")
                        db.adicionar_video_com_acesso(
                            usuario_id=usuario_id,
                            titulo=v_title.strip() or "Vídeo",
                            destinatario="",
                            caminho_arquivo=upload["url"],
                            contatos_ids=[],
                            categoria="Outro",
                            visibilidade="contatos",
                            memorial_id=memorial_id
                        )
                        st.success("Vídeo adicionado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar vídeo: {e}")
                        
        if not videos_list:
            st.info("Nenhum vídeo cadastrado no memorial ainda.")
        else:
            c_cols = st.columns(2)
            for idx, video in enumerate(videos_list):
                with c_cols[idx % 2]:
                    st.video(video["caminho_arquivo"])
                    st.write(f"**{html.escape(video['titulo'])}**")

    # Tab 5: Related People
    with tab_people:
        st.markdown("### 👥 Pessoas Relacionadas")
        if is_owner:
            with st.expander("👥 Vincular contato ao memorial"):
                try:
                    all_user_contatos = db.listar_contatos_usuario(usuario_id) or []
                except Exception:
                    all_user_contatos = []
                opcoes_c = {f"{c['nome']} {c['sobrenome']}": c["id"] for c in all_user_contatos if c.get("nome")}
                
                with st.form("form_vincular_contato_memorial"):
                    cont_selected = st.selectbox("Escolha um contato", options=list(opcoes_c.keys()))
                    v_submit = st.form_submit_button("Vincular")
                    
                if v_submit and cont_selected:
                    c_id = opcoes_c[cont_selected]
                    db.executar(db.conectar(), "UPDATE contatos SET memorial_id = %s WHERE id = %s", (memorial_id, c_id))
                    st.success("Contato vinculado com sucesso!")
                    st.rerun()
                    
        if not contatos_list:
            st.info("Nenhuma pessoa relacionada vinculada a este memorial ainda.")
        else:
            for c in contatos_list:
                st.markdown(f"👤 **{html.escape(c['nome'])} {html.escape(c['sobrenome'])}** ({html.escape(c['parentesco'] or 'Relação não informada')})")

    # Tab 6: Conversar com o Memorial (Curador da Página)
    with tab_curador:
        st.markdown("### ✨ Conversar com o Memorial")
        st.caption(f"Tire dúvidas, recorde momentos e saiba mais sobre {memorial['nome']} de forma empática baseando-se apenas nos registros salvos.")
        
        # Build context for RAG/IA Curador do Memorial
        contexto_textos = []
        contexto_textos.append(f"Nome do Homenageado: {memorial['nome']}")
        contexto_textos.append(f"Relação: {memorial['parentesco']}")
        if memorial['biografia']:
            contexto_textos.append(f"Biografia/Descrição inicial: {memorial['biografia']}")
            
        for m in memorias_list:
            contexto_textos.append(f"Lembrança/História '{m['titulo']}': {m['conteudo']}")
            
        # Also load the conversation history of Curador de Perfil to enrich context
        conversa_perfil_text = ""
        if memorial["conversa_curador"]:
            try:
                conversa_json = json.loads(memorial["conversa_curador"])
                conversa_perfil_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in conversa_json])
            except Exception:
                pass
        if conversa_perfil_text:
            contexto_textos.append(f"Entrevistas e fatos levantados pelo Curador de Perfil:\n{conversa_perfil_text}")
            
        contexto_memorial = "\n\n".join(contexto_textos)

        # Chat interface
        chat_key = f"chat_memorial_{memorial_id}"
        if chat_key not in st.session_state:
            st.session_state[chat_key] = [{
                "role": "assistant",
                "content": f"Olá! Eu sou o Curador do Memorial de {memorial['nome']}. Você pode me perguntar sobre suas histórias, valores, viagens, lembranças de infância e ensinamentos. Responderei com base apenas nos registros preservados aqui. Como posso ajudar você a relembrar hoje?"
            }]

        for msg in st.session_state[chat_key]:
            classe = "ae-chat-bubble-assistant" if msg["role"] == "assistant" else "ae-chat-bubble-user"
            st.markdown(f'<div class="{classe}">{html.escape(msg["content"])}</div>', unsafe_allow_html=True)

        with st.form(f"form_chat_memorial_{memorial_id}", clear_on_submit=True):
            user_msg = st.text_input("Sua pergunta", placeholder="Ex: O que ele gostava de fazer?")
            enviar_chat = st.form_submit_button("Perguntar")

        if enviar_chat and user_msg.strip():
            st.session_state[chat_key].append({"role": "user", "content": user_msg.strip()})
            st.rerun()

        if len(st.session_state[chat_key]) > 0 and st.session_state[chat_key][-1]["role"] == "user":
            with st.spinner("Buscando nos registros e refletindo..."):
                client = _get_openai_client()
                if client:
                    try:
                        system_prompt = f"""
Você é o Curador do Memorial de {memorial['nome']}.
Seu objetivo é responder perguntas de familiares e amigos sobre a vida, histórias, valores, aprendizados e momentos marcantes de {memorial['nome']}.

Regras importantes:
1. Você NÃO deve responder como se fosse {memorial['nome']}. Nunca fale na primeira pessoa ("eu"). Responda sempre na terceira pessoa sobre {memorial['nome']}.
2. Use EXCLUSIVAMENTE o contexto fornecido sobre o memorial de {memorial['nome']}. Não invente fatos, datas, pessoas ou locais.
3. Se a informação solicitada não estiver disponível no contexto abaixo, responda de forma muito empática e respeitosa que ainda não há conteúdo registrado sobre esse assunto no memorial.
4. Nunca invente nenhuma informação ("alucinações").

Contexto disponível sobre {memorial['nome']}:
{contexto_memorial}
                        """.strip()
                        
                        messages = [{"role": "system", "content": system_prompt}]
                        for msg in st.session_state[chat_key]:
                            messages.append({"role": msg["role"], "content": msg["content"]})
                            
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            max_tokens=250,
                            temperature=0.4
                        )
                        
                        ai_resp = response.choices[0].message.content.strip()
                        st.session_state[chat_key].append({"role": "assistant", "content": ai_resp})
                        st.rerun()
                    except Exception as e:
                        print("Erro no Curador de Memorial:", e)
                        st.error("Não foi possível processar a pergunta agora.")
                else:
                    st.error("Serviço de IA indisponível.")

    # Tab 7: Contributions
    with tab_contribs:
        st.markdown("### 📥 Contribuições")
        
        # Owner side - approve/rejest
        if is_owner:
            st.markdown("#### Contribuições Pendentes para aprovação")
            try:
                pendentes = db.listar_contribuicoes_memorial_status(memorial_id, "pendente") or []
            except Exception:
                pendentes = []
                
            if not pendentes:
                st.info("Nenhuma contribuição pendente para aprovação.")
            else:
                for p in pendentes:
                    st.markdown(f"**Autor(a):** {html.escape(p['usuario_contribuidor_nome'])} ({html.escape(p['usuario_contribuidor_email'])})")
                    st.markdown(f"**Tipo:** {html.escape(p['tipo_contribuicao'])}")
                    if p["texto"]:
                        st.markdown(f'*" {html.escape(p["texto"])} "*')
                    if p["arquivo_url"]:
                        st.markdown(f"[Ver arquivo contribuído]({p['arquivo_url']})")
                        
                    c_eval = st.columns(2)
                    with c_eval[0]:
                        if st.button("✅ Aprovar", key=f"btn_aprov_cont_{p['id']}"):
                            db.avaliar_contribuicao(p["id"], "aprovado", st.session_state.usuario_atual["nome"])
                            st.success("Contribuição aprovada!")
                            st.rerun()
                    with c_eval[1]:
                        if st.button("❌ Rejeitar", key=f"btn_rejeit_cont_{p['id']}"):
                            db.avaliar_contribuicao(p["id"], "rejeitado", st.session_state.usuario_atual["nome"])
                            st.success("Contribuição rejeitada!")
                            st.rerun()
                            
        # Guest side - submit contribution
        else:
            st.markdown("#### Contribuir com lembranças")
            st.caption("Ajude a manter esse legado vivo enviando histórias, fotos ou vídeos. O responsável pelo memorial avaliará e aprovará antes de publicar.")
            
            with st.form("form_contribuir_memorial"):
                c_nome = st.text_input("Seu nome completo *", value=st.session_state.usuario_atual.get("nome", ""))
                c_email = st.text_input("Seu e-mail *", value=st.session_state.usuario_atual.get("email", ""))
                c_tipo = st.selectbox("Tipo de contribuição", ["historia", "foto", "video"])
                c_texto = st.text_area("Sua história ou descrição (opcional para foto/vídeo)")
                c_file = st.file_uploader("Arquivo (necessário para foto ou vídeo)", type=["png", "jpg", "jpeg", "webp", "mp4", "mov"])
                c_submit = st.form_submit_button("Enviar contribuição")
                
            if c_submit:
                if not c_nome.strip() or not c_email.strip():
                    st.error("Nome e e-mail são obrigatórios.")
                elif c_tipo != "historia" and not c_file:
                    st.error("O arquivo é obrigatório para contribuições de Foto ou Vídeo.")
                else:
                    try:
                        file_url = ""
                        file_name = ""
                        file_type = ""
                        if c_file:
                            bucket = "fotos" if c_tipo == "foto" else "videos"
                            upload = storage.upload_streamlit_file(bucket, c_file, memorial["usuario_id"], "contribuicoes")
                            file_url = upload["url"]
                            file_name = c_file.name
                            file_type = c_file.type
                            
                        db.criar_contribuicao_memorial(
                            usuario_dono_id=memorial["usuario_id"],
                            usuario_contribuidor_email=c_email.strip(),
                            usuario_contribuidor_nome=c_nome.strip(),
                            tipo_contribuicao=c_tipo,
                            texto=c_texto.strip(),
                            arquivo_url=file_url,
                            memorial_id=memorial_id,
                            arquivo_name=file_name,
                            arquivo_type=file_type
                        )
                        st.success("🎉 Sua contribuição foi enviada e está aguardando a aprovação do responsável pelo memorial. Muito obrigado!")
                    except Exception as e:
                        st.error(f"Erro ao enviar contribuição: {e}")

    # Back button at the very bottom
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
    if st.button("← Voltar para os Memoriais", key="memorial_ver_voltar"):
        st.session_state.pagina_atual = "memorial_lista"
        st.rerun()
