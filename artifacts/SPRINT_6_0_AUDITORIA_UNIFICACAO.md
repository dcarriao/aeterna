# SPRINT 6.0 — AUDITORIA ESTRATÉGICA DE ALINHAMENTO

> Sprint fundadora da Fase 6 (Unificação do Produto). Diferente das sprints anteriores que alteravam código ou conteúdo, esta sprint é exclusivamente de auditoria, arquitetura e planejamento. Nenhuma funcionalidade foi alterada. Todas as divergências foram documentadas para sprints futuras.

---

## Critério de sucesso

> Se uma pessoa navegar pelo site e depois abrir o aplicativo, ela sentirá que entrou exatamente no mesmo produto?

---

## Auditoria 1 — Funcionalidades

Matriz completa em `MATRIZ_SITE_APP.md`.

**Resumo:** 15 funcionalidades estão alinhadas entre site e app. 2 divergências internas do app persistem (não visíveis na Landing). 6 funcionalidades do app não são comunicadas na Landing. 1 funcionalidade (Blog) pertence exclusivamente ao site.

---

## Auditoria 2 — Linguagem

### 2.1 Comparação de nomenclaturas

| Funcionalidade | Landing (index.html) | App (sidebar) | App (heading/conteúdo) | Status |
|---|---|---|---|---|
| Tela inicial | "Início" (hero) | "Início" | `render_inicio` | ✅ Alinhado |
| Minha História | "Minha História" | "📖 Minha História" | `render_minha_historia` | ✅ Alinhado |
| Curador de Histórias | "O Curador" / "Curador de Histórias" | "Curador de Histórias" | `render_assistente` / `render_curador_memoria_primeiro` | ✅ Alinhado |
| Pessoas | "Pessoas" | "👥 Pessoas" | `render_contatos` | ✅ Alinhado |
| Memorial | "Memorial" | "🤍 Memorial" | `render_memoriais_lista` | ✅ Alinhado (heading: "Memorial") |
| Compartilhadas comigo | "Compartilhadas comigo" | "🤝 Compartilhadas Comigo" | `render_historias_compartilhadas_lista` | ✅ Alinhado (diferença de capitalização irrelevante) |
| Novidades | "Novidades" | "🔔 Novidades" | `render_novidades` | ✅ Alinhado |
| Contribuições | — | "✨ Contribuições" | `render_contribuicoes_pendentes` | ✅ Alinhado (não comunicado na Landing) |
| Fotos | "Fotos" | "Fotos" (no expander) | `render_fotos` | ✅ Alinhado |
| Vídeos | "Vídeos" | "Vídeos" (no expander) | `render_videos` | ✅ Alinhado |
| Quem Sou Eu | "Quem Sou Eu" | "Quem Sou Eu" (no expander) | ⚠️ Heading `app.py:2784` diz **"Minha Essência"** | ⚠️ Divergência |
| Mensagens para o Futuro | "Mensagens para o Futuro" | "Mensagens para o Futuro" | `render_agendamentos` | ✅ Alinhado |
| Cofre | "Cofre" | "Cofre" (no expander) | ⚠️ Heading `app.py:3787` diz **"Cofre Digital"** | ⚠️ Divergência |
| Planos | "Planos" | "Meu plano" | `render_planos` | ✅ Aceitável (contextos diferentes) |
| Linha do Tempo | "Linha do Tempo" | (tab dentro de Minha História) | `render_linha_tempo` | ✅ Alinhado |

### 2.2 Divergências de linguagem identificadas

#### Críticas (impacto na percepção de unidade)

| # | Local | Problema | Evidência | Severidade |
|---|---|---|---|---|
| L1 | App heading `app.py:2784` | "Minha Essência" vs "Quem Sou Eu" (sidebar) | Linha: `st.markdown("<h3 style='...'>🧬 Minha Essência</h3>"` | **Média** — usuário vê "Quem Sou Eu" no menu e "Minha Essência" no conteúdo |
| L2 | App heading `app.py:3787` | "Cofre Digital" vs "Cofre" (sidebar) | Linha: `st.markdown("<h3 style='...'>🔐 Cofre Digital</h3>"` | **Média** — mesma divergência |
| L3 | App heading `components/memorial.py:287` | "Memorial de Legados" vs "Memorial" (sidebar) | Heading: "Memorial de Legados" | **Baixa** — usuário vê "Memorial" no menu, heading diferente ao entrar |

#### Médias (impacto na comunicação)

| # | Local | Problema | Evidência |
|---|---|---|---|
| L4 | App footer `app.py:5696, 5875` | "aEterna — Memórias vivas para quem você ama" — não é uma frase oficial da marca e conflita com o posicionamento de "histórias de família" | O Brand Book não usa "memórias vivas" como slogan; o posicionamento oficial é "onde a história da sua família continua sendo escrita" |
| L5 | App `render_inicio` | Título "Início" — genérico, não comunica o valor da plataforma | Comparar com a Landing que diz "A história da sua família ainda está sendo escrita" |
| L6 | App `render_videos` heading | "📹 Vídeos da Minha História" — usa "Minha História" como nome da feature mas o sidebar usa "Vídeos" | Consistente com o menu, mas poderia ser só "Vídeos" |

#### Baixas (cosméticas)

| # | Local | Problema |
|---|---|---|
| L7 | App `render_cofre` | Usa "Cofre Digital" no heading — resquício de nomenclatura antiga |
| L8 | App sidebar | "Compartilhadas Comigo" com "C" maiúsculo em "Comigo" — diferença de capitalização da Landing |

### 2.3 CTAs e botões

| Contexto | Landing | App | Alinhado? |
|---|---|---|---|
| CTA principal | "Descobrir uma história" / "Começar a contar a minha" | Login/Cadastro | ✅ Fluxo contínuo |
| CTA secundário (Hero) | "Ler esta história" (modal) | — (não existe no app) | ✅ Modal é exclusivo da Landing |
| CTA "Começar a história da minha família" | Modal de história | Login/Cadastro | ✅ Alinhado (mesma ação) |
| Login | Link para `aeterna.streamlit.app` | `render_login_compacto` | ✅ Alinhado |
| Cadastro | Mesmo link | `fazer_cadastro` | ✅ Alinhado |

---

## Auditoria 3 — Fluxo

### 3.1 Fluxo completo mapeado

Fluxo completo em `JORNADA_DO_USUARIO.md`.

### 3.2 Quebras de continuidade

| # | Ponto | Quebra | Impacto | Prioridade |
|---|---|---|---|---|
| Q1 | Landing → App | O CTA leva direto ao app sem tela de transição. O visitante "pula" do marketing para o produto sem mediação. | Baixo — aceitável para SaaS | Média |
| Q2 | App → Landing | **Não há link do app para o site.** O usuário logado não consegue acessar o blog, a FAQ, a página "Sobre" ou a política de privacidade a partir do app. | **Alto** — o usuário fica preso no app sem acesso a conteúdo institucional | **Crítica** |
| Q3 | App → Blog | O blog (`/insights/`) não tem link no app. Usuário precisa abrir nova aba e digitar a URL. | Médio — conteúdo editorial fica inacessível | Alta |
| Q4 | App → Páginas legais | Política de privacidade (`/legais/`) não tem link no app. | Médio — pode ser exigido por lei (LGPD) | Alta |
| Q5 | Landing → Login visitante | A Landing não comunica que existe login via chave de acesso (visitante). | Baixo — funcionalidade para quem já recebeu convite | Média |

---

## Auditoria 4 — Navegação

### 4.1 Site (Landing)

```
Header: [Logo] [Início] [O problema] [O Curador] [A plataforma] [Memorial] [FAQ] [CTA]
Body:  23 seções em scroll vertical
Footer: [Logo] [Navegação] [Plataforma (CTA, email, Insights)]
```

**Características:**
- Navegação linear, scroll-based
- 6 links no menu principal
- Menu hamburger em mobile
- Links âncora internos (#id)
- 1 CTA externo para o app (`aeterna.streamlit.app`)

### 4.2 App (Streamlit)

```
Sidebar: [Início] [Minha História] [Pessoas] [Memorial] [Compartilhadas Comigo] [Novidades] [Contribuições]
         [Expander: Curador, Fotos, Vídeos, Quem Sou Eu, Mensagens Futuras, Cofre, Meu plano]
         [Plano card]
         [Logout]
Body:  Página renderizada conforme seleção
```

**Características:**
- Navegação por sidebar com botões
- 7 itens visíveis + 7 em expander
- Planos como card na sidebar (não como item de navegação primário)
- Logout na sidebar

### 4.3 Divergências de navegação

| # | Aspecto | Site | App | Impacto |
|---|---|---|---|---|
| N1 | Funcionalidades "Mais" | Todas visíveis em cards/seções | 7 features em expander (não visíveis de imediato) | Usuário pode não descobrir features no app |
| N2 | Logout | Não aplicável (site é público) | Na sidebar, sem confirmação | Aceitável |
| N3 | Voltar para o site | N/A | **Não existe** | Usuário preso no app |
| N4 | Blog | Link no footer | **Não existe** | Conteúdo editorial inacessível |
| N5 | FAQ | Seção na Landing | **Não existe** | Usuário sem suporte self-service |

---

## Auditoria 5 — Identidade Visual

| Elemento | Site | App | Alinhado? |
|---|---|---|---|
| Cor primária (gold) | `#d4af37` / `#f2c572` / `#f8dc92` | `#d4af37` / `#f2c572` | ✅ |
| Cor de fundo | `#080014` (radial gradients) | `#080014` via `inject_custom_css` | ✅ |
| Gradiente de fundo | Radial + linear gradient | Apenas linear (`135deg, #f5f5f5, #e8f5e9`) | ⚠️ App tem fundo mais claro que o site |
| Tipografia | Inter + Cormorant Garamond | Inter (via CSS injection) | ✅ (Cormorant aparece apenas em títulos específicos no app) |
| Ícones | Emoji (📖, ✨, 🔎) | Emoji (mesmos no sidebar) | ✅ |
| Botões | Gradiente dourado, border-radius 15px | Gradiente dourado (via CSS injection) | ✅ |
| Cards | Borda 1px rgba(gold, .22-.28), bg semi-transparent | Classe `.ae-card` replica o mesmo estilo | ✅ |
| Glassmorphism | `backdrop-filter: blur(16px) saturate(140%)` no carrossel | Não usado no app | ⚠️ App não copia glassmorphism do site |
| Animações | `ae-soft-pulse`, `ae-glow-drift`, `ae-fade-up` | Nenhuma equivalente | ⚠️ App é estático (limitação do Streamlit) |
| Sombras | `box-shadow: 0 30px 90px rgba(0,0,0,.38)` | Similar | ✅ |
| Hero | Carrossel com 8 histórias + glassmorphism card | Apenas `st.image` do logo + login | ⚠️ App não tem hero visual comparável |

### 5.1 Observações visuais

1. O app usa um fundo mais claro (gradiente `#f5f5f5 → #e8f5e9`) que conflita com o fundo escuro do site (`#080014`). O fundo claro é uma herança do Streamlit padrão. O `inject_custom_css` tenta escurecer, mas não replica o mesmo tom de roxo escuro do site.
2. O app não usa Cormorant Garamond (fonte serifada dos títulos) de forma consistente. Apenas alguns títulos específicos a utilizam.
3. O app não tem glassmorphism (backdrop-filter), que é uma marca visual importante do site (Hero card, modal).
4. Animações do site (pulse, glow-drift, fade-up) não existem no app — limitação técnica do Streamlit.

---

## Auditoria 6 — Hierarquia

### 6.1 O que pertence ao site

| Item | Justificativa |
|---|---|
| Apresentação do produto (Landing) | Descoberta, marketing, conversão |
| Blog / Insights (`/insights/`) | Conteúdo editorial, SEO |
| FAQ | Suporte self-service |
| Páginas legais (`/legais/`) | LGPD, termos de uso |
| SEO (sitemap, robots, Schema.org) | Indexação |

### 6.2 O que pertence ao app

| Item | Justificativa |
|---|---|
| Minha História | Criação e edição de conteúdo |
| Curador de Histórias | Interação guiada |
| Fotos / Vídeos | Upload e gestão de mídia |
| Pessoas | Cadastro e gestão de contatos |
| Linha do Tempo | Visualização cronológica |
| Memorial | Gestão de memoriais |
| Compartilhadas comigo | Histórias de outros |
| Novidades | Notificações |
| Contribuições | Moderação |
| Mensagens para o Futuro | Agendamento |
| Cofre | Armazenamento criptografado |
| Planos | Assinatura e pagamento |
| Login / Cadastro | Autenticação |
| Modo visitante | Acesso de convidados |

### 6.3 O que pertence a ambos

| Item | Justificativa |
|---|---|
| Memorial | Site apresenta o conceito; app entrega a funcionalidade |
| Curador | Site explica o conceito com exemplo; app entrega a interação |
| Linha do Tempo | Site mostra preview visual; app entrega a timeline funcional |

### 6.4 Problemas de hierarquia

| # | Problema | Evidência |
|---|---|---|
| H1 | App sidebar tem "Meu plano" como item de navegação, mas não comunica claramente que é uma seção de planos/upgrade | O plano aparece como status card e link separado |
| H2 | O app não tem um "Sobre" institucional acessível | A função `render_sobre` existe (`app.py:3922-3950`) mas não está no sidebar principal |
| H3 | Modo visitante não tem navegação clara | Visitante vê abas (Sobre, Histórias, Aprendizados, Explorar) mas não tem sidebar com features |

---

## Auditoria 7 — Jornada

Fluxograma completo em `JORNADA_DO_USUARIO.md`.

---

## Auditoria 8 — Coerência

### Se removermos o logotipo, a Landing e o aplicativo ainda parecem o mesmo produto?

**Parcialmente sim, com ressalvas.**

**Pontos de coerência:**
- Paleta de cores (gold + roxo escuro) é consistente entre ambos
- Ícones emoji são os mesmos
- Botões com gradiente dourado
- Cards com borda dourada e bg semi-transparente
- Nomenclatura das features é a mesma (após correções da Sprint 6)
- Tom de voz (calmo, respeitoso, narrativo) é consistente
- Conceito de "histórias de família" atravessa ambos

**Pontos de divergência:**
- Fundo do app é mais claro (gradiente verde-claro) vs fundo escuro do site — sem o logo, um usuário não assumiria que é o mesmo produto
- App não tem glassmorphism ou backdrop-filter (marca visual do site)
- App não tem a tipografia Cormorant Garamond de forma consistente
- Hero do site (carrossel de histórias) não tem equivalente no app
- Footer do app ("aEterna — Memórias vivas para quem você ama") não está alinhado com o tom do Brand Book

**Veredito:** A coerência visual é **média-alta**, mas a diferença de fundo (claro vs escuro) é a maior barreira para que os dois sejam percebidos como o mesmo produto sem o logotipo.

---

## Auditoria 9 — Oportunidades

### 9.1 Críticas (resolver antes da Fase 6)

| # | Oportunidade | Problema | Impacto | Evidência |
|---|---|---|---|---|
| O1 | Unificar fundo do app com o site | App usa fundo claro (`#f5f5f5 → #e8f5e9`) enquanto o site usa fundo escuro (`#080014`) | Alto — quebra a identidade visual | `inject_custom_css()` vs Landing CSS |
| O2 | Adicionar link do app para o site | Usuário logado não consegue acessar blog, FAQ, páginas legais | Alto — experiência fechada | `render_sidebar_principal()` não tem link externo |
| O3 | Adicionar link do app para o blog | Conteúdo editorial inacessível para usuários logados | Alto | Footer do app não tem link para `/insights/` |

### 9.2 Altas (resolver na Fase 6)

| # | Oportunidade | Problema | Impacto | Evidência |
|---|---|---|---|---|
| O4 | Unificar heading "Minha Essência" → "Quem Sou Eu" | `app.py:2784` usa nome diferente do sidebar | Médio — confunde usuário em navegação profunda | `render_preferencias()` heading |
| O5 | Unificar heading "Cofre Digital" → "Cofre" | `app.py:3787` usa nome antigo | Médio | `render_cofre()` heading |
| O6 | Unificar heading "Memorial de Legados" → "Memorial" | `memorial.py:287` usa nome diferente | Médio | `render_memoriais_lista()` heading |
| O7 | Adicionar CTA "Sobre a aEterna" no app | App não tem página institucional | Médio — novo usuário quer saber sobre a empresa | `render_sobre()` existe mas não está no menu |

### 9.3 Médias (planejar)

| # | Oportunidade | Problema | Impacto |
|---|---|---|---|
| O8 | Adicionar tipografia Cormorant Garamond no app | Títulos do app usam Inter, não a serifada da marca | Médio — consistência visual |
| O9 | Adicionar glassmorphism em cards do app | App não tem backdrop-filter, diferentemente do site | Baixo — limitação técnica do Streamlit |
| O10 | Comunicar login visitante na Landing | Funcionalidade existe no app mas não é comunicada | Baixo — apenas para quem recebe convite |
| O11 | Adicionar funcionalidades escondidas do expander na Landing | App tem 7 features no expander "Mais" que podem não ser descobertas | Médio — descoberta de produto |

### 9.4 Baixas (nice to have)

| # | Oportunidade | Problema |
|---|---|---|
| O12 | Animações no app | App é mais estático que o site |
| O13 | Footer do app alinhado com Brand Book | "Memórias vivas" não é frase oficial |
| O14 | Reduzir capitalização "Compartilhadas Comigo" → "Compartilhadas comigo" | Diferença cosmética |

---

## Plano de Sprints para Fase 6

### Sprint 6.1 — Unificação Visual do App
- Escurecer fundo do app para replicar `#080014`
- Adicionar Cormorant Garamond em títulos
- Adicionar glassmorphism onde possível
- Alinhar footer com Brand Book

### Sprint 6.2 — Navegação Cruzada
- Adicionar link do app para Landing + Blog + Páginas legais
- Adicionar "Sobre a aEterna" no sidebar
- Adicionar FAQ no app (ou link para a FAQ da Landing)

### Sprint 6.3 — Correção de Nomenclatura Interna
- "Minha Essência" → "Quem Sou Eu" (`app.py:2784`)
- "Cofre Digital" → "Cofre" (`app.py:3787`)
- "Memorial de Legados" → "Memorial" (`memorial.py:287`)

### Sprint 6.4 — Nova Jornada de Primeiro Uso
- Revisar onboarding do app
- Criar tela de boas-vindas pós-cadastro
- Melhorar descoberta de features do expander

---

## Checklist de Sucesso

- [x] **Auditoria 1 (Funcionalidades):** Matriz completa criada em `MATRIZ_SITE_APP.md`
- [x] **Auditoria 2 (Linguagem):** 8 divergências documentadas (2 críticas/médias, 6 baixas)
- [x] **Auditoria 3 (Fluxo):** 5 quebras de continuidade identificadas, sendo 1 crítica
- [x] **Auditoria 4 (Navegação):** 5 divergências documentadas
- [x] **Auditoria 5 (Identidade Visual):** Coerência média-alta; 4 divergências menores
- [x] **Auditoria 6 (Hierarquia):** Divisão clara site vs app; 3 problemas documentados
- [x] **Auditoria 7 (Jornada):** Fluxograma completo em `JORNADA_DO_USUARIO.md`
- [x] **Auditoria 8 (Coerência):** Veredito: coerente sem logo, com ressalvas
- [x] **Auditoria 9 (Oportunidades):** 14 oportunidades classificadas (3 críticas, 4 altas, 4 médias, 3 baixas)
- [x] **Plano de Sprints:** 4 sprints propostas para Fase 6

---

## Documentos complementares

- `MATRIZ_SITE_APP.md` — Matriz completa de funcionalidades
- `JORNADA_DO_USUARIO.md` — Fluxograma completo da jornada
- `ARQUITETURA_DA_PLATAFORMA.md` — Mapa oficial da plataforma

---

> **Ao final da Sprint 6.0, existe um mapa completo da plataforma. Qualquer pessoa que entrar na equipe conseguirá responder o que pertence ao site, o que pertence ao app, como o usuário entra, como continua e como retorna — sem perguntar ao fundador.**
