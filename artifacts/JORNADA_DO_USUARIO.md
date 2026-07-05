# JORNADA DO USUÁRIO — aEterna

> Fluxograma completo da experiência do usuário, desde a descoberta até o uso contínuo. Este documento mapeia todos os pontos de contato entre o usuário e a plataforma, identificando quebras de continuidade entre site e aplicativo.

---

## Fase 1 — Descoberta

```
                      ┌─────────────────────────────┐
                      │      Usuário descobre       │
                      │      a aEterna (Google,     │
                      │      indicação, link)       │
                      └─────────────┬───────────────┘
                                    │
                                    ▼
                      ┌─────────────────────────────┐
                      │      Landing (index.html)    │
                      │                              │
                      │  • Hero: carrossel stories   │
                      │  • Problema: "fotos          │
                      │    sobrevivem, histórias     │
                      │    quase nunca"              │
                      │  • Curador: exemplo diálogo  │
                      │  • Features: ecossistema     │
                      │  • Memorial: continuação     │
                      │  • FAQ                       │
                      └─────────────┬───────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
          ┌─────────────────┐ ┌──────────┐ ┌──────────────┐
          │ Clica CTA       │ │ Clica    │ │ Clica link   │
          │ "Descobrir uma  │ │ "Ler     │ │ "Insights"   │
          │ história"       │ │ esta     │ │ (footer)     │
          └────────┬────────┘ │ história"│ └──────┬───────┘
                   │          └────┬─────┘        │
                   │               │              │
                   ▼               ▼              ▼
          ┌─────────────────┐ ┌──────────┐ ┌──────────────┐
          │ App (Streamlit) │ │ Modal    │ │ Blog         │
          │ Login/Cadastro  │ │ história │ │ (/insights/) │
          └─────────────────┘ │ completa │ └──────────────┘
                              └──────────┘
```

**Observação:** O fluxo Landing → app não tem tela de transição. O visitante "pula" do site para o app. Aceitável para SaaS, mas pode ser melhorado.

---

## Fase 2 — Primeiro Acesso

```
         ┌──────────────────────────────────────┐
         │          App (Streamlit)              │
         │          Login/Cadastro               │
         │                                       │
         │  • Email + senha                      │
         │  • Ou Google (se disponível)          │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │          Cadastro                    │
         │                                       │
         │  • Nome, sobrenome, email             │
         │  • CPF, data de nascimento            │
         │  • Senha                              │
         │  • Telefone / WhatsApp (opcional)     │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     Home (render_inicio)              │
         │                                       │
         │  • Sidebar aparece pela 1ª vez        │
         │  • Estatísticas: 0 memórias           │
         │  • "Bem-vindo à aEterna"              │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     Primeira História                 │
         │                                       │
         │  • Clica "Minha História"             │
         │  • Clica "Nova memória"               │
         │  • Adiciona foto, título, texto       │
         │  • Ou usa o Curador                   │
         └─────────────────┬────────────────────┘
```

**Quebra identificada:** O cadastro pede CPF e data de nascimento — pode ser uma barreira para novos usuários que querem apenas experimentar.

---

## Fase 3 — Primeira História (com Curador)

```
         ┌──────────────────────────────────────┐
         │     Curador de Histórias              │
         │     (render_assistente)               │
         │                                       │
         │  • Curador pergunta: "Quem estava     │
         │    com você nesse dia?"               │
         │  • Usuário responde                   │
         │  • Curador pergunta: "O que           │
         │    aconteceu?"                        │
         │  • Usuário responde                   │
         │  • Curador organiza em estrutura      │
         │  • Usuário revisa e salva             │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     História salva                   │
         │                                       │
         │  • Entra na Linha do Tempo            │
         │  • Aparece em Minha História          │
         │  • Usuário pode adicionar pessoas     │
         │    (Pessoas)                          │
         └─────────────────┬────────────────────┘
```

---

## Fase 4 — Colaboração Familiar

```
         ┌──────────────────────────────────────┐
         │     Compartilhar história             │
         │                                       │
         │  • Usuário define visibilidade        │
         │    (privado/seletivo/contatos)        │
         │  • Convidar familiares                │
         │  • Familiares recebem acesso          │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     Familiar recebe notificação       │
         │                                       │
         │  • Novidades (🔔) aparece com badge   │
         │  • Familiar vê "Sua mãe deixou        │
         │    uma lembrança..."                  │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     Familiar contribui                │
         │                                       │
         │  • Adiciona foto, vídeo, texto        │
         │  • Dono da história revisa            │
         │  • Contribuição aprovada entra        │
         │    na história                        │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     História cresce                   │
         │                                       │
         │  • Linha do Tempo atualizada          │
         │  • Novidades notifica todos           │
         └──────────────────────────────────────┘
```

---

## Fase 5 — Uso Contínuo

```
         ┌──────────────────────────────────────┐
         │     Usuário retorna ao app            │
         │                                       │
         │  • Login (email + senha)              │
         │  • Sidebar com todas as features      │
         └─────────────────┬────────────────────┘
                           │
         ┌─────────────────┼──────────────────┐
         │                 │                  │
         ▼                 ▼                  ▼
   ┌────────────┐   ┌────────────┐   ┌──────────────┐
   │ Adiciona   │   │ Responde   │   │ Cria        │
   │ mais       │   │ a          │   │ Memorial    │
   │ histórias  │   │ perguntas  │   │             │
   │            │   │ do Curador │   │             │
   └─────┬──────┘   └─────┬──────┘   └──────┬───────┘
         │                │                 │
         ▼                ▼                 ▼
   ┌────────────┐   ┌────────────┐   ┌──────────────┐
   │ Linha do   │   │ Mensagens  │   │ Família      │
   │ Tempo      │   │ para o     │   │ contribui    │
   │ cresce     │   │ Futuro     │   │ no Memorial  │
   └────────────┘   └────────────┘   └──────────────┘
```

---

## Fase 6 — Memorial (quando aplicável)

```
         ┌──────────────────────────────────────┐
         │     Alguém da família falece         │
         │                                       │
         │  • Usuário cria Memorial              │
         │  • Familiares são convidados          │
         │    (WhatsApp)                         │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     Memorial construído              │
         │                                       │
         │  • Filhos, irmãos, amigos             │
         │    contribuem com fotos, vídeos,      │
         │    histórias                          │
         │  • Explorador de Histórias            │
         │    (perguntas sobre a pessoa)         │
         │  • Memorial entra na Linha do Tempo   │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     Memorial visitado por quem        │
         │     não tem conta                     │
         │                                       │
         │  • Modo visitante (chave de acesso)   │
         │  • Vê histórias, fotos, vídeos        │
         │  • Não pode editar                    │
         └──────────────────────────────────────┘
```

---

## Fase 7 — Retorno ao Site

```
         ┌──────────────────────────────────────┐
         │     Usuário quer ler o blog           │
         │                                       │
         │  • ❌ Não há link no app              │
         │  • Usuário abre nova aba              │
         │  • Digita aeternalegado.com.br        │
         │  • Navega até /insights/              │
         └─────────────────┬────────────────────┘
                           │
                           ▼
         ┌──────────────────────────────────────┐
         │     ⚠️ QUEBRA DE CONTINUIDADE        │
         │                                       │
         │  O app não tem link para o site.      │
         │  O usuário precisa sair do fluxo      │
         │  para acessar conteúdo editorial.     │
         └──────────────────────────────────────┘
```

---

## Quebras de Continuidade (consolidadas)

| # | Fase | Quebra | Impacto | Prioridade | Solução proposta |
|---|---|---|---|---|---|
| Q1 | 1 → 2 | Landing → App sem tela de transição | Baixo | Média | Criar tela de "loading" ou transição com identidade visual |
| Q2 | 2 | Cadastro pede CPF e data de nascimento | Médio | Alta | Simplificar cadastro inicial, pedir dados extras depois |
| Q3 | 5 | App não tem link para o site | **Alto** | **Crítica** | Adicionar link "Sobre a aEterna" no sidebar |
| Q4 | 5 | App não tem link para o blog | Alto | Alta | Adicionar link "Insights" no sidebar ou footer do app |
| Q5 | 5 | App não tem link para FAQ | Médio | Alta | Adicionar link "FAQ" ou embed da FAQ no app |
| Q6 | 5 | App não tem link para política de privacidade | Médio | Alta | Adicionar link no footer do app |
| Q7 | 6 | Landing não comunica modo visitante | Baixo | Média | Adicionar seção "Para quem recebeu um convite" na Landing |
| Q8 | 7 | Blog não tem link para o app | Baixo | Baixa | Adicionar CTA "Começar minha história" no blog |

---

## Jornada ideal (após correções)

```
Descoberta (Google, indicação)
    │
    ▼
Landing (index.html)
    │
    ├──▶ Blog (/insights/)
    │       │
    │       └──▶ CTA → App
    │
    ├──▶ FAQ
    │
    └──▶ CTA → App
            │
            ▼
        Login / Cadastro simplificado
            │
            ▼
        Home (render_inicio)
            │
            ├──▶ Minha História + Curador
            ├──▶ Pessoas
            ├──▶ Linha do Tempo
            ├──▶ Compartilhar → Família contribui
            ├──▶ Memorial (quando aplicável)
            │
            └──▶ Link "Sobre a aEterna" → Landing
                    │
                    └──▶ Blog (/insights/)
                            │
                            └──▶ CTA → App (ciclo completo)
```

> **Com as correções, o usuário navega entre site e app em um ciclo contínuo, sem nunca precisar sair do ecossistema aEterna.**
