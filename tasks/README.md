# Tarefas do Projeto RFPGen Pro

Este diretório reúne as tarefas sugeridas para iniciar o desenvolvimento do MVP do **RFPGen Pro**. Cada item abaixo pode ser desdobrado em cartões de Sprint conforme necessário.

## Sprint 0 – Configuração Inicial

- [x] Estruturar os diretórios `backend/` e `frontend/` no repositório.
- [x] Adicionar `Dockerfile` e `docker-compose.yml` para API, workers e banco de dados.
- [x] Criar um `README.md` inicial com instruções de setup e execução local.
- [x] Configurar um pipeline simples no GitHub Actions para lint e testes.

## Sprint 1 – Autenticação Básica

- [x] Implementar modelos `User` e `Role` usando FastAPI e SQLAlchemy.
- [x] Criar endpoints de registro e login com senhas armazenadas via Argon2.
- [x] Gerar e validar tokens JWT para autenticação.
- [x] No frontend, criar páginas de login e registro simples.

## Sprint 2 – CI/CD e Qualidade de Código

 - [x] Configurar ferramentas de lint e formatação (Prettier, ESLint, Black).
 - [x] Garantir que o `docker-compose` sobe sem erros em ambiente de CI.
 - [x] Automatizar testes do backend no GitHub Actions.

## Sprint 3 – Próximos Passos

- [x] Desenvolver o módulo de Projetos e upload de RFPs.
- [x] Implementar tarefas Celery iniciais para análise de RFP usando GPT.
- [x] Planejar as funcionalidades da Sprint seguinte de acordo com o backlog.

## Sprint 4 – Gerenciamento de Vendors e Assistants

Planejada de acordo com `plano-inicial.md` para iniciar o fluxo de vendors e
assistants.

- [ ] CRUD de Fornecedores (Vendors).
- [ ] CRUD de configurações de Assistants OpenAI (Admin).
- [ ] Integração com a API da OpenAI para criar/atualizar Assistants.
- [ ] Tarefa Celery para análise de aderência de vendors.
- [ ] Início da geração da BoM assistida por IA.

