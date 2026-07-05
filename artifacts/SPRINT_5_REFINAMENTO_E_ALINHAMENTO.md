# SPRINT 5 — REFINAMENTO, SIMPLIFICAÇÃO E ALINHAMENTO COM O APLICATIVO

> Sprint dedicada a **tirar, simplificar e alinhar**. A Landing e as páginas internas foram refinadas para reduzir redundâncias, alinhar nomenclaturas com o aplicativo e tornar a leitura mais leve, preservando toda a narrativa construída nas Sprints 1-4.

---

## 1. AUDITORIA DE ALINHAMENTO SITE × APLICATIVO

### 1.1 Nomenclaturas

| Funcionalidade | Nome na Landing (Sprint 4) | Nome no App (código) | Status | Ação |
|---|---|---|---|---|
| Memorial | Memorial Vivo | Memorial (sidebar) / Memorial (conteúdo) | ⚠️ Divergente | Renomear para **Memorial** |
| Quem Sou Eu / Essência | Minha Essência | Quem Sou Eu (sidebar) / Minha Essência (conteúdo) | ⚠️ Divergente | Renomear para **Quem Sou Eu** (alinhamento com menu) |
| Compartilhamento | Compartilhamento Familiar | Compartilhadas comigo (sidebar) | ⚠️ Divergente | Renomear para **Compartilhadas comigo** |
| Minha História | Minha História | Minha História | ✅ Consistente | Manter |
| Curador de Histórias | Curador / Curador de Histórias | Curador de Histórias | ✅ Consistente | Manter |
| Explorador de Histórias | Explorador de Histórias | Explorador de Histórias (`utils/assistente_ia.py:563`) | ✅ Consistente | Manter |
| Linha do Tempo | Linha do Tempo | Linha do Tempo | ✅ Consistente | Manter |
| Pessoas | Pessoas | Pessoas | ✅ Consistente | Manter |
| Fotos | Fotos | Fotos | ✅ Consistente | Manter |
| Vídeos | Vídeos | Vídeos | ✅ Consistente | Manter |
| Contribuições | Contribuições | Contribuições | ✅ Consistente | Manter |
| Mensagens para o Futuro | Mensagens para o Futuro | Mensagens para o Futuro | ✅ Consistente | Manter |
| Cofre Digital | Cofre Digital | Cofre Digital | ✅ Consistente | Manter |
| Planos | Planos | Meu plano | ⚠️ Divergente | Aceitável (Planos é mais claro para landing) |
| Novidades | (não comunicado) | Novidades | ❌ Ausente | Aceitável (detalhe operacional) |

### 1.2 Funcionalidades

Todas as funcionalidades comunicadas na Landing existem no aplicativo. Nenhuma promessa incorreta foi identificada.

### 1.3 Identidade visual

- **Landing:** paleta roxa/dourada (`#080014`, `#d4af37`, `#f2c572`) com tipografia Inter + Cormorant Garamond.
- **App:** mesmo gradiente roxo/dourado no header (`styles/theme.py:20`), mas com elementos verdes legados (`app.py:97, 113, 126`).
- **Decisão:** Landing está consistente. A divergência está no app, que mantém resquícios verdes de versões anteriores. A Landing não foi alterada para refletir essa divergência.

### 1.4 Linguagem e tom

A Landing mantém o tom sóbrio e acolhedor construído nas Sprints 1-4. A Política de Privacidade e os Insights também estão alinhados.

### 1.5 Páginas internas

| Página | Status | Ação |
|---|---|---|
| `legais/politicaprivacidade.html` | ✅ Consistente com a Landing | Nenhuma |
| `insights/index.html` | ⚠️ Link quebrado (`.htm` em vez de `.html`) | Corrigido |
| `insights/dom-pedro-ii-bisavo.html` | ✅ Consistente | Nenhuma |
| `insights/milhares-de-fotos-poucas-historias.html` | ✅ Consistente | Nenhuma |
| `insights/dia-mais-feliz-do-seu-avo.html` | ✅ Consistente | Nenhuma |
| `blog.html` | ⚠️ Linka para `/artigos/` (órfão) | Corrigido para `/insights/` |
| `artigos/sabemos-mais-...` | ⚠️ Conteúdo duplicado de `/insights/dom-pedro-ii-bisavo.html` | Mantido (decisão de sprint separada) |

---

## 2. CONTEÚDO REMOVIDO OU SIMPLIFICADO

### 2.1 Seção "Como a aEterna resolve" — REMOVIDA

- **Linhas removidas:** 2650-2687 (37 linhas)
- **Motivo:** Sobrepunha-se à seção "Como funciona" (4 passos) com um fluxo de 5 etapas muito similar (você vive → registra → Curador ajuda → família complementa → história cresce). O "Como funciona" é mais concreto e inclui o exemplo de timeline, o que torna a seção anterior redundante.
- **Benefício:** Reduz a sensação de "já li isso" que o visitante tinha ao chegar no "Como funciona".

### 2.2 Visual-flow de Compartilhamento Familiar — REMOVIDO

- **Linhas removidas:** 3065-3095 (30 linhas)
- **Motivo:** Redundante com o family-flow (5 itens com ícones ＋ ＝) que já está em "A família participa" e com a family-story (4 passos do Natal de 1998) abaixo. O visual-flow era uma terceira explicação do mesmo conceito.
- **Benefício:** Reduz a contagem de representações do mesmo conceito de 3 para 2.

### 2.3 "Como tudo funciona junto" — REDUZIDO de 8 para 4 passos

- **Linhas removidas:** ~30 linhas
- **Motivo:** 8 etapas lineares eram excessivas. Reduzidas para 4 etapas focadas: registrar → família complementa → linha do tempo → legado cresce.
- **Benefício:** Mais escaneável. Mantém o ecossistema visual (grid 5x2) abaixo como complemento.

### 2.4 "As pequenas histórias" — REDUZIDO de 6 para 4 cards

- **Linhas removidas:** ~14 linhas
- **Motivo:** 6 cards de patrimônio invisível eram redundantes entre si. Mantidos os 4 mais universais (bolo, música, foto, conselho). Removidos "apelido" e "objeto antigo" por serem mais abstratos.
- **Benefício:** Mantém a sensação de "todo mundo tem isso" sem cansar o visitante.

### 2.5 Micro-story em "A família participa" — REMOVIDO

- **Linhas removidas:** 3 linhas
- **Motivo:** A seção "A família participa" tinha 2 micro-stories ("Uma história quase nunca está pronta" e "Cada pessoa cadastrada vira um nó"). O segundo era redundante com o people grid logo abaixo.
- **Benefício:** Fecha a seção de forma mais limpa.

### 2.6 Copy de "Linha do Tempo showcase" e "Pessoas showcase" — SIMPLIFICADO

- **Linhas removidas:** ~8 linhas
- **Motivo:** Os 2 parágrafos de copy foram consolidados em 1 parágrafo mais direto.
- **Benefício:** Foco na tela (que é o que importa), menos texto.

**Total de linhas removidas na Landing: ~113 linhas** (3.221 → 3.108).

---

## 3. MELHORIAS DE CLAREZA

| Mudança | Como reduz a carga cognitiva |
|---|---|
| Remoção de "Como a aEterna resolve" | Elimina uma seção inteira que repetia "Como funciona" com menos detalhe. O visitante chega mais rápido à seção prática. |
| Remoção do visual-flow de compartilhamento | O conceito de "compartilhar → contribuir → aprovar" já estava em duas outras formas na mesma seção. Agora aparece uma vez como family-flow + uma vez como family-story. |
| Redução de 8 para 4 passos em "Como tudo funciona junto" | O grid 5x2 de ecossistema já mostra todas as features. O fluxo linear agora é mais enxuto. |
| Redução de 6 para 4 cards em "As pequenas histórias" | Mantém a sensação "todo mundo tem isso" sem que o visitante precise processar 6 exemplos. |
| Renomeação "Memorial Vivo" → "Memorial" | Alinha com o menu do app. Visitante que abrir o app reconhece a mesma seção. |
| Renomeação "Minha Essência" → "Quem Sou Eu" | Alinha com o menu do app. Linguagem mais direta. |
| Renomeação "Compartilhamento Familiar" → "Compartilhadas comigo" | Alinha com o menu do app. Linguagem mais centrada no usuário. |
| Remoção de micro-story redundante | Reduz a sensação de "já ouvi isso". |

**Resultado:** A Landing agora tem 17 seções de conteúdo + 3 inter-quotes + 1 quote central + 1 CTA final = **22 elementos verticais**, vs. 23 seções + 5 elementos = 28 antes da Sprint 5. Redução de ~21% no número de elementos.

---

## 4. REVISÃO DAS PÁGINAS INTERNAS

### 4.1 `legais/politicaprivacidade.html`

- **Status:** ✅ Consistente
- **Observação:** O texto menciona "preservar memórias familiares" e "aEterna não utiliza histórias, mensagens, fotografias, vídeos ou documentos privados para treinamento de modelos de IA sem autorização expressa". Coerente com o tom da Landing.
- **Ação:** Nenhuma.

### 4.2 `insights/index.html`

- **Problema:** Linha 265 — link para `/insights/dia-mais-feliz-do-seu-avo.htm` (extensão errada).
- **Ação:** Corrigido para `.html`.
- **Observação adicional:** Os 3 cards do índice de artigos repetem o mesmo padrão (tag, h2, p, btn) e estão consistentes com a Landing.

### 4.3 `insights/dom-pedro-ii-bisavo.html`, `milhares-de-fotos-poucas-historias.html`, `dia-mais-feliz-do-seu-avo.html`

- **Status:** ✅ Consistente
- **Observação:** Os artigos usam a mesma paleta e tipografia da Landing. O tom é alinhado (preservação, memórias, legado).
- **Ação:** Nenhuma.

### 4.4 `blog.html`

- **Problema:** Linka para `/artigos/sabemos-mais-sobre-dom-pedro-ii-do-que-sobre-nosso-bisavo.html`, que é um diretório órfão.
- **Ação:** Corrigido para `/insights/dom-pedro-ii-bisavo.html`.
- **Observação:** O `blog.html` é uma página legada simples. Mantida para evitar quebrar links externos.

### 4.5 `artigos/sabemos-mais-sobre-dom-pedro-ii-do-que-sobre-nosso-bisavo.html`

- **Problema:** Conteúdo duplicado de `insights/dom-pedro-ii-bisavo.html`. Causa problema de conteúdo duplicado.
- **Decisão:** Mantido nesta sprint (remoção de arquivos é decisão para sprint dedicada, conforme observação do usuário: "registrei no backlog de longo prazo"). O link no `blog.html` foi redirecionado para `/insights/`.

---

## 5. HIERARQUIA DAS INFORMAÇÕES

### 5.1 Essencial (acima da dobra ou nas primeiras 3 seções)

| Seção | Por que é essencial |
|---|---|
| Hero | Primeira impressão. h1 + h2 do problema + CTA principal. |
| O problema | Compreensão imediata do problema em 30s. |
| Por que as histórias desaparecem | Exemplos concretos que validam o problema. |

### 5.2 Importante (seções 4-10)

| Seção | Por que é importante |
|---|---|
| Imagine daqui a 30 anos | Mostra o valor futuro. |
| Manifesto | Posiciona a aEterna como plataforma. |
| As pequenas histórias | Ancora emocional. |
| Como funciona | Passos práticos. |
| O Curador | Apresenta a feature diferenciadora. |
| Fotos e Vídeos | Demonstra a transformação. |
| A família participa | Mostra a colaboração. |

### 5.3 Complementar (seções 11+)

| Seção | Por que é complementar |
|---|---|
| Tudo o que a plataforma oferece | Grade completa de features. |
| Mensagens para o Futuro | Demonstração visual. |
| Cofre Digital | Demonstração visual. |
| Como tudo funciona junto | Integração do ecossistema. |
| Memorial | Continuação da história. |
| Privacidade | Segurança. |
| FAQ | Dúvidas específicas. |
| CTA Final | Ação final. |

**Observação:** O "Manifesto" foi mantido em "Importante" porque a Landing da aEterna se diferencia de outras plataformas de memórias por ser uma plataforma integrada, não um aplicativo de histórias isolado.

---

## 6. JORNADA DO VISITANTE

| Tempo | Seção | O que o visitante entende |
|---|---|---|
| **0-5s** | Hero | Há um produto. O H1 fala de "fotos vs histórias" — uma pergunta provocativa. |
| **5-15s** | Hero copy + CTAs | A aEterna preserva histórias antes que desapareçam. Há um CTA claro. |
| **15-30s** | O problema | "As fotos sobrevivem. As histórias, quase nunca." — o problema é claro. |
| **30-60s** | Por que as histórias desaparecem | 3 exemplos concretos (foto sem contexto, vídeo sem história, lugar sem significado). O visitante se reconhece. |
| **60-90s** | Imagine daqui a 30 anos | Salto temporal: hoje → neto. O valor futuro fica claro. |
| **90-120s** | Manifesto | "Mais do que um lugar para escrever histórias" — a aEterna é uma plataforma. |
| **2-3min** | Como funciona + O Curador + Fotos e Vídeos + A família | Como a plataforma funciona na prática. |
| **3-4min** | Tudo o que oferece + Mensagens + Cofre + Integração | Catálogo de features. |
| **4-5min** | Memorial | A continuação. |
| **5min+** | Privacidade + FAQ | Detalhes para quem quer saber mais. |

**Observação:** A hierarquia permite que o visitante saia a qualquer momento com uma compreensão adequada do produto.

---

## 7. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | 2650-2687 (remoção) | Removida seção "Como a aEterna resolve" |
| `D:\aeterna\index.html` | 3065-3095 (remoção) | Removido visual-flow de compartilhamento |
| `D:\aeterna\index.html` | 3285-3327 (redução) | "Como tudo funciona junto" de 8 para 4 passos |
| `D:\aeterna\index.html` | 2674-2710 (redução) | "As pequenas histórias" de 6 para 4 cards |
| `D:\aeterna\index.html` | 3037-3039 (remoção) | Micro-story redundante em "A família participa" |
| `D:\aeterna\index.html` | 2779-2801 (simplificação) | Copy do "Linha do Tempo showcase" |
| `D:\aeterna\index.html` | 2990-2999 (simplificação) | Copy do "Pessoas showcase" |
| `D:\aeterna\index.html` | ~5 ocorrências (renomeação) | "Memorial Vivo" → "Memorial" |
| `D:\aeterna\index.html` | 1 ocorrência (renomeação) | "Minha Essência" → "Quem Sou Eu" |
| `D:\aeterna\index.html` | 1 ocorrência (renomeação) | "Compartilhamento Familiar" → "Compartilhadas comigo" |
| `D:\aeterna\insights\index.html` | 265 | Link corrigido: `.htm` → `.html` |
| `D:\aeterna\blog.html` | 19 | Link corrigido: `/artigos/` → `/insights/` |

**Total: 3 arquivos alterados. Nenhuma imagem, CSS estrutural, SEO, Schema.org, manifest, sitemap, robots ou JavaScript estrutural foi alterado.**

---

## 8. VALIDAÇÃO

### 8.1 O site e o aplicativo parecem o mesmo produto?

**Sim.** Nomenclaturas alinhadas (Memorial, Quem Sou Eu, Compartilhadas comigo, Minha História, Pessoas, Linha do Tempo, Curador de Histórias, Explorador de Histórias, Fotos, Vídeos, Contribuições, Mensagens para o Futuro, Cofre Digital). Visitante que abrir o app reconhece as mesmas seções.

### 8.2 A Landing ficou mais leve sem perder conteúdo importante?

**Sim.** Reduzida de 3.221 para 3.108 linhas (3.5%). Reduzida de 28 para 22 elementos verticais (21%). Nenhuma feature foi removida. Os exemplos concretos (Natal de 1998, almoço na casa da avó, passeio de bicicleta) foram preservados.

### 8.3 A ordem das informações ficou mais eficiente?

**Sim.** A seção "Como a aEterna resolve" (que era redundante com "Como funciona") foi removida. O visitante agora passa diretamente do Manifesto (posicionamento) para "As pequenas histórias" (ancoragem emocional) e depois para "Como funciona" (passos práticos).

### 8.4 Houve redução de redundâncias?

**Sim.** "Compartilhamento Familiar" estava comunicado de 3 formas na mesma seção (family-flow + visual-flow + family-story). Agora está em 2 formas (family-flow + family-story). "Como tudo funciona junto" foi reduzido de 8 para 4 passos.

### 8.5 O visitante consegue entender rapidamente o valor da plataforma?

**Sim.** Em 30s: "As fotos sobrevivem. As histórias, quase nunca." Em 60s: 3 exemplos concretos + salto temporal para o futuro. Em 2min: como a plataforma funciona. A hierarquia permite saída precoce com compreensão adequada.

### 8.6 Existe alguma promessa no site que ainda não é suportada pelo aplicativo?

**Não.** Verificação completa contra o código do app:

| Funcionalidade prometida | Existe no app? | Evidência |
|---|---|---|
| Minha História | ✅ | `app.py:517-901` |
| Curador de Histórias | ✅ | `app.py:1296-1301` |
| Explorador de Histórias | ✅ | `app.py:1276, 2786, 5013` |
| Pessoas | ✅ | `app.py:2351-2782` |
| Fotos | ✅ | `app.py:1550-1752` |
| Vídeos | ✅ | `app.py:1307-1515` |
| Linha do Tempo | ✅ | `app.py:517-901` |
| Compartilhadas comigo | ✅ | `app.py:5070-5322` |
| Contribuições | ✅ | `app.py:4189-4353` |
| Memorial | ✅ | `components/memorial.py` |
| Mensagens para o Futuro | ✅ | `app.py:3480-3781` |
| Cofre Digital | ✅ | `app.py:3786-3919` |
| Planos | ✅ | `app.py:2886-3476` |
| Quem Sou Eu | ✅ | `app.py:2783-2880` |

---

## 9. PRINCÍPIOS APLICADOS

| Diretriz | Resposta |
|---|---|
| Não criar funcionalidades inexistentes | ✅ Nenhuma |
| Não remover funcionalidades importantes | ✅ Todas as features preservadas |
| Mostrar em vez de explicar (Sprint 4) | ✅ Mantido |
| Alinhar nomenclaturas com o app | ✅ 3 renomeações aplicadas |
| Cortar redundâncias | ✅ 6 simplificações aplicadas |
| Respeitar hierarquia essencial/importante/complementar | ✅ Seções reorganizadas |
| Não alterar SEO | ✅ Nenhuma alteração no `<head>` |
| Não alterar Schema.org | ✅ Nenhum `<script type="application/ld+json">` alterado |
| Não alterar manifest, robots, sitemap | ✅ Nenhuma |
| Não alterar JavaScript estrutural | ✅ Script de menu intocado |
| Não alterar performance | ✅ Nenhuma |
| Não alterar acessibilidade | ✅ Nenhuma |
| Não alterar páginas legais | ✅ `politicaprivacidade.html` não foi alterado em conteúdo |
| Manter SEO, performance, JavaScript estrutural | ✅ Todos preservados |

---

## 10. OBSERVAÇÕES PARA SPRINTS FUTURAS

- **Conteúdo duplicado:** `artigos/sabemos-mais-sobre-dom-pedro-ii-do-que-sobre-nosso-bisavo.html` é uma duplicata de `insights/dom-pedro-ii-bisavo.html`. Decidir entre remover ou redirecionar.
- **Tamanho da Landing:** mesmo com a simplificação, a Landing ainda tem ~3.100 linhas. Em sprints futuras, considerar dividir em múltiplas páginas (ex.: uma página de features, uma página sobre o Memorial).
- **Mobile UX:** apesar de o responsivo estar funcionando, a Landing ainda é longa para mobile. Considerar um menu de âncoras flutuante ou um "tabela de conteúdos" no topo.
- **Materiais para Google Play:** conforme registrado pelo usuário, os materiais para publicação na Play Store (vídeos e imagens promocionais) estão no backlog de longo prazo.

---

**Fim da Sprint 5 — Refinamento, simplificação e alinhamento com o aplicativo.**
