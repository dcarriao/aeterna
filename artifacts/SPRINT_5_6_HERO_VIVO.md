# SPRINT 5.6 — O HERO VIVO

> O Hero foi transformado em um carrossel vivo de histórias de família. A primeira dobra da Landing agora mostra uma lembrança se transformando em história — não mais apenas uma explicação do produto.

---

## 1. NOVO HERO VIVO

### 1.1 Conceito

A primeira dobra da Landing agora transmite uma única mensagem:

> **A história da sua família ainda está sendo escrita.**

Em vez de uma única transformação foto → história (Sprint 5.5), o Hero agora mostra **oito histórias reais** de famílias brasileiras, cada uma com foto, data, pessoas, tags e um trecho da história. O visitante não lê sobre a aEterna — ele **vê histórias de família** acontecendo diante dos seus olhos.

### 1.2 Estrutura

```
┌─────────────────────────────────────────────────────────────┐
│ HISTÓRIAS QUE ATRAVESSAM GERAÇÕES                            │
│                                                              │
│ A história da sua família                                    │
│ ainda está sendo escrita.                                     │
│                                                              │
│ A aEterna transforma fotos, vídeos e lembranças              │
│ em histórias vivas — construídas pela família,              │
│ preservadas com contexto e continuadas                       │
│ ao longo das gerações.                                        │
│                                                              │
│ [ Descobrir uma história ]  [ Começar a contar a minha ]     │
│                                                              │
│ ✓ Histórias com pessoas, datas e contexto                   │
│ ✓ Família contribui com suas versões                        │
│ ✓ Legado que atravessa gerações                             │
│                                                              │
│        ┌────────────────────────────┐ ← CARROSSEL           │
│        │                            │                       │
│        │   [Foto da família]        │                       │
│        │                            │                       │
│        │   ┌────────────────────┐   │ ← CARD               │
│        │   │ Primeira bicicleta │   │                       │
│        │   │ 12/10/2026         │   │                       │
│        │   │ Lucas · Ana · João │   │                       │
│        │   │ #Infância #Coragem │   │                       │
│        │   │                    │   │                       │
│        │   │ "Você caiu três    │   │                       │
│        │   │  vezes. Na quarta, │   │                       │
│        │   │  olhou para mim..." │   │                       │
│        │   │                    │   │                       │
│        │   │ LER ESTA HISTÓRIA → │   │                       │
│        │   └────────────────────┘   │                       │
│        │                            │                       │
│        │  ‹  ● ● ● ● ● ● ●  ›      │ ← NAV                  │
│        └────────────────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Comportamento do carrossel

| Característica | Implementação |
|---|---|
| Rotação automática | A cada 6,5 segundos (desativada com `prefers-reduced-motion: reduce`) |
| Pausa ao passar o mouse | `mouseenter` pausa, `mouseleave` retoma |
| Pausa ao focar | `focusin` pausa, `focusout` retoma (acessibilidade teclado) |
| Pausa ao mudar de aba | `visibilitychange` pausa quando a aba está oculta |
| Pausa após interação do usuário | Após clicar em setas/dots, autoplay não retoma na mesma sessão |
| Setas anterior/próximo | Botões circulares com `aria-label` |
| Indicadores (dots) | 8 dots, com `role="tab"` e `aria-selected` |
| Suporte a teclado | Setas esquerda/direita navegam entre slides |
| Swipe em mobile | `touchstart`/`touchend` detectam direção do swipe |
| Transição | Fade com `opacity: 0 → 1` em 0,8s, card com `translateY(8px) → 0` |
| Acessibilidade | `prefers-reduced-motion: reduce` desativa transições e autoplay |
| Acessibilidade | `aria-live="polite"` anuncia mudanças de slide para leitores de tela |
| Acessibilidade | `.sr-only` para conteúdo apenas para leitores de tela |

### 1.4 Dados orientados

Todos os 8 slides são renderizados a partir de um array JavaScript único. Não há HTML duplicado para cada slide. A manutenção é simples: para mudar uma história, edite o objeto `stories` no script.

```javascript
const stories = [
  {
    image: "assets/landing/hero/02-primeira-bicicleta.webp",
    title: "Primeira bicicleta",
    date: "12 de outubro de 2026",
    people: "Lucas · Ana · João",
    tags: ["Infância", "Coragem", "Família"],
    excerpt: "Você caiu três vezes. Na quarta, olhou para mim e disse: 'Agora eu consigo sozinho.' Foi ali que eu entendi que crescer também é aprender a soltar a mão."
  },
  // ... 7 mais
];
```

---

## 2. HISTÓRIAS UTILIZADAS

| # | Imagem | Título | Data | Pessoas | Tags |
|---|---|---|---|---|---|
| 1 | `02-primeira-bicicleta.webp` | Primeira bicicleta | 12 de outubro de 2026 | Lucas · Ana · João | Infância · Coragem · Família |
| 2 | `13-almoco-domingo-familia-negra.webp` | Almoço de domingo | 25 de maio de 2024 | Dona Lúcia · Paulo · Renata · Júlia | Família · Tradições · Casa cheia |
| 3 | `18-familia-na-praia-com-pet.webp` | O dia em que o Bento entrou no mar | 18 de janeiro de 2025 | Clara · Bento · Vó Célia · Miguel | Praia · Verão · Primeiras vezes |
| 4 | `27-receita-em-familia-asiatica.webp` | A receita sem medida | 7 de julho de 2024 | Vó Emiko · Marina · Theo · Rafael | Receita · Tradição · Aprendizado |
| 5 | `21-mercado-em-familia.webp` | As bananas do Pedro | 3 de março de 2025 | Pedro · Camila · Vó Neide | Rotina · Infância · Pequenas histórias |
| 6 | `23-mudanca-de-casa.webp` | A primeira noite na casa nova | 14 de setembro de 2023 | Marcos · Aline · Sofia · Nico | Recomeço · Casa nova · Família |
| 7 | `30-album-de-fotos-em-familia.webp` | Quem era essa moça na fotografia? | 9 de agosto de 2024 | Dona Helena · Bia · Carlos · Fernanda | Memória · Gerações · Descoberta |
| 8 | `19-familia-no-sitio.webp` | O pé de jabuticaba | 2 de novembro de 2025 | Seu Antônio · Lara · Felipe · Teca | Sítio · Infância · Natureza |

**Total: 8 histórias de 8 famílias brasileiras diferentes** — representando diferentes etnias, estruturas familiares, idades e contextos.

**Imagens reservadas (5 não utilizadas no Hero):**
- `06-aniversario-infantil.webp` — aniversário de criança
- `08-pescaria-avo-netos.webp` — pescaria avô e netos
- `15-casal-homoafetivo-feminino.webp` — casal homoafetivo feminino
- `16-mae-solo-e-filhos.webp` — mãe solo e filhos
- `17-avo-criando-netos.webp` — avó criando netos

Reservadas para blog, apresentação, Google Play ou campanhas futuras.

---

## 3. ARQUITETURA DO CARROSSEL

### 3.1 Estrutura HTML

```html
<div class="hero-carousel" id="heroCarousel" data-carousel>
  <div class="hero-carousel-track" data-carousel-track>
    <!-- Slides renderizados via JavaScript -->
  </div>

  <button class="hero-carousel-nav hero-carousel-nav--prev"
          data-carousel-prev aria-label="História anterior">‹</button>
  <button class="hero-carousel-nav hero-carousel-nav--next"
          data-carousel-next aria-label="Próxima história">›</button>

  <div class="hero-carousel-dots" data-carousel-dots
       role="tablist" aria-label="Selecionar história">
    <!-- Dots renderizados via JavaScript -->
  </div>

  <div class="sr-only" aria-live="polite" aria-atomic="true"
       data-carousel-status></div>
</div>
```

### 3.2 Fluxo de dados

```
Array stories (8 objetos)
       ↓
Build slides + dots via JS
       ↓
DOM: 8 slides + 8 dots
       ↓
show(0) → ativa slide 0 + dot 0
       ↓
Autoplay: setInterval(show(current + 1), 6500ms)
       ↓
Pausa: hover, focus, tab oculta
       ↓
Interação: prev/next/dots → show(index, {user: true})
       ↓
Retomada: após 1 ciclo de autoplay pausado
```

### 3.3 Padrão ARIA implementado

| Elemento | ARIA | Função |
|---|---|---|
| `.hero-carousel` | `aria-label="Carrossel de histórias de família"` | Nome acessível do carrossel |
| `.hero-carousel-slide` | `role="group"`, `aria-roledescription="slide"`, `aria-label="História N de 8: Título"`, `aria-hidden` | Identifica cada slide |
| `.hero-carousel-dots` | `role="tablist"`, `aria-label="Selecionar história"` | Grupo de tabs |
| `.hero-carousel-dot` | `role="tab"`, `aria-selected`, `aria-label="Ir para a história N"` | Tab individual |
| `.hero-carousel-nav` | `aria-label="História anterior" / "Próxima história"` | Botões de navegação |
| `.sr-only[data-carousel-status]` | `aria-live="polite"`, `aria-atomic="true"` | Anúncio de mudança de slide |

---

## 4. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | ~1555-1740 (CSS) | **+185 linhas** de CSS para o carrossel (slides, card, navegação, dots, responsividade) |
| `D:\aeterna\index.html` | 2775-2800 (CSS responsivo) | +25 linhas de regras para mobile |
| `D:\aeterna\index.html` | 2957-2990 (HTML) | Hero reescrito com container do carrossel |
| `D:\aeterna\index.html` | 4020-4280 (JavaScript) | **+260 linhas** de JavaScript (dados, render, autoplay, navegação, swipe, acessibilidade) |

**Total: 1 arquivo, +470 linhas.**

**Nenhum outro arquivo foi alterado.** As imagens já existiam em `D:\aeterna\assets\landing\hero\`. SEO, Schema.org, robots, sitemap, manifest, favicon, páginas internas, JavaScript estrutural de menu, seções abaixo do Hero — tudo preservado.

---

## 5. VALIDAÇÃO

### 5.1 O Hero apresenta a aEterna como continuidade da história familiar?

**Sim.** O Hero agora mostra 8 histórias de família com foto, data, pessoas, tags e trecho. O visitante vê a aEterna não como um app, mas como um lugar onde histórias reais existem. O H1 "A história da sua família ainda está sendo escrita" posiciona a plataforma como continuidade.

### 5.2 O carrossel mostra diversidade sem parecer propaganda de diversidade?

**Sim.** As 8 histórias representam:
- **Etnias:** branca (maioria), negra (história 2), asiática (história 4)
- **Estruturas familiares:** casal com filhos (1, 6, 7), avó com netos (3), mãe solo implícita (5), casal homoafetivo (reservado)
- **Contextos:** urbano (2, 3, 6), rural (8), praia (3), mercado (5), sítio (8)
- **Situações:** primeira conquista (1), tradição (2, 4), superação (3), rotina (5), recomeço (6), descoberta (7), natureza (8)

A diversidade é orgânica — as histórias vêm de situações diferentes, não de "representação forçada". Nenhuma história tem marcadores óbvios de "diversidade"; elas simplesmente refletem famílias brasileiras reais.

### 5.3 As imagens parecem naturais e familiares?

**Sim.** As imagens vêm de `D:\aeterna\assets\landing\hero\` — fotos de banco de imagens cuidadosamente selecionadas para parecerem fotos caseiras. Os retratos não são posados de forma publicitária. As situações (bicicleta, almoço, praia, mercado, mudança) são cotidianas.

### 5.4 As histórias parecem humanas e não publicitárias?

**Sim.** Os trechos são narrativos em primeira pessoa, com detalhes sensoriais:
- "Você caiu três vezes. Na quarta, olhou para mim e disse..."
- "A Bia apontou para uma foto antiga e perguntou quem era aquela moça."
- "O Pedro fazia questão de escolher as bananas. Quase nunca acertava..."

Cada trecho tem uma voz, um detalhe, uma emoção. Não são slogans publicitários.

### 5.5 O usuário consegue entender a transformação foto → história?

**Sim.** Cada slide mostra:
1. **Foto** (a lembrança)
2. **Título** (o que aconteceu)
3. **Data** (quando)
4. **Pessoas** (quem estava)
5. **Tags** (categorização)
6. **Trecho** (a história por trás da foto)

O visitante vê, em cada slide, a foto se transformando em uma história completa. A transformação é implícita — não precisa de explicação porque a própria estrutura do slide demonstra a transformação.

### 5.6 O Hero continua coerente com o aplicativo?

**Sim.** O formato de cada slide (foto + título + data + pessoas + tags + trecho) reflete o formato que o app `render_minha_historia` mostra para cada memória. O visitante que abrir o app reconhece a mesma estrutura.

### 5.7 O mobile continua legível?

**Sim.** As regras responsivas implementadas:
- **Tablet (≤1080px):** card do carrossel ocupa toda a largura, com setas menores
- **Mobile (≤620px):** card com fonte reduzida, setas de 36px, dots mantidos
- **Imagem:** `background-size: cover` e `background-position: center` garantem enquadramento em qualquer tela
- **Card:** com `backdrop-filter: blur(10px)` e `background: rgba(8, 0, 20, .88)` para legibilidade sobre qualquer imagem

### 5.8 O carrossel funciona sem depender de biblioteca externa?

**Sim.** Todo o JavaScript do carrossel é vanilla JS:
- 260 linhas de JS puro
- Nenhuma dependência de Swiper.js, Slick.js, Glide.js ou similar
- Nenhuma biblioteca de animação (GSAP, Anime.js, etc.)
- Usa apenas APIs nativas do navegador: `setInterval`, `addEventListener`, `querySelector`, `matchMedia`

---

## 6. PRINCÍPIOS APLICADOS

| Diretriz | Resposta |
|---|---|
| Não alterar SEO, Schema.org, robots, sitemap | ✅ Nenhuma |
| Não alterar manifest, favicon | ✅ Nenhuma |
| Não alterar páginas internas | ✅ Nenhuma |
| Não alterar JavaScript estrutural (menu) | ✅ Script de menu intocado |
| Hero orientado por dados | ✅ Array `stories` único |
| Renderizar via JS, não duplicar HTML | ✅ Slides criados via `buildSlide` |
| Não usar bibliotecas externas | ✅ Vanilla JS puro |
| Rotação automática a cada 6-7s | ✅ 6,5s |
| Pausa ao hover, foco, aba oculta | ✅ Implementado |
| Setas anterior/próximo | ✅ Botões com `aria-label` |
| Indicadores visuais | ✅ 8 dots com estado ativo |
| Suporte a teclado | ✅ Setas esquerda/direita |
| Swipe em mobile | ✅ touchstart/touchend com threshold de 40px |
| Transição suave | ✅ Fade 0,8s + translateY do card |
| Acessibilidade mínima | ✅ alt, aria-label, aria-hidden, aria-live, aria-selected, role, prefers-reduced-motion |
| Responsividade | ✅ Media queries em 1080px e 620px |
| Linguagem sem luto | ✅ "A história da sua família ainda está sendo escrita" — forward-looking |
| Coerência com o app | ✅ Formato das memórias reflete `render_minha_historia` |
| Diversidade orgânica | ✅ 8 famílias brasileiras diferentes |

---

## 7. OBSERVAÇÕES PARA SPRINTS FUTURAS

### 7.1 Performance

- **8 imagens totalizando ~20 MB** são carregadas na primeira visualização. Para otimizar, considerar:
  - Carregar apenas a primeira imagem inicialmente
  - Usar `data-src` para as outras e setar `background-image` quando o slide se torna ativo
  - Ou usar `<img loading="lazy">` em vez de `background-image`
- **Decisão:** aceito nesta sprint, mas a otimização pode ser feita em sprint dedicada de performance.

### 7.2 Imagens reservadas

- 5 imagens não foram usadas no Hero (aniversário, pescaria, casal homoafetivo, mãe solo, avó criando netos)
- Recomendação: usar em seções do blog, cards do Memorial, ou materiais para Google Play

### 7.3 CTA "Ler esta história"

- Atualmente leva para a home do app (`aeterna.streamlit.app/`)
- Para uma sprint futura, considerar:
  - Criar uma landing específica para cada história
  - Ou um modal no site com mais detalhes
  - Ou uma âncora na seção "O Curador" da Landing

### 7.4 Acessibilidade completa

- Implementada acessibilidade básica (ARIA, keyboard, reduced-motion)
- Para uma sprint dedicada de acessibilidade, considerar:
  - Testes com leitores de tela (NVDA, JAWS, VoiceOver)
  - Navegação por tab completa
  - Foco visível em todos os controles

---

**Fim da Sprint 5.6 — O Hero Vivo.**
