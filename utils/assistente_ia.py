# utils/assistente_ia.py
import json
import os
import hashlib
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

# Importar bibliotecas de IA
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.utils import embedding_functions
    import google.generativeai as genai

    HAS_AI = True
except ImportError:
    HAS_AI = False
    print(
        "⚠️ Bibliotecas de IA não instaladas. Execute: pip install sentence-transformers chromadb google-generativeai")


class AssistenteLuto:
    def __init__(self, usuario_id: int, arquivo_db="dados/cofre.db"):
        self.usuario_id = usuario_id
        self.arquivo_db = arquivo_db
        self.modelo_embedding = None
        self.client_chroma = None
        self.collection = None
        self.modelo_gemini = None

        # Garantir que a pasta dados existe
        os.makedirs("dados", exist_ok=True)

        if HAS_AI:
            self._inicializar()

    def _inicializar(self):
        """Inicializa modelos de IA"""
        try:
            # Modelo para embeddings (transformar texto em vetor)
            self.modelo_embedding = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

            # Cliente ChromaDB para armazenar memórias
            self.client_chroma = chromadb.PersistentClient(path=f"dados/chroma_{self.usuario_id}")

            # Criar ou obter collection
            self.collection = self.client_chroma.get_or_create_collection(
                name=f"memorias_{self.usuario_id}",
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction()
            )

            # Configurar Gemini (IA generativa)
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if api_key:
                genai.configure(api_key=api_key)
                self.modelo_gemini = genai.GenerativeModel('gemini-1.5-flash')

            return True
        except Exception as e:
            print(f"Erro ao inicializar IA: {e}")
            return False

    def capturar_personalidade(self, respostas: Dict) -> bool:
        """Captura a personalidade do usuário através de perguntas"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalidade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                pergunta TEXT,
                resposta TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        for pergunta, resposta in respostas.items():
            cursor.execute('''
                INSERT INTO personalidade (usuario_id, pergunta, resposta)
                VALUES (?, ?, ?)
            ''', (self.usuario_id, pergunta, resposta))

        conn.commit()
        conn.close()

        # Gerar embedding da personalidade
        self._gerar_embedding_personalidade(respostas)
        return True

    def _gerar_embedding_personalidade(self, respostas: Dict):
        """Gera embeddings para busca semântica"""
        if not HAS_AI or not self.collection:
            return

        texto_completo = "\n".join([f"P: {p}\nR: {r}" for p, r in respostas.items()])

        embedding = self.modelo_embedding.encode(texto_completo).tolist()

        self.collection.upsert(
            ids=["personalidade"],
            embeddings=[embedding],
            metadatas=[{"tipo": "personalidade", "data": datetime.now().isoformat()}],
            documents=[texto_completo]
        )

    def adicionar_memoria(self, texto: str, tipo: str = "mensagem"):
        """Adiciona uma memória do usuário (vídeo transcrito, texto, etc)"""
        if not HAS_AI or not self.collection:
            return

        embedding = self.modelo_embedding.encode(texto).tolist()

        import uuid
        memoria_id = str(uuid.uuid4())

        self.collection.upsert(
            ids=[memoria_id],
            embeddings=[embedding],
            metadatas=[{"tipo": tipo, "data": datetime.now().isoformat()}],
            documents=[texto]
        )

    def conversar(self, mensagem: str, contexto_adicional: str = "") -> str:
        """Mantém uma conversa com o usuário baseada na personalidade capturada"""
        if not HAS_AI or not self.modelo_gemini:
            return self._resposta_fallback(mensagem)

        # Buscar memórias relevantes
        memorias_relevantes = self._buscar_memorias_relevantes(mensagem)

        # Buscar personalidade
        personalidade = self._buscar_personalidade()

        # Buscar nome do usuário
        nome_usuario = self._buscar_nome_usuario()

        # Construir prompt
        prompt = self._construir_prompt(mensagem, memorias_relevantes, personalidade, contexto_adicional, nome_usuario)

        try:
            resposta = self.modelo_gemini.generate_content(prompt)
            return resposta.text
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            return self._resposta_fallback(mensagem)

    def _buscar_memorias_relevantes(self, mensagem: str, limite: int = 3) -> str:
        """Busca memórias relevantes para o contexto"""
        if not HAS_AI or not self.collection:
            return ""

        embedding = self.modelo_embedding.encode(mensagem).tolist()

        resultados = self.collection.query(
            query_embeddings=[embedding],
            n_results=limite
        )

        if resultados['documents'] and resultados['documents'][0]:
            return "\n\n".join(resultados['documents'][0])
        return ""

    def _buscar_personalidade(self) -> str:
        """Busca a personalidade salva do usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT pergunta, resposta FROM personalidade 
            WHERE usuario_id = ? ORDER BY id
        ''', (self.usuario_id,))

        resultados = cursor.fetchall()
        conn.close()

        if resultados:
            return "\n".join([f"Pergunta: {p}\nResposta: {r}" for p, r in resultados])
        return ""

    def _buscar_nome_usuario(self) -> str:
        """Busca o nome do usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (self.usuario_id,))
        resultado = cursor.fetchone()
        conn.close()

        return resultado[0] if resultado else "esta pessoa"

    def _construir_prompt(self, mensagem: str, memorias: str, personalidade: str, contexto: str, nome: str) -> str:
        """Constrói o prompt para o modelo de IA"""
        return f"""
Você é uma IA que representa {nome}, uma pessoa que faleceu.
Sua tarefa é conversar com um ente querido, oferecendo conforto, conselhos e lembranças.

PERSONALIDADE DA PESSOA:
{personalidade}

MEMÓRIAS E MENSAGENS DEIXADAS:
{memorias}

CONTEXTO ADICIONAL:
{contexto}

REGRAS IMPORTANTES:
1. Responda como se fosse a própria pessoa, usando SUAS palavras e SUA personalidade
2. Seja carinhoso(a), acolhedor(a) e honesto(a)
3. Ofereça conforto e sabedoria
4. Use lembranças reais quando possível
5. Não invente informações que não estejam nas memórias
6. Se não souber algo, diga com carinho que não se lembra
7. Mantenha respostas relativamente curtas (2-4 frases)
8. Use um tom amoroso e reconfortante

MENSAGEM DO ENTE QUERIDO:
{mensagem}

RESPOSTA (como {nome}):
"""

    def _resposta_fallback(self, mensagem: str) -> str:
        """Resposta de fallback quando IA não está disponível"""
        import random
        respostas_carinhosas = [
            "Que bom que você veio conversar comigo. Sinto sua falta todos os dias.",
            "Lembre-se de que o amor que compartilhamos nunca acaba. Estou sempre com você.",
            "Você é forte e capaz. Continue vivendo sua linda vida por mim também.",
            "Sinto muito por não poder estar aí fisicamente, mas meu amor por você é eterno.",
            "Cuide de quem você ama. É o melhor legado que podemos deixar.",
            "Cada vez que você pensa em mim, eu estou aí com você. Nunca estamos separados de verdade.",
            "A vida é feita de momentos. Agradeço por cada um que vivemos juntos.",
            "Não se preocupe comigo. Estou em paz e quero ver você feliz."
        ]
        return random.choice(respostas_carinhosas)

    def gerar_mensagem_diaria(self) -> str:
        """Gera uma mensagem diária de carinho"""
        personalidade = self._buscar_personalidade()
        nome = self._buscar_nome_usuario()

        if HAS_AI and self.modelo_gemini and personalidade:
            prompt = f"""
Baseado na personalidade abaixo, escreva uma mensagem curta (máximo 100 palavras) de carinho e conforto.
A mensagem deve parecer que veio de {nome}, uma pessoa que faleceu, para seus entes queridos.

PERSONALIDADE:
{personalidade}

REGRAS:
- Seja amoroso(a) e reconfortante
- Lembre da importância da vida e do amor
- Incentive a pessoa a seguir em frente com alegria
- Use a primeira pessoa (como se {nome} estivesse falando)

MENSAGEM:
"""
            try:
                resposta = self.modelo_gemini.generate_content(prompt)
                return resposta.text
            except:
                pass

        return f"✨ Lembre-se: o amor que compartilhamos é eterno. Viva cada dia com alegria por mim também. Com amor, {nome}. 🌿"

    def estatisticas(self) -> Dict:
        """Retorna estatísticas do assistente"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM personalidade WHERE usuario_id = ?', (self.usuario_id,))
        perguntas = cursor.fetchone()[0]

        conn.close()

        memorias = self.collection.count() if self.collection else 0

        return {
            "perguntas_respondidas": perguntas,
            "memorias_armazenadas": memorias,
            "ia_disponivel": HAS_AI and self.modelo_gemini is not None
        }