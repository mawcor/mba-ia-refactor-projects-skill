# Guidelines de Arquitetura: Padrão MVC

Para a Fase 3 da refatoração, o projeto deve ser estruturado em camadas lógicas bem definidas. Se a linguagem e framework suportarem, as seguintes camadas (pastas/arquivos) devem ser criadas e respeitadas.

## Camada 1: Entry point e Configuração
*   **O que faz:** Inicializa a aplicação web, configura middlewares (CORS, body parser), registra rotas e inicializa conexões (ex: DB, dependências globais). Centraliza varíaveis sensíveis, lendo-as do ambiente (environment variables) em vez de hardcoded.
*   **Arquivos comuns:** `app.js`, `app.py`, `server.js`, `config/settings.py`, `config/db.js`.
*   **O que NÃO deve fazer:** Tratar requisições HTTP, ter lógica de negócio, executar consultas SQL.

## Camada 2: Views / Routes
*   **O que faz:** Mapeia URLs e verbos HTTP (GET, POST) para os Controllers apropriados. É o primeiro ponto de contato.
*   **Arquivos comuns:** `routes/user_routes.py`, `routes/index.js`, `views.py`.
*   **O que NÃO deve fazer:** Ter regras condicionais de negócio complexas, acessar banco de dados diretamente, validar detalhadamente (isso pode ir para Middlewares ou Validation Layers, mas idealmente não cruza a lógica de roteamento). Os handlers de rota devem ter no máximo de 5 a 10 linhas.

## Camada 3: Controllers
*   **O que faz:** Orquestra a requisição. Extrai parâmetros do request (body, query, params), chama os Models (ou Services se houver) para a lógica de negócio pesada, formata os dados resultantes (DTOs) e devolve as respostas HTTP (JSON, status codes 200, 400, 500).
*   **Arquivos comuns:** `controllers/user_controller.py`, `controllers/TaskController.js`.
*   **O que NÃO deve fazer:** Executar queries SQL brutas diretamente (usa o Model/ORM para isso). Não se aprofunda em infraestrutura pesada.

## Camada 4: Models / Data Access
*   **O que faz:** Representa as entidades do negócio, encapsula o acesso ao banco de dados (SQL, ORM) e regras de integridade do modelo. 
*   **Arquivos comuns:** `models/user_model.py`, `models/Task.js`, `repositories/...`.
*   **O que NÃO deve fazer:** Conhecer o mundo web (ex: nunca deve receber um objeto `request` HTTP ou chamar métodos de `response`).

## Estrutura de Diretórios Alvo (Exemplo):
```text
src/ (ou na raiz)
├── config/
│   ├── database.py/js
│   └── settings.py/js
├── models/
│   ├── usuario_model.py/js
│   └── produto_model.py/js
├── routes/ (ou views/)
│   └── api_routes.py/js
├── controllers/
│   ├── usuario_controller.py/js
│   └── produto_controller.py/js
├── utils/ (ou middlewares/)
│   └── error_handler.py/js
└── app.py/js (entry point)
```
