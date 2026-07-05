# SPRINT 5.6.3 — LAPIDAÇÃO FINAL DO HERO VIVO

> Sprint dedicada a três correções críticas: (1) alinhamento vertical do grid, (2) alinhamento dos botões, e (3) mudança do CTA "Ler esta história" para abrir um modal com a história completa (em vez de levar ao login). Também adicionadas as 8 histórias completas e o modal acessível.

---

## 1. MUDANÇA PRINCIPAL: CTA ABRE MODAL

### 1.1 Antes (Sprint 5.6.2)

```html
<a class="hero-carousel-cta" href="https://aeterna.streamlit.app/">Ler esta história</a>
```

**Problema:** O usuário clicava em "Ler esta história" e era levado direto para a tela de login/cadastro do app. Isso gerava frustração porque a promessa não era cumprida.

### 1.2 Depois (Sprint 5.6.3)

```html
<a class="hero-carousel-cta" href="#" data-story-cta>Ler esta história</a>
```

**Solução:** O CTA agora abre um modal elegante com a história completa. O modal tem:
- Título da história
- Imagem de capa
- Data, pessoas, tags
- História completa
- Nota: "História organizada com ajuda do Curador da aEterna"
- CTA primário: "Começar a história da minha família" → leva ao app
- CTA secundário: "Fechar"

**Fluxo correto:**
1. Usuário vê o carrossel
2. Clica em "Ler esta história"
3. Modal abre com a história completa
4. Usuário lê a história
5. Usuário pode fechar OU clicar em "Começar a história da minha família" (vai para o app)

---

## 2. MODAL DE HISTÓRIA

### 2.1 Estrutura

```html
<div class="story-modal" id="storyModal" role="dialog" aria-modal="true" aria-labelledby="storyModalTitle" aria-describedby="storyModalText" aria-hidden="true">
  <div class="story-modal-dialog" tabindex="-1">
    <div class="story-modal-cover" id="storyModalCover" role="img" aria-label=""></div>
    <button type="button" class="story-modal-close" id="storyModalClose" aria-label="Fechar história">&times;</button>
    <div class="story-modal-body">
      <div class="story-modal-tags" id="storyModalTags"></div>
      <h3 class="story-modal-title" id="storyModalTitle"></h3>
      <div class="story-modal-meta" id="storyModalMeta"></div>
      <p class="story-modal-text" id="storyModalText"></p>
      <p class="story-modal-note">História organizada com ajuda do Curador da aEterna.</p>
      <div class="story-modal-actions">
        <a class="btn btn-primary" id="storyModalPrimary" href="https://aeterna.streamlit.app/">Começar a história da minha família</a>
        <button type="button" class="btn-close" id="storyModalSecondary">Fechar</button>
      </div>
    </div>
  </div>
</div>
```

### 2.2 Acessibilidade (WCAG 2.1 AA)

| Requisito | Implementação |
|---|---|
| `role="dialog"` | ✅ Atributo presente no container |
| `aria-modal="true"` | ✅ Atributo presente |
| `aria-labelledby` | ✅ Aponta para `storyModalTitle` |
| `aria-describedby` | ✅ Aponta para `storyModalText` |
| `aria-hidden` (toggle) | ✅ `true` quando fechado, `false` quando aberto |
| Fechar com ESC | ✅ `keydown` listener no `document` |
| Fechar clicando fora | ✅ `click` listener verifica `e.target === modal` |
| Foco no diálogo ao abrir | ✅ `dialog.focus()` com `setTimeout(50ms)` |
| Foco retorna ao botão ao fechar | ✅ `lastFocus.focus()` com `setTimeout(50ms)` |
| Trap de foco (Tab) | ✅ Loop entre primeiro e último elemento focável |
| Fechar com botão × | ✅ Botão com `aria-label="Fechar história"` |
| Fechar com botão "Fechar" | ✅ Botão no rodapé do modal |
| `prefers-reduced-motion` | ✅ Não adicionado ao modal (transição é só de opacidade, 250ms) |

---

## 3. HISTÓRIAS COMPLETAS (8)

Cada história tem agora um campo `fullStory` no array de dados. O modal usa `fullStory` quando disponível, com fallback para `excerpt`.

### Exemplo: Primeira bicicleta

```
Você caiu três vezes naquela tarde.

Na primeira, ficou bravo. Na segunda, quase desistiu. Na terceira, olhou para mim como quem perguntava se ainda valia a pena tentar.

Na quarta tentativa, eu soltei o banco sem você perceber. Você pedalou sozinho por poucos metros, virou o rosto e gritou: "Agora eu consigo!"

Foi ali que eu entendi que crescer também é aprender a soltar a mão.
```

### Todas as 8 histórias completas

1. **Primeira bicicleta** — sobre a primeira conquista de um filho
2. **Almoço de domingo** — sobre a história de uma bisavó que chegou com uma mala e uma receita
3. **O dia em que o Bento entrou no mar** — sobre vencer o medo com a ajuda da avó
4. **A receita sem medida** — sobre uma avó que ensinava com o corpo, não com a receita
5. **As bananas do Pedro** — sobre aprender a escolher, a ter voz
6. **A primeira noite na casa nova** — sobre recomeçar do zero
7. **Quem era essa moça na fotografia?** — sobre descobrir a própria avó antes de ser avó
8. **O pé de jabuticaba** — sobre pertencimento a um lugar

---

## 4. CORREÇÃO DE ALINHAMENTO DO HERO

### 4.1 Grid

**Antes:** `align-items: center` — forçava o texto e o carrossel a terem a mesma altura, criando espaços vazios desnecessários.

**Depois:** `align-items: start` — ambos os blocos começam no mesmo eixo vertical, sem forçar alturas iguais.

### 4.2 `.hero-visual`

**Antes:** `min-height: 610px; display: grid; place-items: center` — forçava o carrossel a ter pelo menos 610px e o centralizava verticalmente em um espaço maior que o necessário.

**Depois:** `min-height: 100%; display: block` — o carrossel se adapta à sua própria altura (480px), sem forçar um valor mínimo artificial.

### 4.3 Botões

**Adicionado:** `line-height: 1` no `.btn` para garantir alinhamento vertical consistente entre o `.btn-primary` (com gradiente) e o `.btn-outline` (com borda).

**Já existia:** `display: inline-flex; min-height: 54px; align-items: center; justify-content: center; white-space: nowrap`.

**Resultado:** Os dois botões têm a mesma altura, mesmo baseline, mesmo espaçamento interno.

---

## 5. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` (CSS) | 230–244 | `.btn` adicionado `line-height: 1; text-decoration: none` |
| `D:\aeterna\index.html` (CSS) | 271–276 | `.hero-grid` `align-items: start` (era `center`) |
| `D:\aeterna\index.html` (CSS) | 319–324 | `.hero-visual` removido `min-height: 610px` e `display: grid; place-items: center` |
| `D:\aeterna\index.html` (CSS) | 2607–2850 | **+243 linhas** de CSS para o modal de história |
| `D:\aeterna\index.html` (HTML) | 3245 | CTA do card estático mudado para `href="#" data-story-cta` |
| `D:\aeterna\index.html` (HTML) | 4505–4610 | **+105 linhas** de HTML+JS para o modal (container + script) |
| `D:\aeterna\index.html` (JS) | 4085–4094 | Adicionado campo `fullStory` em cada um dos 8 stories |
| `D:\aeterna\index.html` (JS) | 4360–4365 | CTA no `buildSlide` agora é `<a href="#" data-story-cta>` |
| `D:\aeterna\index.html` (JS) | 4466–4480 | Função `bindCtas()` que abre o modal ao clicar no CTA |

**Total: 1 arquivo, 9 áreas de alteração.**

---

## 6. VALIDAÇÃO

| Critério | Status |
|---|---|
| Hero visualmente equilibrado (texto e carrossel no mesmo eixo) | ✅ `align-items: start` |
| Foto continua sendo protagonista | ✅ Mantido da Sprint 5.6.2 |
| Texto não compete com o carrossel | ✅ Reduzido na Sprint 5.6.1 |
| Botões alinhados (mesma altura, mesmo baseline) | ✅ `line-height: 1` + `inline-flex; align-items: center` |
| Clicar em "Ler esta história" abre modal com história completa | ✅ Modal implementado com `fullStory` |
| Modal fecha com ESC | ✅ `keydown` listener |
| Modal fecha clicando fora | ✅ `click` listener verifica `e.target === modal` |
| Modal fecha com botão × | ✅ Botão com `aria-label="Fechar história"` |
| Foco volta ao botão que abriu o modal | ✅ `lastFocus.focus()` |
| Trap de foco dentro do modal | ✅ Implementado com Tab/Shift+Tab |
| CTA primário do modal leva ao app | ✅ `Começar a história da minha família` → `https://aeterna.streamlit.app/` |
| CTA secundário do modal fecha o modal | ✅ Botão "Fechar" |
| 8 histórias completas adicionadas | ✅ Campo `fullStory` em cada story |
| Modal responsivo (desktop, notebook, mobile) | ✅ Regras em 620px |

---

## 7. COMO TESTAR

1. Abrir `D:\aeterna\index.html` no navegador
2. Verificar que o Hero está visualmente equilibrado (texto e carrossel começam no mesmo eixo)
3. Verificar que o carrossel funciona (setas, dots, autoplay)
4. Clicar em **"Ler esta história"** em qualquer slide
5. Verificar que o modal abre com a história completa, título, data, pessoas, tags
6. Verificar que o modal pode ser fechado com:
   - Botão × (canto superior direito)
   - Botão "Fechar" (rodapé)
   - Tecla ESC
   - Clique fora do diálogo
7. Verificar que o foco volta para o botão "Ler esta história" após fechar
8. Verificar que o CTA **"Começar a história da minha família"** leva ao app (`aeterna.streamlit.app/`)
9. Testar no mobile (DevTools → modo responsivo)

---

**Fim da Sprint 5.6.3 — Lapidação final do Hero Vivo.**
