
## Plano de Desenvolvimento Detalhado: RFPGen Pro MVP

**1. Introdução e Objetivos do MVP**

O objetivo principal do RFPGen Pro MVP é entregar um sistema inteligente que otimize e agilize o fluxo de trabalho da equipe de Pré-Vendas, desde a análise de RFPs/editais até a geração de propostas técnicas. O MVP se concentrará em:

* Implementar o fluxo completo de 5 passos com assistência de IA.
* Utilizar a API da OpenAI (Modelos GPT e Assistants API) como motor de IA.
* Capacitar o Administrador do sistema a gerenciar prompts e, crucialmente, treinar e gerenciar OpenAI Assistants específicos para vendors.
* Fornecer uma interface intuitiva para os usuários de Pré-Vendas (10-15 pessoas inicialmente) e para o Administrador.
* Garantir que o sistema seja robusto, seguro e preparado para futuras evoluções (escalabilidade, novos provedores de IA, internacionalização).

**2. Pilha Tecnológica Adotada**

A seleção da pilha tecnológica visa modernidade, produtividade, escalabilidade e um ecossistema robusto para IA:

* **Frontend:**
    * **Linguagem/Framework:** React (v18+) com Next.js (para estrutura, SSR/SSG se necessário, e roteamento otimizado).
    * **Linguagem de Programação:** TypeScript.
    * **Estilização:** Tailwind CSS (com bibliotecas de componentes como shadcn/ui para acelerar o desenvolvimento de UI acessível e customizável).
    * **Gerenciamento de Estado:** Zustand (ou Jotai) para estado global do cliente, e React Query/TanStack Query para gerenciamento de estado do servidor, cache e sincronização de dados.
    * **Formulários:** React Hook Form com Zod para validação de esquemas.
    * **Requisições HTTP:** Axios (ou `Workspace` API encapsulada).
* **Backend:**
    * **Linguagem/Framework:** Python (v3.10+) com FastAPI (para APIs de alta performance e desenvolvimento rápido).
    * **ORM:** SQLAlchemy (v2.0+) com Alembic para migrações de banco de dados.
    * **Servidor ASGI:** Uvicorn, com Gunicorn para múltiplos workers em produção.
    * **Testes:** Pytest.
* **Inteligência Artificial (IA):**
    * **Provedor Principal:** OpenAI API.
        * Modelos GPT (ex: gpt-4o, gpt-3.5-turbo) para tarefas de geração de texto, análise e sugestões.
        * Assistants API para conhecimento específico de vendors e tarefas mais complexas de BoM e análise de aderência.
* **Processamento Assíncrono de Tarefas:**
    * **Fila de Mensagens:** Redis (como broker Celery e para caching).
    * **Framework de Tarefas:** Celery (para processar análise de RFPs, interações com IA demoradas, geração de documentos em background).
* **Banco de Dados:**
    * PostgreSQL (v14+) (robusto, com bom suporte a JSON e funcionalidades avançadas).
* **Armazenamento de Arquivos:**
    * MinIO (auto-hospedado, compatível com S3 API) ou um serviço de nuvem (AWS S3, Google Cloud Storage, Azure Blob Storage). Para RFPs, templates, propostas geradas e arquivos de conhecimento para OpenAI Assistants.
* **Autenticação e Autorização:**
    * JWTs (JSON Web Tokens) gerenciados pelo backend.
    * Hashing de senhas com Argon2.
    * RBAC (Role-Based Access Control) implementado na lógica da aplicação.
* **Containerização:**
    * Docker e Docker Compose (para consistência entre ambientes de desenvolvimento, teste e produção).
* **CI/CD (Integração Contínua/Entrega Contínua):**
    * GitHub Actions (ou GitLab CI/Jenkins) para automação de build, testes e deploy.
* **Logging e Monitoramento (Planejamento Essencial):**
    * Estrutura de logging centralizada (ex: ELK Stack - Elasticsearch, Logstash, Kibana; ou Grafana Loki com Promtail).
    * Monitoramento de performance da aplicação (APM) e infraestrutura (ex: Prometheus, Grafana, Sentry).

**3. Arquitetura de Alto Nível**

O sistema seguirá uma arquitetura de **Monolítico Modular com Filas de Tarefas Assíncronas**:

1.  **Frontend (Next.js App):** Interface do usuário para Pré-Vendas e Administradores. Consome a API Backend.
2.  **Backend API (FastAPI App):**
    * Endpoints RESTful para todas as funcionalidades.
    * Lógica de negócio, validação, autenticação e autorização.
    * Interage com o Banco de Dados para persistência.
    * Enfileira tarefas demoradas (IA, geração de documentos) no Message Broker.
    * Gerencia a interação com a OpenAI API (modelos GPT e Assistants API), incluindo o ciclo de vida dos Assistants (criação, upload de arquivos, etc.) conforme solicitado pelo Admin.
3.  **Banco de Dados (PostgreSQL):** Armazena dados de usuários, projetos, RFPs, análises da IA, metadados de vendors, BoMs, escopos de serviço, propostas, configurações de prompts, mapeamentos de Assistants, biblioteca de serviços, etc.
4.  **Message Broker (Redis):** Fila para tarefas assíncronas.
5.  **Celery Workers (Python):** Processos em background que consomem tarefas da fila.
    * Realizam chamadas para a OpenAI API (incluindo invocação de Assistants específicos).
    * Processam documentos, geram arquivos.
    * Atualizam o Banco de Dados com os resultados.
6.  **Storage Service (MinIO/Cloud Storage):** Armazena arquivos binários (documentos RFP, templates `.docx`, propostas geradas, arquivos de conhecimento para os OpenAI Assistants).
7.  **OpenAI Platform:** Onde os Assistants são efetivamente hospedados e executados, e os modelos GPT são acessados. O RFPGen Pro interage via API.

*Conceito do Fluxo de Gerenciamento de Assistants:*
`Admin (Frontend) -> Backend API -> [CRUD de Configuração do Assistant no BD, Upload de Arquivos de Conhecimento para Storage] -> Backend API envia comandos para OpenAI API para criar/atualizar Assistant -> OpenAI API retorna IDs/status -> Backend API armazena IDs no BD.`
*Conceito do Uso de Assistants:*
`Usuário inicia tarefa (Frontend) -> Backend API enfileira tarefa (Redis) -> Celery Worker pega tarefa -> Worker lê configuração do Assistant no BD -> Worker interage com OpenAI Assistant API usando ID e contexto -> Worker processa resposta -> Worker atualiza BD.`

**4. Equipe de Desenvolvimento (Sugestão para MVP)**

* **1 Product Owner (PO):** Responsável pela visão do produto, backlog e prioridades. (Pode ser você ou alguém designado).
* **2 Desenvolvedores Backend:** Foco em Python, FastAPI, SQLAlchemy, Celery, e integrações com OpenAI. Um com mais senioridade para liderar a arquitetura da IA.
* **1-2 Desenvolvedores Frontend:** Foco em React/Next.js, TypeScript, e design da interface.
* **1 Engenheiro de QA/Testes:** Responsável pela estratégia de testes, automação e garantia de qualidade.
* **(Parcial) 1 Designer UX/UI:** Para criar wireframes, protótipos e garantir uma boa experiência do usuário, especialmente para o fluxo principal e o painel do Admin.
* **(Parcial) 1 Engenheiro DevOps:** Para configurar e manter CI/CD, infraestrutura de containerização, logging e monitoramento.

**5. Metodologia de Desenvolvimento**

* **Scrum:** Recomenda-se a adoção do Scrum com Sprints de 2 ou 3 semanas.
    * **Cerimônias:** Sprint Planning, Daily Stand-ups, Sprint Review, Sprint Retrospective.
    * **Ferramentas de Gestão:** Jira, Trello, Asana ou similar para gerenciamento do backlog e acompanhamento das Sprints.

**6. Fases de Desenvolvimento do MVP**

As estimativas de tempo são aproximadas e podem variar conforme o tamanho final e experiência da equipe.

* **Fase 0: Configuração e Planejamento Detalhado (Sprint 0) (2-3 semanas)**
    * **Objetivos:** Preparar o terreno para o desenvolvimento, refinar o backlog inicial, alinhar a equipe.
    * **Principais Tarefas:**
        * Configuração dos repositórios Git (frontend, backend).
        * Estrutura inicial dos projetos com linters, formatters, hooks de pré-commit.
        * Pipeline básico de CI/CD (build, testes unitários iniciais).
        * Configuração do Docker e Docker Compose para ambiente de desenvolvimento.
        * Detalhamento das histórias de usuário para a Fase 1.
        * Design UX/UI inicial (wireframes/mockups para as primeiras telas).
        * Definição da arquitetura de logging e monitoramento inicial.
    * **Entregáveis:** Ambiente de desenvolvimento funcional, backlog priorizado para a Fase 1, documentação de arquitetura inicial, designs de UI/UX preliminares.
    * **Foco Tecnológico:** Ferramentas de desenvolvimento, CI/CD, Docker.

* **Fase 1: Fundação, Autenticação e Módulo Admin Inicial (4-6 semanas)**
    * **Objetivos:** Implementar a base da aplicação, autenticação segura e o esqueleto do painel administrativo.
    * **Principais Épicos/Funcionalidades:**
        * **Módulo de Usuários e Autenticação:**
            * Cadastro de usuários (nome, email, senha com Argon2).
            * Login com JWTs.
            * Middleware de proteção de rotas.
            * Fluxo de "Esqueci minha senha".
        * **Módulo Administrativo (Base):**
            * Interface para CRUD de Usuários.
            * Implementação de RBAC básico (Admin, Usuário Pré-Vendas).
            * Layout básico do painel administrativo.
        * **Estrutura Backend/Frontend:**
            * Configuração inicial de FastAPI e Next.js.
            * Modelos de dados iniciais (User, Role) e migrações com Alembic.
    * **Entregáveis:** Sistema com cadastro e login funcional, painel admin com gerenciamento de usuários, API de autenticação.
    * **Foco Tecnológico:** FastAPI, SQLAlchemy, JWT, Argon2, Next.js, React Context/Zustand.

* **Fase 2: Núcleo do Gerenciamento de RFPs e Análise Inicial de Edital (6-8 semanas)**
    * **Objetivos:** Permitir o upload de RFPs e realizar a primeira etapa de análise com IA.
    * **Principais Épicos/Funcionalidades:**
        * **Módulo de Projetos/RFPs:**
            * CRUD para "Projetos" (contêiner para RFPs e propostas).
            * Upload de arquivos RFP (PDF, DOCX, TXT, XLSX, EML) associados a um projeto (usando MinIO/Cloud Storage).
            * Listagem e visualização de projetos/RFPs.
        * **Passo 1: Análise Completa do Edital via IA:**
            * Integração com Celery e Redis para processamento assíncrono do upload e análise.
            * Worker Celery para chamar a API da OpenAI (modelos GPT) para extrair os 13 pontos chave do edital.
            * Armazenamento da análise estruturada no BD.
            * Visualização da análise no frontend (relatório web dentro do projeto).
        * **Módulo Administrativo (Extensão):**
            * Interface para gerenciar prompts base para a análise de edital.
    * **Entregáveis:** Usuário pode criar projetos, anexar RFPs, e ver a análise da IA do edital. Admin pode configurar o prompt da análise.
    * **Foco Tecnológico:** FastAPI, Celery, Redis, OpenAI GPT API, MinIO/Storage, SQLAlchemy.

* **Fase 3: Gerenciamento de OpenAI Assistants e Análise de Vendors/Criação de BoM (8-12 semanas)**
    * **Objetivos:** Implementar a funcionalidade central de gerenciamento de Assistants pelo Admin e utilizá-los para análise de vendors e sugestão de BoM.
    * **Principais Épicos/Funcionalidades:**
        * **Módulo Administrativo (Extensão Crítica):**
            * Interface para CRUD de configurações de OpenAI Assistants (nome, descrição, ID do Assistant da OpenAI).
            * Funcionalidade para o Admin fazer upload de arquivos de conhecimento (via sistema para o Storage, e depois referenciados para a OpenAI Assistants API).
            * Lógica para criar/atualizar Assistants na plataforma OpenAI via API.
            * Mecanismo para mapear "Vendors" (cadastro simples de vendors inicialmente) aos seus respectivos Assistants.
        * **Módulo de Fornecedores (Vendors):**
            * CRUD básico para Fornecedores no sistema (nome, talvez especialidade).
        * **Passo 2: Análise de Aderência de Fornecedores com IA:**
            * Worker Celery para usar o Assistant OpenAI configurado (ou modelo GPT geral como fallback) para analisar a aderência do vendor à RFP.
            * Apresentação do ranking com pontuação e justificativa.
            * Seleção do(s) vendor(es) pelo usuário.
        * **Passo 3: Criação da Bill of Materials (BoM) assistida por IA:**
            * Worker Celery para usar o Assistant do vendor selecionado para sugerir a BoM (PN, Descrição, Qtd, Obs).
            * Interface para visualização e edição textual da BoM.
            * Salvamento da BoM no BD.
    * **Entregáveis:** Admin pode configurar e treinar Assistants. Usuário pode obter análise de vendors e uma BoM sugerida pela IA.
    * **Foco Tecnológico:** OpenAI Assistants API, design de interface complexa para Admin, fluxos de trabalho assíncronos mais elaborados.

* **Fase 4: Escopo de Serviço, Geração de Proposta e Biblioteca de Serviços (6-9 semanas)**
    * **Objetivos:** Completar o fluxo principal com a geração do escopo de serviço e da proposta técnica final.
    * **Principais Épicos/Funcionalidades:**
        * **Biblioteca de Serviços Padrão:**
            * Interface para o Admin gerenciar (CRUD) uma biblioteca de cláusulas/atividades de serviço.
            * IA pode sugerir um conjunto inicial para esta biblioteca.
        * **Passo 4: Definição do Escopo de Serviço assistida por IA:**
            * Worker Celery para sugerir o escopo de serviço (usando modelos GPT e possivelmente a biblioteca de serviços), seguindo a estrutura definida.
            * Interface para edição do escopo.
        * **Módulo de Templates de Documentos (Admin):**
            * Interface para o Admin fazer upload de templates `.docx`.
            * Sistema para definir/listar os placeholders que podem ser usados nos templates.
        * **Passo 5: Geração da Proposta Técnica com IA e Exportação:**
            * Editor de texto rico (WYSIWYG ou Markdown com preview) para cada seção da proposta.
            * Worker Celery para consolidar todas as informações (análise, BoM, escopo, etc.) e gerar o texto de cada seção da proposta usando modelos GPT (mantendo contexto e coerência).
            * Funcionalidade de preenchimento do template `.docx` com os dados e textos gerados.
            * Exportação da proposta em formato `.docx` e PDF.
    * **Entregáveis:** Usuário pode gerar escopos de serviço e propostas técnicas completas, editáveis e exportáveis. Admin gerencia a biblioteca de serviços e templates.
    * **Foco Tecnológico:** Geração de DOCX (ex: python-docx), editor de texto rico no frontend, orquestração de prompts complexos para coerência.

* **Fase 5: Testes Integrados, Refinamentos, Documentação e Preparação para Lançamento (4-6 semanas)**
    * **Objetivos:** Garantir a qualidade, usabilidade e estabilidade do MVP. Preparar para o lançamento para a equipe de Pré-Vendas.
    * **Principais Tarefas:**
        * Execução de testes E2E abrangentes para os fluxos principais.
        * Testes de usabilidade com usuários da equipe de Pré-Vendas.
        * Coleta de feedback e realização de ajustes finos na UI/UX e na lógica da IA (ajuste de prompts base).
        * Otimizações de performance (queries de BD, respostas da API, chamadas de IA).
        * Revisão de segurança.
        * Criação de documentação do usuário final e do administrador.
        * Preparação do ambiente de produção e scripts de deploy.
        * Treinamento da equipe de Pré-Vendas e do Admin.
    * **Entregáveis:** MVP estável, testado e documentado, pronto para uso pela equipe de Pré-Vendas. Materiais de treinamento.
    * **Foco Tecnológico:** Ferramentas de teste E2E (Playwright/Cypress), otimização, documentação.

**7. Considerações sobre Testes**

* **Testes Unitários:** Backend (Pytest cobrindo lógica de negócios, serviços, interações com API OpenAI mockada). Frontend (Jest/React Testing Library para componentes e utilitários).
* **Testes de Integração:** Endpoints da API FastAPI, integração entre componentes frontend e serviços de backend.
* **Testes End-to-End (E2E):** Playwright ou Cypress para simular os fluxos completos do usuário (cadastro, criação de projeto, todo o processo de 5 passos da IA, geração de proposta).
* **Testes Manuais Exploratórios:** Para identificar problemas não cobertos por testes automatizados.
* **Testes de Usabilidade:** Com usuários reais para validar a experiência.
* **Ambiente de Staging/Testes:** Essencial ter um ambiente que replique a produção para testes antes do deploy.

**8. Gestão de Riscos (Principais)**

* **Dependência da OpenAI API:**
    * **Risco:** Mudanças na API, custos, latência, limites de taxa.
    * **Mitigação:** Design de uma camada de abstração para a IA (mesmo que o MVP foque em OpenAI), monitoramento de custos e performance, políticas de retry robustas, clareza nos termos de uso da OpenAI.
* **Complexidade do Gerenciamento de Assistants pelo Admin:**
    * **Risco:** Interface do Admin pode ser complexa; Admins podem ter dificuldade em treinar Assistants eficazmente.
    * **Mitigação:** Design UX/UI cuidadoso, documentação clara, treinamento, começar com funcionalidades mais simples e iterar.
* **Qualidade e Coerência das Saídas da IA:**
    * **Risco:** IA pode gerar conteúdo impreciso, incompleto ou incoerente.
    * **Mitigação:** Engenharia de prompts robusta, permitir fácil edição pelo usuário, feedback indireto para ajuste de prompts, clareza de que a IA é uma *assistente*.
* **Performance de Tarefas de IA:**
    * **Risco:** Análises e gerações podem ser demoradas, impactando a UX.
    * **Mitigação:** Uso extensivo de tarefas assíncronas (Celery), feedback claro ao usuário sobre o progresso, otimizar prompts e interações com a IA.
* **Escopo do MVP (Scope Creep):**
    * **Risco:** Adição de novas funcionalidades durante o desenvolvimento do MVP.
    * **Mitigação:** PO forte para gerenciar o backlog e proteger o escopo do MVP, foco nos objetivos definidos.
* **Curva de Aprendizado do Usuário:**
    * **Risco:** Usuários podem achar o novo fluxo de trabalho e as interações com IA complexos.
    * **Mitigação:** Interface intuitiva, tooltips, documentação, treinamento.

**9. Próximos Passos Pós-Planejamento**

1.  **Validação do Plano:** Apresentar este plano aos stakeholders (você, e qualquer outra parte interessada) para feedback e aprovação final.
2.  **Alocação de Recursos:** Montar/confirmar a equipe de desenvolvimento conforme sugerido.
3.  **Kick-off do Projeto:** Reunião inicial com toda a equipe para alinhar visão, objetivos, e iniciar a Sprint 0/Fase 0.
4.  **Desenvolvimento Iterativo:** Iniciar os ciclos de Sprint, com revisões e adaptações contínuas.

