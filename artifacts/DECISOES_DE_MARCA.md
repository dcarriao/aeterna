# DECISÕES DE MARCA — aEterna

> Registro histórico das principais decisões de marca e produto da aEterna. Este documento é o "ADR de marca" — quando alguém no futuro perguntar "por que fizemos isso?", a resposta está aqui. Inspirado no padrão de Architecture Decision Records (ADR), mas focado em decisões de marca, comunicação e produto.

> Toda decisão aqui foi tomada ao longo das Sprints 0 a 5.6.3 e reflete o que foi construído. Nenhuma decisão é inferência. Cada entrada registra o contexto, a decisão, as alternativas consideradas e as consequências.

---

## Formato de cada entrada

```
### [Data da decisão] — [Título curto da decisão]

**Contexto:** O que motivou a decisão.

**Decisão:** O que foi decidido.

**Por que:** As razões por trás.

**Alternativas consideradas:** O que poderia ter sido feito em vez disso, e por que não foi.

**Consequências:** O que mudou em função da decisão.

**Sprint de origem:** Qual sprint consolidou a decisão.
```

---

## 1. 2026 — A aEterna não é um "memorial digital"

**Contexto:** No início (Sprint 0, Sprint 1), a aEterna carregava um posicionamento herdado de versões antigas do produto (visível em `index_old.html` e `index_old5.html`), que a tratava como "assistente de luto com IA" e "memorial digital". Esse posicionamento conflitava com a visão da plataforma como lugar de **continuação** da história familiar.

**Decisão:** A aEterna é definida como "o lugar onde a história da sua família continua sendo construída, compartilhada e preservada ao longo das gerações". Memorial é um módulo opcional, focado em **continuação da vida**, não em despedida.

**Por que:** O público-alvo da aEterna é a família que está vivendo suas memórias, não apenas a família em luto. Um posicionamento centrado em "memorial digital" limita a plataforma ao momento de perda e ignora o uso cotidiano. Além disso, o termo "memorial" no Brasil tem conotação funerária forte, o que distancia o produto das pessoas que ainda não perderam ninguém.

**Alternativas consideradas:**
- "Plataforma de memórias da família": genérico, não diferenciado, não comunica o valor.
- "Rede social privada de família": posicionamento errado (não é rede social).
- "Assistente de IA para memórias": protagonismo da tecnologia em vez da família.

**Consequências:**
- Toda comunicação da aEterna passou a evitar linguagem de luto, despedida e perda.
- O Memorial foi reposicionado como "continuação da vida", não como "homenagem depois da morte".
- O produto passou a comunicar para famílias que estão vivendo, não apenas para famílias em luto.

**Sprint de origem:** Sprint 1 (Repositionamento da Landing).

---

## 2. 2026 — O Curador não é vendido como IA

**Contexto:** O produto tem um assistente baseado em IA (chat_luto.py, assistente_ia.py). A tentação natural seria chamá-lo de "assistente de IA" ou "IA da aEterna" para vender a tecnologia. Mas isso traria dois problemas: (1) faria o protagonismo ser da tecnologia, não da família; (2) traria desconfiança (muitas pessoas têm receio de "IA escrevendo sobre suas vidas").

**Decisão:** O Curador é apresentado como um **guia** que faz perguntas para ajudar a pessoa a lembrar. Não é "IA" nem "assistente" nem "chatbot". É um guia.

**Por que:** O Curador é uma ferramenta de organização, não de criação. Ele não inventa histórias — ele ajuda a pessoa a lembrar o que ela já sabe. Comunicar isso como "IA" gera expectativa errada (de que a IA vai criar a história sozinha) e desconfiança (de que a IA vai "inventar" coisas).

**Alternativas consideradas:**
- "Assistente de histórias": "assistente" sugere autonomia, como se o assistente fizesse coisas sozinho.
- "IA da aEterna": protagonismo da tecnologia.
- "Robô": impessoal, frio.

**Consequências:**
- O Curador é descrito como "guia silencioso", "guia de histórias" ou "Curador de Histórias".
- O Curador nunca consola, celebra ou opina — apenas pergunta e organiza.
- O Curador não escreve ficção nem substitui pessoas.
- Toda comunicação sobre o Curador foca no que ele faz (perguntar, organizar) e não na tecnologia por trás.

**Sprint de origem:** Sprint 1, consolidado na Sprint 5.7.

---

## 3. 2026 — A Landing passou a vender histórias, não funcionalidades

**Contexto:** A Landing original (Sprint 0, visível em `index_old.html`) era uma apresentação de funcionalidades: planos, preços, recursos, tecnologia. Isso era linguagem de startup vendendo software, não de plataforma que toca a vida das pessoas.

**Decisão:** A Landing passou a ser construída em torno de **histórias**. As funcionalidades aparecem, mas subordinadas à narrativa principal: "a história da sua família ainda está sendo escrita".

**Por que:** O visitante da Landing é uma pessoa (não um decisor de compra corporativo). Essa pessoa não quer saber "o que o produto faz", quer entender "o que o produto muda na minha vida". A narrativa de história é o que responde a essa pergunta.

**Alternativas consideradas:**
- "Plataforma X funcionalidades Y": lista de features, frieza, sensação de "mais um app".
- "Benefícios do produto": vaga, não diferencia.
- "Cases de sucesso": pareceria "depoimento", estranho para um produto que lida com família.

**Consequências:**
- A Landing passou a ter um Hero com uma pergunta provocativa ("O que suas fotos vão contar quando você não estiver mais aqui?"), não um slogan.
- As funcionalidades aparecem em "Tudo o que a plataforma oferece", subordinadas à narrativa.
- O Hero passou a ser um carrossel de histórias reais (Sprint 5.6), não uma tela de aplicativo.
- O CTA "Ler esta história" abre um modal com a história completa (Sprint 5.6.3), não leva direto para o app.

**Sprint de origem:** Sprint 1, refinado nas Sprints 2, 3, 4, 5.6 e 5.6.3.

---

## 4. 2026 — A fotografia é documental, não publicitária

**Contexto:** Ao longo das Sprints 2-4, a aEterna começou a usar imagens de banco (famílias em situações cotidianas). Inicialmente, considerou-se o uso de imagens "polidas" de banco profissional. Mas essas imagens transmitiam um sentimento de "propaganda" que conflitava com a proposta de "família real, momento real".

**Decisão:** A fotografia da aEterna é **documental**. Parece foto de família tirada por alguém da família, não foto de banco de imagens profissional. Imperfeições são aceitas e até bem-vindas.

**Por que:** A aEterna vende preservação de memórias reais. Se a própria comunicação usa imagens artificialmente perfeitas, a promessa de "real" perde credibilidade. A fotografia documental reforça a autenticidade.

**Alternativas consideradas:**
- Banco de imagens profissional (Getty, Shutterstock): muito polido, sensação de "propaganda".
- Imagens de IA: proibidas por padrão, por questão de autenticidade e por problemas de representação.
- Fotos de família cedidas por usuários: ideal para o futuro, mas ainda não viável em escala.

**Consequências:**
- As 13 imagens do Hero (carrossel de histórias) foram selecionadas com critérios documentais.
- O guia `DIRECAO_FOTOGRAFICA.md` foi criado para garantir consistência futura.
- Toda imagem aprovada para uso em comunicação precisa passar pelo checklist do guia.
- Diversidade (étnica, estrutura familiar, faixa etária) é tratada como natural, não como campanha.

**Sprint de origem:** Sprint 2 (introdução de imagens), refinado nas Sprints 4 e 5.6, formalizado na Sprint 5.7.

---

## 5. 2026 — Diversidade é representação natural, não campanha

**Contexto:** Ao selecionar as 8 imagens do carrossel do Hero, considerou-se a questão da representatividade. A tentação natural seria criar uma "campanha de diversidade" com texto explícito ("celebramos todas as famílias"). Mas isso transformaria a diversidade em um marcador comercial, em vez de uma característica natural.

**Decisão:** A diversidade aparece de forma orgânica nas imagens e histórias da aEterna. Não há texto explicito sobre diversidade. A regra é simples: a fotografia da aEterna deve parecer um álbum de família real, e famílias reais são diversas por natureza.

**Por que:** Quando a diversidade é comunicada explicitamente, ela se torna um "claim" comercial que precisa ser justificado. Quando aparece naturalmente, ela é simplesmente "como as coisas são". Isso é mais autêntico e menos sujeito a críticas.

**Alternativas consideradas:**
- "Celebramos todas as famílias": comunicação explícita, mas soa como campanha de marketing.
- "Famílias diversas": explícito, mas redundante (todas as famílias são diversas por natureza).
- Nenhuma menção à diversidade: silenciar a questão também não é ideal.

**Consequências:**
- O carrossel do Hero tem 8 histórias representando famílias brancas, negras, asiáticas, em diferentes estruturas (casal com filhos, mãe solo, avós com netos, casal homoafetivo reservado para futuro).
- Não há texto "narrativo" sobre diversidade na Landing.
- O guia `DIRECAO_FOTOGRAFICA.md` documenta o critério de forma operacional.

**Sprint de origem:** Sprint 2 (introdução de imagens), formalizado na Sprint 5.7.

---

## 6. 2026 — O Hero passou a mostrar uma foto ganhando significado

**Contexto:** O Hero original (Sprint 0, Sprint 1, Sprint 2) mostrava um screenshot do aplicativo. Isso comunicava "este é o app", mas não criava uma reação emocional. A Landing explicava o que a aEterna fazia, mas não mostrava o **efeito** da aEterna.

**Decisão:** O Hero passou a mostrar uma **transformação visual**: a mesma foto aparecia duas vezes, uma sem contexto (foto comum) e outra com overlays (avatar, nome, data, história) — representando a transformação que a aEterna provoca.

**Por que:** Mostrar o **efeito** do produto (a transformação) é mais poderoso do que mostrar a **interface** do produto. O visitante entende o que a aEterna faz ao ver a transformação acontecer, não ao ver um botão de menu.

**Alternativas consideradas:**
- Screenshot do app (Sprint 0-1): mostra interface, mas não emoção.
- Mockup de smartphone (Sprint 4): sofisticado, mas ainda é "mostrar a ferramenta".
- Transformação foto → história (Sprint 5.5): mostra o efeito.

**Consequências:**
- O Hero foi refinado para mostrar 8 histórias reais em um carrossel (Sprint 5.6).
- O CTA "Ler esta história" abre um modal com a história completa (Sprint 5.6.3), não leva direto para o app.
- O Hero agora é uma demonstração viva do que a aEterna faz, não uma explicação.

**Sprint de origem:** Sprint 5.5, refinado nas Sprints 5.6 e 5.6.3.

---

## 7. 2026 — Linguagem de luto é proibida em toda comunicação

**Contexto:** A comunicação inicial do produto (visível em `index_old.html` e `index_old3.html`) usava linguagem como "em memória de", "descansa em paz", "luto", "despedida", "página fúnebre". Essa linguagem distanciava o produto das pessoas que ainda não perderam ninguém.

**Decisão:** A aEterna nunca usa linguagem de luto, despedida ou morte explícita. O Memorial é descrito como "continuação da vida", não como "homenagem depois da morte".

**Por que:** A aEterna quer ser um lugar para famílias que estão vivendo, não apenas para famílias em luto. Linguagem de luto limita o produto ao momento de perda e o torna "pesado". Famílias em momentos felizes também merecem preservar suas memórias.

**Alternativas consideradas:**
- Linguagem explícita de luto: pesada, distanciadora.
- Linguagem neutra: genérica, sem emoção.
- Linguagem de "continuação da vida": emocional sem ser pesada.

**Consequências:**
- Toda comunicação da aEterna passou a evitar palavras como "luto", "despedida", "em memória de", "descansa em paz", "página fúnebre".
- O Memorial é descrito como "a história de [nome] continua sendo construída pela família".
- A Landing passou a falar de "histórias que atravessam gerações" em vez de "histórias preservadas depois da morte".

**Sprint de origem:** Sprint 1, refinado nas Sprints 3, 4 e 5.7.

---

## 8. 2026 — A aEterna não é uma rede social privada

**Contexto:** Ao posicionar a aEterna como "rede social privada de família" (visível em `index_old3.html` e `index_old5.html`), o produto perdia diferenciação. Existem dezenas de apps de "rede social privada de família", e nenhum deles conseguiu escalar. O posicionamento era genérico.

**Decisão:** A aEterna é definida como "lugar onde a história da sua família continua sendo escrita" — não uma rede social. Não tem feed, não tem likes, não tem seguidores, não tem algoritmo de engajamento.

**Por que:** "Rede social" implica conteúdo público (mesmo que privado) com dinâmica social (comentários, likes, follows). A aEterna é diferente: é um lugar para a **própria família** preservar e construir a história ao longo do tempo. Não há dinâmica social.

**Alternativas consideradas:**
- "Rede social privada de família": genérico, disputado por concorrentes.
- "Rede privada de memórias": ainda sugere feed.
- "Espaço privado da família": próximo, mas genérico.
- "Lugar onde a história da sua família continua sendo escrita": específico, diferencia.

**Consequências:**
- A Landing nunca usa o termo "rede social" para se descrever.
- A FAQ tem uma pergunta direta: "A aEterna é uma rede social?" com resposta "Não".
- O produto é construído sem feed, sem likes, sem seguidores.

**Sprint de origem:** Sprint 1, refinado na Sprint 5.7.

---

## 9. 2026 — O Curador faz perguntas, não escreve

**Contexto:** Ao desenvolver o Curador (chat_luto.py, assistente_ia.py), a tentação natural seria fazer o Curador "ajudar" o usuário escrevendo uma história completa a partir de poucas palavras. Mas isso transformaria o Curador em um "ghostwriter" e tiraria a voz da família.

**Decisão:** O Curador é definido como um guia que faz perguntas. Ele nunca escreve uma história completa sem o input da pessoa. Ele organiza o que a pessoa diz.

**Por que:** A história deve ser da família, não do Curador. Se o Curador escreve, a história deixa de ser da família e passa a ser dele. Isso também afeta a confiança: as pessoas precisam saber que o registro é autenticamente delas.

**Alternativas consideradas:**
- Curador escreve história completa a partir de uma frase: tira a voz da família.
- Curador gera texto fictício baseado no que a pessoa diz: inventa coisas.
- Curador faz perguntas: respeita a voz da família.

**Consequências:**
- O Curador nunca consola, nunca celebra, nunca opina.
- O tom do Curador é apenas "quem estava?", "o que aconteceu?", "como você se sentiu?".
- A história final é sempre escrita com a voz de quem viveu, não do Curador.
- A frase "História organizada com ajuda do Curador da aEterna" no modal deixa claro que o Curador ajudou, mas a história é da pessoa.

**Sprint de origem:** Sprint 1, refinado nas Sprints 3 e 5.7.

---

## 10. 2026 — A Landing não fala de tecnologia em primeiro plano

**Contexto:** A Landing original (visível em `index_old.html` e `index_old4.html`) tinha seções como "Segurança e Privacidade" e "Plataformas robustas com criptografia". Isso era linguagem de produto técnico, não de plataforma familiar.

**Decisão:** A Landing fala de **família, história e significado**. Tecnologia aparece apenas quando necessário (ex: "cofre digital", "criptografia") e sempre subordinada ao benefício familiar.

**Por que:** O visitante da Landing é uma pessoa da família, não um CTO. Falar de criptografia em primeiro plano afasta a pessoa. Falar de "lugar privado" ou "espaço protegido" é o mesmo conceito, mas em linguagem familiar.

**Alternativas consideradas:**
- Linguagem técnica detalhada: afasta o público-alvo.
- Linguagem técnica com tradução: ainda é tradução, não comunicação.
- Linguagem de benefício familiar: o que foi escolhido.

**Consequências:**
- A Landing fala de "espaço privado", "lugar seguro", "família participa junto" — não de "criptografia", "arquitetura escalável", "storage".
- A seção "Privacidade" fala de "histórias de família precisam de um espaço seguro", não de "compliance LGPD, criptografia AES-256".
- A documentação técnica do app (app.py) continua usando linguagem técnica — a Landing e a comunicação de marketing não.

**Sprint de origem:** Sprint 1, consolidado na Sprint 5.7.

---

## Como usar este documento

1. **Ao iniciar uma nova feature ou comunicação:** consultar este documento para entender quais decisões anteriores ainda são válidas e o que mudou.
2. **Ao propor uma nova decisão de marca:** adicionar uma entrada neste documento antes de implementá-la, no mesmo formato das entradas existentes.
3. **Ao revisar uma decisão existente:** se a decisão já não se aplica, marcá-la como "**Substituída por** [nova decisão]" com data e link.

---

**Este documento é a memória institucional da aEterna. Para visão e valores, ver `BRAND_BOOK_AETERNA.md`. Para como escrever, ver `GUIA_TOM_DE_VOZ.md`. Para imagem, ver `DIRECAO_FOTOGRAFICA.md`. Para histórias, ver `GUIA_EDITORIAL_HISTORIAS.md`.**
