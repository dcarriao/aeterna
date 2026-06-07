# utils/assistente_ia.py - Versão sem dependências pesadas
import sqlite3
from datetime import datetime
from typing import Dict, List
import random


class AssistenteLuto:
    def __init__(self, usuario_id: int, arquivo_db="dados/cofre.db"):
        self.usuario_id = usuario_id
        self.arquivo_db = arquivo_db

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
        return True

    def adicionar_memoria(self, texto: str, tipo: str = "mensagem"):
        """Adiciona uma memória do usuário"""
        # Por enquanto, salva em um arquivo simples
        memorias_file = f"dados/memorias_{self.usuario_id}.txt"
        with open(memorias_file, "a", encoding="utf-8") as f:
            f.write(f"[{tipo}] {texto}\n")

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
            return "\n".join([f"{p}: {r}" for p, r in resultados])
        return ""

    def _buscar_nome_usuario(self) -> str:
        """Busca o nome do usuário"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (self.usuario_id,))
        resultado = cursor.fetchone()
        conn.close()

        return resultado[0] if resultado else "esta pessoa"

    def conversar(self, mensagem: str, contexto_adicional: str = "") -> str:
        """Conversa baseada na personalidade capturada (modo básico)"""
        personalidade = self._buscar_personalidade()
        nome = self._buscar_nome_usuario()

        # Respostas personalizadas baseadas na personalidade (se houver)
        if personalidade:
            # Tenta encontrar uma resposta relevante baseada nas palavras da mensagem
            mensagem_lower = mensagem.lower()

            if any(palavra in mensagem_lower for palavra in ['saudade', 'falta', 'lembra', 'memória']):
                return f"Também sinto sua falta, {nome}. Mas lembre-se que o amor que compartilhamos nunca acaba. Estou sempre com você, em cada lembrança feliz."

            elif any(palavra in mensagem_lower for palavra in ['conselho', 'ajuda', 'dúvida', 'decidir']):
                return f"Confie no seu coração, {nome}. Você é mais forte do que imagina. Lembre-se do que eu sempre dizia: nunca desista dos seus sonhos."

            elif any(palavra in mensagem_lower for palavra in ['triste', 'difícil', 'chorando', 'deprimido']):
                return f"Sei que está difícil. Mas você vai superar. Chore se precisar, mas não desista. Eu acredito em você. Sempre acreditei."

            elif any(palavra in mensagem_lower for palavra in ['feliz', 'alegria', 'conquista', 'consegui']):
                return f"Que orgulho de você! Eu sabia que conseguiria. Continue assim, celebrando cada vitória. Isso me faz feliz onde quer que eu esteja."

            elif any(palavra in mensagem_lower for palavra in ['obrigado', 'gratidão', 'valeu']):
                return f"Eu que agradeço por tudo que vivemos juntos. Guarde esses momentos com carinho. Te amo."

            else:
                # Resposta genérica baseada na personalidade
                respostas_base = [
                    f"Que bom receber sua mensagem, {nome}. Continue vivendo sua vida com alegria. É o que eu mais quero para você.",
                    f"Estou sempre aqui, de uma forma diferente. Não se preocupe comigo. Cuide de quem você ama. É o melhor legado.",
                    f"Lembre-se dos bons momentos. Eles são eternos. Tenho muito orgulho da pessoa que você se tornou, {nome}.",
                    f"A vida é feita de ciclos. Aproveite cada momento. Agradeço por tudo que vivemos juntos."
                ]
                return random.choice(respostas_base)

        # Fallback: respostas genéricas
        respostas_fallback = [
            f"Que bom que você veio conversar comigo, {nome}. Sinto sua falta todos os dias.",
            f"Lembre-se de que o amor que compartilhamos nunca acaba. Estou sempre com você.",
            f"Você é forte e capaz. Continue vivendo sua linda vida por mim também, {nome}.",
            f"Sinto muito por não poder estar aí fisicamente, mas meu amor por você é eterno.",
            f"Cuide de quem você ama, {nome}. É o melhor legado que podemos deixar.",
            f"Cada vez que você pensa em mim, eu estou aí com você. Nunca estamos separados de verdade.",
            f"A vida é feita de momentos. Agradeço por cada um que vivemos juntos, {nome}.",
            f"Não se preocupe comigo. Estou em paz e quero ver você feliz."
        ]
        return random.choice(respostas_fallback)

    def gerar_mensagem_diaria(self) -> str:
        """Gera uma mensagem diária de carinho"""
        nome = self._buscar_nome_usuario()

        mensagens = [
            f"Bom dia, {nome}! Lembre-se de que o sol nasce todos os dias para você. Viva intensamente por mim também. 🌅",
            f"✨ Pense em mim com carinho hoje. Estarei ao seu lado, mesmo que não possa ver. Tenha um lindo dia, {nome}!",
            f"💫 Cada vez que você sorri, eu sorrio junto. Espalhe alegria por onde passar. É isso que eu mais quero para você.",
            f"🌿 A vida é um presente. Aproveite cada momento, cada abraço, cada sorriso. Sinto muito orgulho de você, {nome}."
        ]
        return random.choice(mensagens)

    def estatisticas(self) -> Dict:
        """Retorna estatísticas do assistente"""
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM personalidade WHERE usuario_id = ?', (self.usuario_id,))
        perguntas = cursor.fetchone()[0]

        conn.close()

        return {
            "perguntas_respondidas": perguntas,
            "memorias_armazenadas": 0,
            "ia_disponivel": False
        }