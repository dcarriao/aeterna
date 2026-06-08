# utils/assistente_ia.py - Versão simplificada sem dependências pesadas
import sqlite3
from datetime import datetime
from typing import Dict, List
import random


class AssistenteLuto:
    def __init__(self, usuario_id: int, arquivo_db="dados/cofre.db"):
        self.usuario_id = usuario_id
        self.arquivo_db = arquivo_db

    def capturar_personalidade(self, respostas: Dict) -> bool:
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
            cursor.execute('INSERT INTO personalidade (usuario_id, pergunta, resposta) VALUES (?, ?, ?)',
                           (self.usuario_id, pergunta, resposta))
        conn.commit()
        conn.close()
        return True

    def adicionar_memoria(self, texto: str, tipo: str = "mensagem"):
        memorias_file = f"dados/memorias_{self.usuario_id}.txt"
        with open(memorias_file, "a", encoding="utf-8") as f:
            f.write(f"[{tipo}] {texto}\n")

    def _buscar_personalidade(self) -> str:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT pergunta, resposta FROM personalidade WHERE usuario_id = ? ORDER BY id',
                       (self.usuario_id,))
        resultados = cursor.fetchall()
        conn.close()
        if resultados:
            return "\n".join([f"{p}: {r}" for p, r in resultados])
        return ""

    def _buscar_preferencias(self) -> str:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT gostos_musica, gostos_comida, melhor_lembranca, dia_mais_feliz, dia_mais_triste
            FROM preferencias_usuario WHERE usuario_id = ?
        ''', (self.usuario_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            preferencias = []
            if row[0]: preferencias.append(f"Música favorita: {row[0]}")
            if row[1]: preferencias.append(f"Comida favorita: {row[1]}")
            if row[2]: preferencias.append(f"Melhor lembrança: {row[2]}")
            if row[3]: preferencias.append(f"Dia mais feliz: {row[3]}")
            if row[4]: preferencias.append(f"Dia mais triste: {row[4]}")
            return "\n".join(preferencias)
        return ""

    def _buscar_nome_usuario(self) -> str:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT nome, sobrenome FROM usuarios WHERE id = ?', (self.usuario_id,))
        resultado = cursor.fetchone()
        conn.close()
        return f"{resultado[0]} {resultado[1]}" if resultado else "esta pessoa"

    def conversar(self, mensagem: str, contexto_adicional: str = "") -> str:
        personalidade = self._buscar_personalidade()
        preferencias = self._buscar_preferencias()
        nome = self._buscar_nome_usuario()
        mensagem_lower = mensagem.lower()

        if personalidade or preferencias:
            contexto = personalidade
            if preferencias:
                contexto += f"\n\nPREFERÊNCIAS PESSOAIS:\n{preferencias}"

            if any(p in mensagem_lower for p in ['saudade', 'falta', 'lembra', 'memória']):
                return f"Também sinto sua falta. Lembre-se que o amor que compartilhamos nunca acaba. Estou sempre com você."
            elif any(p in mensagem_lower for p in ['música', 'canção', 'cantar']):
                return f"Ah, eu adorava música! {preferencias.split('Música favorita: ')[1].split('\n')[0] if 'Música favorita:' in preferencias else 'Eu gostava muito de ouvir minhas músicas favoritas com você.'} Era especial, né?"
            elif any(p in mensagem_lower for p in ['comida', 'comer', 'restaurante']):
                return f"Que saudade de comer {preferencias.split('Comida favorita: ')[1].split('\n')[0] if 'Comida favorita:' in preferencias else 'minha comida favorita'} com você! Era sempre uma alegria."
            elif any(p in mensagem_lower for p in ['conselho', 'ajuda', 'dúvida', 'decidir']):
                return f"Confie no seu coração. Você é mais forte do que imagina. Nunca desista dos seus sonhos."
            elif any(p in mensagem_lower for p in ['triste', 'difícil', 'chorando', 'deprimido']):
                if 'Dia mais triste:' in preferencias:
                    return f"Eu sei como é difícil. Lembra quando {preferencias.split('Dia mais triste: ')[1].split('\n')[0]}? Superamos juntos. Você também vai superar."
                return f"Sei que está difícil. Mas você vai superar. Chore se precisar, mas não desista. Eu acredito em você."
            elif any(p in mensagem_lower for p in ['feliz', 'alegria', 'conquista', 'consegui']):
                if 'Dia mais feliz:' in preferencias:
                    return f"Que orgulho! Lembra do dia mais feliz da minha vida? {preferencias.split('Dia mais feliz: ')[1].split('\n')[0]} Ver você feliz me faz lembrar disso."
                return f"Que orgulho de você! Eu sabia que conseguiria. Continue assim, celebrando cada vitória."
            else:
                respostas_base = [
                    f"Que bom receber sua mensagem. Continue vivendo sua vida com alegria. É o que eu mais quero para você.",
                    f"Estou sempre aqui, de uma forma diferente. Cuide de quem você ama. É o melhor legado.",
                    f"Lembre-se dos bons momentos. Eles são eternos. Tenho muito orgulho de você.",
                    f"A vida é feita de ciclos. Aproveite cada momento. Agradeço por tudo que vivemos juntos."
                ]
                return random.choice(respostas_base)

        respostas_fallback = [
            f"Que bom que você veio conversar comigo. Sinto sua falta todos os dias.",
            f"Lembre-se de que o amor que compartilhamos nunca acaba. Estou sempre com você.",
            f"Você é forte e capaz. Continue vivendo sua linda vida por mim também.",
            f"Sinto muito por não poder estar aí fisicamente, mas meu amor por você é eterno.",
            f"Cuide de quem você ama. É o melhor legado que podemos deixar.",
            f"Cada vez que você pensa em mim, eu estou aí com você. Nunca estamos separados de verdade.",
            f"A vida é feita de momentos. Agradeço por cada um que vivemos juntos.",
            f"Não se preocupe comigo. Estou em paz e quero ver você feliz."
        ]
        return random.choice(respostas_fallback)

    def gerar_mensagem_diaria(self) -> str:
        nome = self._buscar_nome_usuario()
        preferencias = self._buscar_preferencias()

        if preferencias:
            mensagens = [
                f"Bom dia! Lembre-se de viver intensamente. Aproveite cada momento como eu sempre fiz. 🌅",
                f"✨ Lembre-se de {preferencias.split('Melhor lembrança: ')[1].split('\n')[0] if 'Melhor lembrança:' in preferencias else 'dos bons momentos'} com carinho. Estou sempre com você.",
                f"💫 Cada vez que você sorri, eu sorrio junto. Espalhe alegria por onde passar. É o que eu mais quero para você.",
                f"🌿 A vida é um presente. Aproveite cada momento, cada abraço, cada sorriso. Tenho muito orgulho de você."
            ]
        else:
            mensagens = [
                f"Bom dia! Lembre-se de que o sol nasce todos os dias para você. Viva intensamente por mim também. 🌅",
                f"✨ Pense em mim com carinho hoje. Estarei ao seu lado, mesmo que não possa ver. Tenha um lindo dia!",
                f"💫 Cada vez que você sorri, eu sorrio junto. Espalhe alegria por onde passar.",
                f"🌿 A vida é um presente. Aproveite cada momento, cada abraço, cada sorriso. Sinto muito orgulho de você."
            ]
        return random.choice(mensagens)

    def estatisticas(self) -> Dict:
        conn = sqlite3.connect(self.arquivo_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM personalidade WHERE usuario_id = ?', (self.usuario_id,))
        perguntas = cursor.fetchone()[0]
        conn.close()
        return {"perguntas_respondidas": perguntas, "memorias_armazenadas": 0, "ia_disponivel": False}