# Auditoria Funcional — aEterna Mobile App

**Data:** 04/07/2026
**Versão do app:** `1.0.0+19`
**SDK:** Flutter `^3.12.2`
**Plataforma:** Android (APK/AAB)
**Repositório:** `origin/master`

---

## 1. Resumo Executivo

O aEterna Mobile é um aplicativo Flutter de registro de memórias pessoais com integração ao Supabase (banco de dados + storage). O app possui **22 telas**, **17 models**, **16 services**, **7 widgets reutilizáveis** e **4 assets** de logo. Não utiliza gerenciamento de estado (BLoC/Riverpod/Provider) — toda a navegação e estado são gerenciados via callbacks em um `StatefulWidget` central no `main.dart`.

### Pontos fortes
- Ampla cobertura funcional: memórias, pessoas, memoriais, linha do tempo, compartilhamento familiar, curador com IA, contribuições colaborativas.
- Arquitetura consistente: services seguem padrão singleton, models com `fromMap`/`toMap` consistentes com colunas do Supabase.
- Integração com OpenAI (Chat Completions + Visão) para Curador Contextual.
- Trabalhos em background (Workmanager) para notificações proativas.
- Identidade visual definida (cores, tema claro, design system consistente).

### Pontos críticos
- **Cadastro de conta não implementado** — o botão mostra "Criação de conta em breve."
- **Autenticação customizada (SHA-256 direto na tabela `usuarios`)**, sem uso do Supabase Auth — arquitetura insegura.
- **Todas as varáveis de ambiente via `String.fromEnvironment()`** — requerem `--dart-define` no build; não há `.env` fallback.
- **Chave de API OpenAI hardcoded como env var** — exposta no binário compilado.
- **2 widgets não utilizados** (`MediaSuggestionsCard`, `PendingMemoryCard`) — código morto.
- **Idioma/Tema escuro no Perfil desabilitados** — placeholders visíveis mas não funcionais.
- **Caches locais sem invalidação** — `_memoriasContextoCache` in-memory nunca expira.
- **Tratamento de erros frágil** — `catch (_) { return null; }` em vários pontos do `PessoaRepository` (login, etc.)

---

## 2. Estrutura do Projeto

### 2.1 Diretórios

```
lib/
├── curador/                        # Motor de perguntas (fallback offline)
│   └── perguntas.dart
├── models/                         # 17 arquivos de modelo de dados
├── screens/                        # 22 telas
├── services/                       # 16 services
├── theme/                          # Tema e cores
│   └── app_theme.dart
├── widgets/                        # Widgets reutilizáveis
│   ├── memory_card.dart
│   └── home/
│       ├── curador_continuar_card.dart
│       ├── detected_moment_card.dart
│       ├── media_suggestions_card.dart     ← NÃO USADO
│       ├── memoria_do_dia_card.dart
│       ├── memoria_pode_crescer_card.dart
│       └── pending_memory_card.dart        ← NÃO USADO
└── main.dart                       # Entry point + orquestrador central
```

### 2.2 Arquivos por diretório

| Diretório | Arquivos |
|---|---|
| `lib/` | `main.dart` |
| `lib/curador/` | `perguntas.dart` |
| `lib/models/` | `memoria.dart`, `pessoa.dart`, `contribuicao.dart`, `convite_familiar.dart`, `curador_resposta_ia.dart`, `curador_sessao.dart`, `detected_moment.dart`, `media_group.dart`, `media_suggestion.dart`, `memoria_do_dia.dart`, `memoria_pode_crescer.dart`, `memoria_relacionamento.dart`, `memorial.dart`, `pending_memory.dart`, `pessoa_linha_tempo.dart`, `pessoa_relacionamento.dart`, `tipo_relacionamento.dart` |
| `lib/screens/` | 22 telas (listadas na seção 8) |
| `lib/services/` | 16 services (listados na seção 7) |
| `lib/theme/` | `app_theme.dart` |
| `lib/widgets/` | `memory_card.dart` |
| `lib/widgets/home/` | 6 widgets home |
| `assets/` | 4 PNGs de logo |

### 2.3 Dependências principais (pubspec.yaml)

| Package | Versão | Função |
|---|---|---|
| `supabase` | `^2.13.0` | Backend-as-a-Service (DB, Storage) |
| `image_picker` | `^1.2.2` | Câmera/galeria |
| `photo_manager` | `^3.0.0` | Acesso à galeria (AssetEntity) |
| `shared_preferences` | `^2.5.5` | Sessão, cache local, scores |
| `intl` | `^0.20.2` | Formatação de data |
| `http` | `^1.4.0` | Chamadas HTTP (OpenAI API) |
| `local_auth` | `^2.2.0` | Biometria (login) |
| `crypto` | `^3.0.3` | SHA-256 (autenticação) |
| `workmanager` | `^0.9.0` | Tarefas background (galeria, curador) |
| `flutter_local_notifications` | `^17.2.1` | Notificações push locais |
| `app_links` | `^3.4.5` | Deep links (aeterna://share) |
| `share_plus` | `^10.1.4` | Compartilhamento nativo |
| `cupertino_icons` | `^1.0.8` | Ícones iOS |

### 2.4 Assets

| Asset | Tamanho |
|---|---|
| `assets/logo.png` | 269 KB |
| `assets/logo-aeterna-gold.png` | 697 KB |
| `assets/logo-navbar.png` | 511 KB |
| `assets/logo-sidebar.png` | 2,27 MB |

---

## 3. Mapa de Navegação

### 3.1 Estrutura de navegação

O `main.dart` usa `MaterialApp` com `navigatorKey` global. **Não há rotas nomeadas** — toda navegação usa `Navigator.of(context).push(MaterialPageRoute(...))`.

### 3.2 Árvore de navegação

```
MaterialApp (navigatorKey global, theme: AppTheme.light)
├── OnboardingScreen (se _mostrarOnboarding)
│   └── "Começar" → setState(_mostrarOnboarding = false) → Login ou Home
├── LoginScreen (se !_entrou)
│   ├── Autenticação → setState(_entrou = true) → Home
│   └── "Criar conta" → SnackBar "Criação de conta em breve."
│   └── "Esqueci senha" → Dialog de recuperação
└── HomeScreen (hub central, bottom nav)
    ├── Bottom Nav 1: "Minha História" → MinhaHistoriaScreen
    ├── Bottom Nav 2: "Timeline" → TimelineScreen
    ├── Bottom Nav 3: "Pessoas" → PessoasScreen
    ├── Bottom Nav 4: "Compartilhadas" → CompartilhadasScreen
    ├── Bottom Nav 5: "Memoriais" → MemoriaisScreen
    ├── AppBar (canto superior direito) → PerfilScreen
    ├── Card "Curador" → CuradorScreen (diversos modos)
    ├── Card "Conexões descobertas" → ConexoesDescobertasScreen
    ├── Card "Mapa da Vida" → MapaVidaScreen
    ├── FAB / botão "Nova memória" → NovaMemoriaScreen
    └── MemoryCard → MemoriaDetalheScreen
```

### 3.3 Fluxo de navegação completo

| De | Para | Ação |
|---|---|---|
| `main.dart` | `OnboardingScreen` | `home` do `MaterialApp` (condicional) |
| `main.dart` | `LoginScreen` | `home` do `MaterialApp` (condicional) |
| `main.dart` | `HomeScreen` | `home` do `MaterialApp` (condicional) |
| `OnboardingScreen` | `HomeScreen` | Callback `onComecar` → `setState` |
| `LoginScreen` | `HomeScreen` | Callback `onEntrar` → `setState` |
| `HomeScreen` | `NovaMemoriaScreen` | `Navigator.push` |
| `HomeScreen` | `MemoriaDetalheScreen` | `Navigator.push` |
| `HomeScreen` | `TimelineScreen` | `Navigator.push` |
| `HomeScreen` | `CompartilhadasScreen` | `Navigator.push` |
| `HomeScreen` | `MemoriaisScreen` | `Navigator.push` |
| `HomeScreen` | `PessoasScreen` | `Navigator.push` |
| `HomeScreen` | `PerfilScreen` | `Navigator.push` |
| `HomeScreen` | `MinhaHistoriaScreen` | `Navigator.push` |
| `HomeScreen` | `CuradorScreen` | `Navigator.push` (vários modos) |
| `HomeScreen` | `ConexoesDescobertasScreen` | `Navigator.push` |
| `HomeScreen` | `MapaVidaScreen` | `Navigator.push` |
| `NovaMemoriaScreen` | `CuradorScreen` | `Navigator.push` (parâmetros opcionais) |
| `MemoriaDetalheScreen` | `NovaMemoriaScreen` | `Navigator.push` (edição) |
| `MemoriaDetalheScreen` | `MemoriaContribuicaoScreen` | `Navigator.push` |
| `MemoriaDetalheScreen` | `CuradorScreen` | `Navigator.push` (complemento) |
| `PessoasScreen` | `NovaPessoaScreen` | `Navigator.push` |
| `PessoasScreen` | `PessoaDetalheScreen` | `Navigator.push` |
| `PessoasScreen` | `ConvitesScreen` | `Navigator.push` |
| `PessoasScreen` | `GrafoFamiliaScreen` | `Navigator.push` |
| `PessoaDetalheScreen` | `AdicionarRelacionamentoScreen` | `Navigator.push` |
| `PessoaDetalheScreen` | `NovoMemorialScreen` | `Navigator.push` |
| `PessoaDetalheScreen` | `NovaPessoaScreen` | `Navigator.push` (edição) |
| `PessoaDetalheScreen` | `MemorialDetalheScreen` | `Navigator.push` |
| `MemoriaisScreen` | `NovoMemorialScreen` | `Navigator.push` |
| `MemoriaisScreen` | `MemorialDetalheScreen` | `Navigator.push` |
| `Deep link (aeterna://share)` | `NovaMemoriaScreen` | `_navigatorKey.currentState.push` |
| `MethodChannel (share)` | `NovaMemoriaScreen` | `_navigatorKey.currentState.push` |

### 3.4 Telas órfãs

**Nenhuma.** Todas as 22 telas estão conectadas ao fluxo principal.

---

## 4. Matriz de Funcionalidades

| Funcionalidade | Status | Arquivos | Evidência | Observações |
|---|---|---|---|---|
| **Login** | Implementado | `login_screen.dart:68-167`, `pessoa.dart:156-183` | Autenticação via SHA-256 + salt na tabela `usuarios` | Autenticação customizada, NÃO Supabase Auth |
| **Cadastro** | **Ausente** | `login_screen.dart:460` | `Text('Criação de conta em breve.')` | Botão existe mas mostra SnackBar — funcionalidade não implementada |
| **Home** | Implementado | `home_screen.dart` (1213 linhas) | Hub central com 7+ seções carregadas em paralelo | Chamadas a 7 services diferentes |
| **Minha História** | Implementado | `minha_historia_screen.dart` (209 linhas) | Lista de memórias com pull-to-refresh, FAB, modo local | Acessada via bottom nav |
| **Nova Memória** | Implementado | `nova_memoria_screen.dart` (1378 linhas) | Formulário completo: foto, vídeo, título, data, categoria, pessoas, compartilhamento, Curador | Upload de foto/vídeo para Supabase Storage |
| **Curador de Histórias** | Implementado | `curador_screen.dart` (1221 linhas), `perguntas.dart` (312 linhas), `legacy_curator_service.dart` | Chat com IA (OpenAI) com fallback local (`MotorPerguntas`), sessão persistente, modos: proativo, complemento, retomada | 3 modos de entrada + persistência de sessão |
| **Explorador de Histórias** | Ausente | — | Não encontrado no código | Não há tela ou funcionalidade de "descobrir" histórias públicas |
| **Pessoas** | Implementado | `pessoas_screen.dart` (489 linhas), `nova_pessoa_screen.dart` (548 linhas) | Lista de contatos com sugestões automáticas, cadastro com relação | Integra com grafo familiar (Sprint L) |
| **Fotos** | Implementado | `nova_memoria_screen.dart`, `memoria_detalhe_screen.dart`, `curator_invitation_service.dart` | Upload, exibição, detecção automática na galeria | Galeria via `photo_manager`, upload via Supabase Storage |
| **Vídeos** | Implementado | `nova_memoria_screen.dart`, `memoria_detalhe_screen.dart` | Upload e exibição de vídeos | Upload via Supabase Storage, sem player dedicado |
| **Linha do Tempo** | Implementado | `timeline_screen.dart` (656 linhas), `pessoa_linha_tempo.dart` (models) | Timeline cronológica com filtro por pessoa, stats, agrupamento por ano | Acessada via bottom nav |
| **Compartilhadas comigo** | Implementado | `compartilhadas_screen.dart` (407 linhas) | 2 abas: "Você compartilhou" + "Compartilharam com você" | Filtro por familiar |
| **Compartilhamento familiar** | Implementado | `convites_screen.dart`, `convite_familiar.dart`, `pessoa.dart:936-1013` | Convites por e-mail, vínculos bilaterais, permissões por conteúdo | Ciclo completo: enviar → pendente → aceitar/recusar |
| **Contribuições** | Implementado | `memoria_contribuicao_screen.dart` (486 linhas), `supabase_service.dart`, `contribuicao.dart` | Terc. contribuem com texto/foto/vídeo; status pendente/aprovado/rejeitado | Áudio: "Gravação de áudio em breve" (placeholder) |
| **Memorial** | Implementado | `memorial_detalhe_screen.dart` (1640 linhas), `memoriais_screen.dart`, `novo_memorial_screen.dart` | Homenagem a falecidos: biografia, lembranças, moderação, curador IA | Tela mais complexa do app (1640 linhas, 4 abas) |
| **Mensagens para o Futuro** | Ausente | — | Não encontrado no código | Funcionalidade não existe no mobile |
| **Cofre Digital** | Ausente | — | Não encontrado no código | Funcionalidade não existe no mobile |
| **Quem Sou Eu** | Ausente | — | Não encontrado no código | Funcionalidade não existe no mobile |
| **Planos** | Parcial | `perfil_screen.dart:233-467` | Seção "Plano" com `_PlanoScreen` e `_PlanoCard` | Dados fictícios: "Família Premium" com limites hardcoded (15 contatos, 100 histórias). Sem integração com pagamento |
| **Perfil** | Implementado | `perfil_screen.dart` (791 linhas) | Foto, dados pessoais editáveis, plano, segurança, preferências, sobre | Preferências de idioma e tema desabilitadas |
| **Configurações** | Parcial | `perfil_screen.dart:583-679` | Seção "Preferências" no Perfil | Idiomas e Tema visual: `enabled: false` — não funcionais |
| **Notificações** | Implementado | `curator_invitation_service.dart`, `memory_growth_invitation_service.dart` | 2 canais: `curator_invitations` e `memory_growth`, Workmanager 12h | Apenas notificações proativas do Curador; sem tela de configuração |
| **Convites** | Implementado | `convites_screen.dart` (348 linhas), `pessoa.dart:936-1013` | Abas "Recebidos" e "Enviados", ciclo completo | Acessado via PessoasScreen |
| **Visitante** | Ausente | — | Não encontrado no código | Não há modo visitante |
| **Busca** | Ausente | — | Não encontrado no código | Não há funcionalidade de busca |
| **Upload de imagem** | Implementado | `pessoa.dart:472-501`, `supabase_service.dart`, `nova_memoria_screen.dart` | Para bucket `fotos` no Supabase Storage | Via `SupabaseService` ou `PessoaRepository` (2 caminhos diferentes) |
| **Upload de vídeo** | Implementado | `pessoa.dart:493-510`, `supabase_service.dart`, `nova_memoria_screen.dart` | Para bucket `fotos` no Supabase Storage | Mesmo bucket, extensão .mp4/.mov |
| **Persistência local** | Implementado | `shared_preferences` em 7 services | Sessão (`is_logged_in`), cache de scores, decisões do curador, assets usados | 7 services usam SharedPreferences |
| **Persistência Supabase** | Implementado | `supabase_service.dart`, `pessoa.dart` (PessoaRepository) | Todas as operações CRUD | 2 classes concorrentes (`SupabaseService` e `PessoaRepository`) |
| **Offline/cache** | Parcial | `shared_preferences` nos services | Apenas cache de sessão e scores; sem cache de dados do Supabase | Se Supabase estiver offline, app mostra erro ou estado vazio |
| **Tratamento de erros** | Parcial | Vários `catch (_) { return null; }` | Erros são silenciados em login, carregamento de dados | Sem feedback visual para o usuário na maioria dos casos |

---

## 5. Integração Supabase

### 5.1 Inicialização

O Supabase é inicializado em **dois pontos diferentes**:

1. **`SupabaseService`** (`lib/services/supabase_service.dart:11-22`):
```dart
static Future<void> initialize() async {
  _url = String.fromEnvironment('SUPABASE_URL');
  _anonKey = String.fromEnvironment('SUPABASE_ANON_KEY');
  _instance._client = SupabaseClient(_url, _anonKey);
}
```

2. **`PessoaRepository`** (`lib/models/pessoa.dart:83-88`):
```dart
static const _url = String.fromEnvironment('SUPABASE_URL');
static const _anonKey = String.fromEnvironment('SUPABASE_ANON_KEY');
```

**Problema**: Duas classes gerenciam conexões ao Supabase de forma independente. `SupabaseService` tem seu próprio `SupabaseClient`, e `PessoaRepository` tem seu próprio getter `_supabase` que cria um `SupabaseClient` diferente a cada acesso.

### 5.2 Tabelas utilizadas

| Tabela | Operações | Service |
|---|---|---|
| `usuarios` | SELECT (login), UPDATE (perfil) | `PessoaRepository` |
| `contatos` | SELECT, INSERT, UPDATE, DELETE | `PessoaRepository` |
| `memorias` | SELECT (todas as listagens), INSERT, UPDATE (visibilidade, data_evento) | `SupabaseService`, `PessoaRepository` |
| `memoria_fotos` | SELECT (fotos de uma memória), INSERT | `SupabaseService` |
| `fotos` | SELECT, INSERT, DELETE | `SupabaseService`, `PessoaRepository` |
| `videos_memoria` | SELECT, INSERT, DELETE | `PessoaRepository` |
| `memoria_pessoas` | SELECT, INSERT, DELETE | `PessoaRepository` |
| `memoriais` | SELECT, INSERT, UPDATE, DELETE | `SupabaseService` |
| `contribuicoes` | SELECT, INSERT, UPDATE (moderação) | `SupabaseService` |
| `conteudo_colaboradores` | SELECT, INSERT, DELETE (permissões) | `PessoaRepository` |
| `convites_familiares` | SELECT, INSERT, UPDATE | `PessoaRepository` |
| `vinculos_familiares` | SELECT | `PessoaRepository` |
| `pessoas_relacionamentos` | SELECT, INSERT, UPDATE, DELETE | `PessoaRelacionamentoService` |
| `tipos_relacionamento` | SELECT | `PessoaRelacionamentoService` |
| `curador_sessoes` | INSERT, UPDATE | `CuradorSessaoService` |
| `memoria_relacionamentos` | SELECT, INSERT, UPDATE | `MemoryRelationshipService` |
| `curador_mensagens` | INSERT (via RPC) | `CuradorSessaoService` |

### 5.3 Views e RPCs do Supabase

| Nome | Tipo | Usado por |
|---|---|---|
| `curador_sessao_ativa_por_usuario` | View | `CuradorSessaoService` |
| `grafo_pessoas_relacionamentos` | View | `PessoaRelacionamentoService` |
| `memorias_que_podem_crescer(usuario, limite)` | RPC | `MemoryGrowthInvitationService` |
| `buscar_candidatas_relacionamento(p_memoria_id, p_limite)` | RPC | `MemoryRelationshipService` |
| `pessoa_linha_tempo(p_pessoa_id)` | RPC | `PessoaTimelineService` |
| `pessoa_estatisticas(p_pessoa_id)` | RPC | `PessoaTimelineService` |
| `pessoas_recentes(usuario, limite)` | RPC | `PessoaTimelineService` |
| `pessoas_sugeridas(usuario, limite)` | RPC | `PessoaTimelineService` |
| `memorial_da_pessoa(p_pessoa_id)` | RPC | `PessoaTimelineService` |
| `listar_relacionamentos_pessoa(p_pessoa_id)` | RPC | `PessoaRelacionamentoService` |
| `listar_pessoas_com_mesma_relacao(...)` | RPC | `PessoaRelacionamentoService` |
| `memorias_do_dia(p_usuario_id, p_limite)` | RPC | `MemoriasDoDiaService` |
| `curador_listar_mensagens(p_sessao_id)` | RPC | `CuradorSessaoService` |
| `curador_salvar_mensagem(...)` | RPC | `CuradorSessaoService` |
| `curador_finalizar_sessao(...)` | RPC | `CuradorSessaoService` |
| `curador_cancelar_sessao(...)` | RPC | `CuradorSessaoService` |

### 5.4 Storage

- **Bucket:** `fotos`
- **Conteúdo:** Fotos de memória, vídeos, áudio (contribuições), fotos de perfil
- **Acesso:** Via `SupabaseService` (métodos `uploadImagem`, `deletarImagem`) e `PessoaRepository` (métodos `uploadFotoMemoria`, `uploadVideoMemoria`, `uploadFotoPerfil`)
- **Problema:** 2 caminhos de upload concorrentes com lógicas diferentes

### 5.5 Autenticação

O app **NÃO** usa Supabase Auth. Em vez disso:
- Senha + salt armazenados na tabela `usuarios`
- Hash SHA-256 calculado no client e comparado com o hash no banco
- Sessão persiste via `SharedPreferences` (`is_logged_in`, `session_user_email`)
- `usuarioId` é compartilhado via variável estática `PessoaRepository.usuarioId` e `SupabaseService.usuarioId`

**Risco de segurança:** A senha trafega em texto puro na consulta (enviada como parâmetro `eq`), e o hash é calculado no client.

---

## 6. Models

| # | Model | Arquivo | Campos principais | Métodos | Funcionalidade |
|---|---|---|---|---|---|
| 1 | `Memoria` | `lib/models/memoria.dart` | `id`, `titulo`, `contexto`, `categoria`, `criadaEm`, `foto`, `fotoUrl`, `pessoasIds`, `isCompartilhada`, `familiaresIds`, `dataMemoria`, `video`, `videoUrl`, `donoUsuarioId`, `compartilhadaPorNome` | `fromMap`, `isRecebidaDeOutraConta` | Modelo central de memória |
| 2 | `MemoriaRascunho` | `lib/models/memoria.dart` | `titulo`, `contexto`, `categoria`, `foto`, `nomeArquivo`, `pessoasIds`, `isCompartilhada`, `familiaresIds`, `dataMemoria`, `video`, `nomeVideo` | — | Rascunho antes de salvar |
| 3 | `Pessoa` | `lib/models/pessoa.dart` | `id`, `nome`, `apelido`, `parentesco`, `dataNascimento`, `fotoBase64`, `email`, `telefone`, `createdAt` | `toMap`, `fromMap`, `fotoBytes`, `fotoUrl` | Contato/pessoa |
| 4 | `PessoaRepository` | `lib/models/pessoa.dart` | (estático) `usuarioId`, `usuarioEmail` | 30+ métodos estáticos | Repositório Supabase (ver seção 7) |
| 5 | `Contribuicao` | `lib/models/contribuicao.dart` | `id`, `memorialId`, `tipoConteudo`, `conteudoId`, `usuarioDonoId`, `usuarioContribuidorEmail`, `usuarioContribuidorNome`, `tipoContribuicao`, `texto`, `arquivoUrl`, `audioUrl`, `fotoBytes`, `videoBytes`, `audioBytes`, `status`, `createdAt`, `avaliadoEm`, `avaliadoPor` | `fromMap`, `toMap`, `aprovado`, `pendente`, `rejeitado` | Contribuição de terceiros |
| 6 | `ConviteFamiliar` | `lib/models/convite_familiar.dart` | `id`, `usuarioOrigemId`, `contatoId`, `emailDestino`, `usuarioDestinoId`, `status`, `token`, `papelSugerido`, `tipoConteudoAlvo`, `conteudoIdAlvo`, `criadoEm`, `aceitoEm`, `nomeOrigem` | `fromMap`, `pendente`, `aceito`, `recusado` | Convite bilateral |
| 7 | `PapelColaborador` (enum) | `lib/models/convite_familiar.dart` | `editor`, `colaborador`, `leitor` | `fromValor`, `rotulo`, `descricao` | Papéis de permissão |
| 8 | `VinculoFamiliar` | `lib/models/convite_familiar.dart` | `usuarioId`, `nome`, `fotoUrl`, `email` | — | Vínculo entre contas |
| 9 | `Colaborador` | `lib/models/convite_familiar.dart` | `usuarioId`, `nome`, `papel` | — | Colaborador de conteúdo |
| 10 | `CuradorMensagemDTO` | `lib/models/curador_resposta_ia.dart` | `role`, `conteudo`, `tipo` | — | DTO para OpenAI |
| 11 | `CuradorRespostaIA` | `lib/models/curador_resposta_ia.dart` | `pergunta`, `deveEncerrar` | — | Resposta da IA |
| 12 | `CuradorMensagemRole` (enum) | `lib/models/curador_sessao.dart` | `user`, `assistant`, `system` | `fromValor` | Papel na mensagem |
| 13 | `CuradorMensagemTipo` (enum) | `lib/models/curador_sessao.dart` | `inicial`, `pergunta`, `resposta`, `finalizacao`, `fechamento` | — | Tipo da mensagem |
| 14 | `CuradorMensagem` | `lib/models/curador_sessao.dart` | `id`, `sessaoId`, `role`, `conteudo`, `ordem`, `tipo`, `criadoEm` | `fromMap`, `toMap` | Mensagem do Curador |
| 15 | `CuradorSessao` | `lib/models/curador_sessao.dart` | `id`, `usuarioId`, `titulo`, `contextoInicial`, `contextoAtual`, `status`, `etapa`, `totalTurnos`, `memoriaId`, `dataEvento`, `pessoas`, `criadoEm`, `atualizadoEm` | `fromMap`, `emAndamento`, `concluida`, `resumoParaCard` | Sessão do Curador |
| 16 | `DetectedMoment` | `lib/models/detected_moment.dart` | `id`, `inicio`, `fim`, `fotos`, `videos`, `capa`, `utilizado` | — | Momento detectado |
| 17 | `MediaGroup` | `lib/models/media_group.dart` | `dataLabel`, `data`, `midias` | `totalFotos`, `totalVideos` | Grupo de mídias |
| 18 | `MediaSuggestion` | `lib/models/media_suggestion.dart` | `id`, `tipo`, `data`, `asset`, `thumbnailPath`, `utilizada` | — | Mídia sugerida |
| 19 | `MemoriaDoDia` | `lib/models/memoria_do_dia.dart` | `id`, `titulo`, `fotoPrincipal`, `totalPessoas`, `totalContribuicoes`, `totalMidias`, `possuiRelacionamentos`, `anosDecorridos`, `dataReferencia` | `fromMap`, `rotuloTempo` | Memória do dia (Sprint M) |
| 20 | `MemoriaPodeCrescer` | `lib/models/memoria_pode_crescer.dart` | `memoriaId`, `titulo`, `categoria`, `dataEvento`, `ultimaAtualizacaoEm`, `diasDesdeUltimaAtualizacao`, `totalPessoas`, `totalContribuicoes`, `totalContribuicoesPendentes`, `totalFotos`, `totalVideos`, `temColaboradores`, `totalColaboradores`, `contribuidoresUnicos` | `fromMap` | Memória com potencial (Sprint I) |
| 21 | `RelacionamentoStatus` (enum) | `lib/models/memoria_relacionamento.dart` | `pendente`, `confirmado`, `ignorado` | `fromValor` | Status de relação |
| 22 | `MemoriaRelacionamento` | `lib/models/memoria_relacionamento.dart` | `id`, `usuarioId`, `memoriaOrigemId`, `memoriaDestinoId`, `score`, `motivos`, `status`, `criadoEm`, `atualizadoEm`, `tituloOrigem`, `tituloDestino` | `fromMap` | Relação entre memórias (Sprint K) |
| 23 | `RelacionamentoMotivos` | `lib/models/memoria_relacionamento.dart` | 9 campos boolean/int para motivos | `fromMap`, `toMap`, `legendasHumanas` | Motivos do relacionamento |
| 24 | `MemoriaCandidata` | `lib/models/memoria_relacionamento.dart` | `id`, `titulo`, `categoria`, `dataEvento`, `criadaEm`, `pessoasEmComum`, `diasDiferencaEvento`, `mesmoTitulo` | `fromMap` | Candidata a relação |
| 25 | `Memorial` | `lib/models/memorial.dart` | `id`, `nome`, `parentesco`, `dataNascimento`, `dataFalecimento`, `biografia`, `fotoUrl`, `fotoBytes`, `contatoId`, `usuarioId`, `createdAt` | `fromMap`, `toMap` | Memorial de falecido |
| 26 | `PendingMemory` | `lib/models/pending_memory.dart` | `id`, `data`, `fotos`, `videos`, `capa`, `quantidadeFotos`, `quantidadeVideos`, `utilizada`, `criadaEm` | — | Memória pendente da galeria |
| 27 | `PessoaTimelineTipo` (enum) | `lib/models/pessoa_linha_tempo.dart` | `memoria`, `foto`, `contribuicao`, `video` | `rotulo` | Tipo de evento |
| 28 | `PessoaTimelineEvento` | `lib/models/pessoa_linha_tempo.dart` | `tipo`, `conteudoId`, `titulo`, `data`, `memoriaOrigemId`, `contribuicaoId`, `autorContribuicao`, `fotoUrl`, `videoUrl` | `fromMap` | Evento de timeline |
| 29 | `PessoaEstatisticas` | `lib/models/pessoa_linha_tempo.dart` | `totalMemorias`, `totalFotos`, `totalVideos`, `totalContribuicoes`, `primeiraData`, `ultimaData` | `fromMap`, `totalEventos` | Estatísticas |
| 30 | `PessoaVivaResumo` | `lib/models/pessoa_linha_tempo.dart` | `id`, `nome`, `parentesco`, `email`, `fotoUrl`, `ultimaInteracao`, `totalEventos` | `fromMap`, `nomeCompleto`, `ultimaInteracaoHumana` | Resumo para Home |
| 31 | `PessoaSugerida` | `lib/models/pessoa_linha_tempo.dart` | `nome`, `ocorrencias` | `fromMap` | Sugestão de pessoa |
| 32 | `MemorialResumo` | `lib/models/pessoa_linha_tempo.dart` | `id`, `nome` | `fromMap` | Resumo de memorial |
| 33 | `RelacionamentoPessoaStatus` (enum) | `lib/models/pessoa_relacionamento.dart` | `ativo`, `pendente`, `inativo` | — | Status de relação pessoa |
| 34 | `PessoaRelacionamento` | `lib/models/pessoa_relacionamento.dart` | `id`, `usuarioId`, `pessoaAId`, `pessoaBId`, `tipo`, `relacaoA`, `relacaoB`, `confirmado`, `observacoes`, `dataInicio`, `dataFim`, `criadoEm`, `atualizadoEm`, `nomeA`, `nomeB` | `fromMap`, `outraPessoaId`, `rotuloPara`, `rotuloDe` | Relação pessoa-pessoa (Sprint L) |
| 35 | `OutraPessoaNaFamilia` | `lib/models/pessoa_relacionamento.dart` | 10 campos de relação | `fromMap` | Pessoa no grafo |
| 36 | `TipoRelacionamento` | `lib/models/tipo_relacionamento.dart` | `id`, `rotuloA`, `rotuloB`, `categoria`, `ativo` | `fromMap`, `simetrico` | Tipo de relação (Sprint L) |
| 37 | `GeneroRelacao` (enum) | `lib/models/tipo_relacionamento.dart` | `masculino`, `feminino`, `neutro` | `rotuloFlexivel` | Gênero |
| 38 | `TIPOS_RELACIONAMENTO_INICIAIS` | `lib/models/tipo_relacionamento.dart` | 24 tipos pré-definidos | — | Fallback client-side |

---

## 7. Services

| # | Service | Arquivo | Padrão | Responsabilidade | Dependências | Supabase | API Externa |
|---|---|---|---|---|---|---|---|
| 1 | `SupabaseService` | `lib/services/supabase_service.dart` | Singleton | CRUD central de memórias, memoriais, contribuições, upload Storage | Models `Memoria`, `Memorial`, `Contribuicao` | `memorias`, `memoria_fotos`, `fotos`, `memoriais`, `contribuicoes`, `conteudo_colaboradores` | — |
| 2 | `PessoaRepository` | `lib/models/pessoa.dart` | Classe estática | CRUD de contatos, autenticação, convites, vínculos, permissões | Models `Pessoa`, `ConviteFamiliar`, `PapelColaborador`, `VinculoFamiliar`, `Colaborador` | `usuarios`, `contatos`, `memorias`, `fotos`, `videos_memoria`, `memoria_pessoas`, `convites_familiares`, `vinculos_familiares`, `conteudo_colaboradores` | — |
| 3 | `LegacyCuratorService` | `lib/services/legacy_curator_service.dart` | Singleton | Integração OpenAI para curador (perguntas, análise, narrativa, visão) | Models `AnaliseLegado`, `CuradorRespostaIA`, `CuradorMensagemDTO`, `Perguntas` | — | OpenAI Chat Completions (`gpt-4o-mini`) |
| 4 | `CuradorSessaoService` | `lib/services/curador_sessao_service.dart` | Singleton | Sessão persistente do Curador Contextual | Models `CuradorSessao`, `CuradorMensagem`, `PessoaRepository` | `curador_sessoes`, `curador_sessao_ativa_por_usuario`, RPCs `curador_*` | — |
| 5 | `CuratorInvitationService` | `lib/services/curator_invitation_service.dart` | Singleton | Orquestrador de convites do curador (galeria, notificações) | `MomentDetectionService`, `CuratorInvitationScoringService`, `CuratorDecisionLogService`, `WorkmanagerFanOut` | — | `photo_manager`, Workmanager, FlutterLocalNotifications |
| 6 | `CuratorInvitationScoringService` | `lib/services/curator_invitation_scoring_service.dart` | Singleton | Score de momentos detectados para convite | `CuratorDecisionLogService`, `DetectedMoment` | — | SharedPreferences |
| 7 | `CuratorDecisionLogService` | `lib/services/curator_decision_log_service.dart` | Singleton | Log local de auditoria das decisões do curador | `DetectedMoment` | — | SharedPreferences |
| 8 | `MemoryGrowthInvitationService` | `lib/services/memory_growth_invitation_service.dart` | Singleton | Convites para memórias que podem crescer | `MemoryGrowthScoringService`, `WorkmanagerFanOut`, `PessoaRepository` | RPC `memorias_que_podem_crescer` | Workmanager, FlutterLocalNotifications |
| 9 | `MemoryGrowthScoringService` | `lib/services/memory_growth_scoring_service.dart` | Singleton | Score de memórias que podem crescer | `MemoriaPodeCrescer`, `PessoaRepository` | — | SharedPreferences |
| 10 | `MemoryRelationshipService` | `lib/services/memory_relationship_service.dart` | Singleton | Relacionamentos entre memórias (Sprint K) | `SupabaseService`, `Memoria`, `MemoriaRelacionamento`, `MemoriaCandidata`, `PessoaRepository` | RPC `buscar_candidatas_relacionamento`, tabela `memoria_relacionamentos` | — |
| 11 | `MomentDetectionService` | `lib/services/moment_detection_service.dart` | Singleton | Detecta momentos na galeria (agrupamento 90min) | `MediaSuggestionService`, `DetectedMoment` | — | `photo_manager`, SharedPreferences |
| 12 | `MediaSuggestionService` | `lib/services/media_suggestion_service.dart` | Singleton | Sugere mídias da galeria não utilizadas | `MediaGroup`, `MediaSuggestion` | — | `photo_manager`, SharedPreferences |
| 13 | `PendingMemoryService` | `lib/services/pending_memory_service.dart` | Singleton | (Legado) Memórias pendentes da galeria | `MediaSuggestionService`, `PendingMemory` | — | `photo_manager` |
| 14 | `PessoaTimelineService` | `lib/services/pessoa_timeline_service.dart` | Singleton | Linha do tempo e estatísticas de pessoa | `PessoaTimelineEvento`, `PessoaEstatisticas`, `PessoaVivaResumo`, `PessoaSugerida`, `MemorialResumo`, `PessoaRepository` | RPCs `pessoa_linha_tempo`, `pessoa_estatisticas`, `pessoas_recentes`, `pessoas_sugeridas`, `memorial_da_pessoa` | — |
| 15 | `PessoaRelacionamentoService` | `lib/services/pessoa_relacionamento_service.dart` | Singleton | Grafo de relacionamentos pessoa-pessoa | `PessoaRelacionamento`, `TipoRelacionamento`, `PessoaRepository` | `pessoas_relacionamentos`, `tipos_relacionamento`, view `grafo_pessoas_relacionamentos`, RPCs | — |
| 16 | `MemoriasDoDiaService` | `lib/services/memorias_do_dia_service.dart` | Singleton | Memórias que aconteceram no mesmo dia/mês (Sprint M) | `MemoriaDoDia`, `PessoaRepository` | RPC `memorias_do_dia` | — |
| 17 | `WorkmanagerFanOut` | `lib/services/workmanager_fanout.dart` | Classe estática | Ponte global para contornar limitação do Workmanager | — | — | — |

---

## 8. Telas

| # | Tela | Arquivo | Rota/Navegação | Funcionalidade | Estado | Tamanho |
|---|---|---|---|---|---|---|
| 1 | `LoginScreen` | `lib/screens/login_screen.dart` | `home` do MaterialApp (condicional) | Autenticação com e-mail/senha, biometria, "Criar conta" (placeholder) | Stateful | 480 |
| 2 | `OnboardingScreen` | `lib/screens/onboarding_screen.dart` | `home` do MaterialApp (condicional) | 3 páginas de introdução (PageView), marca como visto | Stateful | 168 |
| 3 | `HomeScreen` | `lib/screens/home_screen.dart` | `home` do MaterialApp (condicional) | Hub central com 7+ seções, bottom nav, cards Curador | Stateful | 1213 |
| 4 | `MinhaHistoriaScreen` | `lib/screens/minha_historia_screen.dart` | Push da Home | Lista de memórias com pull-to-refresh | Stateful | 209 |
| 5 | `NovaMemoriaScreen` | `lib/screens/nova_memoria_screen.dart` | Push da Home/Detalhe/DeepLink | Formulário completo de criação/edição de memória | Stateful | 1378 |
| 6 | `CuradorScreen` | `lib/screens/curador_screen.dart` | Push da Home/NovaMemoria/Detalhe | Chat com IA Curador (vários modos de entrada) | Stateful | 1221 |
| 7 | `MemoriaDetalheScreen` | `lib/screens/memoria_detalhe_screen.dart` | Push da Home/Timeline/Compartilhadas | Detalhes completos, contribuições, relações, Curador IA | Stateful | 1534 |
| 8 | `TimelineScreen` | `lib/screens/timeline_screen.dart` | Push da Home (bottom nav) | Linha do tempo cronológica com filtro por pessoa | Stateful | 656 |
| 9 | `CompartilhadasScreen` | `lib/screens/compartilhadas_screen.dart` | Push da Home (bottom nav) | 2 abas: compartilhadas por você e com você | Stateful | 407 |
| 10 | `MemoriaisScreen` | `lib/screens/memoriais_screen.dart` | Push da Home (bottom nav) | Lista de memoriais próprios e colaborativos | Stateful | 302 |
| 11 | `MemorialDetalheScreen` | `lib/screens/memorial_detalhe_screen.dart` | Push de MemoriaisScreen | 4 abas: biografia, lembranças, moderação, curador IA | Stateful | 1640 |
| 12 | `PessoasScreen` | `lib/screens/pessoas_screen.dart` | Push da Home (bottom nav) | Lista de pessoas + sugestões, ações: família, convites | Stateful | 489 |
| 13 | `PessoaDetalheScreen` | `lib/screens/pessoa_detalhe_screen.dart` | Push de PessoasScreen/Home | Detalhes, estatísticas, família, timeline da pessoa | Stateful | 1069 |
| 14 | `NovaPessoaScreen` | `lib/screens/nova_pessoa_screen.dart` | Push de PessoasScreen/Detalhe | Cadastro/edição de pessoa com foto e relação | Stateful | 548 |
| 15 | `PerfilScreen` | `lib/screens/perfil_screen.dart` | Push da Home (AppBar) | Perfil, plano (fictício), segurança, preferências, sobre | Stateful | 791 |
| 16 | `ConvitesScreen` | `lib/screens/convites_screen.dart` | Push de PessoasScreen | 2 abas: convites recebidos e enviados | Stateful | 348 |
| 17 | `ConexoesDescobertasScreen` | `lib/screens/conexoes_descobertas_screen.dart` | Push da Home | Relações de memória pendentes (Sprint K) | Stateful | 276 |
| 18 | `MapaVidaScreen` | `lib/screens/mapa_vida_screen.dart` | Push da Home/Conexões | Visão cronológica com relações destacadas (Sprint K) | Stateful | 261 |
| 19 | `GrafoFamiliaScreen` | `lib/screens/grafo_familia_screen.dart` | Push de PessoasScreen | Árvore familiar (Sprint L) | Stateful | 412 |
| 20 | `AdicionarRelacionamentoScreen` | `lib/screens/adicionar_relacionamento_screen.dart` | Push de PessoaDetalhe | Seleciona tipo de relação e outra pessoa (Sprint L) | Stateful | 335 |
| 21 | `MemoriaContribuicaoScreen` | `lib/screens/memoria_contribuicao_screen.dart` | Push de MemoriaDetalhe | Envio de contribuição (texto/foto/vídeo/áudio placeholder) | Stateful | 486 |
| 22 | `NovoMemorialScreen` | `lib/screens/novo_memorial_screen.dart` | Push de MemoriaisScreen/Detalhe | Criação de memorial com vínculo a pessoa | Stateful | 502 |

---

## 9. Widgets Reutilizáveis

| # | Widget | Arquivo | Usado em | Responsabilidade | Tipo |
|---|---|---|---|---|---|
| 1 | `MemoryCard` | `lib/widgets/memory_card.dart` | `HomeScreen`, `MinhaHistoriaScreen` | Card genérico de memória com foto, título, data, categoria | Stateless |
| 2 | `CuradorContinuarCard` | `lib/widgets/home/curador_continuar_card.dart` | `HomeScreen` | Card "Continuar conversa" para sessão ativa do Curador | Stateless |
| 3 | `DetectedMomentCard` | `lib/widgets/home/detected_moment_card.dart` | `HomeScreen` | Card "Vale a pena guardar este momento?" | Stateless |
| 4 | `MediaSuggestionsCard` | `lib/widgets/home/media_suggestions_card.dart` | **NENHUMA** | Card de sugestões de mídia da galeria | Stateless (não usado) |
| 5 | `MemoriaDoDiaCard` | `lib/widgets/home/memoria_do_dia_card.dart` | `HomeScreen` | Card "Memória do Dia" (Sprint M) | Stateless |
| 6 | `MemoriaPodeCrescerCard` | `lib/widgets/home/memoria_pode_crescer_card.dart` | `HomeScreen` | Card "Memória que pode crescer" (Sprint I) | Stateless |
| 7 | `PendingMemoryCard` | `lib/widgets/home/pending_memory_card.dart` | **NENHUMA** | Card de memórias pendentes (similar ao `DetectedMomentCard`) | Stateless (não usado) |
| 8 | `PessoaPickerSheet` | `lib/screens/nova_memoria_screen.dart` | `NovaMemoriaScreen`, `MemorialDetalheScreen` | Modal bottom sheet para selecionar pessoas | Stateful (inline) |

---

## 10. Identidade Visual

### 10.1 Cores

| Token | Código | Cor | Uso |
|---|---|---|---|
| `roxo` | `#2B1747` | Roxo escuro | Primária, AppBar foreground, FilledButton |
| `dourado` | `#D4A84F` | Dourado | Secundária, destaques |
| `fundo` | `#F7F3EA` | Bege claro | Scaffold background |
| `surface` | `#FFFFFF` | Branco | Cards, inputs |
| `textoSuave` | `#736B78` | Cinza arroxeado | Textos secundários |
| `borda` | `#E5DED2` | Bege escuro | Bordas de input |
| `verdeApoio` | `#527568` | Verde musgo | Apoio visual |

### 10.2 Tipografia

- **Não há `TextTheme` definido** no `AppTheme`. Apenas:
  - AppBar: 22px, w800, roxo
  - FilledButton: 16px, w700
- O app usa os tamanhos/estilos padrão do Material Design 3.

### 10.3 Componentes

| Componente | Tema definido? | Detalhes |
|---|---|---|
| `FilledButton` | Sim | `Size.fromHeight(54)`, `borderRadius: 12`, texto 16px w700 |
| `InputDecoration` | Sim | `filled: true`, fundo branco, borda `#E5DED2` / foco roxo 2px |
| `AppBar` | Sim | Fundo `#F7F3EA`, foreground roxo, `elevation: 0`, `surfaceTintColor: transparent` |
| `Card` | **Não** | Usa `Card` do Material sem customização no tema |
| `BottomNavigationBar` | **Não** | Usa padrão do Material |

### 10.4 Assets

4 variações da logo: `logo.png`, `logo-aeterna-gold.png`, `logo-navbar.png`, `logo-sidebar.png` (esta com 2,27 MB — maior que as demais).

### 10.5 Coerência

- Fundo bege claro (`#F7F3EA`) consistente em todas as telas.
- Cards brancos com cantos `borderRadius: 12` (padrão em `FilledButton`, mas não em `Card`).
- Paleta de cores consistente (roxo + dourado + bege).
- **Problema:** `CardTheme` não definido — cada tela pode usar bordas/roundings diferentes.
- **Problema:** Sem tema escuro.

---

## 11. Lacunas do Mobile

### 11.1 Críticas

| # | Lacuna | Descrição | Prioridade |
|---|---|---|---|
| 1 | **Cadastro de conta** | O app não permite criar conta. Botão exibe "Criação de conta em breve." | **Crítico** |
| 2 | **Autenticação insegura** | SHA-256 no client + senha trafega no `eq()` do Supabase. Sem Supabase Auth. | **Crítico** |
| 3 | **Chaves de API expostas** | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `OPENAI_API_KEY` compiladas no binário via `--dart-define`. Qualquer APK pode ser decompilado para extraí-las. | **Crítico** |
| 4 | **Sem Explorador de Histórias** | Não há funcionalidade de descobrir histórias públicas ou de terceiros (curadoria editorial). | **Alto** |
| 5 | **Sem Mensagens para o Futuro** | Funcionalidade de deixar mensagens programadas para o futuro não existe. | **Alto** |
| 6 | **Sem Cofre Digital** | Armazenamento seguro de documentos não existe. | **Alto** |
| 7 | **Sem Busca** | Não há busca textual ou por categoria/filtro no app. | **Alto** |
| 8 | **Sem Modo Visitante** | Não há experiência sem login. | **Alto** |

### 11.2 Altas

| # | Lacuna | Descrição | Prioridade |
|---|---|---|---|
| 9 | **Planos fictícios** | Seção de plano no Perfil mostra dados hardcoded sem integração com pagamento real. | **Alto** |
| 10 | **Preferências desabilitadas** | "Idioma" e "Tema visual" no Perfil estão com `enabled: false`. | **Alto** |
| 11 | **Áudio em contribuições** | Placeholder "Gravação de áudio em breve." | **Alto** |
| 12 | **Sem tema escuro** | Apenas tema claro definido. | **Médio** |
| 13 | **Code-duplicação Supabase** | `SupabaseService` e `PessoaRepository` são duas camadas concorrentes para acesso ao Supabase, com lógicas de CRUD sobrepostas. | **Alto** |

### 11.3 Médias

| # | Lacuna | Descrição | Prioridade |
|---|---|---|---|
| 14 | **Cache in-memory sem expiração** | `_memoriasContextoCache` no `MemoryRelationshipService` nunca expira. | **Médio** |
| 15 | **Erros silenciados** | `catch (_) { return null; }` esconde falhas do usuário. | **Médio** |
| 16 | **Print statements** | Vários `print()` de debug espalhados pelo código. | **Médio** |
| 17 | **Sem gerenciamento de estado** | Estado concentrado em `StatefulWidget` no `main.dart` — sem Provider/BLoC/Riverpod. | **Médio** |
| 18 | **Deep link apenas para share** | Único deep link: `aeterna://share?image=...`. Sem links para outras telas. | **Médio** |

### 11.4 Baixas

| # | Lacuna | Descrição | Prioridade |
|---|---|---|---|
| 19 | **Widgets não utilizados** | `MediaSuggestionsCard` e `PendingMemoryCard` existem mas não são instanciados. | **Baixo** |
| 20 | **Logo sidebar grande (2,27 MB)** | `logo-sidebar.png` é desproporcionalmente grande. | **Baixo** |
| 21 | **Comentários com encoding quebrado** | Vários comentários em português com acentos corrompidos (ex: "Ã© o curador"). | **Baixo** |
| 22 | **CardTheme não definido** | Cards sem padding/border-radius padronizados no tema global. | **Baixo** |

---

## 12. Riscos

### 12.1 Funcionalidades anunciadas mas incompletas

| Funcionalidade | Onde aparece | Problema |
|---|---|---|
| **Criar conta** | `LoginScreen` botão "Criar conta" | SnackBar "Criação de conta em breve." — funcionalidade não existe |
| **Planos / Premium** | `PerfilScreen` seção "Plano" | Dados fictícios sem integração com backend de pagamento |
| **Gravação de áudio** | `MemoriaContribuicaoScreen` | Placeholder "Gravação de áudio em breve." |
| **Preferências (Idioma/Tema)** | `PerfilScreen` | Componentes desabilitados (`enabled: false`) |
| **Convite por e-mail** | `NovaPessoaScreen` | Texto do convite contém placeholder "[cole aqui o link de instalação]" |

### 12.2 Fluxos quebrados

| Fluxo | Problema |
|---|---|
| **Login sem Supabase** | Se `SUPABASE_ANON_KEY` não estiver configurada, o login falha silenciosamente (retorna `null`) |
| **Usuário offline** | Nenhum cache dos dados do Supabase — telas ficam vazias |
| **Sessão perdida** | Se `SharedPreferences` for limpo, o app não mostra login (só se `is_logged_in` estiver ausente) |
| **Back press no Curador** | `CuradorScreen` cancela a sessão ao sair (confirmação apenas no botão X) |

### 12.3 Inconsistência de nomes

| Arquivo | Problema |
|---|---|
| `curador_` vs `curator_` | Nomes de arquivos/serviços misturam prefixos: `curador_sessao_service.dart` (pt) e `curator_decision_log_service.dart` (en) |
| `SupabaseService` vs `PessoaRepository` | Duas classes competem pela mesma responsabilidade (acesso ao Supabase) |
| `listarCompartilhamentos` / `salvarCompartilhamento` → delega para `listarVinculos` / `salvarVinculo` | Métodos duplicados semanticamente |

### 12.4 Dependências frágeis

| Dependência | Risco |
|---|---|
| `String.fromEnvironment()` para todas as chaves | Se o build não passar `--dart-define`, o app opera em "modo offline" sem aviso claro |
| `http` package (não `dio`) para OpenAI API | Sem interceptors, retry, ou timeouts configurados |
| `flutter_local_notifications` v17.2.4 vs v22 | Versão muito antiga; breaking changes na migração |
| `workmanager` v0.9.0 | Plugin pode não ser compatível com versões futuras do Flutter |
| `supabase` v2.13.0 vs v2.13.4 | Versão ligeiramente desatualizada |

### 12.5 Código antigo/duplicado

| Local | Problema |
|---|---|
| `PendingMemoryService` | Serviço legado que apenas delega para `MediaSuggestionService` e converte para `PendingMemory`. Modelo `PendingMemory` é quase idêntico a `DetectedMoment`. |
| `MediaSuggestionsCard` e `PendingMemoryCard` | Widgets substituídos por `DetectedMomentCard` mas não removidos (2 arquivos, ~400 linhas de código morto) |
| `legacy_curator_service.dart` vs `curador_sessao_service.dart` | Curador legado (estático, sem sessão) coexistindo com novo Curador Contextual (com sessão) — o legado ainda é usado como fallback |

### 12.6 Arquivos não utilizados

| Arquivo | Linhas | Risco |
|---|---|---|
| `lib/widgets/home/media_suggestions_card.dart` | 197 | Código morto |
| `lib/widgets/home/pending_memory_card.dart` | 214 | Código morto |

---

## 13. Recomendações para Paridade Web × Mobile

### 13.1 Implementar imediatamente (crítico)

1. **Cadastro de conta** — Substituir o placeholder por fluxo completo de registro.
2. **Supabase Auth** — Migrar de SHA-256 customizado para Supabase Auth (magic link + provedores OAuth).
3. **Proteção de chaves** — Usar Supabase Row Level Security (RLS) em vez de confiar em `anonKey` + `dart-define`. Remover `OPENAI_API_KEY` do client; criar Edge Function para proxy da OpenAI.
4. **Explorador de Histórias** — Implementar feed público/curado de histórias.

### 13.2 Implementar em médio prazo (alto)

5. **Mensagens para o Futuro** — Agendamento de mensagens para data futura.
6. **Cofre Digital** — Upload de documentos importantes (certidões, testamentos, etc.).
7. **Busca** — Busca textual em memórias, pessoas, memoriais com filtros.
8. **Modo Visitante** — Experiência limitada sem login.
9. **Unificar `SupabaseService` e `PessoaRepository`** — Uma única camada de acesso a dados.
10. **Gerenciamento de estado** — Adotar Riverpod ou BLoC para evitar estado monolítico no `main.dart`.

### 13.3 Melhorias de qualidade (médio)

11. **Plano real** — Integrar com backend de assinatura (Stripe/App Store).
12. **Remover código morto** — Excluir `MediaSuggestionsCard`, `PendingMemoryCard`.
13. **Tratamento de erros** — Substituir `catch (_) { return null; }` por feedback visual ao usuário.
14. **Cache offline** — Implementar cache local dos dados do Supabase (SQLite/Hive).
15. **Padronizar nomenclatura** — Decidir entre `curador_` e `curator_` e renomear todos os arquivos.
16. **Configurar CI/CD** — Validação com `flutter analyze` + testes + build.

### 13.4 Ajustes finos (baixo)

17. **CardTheme global** — Definir `borderRadius`, `elevation`, `padding` no tema.
18. **Comentários** — Corrigir encoding quebrado ou remover comentários em português.
19. **Otimizar assets** — Reduzir tamanho de `logo-sidebar.png` (2,27 MB).
20. **Remover `print` statements** — Substituir por logger adequado.

---

*Relatório gerado automaticamente em 04/07/2026. Nenhum código foi alterado durante a auditoria.*
