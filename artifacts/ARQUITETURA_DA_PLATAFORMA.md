# ARQUITETURA OFICIAL DA PLATAFORMA — aEterna

> Documento oficial de arquitetura de produto da aEterna. Define a estrutura da plataforma, o papel de cada camada, as entidades centrais, os módulos oficiais e as regras de evolução. Este documento substitui qualquer entendimento anterior sobre a arquitetura e serve como fonte de verdade para toda a equipe.

---

## 1. Visão Oficial da Plataforma

> **A aEterna é o lugar onde a história da sua família continua sendo construída, compartilhada e preservada ao longo das gerações.**

Existe **apenas um produto**: a **plataforma aEterna**.

Landing, Site Institucional, App Web (Streamlit) e App Mobile (Flutter) são **interfaces diferentes da mesma plataforma**. Nenhuma camada deve evoluir como produto separado.

A plataforma é composta por **quatro camadas** que se complementam:

```
                    ┌──────────────────────────────────────────────┐
                    │         PLATAFORMA aEterna                  │
                    │                                              │
                    │  "O lugar onde a história da sua família    │
                    │   continua sendo construída, compartilhada  │
                    │   e preservada ao longo das gerações"       │
                    └─────────────────────┬────────────────────────┘
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                │              │              │               │
          ▼                ▼              ▼              ▼               ▼
   ┌────────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  LANDING   │  │    SITE      │  │WEB APP   │  │  MOBILE  │  │ INFRA    │
   │ index.html │  │ institucional│  │Streamlit  │  │  Flutter │  │ backend  │
   │ aeterna-   │  │ /insights/   │  │aeterna.   │  │ reposit.│  │ banco,   │
   │ legado.com │  │ /legais/ FAQ │  │streamlit  │  │ separado │  │ storage  │
   │ .br        │  │ SEO          │  │.app       │  │          │  │ IA       │
   └────────────┘  └──────────────┘  └──────────┘  └──────────┘  └──────────┘
```

---

## 2. Repositórios Oficiais

A plataforma aEterna é mantida em **dois repositórios independentes**, cada um com seu papel:

### Repositório Web

```
URL:  https://github.com/dcarriao/aeterna
Path: D:\aeterna\
```

**Papel:** Contém o código-fonte de:
- **Landing** (`index.html`) — site institucional público
- **Site Institucional** (`/insights/`, `/legais/`, FAQ embutida)
- **App Web Streamlit** (`app.py` + componentes + utils + estilos)
- **Infraestrutura** (banco SQLite, storage, IA, pagamentos)
- **Assets** (imagens, logo, ícones)
- **Artigos** (`/artigos/`)
- **SEO** (sitemap, robots, Schema.org)
- **Documentação** (`/artifacts/`)

**Tecnologias:** Python, Streamlit, HTML, CSS, JavaScript, SQLite

### Repositório Mobile

```
URL:  https://github.com/dcarriao/aeterna_mobile
```

**Papel:** Contém o código-fonte do:
- **App Mobile Flutter** — principal experiência de uso diário

**Tecnologias:** Dart, Flutter

### Relação entre os repositórios

Ambos os repositórios implementam o **mesmo produto** (a plataforma aEterna) em **interfaces diferentes**. Não há subordinação entre eles. O Web App é a **referência funcional atual** (mais completo no momento). O Mobile é o **destino de paridade** (deve espelhar todas as funcionalidades core).

---

## 3. Camadas da Plataforma

### 3.1 Landing (`index.html`)

**URL:** `https://www.aeternalegado.com.br/`
**Repositório:** Web (`/`)
**Tecnologia:** HTML + CSS + JavaScript puro

**Missão:** Fazer alguém se apaixonar pela ideia.

| O que faz | O que NÃO faz |
|-----------|---------------|
| Apresenta o problema ("fotos sobrevivem, histórias quase nunca") | Não cria conteúdo |
| Demonstra o conceito (carrossel de 8 histórias) | Não autentica usuários |
| Explica o Curador (diálogo de 6 turnos) | Não armazena dados |
| Lista funcionalidades (15 cards + ecossistema de 10 tiles) | Não tem interação social |
| Apresenta o Memorial ("continuação da vida") | Não é o produto |
| Responde dúvidas (FAQ com 8 perguntas) | — |
| Converte visitante em usuário (CTAs) | — |

**Público:** Visitante (não logado)

### 3.2 Site Institucional

**URL:** `https://www.aeternalegado.com.br/insights/`, `/legais/`
**Repositório:** Web (`/insights/`, `/legais/`)
**Tecnologia:** HTML estático

**Missão:** Dar suporte ao produto com conteúdo, credibilidade e informação.

| Componente | URL | Função |
|------------|-----|--------|
| **Blog** (`/insights/`) | 3 artigos | Conteúdo editorial, SEO, autoridade |
| **Páginas Legais** (`/legais/`) | 1 página | LGPD, termos de uso |
| **FAQ** | Embutido na Landing | Suporte self-service |
| **SEO** | sitemap.xml, robots.txt, Schema.org | Indexação no Google |
| **Artigos** (`/artigos/`) | Redireciona para `/insights/` | Conteúdo duplicado (legado) |

**Público:** Visitante + Usuário

**Expansão futura:** Páginas de parceiros, downloads, sobre (dedicado), memorial público.

### 3.3 App Web Streamlit

**URL:** `https://aeterna.streamlit.app/`
**Repositório:** Web (`app.py`)
**Tecnologia:** Python + Streamlit

**Missão:** Ser o cliente oficial web da plataforma. Interface completa, referência funcional atual, administração e funcionalidades avançadas.

| Característica | Detalhe |
|----------------|---------|
| **Estado** | ✅ Completo (5881 linhas, 19 seções) |
| **Função** | Cliente oficial desktop/web |
| **Referência** | Fonte funcional atual para todas as features core |
| **Administração** | Painel admin incluso |
| **Desktop** | Experiência completa para tela grande |
| **Streamlit** | Framework Python com interface web |

**Funcionalidades completas:**
- Autenticação (login, cadastro, visitante, recuperação)
- Minha História + Curador
- Pessoas + Fotos + Vídeos + Linha do Tempo
- Memorial + Compartilhadas + Novidades + Contribuições
- Mensagens para o Futuro + Cofre
- Quem Sou Eu + Planos
- Admin + Modo Visitante

**Limitações atuais (devidas ao Streamlit):**
- Sem notificações push nativas
- Sem acesso a câmera/galeria nativa
- Sem biometria
- Sem deep links
- Sem funcionamento offline
- Sem animações elaboradas

**Público:** Usuário logado (qualquer dispositivo com browser)

### 3.4 App Mobile Flutter

**URL:** `https://github.com/dcarriao/aeterna_mobile`
**Repositório:** Mobile (repositório separado)
**Tecnologia:** Dart + Flutter

**Missão:** Ser a principal experiência de uso diário da plataforma. Onde a família vive, onde as histórias acontecem, onde tudo é criado — com notificações nativas, câmera, biometria e deep links.

| Característica | Detalhe |
|----------------|---------|
| **Estado** | Em desenvolvimento (repositório separado) |
| **Função** | Cliente mobile oficial |
| **Experiência** | Principal uso diário da família |
| **Nativo** | Notificações push, câmera, galeria, biometria |
| **Portabilidade** | Android + iOS |

**Deve conter (paridade com Web):**
- Autenticação com biometria
- Minha História + Curador (adaptado para mobile)
- Pessoas + Fotos (com câmera nativa) + Vídeos
- Linha do Tempo (touch-optimized)
- Memorial (com deep links para convites)
- Compartilhadas + Novidades (com push)
- Contribuições
- Mensagens para o Futuro (com WorkManager)
- Cofre (com biometria)
- Quem Sou Eu + Planos

**Deve conter (exclusivo Mobile):**
- Notificações push nativas
- Câmera e galeria nativa
- Biometria (impressão digital, Face ID)
- Deep links (convites, memorial)
- Compartilhamento nativo (WhatsApp, fotos)
- Offline parcial
- Widget (Android/iOS)

**Público:** Usuário logado (smartphone, tablet)

---

## 4. Princípio Oficial

> **Existe apenas um produto: a plataforma aEterna.**

Landing, Site, Web App e Mobile são **interfaces diferentes** da mesma plataforma. Nenhuma camada deve evoluir como produto separado.

### Implicações do princípio

1. **Toda funcionalidade core deve existir em ambas as interfaces** (Web e Mobile), salvo justificativa técnica explícita.
2. **Funcionalidades exclusivas** de uma interface são exceções intencionais (ex: câmera é exclusiva do Mobile; SEO é exclusivo do Site).
3. **Nomenclatura deve ser idêntica** em todas as camadas que comunicam a mesma feature.
4. **Identidade visual deve ser consistente** entre Web e Mobile (cores, tipografia, ícones, botões).
5. **Nova funcionalidade** deve responder em qual(is) camada(s) será implementada antes de ser construída.
6. **Web App é a referência funcional atual** — o que existe no Web deve existir no Mobile (paridade).
7. **Mobile é a principal experiência de uso diário** — o Mobile deve ser priorizado para funcionalidades de uso frequente.
8. **Landing e Site** comunicam o que ambas as interfaces entregam — nunca devem prometer algo que Web e Mobile não têm.

---

## 5. Entidades Centrais da Plataforma

### 5.1 História / Memória

| Atributo | Valor |
|----------|-------|
| **Definição** | Unidade básica de conteúdo da plataforma. Um registro de um momento, evento ou lembrança familiar, com contexto (pessoas, data, local, significado). |
| **Onde aparece** | Landing (carrossel, exemplos), Web App (Minha História, Curador, Linha do Tempo), Mobile (idem) |
| **Relações** | Pessoa (quem participou), Foto (imagem associada), Vídeo (mídia associada), Contribuição (versões da família), Curador (estruturação) |
| **Core?** | ✅ **Core da plataforma** |

### 5.2 Pessoa

| Atributo | Valor |
|----------|-------|
| **Definição** | Ser humano que aparece nas histórias da família. Pode estar vivo ou ter falecido. |
| **Onde aparece** | Landing (showcase Pessoas), Web App (Pessoas, associação a memórias), Mobile (idem) |
| **Relações** | História (participou), Memorial (perfil dedicado), Família (grupo de pessoas relacionadas) |
| **Core?** | ✅ **Core da plataforma** |

### 5.3 Família

| Atributo | Valor |
|----------|-------|
| **Definição** | Grupo de pessoas relacionadas que compartilham histórias na plataforma. Unidade social da aEterna. |
| **Onde aparece** | Landing (seção "A família participa"), Web App (Compartilhadas, Contribuições, Novidades), Mobile (idem) |
| **Relações** | Pessoa (membros), História (conteúdo compartilhado), Compartilhamento (acesso), Convite (crescimento) |
| **Core?** | ✅ **Core da plataforma** |

### 5.4 Foto

| Atributo | Valor |
|----------|-------|
| **Definição** | Imagem associada a uma história, com contexto (quem aparece, quando, onde, o que estava acontecendo). |
| **Onde aparece** | Landing (transformação foto→história), Web App (Fotos, associação a memórias), Mobile (câmera + galeria) |
| **Relações** | História (pertence a), Pessoa (quem aparece) |
| **Core?** | ✅ **Core da plataforma** |

### 5.5 Vídeo

| Atributo | Valor |
|----------|-------|
| **Definição** | Mídia em vídeo associada a uma história, com contexto. |
| **Onde aparece** | Landing (transformação vídeo→história), Web App (Vídeos), Mobile (câmera + galeria) |
| **Relações** | História (pertence a), Pessoa (quem aparece) |
| **Core?** | ✅ **Core da plataforma** |

### 5.6 Curador

| Atributo | Valor |
|----------|-------|
| **Definição** | Guia silencioso da plataforma que faz perguntas para ajudar a pessoa a transformar uma lembrança solta em uma história com pessoas, contexto, datas e aprendizados. |
| **Onde aparece** | Landing (seção dedicada + diálogo exemplo), Web App (render_assistente, render_curador_memoria_primeiro), Mobile (idem) |
| **Relações** | História (estrutura a criação), Pessoa (identifica participantes), Explorador (modo pergunta) |
| **Core?** | ✅ **Core da plataforma** |

### 5.7 Explorador de Histórias

| Atributo | Valor |
|----------|-------|
| **Definição** | Modo do Curador que responde perguntas sobre uma pessoa específica usando apenas o que foi registrado — sem inventar nada. |
| **Onde aparece** | Landing (ecossistema), Web App (assistente_ia.py, modo visitante), Mobile (futuro) |
| **Relações** | Memorial (aplicado a perfis de falecidos), Curador (mesmo motor), Pessoa (objeto da exploração) |
| **Core?** | ✅ **Core da plataforma** |

### 5.8 Memorial

| Atributo | Valor |
|----------|-------|
| **Definição** | Espaço dedicado à história de uma pessoa que faleceu. Construído pela família em conjunto. Continuação da vida daquela pessoa através das histórias que ela deixou. |
| **Onde aparece** | Landing (seção dedicada + exemplo), Web App (memorial.py: lista, criar, página, curador), Mobile (futuro) |
| **Relações** | Pessoa (homenageado), Família (construtoras), História (conteúdo), Explorador (perguntas sobre a pessoa), Convite (WhatsApp) |
| **Core?** | ✅ **Core da plataforma** |

### 5.9 Mensagem para o Futuro

| Atributo | Valor |
|----------|-------|
| **Definição** | Mensagem (texto, áudio ou vídeo) que o usuário grava hoje para ser aberta em uma data futura. |
| **Onde aparece** | Landing (exemplo 2018→2036, ecossistema), Web App (render_agendamentos, dentro de Mensagens), Mobile (futuro, com WorkManager) |
| **Relações** | Pessoa (autor e destinatários), Data (abertura agendada) |
| **Core?** | ✅ **Core da plataforma** |

### 5.10 Cofre

| Atributo | Valor |
|----------|-------|
| **Definição** | Armazenamento criptografado de itens sensíveis da família. |
| **Onde aparece** | Landing (vault demo, ecossistema), Web App (render_cofre), Mobile (futuro, com biometria) |
| **Relações** | Pessoa (dono), Criptografia (segurança) |
| **Core?** | ✅ **Core da plataforma** |

### 5.11 Contribuição

| Atributo | Valor |
|----------|-------|
| **Definição** | Adição de conteúdo (foto, vídeo, texto) por um familiar a uma história que não é dele, sujeita à aprovação do dono. |
| **Onde aparece** | Landing (exemplo Natal 1998), Web App (render_contribuicoes_pendentes), Mobile (futuro) |
| **Relações** | História (alvo da contribuição), Pessoa (autor), Família (contexto), Compartilhamento (permissão) |
| **Core?** | ✅ **Core da plataforma** |

### 5.12 Compartilhamento

| Atributo | Valor |
|----------|-------|
| **Definição** | Ato de definir a visibilidade de uma história (privado, contatos, seletivo). |
| **Onde aparece** | Landing (seção "A família participa"), Web App (compartilhar história), Mobile (futuro, com compartilhamento nativo) |
| **Relações** | História (objeto), Pessoa (alvo do compartilhamento), Contribuição (consequência) |
| **Core?** | ✅ **Core da plataforma** |

### 5.13 Convite

| Atributo | Valor |
|----------|-------|
| **Definição** | Link ou mensagem enviada para um familiar convidá-lo a participar de uma história ou Memorial. |
| **Onde aparece** | Web App (memorial.py:867-944 — convite WhatsApp), Mobile (futuro, com deep links) |
| **Relações** | Memorial (contexto), Pessoa (convidado), Compartilhamento (consequência) |
| **Core?** | ✅ **Core da plataforma** |

### 5.14 Plano

| Atributo | Valor |
|----------|-------|
| **Definição** | Nível de assinatura que define limites de uso (memórias, mídias, contribuições, contatos). |
| **Onde aparece** | Landing (FAQ "gratuito?"), Web App (render_planos + Mercado Pago), Mobile (futuro, com Google Play/App Store) |
| **Relações** | Usuário (assinante), Limites (memórias, mídias, contatos) |
| **Core?** | ✅ **Core da plataforma** |

### 5.15 Visitante

| Atributo | Valor |
|----------|-------|
| **Definição** | Usuário com acesso limitado a uma história ou Memorial específico, através de chave de acesso. |
| **Onde aparece** | Web App (app.py:5603-5700 — modo visitante), Mobile (futuro) |
| **Relações** | Memorial (contexto do acesso), Pessoa (relação com o homenageado) |
| **Core?** | ✅ **Core da plataforma** |

---

## 6. Módulos Oficiais

### Legenda

| Coluna | Significado |
|--------|-------------|
| **Landing** | Apresenta? (✅ apresenta / — não se aplica) |
| **Site** | Explica ou suporta? (✅ sim / — não se aplica) |
| **Web App** | Executa funcionalidade? (✅ sim / ❌ não / ⚠️ parcial) |
| **Mobile** | Executa funcionalidade? (✅ sim / ❌ não / 📝 planejado) |
| **Tipo** | Classificação do módulo |

### Matriz de módulos

| # | Módulo | Landing | Site | Web App | Mobile | Tipo | Observação |
|---|---|---|---|---|---|---|---|
| 1 | **Minha História** | ✅ Apresenta | — | ✅ Executa | 📝 Planejado | **Core** | Módulo principal de criação |
| 2 | **Curador de Histórias** | ✅ Apresenta | ✅ FAQ explica | ✅ Executa | 📝 Planejado | **Core** | Guia silencioso de perguntas |
| 3 | **Explorador de Histórias** | ✅ Apresenta (ecossistema) | — | ✅ Executa | 📝 Planejado | **Core** | Modo pergunta sobre pessoa |
| 4 | **Pessoas** | ✅ Apresenta (showcase) | — | ✅ Executa | 📝 Planejado | **Core** | Cadastro e gestão de contatos |
| 5 | **Fotos** | ✅ Apresenta (transformação) | — | ✅ Executa | 📝 Planejado | **Core** | Upload com contexto |
| 6 | **Vídeos** | ✅ Apresenta (transformação) | — | ✅ Executa | 📝 Planejado | **Core** | Upload com limite por plano |
| 7 | **Linha do Tempo** | ✅ Apresenta (exemplo) | — | ✅ Executa (tab) | 📝 Planejado | **Core** | Visualização cronológica |
| 8 | **Compartilhadas comigo** | ✅ Apresenta (ecossistema) | — | ✅ Executa | 📝 Planejado | **Core** | Histórias recebidas |
| 9 | **Contribuições** | ✅ Apresenta (ecossistema) | — | ✅ Executa | 📝 Planejado | **Core** | Moderação familiar |
| 10 | **Novidades** | ✅ Apresenta (feature card) | — | ✅ Executa | 📝 Planejado | **Core** | Feed de notificações |
| 11 | **Memorial** | ✅ Apresenta (seção + exemplo) | ✅ FAQ explica | ✅ Executa | 📝 Planejado | **Core** | Continuação da vida |
| 12 | **Mensagens para o Futuro** | ✅ Apresenta (exemplo) | — | ✅ Executa | 📝 Planejado | **Core** | Agendamento de mensagens |
| 13 | **Cofre** | ✅ Apresenta (vault demo) | — | ✅ Executa | 📝 Planejado | **Core** | Armazenamento criptografado |
| 14 | **Quem Sou Eu** | ✅ Apresenta (ecossistema) | — | ✅ Executa (com divergência) | 📝 Planejado | **Core** | Preferências do usuário |
| 15 | **Planos** | ✅ Apresenta (FAQ) | — | ✅ Executa | 📝 Planejado | **Core** | Assinatura e pagamento |
| 16 | **Login / Cadastro** | ❌ (só CTA) | — | ✅ Executa | 📝 Planejado | **Core** | Autenticação |
| 17 | **Login Visitante** | ❌ | — | ✅ Executa | 📝 Planejado | **Core** | Acesso por chave |
| 18 | **Recuperação de Senha** | ❌ | — | ✅ Executa | 📝 Planejado | **Core** | Suporte ao login |
| 19 | **Notificações Push** | — | — | ❌ (não é possível) | 📝 Planejado | **Exclusivo Mobile** | Engajamento nativo |
| 20 | **Câmera Nativa** | — | — | ❌ (não é possível) | 📝 Planejado | **Exclusivo Mobile** | Captura direta |
| 21 | **Galeria Nativa** | — | — | ❌ (não é possível) | 📝 Planejado | **Exclusivo Mobile** | Acesso a fotos |
| 22 | **Biometria** | — | — | ❌ (não é possível) | 📝 Planejado | **Exclusivo Mobile** | Login rápido |
| 23 | **Deep Links** | — | — | ❌ | 📝 Planejado | **Exclusivo Mobile** | Convites diretos |
| 24 | **Compartilhamento Nativo** | — | — | ❌ | 📝 Planejado | **Exclusivo Mobile** | Exportar histórias |
| 25 | **Offline Parcial** | — | — | ❌ | 📝 Planejado | **Exclusivo Mobile** | Leitura sem internet |
| 26 | **Detecção Automática** | — | — | ❌ | 📝 Planejado | **Exclusivo Mobile** | Sugestão de histórias |
| 27 | **WorkManager** | — | — | ❌ | 📝 Planejado | **Exclusivo Mobile** | Notificações agendadas |
| 28 | **Widget (Android/iOS)** | — | — | ❌ | 📝 Planejado | **Exclusivo Mobile** | Atalho tela inicial |
| 29 | **Blog / Insights** | ✅ Link no footer | ✅ Executa | ❌ | ❌ | **Exclusivo Site** | Conteúdo editorial |
| 30 | **Páginas Legais** | ❌ (só link futuro) | ✅ Executa | ✅ Executa | 📝 Planejado | **Core + Site** | LGPD, termos |
| 31 | **FAQ** | ✅ Embutida | — | ❌ | ❌ | **Exclusivo Landing** | Suporte self-service |
| 32 | **SEO** | ✅ Schema, sitemap, robots | ✅ Sitemap + robots | ❌ (Streamlit) | ❌ | **Exclusivo Site** | Indexação |
| 33 | **Busca** | ❌ | ❌ | ❌ | 📝 Planejado | **Futuro** | Escalabilidade |
| 34 | **Admin** | — | — | ✅ Executa | ❌ | **Exclusivo Web** | Painel administrativo |
| 35 | **Datas Importantes** | ❌ | — | ✅ Executa | 📝 Planejado | **Core** (dentro de Mensagens) | Datas especiais |
| 36 | **Convites Memorial (WhatsApp)** | ❌ | — | ✅ Executa | 📝 Planejado | **Core** | Link de convite |
| 37 | **Modo Visitante** | ❌ | — | ✅ Executa | 📝 Planejado | **Core** | Acesso de convidados |
| 38 | **Sobre (institucional)** | ✅ Footer | ❌ (falta página) | ⚠️ Existe sem menu | ❌ | **Core** | Informações da empresa |

---

## 7. Fonte de Verdade

Para cada funcionalidade, existe uma **fonte funcional atual** (onde a implementação de referência está hoje) e um **destino de paridade** (onde deve ser espelhada).

| Funcionalidade | Fonte funcional atual | Destino de paridade | Status |
|---|---|---|---|
| Minha História | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Curador de Histórias | **Web App** (chat_luto.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Explorador de Histórias | **Web App** (assistente_ia.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Pessoas | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Fotos | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Vídeos | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Linha do Tempo | **Web App** (app.py) | Mobile | ✅ Web completo (tab), 📝 Mobile pendente |
| Compartilhadas comigo | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Contribuições | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Novidades | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Memorial | **Web App** (memorial.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Mensagens para o Futuro | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Cofre | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Quem Sou Eu | **Web App** (app.py) | Mobile | ⚠️ Web com divergência, 📝 Mobile pendente |
| Planos | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Login / Cadastro | **Web App** (app.py, login_compacto.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Login Visitante | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Recuperação de Senha | **Web App** (login_compacto.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Datas Importantes | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Convites Memorial | **Web App** (memorial.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Modo Visitante | **Web App** (app.py) | Mobile | ✅ Web completo, 📝 Mobile pendente |
| Notificações Push | — | **Mobile** | ❌ Web não suporta, 📝 Mobile pendente |
| Câmera Nativa | — | **Mobile** | ❌ Web não suporta, 📝 Mobile pendente |
| Biometria | — | **Mobile** | ❌ Web não suporta, 📝 Mobile pendente |
| Deep Links | — | **Mobile** | ❌ Ambos pendentes |
| Busca | — | **Mobile** (primeiro) | ❌ Ambos pendentes |

---

## 8. Regras de Evolução

Toda nova funcionalidade proposta deve responder às seguintes perguntas antes de ser implementada:

### 8.1 Checklist de nova funcionalidade

- [ ] **Pertence a qual camada?** (Landing / Site / Web App / Mobile / Mais de uma)
- [ ] **É core ou exclusiva?** (Core = deve existir em Web e Mobile / Exclusiva = justificativa técnica)
- [ ] **Existe no Web App?** (Se não, a referência funcional precisa ser criada primeiro)
- [ ] **Existe no Mobile?** (Se não, precisa ser adicionada ao Mobile)
- [ ] **Precisa ser comunicada na Landing?** (Se for core ou diferencial, sim)
- [ ] **Precisa aparecer no Site?** (Blog explicativo, FAQ, página legal)
- [ ] **Afeta o Brand Book?** (Muda posicionamento, promessa, valores?)
- [ ] **Afeta o Guia Editorial?** (Muda como histórias são escritas?)
- [ ] **Afeta a Matriz de Paridade?** (Adiciona ou remove funcionalidade da matriz)
- [ ] **Afeta a Direção Fotográfica?** (Requer novas imagens ou estilo?)
- [ ] **Afeta o Tom de Voz?** (Requer novo tom ou palavras?)
- [ ] **Afeta as Decisões de Marca?** (Precisa de novo ADR?)

### 8.2 Regras de implementação

1. **Funcionalidades core** devem ser implementadas primeiro no Web App (como referência) e depois espelhadas no Mobile (paridade).
2. **Funcionalidades exclusivas do Mobile** (câmera, push, biometria) devem ser documentadas na Matriz de Paridade como "Exclusivo Mobile".
3. **Funcionalidades exclusivas do Site** (blog, SEO) não precisam de equivalente no Mobile.
4. **Nomenclatura** deve ser idêntica em todas as camadas para a mesma funcionalidade.
5. **Landing nunca deve prometer** uma funcionalidade que não existe no Web App ou no Mobile.
6. **Landing pode apresentar** funcionalidades que existem em apenas uma camada, desde que a camada seja explicita (ex: "disponível no aplicativo").
7. **Nova entidade central** requer atualização deste documento, do Brand Book e da Matriz de Paridade.

---

## 9. Relação com Documentos Existentes

A arquitetura da plataforma se relaciona com os demais documentos da seguinte forma:

| Documento | Relação com a Arquitetura |
|-----------|--------------------------|
| **BRAND_BOOK_AETERNA.md** | Define quem somos, o que fazemos, nosso posicionamento. A arquitetura define **onde** isso é entregue. |
| **GUIA_TOM_DE_VOZ.md** | Define **como** falamos. A arquitetura define **em qual camada** cada tom se aplica (ex: Landing tem tom de apresentação; Curador tem tom de pergunta). |
| **DIRECAO_FOTOGRAFICA.md** | Define **quais imagens** usamos. A arquitetura define **onde** cada imagem aparece (ex: Hero no site, fotos de família no app). |
| **GUIA_EDITORIAL_HISTORIAS.md** | Define **como escrevemos histórias**. A arquitetura define **onde** as histórias são criadas e lidas (Web App e Mobile). |
| **DECISOES_DE_MARCA.md** | Registra **por que** decidimos o que decidimos. A arquitetura executa essas decisões tecnicamente. |
| **MATRIZ_PARIDADE_WEB_MOBILE.md** | Documento irmão da arquitetura. A matriz mapeia funcionalidade por funcionalidade; a arquitetura define a estrutura. |
| **MOBILE_APP_AUDITORIA_FUNCIONAL.md** | Auditória específica do Mobile. A arquitetura contextualiza essa auditoria dentro da visão geral da plataforma. |

### Documentos que referenciam a arquitetura

Sempre que um documento de marca ou produto mencionar uma funcionalidade, deve referenciar este documento para indicar em qual camada ela vive.

---

## 10. Roadmap Conceitual

### Fase 6 — Plataforma (atual)

**Objetivo:** Estabelecer a arquitetura oficial e corrigir a matriz de paridade.

| Sprint | Foco |
|--------|------|
| **6.0** | Auditoria estratégica de alinhamento ✅ |
| **6.0.1** | Arquitetura oficial da plataforma ✅ (esta sprint) |
| **6.1** | Unificação visual do App Web (fundo escuro, tipografia, footer) |
| **6.2** | Navegação cruzada (links app→site, app→blog, FAQ, legais) |
| **6.3** | Correção de nomenclatura interna (Minha Essência, Cofre Digital, Memorial de Legados) |

### Fase 7 — Mobile

**Objetivo:** Alcançar paridade funcional entre Web App e Mobile.

| Sprint | Foco |
|--------|------|
| **7.1** | Autenticação (login, cadastro, visitante, recuperação) |
| **7.2** | Minha História + Curador |
| **7.3** | Pessoas + Fotos + Vídeos + Linha do Tempo |
| **7.4** | Memorial + Compartilhadas + Novidades + Contribuições |
| **7.5** | Mensagens para o Futuro + Cofre |
| **7.6** | Quem Sou Eu + Planos |
| **7.7** | Notificações Push + Câmera + Galeria Nativa |
| **7.8** | Deep Links + Biometria + Compartilhamento Nativo |

### Fase 8 — Conversão

**Objetivo:** Otimizar a jornada de primeiro uso e ativação.

| Sprint | Foco |
|--------|------|
| **8.1** | Onboarding (primeira experiência no Mobile e Web) |
| **8.2** | Primeira memória guiada (Curador como onboarding) |
| **8.3** | Ativação (convite familiar como métrica de sucesso) |
| **8.4** | Ciclo viral (compartilhamento e crescimento orgânico) |

### Fase 9 — Lançamento

**Objetivo:** Lançar oficialmente a plataforma.

| Sprint | Foco |
|--------|------|
| **9.1** | Google Play (publicação, screenshots, descrição) |
| **9.2** | App Store (publicação, screenshots, descrição) |
| **9.3** | Vídeo institucional (conceito, roteiro, produção) |
| **9.4** | Apresentação pública (LinkedIn, imprensa, parceiros) |

---

## 11. Checklist Final

| Pergunta | Resposta |
|---|---|
| **Um dev novo entende a plataforma?** | Sim. Este documento define que existe **um único produto** (plataforma aEterna) com **4 camadas** (Landing, Site, Web App, Mobile) em **2 repositórios**. Qualquer dev sabe onde cada coisa vive. |
| **Um designer entende onde cada experiência vive?** | Sim. A seção 6 (Módulos) mapeia cada funcionalidade por camada. A seção 7 (Fonte de Verdade) mostra qual camada é referência hoje e qual é o destino de paridade. |
| **Um redator entende a diferença entre Landing, Site, Web e Mobile?** | Sim. A seção 3 define o papel de cada camada. Landing = apresentar e converter. Site = suporte. Web App = referência funcional. Mobile = principal uso diário. |
| **Um futuro time consegue evitar divergência entre Web e Mobile?** | Sim. As regras de evolução (seção 8) exigem que toda nova funcionalidade responda se pertence a qual camada, se é core ou exclusiva, e se afeta a matriz de paridade. |
| **O documento corrige a premissa incorreta de que o mobile não existe?** | Sim. A seção 2 define o repositório Mobile (`https://github.com/dcarriao/aeterna_mobile`). A seção 3.4 descreve o Mobile como "principal experiência de uso diário". Nenhuma parte do documento trata o Mobile como inexistente ou subordinado ao Web. Web e Mobile são **clientes oficiais da mesma plataforma**, com o Web como referência funcional atual e o Mobile como destino de paridade. |

---

> **Este documento é a referência arquitetural oficial da plataforma aEterna. Qualquer pessoa que entrar na equipe deve começar por aqui. Qualquer nova funcionalidade deve passar pelo checklist da seção 8 antes de ser construída.**
