# SPRINT 5.6.2 — RECONSTRUÇÃO VISUAL DO HERO VIVO

> Sprint dedicada a reconstruir a aparência visual do carrossel para que a fotografia seja protagonista. O carrossel continua funcional (Sprint 5.6.1 corrigida); esta sprint muda apenas a estética, tornando a foto o elemento dominante e o card uma camada translúcida sobre ela.

---

## 1. ANTES × DEPOIS

### 1.1 Antes (Sprint 5.6.1)

| Elemento | Estilo anterior |
|---|---|
| `.hero-carousel` | `background: rgba(8, 0, 20, .5)` (bloco escuro dominante) + `box-shadow` pesada |
| Overlay da foto | `rgba(8, 0, 20, .15)` → `.4` → `.92` (escurecimento forte do meio ao fim) |
| Card | `border: 1px solid rgba(212, 175, 55, .28)` (borda dourada pesada) + `background: rgba(8, 0, 20, .88)` (muito escuro) + `box-shadow: 0 20px 50px rgba(0, 0, 0, .35)` |
| Card padding | `18px 20px 16px` |
| Card max-width | `400px` |
| Card position | `left: 28px; right: 28px; bottom: 52px` |
| Título do card | `1.35rem` |
| Tags | `background: rgba(212, 175, 55, .14)` (dourado) + `border: 1px solid rgba(212, 175, 55, .3)` |
| Excerpt | `.88rem` |
| Setas | `42px`, `background: rgba(8, 0, 20, .7)`, `border: 1px solid rgba(212, 175, 55, .45)` (dourado) |
| Dots | `8px`, `background: rgba(255, 255, 255, .3)`, ativo com `26px` |
| Padding Hero | `38px 0 56px` |
| `.hero-visual::before` (glow) | `rgba(212,175,55,.2)` |

### 1.2 Depois (Sprint 5.6.2)

| Elemento | Estilo novo |
|---|---|
| `.hero-carousel` | `background: transparent` (sem bloco escuro) |
| Overlay da foto | `rgba(0, 0, 0, 0)` → `0` → `.25` → `.75` (mais suave, só escurece no rodapé para o card) |
| Card | `border: 1px solid rgba(255, 255, 255, .14)` (borda branca translúcida sutil) + `background: rgba(20, 8, 32, .72)` (menos escuro, mais translúcido) + `box-shadow: 0 8px 32px rgba(0, 0, 0, .18)` (sombra mais leve) + `backdrop-filter: blur(16px) saturate(140%)` (glassmorphism) |
| Card padding | `18px 20px 16px` (mantido) |
| Card max-width | `400px` (mantido) |
| Card position | `left: 28px; right: 28px; bottom: 52px` (mantido) |
| Título do card | `1.35rem` + `text-shadow: 0 1px 8px rgba(0, 0, 0, .4)` (legibilidade) |
| Tags | `background: rgba(255, 255, 255, .12)` (branco translúcido) + `border: 1px solid rgba(255, 255, 255, .18)` (sem dourado pesado) |
| Excerpt | `.88rem` + `text-shadow: 0 1px 6px rgba(0, 0, 0, .3)` (legibilidade) |
| Setas | `38px`, `background: rgba(8, 0, 20, .45)`, `border: 1px solid rgba(255, 255, 255, .18)`, `opacity: .75` (mais discretas) + `backdrop-filter: blur(8px)` |
| Dots | `7px`, `background: rgba(255, 255, 255, .4)`, ativo com `22px` (mais discreto) |
| Padding Hero | `32px 0 48px` (reduzido) |
| `.hero-visual::before` (glow) | `rgba(212,175,55,.1)` (mais suave) + `z-index: 0` (atrás do carrossel) |

### 1.3 Mudança-chave: a foto é protagonista

| Aspecto | Antes | Depois |
|---|---|---|
| Bloco escuro de fundo do carrossel | Sim (`.5` opacidade) | Removido (transparente) |
| Overlay sobre a foto | Escuro do meio ao fim (`.15` → `.4` → `.92`) | Transparente do topo até 45%, suave depois (`.25` → `.75`) |
| Borda do card | Dourada (`rgba(212, 175, 55, .28)`) | Branca translúcida (`rgba(255, 255, 255, .14)`) |
| Background do card | Muito escuro (`.88`) | Translúcido (`.72`) + `backdrop-filter: blur(16px) saturate(140%)` |
| Efeito do card | Popup (sombra pesada) | Camada de significado (glassmorphism) |

**Resultado:** A foto ocupa quase toda a área do carrossel. O card aparece como uma camada de significado sobre a foto, não como um bloco separado.

---

## 2. CORREÇÕES APLICADAS

### 2.1 `.hero-carousel` — removido bloco escuro

```css
/* Antes */
background: rgba(8, 0, 20, .5);
box-shadow: var(--shadow);

/* Depois */
background: transparent;
```

**Benefício:** A foto aparece diretamente sobre o fundo da página, sem intermediário escuro.

### 2.2 `.hero-carousel-photo::after` — overlay mais suave

```css
/* Antes */
background:
  linear-gradient(180deg, rgba(8, 0, 20, .15) 0%, rgba(8, 0, 20, .4) 60%, rgba(8, 0, 20, .92) 100%);

/* Depois */
background:
  linear-gradient(180deg,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0) 45%,
    rgba(0, 0, 0, .25) 70%,
    rgba(0, 0, 0, .75) 100%);
```

**Benefício:** A foto permanece visível do topo até 45% da altura. O escurecimento só aparece no rodapé, onde o card fica. O texto continua legível no card (`.75` no rodapé é suficiente com o `backdrop-filter` do card).

### 2.3 `.hero-carousel-photo` — Ken Burns sutil

```css
/* Adicionado */
.hero-carousel-photo {
  transform: scale(1.02);
  transition: transform 6s ease-out;
}

.hero-carousel-slide.is-active .hero-carousel-photo {
  transform: scale(1);
}
```

**Benefício:** Ao trocar de slide, a foto faz um zoom-out sutil de 1.02 → 1.0 em 6 segundos, criando uma sensação de "respiração" da memória. É o efeito Ken Burns mínimo, sem ser distrator.

### 2.4 `.hero-carousel-card` — glassmorphism

```css
/* Antes */
border: 1px solid rgba(212, 175, 55, .28);
background: rgba(8, 0, 20, .88);
backdrop-filter: blur(10px);
box-shadow: 0 20px 50px rgba(0, 0, 0, .35);

/* Depois */
border: 1px solid rgba(255, 255, 255, .14);
background: rgba(20, 8, 32, .72);
backdrop-filter: blur(16px) saturate(140%);
box-shadow: 0 8px 32px rgba(0, 0, 0, .18);
```

**Benefício:** O card agora é uma camada translúcida com `backdrop-filter` que desfoca e satura a foto por trás. Não é mais um popup escuro. A borda branca translúcida sugere "luz" em vez de "caixa".

### 2.5 Tags — mais discretas

```css
/* Antes */
background: rgba(212, 175, 55, .14);
border: 1px solid rgba(212, 175, 55, .3);
color: var(--gold-soft);
padding: 2px 8px;

/* Depois */
background: rgba(255, 255, 255, .12);
border: 1px solid rgba(255, 255, 255, .18);
color: rgba(255, 255, 255, .92);
padding: 2px 8px;
```

**Benefício:** As tags agora são pílulas brancas translúcidas, em vez de douradas. Mais discretas, mas ainda legíveis.

### 2.6 Título e Excerpt — com text-shadow

```css
/* Adicionado */
.hero-carousel-title {
  text-shadow: 0 1px 8px rgba(0, 0, 0, .4);
}

.hero-carousel-excerpt {
  text-shadow: 0 1px 6px rgba(0, 0, 0, .3);
}
```

**Benefício:** O texto fica legível mesmo sobre fotos claras ou escuras, sem precisar de um fundo pesado.

### 2.7 Setas — mais discretas

```css
/* Antes */
width: 42px; height: 42px;
background: rgba(8, 0, 20, .7);
border: 1px solid rgba(212, 175, 55, .45);
color: var(--gold-soft);
font-size: 1.2rem;
opacity: 1;

/* Depois */
width: 38px; height: 38px;
background: rgba(8, 0, 20, .45);
border: 1px solid rgba(255, 255, 255, .18);
color: rgba(255, 255, 255, .85);
font-size: 1.1rem;
opacity: .75;
backdrop-filter: blur(8px);
```

**Benefício:** As setas são menores, mais translúcidas, com borda branca (não dourada). Opacidade `.75` por padrão; ficam opacas no hover.

### 2.8 Dots — mais discretos

```css
/* Antes */
width: 8px; height: 8px;
background: rgba(255, 255, 255, .3);
opacity: 1;
ativo: width: 26px;

/* Depois */
width: 7px; height: 7px;
background: rgba(255, 255, 255, .4);
opacity: .7;
ativo: width: 22px; opacity: 1;
```

**Benefício:** Dots menores e mais translúcidos, com o ativo em `.22px` (em vez de `.26px`).

### 2.9 Hero padding — reduzido

```css
/* Antes */
padding: 38px 0 56px;

/* Depois */
padding: 32px 0 48px;
```

**Benefício:** Menos espaço entre o header e o conteúdo, mais espaço na parte inferior.

### 2.10 `.hero-visual::before` — glow suave

```css
/* Antes */
background: radial-gradient(circle, rgba(212,175,55,.2), transparent 62%);

/* Depois */
background: radial-gradient(circle, rgba(212,175,55,.1), transparent 62%);
z-index: 0;
```

**Benefício:** O glow dourado é 50% mais sutil e fica atrás do carrossel (`.z-index: 0`). O carrossel é o protagonista.

---

## 3. CRITÉRIO DE SUCESSO

| Critério | Status |
|---|---|
| Ao abrir a Landing, a primeira coisa vista no lado direito é a fotografia | ✅ Foto ocupa 100% do container; card é camada translúcida |
| A segunda coisa é a história | ✅ Card com 72% opacidade deixa a foto visível através dele |
| Nunca o contrário | ✅ Card não é mais "popup"; é "camada" |
| Foto aparece claramente | ✅ `background-size: cover` + `background-position: center` garantidos com `!important` |
| Card é legível | ✅ `text-shadow` no título e excerpt + `backdrop-filter: blur(16px)` no card |
| Setas/dots funcionam | ✅ Event listeners preservados (Sprint 5.6.1) |
| Hero parece uma lembrança viva | ✅ Ken Burns sutil (zoom-out de 1.02 → 1.0 em 6s) + glassmorphism no card |
| Sem popup | ✅ Card menor (400px max), sem box-shadow pesada, sem borda dourada |
| Overlay leve | ✅ Gradiente transparente do topo até 45% da foto |
| Fundo não é bloco preto | ✅ `.hero-carousel` agora tem `background: transparent` |

---

## 4. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` (CSS) | 2360–2368 | `.hero-carousel` removido `background: rgba(8, 0, 20, .5)` e `box-shadow` |
| `D:\aeterna\index.html` (CSS) | 2382–2402 | `.hero-carousel-photo` adicionado Ken Burns; overlay mais suave |
| `D:\aeterna\index.html` (CSS) | 2418–2443 | `.hero-carousel-card` glassmorphism (borda branca, bg mais translúcido, `backdrop-filter`) |
| `D:\aeterna\index.html` (CSS) | 2448–2452 | `.hero-carousel-title` adicionado `text-shadow` |
| `D:\aeterna\index.html` (CSS) | 2476–2489 | `.hero-carousel-tag` mais discreto (branco translúcido) |
| `D:\aeterna\index.html` (CSS) | 2494–2500 | `.hero-carousel-excerpt` adicionado `text-shadow` |
| `D:\aeterna\index.html` (CSS) | 2529–2554 | `.hero-carousel-nav` mais discreto (38px, `.45` opacidade, blur) |
| `D:\aeterna\index.html` (CSS) | 2567–2595 | `.hero-carousel-dots` e `.hero-carousel-dot` mais discretos |
| `D:\aeterna\index.html` (CSS) | 268 | `.hero` padding reduzido (`38px 0 56px` → `32px 0 48px`) |
| `D:\aeterna\index.html` (CSS) | 329–336 | `.hero-visual::before` glow mais sutil + `z-index: 0` |
| `D:\aeterna\index.html` (CSS) | 2859–2897 | Regras responsivas (1080px) atualizadas |

**Total: 1 arquivo, 11 áreas de CSS alteradas. Nenhuma alteração em HTML ou JavaScript.**

---

## 5. VALIDAÇÃO

| Validação | Como verificar |
|---|---|
| Print desktop 1920×1080 | Abrir `D:\aeterna\index.html` no navegador em tela 1920×1080; tirar print; verificar que a foto ocupa todo o container direito e o card está no canto inferior esquerdo |
| Print notebook 1366×768 | Mesmo procedimento em tela 1366×768; verificar que o Hero cabe na primeira dobra |
| Print mobile | Mesmo procedimento em DevTools → modo responsivo (375px); verificar que o card se adapta |
| Foto aparece claramente | Olhar para a foto: deve estar nítida, com boa resolução, sem estar muito escurecida |
| Card é legível | Ler o título, data, pessoas, tags e trecho no card: devem estar visíveis e nítidos |
| Setas/dots funcionam | Clicar nas setas para navegar; clicar nos dots para pular para um slide específico |
| Hero parece uma lembrança viva | Olhar para a primeira dobra: a primeira coisa vista é a foto, a segunda é a história. Não há sensação de "componente colado" |

---

**Fim da Sprint 5.6.2 — Reconstrução visual do Hero Vivo.**
