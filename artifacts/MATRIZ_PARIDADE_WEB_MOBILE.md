# MATRIZ DE PARIDADE WEB × MOBILE — aEterna

> Documento oficial de referência da plataforma aEterna. Define o que cada camada (Landing, Site Institucional, Aplicativo Mobile) deve conter, o que já contém e o que ainda precisa ser implementado. Este documento substitui qualquer entendimento anterior sobre divisão de responsabilidades e serve como fonte de verdade para as próximas sprints.

---

## 1. Visão Geral

### O que é a plataforma aEterna

> A aEterna é o lugar onde a história da sua família continua sendo construída, compartilhada e preservada ao longo das gerações.

É uma plataforma integrada — não um conjunto de produtos separados. Ela se manifesta através de três pontos de contato, cada um com um papel específico:

| Camada | Produto | Papel |
|--------|---------|-------|
| **Landing** | `index.html` (aeternalegado.com.br) | Apresentar o conceito, converter visitantes em usuários |
| **Site Institucional** | `/insights/`, `/legais/`, FAQ | Suporte ao produto: conteúdo editorial, legal, SEO |
| **Aplicativo Mobile** | Flutter (não implementado) | Ser o produto principal (não existe neste repositório) |
| **Aplicativo Web** | Streamlit (aeterna.streamlit.app) | Produto funcional atual (substitui temporariamente o Mobile) |

### Observação crítica

**O Aplicativo Mobile (Flutter) não existe neste repositório.** O código-fonte presente contém apenas:
- `index.html` — Landing Page
- `app.py` — Aplicação Streamlit (substituta funcional do Mobile)
- Páginas internas do site (`/insights/`, `/legais/`)
- Componentes, utilitários e estilos

O aplicativo Mobile mencionado nas referências históricas (Sprint 0) nunca foi implementado ou está em outro repositório. **Toda referência a "Mobile" neste documento reflete o estado esperado vs. o estado real.** A plataforma atual é 100% web.

### Estado atual da plataforma

```
                       ┌─────────────────────────────┐
                       │      USUÁRIO                │
                       └──────────┬──────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
        ┌─────────────────┐ ┌──────────┐ ┌──────────────┐
        │    LANDING      │ │   SITE   │ │  APP (WEB)   │
        │  index.html     │ │insights/ │ │  Streamlit   │
        │  aeternalegado  │ │ leçais/  │ │aeterna.stream│
        │  .com.br        │ │  FAQ     │ │  lit.app     │
        └─────────────────┘ └──────────┘ └──────────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │   MOBILE     │
                                        │  (Flutter)   │
                                        │  ❌ NÃO      │
                                        │  EXISTE      │
                                        └──────────────┘
```

---

## 2. Jornada Oficial do Usuário

```
1. DESCOBERTA
   ├── Google / Indicação / Link direto
   │
   ├──▶ Landing (index.html)
   │      ├── Hero: carrossel com 8 histórias de família
   │      ├── Problema: "As fotos sobrevivem. As histórias, quase nunca."
   │      ├── Curador: exemplo de diálogo (6 turnos)
   │      ├── Funcionalidades: grid com 15 cards + ecossistema (10 tiles)
   │      ├── Memorial: "continuação da vida"
   │      └── FAQ: 8 perguntas
   │
   ├──▶ Blog (/insights/)
   │      └── 3 artigos (Dom Pedro II, Milhares de Fotos, Dia mais feliz)
   │
   └──▶ Páginas legais (/legais/politicaprivacidade.html)
   │
   ▼
2. PRIMEIRO ACESSO
   │
   ├── CTA "Descobrir uma história" ou "Começar a contar a minha"
   │
   ├──▶ App (aeterna.streamlit.app)
   │      └── Login/Cadastro
   │            ├── Email + senha
   │            ├── Nome, sobrenome, CPF, data de nascimento
   │            └── Telefone (opcional)
   │
   ▼
3. PRIMEIRA HISTÓRIA
   │
   ├──▶ Home (render_inicio)
   │      └── Sidebar de navegação aparece
   │
   ├──▶ Minha História (render_minha_historia)
   │      └── "Nova memória" → formulário (foto, título, texto, data, pessoas)
   │
   ├──▶ Curador de Histórias (render_assistente)
   │      └── Diálogo: Curador pergunta → usuário responde → Curador estrutura
   │
   └──▶ História salva → entra na Linha do Tempo
   │
   ▼
4. CONSTRUÇÃO DA ÁRVORE FAMILIAR
   │
   ├──▶ Pessoas (render_contatos)
   │      └── Cadastra familiares: nome, parentesco, datas
   │
   ├──▶ Fotos (render_fotos)
   │      └── Upload de fotos, associadas a histórias e pessoas
   │
   ├──▶ Vídeos (render_videos)
   │      └── Upload de vídeos, com limite por plano
   │
   └──▶ Linha do Tempo (tab em Minha História)
   │
   ▼
5. COLABORAÇÃO FAMILIAR
   │
   ├──▶ Compartilhar história
   │      └── Definir visibilidade (privado / contatos / seletivo)
   │
   ├──▶ Familiar recebe notificação
   │      └── Novidades (🔔) com badge de contribuições
   │
   ├──▶ Familiar contribui
   │      └── Adiciona foto, vídeo ou texto → dono aprova
   │
   └──▶ História cresce com múltiplas vozes
   │
   ▼
6. USO CONTÍNUO
   │
   ├──▶ Mais histórias
   ├──▶ Mensagens para o Futuro
   │      └── Grava mensagem hoje → abre em data futura
   ├──▶ Cofre
   │      └── Itens criptografados
   └──▶ Memorial (quando aplicável)
   │      └── Família constrói história de quem se foi
   │
   ▼
7. RETORNO AO SITE
   │
   └──▶ ⚠️ QUEBRA: App não tem link para o site
         Usuário precisa abrir nova aba manualmente
```

---

## 3. Papéis de Cada Produto

| Produto | Missão | Público | Estado |
|---------|--------|---------|--------|
| **Landing** (`index.html`) | Fazer alguém se apaixonar pela ideia. Apresentar o problema, a solução e o valor — sem entregar o produto completo. | Visitante (não logado) | ✅ Completa (23 seções, 4643 linhas) |
| **Site Institucional** (`/insights/`, `/legais/`, FAQ) | Dar suporte ao produto: conteúdo editorial que aprofunda o conceito, páginas legais obrigatórias, FAQ para dúvidas comuns. | Visitante + Usuário | ✅ Parcial (blog com 3 artigos, 1 página legal, FAQ na Landing) |
| **App Web (Streamlit)** (`app.py`) | Ser o produto funcional atual. Onde a família cria, organiza e compartilha histórias. Substituto temporário do Mobile. | Usuário logado | ✅ Completo (5881 linhas, 19 seções) |
| **App Mobile (Flutter)** | Ser o produto principal. Onde a família vive. Onde as histórias acontecem. Onde tudo é criado — com notificações nativas, câmera, biometria, deep links. | Usuário logado | ❌ **Não existe** |

### Papel detalhado de cada camada

#### Landing (index.html)

**Missão específica:** Converter visitante em usuário.

O que faz:
- Apresenta o problema ("fotos sobrevivem, histórias quase nunca")
- Apresenta a solução (plataforma integrada)
- Demonstra o conceito com exemplos (carrossel de histórias, diálogo do Curador)
- Lista funcionalidades (15 cards + ecossistema)
- Explica o Memorial
- Responde dúvidas (FAQ)
- Convida para ação (CTAs)

O que NÃO faz:
- Não cria conteúdo
- Não autentica
- Não armazena dados
- Não tem interação social

#### Site Institucional

**Missão específica:** Suporte, conteúdo e credibilidade.

Componentes:
- **Blog** (`/insights/`): 3 artigos sobre memória familiar, SEO
- **Páginas Legais** (`/legais/politicaprivacidade.html`): LGPD, termos
- **FAQ** (embutido na Landing): 8 perguntas frequentes
- **SEO** (sitemap.xml, robots.txt, Schema.org): Indexação

O que NÃO faz (ainda):
- Não tem página de parceiros
- Não tem página de downloads
- Não tem memorial público
- Não tem convites públicos
- Não tem página "Sobre" dedicada (existe `render_sobre` no app mas não no site)

#### App Web — Streamlit (estado atual)

**Missão específica:** Ser o produto funcional enquanto o Mobile não existe.

Componentes:
- **Autenticação:** Login, Cadastro, Login Visitante, Recuperação de Senha
- **Criação:** Minha História, Curador, Fotos, Vídeos
- **Organização:** Linha do Tempo, Pessoas, Tags
- **Colaboração:** Compartilhadas, Contribuições, Novidades
- **Futuro:** Mensagens para o Futuro, Cofre
- **Memorial:** Criação, gestão, curador, convites
- **Configuração:** Quem Sou Eu, Planos, Admin
- **Visitante:** Modo leitura para convidados

Limitações:
- Sem notificações push nativas
- Sem acesso a câmera/galeria nativa
- Sem biometria
- Sem deep links
- Sem funcionamento offline
- Interface mais estática (sem animações elaboradas)

#### App Mobile — Flutter (estado futuro desejado)

**Missão específica:** Ser o produto principal. Substituir o Streamlit como interface principal do usuário.

Deve conter (não implementado):
- Todas as funcionalidades do app Streamlit
- Notificações push nativas
- Acesso à câmera e galeria
- Biometria (impressão digital, Face ID)
- Deep links (convites, memorial público)
- Compartilhamento nativo (WhatsApp, fotos, links)
- Funcionamento offline parcial
- WorkManager (notificações agendadas, Mensagens para o Futuro)
- Detecção automática de momentos (fotos no dispositivo)

---

## 4. Matriz de Funcionalidades

### Legenda

| Símbolo | Significado |
|---------|-------------|
| ✅ | Implementado e completo |
| ⚠️ | Implementado parcialmente ou com divergência |
| ❌ | Não implementado |
| — | Não se aplica (não deve existir nesta camada) |
| 📝 | Planejado para futura implementação |

### Matriz completa

| # | Funcionalidade | Landing | Site | App Web (Streamlit) | App Mobile (Flutter) | Status | Evidência | Observação |
|---|---|---|---|---|---|---|---|---|
| 1 | **Login (email/senha)** | ❌ (só CTA) | — | ✅ `fazer_login` | ❌ | **Web OK, Mobile falta** | `app.py:276-295` | Sem Mobile não há login mobile |
| 2 | **Cadastro** | ❌ (só CTA) | — | ✅ `fazer_cadastro` | ❌ | **Web OK, Mobile falta** | `app.py:334-344` | Cadastro pede CPF + data nascimento |
| 3 | **Login Visitante (chave)** | ❌ | — | ✅ `fazer_login_visitante` | ❌ | **Web OK, Mobile falta** | `app.py:298-317` | Não comunicado na Landing |
| 4 | **Recuperação de Senha** | ❌ | — | ✅ `login_compacto.py:397-417` | ❌ | **Web OK, Mobile falta** | `login_compacto.py:397-417` | Não comunicado na Landing |
| 5 | **Cadastro biométrico** | — | — | ❌ | ❌ | **Falta em ambos** | — | Nenhuma camada tem |
| 6 | **Cadastro Google/Apple** | — | — | ❌ | ❌ | **Falta em ambos** | — | Nenhuma camada tem |
| 7 | **Home / Início** | ✅ Hero | — | ✅ `render_inicio` | ❌ | **Web OK, Mobile falta** | `index.html:3207`, `app.py:4621` | Landing mostra stories, App mostra métricas |
| 8 | **Minha História** | ✅ Apresenta (cards + passos) | ✅ Explica (exemplo timeline) | ✅ `render_minha_historia` | ❌ | **Web OK, Mobile falta** | `index.html:3417-3498`, `app.py:517-901` | Nome consistente |
| 9 | **Curador de Histórias** | ✅ Apresenta (seção + diálogo) | ✅ Explica (FAQ) | ✅ `render_assistente` + `render_curador_memoria_primeiro` | ❌ | **Web OK, Mobile falta** | `index.html:3500-3558`, `app.py:1296-1301` | Guia silencioso, faz perguntas |
| 10 | **Explorador de Histórias** | ✅ Apresenta (ecossistema) | — | ✅ `assistente_ia.py` | ❌ | **Web OK, Mobile falta** | `index.html:4000-4058`, `assistente_ia.py` | Modo pergunta sobre pessoa |
| 11 | **Pessoas / Contatos** | ✅ Apresenta (showcase) | ✅ Explica | ✅ `render_contatos` | ❌ | **Web OK, Mobile falta** | `index.html:3685-3699`, `app.py:2351-2782` | Cadastro + perfil + linha do tempo |
| 12 | **Fotos** | ✅ Apresenta (transformação foto→história) | — | ✅ `render_fotos` | ❌ | **Web OK, Mobile falta** | `index.html:3562-3617`, `app.py:1550-1752` | Upload, grid, associar a história |
| 13 | **Vídeos** | ✅ Apresenta (transformação vídeo→história) | — | ✅ `render_videos` | ❌ | **Web OK, Mobile falta** | `index.html:3562-3617`, `app.py:1307-1515` | Upload com limite por plano |
| 14 | **Linha do Tempo** | ✅ Apresenta (exemplo 2001-2035) | ✅ Explica | ✅ Tab em Minha História | ❌ | **Web OK, Mobile falta** | `index.html:3462-3497`, `app.py:2309` | Cronológica, filtros por pessoa |
| 15 | **Compartilhadas comigo** | ✅ Apresenta (ecossistema) | — | ✅ `render_historias_compartilhadas_lista` | ❌ | **Web OK, Mobile falta** | `index.html:4000-4058`, `app.py:5070-5322` | Histórias recebidas de outros |
| 16 | **Novidades** | ✅ Apresenta (feature card) | — | ✅ `render_novidades` | ❌ | **Web OK, Mobile falta** | `index.html:3305-3310`, `app.py:5323-5564` | Feed de notificações |
| 17 | **Contribuições** | ✅ Apresenta (ecossistema) | — | ✅ `render_contribuicoes_pendentes` | ❌ | **Web OK, Mobile falta** | `index.html:4000-4058`, `app.py:4189-4353` | Moderação de contribuições |
| 18 | **Memorial** | ✅ Apresenta (seção dedicada + exemplo) | ✅ Explica (FAQ) | ✅ `memorial.py` | ❌ | **Web OK, Mobile falta** | `index.html:4068-4137`, `memorial.py` | Continuação da vida |
| 19 | **Mensagens para o Futuro** | ✅ Apresenta (exemplo 2018→2036) | — | ✅ `render_agendamentos` | ❌ | **Web OK, Mobile falta** | `index.html:3334-3363`, `app.py:3480-3781` | Agendamento de mensagens |
| 20 | **Cofre** | ✅ Apresenta (vault demo + ecossistema) | — | ✅ `render_cofre` | ❌ | **Web OK, Mobile falta** | `index.html:1872-1979`, `app.py:3786-3919` | Armazenamento criptografado |
| 21 | **Planos / Assinatura** | ✅ Apresenta (FAQ "gratuito?") | — | ✅ `render_planos` + Mercado Pago | ❌ | **Web OK, Mobile falta** | `index.html:4208-4212`, `app.py:2886-3476` | Planos, upgrade, pagamento |
| 22 | **Quem Sou Eu** | ✅ Apresenta (feature card) | — | ⚠️ `render_preferencias` (heading "Minha Essência") | ❌ | **Web OK com divergência, Mobile falta** | `index.html:4000-4058`, `app.py:2783-2880` | Sidebar OK, heading errado |
| 23 | **Sobre (institucional)** | ❌ (só footer) | ❌ (não tem página dedicada) | ✅ `render_sobre` (não está no menu) | ❌ | **Web incompleto, Mobile falta** | `app.py:3922-3950` | Existe mas não é acessível |
| 24 | **Admin (painel)** | — | — | ✅ `render_admin_panel` | ❌ | **Web OK** | `app.py:3954-3969` | Interno, não deve ser público |
| 25 | **Modo Visitante** | ❌ | — | ✅ `app.py:5603-5700` | ❌ | **Web OK, Mobile falta** | `app.py:5603-5700` | Acesso de convidados com chave |
| 26 | **Blog / Insights** | ✅ Link no footer | ✅ `/insights/` (3 artigos) | ❌ | ❌ | **Site OK, App falta** | `index.html:4246`, `insights/` | Blog é exclusivo do site |
| 27 | **Páginas Legais** | ❌ (só link futuro) | ✅ `/legais/politicaprivacidade.html` | ✅ `legal_texts.py` | ❌ | **Site + Web OK, Mobile falta** | `legais/politicaprivacidade.html`, `legal_texts.py` | LGPD, termos |
| 28 | **FAQ** | ✅ Embutida (8 perguntas) | — | ❌ (não existe no app) | ❌ | **Landing OK, App + Mobile falta** | `index.html:4166-4212` | Self-service |
| 29 | **SEO** | ✅ Schema.org, sitemap, robots | ✅ Sitemap + robots | ❌ (Streamlit não indexa) | ❌ | **Site OK** | `index.html:32-41`, `sitemap.xml`, `robots.txt` | Site é indexável |
| 30 | **Busca** | ❌ | ❌ | ❌ | ❌ | **Falta em todas** | — | Nenhuma camada tem busca |
| 31 | **Notificações Push** | — | — | ❌ (não é possível no Streamlit) | ❌ | **Falta em ambas** | — | Mobile precisa implementar |
| 32 | **Câmera / Galeria Nativa** | — | — | ❌ (só upload de arquivo) | ❌ | **Falta em ambas** | — | Mobile precisa implementar |
| 33 | **Deep Links** | — | — | ❌ | ❌ | **Falta em ambas** | — | Convites, memorial público |
| 34 | **Biometria** | — | — | ❌ | ❌ | **Falta em ambas** | — | Impressão digital, Face ID |
| 35 | **Compartilhamento Nativo** | — | — | ❌ (só link) | ❌ | **Falta em ambas** | — | WhatsApp, fotos nativas |
| 36 | **Offline** | — | — | ❌ | ❌ | **Falta em ambas** | — | Funcionamento sem internet |
| 37 | **Detecção Automática** | — | — | ❌ | ❌ | **Falta em ambas** | — | Fotos no dispositivo |
| 38 | **WorkManager** | — | — | ❌ | ❌ | **Falta em ambas** | — | Notificações agendadas |
| 39 | **Datas Importantes** | ❌ | — | ✅ `app.py:3493-3600` | ❌ | **Web OK, Mobile falta** | `app.py:3493-3600` | Dentro de Mensagens |
| 40 | **Convites Memorial (WhatsApp)** | ❌ | — | ✅ `memorial.py:867-944` | ❌ | **Web OK, Mobile falta** | `memorial.py:867-944` | Link de convite |
| 41 | **Hero (carrossel histórias)** | ✅ 8 histórias | — | ❌ | ❌ | **Landing OK** | `index.html:3228-3265` | Exclusivo da Landing |

---

## 5. Funcionalidades Exclusivas do Site

Estas funcionalidades pertencem exclusivamente ao Site (Landing + páginas internas) e **não devem ser implementadas no Mobile**:

| # | Funcionalidade | Onde | Motivo |
|---|---|---|---|
| S1 | **Hero com carrossel de histórias** | Landing | Apresentação do conceito, não é funcionalidade do produto |
| S2 | **Seção Problema** | Landing | Contextualização, não é funcionalidade |
| S3 | **Seção "Por que as histórias desaparecem"** | Landing | Reflexão, não é funcionalidade |
| S4 | **Seção "Imagine daqui a 30 anos"** | Landing | Projeção de valor, não é funcionalidade |
| S5 | **Manifesto da plataforma** | Landing | Posicionamento, não é funcionalidade |
| S6 | **Seção "Pequenas Histórias"** | Landing | Exemplos inspiracionais |
| S7 | **Seção "Como funciona" (4 passos)** | Landing | Explicação do fluxo |
| S8 | **Seção "Família participa" com exemplo Natal 1998** | Landing | Demonstração de colaboração |
| S9 | **Ecossistema (10 tiles)** | Landing | Visão integrada da plataforma |
| S10 | **Transformação foto→história e vídeo→história** | Landing | Demonstração visual do valor |
| S11 | **FAQ** | Landing | Suporte self-service (pode ser linkada do app) |
| S12 | **SEO** | `sitemap.xml`, `robots.txt`, `index.html` | Indexação no Google |
| S13 | **Schema.org (JSON-LD)** | `index.html` | Dados estruturados para busca |
| S14 | **Blog / Insights** | `/insights/` | Conteúdo editorial, autoridade |
| S15 | **Páginas Legais** | `/legais/` | LGPD, termos de uso |
| S16 | **Open Graph / Twitter Cards** | `index.html` | Compartilhamento em redes sociais |

---

## 6. Funcionalidades Exclusivas do Mobile (futuro)

Estas funcionalidades pertencem exclusivamente ao Aplicativo Mobile e **não devem ser implementadas no Site**:

| # | Funcionalidade | Motivo | Prioridade |
|---|---|---|---|
| M1 | **Notificações Push** | Engajamento, lembretes do Curador, Novidades | **Crítica** |
| M2 | **Câmera Nativa** | Capturar fotos diretamente para as histórias | **Crítica** |
| M3 | **Galeria Nativa** | Acessar fotos do dispositivo | **Crítica** |
| M4 | **Biometria** | Login rápido e seguro | Alta |
| M5 | **Deep Links** | Convites diretos (WhatsApp, links) | Alta |
| M6 | **Compartilhamento Nativo** | Compartilhar histórias em outros apps | Alta |
| M7 | **WorkManager** | Agendamento de Mensagens para o Futuro | Média |
| M8 | **Detecção Automática de Momentos** | Sugerir histórias baseadas em fotos do dispositivo | Média |
| M9 | **Offline Parcial** | Ler histórias sem internet | Média |
| M10 | **Widget (Android/iOS)** | Atalho para nova história na tela inicial | Baixa |
| M11 | **App Shortcuts** | Acesso rápido a funções específicas | Baixa |

---

## 7. Funcionalidades que DEVEM Existir em Ambos

Estas funcionalidades devem estar presentes tanto no App Web (Streamlit) quanto no App Mobile (Flutter), com paridade de experiência:

| # | Funcionalidade | Web (Streamlit) | Mobile (Flutter) | Prioridade Mobile |
|---|---|---|---|---|
| P1 | **Login / Cadastro** | ✅ | ❌ | **Crítica** |
| P2 | **Minha História** | ✅ | ❌ | **Crítica** |
| P3 | **Curador de Histórias** | ✅ | ❌ | **Crítica** |
| P4 | **Pessoas / Contatos** | ✅ | ❌ | **Crítica** |
| P5 | **Fotos** | ✅ | ❌ | **Crítica** |
| P6 | **Vídeos** | ✅ | ❌ | **Crítica** |
| P7 | **Linha do Tempo** | ✅ | ❌ | **Crítica** |
| P8 | **Memorial** | ✅ | ❌ | **Crítica** |
| P9 | **Compartilhadas comigo** | ✅ | ❌ | **Crítica** |
| P10 | **Novidades** | ✅ | ❌ | **Crítica** |
| P11 | **Mensagens para o Futuro** | ✅ | ❌ | **Alta** |
| P12 | **Cofre** | ✅ | ❌ | **Alta** |
| P13 | **Quem Sou Eu** | ⚠️ (heading "Minha Essência") | ❌ | **Alta** |
| P14 | **Planos / Assinatura** | ✅ | ❌ | **Alta** |
| P15 | **Login Visitante** | ✅ | ❌ | **Média** |
| P16 | **Explorador de Histórias** | ✅ | ❌ | **Média** |
| P17 | **Datas Importantes** | ✅ | ❌ | **Média** |
| P18 | **Sobre (institucional)** | ⚠️ (existe sem menu) | ❌ | **Baixa** |
| P19 | **FAQ** | ❌ | ❌ | **Baixa** (pode ser link) |

---

## 8. Funcionalidades que Ainda Faltam

### 8.1 No Mobile (Flutter) — ordem de implementação recomendada

| # | Funcionalidade | Prioridade | Motivo | Dependências |
|---|---|---|---|---|
| F1 | **Login + Cadastro** | **Crítica** | Sem autenticação não existe produto | — |
| F2 | **Minha História + Curador** | **Crítica** | Core do produto, primeira ação do usuário | F1 |
| F3 | **Pessoas + Fotos + Vídeos** | **Crítica** | Organização da árvore familiar | F1, F2 |
| F4 | **Linha do Tempo** | **Crítica** | Visualização do conteúdo criado | F2, F3 |
| F5 | **Memorial** | **Crítica** | Diferencial da plataforma | F1, F2, F3 |
| F6 | **Notificações Push (Novidades)** | **Crítica** | Engajamento, retenção | F1, F2 |
| F7 | **Compartilhadas comigo** | **Crítica** | Colaboração familiar | F1 |
| F8 | **Contribuições** | **Crítica** | Moderação de conteúdo familiar | F1, F2 |
| F9 | **Mensagens para o Futuro** | **Alta** | Landing já vende, app web já tem | F1, F2 |
| F10 | **Cofre** | **Alta** | Landing já vende, app web já tem | F1 |
| F11 | **Quem Sou Eu** | **Alta** | Fundamental para personalização e IA | F1 |
| F12 | **Planos / Assinatura** | **Alta** | Monetização | F1 |
| F13 | **Câmera Nativa** | **Alta** | Captura direta de fotos | — |
| F14 | **Deep Links (convites)** | **Alta** | Compartilhamento de memorial | F1 |
| F15 | **Login Visitante** | **Média** | Acesso de convidados | F1 |
| F16 | **Busca** | **Média** | Escalabilidade do conteúdo | F2-F11 |
| F17 | **Biometria** | **Média** | Login rápido | F1 |
| F18 | **Compartilhamento Nativo** | **Média** | Exportar histórias | F1-F11 |
| F19 | **Offline** | **Média** | Leitura sem internet | F1-F11 |
| F20 | **Datas Importantes** | **Média** | Agendamento de mensagens | F9 |
| F21 | **Detecção Automática** | **Baixa** | Sugestão de histórias | F13 |
| F22 | **Widget / App Shortcuts** | **Baixa** | Atalhos de acesso | F1-F11 |

### 8.2 No App Web (Streamlit) — correções necessárias

| # | Funcionalidade | Problema | Prioridade |
|---|---|---|---|
| W1 | **FAQ no app** | Não existe, usuário não tem suporte self-service | Média |
| W2 | **Link para o site** | App não tem link para Landing, Blog, FAQ, Legais | **Crítica** |
| W3 | **Heading "Minha Essência" → "Quem Sou Eu"** | Divergência com sidebar | Média |
| W4 | **Heading "Cofre Digital" → "Cofre"** | Divergência com sidebar | Média |
| W5 | **Heading "Memorial de Legados" → "Memorial"** | Divergência com sidebar | Média |
| W6 | **Sobre no menu** | `render_sobre` existe mas não está acessível | Média |
| W7 | **Fundo escuro** | App usa fundo claro, site usa escuro | Média |

### 8.3 No Site — lacunas

| # | Funcionalidade | Problema | Prioridade |
|---|---|---|---|
| S1 | **Página "Sobre" dedicada** | Não existe, só `render_sobre` no app | Média |
| S2 | **Página de parceiros** | Não existe | Baixa |
| S3 | **Página de downloads** | Não existe | Baixa |
| S4 | **Memorial público** | Não existe (convites são via link) | Baixa |
| S5 | **Mais artigos no blog** | Só 3 artigos | Média |

---

## 9. Inconsistências Encontradas

### 9.1 Nomenclatura

| # | Inconsistência | Onde | Severidade | Evidência |
|---|---|---|---|---|
| I1 | "Quem Sou Eu" (sidebar) vs "Minha Essência" (heading) | App Web | **Média** | `app.py:2784` |
| I2 | "Cofre" (sidebar) vs "Cofre Digital" (heading) | App Web | **Média** | `app.py:3787` |
| I3 | "Memorial" (sidebar) vs "Memorial de Legados" (heading) | App Web | Média | `memorial.py:287` |
| I4 | "Compartilhadas comigo" (Landing) vs "Compartilhadas Comigo" (app) | Landing vs App | Baixa | Capitalização |
| I5 | "Planos" (Landing) vs "Meu plano" (app sidebar) | Landing vs App | Baixa | Intencional (contextos diferentes) |

### 9.2 Experiência

| # | Inconsistência | Onde | Severidade | Impacto |
|---|---|---|---|---|
| I6 | Fundo escuro (`#080014`) no site vs fundo claro (`#f5f5f5`) no app | Site vs App | **Alta** | Quebra identidade visual |
| I7 | App sem link de volta para o site | App | **Crítica** | Usuário preso no app |
| I8 | App sem link para o blog | App | Alta | Conteúdo editorial inacessível |
| I9 | App sem FAQ | App | Média | Sem suporte self-service |
| I10 | Landing comunica 15 features; app tem 7 no expander "Mais" | Landing vs App | Média | Descoberta de produto |
| I11 | Hero do site (carrossel stories) sem equivalente no app | Site | Média | App não mostra stories |

### 9.3 Tecnologia

| # | Inconsistência | Detalhe | Severidade |
|---|---|---|---|
| I12 | Streamlit não suporta notificações push | App web limitado | **Alta** (Mobile precisa resolver) |
| I13 | Streamlit não suporta câmera nativa | App web limitado | **Alta** (Mobile precisa resolver) |
| I14 | Streamlit tem fundo claro por padrão | Difícil de escurecer completamente | Média |
| I15 | App não tem animações (glassmorphism, pulse, glow) | App mais estático | Baixa |

---

## 10. Roadmap Recomendado

Após esta sprint, a ordem recomendada de implementação é:

### Sprint 6.1 — Unificação Visual do App Web
- Escurecer fundo do app (`#080014`)
- Adicionar Cormorant Garamond em títulos
- Corrigir footer ("Memórias vivas" → alinhado com Brand Book)
- Adicionar glassmorphism onde possível

### Sprint 6.2 — Navegação Cruzada
- Adicionar link do app para a Landing
- Adicionar link do app para o Blog
- Adicionar link do app para FAQ e Páginas Legais
- Adicionar "Sobre a aEterna" no sidebar do app

### Sprint 6.3 — Correção de Nomenclatura Interna
- "Minha Essência" → "Quem Sou Eu" (`app.py:2784`)
- "Cofre Digital" → "Cofre" (`app.py:3787`)
- "Memorial de Legados" → "Memorial" (`memorial.py:287`)

### Sprint 6.x — Construção do Mobile (Flutter)
- **Sprint M1:** Autenticação (login, cadastro, visitante, recuperação)
- **Sprint M2:** Minha História + Curador
- **Sprint M3:** Pessoas + Fotos + Vídeos + Linha do Tempo
- **Sprint M4:** Memorial + Compartilhadas + Novidades + Contribuições
- **Sprint M5:** Mensagens para o Futuro + Cofre
- **Sprint M6:** Quem Sou Eu + Planos
- **Sprint M7:** Notificações Push + Câmera + Galeria
- **Sprint M8:** Deep Links + Biometria + Compartilhamento Nativo
- **Sprint M9:** Offline + Detecção Automática
- **Sprint M10:** Refatoração e Performance

---

## Apêndice A — Checklist de Sucesso

Um novo desenvolvedor, ao ler este documento, conseguirá responder:

| Pergunta | Resposta |
|---|---|
| O que é a aEterna? | "O lugar onde a história da sua família continua sendo construída, compartilhada e preservada ao longo das gerações." |
| Qual é o papel de cada produto? | Landing = apresentar e converter. Site = suporte (blog, legal, SEO). App Web = produto funcional atual. Mobile = produto principal futuro. |
| O que pertence ao Site? | Hero, problema, manifesto, FAQ, blog, páginas legais, SEO, Schema.org — tudo que é apresentação e conteúdo editorial. |
| O que pertence ao Mobile? | Notificações push, câmera nativa, biometria, deep links, compartilhamento nativo, offline, detecção automática — tudo que é experiência nativa. |
| O que pertence a ambos? | Minha História, Curador, Pessoas, Fotos, Vídeos, Linha do Tempo, Memorial, Compartilhadas, Novidades, Contribuições, Mensagens Futuras, Cofre, Quem Sou Eu, Planos, Login, Cadastro — toda funcionalidade core do produto. |
| O que falta implementar? | Mobile inteiro (Flutter) + correções de nomenclatura no app web + links de navegação cruzada. |
| Qual é a ordem correta das próximas evoluções? | 6.1 (visual web) → 6.2 (navegação) → 6.3 (nomenclatura) → M1 a M10 (Mobile). |

---

> **Este documento é a referência arquitetural oficial da plataforma aEterna. Nenhuma funcionalidade nova deve ser desenvolvida sem antes consultar esta matriz para determinar em qual camada ela pertence.**
