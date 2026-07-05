# MATRIZ SITE × APLICATIVO — aEterna

> Documento oficial de referência para a Fase 6. Mapeia toda funcionalidade existente no site (Landing + páginas internas) e no aplicativo (Streamlit), indicando status de alinhamento, divergências e prioridade de correção.

---

## Legenda

| Status | Significado |
|---|---|
| ✅ Alinhado | Mesmo nome, mesmo conceito, mesma função |
| ⚠️ Divergente | Nome ou implementação diferente |
| ❌ Ausente | Não existe em um dos lados |
| 🔧 Corrigido | Foi divergente, já corrigido em sprint anterior |
| 📝 Planejado | Será corrigido em sprint futura |

---

## Matriz completa

| # | Funcionalidade | Landing (index.html) | App (app.py / componentes) | Status | Prioridade | Evidência Landing | Evidência App | Observação |
|---|---|---|---|---|---|---|---|---|
| 1 | **Home / Início** | Hero com carrossel + eyebrow "Histórias que atravessam gerações" + CTAs | `render_inicio` com estatísticas, memórias recentes | ✅ Alinhado | — | `index.html:3207-3267` | `app.py:4621` | App mostra métricas; site mostra stories. Conceito alinhado. |
| 2 | **Login** | CTA → `aeterna.streamlit.app` | `render_login_compacto` + `fazer_login` | ✅ Alinhado | — | `index.html:3217` | `app.py:276-295, 5592-5598` | Fluxo: site → CTA → login |
| 3 | **Cadastro** | Mesmo CTA (cadastro integrado ao login) | `fazer_cadastro` | ✅ Alinhado | — | `index.html:3218` | `app.py:334-344` | Fluxo direto |
| 4 | **Login visitante** | ❌ Não comunicado | `fazer_login_visitante` + chave de acesso | ❌ Ausente na Landing | **Média** | N/A | `app.py:298-317` | Funcionalidade existe no app, não é comunicada |
| 5 | **Minha História** | Feature card + Passo 1-4 + ecossistema | Sidebar 📖 + `render_minha_historia` | ✅ Alinhado | — | `index.html:3417-3498` | `app.py:4401, 517-901` | Nomenclatura consistente |
| 6 | **Curador de Histórias** | Seção dedicada + diálogo de 6 turnos + 4 pontos | Sidebar (expander) + `render_assistente` | ✅ Alinhado | — | `index.html:3500-3558` | `app.py:4414, 1296-1301` | Conceito e nome alinhados |
| 7 | **Explorador de Histórias** | Feature card + ecossistema | `utils/assistente_ia.py` (modo luto/visita) | ✅ Alinhado | — | `index.html:4100` | `assistente_ia.py` | Nome consistente |
| 8 | **Pessoas** | Feature card + Showcase + ecossistema | Sidebar 👥 + `render_contatos` | ✅ Alinhado | — | `index.html:3685-3699` | `app.py:4402, 2351-2782` | Alinhado |
| 9 | **Fotos** | Feature card + Transformação foto→história | Sidebar (expander) + `render_fotos` | ✅ Alinhado | — | `index.html:3562-3617` | `app.py:4415, 1550-1752` | Alinhado |
| 10 | **Vídeos** | Feature card + ecossistema | Sidebar (expander) + `render_videos` | ✅ Alinhado | — | `index.html:3562-3617` | `app.py:4416, 1307-1515` | Alinhado |
| 11 | **Linha do Tempo** | Feature card + Showcase + exemplo (2001-2035) | Tab em Minha História + `render_linha_tempo` | ✅ Alinhado | — | `index.html:3462-3497` | `app.py:2309` | Alinhado (dentro de Minha História) |
| 12 | **Compartilhadas comigo** | Feature card + ecossistema | Sidebar 🤝 + `render_historias_compartilhadas_lista` | ✅ Alinhado | — | `index.html:4000-4058` | `app.py:4404-4408, 5070-5322` | Nome consistente |
| 13 | **Novidades** | Feature card + ecossistema (🔧 Sprint 6) | Sidebar 🔔 + `render_novidades` | ✅ Alinhado | — | `index.html:3305-3310` | `app.py:4409, 5323-5564` | Adicionado na Sprint 6 |
| 14 | **Contribuições** | Feature card (ecossistema) | Sidebar ✨ + `render_contribuicoes_pendentes` | ✅ Alinhado | — | `index.html:4000-4058` | `app.py:4410, 4189-4353` | Alinhado |
| 15 | **Memorial** | Feature card + Seção dedicada + exemplo família | Sidebar 🤍 + `render_memoriais_lista` | ✅ Alinhado | — | `index.html:4068-4137` | `app.py:4403, `memorial.py`` | Alinhado |
| 16 | **Mensagens para o Futuro** | Feature card + Seção dedicada + exemplo (2018→2036) | Sidebar (expander) + `render_agendamentos` | ✅ Alinhado | — | `index.html:3334-3363, 4000-4058` | `app.py:4418, 3480-3781` | Alinhado |
| 17 | **Cofre** | Feature card + ecossistema + vault demo | Sidebar (expander) + `render_cofre` | ⚠️ **Divergente** | **Média** | `index.html:4000-4058, 1872-1979` | `app.py:4419, 3786-3919` | Landing diz "Cofre" (corrigido). App heading diz "Cofre Digital" (`app.py:3787`) |
| 18 | **Planos** | Feature card + FAQ "gratuito?" | Sidebar "Meu plano" + `render_planos` | ✅ Aceitável | — | `index.html:4000-4058, 4208-4212` | `app.py:4420, 2886-3476` | "Planos" (marketing) vs "Meu plano" (pessoal) — diferença intencional |
| 19 | **Quem Sou Eu** | Feature card + ecossistema | Sidebar (expander) + `render_preferencias` | ⚠️ **Divergente** | **Média** | `index.html:4000-4058` | `app.py:4417, 2783-2880` | Sidebar OK. Heading `app.py:2784` diz **"Minha Essência"** |
| 20 | **Visitante (modo leitura)** | ❌ Não comunicado | `render_visao_historia_compartilhada` | ❌ Ausente na Landing | Baixa | N/A | `app.py:4110-4188` | Funcionalidade existe no app |
| 21 | **Convites Memorial (WhatsApp)** | ❌ Não comunicado | `memorial.py:867-944` | ❌ Ausente na Landing | Baixa | N/A | `memorial.py:867-944` | Funcionalidade existe |
| 22 | **Recuperação de senha** | ❌ Não comunicado | `login_compacto.py:397-417` | ❌ Ausente na Landing | Baixa | N/A | `login_compacto.py:397-417` | Funcionalidade existe |
| 23 | **Datas importantes** | ❌ Não comunicado | `app.py:3493-3600` (dentro de Mensagens) | ❌ Ausente na Landing | Baixa | N/A | `app.py:3493-3600` | Funcionalidade existe |
| 24 | **Admin (painel)** | ❌ Não comunicado (correto) | `render_admin_panel` | ✅ Correto | — | N/A | `app.py:3954-3969` | Interno, não deve ser comunicado |
| 25 | **Blog / Insights** | ✅ `/insights/` + 3 artigos | ❌ Não existe no app | ✅ Correto | — | `index.html:4246` | N/A | Blog é exclusivo do site |
| 26 | **Páginas legais** | ✅ `/legais/politicaprivacidade.html` | ✅ `legal_texts.py` | ✅ Alinhado | — | `index.html` (footer futuro) | `legal_texts.py` | Ambos têm versões |

---

## Resumo estatístico

| Status | Quantidade | % |
|---|---|---|
| ✅ Alinhado | 19 | 73% |
| ⚠️ Divergente | 2 | 8% |
| ❌ Ausente na Landing | 4 | 15% |
| ✅ Correto (não deve estar na Landing) | 1 | 4% |
| **Total** | **26** | **100%** |

---

## Divergências pendentes de correção

### Divergências internas do app (heading vs sidebar)

| # | Funcionalidade | Sidebar diz | Heading diz | Arquivo:Linha | Prioridade |
|---|---|---|---|---|---|
| D1 | Quem Sou Eu | "Quem Sou Eu" | "Minha Essência" | `app.py:2784` | **Média** |
| D2 | Cofre | "Cofre" | "Cofre Digital" | `app.py:3787` | **Média** |
| D3 | Memorial | "Memorial" | "Memorial de Legados" | `memorial.py:287` | **Média** |

### Funcionalidades não comunicadas na Landing

| # | Funcionalidade | Existe em | Prioridade |
|---|---|---|---|
| F1 | Login visitante | `app.py:298-317` | Média |
| F2 | Convites Memorial (WhatsApp) | `memorial.py:867-944` | Baixa |
| F3 | Recuperação de senha | `login_compacto.py:397-417` | Baixa |
| F4 | Datas importantes | `app.py:3493-3600` | Baixa |
| F5 | Modo visitante | `app.py:4110-4188` | Baixa |

---

## Histórico de correções

| Sprint | Correção |
|---|---|
| Sprint 6 | "Cofre Digital" → "Cofre" na Landing (3 ocorrências) |
| Sprint 6 | Adicionado card "Novidades" na grade de features |
| Sprint 6.0 | Auditoria completa documentada |
| Sprint 6.1 (planejado) | Unificação visual do app |
| Sprint 6.2 (planejado) | Navegação cruzada |
| Sprint 6.3 (planejado) | Correção de nomenclatura interna |
