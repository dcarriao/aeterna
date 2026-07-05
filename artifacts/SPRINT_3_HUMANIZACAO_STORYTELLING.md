# SPRINT 3 — HUMANIZAÇÃO DA LANDING E STORYTELLING

> Humanização da `index.html` com micro-histórias, storytelling de funcionalidades, novas seções emocionais, citações e exemplos concretos. A arquitetura de 15 seções da Sprint 2 foi preservada, com 2 novas seções de humanização inseridas em pontos específicos da narrativa.

---

## 1. RESUMO DAS ALTERAÇÕES

A Sprint 3 transformou a Landing de uma **apresentação completa da plataforma** em uma **experiência emocionalmente envolvente**. O visitante agora:

- Reconhece suas próprias situações em micro-histórias concretas (almoço de domingo, Natal de 1998, receita da avó).
- Imagina o futuro com clareza (a seção "Imagine daqui a 30 anos").
- Sente que a aEterna entende o que é uma família real (a seção "As pequenas histórias").
- Vê o Curador funcionando em um diálogo natural (em vez de apenas ouvir falar dele).
- Entende que a colaboração familiar produz histórias maiores do que qualquer versão isolada.
- Imagina o Memorial sem pensar em luto.

A sequência de seções da Sprint 2 foi **preservada**; a Sprint 3 adicionou 2 novas seções (`futuro` e `pequenas-historias`) em pontos específicos, 3 citações entre seções, e elementos de storytelling dentro de seções existentes.

**Não foi alterado:** SEO, Schema.org, robots, sitemap, manifest, favicon, JavaScript estrutural, performance, acessibilidade, páginas legais, paleta, tipografia, layout, arquitetura de 15 seções da Sprint 2.

---

## 2. NOVAS MICRO-HISTÓRIAS

A Landing agora contém 12 micro-histórias concretas:

| # | Onde foi inserida | Micro-história | Objetivo |
|---|---|---|---|
| 1 | Problema (`index.html:1907`) | "Você gravou o primeiro passeio de bicicleta do seu filho. A foto vai ficar. Mas quem vai contar para seus netos como foi aquele dia?" | Empatia com a perda da história |
| 2 | Imagine daqui a 30 anos (`index.html:1980`) | Foto do aniversário do filho com texto sobre quem estava ali e por que o dia foi importante | Valor futuro da preservação |
| 3 | Imagine daqui a 30 anos (`index.html:1988`) | Neto encontra a foto e descobre quem estava ali, o que riam, por que importou | Materialização do benefício |
| 4 | As pequenas histórias (`index.html:2063-2093`) | 6 exemplos (bolo, música, apelido, foto, objeto, conselho) | Mostrar o patrimônio invisível |
| 5 | Curador (diálogo) (`index.html:2190-2213`) | "Almoço de domingo na casa da avó / meu pai ensinou meu irmão a descascar laranja" | Mostrar o Curador em ação |
| 6 | Como funciona (timeline) (`index.html:2149-2161`) | 2001 (nascimento) → 2008 (viagem) → 2016 (primeiro emprego) → 2035 (mensagem para netos) | Materializar a Linha do Tempo |
| 7 | A família participa (`index.html:2271-2290`) | Natal de 1998: você + irmã + pai + filho | Mostrar a colaboração crescendo |
| 8 | Plataforma (Mensagem para o Futuro) (`index.html:2418-2422`) | "Parabéns pelos seus 18 anos. Se você está lendo essa mensagem…" | Exemplo real de mensagem |
| 9 | Memorial (`index.html:2501-2517`) | Filha + irmão + esposa + neto construindo Memorial do pai | Memorial como construção coletiva |
| 10 | Inter-quote 1 (`index.html:1964`) | "Hoje conseguimos guardar arquivos. Ainda estamos aprendendo a guardar significado." | Reflexão sobre o problema |
| 11 | Inter-quote 2 (`index.html:2051`) | "Cada família possui um patrimônio invisível. A aEterna existe para torná-lo visível." | Reforço do valor |
| 12 | Inter-quote 3 (`index.html:2456`) | "Você herdou histórias da sua família. Com a aEterna, você também pode deixá-las." | Ponte antes do Memorial |

---

## 3. NOVAS SEÇÕES

### 3.1 Imagine daqui a 30 anos

- **Arquivo:** `D:\aeterna\index.html:1968-1997`
- **ID:** `futuro`
- **Objetivo:** Criar um salto temporal mental que faz o visitante visualizar o valor futuro de suas histórias.
- **Mensagem transmitida:** "Uma pequena escolha hoje se transforma em herança daqui a décadas."
- **Componentes novos:** `.future-jump` + `.future-jump-grid` + `.future-jump-card` + `.future-jump-arrow` + `.fj-label`.
- **Estrutura:** dois cards lado a lado (Hoje / Daqui a 30 anos) conectados por uma seta dourada.
- **Contribuição para a experiência:** quebra a leitura de "problema-solução" e insere uma projeção emocional que ancora a decisão do visitante.

### 3.2 As pequenas histórias

- **Arquivo:** `D:\aeterna\index.html:2055-2099`
- **ID:** `pequenas-historias`
- **Objetivo:** Mostrar que toda família possui um patrimônio invisível composto de pequenos momentos.
- **Mensagem transmitida:** "Nem sempre o que vale a pena registrar é o que parece grande."
- **Componentes novos:** `.small-stories` + `.small-story-card` + `.ss-emoji` + `.ss-note`.
- **Conteúdo:** 6 cards com emoji, frase em destaque e nota explicativa.
- **Contribuição para a experiência:** após o manifesto de plataforma, ancora a noção de "patrimônio invisível" em exemplos cotidianos e emocionalmente identificáveis.

### 3.3 Citações entre seções (3)

| Posição | Citação | Efeito |
|---|---|---|
| Entre "Por que desaparecem" e "Imagine daqui a 30 anos" | "Hoje conseguimos guardar arquivos. Ainda estamos aprendendo a guardar significado." | Reflexão que prepara o salto temporal |
| Entre "Manifesto" e "As pequenas histórias" | "Cada família possui um patrimônio invisível. A aEterna existe para torná-lo visível." | Conecta a posição da plataforma com o que vem a seguir |
| Entre "Como tudo funciona junto" e "Memorial" | "Você herdou histórias da sua família. Com a aEterna, você também pode deixá-las." | Liga a herança ao Memorial como continuação |

- **Componente novo:** `.inter-quote`.
- **Efeito:** cria pausas respiratórias entre seções técnicas e ameniza a densidade da página.

---

## 4. FLUXOS NARRATIVOS ADICIONADOS

### 4.1 Storytelling do Curador

- **Arquivo:** `D:\aeterna\index.html:2190-2213`
- **Formato:** diálogo de 6 turnos entre "Você" e "Curador".
- **Personagem:** uma pessoa contando a história de um almoço de domingo.
- **O que mostra:** que o Curador não é um chatbot que faz perguntas genéricas — ele conduz a memória para o que importa (o que o pai fez, o que aquilo significou).
- **Funcionalidade do app referenciada:** `components/chat_luto.py:280` (`_render_curador_memoria_primeiro`) e `components/chat_luto.py:126` (`_curador_analisar_memoria_com_ia`).
- **Componente novo:** `.curador-dialogue` + `.cd-line` + `.cd-speaker` + `.cd-bubble`.

### 4.2 Storytelling da colaboração familiar

- **Arquivo:** `D:\aeterna\index.html:2271-2295`
- **Formato:** 4 etapas numeradas mostrando a história do Natal de 1998 crescendo.
- **O que mostra:** que uma história começa com uma pessoa e vai sendo completada por outras.
- **Funcionalidade do app referenciada:** `app.py:1060-1192` (`render_form_contribuicao_memoria`) + `app.py:4189-4353` (`render_contribuicoes_pendentes`).
- **Componente novo:** `.family-story` + `.fs-step` + `.fs-num`.

### 4.3 Storytelling do Memorial

- **Arquivo:** `D:\aeterna\index.html:2501-2521`
- **Formato:** 4 etapas numeradas mostrando o Memorial crescendo (filha → irmão → esposa → neto).
- **O que mostra:** que o Memorial é uma construção coletiva, sem qualquer referência a luto.
- **Funcionalidade do app referenciada:** `components/memorial.py:22-160` (`render_criar_memorial`) + `components/memorial.py:371-540` (`render_curador_perfil`) + `components/memorial.py:542-1210` (`render_pagina_memorial`).
- **Componente:** mesmo `.family-story` reusado (mesma estrutura visual).

### 4.4 Exemplo da Linha do Tempo

- **Arquivo:** `D:\aeterna\index.html:2149-2162`
- **Formato:** 4 linhas de ano + evento.
- **O que mostra:** que a Linha do Tempo pode contar anos de família em poucas linhas.
- **Funcionalidade do app referenciada:** `app.py:517-901` (`render_minha_historia`).
- **Componente novo:** `.timeline-example` + `.tl-row` + `.tl-year` + `.tl-event`.

### 4.5 Exemplo de Mensagem para o Futuro

- **Arquivo:** `D:\aeterna\index.html:2418-2423`
- **Formato:** mensagem em destaque entre aspas + linha de assinatura.
- **O que mostra:** como é uma Mensagem para o Futuro real — texto humano, datado, pessoal.
- **Funcionalidade do app referenciada:** `app.py:3480-3781` (`render_agendamentos`).
- **Componente novo:** `.message-example` (com aspas decorativas via `::before`).

### 4.6 Micro-história após a seção "Imagine"

- **Arquivo:** `index.html:1993-1995`
- **Formato:** parágrafo curto com ênfase em itálico.
- **Texto:** "Esse é o tipo de coisa que **não cabe em uma legenda** e que quase nunca cabe em uma conversa. Mas cabe em uma história bem registrada."
- **Objetivo:** conectar visualmente a seção com o resto da Landing.

### 4.7 Micro-história após a seção "A família participa"

- **Arquivo:** `index.html:2293-2295`
- **Texto:** "Uma história **quase nunca está pronta** quando você termina de escrevê-la. Ela termina de crescer quando alguém da sua família acrescenta a peça que faltava."
- **Objetivo:** reforçar a ideia de construção coletiva.

### 4.8 Micro-história após o Memorial

- **Arquivo:** `index.html:2519-2521`
- **Texto:** "A história daquela pessoa **continua crescendo** com cada contribuição. O Memorial não termina — ele vai sendo escrito pela vida que ela deixou."
- **Objetivo:** reforçar o Memorial como construção contínua, sem linguagem de luto.

---

## 5. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | Linhas 1280-1545 (CSS) | **+266 linhas** de CSS para 8 novos componentes |
| `D:\aeterna\index.html` | Linhas 1395-1410 (CSS responsivo) | Regras responsivas para os novos componentes |
| `D:\aeterna\index.html` | Linhas 1962-1997 (novas seções) | Inter-quote 1 + "Imagine daqui a 30 anos" |
| `D:\aeterna\index.html` | Linhas 2048-2099 (novas seções) | Inter-quote 2 + "As pequenas histórias" |
| `D:\aeterna\index.html` | Linhas 2149-2162 (refinamento) | Exemplo de Linha do Tempo no final de "Como funciona" |
| `D:\aeterna\index.html` | Linhas 2190-2213 (refinamento) | Diálogo do Curador |
| `D:\aeterna\index.html` | Linhas 2271-2295 (refinamento) | Storytelling de colaboração familiar |
| `D:\aeterna\index.html` | Linhas 2418-2423 (refinamento) | Exemplo de Mensagem para o Futuro |
| `D:\aeterna\index.html` | Linhas 2454-2458 (nova seção) | Inter-quote 3 antes do Memorial |
| `D:\aeterna\index.html` | Linhas 2501-2521 (refinamento) | Storytelling do Memorial |

**Nenhum outro arquivo foi alterado.** Não houve mudanças em SEO, em Schema.org, em JavaScript estrutural, em manifest, em sitemap, em favicon, em páginas legais, em imagens, em CSS de classes existentes (apenas adições), em arquivos do aplicativo.

---

## 6. RITMO DA LEITURA

A Sprint 3 introduziu variação explícita no ritmo de leitura, alternando entre:

| Tipo | Seções |
|---|---|
| **Narrativa emocional** | Hero, Problema, Por que desaparecem, Imagine daqui a 30 anos, As pequenas histórias |
| **Funcionalidade prática** | Como funciona, O Curador, A família participa, Tudo o que a plataforma oferece, Como tudo funciona junto |
| **Exemplo concreto** | Diálogo do Curador, Família participa, Mensagem para o Futuro, Memorial, Linha do Tempo |
| **Reflexão (citações)** | 3 inter-quotes entre seções |
| **Reflexão (manifesto)** | Manifesto da plataforma, Quote central |

A ordem resultante evita sequências longas de seções técnicas, intercalando narrativa com funcionalidade, e exemplo com reflexão.

---

## 7. VALIDAÇÃO

### 7.1 O visitante consegue imaginar sua própria família utilizando a plataforma?

**Sim.** Evidências:

- **Passeio de bicicleta** (`index.html:1907`) — situação comum de qualquer pai/mãe.
- **Almoço de domingo na casa da avó** (`index.html:2190`) — referência universal no Brasil.
- **Receita da avó / música do pai / apelido dos irmãos** (`index.html:2063-2093`) — qualquer família possui esses elementos.
- **Natal de 1998** (`index.html:2271`) — memórias de família típicas.
- **Passeio na casa nova** (`index.html:2272`) — marco familiar comum.
- **Aniversário do filho com texto sobre o que estava acontecendo** (`index.html:1980`) — situação realista para quem tem filhos pequenos.
- **Foto antiga do casamento** (`index.html:2501`) — elemento comum em qualquer álbum de família.
- **Torta que ninguém mais sabe a receita** (`index.html:2277`) — perda frequente de saberes familiares.
- **Mensagem para os 18 anos do neto** (`index.html:2420`) — planejamento comum entre avós.

### 7.2 A Landing ficou mais humana sem se tornar melodramática?

**Sim.** Verificação:

- Nenhuma palavra "luto", "perda", "morte", "despedida", "chorar" foi adicionada (mantendo o trabalho das Sprints 1 e 2).
- As histórias escolhidas são cotidianas, não trágicas (almoço, Natal, aniversário, receita).
- Os exemplos familiares têm tom positivo ou neutro — não há "saudade" enfatizada como dor, apenas como memória.
- A citação "saudade" aparece apenas no quote central mantido da Sprint 1, que já era leve.
- A escala emocional é gradual: começa com problema (perdas pequenas) e termina em reflexão (herança).

### 7.3 Os exemplos utilizados representam situações comuns da vida?

**Sim.** Lista das situações usadas:

| Situação | Onde |
|---|---|
| Primeiro passeio de bicicleta do filho | Problema, Hero |
| Foto de aniversário | Imagine daqui a 30 anos |
| Bolo da avó / receita | As pequenas histórias |
| Música do pai | As pequenas histórias |
| Apelido dos irmãos | As pequenas histórias |
| Foto antiga sem contexto | As pequenas histórias |
| Objeto antigo guardado | As pequenas histórias |
| Conselho do pai | As pequenas histórias |
| Almoço de domingo na casa da avó | Diálogo do Curador |
| Descascar laranja sem quebrar a casca | Diálogo do Curador |
| Nascimento da filha (2001) | Timeline |
| Primeira viagem em família para a praia (2008) | Timeline |
| Primeiro emprego da filha (2016) | Timeline |
| Mensagem agendada para o neto (2035) | Timeline |
| Natal de 1998 na casa nova | Família participa |
| Torta que ninguém sabe a receita | Família participa |
| 18 anos do neto | Mensagem para o Futuro |
| Foto do casamento dos pais | Memorial |
| Vídeo do pai falando sobre paternidade | Memorial |

Todas as situações pertencem ao repertório comum de qualquer família brasileira.

### 7.4 A narrativa continua centrada na família?

**Sim.** Verificação seção por seção:

| Seção | Centro |
|---|---|
| Hero | pergunta humana |
| Problema | perda das histórias |
| Por que desaparecem | exemplos cotidianos |
| Imagine daqui a 30 anos | neto + foto da família |
| Como resolve | 5 etapas humanas |
| Manifesto | patrimônio familiar |
| As pequenas histórias | coisas de família |
| Como funciona | 4 passos + timeline familiar |
| O Curador | diálogo com avó, pai, irmão |
| A família participa | contribuição familiar |
| Tudo o que oferece | 14 cards (12 mencionam pessoas) |
| Como tudo funciona junto | etapas da vida familiar |
| Memorial | construído em conjunto pela família |
| Privacidade | histórias de família |
| FAQ | identidade da plataforma |
| CTA Final | família |

A tecnologia aparece apenas como meio. Em nenhum ponto da Landing o foco muda da família para a plataforma.

### 7.5 As funcionalidades continuam sendo apresentadas corretamente?

**Sim.** Verificação contra o código do app:

| Funcionalidade | Onde aparece | Como | Verificação no código |
|---|---|---|---|
| Curador de Histórias | Seção dedicada + diálogo | Faz perguntas, organiza, sugere conexões | `app.py:1296-1301`, `components/chat_luto.py:1058` |
| Linha do Tempo | Exemplo com 4 marcos | "2001 → 2008 → 2016 → 2035" | `app.py:517-901` |
| Mensagens para o Futuro | Exemplo real com texto datado | Mensagem de 2018 para 2036 | `app.py:3480-3781` |
| Contribuições familiares | Storytelling do Natal 1998 | Cada familiar acrescenta | `app.py:1060-1192`, `app.py:4189-4353` |
| Memorial | Storytelling com filha/irmão/esposa/neto | Construído em conjunto | `components/memorial.py:542-1210` |
| Explorador de Histórias | Card na grade "Tudo o que oferece" | "Responde perguntas sobre a história registrada" | `app.py:1276, 2786, 5013` |

Nenhuma funcionalidade foi distorcida pela humanização. Os exemplos ilustram exatamente o que o app faz.

### 7.6 A Landing desperta curiosidade para explorar o aplicativo?

**Sim.** Evidências:

- O diálogo do Curador termina com a pergunta "E o que você sentiu vendo aquilo?" — deixa o visitante querendo experimentar a interação.
- O exemplo da Mensagem para o Futuro ("Parabéns pelos seus 18 anos…") é concreto o suficiente para que o visitante pense: "Eu quero escrever uma mensagem assim para alguém."
- A timeline com 2001 → 2008 → 2016 → 2035 convida o visitante a pensar nos marcos da própria família.
- O storytelling do Memorial termina com "O neto, anos depois, escreve uma lembrança do avô que só ele guarda" — ativa o desejo de preservação intergeracional.
- A última micro-história ("A história daquela pessoa continua crescendo") convida o visitante a abrir o aplicativo para ver como isso aconteceria na prática.

---

## 8. PRINCÍPIOS APLICADOS

| Diretriz | Resposta |
|---|---|
| Não alterar SEO, Schema.org, robots, sitemap, manifest, favicon | ✅ Nenhuma alteração no `<head>` |
| Não alterar JavaScript estrutural | ✅ Script de menu intocado |
| Não alterar performance, acessibilidade | ✅ Mantido |
| Não alterar páginas legais | ✅ `legais/politicaprivacidade.html` intocado |
| Manter arquitetura construída na Sprint 2 | ✅ 15 seções originais preservadas + 2 novas inseridas em pontos específicos |
| Cada funcionalidade tem que existir no app | ✅ Verificado contra `app.py`, `components/*.py` |
| Não criar funcionalidades inexistentes | ✅ |
| Substituir afirmações abstratas por situações concretas | ✅ 12 micro-histórias adicionadas |
| Curador sem ser chatbot | ✅ Apresentado como guia silencioso com diálogo natural |
| Memorial sem linguagem de luto | ✅ "Construído em conjunto", "continua crescendo" |
| Não usar imagens de bancos genéricos | ✅ Nenhuma imagem adicionada |
| Manter paleta, tipografia, componentes | ✅ Apenas reuso de variáveis e classes já existentes |
| Cada seção deve responder "consigo imaginar alguém da minha família vivendo isso?" | ✅ Todas as novas seções e micro-histórias passaram pelo crivo |

---

## 9. RESUMO FINAL

A Sprint 3 transformou a Landing Page de uma apresentação de plataforma em uma **experiência emocional**, mantendo toda a amplitude da Sprint 2 e adicionando:

- **2 novas seções emocionais:** "Imagine daqui a 30 anos" e "As pequenas histórias".
- **3 citações entre seções** que criam pausas respiratórias.
- **6 micro-histórias concretas** distribuídas pelas seções existentes.
- **5 elementos de storytelling de funcionalidades:** diálogo do Curador, Natal de 1998, Mensagem para o Futuro, Linha do Tempo, Memorial.
- **3 micro-histórias de fecho** com `<em>` para ênfase emocional.

Total de micro-histórias adicionadas: **12**. Total de citações: **3**. Total de seções: **17** (15 originais + 2 novas + 3 inter-quotes com classe própria).

O visitante agora sai da Landing pensando não apenas "a aEterna é uma plataforma completa", mas também:

> "Existem histórias da minha família que eu realmente não quero perder."

Que é o gatilho principal para iniciar o uso da plataforma.

---

**Fim da Sprint 3 — Humanização da Landing e Storytelling.**
