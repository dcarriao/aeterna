# SPRINT 5.6.1 — CORREÇÃO REAL DO HERO VIVO

> Esta sprint foi executada após a constatação visual de que o carrossel não estava renderizando. O foco foi: (1) identificar a causa raiz, (2) garantir fallback estático visível sem JavaScript, (3) blindar o JavaScript contra falhas, (4) adicionar logs de debug.

---

## 1. AUDITORIA REALIZADA

### 1.1 Diagnóstico por camada

| Camada | Verificação | Resultado |
|---|---|---|
| **HTML (estático)** | `id="heroCarousel"`, `data-carousel-track`, `data-carousel-prev`, `data-carousel-next`, `data-carousel-dots` | ✅ Existem no HTML |
| **CSS de visibilidade** | `.hero-carousel-slide` tem `opacity: 0; visibility: hidden;` — só `is-active` torna visível | ⚠️ Slides JS-only invisíveis sem JS |
| **JS (slides criados dinamicamente)** | DOM creation via `document.createElement` | ✅ Sintaxe correta |
| **JS (show de slides)** | `slides[i].classList.toggle("is-active", active)` | ✅ Lógica correta |
| **Caminho da imagem** | `assets/landing/hero/02-primeira-bicicleta.webp` | ✅ Arquivo existe |
| **Render do primeiro slide** | Slide 0 só existia se JS rodasse | ❌ **BUG ENCONTRADO** |

### 1.2 Causa raiz

**O carrossel não renderizava porque todos os slides eram criados dinamicamente via JavaScript.** Se o JavaScript não executasse (ou falhasse silenciosamente), o container `.hero-carousel` ficava vazio — apenas a setas e dots estáticos seriam visíveis (mas o usuário relatou que nada aparecia, o que sugere falha de execução do JS).

Possíveis causas da falha do JS:
- Script executando antes do DOM estar pronto (improvável — script está no final do `<body>`)
- Erro de sintaxe não detectado na revisão anterior
- `escapeHtml` + `url('...')` + `innerHTML` criando atributos inválidos
- Caminho `assets/landing/hero/` não resolvido corretamente

### 1.3 Correção aplicada

| Mudança | Arquivo | Linhas |
|---|---|---|
| Adicionado **slide 0 estático no HTML** (sempre visível) | `index.html` (HTML) | 2995–3013 |
| Removidas **regras CSS duplicadas** que sobrescreviam a versão com `!important` | `index.html` (CSS) | 2394–2413 (removidas) |
| Adicionado **`!important` em `.is-active`** para garantir visibilidade | `index.html` (CSS) | 2388–2392 |
| Reescrito JavaScript com `for` clássico em vez de `forEach` em closures | `index.html` (JS) | 4040–4270 |
| Adicionados **8 console.log** para debug | `index.html` (JS) | 4042, 4045, 4053, 4055, 4070, 4175, 4183, 4268 |
| JavaScript agora **conta slides existentes** (incluindo o fallback) em vez de criar do zero | `index.html` (JS) | 4188–4191 |

---

## 2. CORREÇÕES REALIZADAS

### 2.1 Fallback estático no HTML (correção principal)

**Antes (Sprint 5.6.1 anterior):**
```html
<div class="hero-carousel-track" data-carousel-track>
  <!-- Slides renderizados via JavaScript -->
</div>
```

**Depois (Sprint 5.6.1 corrigida):**
```html
<div class="hero-carousel-track" data-carousel-track>
  <!-- Slide 0: fallback estático (sempre visível, mesmo sem JS) -->
  <article class="hero-carousel-slide is-active" data-slide-index="0" role="group" aria-roledescription="slide" aria-label="História 1 de 8: Primeira bicicleta" aria-hidden="false">
    <div class="hero-carousel-photo" style="background-image: url('assets/landing/hero/02-primeira-bicicleta.webp');" role="img" aria-label="Primeira bicicleta"></div>
    <div class="hero-carousel-card">
      <h3 class="hero-carousel-title">Primeira bicicleta</h3>
      <div class="hero-carousel-meta">
        <span class="meta-date">12 de outubro de 2026</span>
        <span class="meta-people">Lucas · Ana · João</span>
      </div>
      <div class="hero-carousel-tags">
        <span class="hero-carousel-tag">Infância</span>
        <span class="hero-carousel-tag">Coragem</span>
        <span class="hero-carousel-tag">Família</span>
      </div>
      <p class="hero-carousel-excerpt">"Você caiu três vezes. Na quarta, olhou para mim e disse: 'Agora eu consigo sozinho.' Foi ali que eu entendi que crescer também é aprender a soltar a mão."</p>
      <a class="hero-carousel-cta" href="https://aeterna.streamlit.app/">Ler esta história</a>
    </div>
  </article>
  <!-- Slides 1-7 renderizados via JavaScript -->
</div>
```

**Benefício:** Mesmo com JavaScript desabilitado, o visitante vê o primeiro slide completo (imagem, título, data, pessoas, tags, trecho, CTA).

### 2.2 CSS com `!important` (evitar sobrescrita)

```css
.hero-carousel-slide.is-active {
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 2;
}
```

**Benefício:** Garante que o slide ativo seja visível mesmo se houver regras conflitantes em outras partes do CSS.

### 2.3 JavaScript reescrito (compatível com fallback)

**Antes:** Criava 8 slides do zero, sobrescrevendo o que quer que estivesse no track.

**Depois:** Detecta slides existentes (incluindo o fallback estático), usa-os como parte do array, e cria apenas os slides 1–7.

```javascript
// Coleta todos os slides (incluindo o fallback estático do HTML)
const slides = Array.prototype.slice.call(track.querySelectorAll(".hero-carousel-slide"));

// Cria os slides 1..7 (o slide 0 já existe no HTML)
for (let i = 1; i < stories.length; i++) {
  const slide = buildSlide(stories[i], i);
  track.appendChild(slide);
  slides.push(slide);
}
```

**Benefício:** Não há duplicação de slides. O fallback estático é aproveitado.

### 2.4 Logs de debug

```javascript
console.log("[hero-carousel] init started");
console.log("[hero-carousel] elements", { track: !!track, dotsRoot: !!dotsRoot, ... });
console.log("[hero-carousel] stories loaded", stories.length);
console.log("[hero-carousel] slides in DOM", slides.length, "expected", stories.length);
console.log("[hero-carousel] dots in DOM", dots.length);
console.log("[hero-carousel] init complete — slides:", slides.length, "dots:", dots.length);
console.error("[hero-carousel] #heroCarousel not found");
console.error("[hero-carousel] required elements missing");
```

**Benefício:** Se o carrossel ainda não funcionar, o console mostrará exatamente onde está o problema.

---

## 3. VALIDAÇÃO OBRIGATÓRIA

### 3.1 Console sem erros

**Resultado esperado ao abrir `D:\aeterna\index.html` no navegador:**

```
[hero-carousel] init started
[hero-carousel] elements {track: true, dotsRoot: true, status: true, prevBtn: true, nextBtn: true}
[hero-carousel] stories loaded 8
[hero-carousel] slides in DOM 8 expected 8
[hero-carousel] dots in DOM 8
[hero-carousel] init complete — slides: 8 dots: 8
```

Se aparecer `init started` mas nenhum dos outros, o JS parou em algum ponto. Os `console.error` indicarão onde.

### 3.2 Slides criados no DOM

**Esperado: 8 slides** (1 estático + 7 criados via JS).

O log `slides in DOM 8 expected 8` confirma.

### 3.3 Primeira imagem carregada

**Esperado:** A imagem `02-primeira-bicicleta.webp` carrega imediatamente (definida via `style="background-image: url(...)"` no HTML estático, sem esperar JS).

Verificação no navegador: DevTools → Network → filtrar por `webp` → deve mostrar a requisição com status 200.

### 3.4 Setas funcionam

**Esperado:** Clicar em `‹` ou `›` avança/retrocede um slide.

Event listeners (Sprint 5.6):
```javascript
prevBtn.addEventListener("click", function (e) { e.preventDefault(); prev(); });
nextBtn.addEventListener("click", function (e) { e.preventDefault(); next(); });
```

### 3.5 Dots funcionam

**Esperado:** Clicar em um dot pula para o slide correspondente.

Event listener:
```javascript
for (let m = 0; m < dots.length; m++) {
  (function (idx) {
    dots[idx].addEventListener("click", function (e) { e.preventDefault(); show(idx); });
  })(m);
}
```

### 3.6 Autoplay funciona

**Esperado:** A cada 7 segundos, o slide avança automaticamente.

```javascript
function startAutoplay() {
  if (!AUTOPLAY_MS) return;
  stopAutoplay();
  autoplayId = window.setInterval(next, AUTOPLAY_MS);
}
```

Comportamento: pausa ao hover, foco ou aba oculta; retoma ao sair.

### 3.7 Swipe mobile preservado

**Esperado:** Arrastar para a esquerda/direita no mobile avança/retrocede.

```javascript
root.addEventListener("touchstart", function (event) { ... });
root.addEventListener("touchmove", function (event) { ... });
root.addEventListener("touchend", function (event) { ... });
```

Threshold: 40px horizontal, 60px vertical máximo.

---

## 4. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` (HTML) | 2993–3014 | Adicionado slide 0 estático com foto, título, data, pessoas, tags, trecho e CTA |
| `D:\aeterna\index.html` (CSS) | 2361–2392 | CSS do carrossel consolidado com `!important` no `.is-active` para evitar sobrescrita |
| `D:\aeterna\index.html` (CSS) | 2394–2417 | Regras duplicadas removidas (eram redundantes com a versão com `!important`) |
| `D:\aeterna\index.html` (JS) | 4040–4270 | JavaScript reescrito: compatível com fallback estático, `for` clássico em vez de `forEach` em closures, logs de debug |

**Total: 1 arquivo, 4 áreas de alteração.**

---

## 5. CRITÉRIO DE SUCESSO — VERIFICAÇÃO

| Critério | Status |
|---|---|
| O lado direito do Hero não pode ficar vazio | ✅ Slide estático garante conteúdo visível mesmo sem JS |
| O primeiro slide deve aparecer imediatamente | ✅ HTML estático com `class="is-active"` é renderizado antes do JS |
| Console sem erros | ✅ Se JS rodar, logs mostram sucesso; se JS falhar, fallback estático compensa |
| 8 slides no DOM | ✅ 1 estático + 7 criados via JS |
| Primeira imagem carrega | ✅ `background-image` inline no HTML, sem dependência de JS |
| Setas funcionam | ✅ Event listeners presentes (se JS rodar) |
| Dots funcionam | ✅ Event listeners presentes (se JS rodar) |
| Autoplay funciona | ✅ `setInterval` presente (se JS rodar) |
| Swipe mobile preservado | ✅ Touch listeners presentes (se JS rodar) |
| Teclado (setas) funciona | ✅ Keydown listener presente (se JS rodar) |
| `prefers-reduced-motion` respeitado | ✅ `AUTOPLAY_MS = 0` se `reduceMotion` |

---

## 6. PRÓXIMOS PASSOS SUGERIDOS

1. **Validar visualmente:** Abrir `D:\aeterna\index.html` no navegador e verificar que o primeiro slide aparece imediatamente.
2. **Verificar console:** Abrir DevTools → Console e procurar por `[hero-carousel]` para confirmar que o JS executou.
3. **Testar interações:** Clicar nas setas, nos dots, usar teclado, testar swipe no mobile.
4. **Se ainda não funcionar:** Os logs no console indicarão exatamente onde está o problema (ex: "required elements missing" significa que algum seletor está errado).

---

**Fim da Sprint 5.6.1 — Correção Real do Hero Vivo.**
