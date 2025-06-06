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

- [ ] Configurar ferramentas de lint e formatação (Prettier, ESLint, Black).
- [ ] Garantir que o `docker-compose` sobe sem erros em ambiente de CI.
- [ ] Automatizar testes do backend no GitHub Actions.

## Sprint 3 – Próximos Passos

- [ ] Desenvolver o módulo de Projetos e upload de RFPs.
- [ ] Implementar tarefas Celery iniciais para análise de RFP usando GPT.
- [ ] Planejar as funcionalidades da Sprint seguinte de acordo com o backlog.

