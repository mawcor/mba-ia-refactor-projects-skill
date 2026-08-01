# Catálogo de Anti-Patterns e Code Smells

Este catálogo detalha 10 anti-patterns arquiteturais, classificados por severidade, que a skill deve buscar identificar durante a Fase 2 (Auditoria).

## CRITICAL

### 1. God Class / God File / God Method
*   **Descrição:** Arquivo, classe ou método único contendo responsabilidades demais (banco de dados, lógica de negócio, formatação, validação e roteamento).
*   **Sinal de Detecção:** Arquivos muito grandes (ex: `app.py` com mais de 100 linhas e queries SQL, ou `models.py` contendo lógica de rotas).
*   **Impacto:** Impossível de testar isoladamente, mudanças quebram partes não relacionadas.

### 2. Hardcoded Credentials / Secrets
*   **Descrição:** Chaves secretas, senhas de banco ou tokens de API diretamente no código-fonte.
*   **Sinal de Detecção:** Variáveis como `SECRET_KEY = "xxx..."`, `db_password = "123"` ou `config.paymentGatewayKey` definidas inline.
*   **Impacto:** Falha grave de segurança, vazamento de credenciais.

### 3. Arbitrary SQL Execution / SQL Injection Vulnerability
*   **Descrição:** Aceitar strings brutas do cliente e executar como queries no banco de dados, ou concatenar strings na query.
*   **Sinal de Detecção:** Montagem de SQL como:  `"SELECT * FROM users WHERE name = '{name}'"`.
*   **Impacto:** Falha de segurança que permite roubo ou exclusão total de dados.

## HIGH

### 4. Lógica de Negócio em Views/Rotas (Fat Controllers/Routes)
*   **Descrição:** Rotas (endpoints) ou Views fazendo manipulação complexa de dados, cálculos financeiros ou de datas, e manipulando a resposta final, em vez de delegar.
*   **Sinal de Detecção:** Callbacks de rotas (`app.get(...)`, `@app.route(...)`) com mais de 20-30 linhas, contendo ifs complexos, laços, cálculos ou lógicas condicionais profundas.
*   **Impacto:** Dificulta a reutilização de código e viola o SRP (Single Responsibility Principle).

### 5. Queries N+1 (N+1 Problem) / Callback Hell no DB
*   **Descrição:** Executar uma query de consulta para um objeto pai e, dentro de um laço (`for` ou `.forEach`), executar outra query para os objetos filhos.
*   **Sinal de Detecção:** Loop iterando sobre um array e chamando consultas SQL ou do ORM dentro dele (ex: `courses.forEach(c => db.all("SELECT ... WHERE course_id = c.id", (err, enrollments) => { ... db.get(user_id) ... }))`).
*   **Impacto:** Queda drástica de performance conforme o banco cresce.

### 6. Uso de APIs Obsoletas (Deprecated APIs)
*   **Descrição:** Bibliotecas ou funções defasadas ou consideradas má prática na stack atual.
*   **Sinal de Detecção:** Importação de pacotes antigos ou métodos desencorajados (ex: Em Express, usar `res.send()` para enviar objetos, preferir `res.json()`. Em Python ORMs obsoletos, ou conexões sincrônicas bloqueantes para alta concorrência). *A skill deve focar em identificar sintaxes ultrapassadas como callbacks de aninhamento infinito (callback hell) em JS ao invés de `async/await` com Promises.*
*   **Impacto:** Dificuldade de atualização futura e problemas de performance/manutenção.

## MEDIUM

### 7. Ausência de Tratamento Centralizado de Erros (Error Handling)
*   **Descrição:** Capturar exceções espalhadas por toda aplicação repetindo a mesma lógica de retorno de erro, ou omitir o tratamento.
*   **Sinal de Detecção:** Múltiplos `try/except` ou `if (err) return res.status(500).send(...)` retornando respostas HTTP genéricas, sem usar um Middleware ou Error Handler global.
*   **Impacto:** Inconsistência nas respostas de erro para o cliente.

### 8. Lógica de Acesso a Dados Espalhada (No Repository/Model pattern)
*   **Descrição:** Queries SQL cruas (`sqlite3.Database` ou `db.cursor()`) feitas diretamente em rotas ou controllers que não são classes de modelo.
*   **Sinal de Detecção:** Expressões como `cursor.execute()` fora de arquivos dedicados a Models/Repositórios.
*   **Impacto:** Dificulta a substituição do banco de dados ou mocking em testes unitários.

## LOW

### 9. Retornos de API Inconsistentes / Magic Numbers
*   **Descrição:** Retornar respostas textuais ("Sucesso") junto com objetos complexos em diferentes endpoints, ou usar números mágicos.
*   **Sinal de Detecção:** Mistura de `jsonify({"mensagem": "ok"})` e retorno de dicionários diretos `return {"status": "ok"}` no mesmo app. Uso de literais para IDs ou Status em vez de constantes.
*   **Impacto:** Difícil para clientes da API consumirem os dados de forma previsível.

### 10. Código Acoplado sem Injeção de Dependências
*   **Descrição:** Instanciar diretamente serviços complexos dentro de classes/funções.
*   **Sinal de Detecção:** `db = new sqlite3.Database()` instanciado diretamente no construtor sem possibilidade de injetar mock.
*   **Impacto:** Dificulta a criação de mocks para testes.
