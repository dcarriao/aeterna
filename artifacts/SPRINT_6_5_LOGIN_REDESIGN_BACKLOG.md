# SPRINT 6.5 — REDESENHO DA TELA DE LOGIN

**Status:** Backlog (não iniciada)
**Escopo:** App Web Streamlit — `components/login_compacto.py` + `app.py`
**Não alterar:** Mobile, Banco, Regras de negócio

---

## Problemas identificados (Sprint 6.4.3)

A tela de Login atual (`render_login_compacto`) apresenta os seguintes problemas:

1. **Visual abaixo do padrão premium da aEterna** — não condiz com a identidade visual escura (roxo + dourado) implementada no restante do App Web durante a Sprint 6.4

2. **Elementos desalinhados** — cards, inputs e botões não seguem um grid consistente

3. **Botão "Esqueci minha senha" estranho** — posicionamento, estilo e fluxo precisam ser revistos

4. **Textos desatualizados** — algumas strings não fazem mais sentido com o posicionamento atual do produto

5. **Hierarquia confusa** — a relação entre:
   - Login (Entrar)
   - Criar Conta
   - Acessar história compartilhada (chave compartilhada)
   
   não está clara visualmente. Os três fluxos competem pela atenção do usuário sem uma hierarquia definida.

6. **Seção "Novo por aqui?"** — precisa de revisão de layout e conteúdo

7. **Acesso por chave compartilhada** — fluxo funcional mas visualmente subestimado

## Escopo proposto

### Obrigatório
- Redesign completo do card de login com paleta roxo + dourado (seguindo `inject_custom_css()` e `styles/theme.py`)
- Alinhamento de grid para todos os elementos do formulário
- Revisão da hierarquia: Login como ação principal, Criar Conta como secundária, Chave Compartilhada como terciária/recuada
- Novo tratamento visual para "Esqueci minha senha" (link sutil, não botão)
- Revisão de todos os textos da tela
- Botão de submit com gradiente dourado (padrão do App Web)
- Estado de loading/feedback visual no submit

### Desejável
- Animação sutil de transição entre os modos (login → cadastro → visitante)
- Validação visual inline de campos (borda vermelha em campo inválido)
- Responsividade para mobile (360px–430px)

### Fora de escopo
- Alteração do fluxo de autenticação (backend)
- Alteração do banco de dados
- Alteração das regras de negócio
- Redesign do Mobile (Flutter)

## Arquivos envolvidos

- `D:\aeterna\components\login_compacto.py` — função `render_login_compacto()` e sub-funções `_render_login_principal`, `_render_cadastro`, `_render_visitante`, `_render_recuperar_senha`
- `D:\aeterna\app.py` — funções `fazer_login()`, `fazer_cadastro()`, `fazer_login_visitante()` (apenas se ajustes de callback forem necessários)
- `D:\aeterna\styles\theme.py` — classes CSS utilitárias para reuso

## Critérios de aceite

- [ ] Tela de login visualmente coerente com o restante do App Web (Sprint 6.4)
- [ ] Todos os elementos alinhados em grid consistente
- [ ] Hierarquia clara entre login, criar conta e chave compartilhada
- [ ] "Esqueci minha senha" como link sutil
- [ ] Textos revisados e atualizados
- [ ] Botão submit com gradiente dourado
- [ ] Responsivo em 360px, 390px, 430px
- [ ] Nenhuma funcionalidade de autenticação alterada
- [ ] Banco não alterado
- [ ] Mobile não alterado
- [ ] Regras de negócio não alteradas
