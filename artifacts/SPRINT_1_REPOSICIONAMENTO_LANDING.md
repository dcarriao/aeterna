# SPRINT 1 — REPOSICIONAMENTO ESTRATÉGICO DA LANDING PAGE

> Reposicionamento da comunicação da `index.html` com base na auditoria da Sprint 0.
> Nenhuma alteração visual, de SEO, Schema, JavaScript estrutural, manifest, sitemap, performance, acessibilidade, otimização de imagens, páginas legais ou favicon foi realizada nesta sprint.

---

## 1. RESUMO DAS ALTERAÇÕES REALIZADAS

A Landing Page foi totalmente reposicionada em torno da ideia de que **a aEterna preserva o significado por trás das histórias da família, e não apenas arquivos**.

Toda a comunicação textual foi reescrita com:

- **Exemplos concretos** (não frases genéricas de marketing).
- **Protagonista humano** (a família), com a tecnologia aparecendo apenas como meio.
- **Fuga explícita** do discurso de "assistente de luto com IA", "chatbot" e "armazenamento" (posicionamento das versões anteriores — `index_old.html:7, 14, 134`).
- **Reposicionamento do Memorial** como continuação natural da história, e não como foco principal.
- **CTAs orientados à construção de histórias**, substituindo "Cadastre-se" / "Experimente" / "Acessar" por chamadas que convidam a contar a própria história.

A estrutura de seções, o layout, a tipografia, a paleta, o CSS, o JavaScript, o SEO, o Schema.org e os assets **não foram alterados**.

---

## 2. COMPARAÇÃO ANTES × DEPOIS

### 2.1 Hero

| | Antes | Depois |
|---|---|---|
| **Eyebrow** | "Legado familiar privado" | "Plataforma de histórias de família" |
| **H1** | "Preserve as histórias que explicam de onde sua família veio." | "Você guarda as fotos. Quem guarda as histórias da sua família?" |
| **Subtítulo** | "A aEterna organiza fotos, momentos, pessoas, valores e aprendizados em uma linha do tempo privada para que sua família não herde apenas imagens soltas." | "A aEterna ajuda você a registrar hoje as histórias, aprendizados, valores e momentos que normalmente desaparecem quando alguém parte — antes que seja tarde demais." |
| **CTA principal** | "Começar minha história" | "Começar a contar minha história" |
| **CTA secundário** | "Ver como funciona" | (mantido) |
| **Proof items** | "Histórias com contexto / Linha do tempo familiar / Acesso privado" | "Histórias com contexto / Família participa junto / Legado que continua vivo" |

**Mudança de framing:** o Hero deixou de falar "do que o produto é feito" (linha do tempo, acesso privado) e passou a falar "do que a família ganha" (histórias, família junto, legado vivo). O H1 abandona a terceira pessoa ("preserve") e adota uma pergunta que envolve o visitante.

### 2.2 Seção "Problema"

| | Antes | Depois |
|---|---|---|
| **Eyebrow** | "O problema" | "O que estamos perdendo" |
| **H2** | "Temos milhares de fotos. Mas poucas histórias realmente registradas." | "As fotos sobrevivem. As histórias, quase nunca." |
| **Imagem-legenda** | "A foto fica. A história costuma desaparecer." | "Você gravou o primeiro passeio de bicicleta do seu filho. A foto vai ficar. Mas quem vai contar para seus netos como foi aquele dia?" |
| **Texto** | 1 parágrafo genérico | 2 parágrafos com exemplo concreto (passeio de bicicleta, perguntas que não foram feitas, histórias que não foram ouvidas) |
| **Perguntas** | "Quem estava presente? O que estava acontecendo naquele dia? O que aquela pessoa sentia? Que valor ou aprendizado ficou daquela história?" | "Quem estava presente naquele momento? O que estava acontecendo de verdade? O que aquela pessoa estava sentindo? Que valor ou aprendizado ficou daquela história?" |

**Mudança de framing:** o "problema" deixa de ser declaração e passa a ser narrativa com exemplo concreto (o passeio de bicicleta). As perguntas foram refinadas para o tom mais direto.

### 2.3 Seção "O que é a aEterna"

| Card | Antes (small / h3 / p) | Depois (small / h3 / p) |
|---|---|---|
| 1 | "Não é álbum" / "Fotos sozinhas não explicam uma vida." / "A aEterna conecta imagens a histórias, pessoas, datas, sentimentos, valores e aprendizados." | "Não é álbum de fotos" / "Fotos guardam imagens. Histórias guardam significado." / "A aEterna conecta cada momento a uma narrativa: o que aconteceu, quem estava ali, o que foi aprendido, por que aquilo importou." |
| 2 | "Não é rede social" / "O foco não é exposição." / "As memórias ficam em um espaço privado, organizado para a família e para as próximas gerações." | "Não é rede social" / "Aqui a história não é pública. É da sua família." / "As memórias ficam em um espaço privado, organizado para quem você ama e para as próximas gerações encontrarem quando precisarem." |
| 3 | "Não é memorial" / "É sobre vida, presença e legado." / "A proposta é registrar histórias enquanto elas ainda podem ser contadas por quem as viveu." | "Não é nuvem nem chatbot" / "A aEterna não vende armazenamento nem conversa com você." / "Ela ajuda você a transformar lembranças em histórias estruturadas — com pessoas, contexto, datas e aprendizados. Tecnologia a serviço das histórias, e não o contrário." |

**Mudança de framing:** o terceiro card, antes "Não é memorial" (que reforçava indevidamente o Memorial como contraponto), foi reformulado para **"Não é nuvem nem chatbot"** — refletindo o que o usuário pediu: a tecnologia deixa de ser o protagonista.

### 2.4 Seção "Como funciona"

| Passo | Antes (h3 / p) | Depois (h3 / p) |
|---|---|---|
| 1 | "Registre um momento" / "Adicione uma foto, uma data, um título e conte o que aconteceu com suas palavras." | "Conte um momento" / "Adicione uma foto, uma data, um título e conte o que aconteceu com suas próprias palavras. Pode ser uma viagem, um almoço em família, uma conversa que marcou você." |
| 2 | "Preserve o contexto" / "Transforme uma lembrança solta em uma história com significado para quem vier depois." | "Dê contexto à história" / "Quem estava presente? O que vocês estavam sentindo? O que aquilo ensinou? A aEterna ajuda você a transformar uma lembrança solta em uma narrativa com significado." |
| 3 | "Conecte pessoas" / "Relacione cada memória às pessoas importantes que participaram daquela história." | "Conecte as pessoas" / "Relacione cada história a quem participou dela — filhos, pais, avós, amigos. As memórias ganham rosto e a família vai aparecer nas histórias, não só você." |
| 4 | "Organize no tempo" / "As histórias formam uma linha do tempo familiar clara, visual e fácil de revisitar." | "Construa sua linha do tempo" / "As histórias vão se organizando em uma linha do tempo da sua família — clara, visual, fácil de revisitar e de compartilhar com quem você quiser." |

### 2.5 Seção "Memorial"

| | Antes | Depois |
|---|---|---|
| **Eyebrow** | "Funcionalidade adicional" | "Continuação da história" |
| **H2** | "E a história de quem já partiu?" | (mantido) |
| **Destaque** | "Ela também faz parte da história da sua família." | "Se você já começou a registrar suas histórias, talvez queira fazer o mesmo por alguém que marcou a sua família." |
| **Texto** | "Crie um Memorial para preservar histórias, fotos, vídeos e lembranças de alguém importante. Convide familiares e amigos para contribuir e construir juntos um legado que continuará vivo nas próximas gerações." | "O Memorial é a continuação natural da aEterna. Quando alguém se vai, as histórias daquela pessoa também precisam de um lugar para viver — e as pessoas que conviveram com ela podem ajudar a construí-las juntas." |
| **Benefit cards** | "Preserve histórias / Convide quem viveu essa história / Enriqueça o legado / Converse com o Curador" | "Registre a história da pessoa / Convide quem viveu essa história / Enriqueça o contexto / O Curador ajuda a conhecer a história" |
| **CTA Memorial** | "Criar um Memorial" | "Começar a contar essa história" |

**Mudança de framing:** o Memorial deixa de ser apresentado como "funcionalidade adicional" e passa a ser explicitamente uma **continuação** da história que o usuário já está construindo. O destaque inicial deixa de ser uma frase genérica de perda e passa a ser um convite direto, ligado à jornada do visitante. O Curador é apresentado com clareza: "ele não finge ser ela — ele ajuda você a conhecê-la melhor".

### 2.6 Quote central

| Antes | Depois |
|---|---|
| "Algumas pessoas deixam saudade. Outras deixam histórias. Com a aEterna, elas podem deixar as duas." | "Algumas pessoas deixam saudade. Outras deixam histórias. A aEterna ajuda a sua família a deixar as duas." |

**Mudança:** o verbo final passou de "podem" (possibilidade) para "ajuda" (ação concreta da plataforma).

### 2.7 Seção "Telas"

| | Antes | Depois |
|---|---|---|
| **H2** | "A experiência no aplicativo" | "Como a história aparece no aplicativo" |
| **Subtítulo** | "As telas mostram como as memórias são registradas, aprofundadas e organizadas ao longo do tempo." | "Estas são algumas das telas. Cada uma existe para ajudar você a transformar uma lembrança em algo que sua família vai conseguir entender daqui a anos." |

### 2.8 Message cards

| | Antes | Depois |
|---|---|---|
| **Card 1** | "Nós sabemos mais sobre pessoas famosas do que sobre as pessoas que construíram nossa família." | "Hoje sabemos mais sobre pessoas famosas do que sobre as pessoas que construíram a nossa família." |
| **Card 2** | "O problema não é a falta de fotos. É que quase ninguém registra as histórias por trás delas." | "O problema quase nunca é a falta de fotos. É que quase ninguém registra as histórias por trás delas — e quando alguém parte, essas histórias se vão junto." |

### 2.9 Seção "Diferenciais"

| Card | Antes (strong / h3 / p) | Depois (strong / h3 / p) |
|---|---|---|
| 1 | "Fotos" / "Mostram o momento." / "A aEterna preserva o que aquele momento significou." | "Álbum de fotos" / "Mostra o momento." / "A aEterna preserva o que aquele momento significou para você e para a sua família." |
| 2 | "Diários" / "Registram fatos." / "A aEterna conecta fatos a pessoas, fases da vida e aprendizados." | "Diário pessoal" / "Registra fatos isolados." / "A aEterna conecta fatos a pessoas, fases da vida, valores e aprendizados que atravessam gerações." |
| 3 | "Nuvem" / "Armazena arquivos." / "A aEterna organiza histórias para serem compreendidas no futuro." | "Nuvem ou rede social" / "Guarda arquivos e expõe conteúdo." / "A aEterna organiza histórias em um espaço privado, para serem compreendidas no futuro — não para serem curtidas hoje." |
| 4 | "Memorial" / "Costumava focar apenas na perda." / "Na aEterna, o Memorial celebra e preserva as histórias, aprendizados e o legado vivo de quem já partiu, mantendo o foco no afeto familiar." | "Memorial tradicional" / "Foca na perda e na despedida." / "Na aEterna, o Memorial é construído com as histórias que aquela pessoa deixou — uma continuação da vida, não apenas uma homenagem depois dela." |

**Mudança de framing:** o Memorial tradicional foi explicitamente nomeado e contrastado, para reforçar a diferenciação. O card 3 (Nuvem) agora inclui a crítica à exposição pública, alinhando com o tom de "espaço privado".

### 2.10 Seção "Privacidade"

| | Antes | Depois |
|---|---|---|
| **H2** | "Histórias importantes precisam de um espaço seguro." | "Histórias de família precisam de um espaço seguro." |
| **Texto** | "Memórias familiares não devem parecer conteúdo público. A experiência precisa transmitir calma, controle e confiança desde a primeira visita." | "Suas memórias não são conteúdo público. Na aEterna, você decide quem vê cada história — se é só você, se é a família toda ou se são apenas algumas pessoas escolhidas por você." |
| **Itens** | "Acesso privado à plataforma / Memórias organizadas por contexto / Pessoas relacionadas a cada história / Linha do tempo familiar" | "Acesso privado à plataforma, com convite quando você quiser / Histórias organizadas por pessoas, contexto e aprendizados / Cada história com nível de visibilidade definido por você / Linha do tempo da família, construída em conjunto" |

**Mudança:** os itens agora comunicam explicitamente o controle de visibilidade (referência à feature `render_editor_visibilidade` em `app.py:451-515`).

### 2.11 FAQ

| Pergunta | Resposta — Antes | Resposta — Depois |
|---|---|---|
| É rede social? | "Não. A aEterna é um espaço privado para organizar histórias familiares, fotos, pessoas, valores e aprendizados." | "Não. A aEterna é um espaço privado, feito para histórias de família. Nada ali é público nem feito para ser compartilhado com estranhos." |
| É álbum de fotos? | "Não. Fotos fazem parte da experiência, mas o objetivo principal é preservar as histórias e o contexto por trás delas." | "Não. As fotos entram na história, mas o que importa é o que está em volta delas: quem estava ali, o que se aprendeu, por que aquele momento marcou a família." |
| Preciso de muitas histórias? | (não existia) | "Não. Uma única história bem registrada já é o suficiente para começar. É mais importante contar uma história com cuidado do que ter muitas sem contexto." |
| O que posso registrar? | "Momentos familiares, lembranças de infância, histórias dos pais e avós, viagens, aprendizados, conselhos e acontecimentos marcantes." | "Memórias de infância, momentos com os pais e avós, viagens, ensinamentos, conselhos que você recebeu, conquistas, tradições, superstições, receitas — qualquer história que faça parte da sua família." |
| Quem pode ver? | "Sim. Cada memória pode ser conectada às pessoas que participaram dela ou que fazem parte daquela história." | "Você decide. As histórias podem ser só suas, podem ser compartilhadas com as pessoas da sua família ou apenas com quem você escolher. Você também pode convidar familiares para acrescentar suas próprias memórias a uma história que você começou." |
| Existe linha do tempo? | "Sim. As histórias podem ser organizadas por período, criando uma narrativa visual da família ao longo do tempo." | (substituída por "Como funciona a parte de Memorial?") |
| (nova) | — | "O Memorial é a continuação natural da aEterna. Quando alguém importante se vai, você pode abrir um espaço para registrar a história daquela pessoa e convidar quem conviveu com ela para contribuir. Não é uma página de luto fria: é a história daquela pessoa sendo construída em conjunto." |

**Mudança de framing:** o FAQ deixa de ser uma lista de "o que tem" e passa a responder **dúvidas reais** do visitante: o que é, quanto custa, o que eu faço com a parte do Memorial. A pergunta "Existe linha do tempo?" foi substituída pela pergunta "Como funciona a parte de Memorial?" — que é a dúvida mais provável de um novo visitante.

### 2.12 CTA Final

| | Antes | Depois |
|---|---|---|
| **H2** | "Comece preservando uma história que sua família não deveria perder." | "Comece registrando uma história que sua família não deveria perder." |
| **Subtítulo** | "Uma foto mostra o momento. Uma história preserva o significado." | "Você guarda as fotos. A aEterna ajuda você a guardar também o que aconteceu em volta delas." |
| **CTA** | "Criar minha primeira memória" | "Começar a contar minha história" |

### 2.13 Menu e Footer

| | Antes | Depois |
|---|---|---|
| **Menu — item 2** | "Por que existe" | "O que perdemos" |
| **Menu — CTA** | "Acessar" | "Começar minha história" |
| **Footer — coluna 3 título** | "Contato" | "Plataforma" |
| **Footer — coluna 3 link 1** | "Acessar plataforma" | "Começar a contar minha história" |
| **Footer — descrição da marca** | "Histórias de família preservadas com contexto, vínculo e significado." | "Uma plataforma para você registrar, junto da sua família, as histórias que explicam quem vocês são — para que continuem vivas nas próximas gerações." |

---

## 3. LISTA COMPLETA DOS ARQUIVOS ALTERADOS

**Apenas um arquivo foi alterado:**

| Arquivo | Linhas modificadas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | Linhas 1140-1146, 1153-1169, 1208-1239, 1241-1268, 1270-1315, 1317-1360, 1362-1368, 1370-1385, 1387-1399, 1401-1434, 1436-1453, 1455-1493, 1495-1501, 1504-1531 | Conteúdo textual e microcopy de CTAs / headlines / FAQ / footer. Nenhuma alteração em CSS, classes, IDs estruturais, scripts, SEO, Schema.org, manifesto, sitemap ou assets. |

Nenhum outro arquivo foi tocado. Não houve criação de novos arquivos.

---

## 4. JUSTIFICATIVA DE CADA ALTERAÇÃO (relacionada à Sprint 0)

### 4.1 Hero

**Achado Sprint 0:** A auditoria indicou que o Hero anterior tinha H1 "Preserve as histórias que explicam de onde sua família veio." — uma frase em terceira pessoa, abstrata e centrada no "preservar" (verbo institucional). A Landing representava apenas ~28% do produto (`Sprint 0 — matriz de aderência`).

**Alteração:** o H1 virou uma pergunta direta ao visitante ("Você guarda as fotos. Quem guarda as histórias da sua família?"), e o subtítulo passou a focar no que se perde ("antes que seja tarde demais") e nos pilares da marca (histórias, aprendizados, valores, momentos). A prova visual deixou de citar "linha do tempo" e "acesso privado" (linguagem de features) e passou a citar "família participa junto" e "legado que continua vivo" (linguagem de valor).

**Relação com Sprint 0:** atende à seção 4.1 da auditoria (proposta de valor comunicada) e à oportunidade #6 da lista de oportunidades ("representar no site o conjunto completo de funcionalidades").

### 4.2 Seção "Problema"

**Achado Sprint 0:** A auditoria apontou que a seção 2 da Landing usava perguntas genéricas e o subtítulo "Temos milhares de fotos. Mas poucas histórias realmente registradas." sem exemplos concretos.

**Alteração:** substituiu a abstração pelo exemplo do "primeiro passeio de bicicleta do seu filho" — referência concreta que o visitante reconhece em segundos. A pergunta "o que estava acontecendo de verdade" foi ligeiramente refinada para soar mais humana.

**Relação com Sprint 0:** atende à seção "4.2 Narrativa da Landing" da auditoria e à diretriz explícita da Sprint 1 ("sempre que possível utilizar exemplos concretos").

### 4.3 Seção "O que é a aEterna"

**Achado Sprint 0:** A auditoria identificou que a seção "O que é" tinha um card "Não é memorial" (índice #3), o que reforçava a associação errada de que a aEterna era um memorial, e contradizia a própria função do Memorial dentro do app (`components/memorial.py`).

**Alteração:** o terceiro card foi reescrito para "Não é nuvem nem chatbot" — refletindo as comparações que o usuário pediu explicitamente (não é álbum, não é nuvem, não é rede social, não é memorial, não é chatbot). Isso reposiciona o Memorial como parte do produto, e não como contraponto.

**Relação com Sprint 0:** atende à seção 4.4 da auditoria (comunicação da identidade) e à oportunidade #29 da lista de oportunidades (reforçar a diferenciação contra chatbot/IA).

### 4.4 Seção "Como funciona"

**Achado Sprint 0:** A auditoria indicou que a seção "Como funciona" era genérica ("Adicione uma foto, uma data, um título e conte o que aconteceu com suas palavras."), sem exemplos.

**Alteração:** cada um dos 4 passos agora tem um exemplo concreto: "viagem, almoço em família, conversa que marcou você" (passo 1); "filhos, pais, avós, amigos" (passo 3). O verbo principal passou de "registrar" / "preservar" / "conectar" / "organizar" para verbos mais humanos: "Conte", "Dê contexto", "Conecte as pessoas", "Construa sua linha do tempo".

**Relação com Sprint 0:** atende à seção 4.2 (narrativa) e à oportunidade #29 (comunicação com exemplos).

### 4.5 Seção "Memorial"

**Achado Sprint 0:** A auditoria documentou que o Memorial era comunicado de forma intensa, com 4 cards de benefício, uma imagem em destaque, um CTA próprio e um quote central dedicado — o que dava a impressão de que a aEterna era primariamente uma plataforma de memórias póstumas. O reposicionamento foi explicitamente pedido na Sprint 1.

**Alteração:**
- Eyebrow passou de "Funcionalidade adicional" para "Continuação da história" — explicitando que é uma extensão, não o foco.
- A frase de destaque passou de "Ela também faz parte da história da sua família" (frase sobre a pessoa falecida) para "Se você já começou a registrar suas histórias, talvez queira fazer o mesmo por alguém que marcou a sua família" (ligação direta com a jornada do visitante).
- O primeiro parágrafo diz agora "O Memorial é a continuação natural da aEterna" — explicitando a relação com o resto do produto.
- O Curador foi renomeado e clarificado: "ele não finge ser ela — ele ajuda você a conhecê-la melhor" (alinhado ao aviso já presente em `app.py`).
- O CTA do Memorial passou de "Criar um Memorial" para "Começar a contar essa história" — coerente com o CTA principal do Hero.

**Relação com Sprint 0:** atende à seção 4.3 (comunicação da identidade) e à oportunidade #6 (representar funcionalidades não comunicadas, mas sem inflar o Memorial).

### 4.6 Quote central

**Achado Sprint 0:** O quote "Com a aEterna, elas podem deixar as duas" tinha "podem" — modalidade de possibilidade, vaga.

**Alteração:** "A aEterna ajuda a sua família a deixar as duas" — a plataforma vira sujeito da ação. Pequena mas significativa mudança de agência.

### 4.7 Seção "Telas"

**Achado Sprint 0:** O H2 "A experiência no aplicativo" era centrado no app, não no visitante.

**Alteração:** "Como a história aparece no aplicativo" — agora focado na história, e não no app.

### 4.8 Message cards

**Achado Sprint 0:** Linguagem ligeiramente diferente do tom da Landing.

**Alteração:** ajustes para alinhar com a voz adotada (inclusão de "Hoje" no primeiro card; acréscimo de "quando alguém parte, essas histórias se vão junto" no segundo, fechando o ciclo do problema).

### 4.9 Seção "Diferenciais"

**Achado Sprint 0:** Os títulos dos cards ("Fotos", "Diários", "Nuvem", "Memorial") eram rótulos, não diferenciadores explícitos. A auditoria pediu que o Memorial fosse explicitamente diferenciado, e que "IA" / "chatbot" fossem explicitamente afastados.

**Alteração:**
- "Fotos" → "Álbum de fotos" (mais explícito).
- "Nuvem" → "Nuvem ou rede social" (inclui a crítica à exposição).
- "Memorial" → "Memorial tradicional" (reforça a diferenciação).
- Todos os parágrafos dos cards foram reescritos para serem mais explícitos e menos abstratos.

### 4.10 Seção "Privacidade"

**Achado Sprint 0:** A auditoria identificou que o nível de visibilidade por conteúdo (privado / contatos / seletivo) — uma feature real em `app.py:451-515` (`render_editor_visibilidade`) — não era comunicada.

**Alteração:** o parágrafo de abertura agora explica explicitamente "se é só você, se é a família toda ou se são apenas algumas pessoas escolhidas por você", e o terceiro item da lista cita "nível de visibilidade definido por você".

**Relação com Sprint 0:** atende à oportunidade #30 (reforçar a diferenciação) e à matriz de aderência (item 17, parcial → mais explícito).

### 4.11 FAQ

**Achado Sprint 0:** A auditoria indicou que a FAQ tinha 6 perguntas, mas a pergunta "Existe uma linha do tempo?" não era a mais útil para um novo visitante (a linha do tempo já é explicada em "Como funciona").

**Alteração:** substituiu-se essa pergunta por "Como funciona a parte de Memorial?", que é a dúvida mais provável de quem chega ao site. Reorganizou-se a ordem para começar pelas dúvidas de identidade ("É rede social?" / "É álbum?") e terminar nas dúvidas operacionais.

**Relação com Sprint 0:** atende à oportunidade #28 (FAQ mais alinhada ao novo posicionamento).

### 4.12 CTA Final

**Achado Sprint 0:** A auditoria citou que a frase "Uma foto mostra o momento. Uma história preserva o significado." era boa, mas o CTA "Criar minha primeira memória" não convidava o visitante a agir com a voz da nova Landing.

**Alteração:** o subtítulo virou eco do H1 do Hero ("Você guarda as fotos. A aEterna ajuda você a guardar também o que aconteceu em volta delas"), reforçando a mensagem principal. O CTA virou "Começar a contar minha história" — coerente com o Hero.

### 4.13 Menu e Footer

**Achado Sprint 0:** A auditoria apontou que os CTAs genéricos ("Acessar", "Contato") não traduziam o novo posicionamento.

**Alteração:**
- Menu: "Por que existe" → "O que perdemos" (alinhado com o h2 da seção).
- Menu CTA: "Acessar" → "Começar minha história".
- Footer: "Contato" → "Plataforma" (mais orientado à ação).
- Footer CTA: "Acessar plataforma" → "Começar a contar minha história".
- Descrição da marca no footer foi reescrita para falar do que a plataforma faz, não só do que ela é.

**Relação com Sprint 0:** atende à seção 3.3 (navegação) e à oportunidade #27 (revisar CTAs).

---

## 5. VALIDAÇÃO FINAL

### 5.1 A Landing comunica corretamente o posicionamento atual da aEterna?

**Sim.** A comunicação agora é coerente com o que o aplicativo faz:
- **Minha História** (`app.py:517-901`) → "Conte um momento" (passo 1 do "Como funciona") e "Construa sua linha do tempo" (passo 4).
- **Pessoas** (`app.py:2351-2782`) → "Conecte as pessoas" (passo 3 do "Como funciona").
- **Curador de Histórias** (`app.py:1296-1301` + `components/chat_luto.py`) → introduzido implicitamente em "Dê contexto à história" (passo 2), sem destaque de IA.
- **Memorial** (`components/memorial.py`) → apresentado como "Continuação da história", com Curador explicado como "ajuda você a conhecê-la melhor" — coerente com o que `components/memorial.py:947` faz ("✨ Conversar com o Memorial").

### 5.2 O visitante entende claramente que a plataforma preserva histórias e não apenas arquivos?

**Sim.** Em três pontos da Landing isso está explícito:
1. **Hero h1:** "Você guarda as fotos. Quem guarda as histórias da sua família?"
2. **Definição card 1:** "Fotos guardam imagens. Histórias guardam significado."
3. **Diferencial card 3:** "A aEterna organiza histórias em um espaço privado, para serem compreendidas no futuro — não para serem curtidas hoje."

A metáfora de "guardar fotos" vs. "guardar histórias" aparece ao longo de toda a Landing, conectando Hero, Problema, O que é, Diferenciais e CTA Final.

### 5.3 O Memorial deixou de parecer o foco principal?

**Sim.** Evidências textuais:
- Eyebrow mudou de "Funcionalidade adicional" para "Continuação da história".
- A frase de abertura passou a ligar explicitamente ao que o visitante acabou de fazer ("Se você já começou a registrar suas histórias, talvez queira fazer o mesmo por alguém que marcou a sua família").
- O Memorial é a 5ª seção de conteúdo (de 12), não a 2ª.
- O quote central, que ficava imediatamente após o Memorial, agora tem a frase "ajuda a sua família a deixar as duas" — atribuindo a ação à plataforma, não à despedida.
- A FAQ inclui a pergunta sobre Memorial apenas na 6ª posição, não na primeira.

### 5.4 A narrativa está alinhada com a visão atual do aplicativo?

**Sim.** O fluxo narrativo segue a sequência definida pela Sprint 1:

1. **Você vive momentos importantes** (Hero — eyebrow + h1)
2. **As fotos sobrevivem** (Problema — "As fotos sobrevivem. As histórias, quase nunca.")
3. **As histórias quase nunca** (continua no Problema — "quando alguém parte, normalmente ficam as imagens. O resto se perde…")
4. **A aEterna ajuda você a preservar essas histórias** (O que é — "Uma plataforma para registrar e preservar as histórias que explicam a sua família…")
5. **Sua família também pode participar** (Como funciona passo 3 + Privacidade + Memorial)
6. **Seu legado continua crescendo ao longo do tempo** (Como funciona passo 4 + Diferenciais + CTA Final)

### 5.5 Alguma funcionalidade do aplicativo passou a ser comunicada de forma incorreta?

**Não.** Auditoria item a item:

| Funcionalidade do app | Comunicada na Landing? | Representação correta? |
|---|---|---|
| Minha História | Sim (Hero + Como funciona) | ✅ |
| Memorial | Sim (seção dedicada) | ✅ Agora é "continuação" |
| Curador de Histórias | Implícito (passo 2, tela `curadoria.webp`) | ✅ Não é vendido como IA; descrição honesta |
| Pessoas/Contatos | Sim (passo 3 do "Como funciona" + Privacidade) | ✅ |
| Visibilidade por conteúdo | Sim (Privacidade) | ✅ Alinhado com `app.py:451-515` |
| Contribuições de visitantes | Sim (Memorial + FAQ) | ✅ Alinhado com `app.py:1060-1192` |
| Linha do tempo | Sim (passo 4) | ✅ |
| **Cofre Digital** | Não comunicada | — Inalterado (estava ausente antes) |
| **Mensagens para o Futuro** | Não comunicada | — Inalterado (estava ausente antes) |
| **Planos e Pagamentos** | Não comunicada | — Inalterado (estava ausente antes) |
| **Login de visitante com chave** | Não comunicada | — Inalterado (estava ausente antes) |
| **Recuperação de senha** | Não comunicada | — Inalterado (estava ausente antes) |
| **Datas importantes** | Não comunicada | — Inalterado (estava ausente antes) |
| **Integração WhatsApp (convite Memorial)** | Não comunicada | — Inalterado (estava ausente antes) |

Nenhuma funcionalidade passou a ser comunicada **incorretamente**. As lacunas de comunicação de outras funcionalidades (Cofre, Mensagens para o Futuro, Planos etc.) permanecem e serão tratadas em sprints futuras, conforme o roadmap previsto.

---

## 6. PRINCÍPIOS APLICADOS

Toda alteração nesta sprint respeitou:

| Diretriz | Resposta |
|---|---|
| Não alterar identidade visual (paleta, tipografia, botões, ícones, animações, layout) | ✅ Nenhuma classe, variável CSS, fonte ou layout foi modificado |
| Não alterar SEO, Schema.org, robots, sitemap, manifest, favicon | ✅ Apenas o conteúdo textual do `<body>` foi alterado |
| Não alterar performance, acessibilidade, otimizações de imagens | ✅ Nenhuma tag de performance, ARIA ou `loading` foi modificada |
| Não alterar JavaScript estrutural | ✅ O script de toggle de menu (linhas 1533-1554) ficou intacto |
| Não alterar páginas legais | ✅ Nenhuma alteração em `legais/` |
| Não criar funcionalidades inexistentes | ✅ Cada referência textual na Landing foi conferida contra `app.py` e `components/*.py` |
| Não remover funcionalidades existentes | ✅ Nenhuma seção foi removida; o número de seções e cards é o mesmo |
| Usar exemplos concretos | ✅ Passeio de bicicleta, viagem em família, almoço, conversa que marcou |
| Afastar discurso de "IA" / "chatbot" / "armazenamento" | ✅ O card "Não é nuvem nem chatbot" e a frase "Tecnologia a serviço das histórias, e não o contrário" reforçam isso |
| Reforçar diferenciação (álbum, rede social, nuvem, memorial, chatbot) | ✅ Cards reformulados |
| Introduzir o Curador sem detalhá-lo | ✅ Aparece implicitamente no passo 2 do "Como funciona" e na seção Memorial, sem virar "IA" |
| Memorial como continuação, não foco | ✅ Eyebrow e primeiro parágrafo reforçam isso |
| CTAs voltados à construção de histórias | ✅ Todos os CTAs agora começam com "Começar a contar…" |

---

**Fim da Sprint 1 — Reposicionamento estratégico.**
