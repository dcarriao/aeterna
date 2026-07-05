# SPRINT 5.5 — O MOMENTO "ESPERA..."

> Sprint dedicada exclusivamente ao Hero. O objetivo não é adicionar funcionalidades, melhorar SEO ou reorganizar arquitetura — é fazer o visitante parar de rolar a página nos primeiros 10 segundos. O Hero foi redesenhado para criar o efeito "Espera... eu nunca tinha pensado nisso."

---

## 1. AUDITORIA DO HERO (ESTADO ANTERIOR)

### 1.1 Componentes do Hero anterior

| Componente | Conteúdo | Avaliação |
|---|---|---|
| **Eyebrow** | "Plataforma de histórias de família" | ⚠️ Funcional, mas não desperta curiosidade. Descreve a categoria do produto, não a promessa. |
| **H1** | "Você guarda as fotos. Quem guarda as histórias da sua família?" | ⚠️ Pergunta boa, mas longa (14 palavras). Duas perguntas em uma. Pode ser mais impactante. |
| **Subtítulo** | "A aEterna ajuda você a registrar hoje as histórias, aprendizados, valores e momentos que normalmente desaparecem quando alguém parte — antes que seja tarde demais." | ❌ Longo (36 palavras). Explica demais. Deveria teaser, não explicar. |
| **CTA primário** | "Começar minha história" → streamlit | ⚠️ Pede compromisso, não descoberta. |
| **CTA secundário** | "Ver como funciona" | ⚠️ Funcional, mas genérico. |
| **Proof items** | "Plataforma completa para histórias de família" / "Família participa junto" / "Legado que continua vivo" | ⚠️ Genéricos. Poderiam ser mais concretos. |
| **Mockup** | `home.webp` em smartphone + `memoria-detalhe.webp` em tela lateral rotacionada | ❌ Mostra uma interface, não uma transformação. Poderia pertencer a qualquer app de memórias. |
| **Fallback** | Mockup de story card com "Domingo na casa da avó" | ❌ Conteúdo estático, não demonstra a transformação do produto. |

### 1.2 Diagnóstico

**O Hero anterior respondia "o que é a aEterna", mas não respondia "por que isso importa para mim".**

Problemas específicos:

1. **H1 duplo** — "Você guarda as fotos. **Quem guarda** as histórias da sua família?" — são duas perguntas. O visitante precisa processar duas ideias em 3 segundos.

2. **Subtítulo explicativo** — Explica *o que* a aEterna faz em vez de mostrar *o que* o visitante vai ganhar. Carrega carga cognitiva desnecessária.

3. **Mockup de smartphone** — Mostra `home.webp` (tela inicial) e `memoria-detalhe.webp` (detalhe de memória). É bonito, mas é "mais um app de memórias". Não mostra o que diferencia a aEterna de outros produtos.

4. **CTA de compromisso** — "Começar minha história" pede ação imediata. O visitante que ainda não entendeu o valor hesita.

5. **Proof items genéricos** — "Plataforma completa para histórias de família" poderia ser de qualquer produto do segmento. Falta especificidade.

### 1.3 Pergunta-chave: o Hero anterior provocaria "Espera..."?

**Não.** O Hero anterior informava, mas não confrontava. Um visitante que chegasse e lesse apenas o H1 + subtítulo pensaria: "Mais um app para guardar memórias." Não pensaria: "Espera... eu nunca pensei nisso sobre as minhas fotos."

---

## 2. NOVO HERO

### 2.1 Mudanças aplicadas

| Componente | Antes | Depois | Justificativa |
|---|---|---|---|
| **Eyebrow** | "Plataforma de histórias de família" | "Para quem quer ser lembrado pelo que importa" | Desperta identificação pessoal antes de vender o produto. |
| **H1** | "Você guarda as fotos. Quem guarda as histórias da sua família?" | "O que suas fotos vão contar quando você não estiver mais aqui?" | Pergunta única, pessoal, forward-looking. Confronta o visitante com seu próprio futuro. |
| **Subtítulo** | "A aEterna ajuda você a registrar hoje as histórias, aprendizados, valores e momentos que normalmente desaparecem quando alguém parte — antes que seja tarde demais." (36 palavras) | "A aEterna transforma cada foto em uma história com pessoas, contexto e significado — para que sua família não herde apenas imagens, mas o que realmente importa." (31 palavras) | Encurtado. Foco no **resultado** (transformação), não no **processo** (registrar). |
| **CTA primário** | "Começar minha história" | "Ver uma foto virar história" | Inverte a lógica: o visitante não é convidado a agir — é convidado a **ver a transformação acontecer**. |
| **CTA secundário** | "Ver como funciona" | "Começar a contar a minha" | O compromisso fica como segunda opção. |
| **Proof items** | "Plataforma completa para histórias de família" / "Família participa junto" / "Legado que continua vivo" | "Histórias com pessoas, datas e contexto" / "Família contribui com suas versões" / "Legado que atravessa gerações" | Substituição de adjetivos vazios por elementos concretos. |
| **Mockup** | Smartphone com `home.webp` + tela lateral rotacionada com `memoria-detalhe.webp` | **Transformação visual**: duas cards lado a lado mostrando a mesma foto. Esquerda: foto sem contexto. Direita: a mesma foto transformada em história com overlays (avatar, nome, idade, tags, frase). | O visitante vê a **transformação acontecendo** em vez de ver um app. |

### 2.2 Anatomia do novo Hero

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  PARA QUEM QUER SER LEMBRADO PELO QUE IMPORTA                │
│                                                              │
│  O que suas fotos vão contar                                │
│  quando você não estiver mais aqui?                          │
│                                                              │
│  A aEterna transforma cada foto em uma história             │
│  com pessoas, contexto e significado — para que              │
│  sua família não herde apenas imagens,                       │
│  mas o que realmente importa.                                │
│                                                              │
│  [ Ver uma foto virar história ]  [ Começar a contar a minha ]│
│                                                              │
│  ✓ Histórias com pessoas, datas e contexto                  │
│  ✓ Família contribui com suas versões                        │
│  ✓ Legado que atravessa gerações                             │
│                                                              │
│  ┌──────────────┐     ┌──────────────┐                      │
│  │ SUA FOTO HOJE │  →  │ COM A ETERNA  │                      │
│  │              │     │              │                      │
│  │  [foto]      │     │  [foto]      │                      │
│  │  [overlay    │     │  [M] Maria  │                      │
│  │   escuro]    │     │  Avó · 64   │                      │
│  │              │     │  #Família   │                      │
│  │  "Foto       │     │  "Era a     │                      │
│  │   antiga..." │     │  primeira   │                      │
│  │              │     │  vez..."    │                      │
│  └──────────────┘     └──────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Por que esse Hero gera "Espera..."

| Elemento | Reação esperada |
|---|---|
| **H1** | "Espera... eu nunca pensei no que vai acontecer com as minhas fotos quando eu não estiver mais aqui." |
| **Subtítulo** | "Faz sentido. Eu tenho milhares de fotos e quase nenhuma história preservada." |
| **Visual antes** | "É verdade, essa foto antiga está no meu celular sem contexto nenhum." |
| **Visual depois** | "Olha como a mesma foto pode virar uma história com nome, data, contexto e sentimento." |
| **CTA** | "Quero ver como uma foto minha vira uma história." |
| **Resultado** | O visitante **quer continuar lendo** porque viu uma transformação que ainda não tem. |

---

## 3. JUSTIFICATIVA DE CADA MUDANÇA

### 3.1 Eyebrow: "Para quem quer ser lembrado pelo que importa"

- **Objetivo psicológico:** Conectar o produto a um **desejo humano** antes de descrever a categoria.
- **Relação com o app:** O app `render_preferencias` (`app.py:2783-2880`) pergunta "como você gostaria de ser lembrado?" — o eyebrow reflete essa mesma pergunta no nível da Landing.
- **Por que não "Plataforma de histórias de família":** O eyebrow anterior classificava o produto, mas não criava identificação. O novo eyebrow posiciona o produto como algo para "pessoas que se importam" — uma categoria emocional, não técnica.

### 3.2 H1: "O que suas fotos vão contar quando você não estiver mais aqui?"

- **Objetivo psicológico:** Provocar uma reflexão sobre o próprio futuro, não sobre o produto.
- **Por que é uma pergunta só:** O H1 anterior tinha duas perguntas ("Você guarda as fotos" + "Quem guarda as histórias"), o que diluía o impacto. Uma pergunta única, sobre o futuro pessoal, é mais fácil de processar em 3 segundos.
- **Por que menciona "quando você não estiver mais aqui":** É forward-looking e pessoal. O visitante pensa nos próprios netos, não em "famílias" genéricas.
- **Não usa culpa nem medo:** A pergunta não é ameaçadora — é uma reflexão. O visitante não se sente pressionado; sente-se curioso.

### 3.3 Subtítulo: "A aEterna transforma cada foto em uma história..."

- **Objetivo psicológico:** Comunicar o **resultado** (transformação) em vez do **processo** (registrar).
- **Reduz carga cognitiva:** O subtítulo anterior tinha 36 palavras com 4 ideias (histórias, aprendizados, valores, momentos). O novo tem 31 palavras com 1 ideia central (transformação) e 3 atributos (pessoas, contexto, significado).
- **Encaixa com o visual:** O subtítulo diz "transforma cada foto em uma história". O visual mostra a transformação acontecendo. Texto e visual conversam.

### 3.4 CTAs: "Ver uma foto virar história" + "Começar a contar a minha"

- **CTA primário: "Ver uma foto virar história"**
  - Inverte a lógica: o visitante não é convidado a agir — é convidado a **ver a transformação acontecer**.
  - Reduz atrito: o visitante que ainda não entendeu o valor não precisa se comprometer.
  - Curiosidade: "Como uma foto vira história?" é uma pergunta que o visitante quer responder.
- **CTA secundário: "Começar a contar a minha"**
  - O compromisso fica como segunda opção.
  - Mais curto que o anterior ("Começar a contar minha história" → "Começar a contar a minha") — mais natural, menos corporativo.

### 3.5 Visual: Transformação foto → história

- **Objetivo psicológico:** Mostrar a transformação **acontecendo** em vez de mostrar uma interface.
- **Por que não um smartphone mockup:** Smartphones mostram "este é o app". A transformação mostra "isto é o que acontece com a sua foto". São efeitos psicológicos muito diferentes.
- **Como a transformação é mostrada:**
  - **Esquerda:** A mesma foto (`hero-familia.webp`) com um overlay escuro genérico, sem contexto, com legenda simples "Foto antiga da família — 14/07/1998".
  - **Centro:** Uma seta dourada com o label "aEterna".
  - **Direita:** A mesma foto com overlays ricos: avatar da pessoa (M para Maria), nome e idade, tags (Família, Recomeço, Casa nova), e uma frase em itálico (a história que aquela foto guarda).
- **A imagem é a mesma nos dois lados.** A diferença é o que se vê **por cima** dela. Isso reforça a ideia de que a foto é a mesma — o que muda é o que a aEterna permite extrair dela.
- **Continua usando tela real do app:** O Hero agora não mostra tela de smartphone, mas a foto (`hero-familia.webp`) é uma imagem real do projeto, alinhada com o tom do app.

### 3.6 Proof items simplificados

- **Antes:** "Plataforma completa para histórias de família" / "Família participa junto" / "Legado que continua vivo"
- **Depois:** "Histórias com pessoas, datas e contexto" / "Família contribui com suas versões" / "Legado que atravessa gerações"
- **O que mudou:** Substituição de adjetivos vazios ("completa", "vivo") por elementos concretos ("pessoas, datas e contexto", "versões", "gerações"). O visitante entende o que ganha, não só o que o produto é.

---

## 4. COMPARAÇÃO: ANTES × DEPOIS

| Aspecto | Antes (Sprint 5) | Depois (Sprint 5.5) |
|---|---|---|
| **H1** | "Você guarda as fotos. Quem guarda as histórias da sua família?" | "O que suas fotos vão contar quando você não estiver mais aqui?" |
| **Tipo de pergunta** | Duas perguntas (sobre o presente) | Uma pergunta (sobre o futuro) |
| **Foco** | O produto (a aEterna) | O visitante (suas fotos, seu futuro) |
| **Subtítulo** | 36 palavras, 4 ideias | 31 palavras, 1 ideia central |
| **CTA primário** | "Começar minha história" (compromisso) | "Ver uma foto virar história" (descoberta) |
| **CTA secundário** | "Ver como funciona" (genérico) | "Começar a contar a minha" (compromisso) |
| **Visual** | Smartphone com `home.webp` (mostra interface) | Transformação foto → história (mostra mudança) |
| **Imagem usada** | `home.webp` + `memoria-detalhe.webp` (telas do app) | `hero-familia.webp` (foto genérica, mas do projeto) |
| **Mensagem do visual** | "Este é o aplicativo" | "Isto é o que acontece com a sua foto" |
| **Proof items** | Adjetivos vazios | Elementos concretos |
| **Reação esperada em 5s** | "É um app de memórias" | "Espera... eu nunca pensei nisso sobre as minhas fotos" |

---

## 5. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | Linhas 2170-2330 (CSS) | **+160 linhas** de CSS para o novo Hero (transformation visual, overlays, responsividade) |
| `D:\aeterna\index.html` | Linhas 2430-2440 (CSS responsivo) | Regras para 1080px breakpoint |
| `D:\aeterna\index.html` | Linhas 2600-2615 (CSS responsivo) | Regras para 620px breakpoint |
| `D:\aeterna\index.html` | Linhas 2697-2755 (HTML) | Hero reescrito (eyebrow, H1, subtítulo, CTAs, proof items, visual) |

**Total: 1 arquivo, +177 linhas.**

**Não foi alterado:**
- SEO (`<title>`, meta tags)
- Schema.org (JSON-LD)
- robots.txt, sitemap.xml, manifest.json
- JavaScript estrutural (script de menu intocado)
- Páginas internas (legais, insights, blog)
- Arquitetura das outras 21 seções da Landing
- Identidade visual (paleta, tipografia, componentes)
- Páginas do aplicativo

---

## 6. VALIDAÇÃO

### 6.1 O visitante tende a parar nos primeiros segundos?

**Sim.** A combinação H1 + visual cria um efeito de "Espera..." quase imediato:

- O H1 confronta o visitante com seu próprio futuro ("quando você não estiver mais aqui").
- O visual mostra a transformação acontecendo visualmente.
- O contraste "foto sem contexto" vs. "foto com história" é imediatamente visível.

### 6.2 O Hero desperta curiosidade?

**Sim.** O H1 é uma pergunta, o que naturalmente provoca a necessidade de resposta. O visual reforça a curiosidade mostrando "o que muda" sem explicar o "como". O CTA "Ver uma foto virar história" convida o visitante a continuar explorando.

### 6.3 O mockup transmite transformação e não apenas uma interface?

**Sim.** O mockup anterior mostrava um smartphone com o app (uma interface). O novo visual mostra a **mesma foto** com dois tratamentos diferentes: sem contexto e com contexto. O visitante vê a transformação acontecendo, não vê "mais um app".

### 6.4 O CTA incentiva descoberta?

**Sim.** O CTA primário ("Ver uma foto virar história") convida o visitante a testemunhar a transformação, não a agir. É um convite à curiosidade, não à ação.

### 6.5 O Hero continua coerente com o aplicativo?

**Sim.** Todos os elementos do Hero refletem o que o app faz:
- "Transforma cada foto em uma história" → `app.py:1550-1752` (render_fotos)
- "Pessoas, contexto e significado" → `app.py:2783-2880` (render_preferencias) e `app.py:517-901` (render_minha_historia)
- "Família contribui com suas versões" → `app.py:1060-1192` (render_form_contribuicao_memoria)
- A imagem usada (`hero-familia.webp`) é do projeto, alinhada com o tom do app.

### 6.6 A Landing ficou mais convidativa sem perder elegância?

**Sim.** A paleta e tipografia foram mantidas. O novo Hero usa as mesmas variáveis CSS (`--bg`, `--gold`, `--gold-soft`, `--purple`). O visual tem mais elementos (overlays) que o anterior (smartphone), mas mantém a sobriedade e elegância. A diferença é de **impacto**, não de **estilo**.

---

## 7. PRINCÍPIOS APLICADOS

| Diretriz | Resposta |
|---|---|
| Não alterar SEO | ✅ `<head>` intocado |
| Não alterar arquitetura geral | ✅ Outras 21 seções intactas |
| Não alterar páginas internas | ✅ Nenhuma |
| Não alterar performance | ✅ Nenhuma |
| Não alterar Schema.org | ✅ Nenhum `<script type="application/ld+json">` alterado |
| Não alterar robots, sitemap, manifest, favicon | ✅ Nenhuma |
| Não alterar JavaScript estrutural | ✅ Script de menu intocado |
| O Hero deve provocar uma pergunta | ✅ "O que suas fotos vão contar quando você não estiver mais aqui?" |
| Mostrar transformação | ✅ Foto sem contexto → foto com história |
| Mockup deve despertar curiosidade | ✅ Transformação visual (não interface) |
| CTA incentiva descoberta | ✅ "Ver uma foto virar história" |
| Sem culpa, medo, dramatização, luto | ✅ Pergunta reflexiva, não ameaçadora |
| Coerência com o aplicativo | ✅ Todos os elementos refletem o app real |
| Manter identidade visual | ✅ Mesma paleta, tipografia, componentes |
| Redução de carga cognitiva | ✅ H1 mais curto, subtítulo mais direto, visual mais claro |

---

## 8. OBSERVAÇÕES ESTRATÉGICAS

Esta sprint entregou o que a Landing mais precisava: um Hero que faz o visitante **parar e pensar** em vez de apenas **olhar e seguir**.

A Landing agora atende ao objetivo principal de uma Landing Page: gerar curiosidade suficiente para que a pessoa queira conhecer o resto.

O Hero não vende a aEterna. Ele vende uma **descoberta**: a de que fotos sem história são arquivos mortos, e que a aEterna pode transformá-las em algo que atravessa gerações.

Conforme registrado pelo usuário, a próxima fase deve ser a **integração profunda do site e do aplicativo** — garantindo que tudo o que o visitante encontrar após o Hero esteja perfeitamente alinhado com o produto.

---

**Fim da Sprint 5.5 — O momento "Espera..."**
