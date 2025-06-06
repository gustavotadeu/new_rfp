# RFPGen Pro

Este repositório contém o código inicial do projeto **RFPGen Pro**.

## Configuração Rápida

Requisitos:
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)

Para iniciar os serviços de desenvolvimento (API, worker, banco de dados e Redis), execute:

```bash
docker-compose up --build
```

A API ficará disponível em `http://localhost:8000`.

## Estrutura do Projeto

- `backend/` - Código Python da API e dos workers.
- `frontend/` - Código do frontend (a ser desenvolvido).
- `docker-compose.yml` - Orquestração dos serviços em contêiner.
- `Dockerfile` - Imagem base para API e workers.

## Testes

Os testes podem ser executados com:

```bash
pytest
```

## Pipeline CI

Os fluxos de lint e testes são executados automaticamente via GitHub Actions a cada push.
