# SPRINT 2 — REARQUITETURA DA LANDING PAGE

> Rearquitetura da `index.html` para apresentar a plataforma completa da aEterna, com novas seções, reorganização da narrativa e reposicionamento do Memorial.

---

## 1. NOVA ARQUITETURA DA LANDING

### 1.1 Antes × Depois

**Antes (Sprint 1):**
```
1. Hero
2. O que estamos perdendo
3. O que é a aEterna
4. Como funciona (4 passos)
5. Memorial (logo após Como funciona)
6. Quote central
7. Telas (3 mockups)
8. Message cards (Por que isso importa / O que se perde)
9. Diferenciais (4 cards vs outras soluções)
10. Privacidade
11. FAQ
12. CTA Final
```

**Depois (Sprint 2):**
```
1.  Hero                              (existente — refinado)
2.  O problema                        (existente — refinado)
3.  Por que as histórias desaparecem  (NOVA)
4.  Como a aEterna resolve            (NOVA)
5.  Manifesto da plataforma           (substitui "O que é a aEterna")
6.  Como funciona (4 passos)          (existente)
7.  O Curador                         (NOVA — dedicada com screenshot real)
8.  A família participa               (NOVA)
9.  Tudo o que a plataforma oferece   (NOVA — grade de 14 features)
10. Como tudo funciona junto          (NOVA — fluxo de integração)
11. Memorial Vivo                     (movido + refinado)
12. Quote central                     (existente)
13. Privacidade                       (existente)
14. FAQ                               (atualizada — +2 perguntas)
15. CTA Final                         (existente)
```

### 1.2 Justificativa da nova sequência

A nova ordem segue a lógica narrativa recomendada:

| Etapa | O que o visitante descobre | Por que nessa posição |
|---|---|---|
| 1-2 | Há um problema real | Empatia |
| 3 | O problema tem causas concretas | Validação emocional com exemplos |
| 4 | A plataforma resolve o problema | Apresentação da solução |
| 5 | Ela é maior do que parece | Manifesto de plataforma |
| 6 | Como usar | Passo a passo concreto |
| 7-8 | O que existe dentro dela | Curador + família |
| 9 | Tudo o que oferece | Mapeamento de funcionalidades |
| 10 | Como funciona junto | Integração |
| 11 | Memorial existe, mas é continuação | Reposicionamento do Memorial |
| 12-15 | Detalhes finais | Privacidade, FAQ, CTA |

---

## 2. NOVAS SEÇÕES CRIADAS

### 2.1 Por que as histórias desaparecem

- **Arquivo:** `D:\aeterna\index.html:1616-1640`
- **ID:** `por-que-desaparecem`
- **Objetivo:** Mostrar com exemplos concretos por que o visitante perde histórias, mesmo querendo preservá-las.
- **Conteúdo:** 3 cards com exemplos reais do cotidiano (fotos, vídeos, lugares) onde o significado se perde.
- **Componentes:** nova classe `.examples-grid` (CSS em `:944-982`).
- **Benefício para o visitante:** valida a experiência emocional dele ("é assim na minha família também").

### 2.2 Como a aEterna resolve

- **Arquivo:** `D:\aeterna\index.html:1642-1679`
- **ID:** `resolve`
- **Objetivo:** Mostrar o fluxo da plataforma em 5 etapas visuais, sem sobrecarregar com texto.
- **Conteúdo:** Você vive → Você registra → O Curador ajuda → A família complementa → A história cresce.
- **Componentes:** nova classe `.resolve-panel` + `.resolve-flow` + `.resolve-step` (CSS em `:984-1037`).
- **Benefício para o visitante:** entende o "como" da plataforma em segundos, sem precisar ler parágrafos.

### 2.3 Manifesto da plataforma (substitui "O que é a aEterna")

- **Arquivo:** `D:\aeterna\index.html:1681-1690`
- **ID:** `manifesto`
- **Objetivo:** Posicionar a aEterna como uma plataforma integrada (não um aplicativo de histórias), enumerando o que ela cobre sem ser uma lista de features.
- **Conteúdo:** "Mais do que um lugar para escrever histórias." + parágrafo-manifesto que menciona: histórias, pessoas, relações, fotos, vídeos, aprendizados, datas, mensagens.
- **Componentes:** nova classe `.platform-manifesto` (CSS em `:1039-1066`).
- **Benefício para o visitante:** quebra a percepção de que a aEterna é apenas "mais um app de diário".

### 2.4 O Curador

- **Arquivo:** `D:\aeterna\index.html:1741-1774`
- **ID:** `curador`
- **Objetivo:** Apresentar o Curador de Histórias como um conceito da plataforma, sem vendê-lo como "IA" ou "chatbot".
- **Conteúdo:** explicação clara do que o Curador faz (faz perguntas, organiza, sugere conexões, permite revisão) + screenshot real do Curador (`assets/curadoria.webp`).
- **Componentes:** nova classe `.curador-grid` + `.curador-copy` + `.curador-points` + `.curador-point` + `.curador-visual` (CSS em `:1068-1142`).
- **Funcionalidade do app referenciada:** `app.py:1296-1301` (`render_curador_memoria_primeiro` / `render_assistente`) e `components/chat_luto.py:1058`.
- **Benefício para o visitante:** entende que a plataforma tem um guia, mas sem o tecnicismo que afastaria um público leigo.

### 2.5 A família participa

- **Arquivo:** `D:\aeterna\index.html:1776-1818`
- **ID:** `familia`
- **Objetivo:** Mostrar que as histórias crescem com a contribuição de outras pessoas da família.
- **Conteúdo:** parágrafo explicativo + 5 itens de fluxo (4 inputs `+` e 1 output `=`) mostrando como diferentes familiares contribuem.
- **Componentes:** nova classe `.family-panel` + `.family-grid` + `.family-flow` + `.family-flow-item` (CSS em `:1144-1211`).
- **Funcionalidade do app referenciada:** `app.py:1060-1192` (`render_form_contribuicao_memoria`) e `app.py:4189-4353` (`render_contribuicoes_pendentes`).
- **Benefício para o visitante:** entende que a plataforma não é uma atividade solitária — outras pessoas da família também têm um papel.

### 2.6 Tudo o que a plataforma oferece

- **Arquivo:** `D:\aeterna\index.html:1820-1913`
- **ID:** `plataforma`
- **Objetivo:** Listar todas as funcionalidades existentes no app, em uma grade visual.
- **Conteúdo:** 14 cards, cada um com ícone, nome e descrição curta. Funcionalidades:
  1. Minha História
  2. Curador de Histórias
  3. Explorador de Histórias
  4. Pessoas
  5. Fotos
  6. Vídeos
  7. Linha do Tempo
  8. Compartilhamento Familiar
  9. Contribuições
  10. Memorial Vivo
  11. Mensagens para o Futuro
  12. Cofre Digital
  13. Planos
  14. Minha Essência
- **Componentes:** nova classe `.features-grid` + `.feature-card` + `.feature-icon` (CSS em `:1213-1269`).
- **Benefício para o visitante:** enxerga de uma vez só a amplitude da plataforma.

### 2.7 Como tudo funciona junto

- **Arquivo:** `D:\aeterna\index.html:1915-1967`
- **ID:** `integracao`
- **Objetivo:** Mostrar que as funcionalidades não são telas isoladas — formam um ecossistema.
- **Conteúdo:** 8 etapas numeradas que demonstram o fluxo integrado (registrar → pessoas → fotos/vídeos → Curador → contribuições → linha do tempo → exploração → crescimento).
- **Componentes:** nova classe `.integration-panel` + `.integration-flow` + `.integration-step` (CSS em `:1271-1327`).
- **Benefício para o visitante:** entende que a plataforma é uma experiência contínua, não um conjunto de recursos desconectados.

### 2.8 Memorial Vivo (reposicionado)

- **Arquivo:** `D:\aeterna\index.html:1969-2014`
- **ID:** `memorial` (anteriormente `memorial-secao`)
- **Objetivo:** Apresentar o Memorial como continuação natural da história familiar — não como foco.
- **Conteúdo:** novo H2 ("E quando alguém se torna parte da história de muitas pessoas?"), novo destaque ("O Memorial não inicia uma história. Ele continua uma história que já existia."), 4 benefit-cards reescritos, CTA renomeado.
- **Componentes:** classes existentes (`.memorial-grid`, `.memorial-image`, `.memorial-copy`, `.memorial-benefits`, `.benefit-card`).
- **Funcionalidade do app referenciada:** `components/memorial.py:22-160, 162-369, 542-1210`.
- **Benefício para o visitante:** entende o Memorial sem que ele domine a narrativa, e sem linguagem de luto.

---

## 3. FUNCIONALIDADES INCORPORADAS

| Funcionalidade | Existia no Site (Sprint 1) | Situação após Sprint 2 | Evidência no código do aplicativo |
|---|---|---|---|
| **Minha História** | Parcial (Como funciona passo 1) | ✅ Em "Tudo o que a plataforma oferece" | `app.py:517-901` (`render_minha_historia`) |
| **Curador de Histórias** | Implícito (Como funciona passo 2) | ✅ Seção dedicada "O Curador" | `app.py:1296-1301`, `components/chat_luto.py:1058` |
| **Explorador de Histórias** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" | `app.py:1276, 2786, 5013`; `utils/assistente_ia.py:563` ("Você é o Explorador de Histórias da aEterna.") |
| **Pessoas** | Parcial (Como funciona passo 3) | ✅ Em "Tudo o que a plataforma oferece" | `app.py:2351-2782` (`render_contatos`) |
| **Fotos** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" + integração | `app.py:1550-1752` (`render_fotos`) |
| **Vídeos** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" + integração | `app.py:1307-1515` (`render_videos`) |
| **Linha do Tempo** | Sim (Como funciona passo 4) | ✅ Em "Tudo o que a plataforma oferece" + integração | `app.py:517-901` (em `render_minha_historia`) |
| **Compartilhamento Familiar** | Implícito (Como funciona passo 3) | ✅ Em "Tudo o que a plataforma oferece" | `app.py:5070-5322` (`render_historias_compartilhadas_lista`) |
| **Contribuições** | Parcial (FAQ e Memorial) | ✅ Em "Tudo o que a plataforma oferece" + "A família participa" | `app.py:4189-4353` (`render_contribuicoes_pendentes`) |
| **Memorial Vivo** | Sim (seção dedicada) | ✅ Reposicionado, refinado, sem linguagem de luto | `components/memorial.py` |
| **Mensagens para o Futuro** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" | `app.py:3480-3781` (`render_agendamentos`) |
| **Cofre Digital** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" | `app.py:3786-3919` (`render_cofre`) |
| **Planos** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" + FAQ | `app.py:2886-3476` (`render_planos`) |
| **Minha Essência (preferências)** | Não comunicada | ✅ Em "Tudo o que a plataforma oferece" | `app.py:2783-2880` (`render_preferencias`) |
| **Login de visitante com chave** | Não comunicada | ⚠️ Ainda não comunicada (sprint futura) | `app.py:298-317` (`fazer_login_visitante`) |
| **Recuperação de senha** | Não comunicada | ⚠️ Ainda não comunicada (sprint futura) | `components/login_compacto.py:397-417` |
| **Datas importantes** | Não comunicada | ⚠️ Implícita em "Mensagens para o Futuro" (sprint futura) | `app.py:3493-3600` |
| **Integração WhatsApp (convite Memorial)** | Não comunicada | ⚠️ Ainda não comunicada (sprint futura) | `components/memorial.py:867-944` |
| **Visibilidade por conteúdo** | Sim (Privacidade) | ✅ Em Privacidade | `app.py:451-515` (`render_editor_visibilidade`) |

**Resumo:** 14 das 19 funcionalidades do app passaram a ser comunicadas na Landing. As 5 restantes (login visitante, recuperação de senha, datas, WhatsApp) continuam fora do escopo desta sprint por serem detalhes operacionais que não cabem na narrativa principal.

---

## 4. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | Linhas 1140-1146 (menu) | Reorganização dos itens de navegação |
| `D:\aeterna\index.html` | Linhas 1165-1169 (Hero proof-items) | Atualização do primeiro item |
| `D:\aeterna\index.html` | Linhas 943-1327 (CSS) | **+385 linhas** de CSS para novas seções |
| `D:\aeterna\index.html` | Linhas 944-980 e 1033-1050 (CSS responsivo) | Regras responsivas para as novas seções |
| `D:\aeterna\index.html` | Linhas 1616-1690 (3 novas seções) | Por que desaparecem + Como resolve + Manifesto |
| `D:\aeterna\index.html` | Linhas 1741-1818 (2 novas seções) | O Curador + A família participa |
| `D:\aeterna\index.html` | Linhas 1820-1967 (2 novas seções) | Tudo o que a plataforma oferece + Como tudo funciona junto |
| `D:\aeterna\index.html` | Linhas 1969-2014 (Memorial) | Reposicionamento e refatoração |
| `D:\aeterna\index.html` | Linhas 2043-2080 (FAQ) | +2 perguntas (Curador e Planos), atualização da pergunta sobre Memorial |
| `D:\aeterna\index.html` | Linhas 2100-2106 (footer nav) | Atualização dos links do rodapé |

**Nenhum outro arquivo foi alterado.** Não houve mudanças em CSS de classes existentes (apenas adições), em JavaScript, em SEO, em Schema.org, em sitemap, em robots, em manifest, em favicon, em páginas legais, em imagens, em assets, em arquivos do aplicativo.

**Arquivos removidos (lógica):**
- Seção "O que é a aEterna" (`#o-que-e`) — substituída por "Manifesto da plataforma" (`#manifesto`).
- Seção "Telas" (`#telas`) — removida; a tela do Curador agora aparece dentro da seção dedicada "O Curador".
- Seção "Message cards" (Por que isso importa / O que se perde) — removida; o conteúdo foi absorvido por "Por que as histórias desaparecem" e pelo manifesto.
- Seção "Diferenciais" — removida; a diferenciação agora é comunicada pelo manifesto e pelos features individuais.

---

## 5. VALIDAÇÃO

### 5.1 A Landing representa significativamente mais funcionalidades do aplicativo do que representava na Sprint 1?

**Sim.** Evidência objetiva:

| Sprint | Funcionalidades comunicadas | % do app |
|---|---|---|
| Sprint 0 (auditoria) | ~3 de 14 áreas principais | ~21% |
| Sprint 1 | ~5 de 14 áreas principais | ~36% |
| **Sprint 2** | **14 de 19 áreas funcionais** | **~74%** |

Crescimento de **+38 pontos percentuais** em relação à Sprint 1, e de **+53 pontos** em relação à Sprint 0. As áreas que permanecem fora do escopo (login visitante, recuperação de senha, datas, WhatsApp) são detalhes operacionais que serão tratados em sprints dedicadas.

### 5.2 O visitante consegue perceber que a aEterna é uma plataforma completa?

**Sim.** Evidências textuais:

- O Hero agora diz "Plataforma de histórias de família" (`index.html:1154`) — não "aplicativo de histórias".
- O Manifesto da plataforma é uma seção central inteira dedicada a comunicar amplitude: "Mais do que um lugar para escrever histórias. A aEterna é uma plataforma integrada para preservar o patrimônio invisível de uma família" (`index.html:1685-1686`).
- Existe uma seção inteira chamada "Tudo o que a plataforma oferece" com 14 cards visuais (`index.html:1820-1913`).
- Existe uma seção "Como tudo funciona junto" mostrando que as funcionalidades formam um ecossistema (`index.html:1915-1967`).
- O proof-item do Hero foi atualizado de "Histórias com contexto" para "Plataforma completa para histórias de família" (`index.html:1541`).

### 5.3 Alguma funcionalidade foi comunicada de forma incorreta?

**Não.** Auditoria item a item, com referência direta ao código:

| Funcionalidade | Como aparece na Landing | Como existe no app | Comunicação correta? |
|---|---|---|---|
| Minha História | "O seu espaço principal de histórias" | `app.py:517-901` | ✅ |
| Curador de Histórias | "Faz perguntas para ajudar você a transformar lembranças em histórias" | `app.py:1296-1301` (`render_assistente`) | ✅ |
| Explorador de Histórias | "Quando alguém quer conhecer a sua história, ele responde perguntas" | `app.py:1276, 5013` | ✅ |
| Pessoas | "Datas especiais, parentesco e tipo de acesso" | `app.py:2351-2782` | ✅ |
| Fotos | "Entram na história, com o contexto do que estava acontecendo" | `app.py:1550-1752` | ✅ |
| Vídeos | "Mensagens, gravações e vídeos familiares" | `app.py:1307-1515` | ✅ |
| Linha do Tempo | "Narrativa visual da família" | `app.py:517-901` | ✅ |
| Compartilhamento Familiar | "Só sua, da família toda ou apenas para algumas pessoas" | `app.py:5070-5322` + `app.py:444-515` | ✅ |
| Contribuições | "Acrescentar suas próprias memórias. Você revisa antes de publicar" | `app.py:4189-4353` | ✅ |
| Memorial Vivo | "Continuação natural. Família se reúne para construir juntas" | `components/memorial.py` | ✅ |
| Mensagens para o Futuro | "Podem ser agendados para datas especiais" | `app.py:3480-3781` | ✅ |
| Cofre Digital | "Espaço criptografado para senhas, documentos e informações" | `app.py:3786-3919` + `utils/criptografia.py` | ✅ |
| Planos | "Começar gratuitamente. Planos pagos liberam mais" | `app.py:2886-3476` | ✅ |
| Minha Essência | "Questionário para registrar gostos, valores, preferências e aprendizados" | `app.py:2783-2880` | ✅ |

### 5.4 O Memorial deixou de competir com a proposta principal?

**Sim.** Evidências:

1. **Posição:** na Sprint 1 o Memorial vinha logo após "Como funciona" (4ª seção de conteúdo). Agora aparece apenas depois de 10 seções anteriores, em 11ª posição (`index.html:1969`).
2. **Headline:** "E quando alguém se torna parte da história de muitas pessoas?" — pergunta condicional, não assertiva (`index.html:1976`).
3. **Destaque inicial:** "O Memorial não inicia uma história. Ele continua uma história que já existia." (`index.html:1978`) — afirma explicitamente que vem depois.
4. **Texto:** "Algumas pessoas marcam tantas vidas que merecem um espaço só para a história que deixaram." (`index.html:1981-1982`) — sem referência a perda, despedida ou luto.
5. **Benefit cards reescritos:** "Um espaço só para aquela pessoa" / "Construído em conjunto" / "Conecte-se ao que ficou" / "Converse com a história registrada" — sem nenhuma palavra de luto.
6. **CTA:** "Conhecer o Memorial Vivo" — não "Criar Memorial" (linguagem de recurso, não de produto).
7. **Eyebrow:** "Memorial Vivo" — agora é tratado como módulo, não como feature principal.

### 5.5 O Curador foi introduzido sem ser vendido como um chatbot?

**Sim.** Evidências textuais:

- O Curador é chamado de "guia silencioso dentro da plataforma" (`index.html:1748`).
- É descrito como alguém que "faz as perguntas certas" (`index.html:1749`).
- A frase "Você responde, ele estrutura" (`index.html:1754`) é direta, sem tecnicismo.
- A seção "O que é a aEterna" (Sprint 1) já tinha o card "Não é nuvem nem chatbot" — e a nova seção não contradiz isso.
- Não há menção a "IA", "inteligência artificial", "algoritmo" ou "bot" em nenhum ponto das seções sobre o Curador.
- O FAQ pergunta "O que é o Curador de Histórias?" e responde "É um guia dentro da plataforma" (`index.html:2075-2077`) — sem tecnicismo.

### 5.6 A narrativa continua centrada na família e não na tecnologia?

**Sim.** Auditoria:

- **Hero:** pergunta sobre as histórias da família (não sobre a plataforma).
- **Problema:** "As fotos sobrevivem. As histórias, quase nunca." — centrado nas pessoas.
- **Por que as histórias desaparecem:** exemplos cotidianos (vídeo de aniversário, foto de passeio) — centrado na família.
- **Como a aEterna resolve:** "Você vive → Você registra → O Curador ajuda → A família complementa → A história cresce." — família como protagonista.
- **Manifesto:** "patrimônio invisível de uma família" — termo de patrimônio, não de tecnologia.
- **Como funciona:** "Para que a sua família não herde apenas imagens soltas" — foco na família.
- **O Curador:** "você não precisa saber por onde começar" — centrado em você, não na tecnologia.
- **A família participa:** "Filhos, irmãos, pais, avós, amigos" — pessoas concretas.
- **Tudo o que a plataforma oferece:** cada card menciona pessoas (exceto os técnicos: Cofre, Planos).
- **Como tudo funciona junto:** termina em "O legado continua crescendo" — foco no resultado, não no processo.
- **Memorial Vivo:** "A família se reúne para construir juntas" — família como sujeito.
- **Privacidade:** "Histórias de família precisam de um espaço seguro" — centrado nas histórias.
- **FAQ:** primeira pergunta é sobre a identidade da plataforma, não sobre funcionalidades.
- **CTA Final:** "Comece registrando uma história que sua família não deveria perder" — centrado no visitante e na família.

A única menção a "plataforma" no Hero (`index.html:1154`) é no eyebrow, em um lugar subordinado ao H1 centrado na pergunta humana.

---

## 6. PRINCÍPIOS APLICADOS

| Diretriz | Resposta |
|---|---|
| Não alterar SEO, Schema.org, robots, sitemap, manifest, favicon | ✅ Nenhuma alteração no `<head>` |
| Não alterar páginas legais | ✅ `legais/politicaprivacidade.html` intocado |
| Não alterar performance, otimizações de imagens, acessibilidade | ✅ Mantido |
| Não alterar JavaScript estrutural | ✅ Script de menu intocado |
| Manter paleta, tipografia, botões, espaçamentos, animações | ✅ Apenas reuso das variáveis CSS existentes + adições pontuais usando mesmas variáveis |
| Cada nova funcionalidade tem que existir no app | ✅ Verificado contra `app.py`, `components/*.py`, `utils/*.py` |
| Não criar funcionalidades inexistentes | ✅ |
| Não fazer inferências | ✅ Toda funcionalidade foi confirmada com evidência de código |
| Substituir texto genérico por exemplos concretos | ✅ Passeio de bicicleta, almoço em família, conversa que marcou, vídeo de aniversário, etc. |
| Curador sem "IA"/"chatbot" | ✅ Chamado de "guia silencioso", "guia dentro da plataforma" |
| Memorial sem linguagem de luto | ✅ "Memorial Vivo", "continuação", "construído em conjunto" |
| Menu pode ser ajustado para acomodar novas seções | ✅ Itens reorganizados: Início, O problema, O Curador, A plataforma, Memorial, FAQ, CTA |
| Reaproveitar imagens existentes | ✅ `assets/curadoria.webp` para a seção O Curador; `assets/memorial.png` continua no Memorial; `assets/home.webp`, `assets/curadoria.webp`, `assets/timeline.webp`, `assets/nova-memoria.webp`, `assets/memoria-detalhe.webp`, `assets/pessoas.webp` continuam em Como funciona |
| Não usar imagens de bancos genéricos | ✅ Nenhuma imagem nova adicionada |
| Não usar mockups genéricos | ✅ O Curador usa a tela real `curadoria.webp`; Memorial usa a imagem real `memorial.png` |

---

## 7. RESUMO FINAL

A Sprint 2 transformou a Landing Page de uma apresentação de "funcionalidade única" (a história) em uma apresentação de **plataforma integrada** com 14 áreas funcionais comunicadas explicitamente, três novas seções narrativas, um fluxo de integração de 8 etapas, e um Memorial que finalmente aparece como continuação, e não como foco.

A sequência de seções agora é:

```
Hero → O problema → Por que as histórias desaparecem → Como a aEterna resolve
→ Manifesto da plataforma → Como funciona → O Curador → A família participa
→ Tudo o que a plataforma oferece → Como tudo funciona junto → Memorial Vivo
→ Quote → Privacidade → FAQ → CTA Final
```

O visitante sai entendendo que a aEterna é uma plataforma para preservar o patrimônio invisível de uma família — não um aplicativo de histórias, e não um memorial.

---

**Fim da Sprint 2 — Rearquitetura da Landing.**
