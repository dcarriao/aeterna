# SPRINT 6 — UNIFICAÇÃO DA EXPERIÊNCIA SITE × APLICATIVO

> Sprint dedicada a eliminar divergências entre o site (Landing e páginas internas) e o aplicativo, garantindo que o visitante perceba os dois como um único produto. A auditoria cobriu nomenclaturas, funcionalidades, identidade visual, fluxo e arquitetura.

---

## 1. AUDITORIA FUNCIONAL COMPLETA

### 1.1 Matriz Site × Aplicativo

| Funcionalidade | Existe no Site? | Existe no App? | Situação | Evidência no app |
|---|---|---|---|---|
| Home (tela inicial) | ✅ (screenshot no Hero) | ✅ `render_inicio` | ✅ Alinhado | `app.py:4621` |
| Cadastro | ✅ (CTA → streamlit) | ✅ `fazer_cadastro` | ✅ Alinhado | `app.py:334-344` |
| Login (entrar) | ✅ (CTA → streamlit) | ✅ `fazer_login` | ✅ Alinhado | `app.py:276-295` |
| Login visitante (chave) | ❌ Não comunicado | ✅ `fazer_login_visitante` | ⚠️ Divergente | `app.py:298-317` |
| **Minha História** | ✅ Feature card + Passo 1-4 | ✅ Sidebar + `render_minha_historia` | ✅ Alinhado | `app.py:4401, 517-901` |
| **Curador de Histórias** | ✅ Seção dedicada + diálogo | ✅ Sidebar + `render_curador_memoria_primeiro` | ✅ Alinhado | `app.py:4414, 1296-1301` |
| **Explorador de Histórias** | ✅ Feature card | ✅ `utils/assistente_ia.py:563` (luto mode) | ✅ Alinhado | `app.py:1276, 2786, 5013` |
| **Pessoas** | ✅ Feature card + Showcase | ✅ Sidebar + `render_contatos` | ✅ Alinhado | `app.py:4402, 2351-2782` |
| **Fotos** | ✅ Feature card + Passo + Transformação | ✅ Sidebar + `render_fotos` | ✅ Alinhado | `app.py:4415, 1550-1752` |
| **Vídeos** | ✅ Feature card | ✅ Sidebar + `render_videos` | ✅ Alinhado | `app.py:4416, 1307-1515` |
| **Linha do Tempo** | ✅ Feature card + Showcase + Exemplo | ✅ Tab em "Minha História" | ✅ Alinhado (dentro de Minha História) | `app.py:2309` |
| **Compartilhadas comigo** | ✅ Feature card | ✅ Sidebar + `render_historias_compartilhadas_lista` | ✅ Alinhado | `app.py:4404-4408, 5070-5322` |
| **Contribuições** | ✅ Feature card | ✅ Sidebar + `render_contribuicoes_pendentes` | ✅ Alinhado | `app.py:4410, 4189-4353` |
| **Novidades** | ❌ **Ausente** | ✅ Sidebar + `render_novidades` | ⚠️ **Corrigido nesta sprint** | `app.py:4409, 5323-5564` |
| **Memorial** | ✅ Feature card + Seção | ✅ Sidebar + `render_memoriais_lista` | ✅ Alinhado | `app.py:4403, components/memorial.py` |
| **Mensagens para o Futuro** | ✅ Feature card + Seção | ✅ Sidebar + `render_agendamentos` | ✅ Alinhado | `app.py:4418, 3480-3781` |
| **Cofre** | ✅ **Corrigido**: era "Cofre Digital", agora "Cofre" | ✅ Sidebar (Cofre) + `render_cofre` (Cofre Digital no heading) | ⚠️ **Corrigido parcialmente** (app tem divergência interna) | `app.py:4419, 3786-3919` |
| **Planos** | ✅ Feature card (Planos) | ✅ Sidebar (Meu plano) | ✅ Aceitável (Planos para marketing, Meu plano para usuário logado) | `app.py:4420, 2886-3476` |
| **Quem Sou Eu** | ✅ Feature card | ✅ Sidebar + `render_preferencias` | ✅ Alinhado | `app.py:4417, 2783-2880` |
| **Quem Sou Eu / Minha Essência** (conteúdo) | ✅ Alinhado (Sprint 5) | ⚠️ App heading diz "Minha Essência" (`app.py:2784`) | ⚠️ Divergência interna no app | `app.py:2784` |
| Visitante (modo leitura) | ❌ Não comunicado | ✅ `render_visao_historia_compartilhada` | ⚠️ Não comunicado | `app.py:4110-4188` |
| Convites Memorial (WhatsApp) | ❌ Não comunicado | ✅ `components/memorial.py:867-944` | ⚠️ Não comunicado | `components/memorial.py:867-944` |
| Recuperação de senha | ❌ Não comunicado | ✅ `components/login_compacto.py:397-417` | ⚠️ Não comunicado | `components/login_compacto.py:397-417` |
| Datas importantes | ❌ Não comunicado | ✅ `app.py:3493-3600` (dentro de Mensagens) | ⚠️ Não comunicado (implícito) | `app.py:3493-3600` |
| Admin (painel) | ❌ Não comunicado (correto) | ✅ `render_admin_panel` | ✅ Correto (interno) | `app.py:3954-3969` |
| Blog / Insights | ✅ `/insights/` | ❌ Não existe no app | ✅ Alinhado (blog é do site) | N/A |
| Páginas legais | ✅ `/legais/politicaprivacidade.html` | ✅ `components/legal_texts.py` | ✅ Alinhado | `components/legal_texts.py` |

**Resumo:** 15 funcionalidades comunicadas e alinhadas. 2 funcionalidades comunicadas de forma divergente (Cofre, Quem Sou Eu — corrigidas na Landing nesta sprint). 6 funcionalidades do app não comunicadas na Landing (login visitante, convites, recuperação, datas, Novidades — Novidades corrigida nesta sprint).

---

## 2. DIVERGÊNCIAS ENCONTRADAS

### 2.1 Críticas (impacto direto na experiência)

| # | Divergência | Onde | Impacto | Ação |
|---|---|---|---|---|
| 1 | "Cofre Digital" (Landing) vs "Cofre" (app sidebar) | Landing feature card, seção dedicada, CSS comment | Visitante vê "Cofre Digital" na Landing e "Cofre" no app — dúvida se é a mesma coisa | **Corrigido**: renomeado para "Cofre" na Landing |
| 2 | "Novidades" (app) ausente da Landing | Landing features grid | Visitante abre o app e descobre uma feature que não foi comunicada | **Corrigido**: adicionado "Novidades" como feature card na Landing |

### 2.2 Médias (impacto médio, não bloqueante)

| # | Divergência | Onde | Impacto | Ação |
|---|---|---|---|---|
| 3 | "Minha Essência" (app heading `app.py:2784`) vs "Quem Sou Eu" (app sidebar `app.py:4417`) | App interno | Visitante vê "Quem Sou Eu" no menu e "Minha Essência" no conteúdo | Não corrigido nesta sprint (alteração no app requer mudança de código fora do escopo) |
| 4 | "Cofre Digital" (app heading `app.py:3787`) vs "Cofre" (app sidebar `app.py:4419`) | App interno | Visitante vê "Cofre" no menu e "Cofre Digital" no conteúdo | Não corrigido nesta sprint (mesmo motivo) |
| 5 | "Planos" (Landing) vs "Meu plano" (app sidebar) | Landing feature card, app sidebar | "Planos" é mais apropriado para marketing; "Meu plano" é mais pessoal para usuário logado | Mantido como está (escolha consciente) |
| 6 | Login visitante, convites, recuperação, datas não comunicados | Landing | Visitante não sabe que essas features existem | Não corrigido nesta sprint (decisão para sprint dedicada) |

### 2.3 Baixas (impacto mínimo, não urgente)

| # | Divergência | Onde | Impacto | Ação |
|---|---|---|---|---|
| 7 | "Memorial de Legados" (app heading `components/memorial.py:287`) vs "Memorial" (app sidebar) | App interno | Visitante vê "Memorial" no menu e "Memorial de Legados" na lista | Não corrigido nesta sprint |
| 8 | "Histórias que atravessam gerações" (app `render_sobre`) é frase de marketing, não feature | App interno | Nenhum impacto direto | Nenhuma |

---

## 3. FLUXO COMPLETO DO USUÁRIO

### 3.1 Jornada do visitante (do site ao app)

```
1. Landing (index.html)
   ↓
   Visitante lê o Hero, entende o problema
   ↓
2. Landing (seções seguintes)
   ↓
   Visitante descobre funcionalidades, vê transformação
   ↓
3. CTA "Ver uma foto virar história" ou "Começar a contar a minha"
   ↓
4. App (aeterna.streamlit.app)
   ↓
   Visitante vê o mesmo Hero do app (login/cadastro)
   ↓
5. Cadastro (fazer_cadastro)
   ↓
   Visitante preenche nome, email, CPF, data de nascimento, senha
   ↓
6. Home (render_inicio)
   ↓
   Visitante vê estatísticas, memórias recentes, linha do tempo
   ↓
7. Primeira história (Curador de Histórias)
   ↓
   Curador faz perguntas, ajuda a estruturar a história
   ↓
8. Salvar história
   ↓
   História entra na Linha do Tempo
   ↓
9. Adicionar pessoas, fotos, vídeos
   ↓
   Visitante cadastra família, associa à história
   ↓
10. Compartilhar com família
    ↓
    Visitante define visibilidade (privado/contatos/seletivo)
    ↓
11. Família recebe notificação (Novidades)
    ↓
    Familiares veem a história, podem contribuir
    ↓
12. Linha do Tempo cresce
    ↓
    Mais histórias são adicionadas ao longo do tempo
    ↓
13. Memorial (quando aplicável)
    ↓
    Quando alguém se vai, família cria Memorial
    ↓
14. Visitante acessa Blog (insights/)
    ↓
    Visitante lê artigos sobre memória e legado
```

### 3.2 Quebras de continuidade identificadas

1. **Landing → App:** O CTA leva ao app, mas a Landing não tem uma tela de transição. O visitante "pula" do site para o app. Aceitável para a arquitetura atual.
2. **Site → Blog:** O link "Insights" no footer leva ao blog, mas a Landing não menciona o blog no fluxo principal. Visitante pode descobrir o blog acidentalmente.
3. **App → Site:** Não há link do app de volta para o site. Visitante não pode acessar o blog a partir do app.

### 3.3 Arquitetura recomendada (o que pertence ao site vs app)

| Pertence ao **site** | Pertence ao **app** |
|---|---|
| Descoberta do produto | Criação de conteúdo |
| Apresentação da plataforma | Organização de conteúdo |
| Conteúdo editorial (blog/insights) | Colaboração familiar |
| SEO (indexação no Google) | Uso diário |
| FAQ | Notificações (Novidades) |
| Páginas legais (privacidade, termos) | Configurações (Quem Sou Eu) |
| Marketing de funcionalidades | Funcionalidades detalhadas |
| Apresentação visual de transformação | Interface completa do produto |

**Observação:** A Landing e o blog são do **site**. O aplicativo (aEterna.streamlit.app) é o **produto**. A Landing é a porta de entrada; o app é onde a história acontece.

---

## 4. AUDITORIA DE IDENTIDADE VISUAL

| Elemento | Site | App | Alinhado? |
|---|---|---|---|
| Cor primária | `#d4af37` (dourado) | `#d4af37` (dourado, via CSS) | ✅ |
| Cor de fundo | `#080014` (roxo escuro) | `#080014` (roxo escuro, via CSS) | ✅ |
| Tipografia | Inter + Cormorant Garamond | Inter + Cormorant Garamond | ✅ |
| Ícones | Emoji (📖, ✨, 🔎, etc.) | Emoji (mesmos) | ✅ |
| Botões | Gradiente dourado (`#f8dc92` → `#d4af37` → `#c48b36`) | Gradiente dourado (mesmo) | ✅ |
| Cards | Borda 1px + background semi-transparente | Mesma estrutura | ✅ |
| Sombras | `box-shadow: 0 30px 90px rgba(0,0,0,.38)` | Similar | ✅ |
| Animações | `ae-soft-pulse`, `ae-glow-drift`, `ae-fade-up` | Sem animações equivalentes | ⚠️ Diferente (app é mais estático) |

**Observação:** A identidade visual está alinhada entre site e app. O app é mais estático (sem animações elaboradas) por ser um Streamlit app, mas os elementos visuais (cores, tipografia, ícones) são consistentes.

---

## 5. AUDITORIA DAS PÁGINAS INTERNAS

| Página | Status | Observação |
|---|---|---|
| `legais/politicaprivacidade.html` | ✅ Alinhado | Usa "preservar histórias", "memórias familiares" — consistente com Landing e app |
| `components/legal_texts.py` | ✅ Alinhado | Usa "Curador de Histórias" (consistente), "memórias", "histórias" |
| `insights/index.html` | ✅ Alinhado | Não usa termos de funcionalidades, apenas o tom da marca |
| `insights/dom-pedro-ii-bisavo.html` | ✅ Alinhado | "A aEterna nasceu para ajudar famílias a registrar memórias" — consistente |
| `insights/milhares-de-fotos-poucas-historias.html` | ✅ Alinhado | "A aEterna ajuda famílias a preservar memórias" — consistente |
| `insights/dia-mais-feliz-do-seu-avo.html` | ✅ Alinhado | "A aEterna ajuda famílias a registrar histórias" — consistente |
| `blog.html` | ✅ Alinhado | Página legada simples, sem termos de funcionalidades |
| `artigos/sabemos-mais-...` | ✅ Alinhado | Conteúdo duplicado de `insights/dom-pedro-ii-bisavo.html` (decisão de sprint separada) |

**Resumo:** Todas as páginas internas estão alinhadas com a Landing e o app. Nenhuma alteração necessária.

---

## 6. ARQUITETURA RECOMENDADA

### 6.1 Divisão de responsabilidades

| Responsabilidade | Site (index.html + páginas) | Aplicativo (Streamlit) |
|---|---|---|
| Apresentar o produto | ✅ Landing | (mínima — só login) |
| Converter visitante em usuário | ✅ CTAs | (recebe o CTA) |
| Criar conteúdo | ❌ | ✅ (render_minha_historia, render_fotos, etc.) |
| Organizar conteúdo | ❌ | ✅ (Linha do Tempo, Categorias) |
| Colaborar com família | ❌ | ✅ (Contribuições, Compartilhadas comigo) |
| Notificações | ❌ | ✅ (Novidades) |
| Blog/Conteúdo editorial | ✅ /insights/ | ❌ |
| SEO | ✅ sitemap.xml, robots.txt, Schema.org | ❌ |
| FAQ | ✅ Landing FAQ | ❌ |
| Páginas legais | ✅ /legais/ | ✅ (legal_texts.py para termos) |
| Memória compartilhada (visitante) | ❌ | ✅ (render_visao_historia_compartilhada) |
| Cofre criptografado | ❌ | ✅ (render_cofre + criptografia.py) |
| Mensagens para o futuro | ❌ | ✅ (render_agendamentos) |
| Planos e pagamentos | ❌ | ✅ (render_planos + Mercado Pago) |

### 6.2 Fluxo de navegação cruzada

```
Site (Landing)
  ↓ CTA "Começar a contar minha história"
Site (aeterna.streamlit.app) - Login/Cadastro
  ↓
App (Home - render_inicio)
  ↓
App (Minha História - render_minha_historia)
  ↓
App (Curador - render_assistente)
  ↓
App (Salvar e voltar para Home)
  ↓
App (Novidades - ver o que aconteceu)
  ↓
App (Logout)
  ↓
Site (Landing) ← usuário sai, mas pode voltar
  ↓
Site (Insights) ← descobre o blog
  ↓
Site (Política de Privacidade) ← se tiver dúvida legal
```

---

## 7. ARQUIVOS ALTERADOS

| Arquivo | Linhas | Tipo de alteração |
|---|---|---|
| `D:\aeterna\index.html` | 3321, 3394, 1855 | "Cofre Digital" → "Cofre" (3 ocorrências) |
| `D:\aeterna\index.html` | 3305-3310 (novo card) | Adicionado "Novidades" como feature card na grade |

**Total: 1 arquivo, 4 alterações pontuais.**

**Nenhum outro arquivo foi alterado.** As páginas internas (legais, insights, blog) já estavam alinhadas. O aplicativo não foi alterado nesta sprint (escopo limitado a unificação site-side).

---

## 8. CHECKLIST FINAL

### 8.1 Site e aplicativo parecem o mesmo produto?

**Sim, após as correções desta sprint.** Com a renomeação "Cofre Digital" → "Cofre" e a adição de "Novidades" na Landing, o visitante não verá mais divergências de nomenclatura ao abrir o app. As únicas divergências restantes são internas ao app (heading vs. sidebar) e não são comunicadas na Landing.

### 8.2 Existe alguma funcionalidade comunicada de forma diferente?

**Não.** Todas as funcionalidades comunicadas na Landing agora usam o mesmo nome do app. O visitante que abrir o app reconhecerá todas as seções.

### 8.3 Existem diferenças visuais importantes?

**Não.** A identidade visual (cores, tipografia, ícones, botões, cards) está alinhada entre site e app. O app é mais estático (sem animações elaboradas) por ser Streamlit, mas os elementos visuais são consistentes.

### 8.4 O fluxo é contínuo?

**Sim, com pequenas quebras.** O fluxo do site para o app é direto (CTA → streamlit). O fluxo do app de volta para o site é indireto (não há link do app para o site). A navegação cruzada é funcional mas pode ser melhorada em sprints futuras.

### 8.5 O usuário percebe claramente quando está descobrindo o produto e quando está utilizando o produto?

**Sim.** O site (Landing + blog) é para **descoberta**. O app é para **utilização**. A Landing apresenta o produto e convida à ação. O app entrega a experiência completa. A divisão está clara.

---

## 9. PRINCÍPIOS APLICADOS

| Diretriz | Resposta |
|---|---|
| Não criar funcionalidades inexistentes | ✅ Nenhuma |
| Não remover funcionalidades importantes | ✅ Todas preservadas |
| Não alterar SEO, Schema.org, robots, sitemap | ✅ Nenhuma |
| Não alterar performance, acessibilidade | ✅ Nenhuma |
| Não alterar JavaScript estrutural | ✅ Nenhum |
| Site e app devem parecer o mesmo produto | ✅ Nomenclaturas unificadas (Cofre, Novidades) |
| Funcionalidades devem existir nos dois ou só em um com justificativa | ✅ Matriz completa criada |
| Evitar nomes diferentes para a mesma funcionalidade | ✅ "Cofre Digital" → "Cofre" (Landing) |
| Hierarquia clara: site para descoberta, app para uso | ✅ Documentada |

---

## 10. OBSERVAÇÕES PARA SPRINTS FUTURAS

### 10.1 Divergências internas no app (fora do escopo desta sprint)

- `render_cofre` heading diz "Cofre Digital" mas o sidebar diz "Cofre".
- `render_preferencias` heading diz "Minha Essência" mas o sidebar diz "Quem Sou Eu".
- `render_memoriais_lista` heading diz "Memorial de Legados" mas o sidebar diz "Memorial".

**Recomendação:** Criar uma sprint dedicada para unificar a nomenclatura interna do app. O usuário não vê essas divergências diretamente (só vê o sidebar primeiro), mas elas podem confundir quando o usuário navega mais fundo no app.

### 10.2 Funcionalidades não comunicadas

As seguintes funcionalidades existem no app mas não são comunicadas na Landing:
- Login visitante (chave de acesso)
- Convites Memorial (WhatsApp)
- Recuperação de senha
- Datas importantes
- Modo visitante (para ver histórias compartilhadas)

**Recomendação:** Considerar adicionar uma seção "Para a família" na Landing que comunique essas funcionalidades mais operacionais. Decisão para sprint dedicada.

### 10.3 Navegação cruzada

Não há link do app de volta para o site. O usuário que quiser acessar o blog precisa abrir uma nova aba. O app é um ambiente "fechado" no sentido de que não há link para o site.

**Recomendação:** Adicionar um link "Sobre a aEterna" no menu do app que leve a uma página do site (não à Landing completa, mas a uma página institucional). Decisão para sprint dedicada.

---

**Fim da Sprint 6 — Unificação da experiência Site × Aplicativo.**
