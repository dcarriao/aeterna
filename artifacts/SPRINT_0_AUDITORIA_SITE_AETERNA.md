# SPRINT 0 — AUDITORIA TÉCNICA E ESTRATÉGICA DO SITE DA aEterna

> Documento de auditoria baseado em evidências encontradas no código-fonte.
> Nenhuma alteração foi implementada. Nenhuma inferência foi utilizada sem comprovação.
> Itens não confirmados no código estão explicitamente sinalizados.

---

## 1. RESUMO EXECUTIVO

O repositório `D:\aeterna` é um **projeto Streamlit** (Python) acompanhado de um **conjunto de páginas HTML estáticas** servidas como site institucional em `aeternalegado.com.br`.

- O **aplicativo** (a plataforma) é `app.py` (5.881 linhas) e é hospedado em `https://aeterna.streamlit.app/` (evidência: `index.html:1145, 1161, 1348, 1492, 1515`; `.streamlit/secrets.toml:APP_URL`).
- O **site institucional** é composto por arquivos HTML soltos na raiz do projeto, com CSS e JavaScript embutidos em `index.html`. Não há framework JS, não há build, não há CSS externo.
- A Landing Page atual (`index.html`) é uma página de 1.549 linhas, com 14 seções de conteúdo, single-file, sem dependências externas além de Google Fonts.
- A plataforma (aplicativo) é um **sistema completo** de legado familiar com ~14 áreas funcionais (Minha História, Memorial, Pessoas, Curador de Histórias, Fotos, Vídeos, Mensagens para o Futuro, Cofre Digital, Planos etc.), mas o site comunica apenas um recorte reduzido dessas funcionalidades, com ênfase nas áreas "Minha História" e "Memorial".
- Há um **blog de conteúdo** chamado "Insights" em `/insights/` (4 artigos). Existe também um diretório legado `/artigos/` (1 artigo) e um `blog.html` legado (1 artigo).
- Há **uma página legal** (`legais/politicaprivacidade.html`). Não existem Termos de Uso, página LGPD ou página de Cookies como arquivos HTML publicados.
- Existem **versões antigas** dos arquivos (`index_old.html` a `index_old5.html`, `app_old.py` a `app_old6.py`, `components/antigos/...`) mantidas no repositório, o que polui a árvore de arquivos e pode causar confusão.

A auditoria identificou que:

- A **Landing Page** está bem estruturada visualmente, mas **não representa** grande parte das funcionalidades do aplicativo.
- Há **inconsistências de identidade**: o `manifest.json` declara o `theme_color` verde (`#2E8B57`) e descrição de "senhas e mensagens eternas", incompatíveis com a paleta dourada/roxa da Landing atual.
- Há **múltiplas fontes de verdade** para o mesmo conteúdo (ex.: `blog.html` vs `insights/index.html`; `legais/politicaprivacidade.html` vs `components/legal_texts.py`).
- Existem **problemas concretos** de SEO, links quebrados, validação de Schema.org, contraste, organização de diretórios e falta de Páginas Legais completas.

---

## 2. INVENTÁRIO TÉCNICO

### 2.1 Páginas HTML existentes

| Arquivo | Localização | Estado | Evidência |
|---|---|---|---|
| `index.html` | raiz | Ativo (Landing) | 1.549 linhas, único linkado no `sitemap.xml` e `CNAME` |
| `index_old.html` | raiz | Legado | 252 linhas, codificação corrompida (ex.: "AAssistentes", "memA3rias") |
| `index_old2.html` | raiz | Legado | 763 linhas, codificação corrompida |
| `index_old3.html` | raiz | Legado | 438 linhas |
| `index_old4.html` | raiz | Legado | 680 linhas |
| `index_old5.html` | raiz | Legado | 726 linhas |
| `blog.html` | raiz | Legado | 34 linhas, linka para `/artigos/` |
| `insights/index.html` | `/insights/` | Ativo (índice do blog) | 276 linhas |
| `insights/dom-pedro-ii-bisavo.html` | `/insights/` | Ativo | 346 linhas |
| `insights/milhares-de-fotos-poucas-historias.html` | `/insights/` | Ativo | 262 linhas |
| `insights/dia-mais-feliz-do-seu-avo.html` | `/insights/` | Ativo | (apenas 97 linhas) |
| `artigos/sabemos-mais-sobre-dom-pedro-ii-do-que-sobre-nosso-bisavo.html` | `/artigos/` | Legado/órfão | 169 linhas, não linkado no `sitemap.xml` |
| `legais/politicaprivacidade.html` | `/legais/` | Ativo (parcial) | 302 linhas |
| Termos de Uso HTML | — | **Não existe** como arquivo | Existe apenas como string em `components/legal_texts.py:1-25` |
| Política LGPD HTML | — | **Não existe** como arquivo | Existe apenas como string em `components/legal_texts.py:64-73` |
| Cookies HTML | — | **Não existe** | — |

**Evidência do sitemap.xml:**
```
https://www.aeternalegado.com.br/
https://www.aeternalegado.com.br/insights/
https://www.aeternalegado.com.br/insights/dom-pedro-ii-bisavo.html
https://www.aeternalegado.com.br/insights/milhares-de-fotos-poucas-historias.html
https://www.aeternalegado.com.br/insights/dia-mais-feliz-do-seu-avo.html
```

**Observação:** `sitemap.xml:14` lista `insights/dom-pedro-ii-bisavo.html` (formato curto), mas o arquivo está em `insights/` com nome longo. O `sitemap.xml:22` lista `insights/dia-mais-feliz-do-seu-avo.html`, que corresponde ao arquivo existente.

### 2.2 Componentes reutilizáveis (app.py, components/)

| Componente | Arquivo | Responsabilidade | Dependências |
|---|---|---|---|
| `render_login` | `app.py:350-437` | Tela de login (entrar, visitante, cadastro) com 3 abas | `db`, `gerente_usuarios`, `logger` |
| `render_minha_historia` | `app.py:517-901` | Lista memórias do usuário, com prateleira, coleções, contribuições | `db` |
| `render_cabecalho_visitante` | `app.py:908-952` | Cabeçalho do modo visitante | — |
| `render_sobre_visitante` | `app.py:955-1005` | Resumo da pessoa no modo visitante | `db`, `exibir_foto_segura` |
| `render_contribuicoes_aprovadas` | `app.py:1008-1041` | Lista contribuições aprovadas | `exibir_foto_segura`, `exibir_video_seguro` |
| `render_form_contribuicao_memoria` | `app.py:1060-1192` | Formulário para visitantes contribuírem | `db`, `storage` |
| `render_historias_visitante` | `app.py:1195-1237` | Lista de memórias do ponto de vista visitante | `db` |
| `render_aprendizados_visitante` | `app.py:1240-1289` | Aprendizados e valores do homenageado | `db` |
| `render_assistente` / `render_curador_memoria_primeiro` | `app.py:1296-1301`, `components/chat_luto.py:1058` | Curador de Histórias (IA) | `OpenAI`, `db` |
| `render_chat_luto` | `components/chat_luto.py:1066` | Chat IA para o modo luto | `OpenAI`, `db` |
| `render_videos` | `app.py:1307-1515` | Gerenciamento de vídeos | `db`, `gerente_videos`, `storage` |
| `render_fotos` | `app.py:1550-1752` | Álbum de memórias fotográficas | `db`, `storage` |
| `render_perfil_pessoa_vivo` | `app.py:1928-2350` | Perfil detalhado de um contato (vivo) | `db` |
| `render_contatos` | `app.py:2351-2782` | CRUD de contatos/pessoas | `db` |
| `render_preferencias` | `app.py:2783-2880` | "Minha Essência" (foto, gostos, melhor lembrança, etc.) | `db`, `storage` |
| `render_planos` | `app.py:2886-3476` | Planos, preços, Mercado Pago | `db`, `mp_service` |
| `render_agendamentos` | `app.py:3480-3781` | Mensagens para o Futuro + Datas importantes | `db` |
| `render_cofre` | `app.py:3786-3919` | Cofre Digital (Senhas + Documentos criptografados) | `db`, `crypto` |
| `render_sobre` | `app.py:3925-3953` | Página "Sobre" interna | — |
| `render_admin_panel` | `app.py:3954-3969` | Painel administrativo | `db` |
| `render_criar_memorial` | `components/memorial.py:22-160` | Formulário de criação de Memorial | `db`, `storage` |
| `render_memoriais_lista` | `components/memorial.py:162-369` | Lista de memoriais do usuário | `db` |
| `render_curador_perfil` | `components/memorial.py:371-540` | IA Curador de Perfil do homenageado | `OpenAI`, `db` |
| `render_pagina_memorial` | `components/memorial.py:542-1210` | Página completa do Memorial (7 abas) | `db`, `OpenAI` |
| `render_aceite_convite` | `components/memorial.py:1212-1308` | Aceitar convite de contribuição ao Memorial | `db` |
| `render_login_compacto` | `components/login_compacto.py:369-396` | Login compacto (alternativo) | `legal_texts` |
| `render_redefinicao_senha` | `components/login_compacto.py:453-495` | Recuperação de senha | `EmailService` |
| `aplicar_css_dashboard` | `components/dashboard_ui.py:4-3454` | CSS global do dashboard | — |
| `render_sidebar_premium` | `components/dashboard_ui.py:3456-3508` | Sidebar para visitantes (modo leitura) | — |
| `render_painel_inicial` | `components/dashboard_ui.py:3512-3546` | Hero "Bem-vindo" do dashboard | — |
| `aplicar_css_mobile` | `components/mobile_ui.py:3-281` | CSS para layout mobile | — |
| `aplicar_tema` | `styles/theme.py:3-83` | Tema base do Streamlit | — |
| `render_landing` | `components/landing.py:3-49` | Landing alternativa interna (não usada na página estática) | — |

**Observação:** A função `render_landing` em `components/landing.py` existe mas **não é chamada** por `app.py` (a página institucional real é o `index.html` estático). Ela foi descontinuada pelo `index.html` atual.

### 2.3 Imagens / assets (assets/)

Total: **46 arquivos** no diretório `assets/`. Listagem com tamanho e uso:

| Arquivo | Tamanho | Uso confirmado no código |
|---|---|---|
| `appstore-icon.png` | 458 KB | Não referenciado (provavelmente PWA) |
| `bisavo-foto-celular.webp` | 2.061 KB | `artigos/...bisavo.html:70`, `insights/index.html:222` |
| `correcttree.png` | 19 KB | `app.py:2889` (em `render_planos`) |
| `cta-tree.webp` | 2.365 KB | **Não referenciado** |
| `curadoria.webp` | 1.390 KB | `index.html:1373` (tela de curadoria) |
| `dia-mais-feliz-avo.webp` | 2.288 KB | `insights/index.html:253` |
| `favicon.ico` | 374 B | Não há `<link rel="icon">` no `index.html` |
| `favicon-16.png` … `favicon-128.png` | 349 B–7.5 KB | Não referenciados |
| `fotos-sem-historias.webp` | 2.251 KB | `insights/index.html:237` |
| `hero-familia.webp` | 2.245 KB | `index.html:27, 455, 516` |
| `home.webp` | 1.586 KB | `index.html:1175, 1372` |
| `icon-72.png` … `icon-512.png` | 2.9 KB–85 KB | `manifest.json:16-67` |
| `lgpd-badge.png` | 2.340 KB | **Não referenciado** |
| `logo-aeterna-gold.png` | 713 KB | **Não referenciado** |
| `logo-aeterna-gold.svg` | 713 KB | **Não referenciado** (mesmo tamanho do .png) |
| `logo-navbar-clean.png` | 214 KB | `index.html:26, 1132, 1500` |
| `logo-navbar.png` | 523 KB | `index.html:38` (Schema.org), `insights/index.html:200` |
| `logo-sidebar.png` | 2.324 MB | `app.py` (sidebar) |
| `memoria-detalhe.webp` | 1.513 KB | `index.html:1201, 1280` |
| `memorial.png` | 1.523 MB | `index.html:879` |
| `nova-memoria.webp` | 1.449 MB | `index.html:1271` |
| `pessoas.webp` | 1.141 MB | `index.html:1289` |
| `playstore-icon.png` | 144 KB | **Não referenciado** |
| `splash-*.png` | 21 KB–159 KB | **Não referenciados** (PWA legado) |
| `ssl-badge.png` | 2.581 MB | **Não referenciado** |
| `timeline.webp` | 1.472 MB | `index.html:1298, 1374` |

**Observações importantes:**
- Não há `<link rel="icon">` em `index.html` (apenas `og:image`).
- `appstore-icon.png`, `playstore-icon.png`, `splash-*.png` são indícios de PWA/cordova empacotado, mas a Landing não linka para as lojas nem para instalação.
- Há **imagens grandes não otimizadas** (todas >1 MB) sem `loading="lazy"` no `index.html`.

### 2.4 Folhas de estilo

| Origem | Arquivo | Observação |
|---|---|---|
| Inline (Landing) | `index.html:43-1125` | ~1082 linhas de CSS dentro de `<style>` |
| Inline (Insights) | `insights/index.html:13-192` | ~180 linhas |
| Inline (Política) | `legais/politicaprivacidade.html:11-103` | ~93 linhas |
| Inline (App Streamlit) | `app.py:86-237` (CSS injetado), `app.py:914-944`, `app.py:4474-4587` | CSS injetado em `st.markdown` |
| Tema (App) | `styles/theme.py:1-83` | Função `aplicar_tema()` |
| Dashboard | `components/dashboard_ui.py:4-3454` | ~3.450 linhas de CSS injetado |
| Mobile | `components/mobile_ui.py:3-281` | CSS responsivo mobile |
| Memorial | `components/memorial.py:23-71, 163-...` | CSS específico |
| Login compacto | `components/login_compacto.py:10-...` | CSS do login |

**Não há** um arquivo CSS externo único. Não há pré-processador (Sass/Less). Não há framework CSS (Bootstrap, Tailwind).

### 2.5 JavaScript

| Origem | Tamanho | Função |
|---|---|---|
| `index.html:1526-1547` | 22 linhas | Toggle do menu mobile + scroll suave para âncoras |
| `index.html:1175, 1201` | inline `onerror` | Fallback quando as imagens de tela falham ao carregar |

**Não há** framework JS, **não há** bundle, **não há** TypeScript, **não há** testes JS.

### 2.6 Bibliotecas (dependências)

**Site estático (HTML):**
- Google Fonts (`Inter`, `Cormorant Garamond`) — `index.html:30`, `legais/politicaprivacidade.html:9`, `insights/*.html`

**Aplicativo (Python, `requirements.txt`):**
```
streamlit
cryptography
python-dotenv
Pillow
openai>=1.93.0
psycopg2-binary
supabase
mercadopago
```

**Frameworks:**
- **Streamlit** (framework web do app).
- Não há framework web JS no site institucional.

**Ferramentas de build:** Nenhuma detectada. Não há `package.json`, `webpack.config.js`, `vite.config.js`, `tsconfig.json`, `Makefile`, `pyproject.toml` (apenas `requirements.txt` e `setup.py`).

### 2.7 Banco de dados

Estrutura documentada em `utils/estrutura_banco.txt`. Tabelas detectadas:

`agendamentos`, `configuracoes`, `consentimentos`, `contatos`, `documentos`, `memorias`, `personalidade`, `planos`, `preferencias_usuario`, `senhas`, `usuarios`, `videos`, `videos_acesso`, `sqlite_sequence`.

Migrações em `utils/migrar*.py` (vários arquivos).

---

## 3. ARQUITETURA ATUAL

### 3.1 Arquitetura técnica

```
┌──────────────────────────────────────────────────────────────┐
│  SITE ESTÁTICO (GitHub Pages?)  →  aeternalegado.com.br       │
│  ┌────────────────────────────┐                              │
│  │  index.html  (Landing)     │── links → aeterna.streamlit  │
│  │  /insights/  (Blog)        │   .app/ (aplicativo)        │
│  │  /legais/   (1 página)     │                              │
│  │  CNAME = aeternalegado.com │                              │
│  │  robots.txt, sitemap.xml    │                              │
│  │  manifest.json (PWA)        │                              │
│  └────────────────────────────┘                              │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│  APLICATIVO (Streamlit Cloud) → aeterna.streamlit.app        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  app.py  (5.881 linhas)                                │  │
│  │  components/  (memorial, chat_luto, dashboard, ...)    │  │
│  │  utils/  (banco, storage, mercado_pago, ...)           │  │
│  │  styles/theme.py                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│  Supabase (Postgres)  +  Supabase Storage  +  Mercado Pago  │
└──────────────────────────────────────────────────────────────┘
```

**Evidências:**
- `app.py:1-30` — imports de Streamlit, Supabase, Mercado Pago, OpenAI.
- `.streamlit/secrets.toml` — `APP_URL = "https://aeterna.streamlit.app"`, `DATABASE_URL = "postgresql://...supabase.co..."`.
- `index.html:1145, 1161, 1348, 1492, 1515` — todos os CTAs apontam para `https://aeterna.streamlit.app/`.

### 3.2 Fluxo da Landing Page (`index.html`)

```
Header (sticky)
   │
   ▼
[1] Hero  (id="inicio")
   - eyebrow "Legado familiar privado"
   - h1 "Preserve as histórias que explicam de onde sua família veio."
   - parágrafo de proposta de valor
   - CTA primário "Começar minha história"  →  aeterna.streamlit.app
   - CTA secundário "Ver como funciona"      →  #como-funciona
   - 3 proof items
   - mockup visual do app (tela + side)
   │
   ▼
[2] Problema  (id="problema")
   - 4 perguntas: Quem estava presente? O que estava acontecendo? O que sentia? Que valor ficou?
   │
   ▼
[3] O que é a aEterna  (id="o-que-e")
   - 3 cards de definição: Não é álbum / Não é rede social / Não é memorial
   │
   ▼
[4] Como funciona  (id="como-funciona")
   - 4 passos: Registre / Preserve o contexto / Conecte pessoas / Organize no tempo
   │
   ▼
[5] Memorial  (id="memorial-secao")
   - Texto: "E a história de quem já partiu?"
   - 4 benefit-cards: Preserve / Convide / Enriqueça / Converse com o Curador
   - CTA "Criar um Memorial"  →  aeterna.streamlit.app
   │
   ▼
[6] Quote central ("Algumas pessoas deixam saudade...")
   │
   ▼
[7] Telas  (id="telas")
   - 3 mockups: home / curadoria / timeline
   │
   ▼
[8] Message grid (Por que isso importa / O que se perde)
   │
   ▼
[9] Diferenciais  — 4 cards (Fotos / Diários / Nuvem / Memorial)
   │
   ▼
[10] Privacidade  (id="privacidade")
   - 4 itens: Acesso privado / Memórias por contexto / Pessoas / Linha do tempo
   │
   ▼
[11] FAQ  (id="faq")
   - 6 perguntas (details/summary)
   │
   ▼
[12] CTA Final
   - "Comece preservando uma história que sua família não deveria perder."
   - CTA "Criar minha primeira memória"  →  aeterna.streamlit.app
   │
   ▼
Footer
   - logo, descrição, navegação, contato, copyright
```

**Mapear trecho HTML de cada CTA:**

| CTA | Texto | Link | Localização |
|---|---|---|---|
| 1 | "Começar minha história" | `https://aeterna.streamlit.app/` | `index.html:1161` |
| 2 | "Ver como funciona" | `#como-funciona` | `index.html:1162` |
| 3 | "Criar um Memorial" | `https://aeterna.streamlit.app/` | `index.html:1348` |
| 4 | "Criar minha primeira memória" | `https://aeterna.streamlit.app/` | `index.html:1492` |
| 5 (header) | "Acessar" | `https://aeterna.streamlit.app/` | `index.html:1145` |
| 6 (footer) | "Acessar plataforma" | `https://aeterna.streamlit.app/` | `index.html:1515` |
| 7 (footer) | "Insights" | `/insights/` | `index.html:1517` |
| 8 (footer) | "contato@..." | `mailto:contato@aeternalegado.com.br` | `index.html:1516` |

### 3.3 Navegação do site

**Menu principal (desktop e mobile) — `index.html:1140-1146`:**
- Início (`#inicio`)
- Por que existe (`#problema`)
- Como funciona (`#como-funciona`)
- Telas (`#telas`)
- FAQ (`#faq`)
- Acessar (CTA — `https://aeterna.streamlit.app/`)

**Menu mobile:**
- Botão hambúrguer aparece em `max-width: 860px` (`index.html:991-1014`).
- Abre/fecha com toggle de classe `show` (`index.html:1530-1535`).
- Após clicar em qualquer âncora, fecha automaticamente (`index.html:1543`).

**Rodapé — `index.html:1497-1524`:**
- Coluna 1: Logo + descrição.
- Coluna 2: Navegação (mesmos itens do header).
- Coluna 3: Contato (Acessar plataforma, e-mail, Insights).
- Copyright.

**Links externos:**
- `https://aeterna.streamlit.app/` (em 6 pontos do site).
- `mailto:contato@aeternalegado.com.br`.
- `/insights/`.

**Links internos (âncoras):** Todos os links de menu apontam para seções da própria `index.html`. Não há navegação entre páginas HTML (o site é single-page).

### 3.4 Navegação do aplicativo (sidebar)

Referência: `app.py:4393-4619` (`render_sidebar_principal`).

| Item | Página | Origem |
|---|---|---|
| 🏠 Início | `inicio` | `app.py:4400` |
| 📖 Minha História | `minha_historia` | `app.py:4401` |
| 👥 Pessoas | `pessoas` | `app.py:4402` |
| 🤍 Memorial | `memorial_lista` | `app.py:4403` |
| 🤝 Compartilhadas Comigo | `historias_compartilhadas` | `app.py:4404-4408` |
| 🔔 Novidades | `novidades` | `app.py:4409` |
| ✨ Contribuições | `contribuicoes` | `app.py:4410` |
| 🧩 Mais › Curador de Histórias | `assistente` | `app.py:4413` |
| 🧩 Mais › Fotos | `fotos` | `app.py:4415` |
| 🧩 Mais › Vídeos | `videos` | `app.py:4416` |
| 🧩 Mais › Quem Sou Eu | `quem_sou_eu` | `app.py:4417` |
| 🧩 Mais › Mensagens para o Futuro | `mensagens` | `app.py:4418` |
| 🧩 Mais › Cofre | `cofre` | `app.py:4419` |
| 🧩 Mais › Meu plano | `planos` | `app.py:4420` |
| 👤 {nome} › Meu plano | `planos` | `app.py:4611` |
| 👤 {nome} › Configurações | `quem_sou_eu` | `app.py:4614` |
| 👤 {nome} › Sair | logout | `app.py:4617` |
| Admin | `admin` | `app.py:4435` (somente se is_admin) |

---

## 4. AUDITORIA DA COMUNICAÇÃO

### 4.1 Proposta de valor comunicada

**Tagline (title):** "Histórias de família preservadas com contexto" — `index.html:7`.

**Hero headline (h1):** "Preserve as histórias que explicam de onde sua família veio." — `index.html:1155`.

**Hero copy:** "A aEterna organiza fotos, momentos, pessoas, valores e aprendizados em uma linha do tempo privada para que sua família não herde apenas imagens soltas." — `index.html:1157`.

**Eyebrow:** "Legado familiar privado" — `index.html:1154`.

**Meta description:** "A aEterna ajuda famílias a preservar histórias, valores, aprendizados, fotos e momentos importantes em uma linha do tempo privada." — `index.html:8`.

### 4.2 Narrativa da Landing

A Landing constrói uma narrativa clara:

1. **Problema** (Seção 2): "Temos milhares de fotos. Mas poucas histórias realmente registradas." (`index.html:1217`).
2. **Reposicionamento** (Seção 3): "Não é álbum. Não é rede social. Não é memorial." (`index.html:1242, 1248, 1254`).
3. **Solução** (Seção 4): 4 passos — Registrar, Preservar contexto, Conectar pessoas, Organizar no tempo (`index.html:1273-1303`).
4. **Extensão** (Seção 5): Memorial para quem já partiu, com Curador de Perfil IA (`index.html:1316-1344`).
5. **Prova visual** (Seção 7): 3 telas do app (`index.html:1370-1375`).
6. **Diferenciação** (Seção 9): vs. Fotos, Diários, Nuvem, Memorial tradicional (`index.html:1401-1425`).
7. **Privacidade** (Seção 10): "Acesso privado à plataforma" (`index.html:1440-1444`).
8. **FAQ** (Seção 11): 6 perguntas-chave (`index.html:1454-1484`).
9. **CTA final** (Seção 12): "Comece preservando uma história que sua família não deveria perder." (`index.html:1490`).

### 4.3 Comunicação da identidade (histórias, memórias, valores, pessoas, relações, legado)

| Pilar | Presente no site? | Evidência |
|---|---|---|
| Histórias | Sim, núcleo da comunicação | h1, h2, h3 em todas as seções; "Histórias com contexto" em `index.html:1166` |
| Memórias | Sim | "Memórias organizadas por contexto" (`index.html:1441`); "Minha História" no menu do app |
| Valores | Sim | "Valores e aprendizados" (`index.html:1157`); card "Valores e jeito de ser" no app (`app.py:1247`) |
| Pessoas | Sim | "Pessoas relacionadas a cada história" (`index.html:1442`); `app.py:2351` (`render_contatos`) |
| Relações | Parcial | "Conecte pessoas" (passo 3, `index.html:1292`); "Convide quem viveu essa história" (Memorial, `index.html:1333`) |
| Legado familiar | Sim, forte | "Legado familiar privado" (eyebrow, `index.html:1154`); "legado para as próximas gerações" em Memorial, Privacidade, Footer |
| Preservação de quem já partiu | Sim | Seção inteira Memorial (`index.html:1309-1353`) com Curador IA |

**Pílares NÃO comunicados explicitamente no site (apenas no app):**
- **Cofre Digital** (senhas + documentos) — não mencionado em `index.html`.
- **Mensagens para o Futuro** (agendamentos) — não mencionado.
- **Datas importantes** (aniversários, conquistas) — não mencionado.
- **Planos pagos** (Gratuito / Premium) — não mencionado.
- **Visibilidade por conteúdo** (privado / contatos / seletivo) — mencionado genericamente em "Acesso privado".
- **Compartilhamento comigo** (modo visitante) — apenas implícito no Memorial.
- **Cofre criptografado** — não mencionado.
- **Login via chave de acesso** (visitante) — apenas no Memorial.
- **Notificações de novidades** — não mencionado.
- **Administração do usuário** (foto, dados) — não mencionado.
- **Integração com Mercado Pago** — não mencionado.
- **Integração com WhatsApp para convites** — não mencionado (`components/memorial.py:867`).

### 4.4 Identidade da marca — observações

A Landing atual transmite:
- **Paleta:** roxo profundo (`#080014`, `#120322`) com dourado (`#d4af37`, `#f2c572`) — `index.html:44-66`.
- **Tipografia:** "Inter" para corpo + "Cormorant Garamond" serif para títulos (sensação de memorial/novela) — `index.html:80, 281, 482, 533, 696, 745, 812, 886, 933`.
- **Tom:** sóbrio, acolhedor, focado em família e memória.

**Inconsistências de marca detectadas:**
- `manifest.json:4` — `description: "Guarde senhas e mensagens eternas para seus entes queridos"` (alinhado ao posicionamento antigo).
- `manifest.json:7` — `theme_color: "#2E8B57"` (verde) — **não confere com a paleta roxa/dourada da Landing**.
- `app.py:97` — gradiente verde `#90EE90 → #2E8B57 → #1B5E20` no header do login (inconsistente com Landing).
- `app.py:113` — botões verdes `#3CB371 → #1B5E20` (inconsistente com a Landing).
- `app.py:126` — sidebar verde `linear-gradient(180deg, #e8f5e9 0%, #f0faf0 100%)`.
- `styles/theme.py:20` — `linear-gradient(135deg, #26113f 0%, #4b256f 52%, #b77945 100%)` no hero do Streamlit (consistente com a Landing).
- `.streamlit/config.toml` — `primaryColor = "#6B21A8"` (roxo), `backgroundColor = "#F8F5EE"` (creme) — parcial.

**Conclusão:** Existem **dois sistemas visuais** paralelos: o do **site institucional** (roxo/dourado/cinza) e o do **aplicativo Streamlit** (verde/roxo com variâncias). A Landing atual está coerente consigo mesma, mas o app Streamlit ainda carrega elementos verdes herdados de versões anteriores.

---

## 5. AUDITORIA TÉCNICA

### 5.1 SEO

| Item | Status | Evidência |
|---|---|---|
| `<title>` único | ✅ | `index.html:7` |
| Meta description | ✅ | `index.html:8` |
| Meta keywords | ✅ | `index.html:9` |
| Meta author | ✅ | `index.html:10` |
| `meta robots` | ✅ | `index.html:11` |
| Canonical | ✅ | `index.html:12` |
| Open Graph completo | ✅ Parcial | og:type, og:url, og:title, og:description, og:image, og:locale — `index.html:14-19`. **Falta** `og:site_name`. |
| Twitter Card | ✅ | `index.html:21-24` |
| Schema.org | ⚠️ Incompleto | Apenas `Organization` (`index.html:32-41`). Falta `WebSite`, `WebPage`, `BreadcrumbList`, `FAQPage` (mesmo havendo um FAQ na página!). |
| `robots.txt` | ✅ | `robots.txt:1-4` |
| `sitemap.xml` | ⚠️ | `sitemap.xml:1-24` — apenas 5 URLs. **Faltam:** `/legais/politicaprivacidade.html` e páginas institucionais. |
| `lang` correto | ✅ | `<html lang="pt-br">` em `index.html:2` |
| `lang` em páginas internas | ⚠️ | `blog.html:2` usa `pt-BR`; `politicaprivacidade.html:2` usa `pt-BR`; `artigos/...bisavo.html:2` usa `pt-BR` — **inconsistente** com `pt-br` do `index.html`. |
| Headings hierárquicos | ✅ | h1 único (Hero), h2 nas seções, h3 em cards. |
| Imagens com `alt` | ⚠️ | Maioria tem `alt` (`index.html:1132, 1175, 1201, 1372-1374, 1500`). **`index.html:1136` — `<span class="menu-lines" aria-hidden="true"></span>` está OK, mas o `<button id="menuBtn">` não tem texto visível (apenas `aria-label`). OK, mas a `aria-label="Abrir menu"` é fixa e não alterna para "Fechar menu".** |
| `preload` de imagens críticas | ✅ | `index.html:26-27` |

**Link quebrado crítico:**
- `insights/index.html:265` aponta para `/insights/dia-mais-feliz-do-seu-avo.htm` (extensão `.htm` em vez de `.html`).
- O `sitemap.xml:14` usa `insights/dom-pedro-ii-bisavo.html` (curto) — **a URL real** (e o canonical em `insights/dom-pedro-ii-bisavo.html:10`) usa a forma curta. OK.
- `artigos/...bisavo.html:15` declara `og:url` apontando para `/artigos/...`, mas o `sitemap.xml` **não inclui** esta URL e o `blog.html:19` aponta para ela. **Link órfão**.
- `blog.html` não está no `sitemap.xml`.

### 5.2 Acessibilidade

| Item | Status | Evidência |
|---|---|---|
| `<html lang>` | ✅ | `index.html:2` |
| Hierarquia de headings | ✅ | h1 → h2 → h3 em ordem |
| `alt` em imagens | ✅ Maioria | Exceto onde `aria-hidden="true"` (logo) |
| `aria-label` no botão de menu | ✅ | `index.html:1135` |
| `aria-expanded` no toggle | ✅ | `index.html:1135, 1533, 1544` |
| `aria-label` no nav | ✅ | `index.html:1139` |
| Contraste | ⚠️ Verificar | Texto principal branco (`#ffffff`) sobre roxo escuro (`#080014`) — OK. Texto cinza claro `#cfc4da` (`--muted`) sobre roxo — provavelmente OK. Texto cinza-rosado `#a99bb7` (`--muted-soft`) — pode ser insuficiente em alguns pontos. **Não foi possível medir valor exato de contraste via código** — exige inspeção visual. |
| Navegação por teclado | ⚠️ | O menu mobile depende apenas de JavaScript (`index.html:1526-1547`). A função `scrollIntoView` é acionada por click, mas o menu também precisa fechar via `Escape` (não implementado). |
| Foco visível | ⚠️ | Não há regra CSS explícita de `:focus-visible` no `index.html`. |
| `<details>` no FAQ | ✅ | Semântica nativa (`index.html:1455-1483`) |
| `role` ou `aria-hidden` em imagens decorativas | ✅ | `index.html:1201` (`alt=""` no screen-side) |
| `<main>`, `<header>`, `<footer>` | ✅ | `index.html:1129, 1150, 1497` |
| `<nav>` com `aria-label` | ✅ | `index.html:1139` |
| Skip link | ❌ Ausente | Não há link "Pular para o conteúdo" no `index.html`. |
| `<label>` em forms | N/A | Não há `<form>` na Landing. |

**Observação:** `insights/index.html` e `insights/*.html` (artigos individuais) **não têm** `aria-label` em `<nav>`, não usam `<main>`, e misturam `<article>` com estrutura simples.

### 5.3 Performance

| Item | Status | Evidência |
|---|---|---|
| Tamanho da página HTML | 1.549 linhas, ~52 KB | `index.html` |
| Tamanho total dos assets (estimado) | ~38 MB | Soma dos arquivos em `assets/` |
| `loading="lazy"` em imagens | ❌ Ausente | Nenhuma ocorrência de `loading="lazy"` em `index.html` |
| `preload` em imagens críticas | ✅ | `index.html:26-27` (logo + hero) |
| `preconnect` em domínios externos | ✅ | `index.html:28-29` (Google Fonts) |
| Imagens em formato moderno | ✅ Maioria | `.webp` para hero, telas; PNG para ícones |
| Imagens grandes não otimizadas | ⚠️ | `bisavo-foto-celular.webp` (2.0 MB), `cta-tree.webp` (2.3 MB), `dia-mais-feliz-avo.webp` (2.2 MB), `fotos-sem-historias.webp` (2.2 MB), `hero-familia.webp` (2.2 MB), `home.webp` (1.5 MB), `lgpd-badge.png` (2.3 MB), `logo-sidebar.png` (2.3 MB), `ssl-badge.png` (2.5 MB) |
| `width`/`height` em `<img>` | ❌ Ausente | Apenas `max-width: 100%` global (`index.html:111`) |
| CSS crítico inline | ✅ | Todo o CSS da Landing está em `<style>` no `<head>`. |
| CSS não utilizado (dead CSS) | ⚠️ | Classes como `.ct-ps-bars`, `.ae-psc*` (do Streamlit) vazaram para `app.py`. No `index.html`, todas as classes parecem usadas. |
| JavaScript blocking | ✅ | Script no final do `<body>` (`index.html:1526`). |
| Quantidade de requests | ~5 fonts + ~10 imagens + 1 HTML + 1 JS inline | — |
| Cache headers | Não verificável pelo HTML | — |
| Minificação | ❌ | HTML, CSS e JS não estão minificados. |

### 5.4 Navegação e UX

| Item | Status | Evidência |
|---|---|---|
| Menu principal com 5 âncoras | ✅ | `index.html:1140-1144` |
| CTA no menu (header) | ✅ | "Acessar" (`index.html:1145`) |
| Menu mobile funcional | ✅ | Toggle JS (`index.html:1526-1547`) |
| Scroll suave para âncoras | ✅ | `scroll-behavior: smooth` (`index.html:75`) + JS (`index.html:1537-1546`) |
| Botão "voltar ao topo" | ❌ Ausente | — |
| Links de footer | ✅ | `index.html:1505-1517` |
| Breadcrumbs | ❌ Ausente | — |
| Âncora "Acessar" fora do menu | ✅ | No header (`index.html:1145`) e no footer (`index.html:1515`) |
| Fechar menu mobile ao clicar em item | ✅ | `index.html:1543-1544` |
| Fechar menu mobile com tecla Escape | ❌ | Não implementado |
| Trap de foco no menu mobile aberto | ❌ | Não implementado |
| Páginas 404 customizadas | ❌ | Não há `404.html` |

### 5.5 Estrutura de diretórios

| Item | Status | Observação |
|---|---|---|
| Diretório `components/antigos/` (11 arquivos) | ⚠️ | Mantém versões antigas; ocupa espaço; pode causar confusão |
| `app_old.py` ... `app_old6.py` na raiz (6 arquivos) | ⚠️ | Idem |
| `index_old.html` ... `index_old5.html` (5 arquivos) | ⚠️ | Idem |
| `app_old5.py` e `app_old6.py` referenciados em `requirements.txt`? | ❌ | Nenhuma referência, mas coexistem na raiz |
| `utils/aeterna.db` e `utils/cofre.db` | ⚠️ | Bancos de teste commitados? `.gitignore:14-15` ignora `*.db` em `dados/`, mas não em `utils/`. |
| `artigos/` (1 arquivo) | ⚠️ | Diretório órfão; não linkado em `sitemap.xml` nem no menu; `blog.html:19` aponta para ele. |
| `dados/chroma_1/chroma.sqlite3` | ⚠️ | Banco do ChromaDB (provavelmente dev), `dados/` está no `.gitignore` mas o diretório `chroma_1/` foi commitado. |
| `fotos/usuario_2/` e `fotos_perfil/usuarios/` | ⚠️ | Contêm mídias de teste; não ignorados pelo `.gitignore`. |
| `icons/` (vazio) | ⚠️ | Diretório vazio sem uso. |
| `artifacts/` | ⚠️ | PDFs e PNGs de sprints; parecem ser entregáveis internos. |
| `jobs/processar_mensagens_futuro.py` | ⚠️ | Script agendado; sem documentação de quando roda. |
| `output/pdf/`, `tmp/pdfs/` | ⚠️ | PDFs gerados; sem política de retenção documentada. |
| `logs/` (13 arquivos) | ⚠️ | Logs commitados; `.gitignore:27` ignora `*.log`, mas há `.log` commitados. |

### 5.6 Formulários

| Formulário | Arquivo | Validações observadas | Mensagens ao usuário |
|---|---|---|---|
| Login (Entrar) | `app.py:365-377` | Verifica `email and senha` | "E-mail ou senha incorretos" |
| Login (Visitante) | `app.py:381-395` | Verifica 3 campos | "Credenciais inválidas" |
| Cadastro | `app.py:400-437` | Campos obrigatórios, CPF 11 dígitos, senha ≥ 6, confirmação de senha | "Preencha todos os campos obrigatórios", "CPF inválido", "As senhas não coincidem", "Este CPF já está cadastrado", "Este e-mail já está cadastrado" |
| Memorial (criar) | `components/memorial.py:84-160` | Nome obrigatório | "O nome do homenageado é obrigatório" |
| Senha (Cofre) | `app.py:3798-3816` | Serviço, usuário, senha obrigatórios | "Senha de {serviço} adicionada!" |
| Documento (Cofre) | `app.py:3849-3880` | Arquivo obrigatório | "{titulo_final} salvo!" |
| Agendamento (Mensagens para o futuro) | `app.py:3616-3781` | Contato com e-mail obrigatório, data futura | "Cadastre um contato primeiro", "Adicione um e-mail para receber mensagens" |
| Contribuição (Memorial) | `app.py:1060-1192` | Texto ou arquivo obrigatório, foto ≤ 10 MB, vídeo ≤ 100 MB, formato | "Escreva uma lembrança ou envie uma foto/vídeo para contribuir.", "A foto deve ter no máximo 10 MB.", "O vídeo deve ter no máximo 100 MB.", "Formato de arquivo não permitido." |
| Recuperação de senha | `components/login_compacto.py:397-417` | — | (envia e-mail) |
| Newsletter / contato | ❌ | **Não existe** formulário na Landing | — |

**Observação:** A Landing **não tem nenhum formulário**. O único caminho de conversão é o clique no CTA que abre `https://aeterna.streamlit.app/`.

### 5.7 Páginas Legais

| Página | Arquivo | Status | Evidência |
|---|---|---|---|
| Política de Privacidade | `legais/politicaprivacidade.html` | ✅ Ativa (visível) | 302 linhas, mas **não linkada em `index.html`** (verificado: não há `<a href="/legais/...">` em `index.html`). |
| Termos de Uso | ❌ | Não publicado | Existe apenas como string em `components/legal_texts.py:1-25`. |
| Política LGPD (texto) | ❌ | Não publicado | Existe apenas como string em `components/legal_texts.py:64-73`. |
| Cookies / Cookie banner | ❌ | Não publicado, não implementado | — |
| Aceite de termos no cadastro | ✅ | Implementado | `db.criar_usuario(...)` e a tabela `consentimentos` (evidência em `utils/estrutura_banco.txt:11-19`) |
| **Linkagem no site** | ❌ | Nenhuma página legal é linkada no `index.html` (rodapé ou header) | — |
| Versão atualizada | ⚠️ | Declara "Junho de 2026" (em `legais/politicaprivacidade.html:114` e `components/legal_texts.py:4, 31`) | — |

**Evidência de link ausente:** busca em `index.html` por `politicaprivacidade`, `termos`, `legal`, `lgpd` — **nenhuma ocorrência**.

### 5.8 Segurança (observações a partir do código)

- HTTPS forçado: o `canonical` e OG URLs usam `https://www.aeternalegado.com.br/`.
- `.streamlit/secrets.toml` está **fora do controle de versão** segundo `.gitignore:30`.
- A `Política de Privacidade` em `legais/politicaprivacidade.html:252` declara explicitamente: "A aEterna não utiliza histórias, mensagens, fotografias, vídeos ou documentos privados para treinamento de modelos de Inteligência Artificial sem autorização expressa do titular." — coerente com o uso de OpenAI configurado por feature flag.
- HTML não tem nenhum `<form>` que receba dados, reduzindo superfície de ataque na Landing.
- A `integrity` de fontes externas (Google Fonts) não é verificada.

---

## 6. MATRIZ DE ADERÊNCIA SITE × APLICATIVO

Para a matriz, considerei todas as áreas funcionais do appStreamlit (14 áreas) e o que o site institucional comunica.

| # | Funcionalidade do App | Existe no App | Existe no Site | Representação Correta | Observações |
|---|---|---|---|---|---|
| 1 | **Login de usuário (entrar)** | ✅ `app.py:276-295` | ❌ Não comunicada | — | Site só tem CTA "Acessar" → app |
| 2 | **Login de visitante (chave de acesso)** | ✅ `app.py:298-317`, `components/login_compacto.py:267-289` | ❌ Não comunicada | — | Modalidade de "Conhecer a história de alguém" não é mencionada na Landing |
| 3 | **Cadastro de usuário** | ✅ `app.py:334-344, 398-437` | ❌ Não comunicada | — | Cadastro só acontece dentro do app |
| 4 | **Minha História (lista de memórias)** | ✅ `app.py:517-901` | ✅ Parcial | ⚠️ | Hero mostra a tela "Home" (`index.html:1172-1196`) e um passo "Registre um momento" (`index.html:1274`). Não menciona "Coleções", "Categorias" (Família, Viagens, etc.) nem o sistema de visibilidade. |
| 5 | **Curador de Histórias (IA)** | ✅ `app.py:1296-1301`, `components/chat_luto.py:1058` | ✅ Parcial | ✅ | Passo 1 do "Como funciona" menciona "Conte o que aconteceu com suas palavras" (`index.html:1275`). Tela `curadoria.webp` mostrada em `index.html:1373`. Não menciona explicitamente que é IA. |
| 6 | **Memorial (homenagem póstuma)** | ✅ `components/memorial.py:22-160, 162-369, 542-1210` | ✅ Sim | ✅ | Seção inteira dedicada (`index.html:1309-1353`). Cita o Curador de Perfil, convites, contribuição. |
| 7 | **Pessoas / Contatos** | ✅ `app.py:2351-2782` | ⚠️ Muito superficial | ⚠️ | Mencionado em "Conecte pessoas" (passo 3, `index.html:1292`) e "Pessoas relacionadas a cada história" (`index.html:1442`). Não menciona perfil de pessoa, datas especiais, chave de acesso, parentesco. |
| 8 | **Compartilhadas Comigo** | ✅ `app.py:5070-5322` | ❌ Não comunicada | — | Não há menção no site |
| 9 | **Novidades** | ✅ `app.py:5323-5564` | ❌ Não comunicada | — | — |
| 10 | **Contribuições** | ✅ `app.py:4189-4353` | ✅ Parcial | ✅ | "Convide familiares e amigos para contribuir" (Memorial, `index.html:1322, 1333`). Não menciona workflow de aprovação. |
| 11 | **Fotos (álbum)** | ✅ `app.py:1550-1752` | ⚠️ Superficial | ⚠️ | Cards "Não é álbum" (`index.html:1242-1244`) comunicam o contrário. "Como funciona" não menciona álbuns especificamente. |
| 12 | **Vídeos** | ✅ `app.py:1307-1515` | ❌ Não comunicada | — | Não há menção a upload ou visualização de vídeos na Landing. |
| 13 | **Quem Sou Eu / Minha Essência** | ✅ `app.py:2783-2880` | ❌ Não comunicada | — | Não há menção ao questionário de preferências (música, comida, melhor lembrança, dia mais feliz). |
| 14 | **Mensagens para o Futuro (agendamentos)** | ✅ `app.py:3480-3781` | ❌ Não comunicada | — | Não há menção a mensagens agendadas, datas recorrentes, envio programado. |
| 15 | **Cofre Digital (senhas + documentos)** | ✅ `app.py:3786-3919` | ❌ Não comunicada | — | Funcionalidade sensível (criptografia local) completamente ausente da Landing. |
| 16 | **Planos e Pagamentos** | ✅ `app.py:2886-3476`, `utils/mercado_pago_service.py` | ❌ Não comunicada | — | Não há página de preços, não há menção a Mercado Pago, não há menção a "Premium". |
| 17 | **Visibilidade por conteúdo (privado/contatos/seletivo)** | ✅ `app.py:444-515` | ⚠️ | ⚠️ | Apenas "Acesso privado" genérico. Não explica os 3 níveis. |
| 18 | **Datas importantes** | ✅ `app.py:3493-3600` | ❌ Não comunicada | — | — |
| 19 | **Foto de perfil** | ✅ `app.py:2792-2835` | ❌ Não comunicada | — | — |
| 20 | **Recuperação de senha** | ✅ `components/login_compacto.py:397-417` | ❌ Não comunicada | — | — |
| 21 | **Modo visitante com chave** | ✅ `app.py:298-317` | ❌ Não comunicada | — | — |
| 22 | **Integração WhatsApp (convite Memorial)** | ✅ `components/memorial.py:867-944` | ❌ Não comunicada | — | — |
| 23 | **PWA / app instalável** | ⚠️ Parcial | ⚠️ | ⚠️ | `manifest.json` existe, mas `index.html` não inclui `<link rel="manifest">` e não há service worker. |
| 24 | **Blog/Insights** | — | ✅ | ✅ | `insights/` com 3 artigos, linkado no footer (`index.html:1517`) |
| 25 | **Política de Privacidade** | ✅ (no fluxo de cadastro via string) | ❌ Não linkada | — | Arquivo existe em `legais/`, mas **não há link no site**. |

**Resumo:** de 25 funcionalidades, **11 não são comunicadas** (44%), **7 são comunicadas parcialmente**, **3 são comunicadas corretamente** e **4 não se aplicam**.

---

## 7. LISTA DE OPORTUNIDADES

> Sem propor implementações nesta sprint. Apenas relação do que foi observado.

### 7.1 SEO e indexação

1. Adicionar `og:site_name` ao `index.html`.
2. Adicionar Schema.org `FAQPage` à seção FAQ de `index.html` (a FAQ tem 6 perguntas — basta gerar `Question`/`Answer`).
3. Adicionar Schema.org `WebSite` com `SearchAction` e `WebPage`.
4. Adicionar `BreadcrumbList` nas páginas `/insights/*.html`.
5. Corrigir o `lang` das páginas internas: padronizar em `pt-BR` ou `pt-br`.
6. Adicionar `/legais/politicaprivacidade.html` ao `sitemap.xml`.
7. Remover `artigos/` ou redirecioná-lo para `/insights/` (a página `artigos/sabemos-mais-sobre-dom-pedro-ii-do-que-sobre-nosso-bisavo.html` é uma duplicata de `insights/dom-pedro-ii-bisavo.html`).
8. Corrigir o link quebrado em `insights/index.html:265` (`.htm` → `.html`).
9. Adicionar `lastmod` em todas as URLs do `sitemap.xml`.
10. Padronizar formato das URLs no `sitemap.xml` (algumas sem `.html` final, inconsistência).
11. Publicar páginas de Termos de Uso e LGPD como HTML e linká-las.
12. Adicionar `hreflang` (mesmo sendo single-language, é boa prática).

### 7.2 Acessibilidade

13. Adicionar "Pular para o conteúdo" (`skip-link`).
14. Implementar fechamento do menu mobile com `Escape`.
15. Adicionar regra CSS `:focus-visible` com indicador visível.
16. Adicionar `<main id="conteudo">` com `tabindex="-1"` para receber o foco do skip-link.
17. Tornar o `aria-label` do botão de menu dinâmico ("Abrir menu" / "Fechar menu") — atualmente `index.html:1135` é fixo.
18. Auditar contraste de texto, especialmente `--muted-soft: #a99bb7` sobre `--bg: #080014`.

### 7.3 Performance

19. Adicionar `loading="lazy"` em todas as imagens que não estão acima da dobra.
20. Adicionar `decoding="async"` nas imagens.
21. Definir `width` e `height` explícitos em todas as `<img>` (evita CLS).
22. Comprimir as imagens >1 MB que não estão sendo usadas (ex.: `cta-tree.webp`, `lgpd-badge.png`, `ssl-badge.png`, `appstore-icon.png`, `playstore-icon.png`).
23. Avaliar a remoção das imagens não referenciadas em `assets/`.
24. Considerar a conversão do `logo-aeterna-gold.png` (713 KB) para vetor (`.svg`) ou WebP.
25. Adicionar `<link rel="icon">` (favicon) ao `index.html`.

### 7.4 Conteúdo e comunicação

26. Criar uma página "Funcionalidades" listando todas as áreas do app (Cofre, Mensagens para o Futuro, Datas, Planos).
27. Criar página de "Planos e Preços" (atualmente `app.py:2886-3476` mostra a tabela, mas o site não).
28. Adicionar FAQ no site sobre o Curador IA, deixando claro que é IA e não representa a pessoa.
29. Adicionar uma seção "Casos de uso" ou "Para quem é" no site.
30. Publicar página LGPD separada (banner de consentimento já existe em `components/landing.py:48`).
31. Publicar página de Termos de Uso.
32. Publicar banner de cookies (mesmo que seja apenas um aviso estático, a LGPD recomenda).

### 7.5 Identidade visual

33. Harmonizar paleta do app Streamlit com a paleta da Landing (substituir verdes por dourados/roxos ou documentar oficialmente a dualidade).
34. Atualizar `manifest.json:4` (description) e `manifest.json:7` (theme_color) para refletir o posicionamento atual.
35. Adicionar `<link rel="manifest" href="manifest.json">` ao `index.html` (manifest existe mas não é linkado).
36. Implementar tema Apple-touch-icon (`apple-touch-icon` em `index.html`).
37. Implementar `theme-color` e `color-scheme` no `<head>` da Landing para alinhar com a paleta.

### 7.6 Estrutura e organização

38. Mover os arquivos `index_old*.html`, `app_old*.py` e `components/antigos/` para um diretório `legacy/` ou removê-los do controle de versão (`.gitignore`).
39. Remover `artigos/` ou fundir com `insights/`.
40. Remover `utils/aeterna.db` e `utils/cofre.db` do repositório.
41. Remover `dados/chroma_1/` ou movê-lo para uma pasta `data/`.
42. Remover `fotos/`, `fotos_perfil/` e `videos/` de teste ou movê-los para `samples/`.
43. Limpar `icons/` (vazio).
44. Documentar a função de `artifacts/`, `output/`, `tmp/`, `jobs/`, `logs/` ou ignorá-los.
45. Documentar a estratégia de versionamento: quando uma versão é "ativa" e quando vai para `legacy/`.

### 7.7 Páginas legais

46. Linkar a Política de Privacidade no rodapé do `index.html`.
47. Publicar Termos de Uso como HTML e linkar no rodapé.
48. Publicar Política de Cookies e linkar no rodapé.
49. Adicionar caixa de "Última atualização" com data efetiva e link para a versão anterior.
50. Adicionar link para o canal de exercício de direitos do titular (e-mail já existe: `contato@aeternalegado.com.br`, mas poderia estar mais visível).

### 7.8 Robustez técnica

51. Implementar `404.html` customizada.
52. Adicionar `verificação` de propriedade do Google Search Console (não há tag de verificação).
53. Adicionar Sitemap auto-gerado (e remover o `sitemap.xml` estático, que pode ficar desatualizado).
54. Implementar RSS/Atom para o blog `insights/`.
55. Adicionar analytics (Google Analytics 4, Plausible, etc.) — não há nenhuma tag de analytics na Landing.
56. Considerar migrar de GitHub Pages para um host que suporte redirects 301 (para corrigir o link `.htm` → `.html`).
57. Adicionar teste automatizado de links quebrados (algum dos links em `index.html` aponta para `https://aeterna.streamlit.app/` que pode mudar).

---

## 8. PRIORIZAÇÃO

Critério:
- **Impacto**: consequência para SEO, conversão, conformidade legal, performance ou compreensão do produto.
- **Esforço**: estimativa qualitativa baseada na quantidade de arquivos, dependências e risco de regressão (sem código nesta sprint).
- **Justificativa**: evidência objetiva do motivo da classificação.

### 8.1 Alta prioridade

| # | Oportunidade | Impacto | Esforço | Justificativa |
|---|---|---|---|---|
| 1 | **Publicar e linkar Termos de Uso, Política de Privacidade e Cookies no rodapé** | Alto | Baixo | `legais/politicaprivacidade.html` existe mas **não é linkada** em `index.html`; Termos de Uso e LGPD não existem como HTML publicado. Exigência legal (LGPD) e padrão de mercado. |
| 2 | **Corrigir link quebrado `dia-mais-feliz-do-seu-avo.htm`** | Alto | Trivial | `insights/index.html:265` aponta para `.htm` em vez de `.html`; gera 404 e prejudica UX. |
| 3 | **Decidir destino de `artigos/`** (remover ou fundir com `insights/`) | Alto | Baixo | Existe duplicata de conteúdo (artigos quase idênticos em `artigos/` e `insights/`); polui SEO com conteúdo duplicado. |
| 4 | **Atualizar `manifest.json`** (description, theme_color) | Médio | Trivial | `manifest.json:4, 7` carrega posicionamento antigo ("senhas", verde `#2E8B57`); causa inconsistência ao instalar PWA. |
| 5 | **Adicionar Schema.org `FAQPage`** | Alto | Baixo | FAQ tem 6 perguntas prontas em `index.html:1454-1484`; sem Schema, perde-se rich results. |
| 6 | **Representar no site o conjunto completo de funcionalidades** (Cofre, Mensagens para o Futuro, Planos, Datas) | Alto | Médio | 11 das 25 funcionalidades não são comunicadas; Landing atual representa apenas ~28% do produto. |
| 7 | **Adicionar `<link rel="icon">` e `manifest` ao `index.html`** | Médio | Trivial | `favicon.ico` e `manifest.json` existem; falta o link. |

### 8.2 Média prioridade

| # | Oportunidade | Impacto | Esforço | Justificativa |
|---|---|---|---|---|
| 8 | **Adicionar skip-link e foco visível** | Médio | Baixo | Boa prática de acessibilidade; landing longa com 12 seções. |
| 9 | **Implementar `loading="lazy"` e `width`/`height`** | Médio | Baixo | Landing não tem `loading="lazy"` em nenhuma imagem; melhoria de LCP. |
| 10 | **Harmonizar paleta Streamlit com Landing** | Médio | Médio | Dois sistemas visuais (verde/roxo) no app, roxo/dourado na Landing. Inconsistência de marca. |
| 11 | **Padronizar `lang` em todas as páginas HTML** | Baixo | Trivial | `pt-br` na Landing, `pt-BR` nas demais. |
| 12 | **Mover arquivos `*_old*` e `components/antigos/` para `legacy/`** | Médio | Baixo | Poluição da árvore, dificulta navegação; conteúdo morto. |
| 13 | **Adicionar `og:site_name`, `BreadcrumbList`, `WebSite` Schema** | Médio | Baixo | Melhora SERP. |
| 14 | **Implementar `404.html` customizada** | Médio | Trivial | Boa prática. |
| 15 | **Publicar página de Planos no site** | Médio | Médio | App já tem `render_planos` (`app.py:2886`) com a tabela; basta transpor para o site. |
| 16 | **Adicionar `lastmod` ao `sitemap.xml`** | Baixo | Baixo | SEO. |
| 17 | **Adicionar `favicon-32.png` ou `favicon.ico` no `<head>`** | Médio | Trivial | Identidade de aba. |

### 8.3 Baixa prioridade

| # | Oportunidade | Impacto | Esforço | Justificativa |
|---|---|---|---|---|
| 18 | Comprimir imagens >1 MB não usadas em `assets/` | Baixo | Médio | Imagens como `cta-tree.webp` (2.3 MB) e `lgpd-badge.png` (2.3 MB) não estão linkadas; peso morto. |
| 19 | Remover diretórios vazios/órfãos (`icons/`) | Baixo | Trivial | Limpeza. |
| 20 | Adicionar feed RSS para o blog `insights/` | Baixo | Médio | Marketing de conteúdo. |
| 21 | Adicionar Google Analytics / Plausible | Médio | Trivial | Não há analytics; impossível medir conversão da Landing. |
| 22 | Documentar `artifacts/`, `output/`, `tmp/`, `jobs/`, `logs/` | Baixo | Baixo | — |
| 23 | Adicionar `apple-touch-icon` | Baixo | Trivial | PWA / iOS. |
| 24 | Fechamento do menu mobile com `Escape` | Baixo | Trivial | UX. |
| 25 | Migrar `blog.html` para `insights/index.html` (ou redirecionar) | Baixo | Trivial | `blog.html` referencia `/artigos/`, que está em desuso. |

---

## 9. NOTAS FINAIS

- Esta auditoria baseou-se **exclusivamente em leitura estática** dos arquivos do repositório. Nenhuma análise de runtime, lighthouse, PageSpeed Insights ou console do navegador foi executada.
- Itens marcados como "**Não foi possível verificar**" dependem de inspeção visual ou execução real:
  - Contraste exato de cores em todos os pontos da Landing.
  - Tempo de carregamento real.
  - Comportamento do menu mobile em diferentes dispositivos.
- Toda referência a arquivos foi feita com `file_path:line_number` para rastreabilidade.
- A identidade visual do **site** e do **app Streamlit** ainda estão em transição: o site está consolidado em roxo/dourado, mas o app Streamlit tem resquícios verdes (`app.py:97, 113, 126`).
- O `CNAME` em `D:\aeterna\CNAME` confirma que o site é publicado em `aeternalegado.com.br`.
- O `app.py` confirma que o aplicativo está publicado em `https://aeterna.streamlit.app/` (`.streamlit/secrets.toml:APP_URL`).

---

**Fim da Sprint 0 — Auditoria.**
