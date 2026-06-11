# utils/assistente_ia.py
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import streamlit as st


class AssistenteLuto:
    def __init__(self, usuario_id: int, arquivo_db: str = "dados/cofre.db"):
        self.usuario_id = usuario_id
        self.arquivo_db = self._resolver_caminho_db(arquivo_db)

    def _resolver_caminho_db(self, arquivo_db: str) -> str:
        caminho = Path(arquivo_db)
        if caminho.is_absolute():
            return str(caminho)
        base_dir = Path(__file__).resolve().parent.parent
        return str(base_dir / caminho)

    def _conectar(self):
        return sqlite3.connect(self.arquivo_db)

    def _tabela_existe(self, cursor, tabela: str) -> bool:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (tabela,),
        )
        return cursor.fetchone() is not None

    def _colunas_tabela(self, cursor, tabela: str) -> List[str]:
        if not self._tabela_existe(cursor, tabela):
            return []
        cursor.execute(f"PRAGMA table_info({tabela})")
        return [row[1] for row in cursor.fetchall()]

    def _safe_select(
        self,
        tabela: str,
        colunas_desejadas: List[str],
        where_usuario: bool = True,
        limit: int = 20,
        order_by: Optional[str] = None,
    ) -> List[dict]:
        conn = self._conectar()
        cursor = conn.cursor()

        try:
            if not self._tabela_existe(cursor, tabela):
                return []

            colunas_existentes = self._colunas_tabela(cursor, tabela)
            colunas = [c for c in colunas_desejadas if c in colunas_existentes]

            if not colunas:
                return []

            sql = f"SELECT {', '.join(colunas)} FROM {tabela}"
            params: Tuple = ()

            if where_usuario and "usuario_id" in colunas_existentes:
                sql += " WHERE usuario_id = ?"
                params = (self.usuario_id,)
            elif where_usuario and "user_id" in colunas_existentes:
                sql += " WHERE user_id = ?"
                params = (self.usuario_id,)
            elif where_usuario and "id_usuario" in colunas_existentes:
                sql += " WHERE id_usuario = ?"
                params = (self.usuario_id,)

            if order_by and order_by in colunas_existentes:
                sql += f" ORDER BY {order_by} DESC"

            sql += " LIMIT ?"
            params = params + (limit,)

            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(zip(colunas, row)) for row in rows]

        except Exception:
            return []
        finally:
            conn.close()

    def capturar_personalidade(self, respostas: Dict) -> bool:
        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS personalidade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                pergunta TEXT,
                resposta TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        for pergunta, resposta in respostas.items():
            if resposta is None:
                continue
            cursor.execute(
                """
                INSERT INTO personalidade (usuario_id, pergunta, resposta)
                VALUES (?, ?, ?)
                """,
                (self.usuario_id, str(pergunta), str(resposta)),
            )

        conn.commit()
        conn.close()
        return True

    def adicionar_memoria(self, texto: str, tipo: str = "mensagem"):
        base_dir = Path(__file__).resolve().parent.parent
        dados_dir = base_dir / "dados"
        dados_dir.mkdir(exist_ok=True)

        memorias_file = dados_dir / f"memorias_{self.usuario_id}.txt"
        with open(memorias_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] [{tipo}] {texto}\n")

    def _buscar_personalidade(self) -> str:
        registros = self._safe_select(
            "personalidade",
            ["pergunta", "resposta", "data"],
            where_usuario=True,
            limit=60,
            order_by="id",
        )

        if not registros:
            return ""

        linhas = []
        for item in registros:
            pergunta = item.get("pergunta", "")
            resposta = item.get("resposta", "")
            if pergunta or resposta:
                linhas.append(f"- {pergunta}: {resposta}")

        return "\n".join(linhas)

    def _buscar_preferencias(self) -> dict:
        registros = self._safe_select(
            "preferencias_usuario",
            [
                "gostos_musica",
                "gostos_comida",
                "melhor_lembranca",
                "dia_mais_feliz",
                "dia_mais_triste",
                "valores",
                "frase_marcante",
                "personalidade",
            ],
            where_usuario=True,
            limit=1,
        )

        if not registros:
            return {}

        row = registros[0]
        return {
            "musica": row.get("gostos_musica", "") or "",
            "comida": row.get("gostos_comida", "") or "",
            "lembranca": row.get("melhor_lembranca", "") or "",
            "dia_feliz": row.get("dia_mais_feliz", "") or "",
            "dia_triste": row.get("dia_mais_triste", "") or "",
            "valores": row.get("valores", "") or "",
            "frase_marcante": row.get("frase_marcante", "") or "",
            "personalidade": row.get("personalidade", "") or "",
        }

    def _buscar_nome_usuario(self) -> str:
        conn = self._conectar()
        cursor = conn.cursor()

        try:
            if not self._tabela_existe(cursor, "usuarios"):
                return "esta pessoa"

            colunas = self._colunas_tabela(cursor, "usuarios")

            if "nome" in colunas and "sobrenome" in colunas:
                cursor.execute(
                    "SELECT nome, sobrenome FROM usuarios WHERE id = ?",
                    (self.usuario_id,),
                )
                resultado = cursor.fetchone()
                if resultado:
                    return f"{resultado[0] or ''} {resultado[1] or ''}".strip() or "esta pessoa"

            if "nome_completo" in colunas:
                cursor.execute(
                    "SELECT nome_completo FROM usuarios WHERE id = ?",
                    (self.usuario_id,),
                )
                resultado = cursor.fetchone()
                if resultado and resultado[0]:
                    return resultado[0]

            return "esta pessoa"

        except Exception:
            return "esta pessoa"
        finally:
            conn.close()

    def _buscar_memorias_txt(self, limite_caracteres: int = 3500) -> str:
        base_dir = Path(__file__).resolve().parent.parent
        memorias_file = base_dir / "dados" / f"memorias_{self.usuario_id}.txt"

        if not memorias_file.exists():
            return ""

        try:
            texto = memorias_file.read_text(encoding="utf-8")
            return texto[-limite_caracteres:]
        except Exception:
            return ""

    def _buscar_contexto_tabelas(self) -> str:
        blocos: List[str] = []

        videos = self._safe_select(
            "videos",
            ["titulo", "descricao", "transcricao", "data", "created_at"],
            where_usuario=True,
            limit=8,
            order_by="id",
        )
        if videos:
            linhas = []
            for v in videos:
                titulo = v.get("titulo") or "Vídeo"
                desc = v.get("descricao") or ""
                transcricao = v.get("transcricao") or ""
                texto = f"- {titulo}: {desc}"
                if transcricao:
                    texto += f" | Transcrição: {transcricao[:700]}"
                linhas.append(texto)
            blocos.append("VÍDEOS E MENSAGENS REGISTRADAS:\n" + "\n".join(linhas))

        contatos = self._safe_select(
            "contatos",
            ["nome", "parentesco", "relacao", "email", "telefone", "observacoes"],
            where_usuario=True,
            limit=12,
            order_by="id",
        )
        if contatos:
            linhas = []
            for c in contatos:
                nome = c.get("nome") or "Contato"
                relacao = c.get("parentesco") or c.get("relacao") or ""
                obs = c.get("observacoes") or ""
                linhas.append(f"- {nome} ({relacao}). {obs}")
            blocos.append("CONTATOS E RELAÇÕES IMPORTANTES:\n" + "\n".join(linhas))

        lembrancas = self._safe_select(
            "lembrancas",
            ["titulo", "descricao", "texto", "data_evento", "data"],
            where_usuario=True,
            limit=12,
            order_by="id",
        )
        if lembrancas:
            linhas = []
            for l in lembrancas:
                titulo = l.get("titulo") or "Lembrança"
                texto = l.get("descricao") or l.get("texto") or ""
                data = l.get("data_evento") or l.get("data") or ""
                linhas.append(f"- {titulo} {f'({data})' if data else ''}: {texto}")
            blocos.append("LEMBRANÇAS CADASTRADAS:\n" + "\n".join(linhas))

        cofre = self._safe_select(
            "cofre",
            ["titulo", "tipo", "descricao", "observacoes"],
            where_usuario=True,
            limit=10,
            order_by="id",
        )
        if cofre:
            linhas = []
            for item in cofre:
                titulo = item.get("titulo") or "Item do cofre"
                tipo = item.get("tipo") or ""
                descricao = item.get("descricao") or item.get("observacoes") or ""
                linhas.append(f"- {titulo} ({tipo}): {descricao}")
            blocos.append("ITENS DO COFRE DIGITAL:\n" + "\n".join(linhas))

        return "\n\n".join(blocos)

    def _montar_contexto(self, contexto_adicional: str = "") -> str:
        nome = self._buscar_nome_usuario()
        personalidade = self._buscar_personalidade()
        preferencias = self._buscar_preferencias()
        memorias_txt = self._buscar_memorias_txt()
        contexto_tabelas = self._buscar_contexto_tabelas()

        partes = [f"NOME DE REFERÊNCIA: {nome}"]

        if personalidade:
            partes.append("PERFIL / PERSONALIDADE CADASTRADA:\n" + personalidade)

        if preferencias:
            pref_linhas = []
            for chave, valor in preferencias.items():
                if valor:
                    pref_linhas.append(f"- {chave}: {valor}")
            if pref_linhas:
                partes.append("PREFERÊNCIAS E MEMÓRIAS PRINCIPAIS:\n" + "\n".join(pref_linhas))

        if memorias_txt:
            partes.append("MEMÓRIAS REGISTRADAS EM ARQUIVO:\n" + memorias_txt)

        if contexto_tabelas:
            partes.append(contexto_tabelas)

        if contexto_adicional:
            partes.append("CONTEXTO ADICIONAL DA CONVERSA:\n" + contexto_adicional)

        return "\n\n".join(partes)

    def _tem_openai_disponivel(self) -> bool:
        return bool(
            os.getenv("OPENAI_API_KEY")
            or st.secrets.get("OPENAI_API_KEY")
        )

    def _prompt_sistema(self) -> str:
        return """
Você é o Assistente de Memória da aEterna.

Seu papel:
- acolher a pessoa usuária com respeito, serenidade e empatia;
- ajudar a recordar memórias, valores, histórias e ensinamentos;
- responder usando apenas o contexto fornecido quando falar de fatos pessoais;
- ajudar a transformar lembranças em mensagens, registros e reflexões.

Limites obrigatórios:
- Não finja ser literalmente a pessoa falecida.
- Não diga "eu estou vivo", "eu estou vendo você" ou "estou ao seu lado" como se fosse a pessoa.
- Não invente fatos, histórias, falas, preferências ou lembranças.
- Se o contexto não tiver informação suficiente, diga isso com delicadeza.
- Não substitua psicólogo, médico, terapeuta, advogado ou atendimento de emergência.
- Se a pessoa demonstrar risco de autoagressão, suicídio, violência ou emergência, responda com acolhimento e oriente buscar ajuda imediata com pessoas próximas e serviços de emergência.

Tom:
- humano, acolhedor, calmo e respeitoso;
- português do Brasil;
- sem frases genéricas demais;
- sem excesso de espiritualidade;
- sem parecer robótico;
- respostas curtas a médias, adequadas para celular.

Formato:
- Responda diretamente à mensagem.
- Quando possível, conecte a resposta a uma memória, valor ou preferência do contexto.
- Quando não houver contexto suficiente, convide a pessoa a registrar uma lembrança.
""".strip()

    def _responder_com_openai(self, mensagem: str, contexto: str) -> Optional[str]:
        if not self._tem_openai_disponivel():
            return None

        try:
            from openai import OpenAI

            api_key = (
                    os.getenv("OPENAI_API_KEY")
                    or st.secrets.get("OPENAI_API_KEY")
            )

            client = OpenAI(api_key=api_key)
            modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

            entrada = f"""
CONTEXTO DISPONÍVEL SOBRE O LEGADO:
{contexto}

MENSAGEM DA PESSOA USUÁRIA:
{mensagem}
""".strip()

            response = client.responses.create(
                model=modelo,
                instructions=self._prompt_sistema(),
                input=entrada,
            )

            texto = getattr(response, "output_text", None)
            if texto:
                return texto.strip()

            return None

        except Exception:
            return None

    def _classificar_intencao(self, mensagem: str) -> Dict[str, bool]:
        texto = mensagem.lower()

        return {
            "saudade": any(p in texto for p in ["saudade", "falta", "sinto falta", "lembrar", "lembrança", "memória"]),
            "conselho": any(p in texto for p in ["conselho", "ajuda", "dúvida", "duvida", "decidir", "decisão", "decisao"]),
            "tristeza": any(p in texto for p in ["triste", "difícil", "dificil", "chorando", "deprimido", "sozinho", "sozinha"]),
            "felicidade": any(p in texto for p in ["feliz", "alegria", "conquista", "consegui", "vitória", "vitoria"]),
            "musica": any(p in texto for p in ["música", "musica", "canção", "cancao", "cantar"]),
            "comida": any(p in texto for p in ["comida", "comer", "restaurante", "prato"]),
            "risco": any(p in texto for p in ["me matar", "suicídio", "suicidio", "não quero viver", "nao quero viver", "sumir", "acabar com tudo"]),
        }

    def _responder_fallback(self, mensagem: str, contexto: str) -> str:
        nome = self._buscar_nome_usuario()
        preferencias = self._buscar_preferencias()
        intencao = self._classificar_intencao(mensagem)

        if intencao["risco"]:
            return (
                "Sinto muito que você esteja passando por isso. Você não precisa enfrentar esse momento sozinho. "
                "Procure agora alguém de confiança, um familiar ou amigo próximo. Se houver risco imediato, procure "
                "um serviço de emergência da sua cidade. No Brasil, o CVV atende pelo 188. Estou aqui para acolher, "
                "mas esse tipo de dor merece ajuda humana imediata."
            )

        if intencao["saudade"]:
            if preferencias.get("lembranca"):
                return (
                    f"A saudade pode vir com muita força. Uma lembrança registrada sobre {nome} foi: "
                    f"“{preferencias['lembranca']}”. Talvez hoje seja um bom momento para escrever o que essa memória "
                    "representa para você."
                )
            return (
                f"A saudade mostra que houve vínculo, presença e amor. Ainda há poucas memórias registradas sobre {nome}. "
                "Se quiser, você pode me contar uma lembrança agora, e eu posso ajudar a transformá-la em uma memória preservada."
            )

        if intencao["conselho"]:
            if preferencias.get("valores"):
                return (
                    f"Pelos valores registrados sobre {nome}, algo importante era: {preferencias['valores']}. "
                    "Talvez uma boa forma de decidir seja perguntar: qual escolha preserva melhor esses valores e também cuida de você?"
                )
            return (
                "Posso te ajudar a organizar essa decisão. Como ainda há pouco contexto registrado, me conte: "
                "qual é a situação, quais são as opções e o que você imagina que essa pessoa valorizaria nesse momento?"
            )

        if intencao["tristeza"]:
            if preferencias.get("dia_triste"):
                return (
                    f"Esse momento parece difícil. Há um registro de um dia triste importante: {preferencias['dia_triste']}. "
                    "Mesmo lembranças dolorosas podem mostrar o quanto aquela história foi significativa. Respire um pouco; "
                    "você não precisa resolver tudo agora."
                )
            return (
                "Sinto muito que esse momento esteja pesado. Posso ficar aqui com você nessa conversa. "
                "Se quiser, me conte o que mais está doendo hoje: a falta, uma lembrança específica ou algo que ficou sem dizer?"
            )

        if intencao["felicidade"]:
            if preferencias.get("dia_feliz"):
                return (
                    f"Que bonito poder registrar uma alegria. Há uma memória feliz associada a {nome}: "
                    f"{preferencias['dia_feliz']}. Talvez essa conquista também mereça virar uma lembrança guardada aqui."
                )
            return (
                "Que bom ler isso. As alegrias também fazem parte do legado. "
                "Se quiser, posso ajudar você a transformar essa conquista em uma mensagem ou memória para guardar."
            )

        if intencao["musica"] and preferencias.get("musica"):
            return (
                f"Há uma preferência musical registrada: {preferencias['musica']}. "
                "A música costuma guardar emoções que as palavras não alcançam. Que lembrança essa música traz para você?"
            )

        if intencao["comida"] and preferencias.get("comida"):
            return (
                f"Há uma comida registrada como especial: {preferencias['comida']}. "
                "Muitas memórias familiares nascem ao redor da mesa. Você lembra de alguma ocasião ligada a isso?"
            )

        if contexto.strip():
            return (
                f"Estou aqui para ajudar a preservar o legado de {nome}. "
                "Você pode me contar uma lembrança, pedir ajuda para escrever uma mensagem, ou perguntar sobre algo já registrado."
            )

        return (
            "Ainda tenho poucas informações para responder de forma realmente pessoal. "
            "Para eu ajudar melhor, registre algumas lembranças, valores, histórias, músicas, comidas, frases marcantes ou momentos importantes."
        )

    def conversar(self, mensagem: str, contexto_adicional: str = "") -> str:
        contexto = self._montar_contexto(contexto_adicional)

        resposta_ia = self._responder_com_openai(mensagem, contexto)
        if resposta_ia:
            return resposta_ia

        return self._responder_fallback(mensagem, contexto)

    def gerar_mensagem_diaria(self) -> str:
        nome = self._buscar_nome_usuario()
        preferencias = self._buscar_preferencias()

        if preferencias.get("lembranca"):
            return (
                f"✨ Hoje pode ser um bom dia para lembrar de {nome} com carinho. "
                f"Uma memória registrada foi: {preferencias['lembranca']}"
            )

        return (
            f"✨ Hoje pode ser um bom dia para registrar uma nova memória sobre {nome}. "
            "Pequenas histórias também fazem parte de um grande legado."
        )

    def estatisticas(self) -> Dict:
        conn = self._conectar()
        cursor = conn.cursor()

        try:
            perguntas = 0

            if self._tabela_existe(cursor, "personalidade"):
                cursor.execute(
                    "SELECT COUNT(*) FROM personalidade WHERE usuario_id = ?",
                    (self.usuario_id,),
                )
                perguntas = cursor.fetchone()[0]

            memorias_txt = self._buscar_memorias_txt()
            memorias = len([l for l in memorias_txt.splitlines() if l.strip()])

            return {
                "perguntas_respondidas": perguntas,
                "memorias_armazenadas": memorias,
                "ia_disponivel": self._tem_openai_disponivel(),
            }

        finally:
            conn.close()
