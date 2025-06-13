# RFPGen Pro

Este repositório contém o código inicial do projeto **RFPGen Pro**.

## Configuração Rápida

Requisitos:
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)

Para iniciar os serviços de desenvolvimento (API, worker, banco de dados e Redis), execute:

```bash
docker-compose up --build
```

O arquivo `docker-compose.yml` já define as variáveis de ambiente
`CELERY_BROKER_URL` e `CELERY_RESULT_BACKEND` apontando para o serviço
`redis`, garantindo que os workers do Celery consigam se conectar ao
Redis corretamente.

A API ficará disponível em `http://localhost:8000`.

O frontend simples pode ser acessado em `http://localhost:3000`.
Após fazer login, abra `project.html` para criar projetos, fazer upload de RFPs
e iniciar a análise via Celery.

Os principais endpoints de autenticação são:

- `POST /register` – cria um novo usuário.
- `POST /login` – retorna um token JWT.

Durante a inicialização, um usuário **admin** é criado automaticamente com:

- Usuário: `admin@example.com`
- Senha: `admin`

O endpoint raiz `/` exige um token válido no cabeçalho `Authorization` (formato `Bearer <token>`).

## Estrutura do Projeto

- `backend/` - Código Python da API e dos workers.
- `frontend/` - Código do frontend com páginas de login, registro e projetos.
- `docker-compose.yml` - Orquestração dos serviços em contêiner.
- `Dockerfile` - Imagem base para API e workers.

## Testes

Os testes podem ser executados com:

```bash
pytest
```

Para rodar os testes iniciais do frontend:

```bash
cd frontend
npm test
```
ou via Docker Compose:

```bash
docker-compose run --rm frontend npm test
```

## Pipeline CI

Os fluxos de lint e testes são executados automaticamente via GitHub Actions a cada push.
