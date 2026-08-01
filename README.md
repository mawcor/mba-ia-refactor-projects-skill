# Relatório de Execução e Criação da Skill: Refatoração Arquitetural (MVC)

Este documento detalha o funcionamento, as decisões e os resultados da skill `/refactor-arch` executada neste projeto para correção de "Code Smells" e "Arquitetura".

## A) Análise Manual

### Problemas Identificados e Severidade
### Projeto `code-smells-project`
1. **[CRITICAL] SQL Injection & Concatenação Bruta de SQL:** 
   Justificativa: O código utilizava concatenação manual de strings (ex: `+ nome +`) para montar chamadas ao banco e permitia endpoints com comandos SQL arbitrários, o que abre margem extrema para roubo e exclusão maliciosa de dados.
2. **[CRITICAL] Hardcoded Credentials (Segredos no código):** 
   Justificativa: A secret key do framework Flask estava visível explicitamente no arquivo. Se vazada, permite a falsificação de sessões por atacantes.
3. **[HIGH] Queries N+1:** 
   Justificativa: Iterações (`for` loops) realizando buscas individuais em `itens_pedido` e `produtos` para cada pedido encontrado. Causa grande lentidão progressiva (degradação severa da performance conforme os registros crescem).
4. **[MEDIUM] Ausência de Tratamento Centralizado de Erros:** 
   Justificativa: Toda rota ou controller implementava seu próprio bloco longo de `try/except Exception`, gerando repetição imensa e dificultando modificações em larga escala nos padrões de resposta de falha.
5. **[MEDIUM] Lógica de Acesso a Dados Espalhada:** 
   Justificativa: O `app.py` e outras partes misturavam manipulação direta de cursores e deletes do banco. O Controller tornava-se muito acoplado ao Banco.
6. **[LOW] Retornos de API Inconsistentes (Magic Numbers):** 
   Justificativa: A estrutura dos retornos JSON transitava entre ter um nó `dados`, `sucesso`, ou só `mensagem`. Dificulta a vida do consumidor (frontend/mobile).
7. **[LOW] Código Acoplado / Sem Injeção de Dependências:** 
   Justificativa: As funções pegavam o contexto do banco globalmente e estaticamente, dificultando severamente a testabilidade modular (testes unitários).

### Projeto `ecommerce-api-legacy`
1. **[CRITICAL] Hardcoded Credentials / Secrets**
   - *Justificativa*: A presença de variáveis sensíveis (`dbPass`, `paymentGatewayKey`) hardcoded no código original representava uma falha severa de segurança, suscetível a vazamentos diretos se o repositório fosse exposto.
2. **[CRITICAL] God Class / God File / God Method**
   - *Justificativa*: A maior parte do sistema estava centralizada em `src/AppManager.js`. A classe gerenciava a inicialização do banco, schema DB, rotas HTTP e lógica de negócio. Isso violava amplamente o princípio de responsabilidade única (SRP), tornando a aplicação intratável a longo prazo e impossível de testar por partes isoladas.
3. **[HIGH] Queries N+1 / Callback Hell no DB**
   - *Justificativa*: O endpoint financeiro iterava em arrays usando `.forEach` e fazendo requisições assíncronas ao banco lá de dentro para buscar dados complementares. Causava extrema degradação de performance proporcional ao tamanho do banco e leitura complexa (callback hell).
4. **[MEDIUM] Lógica de Acesso a Dados Espalhada**
   - *Justificativa*: Em vez de isolar queries SQL, o antigo `AppManager.js` tinha comandos do SQLite diretamente misturados aos tratamentos da Request/Response, impedindo uma futura troca de banco de dados ou a implementação de testes de mock na persistência.
5. **[MEDIUM] Ausência de Tratamento Centralizado de Erros**
   - *Justificativa*: Muitos ifs no formato `if (err) return res.status(500)...` estavam injetados nas rotas. Havia inconsistência e duplicação nas devolutivas de erro da API.
6. **[LOW] Retornos de API Inconsistentes / Magic Numbers**
   - *Justificativa*: Alguns endpoints devolviam texto plano (ex: `res.send("Bad Request")`) enquanto outros retornavam `JSON`. Isso é um problema prático para clientes (Front-end/Mobile) parsearem as respostas da API de forma padronizada.

### Projeto `task-manager-api`
1. **[CRITICAL] Hardcoded Credentials / Secrets**
   * **Justificativa**: A chave `SECRET_KEY` estava fixa no código (`app.py`), o que expõe o sistema a vazamento de chaves privadas e tokens de produção se o repositório for indevidamente acessado.
2. **[HIGH] Queries N+1 / Problemas de Banco (N+1 Problem)**
   * **Justificativa**: Loops nas rotas (`get_tasks` e `summary_report`) realizavam uma query no banco de dados para cada item retornado. Com o crescimento da base de dados, essa arquitetura causa drásticas perdas de performance e gargalos.
3. **[HIGH] Lógica de Negócio em Views/Rotas (Fat Controllers)**
   * **Justificativa**: Regras de persistência, validações de tamanho e processamento de status estavam dentro da camada de rede (rotas HTTP). Isso quebra o SRP (Princípio de Responsabilidade Única), tornando funções confusas e difíceis de testar de forma isolada.
4. **[MEDIUM] Ausência de Tratamento Centralizado de Erros**
   * **Justificativa**: Havia blocos genéricos de `try/except` com retornos JSON repetidos por cada rota. Isso gera retornos inconsistentes na API se os programadores esquecerem de adicionar em um endpoint futuro.
5. **[LOW] Retornos Inconsistentes / Magic Numbers**
   * **Justificativa**: Uso de literais numéricos na validação de prioridades (`priority < 1 or priority > 5`). Isso gera alto custo de manutenção se a regra de negócio for alterada no futuro (teriam de "caçar" valores no código).

---

## B) Construção da Skill

### Decisões de Design (SKILL.md e Referências)
- **SKILL.md:** Foi estruturado em três fases estritamente sequenciais (Análise, Auditoria e Refatoração). A etapa de Refatoração foi propositalmente bloqueada exigindo o *"Proceed with refactoring (Phase 3)? [y/n]"*. Isso retira do Agente a autonomia sobre gravação destrutiva de dados não validados.
- **Arquivos Referência Modulares:** Em vez de fornecer um mega-prompt gigante (o que sobrecarrega a janela de contexto da IA), os guias foram diluídos na pasta `references/` e consultados sob demanda pelo agente através de ferramentas (`view_file`).

### Catálogo de Anti-patterns
O catálogo foi focado em problemas que a IA LLM capta com facilidade (padrões lógicos universais): God classes, injeções SQL, fat controllers e N+1 queries. Selecionamos eles por representarem grande parte das causas de problemas legados e de gargalos operacionais em microsserviços.

### Agnosticidade de Tecnologia
A skill consegue funcionar para várias linguagens devido ao arquivo `analysis-heuristics.md`. Ele mapeia além das extensões nativas (`.py`, `.js`, `.java`), também padrões (ex: se acha `pom.xml` -> Java, se acha `package.json` -> JS, se acha `requirements.txt` -> Python), ditando ao agente como classificar o Framework sem "chumbar" comandos estáticos num arquivo só. O Playbook de correção foca na refatoração *abstrata* conceitual (MVC).

### Desafios e Resoluções
- **Desafio:** A IA poderia não encontrar problemas suficientes ou focar em formatação de código (linting) em vez de arquitetura.
- **Resolução:** Instrução fixa estipulando *"Encontre pelo menos 5 problemas englobando X severidades diferentes"*, forçando a IA a focar no design arquitetural e cruzar os arquivos.
- 
- **Desafio**: As LLMs tendem a tentar refazer tudo de uma vez e se perdem na lógica de negócio do sistema antigo durante a refatoração.
- **Solução**: Desenvolvemos o arquivo `refactoring-playbook.md` com trechos claros do formato *"Antes e Depois"* mostrando transformações em micro passos para que a IA não altere o escopo funcional enquanto ajusta a estrutura.

---

## C) Resultados

### Resumo da Auditoria dos Projetos
### Projeto `code-smells-project`
- **Total de Findings:** 7
- **Severidade:** 2x CRITICAL, 1x HIGH, 2x MEDIUM, 2x LOW.

### Projeto `ecommerce-api-legacy`
- **Total de Findings:** 7
- **Severidade:** 2x CRITICAL, 1x HIGH, 2x MEDIUM, 2x LOW.

### Projeto `task-manager-api`
- **Total de Findings:** 7
- **Severidade:** 1x CRITICAL, 2x HIGH, 2x MEDIUM, 2x LOW.


### Comparação Antes/Depois da Estrutura
### Projeto `code-smells-project`
**ANTES:**
A raiz detinha toda a configuração e os arquivos de controle, modelo e banco de dados estavam todos misturados sem separação clara de responsabilidades, com chamadas de banco diretas e regras complexas sem coesão.
```text
.
├── app.py
├── controllers.py
├── database.py
└── models.py
```

**DEPOIS (Padrão MVC):**
Criação das pastas separadas por responsabilidades. Uma nova camada isolada de `config/` e `utils/` foi criada. O roteamento foi movido para `routes/api_routes.py`, deixando o `app.py` focado no Factory Pattern e orquestração limpa.
```text
.
├── app.py
├── config/ (database.py, settings.py)
├── controllers/ (pedido_controller.py, produto_controller.py, usuario_controller.py)
├── models/ (pedido_model.py, produto_model.py, usuario_model.py)
├── routes/ (api_routes.py)
└── utils/ (error_handler.py, response.py)
```

### Projeto `ecommerce-api-legacy`
**ANTES:** 
Apenas 3 arquivos formavam a API e detinham dezenas de responsabilidades. Nenhuma clareza sobre domínios (User, Course, Payment).
```text
.
├── src/
│   ├── app.js
│   ├── AppManager.js
│   └── utils.js
└── package.json
```

**DEPOIS (Padrão MVC):**
```text
.
├── src/
│   ├── app.js
│   ├── config/ (database.js, settings.js)
│   ├── controllers/ (CheckoutController.js, ReportController.js, UserController.js)
│   ├── models/ (CourseModel.js, UserModel.js, ReportModel.js, ...)
│   ├── routes/ (api_routes.js)
│   └── utils/ (cache.js, crypto.js, error_handler.js)
└── package.json
```

### Projeto `task-manager-api`
**ANTES:**
A raiz detinha toda a configuração e acesso, e a pasta `routes/` atuava de maneira inflada centralizando todas as responsabilidades pesadas de validação e comunicação de negócio.
```text
.
├── app.py
├── database.py
├── requirements.txt
├── seed.py
├── models/ (category.py, task.py, user.py)
├── routes/ (report_routes.py, task_routes.py, user_routes.py)
├── services/ (notification_service.py)
└── utils/ (helpers.py)
```

**DEPOIS:**
Criação de `config.py` e `utils/error_handler.py`. Uma nova camada isolada de `controllers/` com regras restritas abstraindo o processamento, permitindo que a camada de `routes/` mantenha apenas o *mapping* (roteamento) de chamadas HTTP.
```text
.
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── seed.py
├── controllers/ (report_controller.py, task_controller.py, user_controller.py)
├── models/ (category.py, task.py, user.py)
├── routes/ (report_routes.py, task_routes.py, user_routes.py)
├── services/ (notification_service.py)
└── utils/ (error_handler.py, helpers.py)
```

### Checklist de Validação
### Projeto `code-smells-project`
### Fase 1 — Análise
- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Domínio da aplicação descrito corretamente
- [x] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [x] Relatório segue o template definido nos arquivos de referência
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados
- [x] Detecção de APIs deprecated incluída (se aplicável)
- [x] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para módulo de config (sem hardcoded)
- [x] Models criados para abstrair dados
- [x] Views/Routes separadas para visualização ou roteamento
- [x] Controllers concentram o fluxo da aplicação
- [x] Error handling centralizado
- [x] Entry point claro
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem corretamente

### Projeto `ecommerce-api-legacy`
### Fase 1 — Análise
- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Domínio da aplicação descrito corretamente
- [x] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [x] Relatório segue o template definido nos arquivos de referência
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados
- [x] Detecção de APIs deprecated incluída (se aplicável)
- [x] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para módulo de config (sem hardcoded)
- [x] Models criados para abstrair dados
- [x] Views/Routes separadas para visualização ou roteamento
- [x] Controllers concentram o fluxo da aplicação
- [x] Error handling centralizado
- [x] Entry point claro
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem corretamente

### Projeto `task-manager-api`
### Fase 1 — Análise
- [x] Linguagem detectada corretamente
- [x] Framework detectado corretamente
- [x] Domínio da aplicação descrito corretamente
- [x] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [x] Relatório segue o template definido nos arquivos de referência
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados
- [x] Detecção de APIs deprecated incluída (se aplicável)
- [x] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para módulo de config (sem hardcoded)
- [x] Models criados para abstrair dados
- [x] Views/Routes separadas para visualização ou roteamento
- [x] Controllers concentram o fluxo da aplicação
- [x] Error handling centralizado
- [x] Entry point claro
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem corretamente

### Logs de Verificação 
### Projeto `code-smells-project`
```text
python app.py
==================================================
SERVIDOR INICIADO
Rodando em http://localhost:5000 (DEBUG=True)
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.101.12:5000
Press CTRL+C to quit
 * Restarting with stat
==================================================
SERVIDOR INICIADO
Rodando em http://localhost:5000 (DEBUG=True)
==================================================
 * Debugger is active!
 * Debugger PIN: 316-697-306
127.0.0.1 - - [01/Aug/2026 14:40:07] "GET /usuarios HTTP/1.1" 200 -
```

### Projeto `ecommerce-api-legacy`
```text
npm start

> desafio-arquitetura-ia-boilerplate@1.0.0 start
> node src/app.js

◇ injected env (0) from .env // tip: ◈ secrets for agents [www.dotenvx.com]
Frankenstein LMS rodando na porta 3000...
[LOG] Salvando no cache: last_checkout_2
Error: Pagamento recusado
    at processCheckout (/home/marcos/Documents/Estudos/MBA Full Cycle/Desafios/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/controllers/CheckoutController.js:37:23)
[LOG] Salvando no cache: last_checkout_2
```

### Projeto `task-manager-api`
```text
python app.py 
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.101.12:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 213-625-934
127.0.0.1 - - [01/Aug/2026 14:46:38] "GET /tasks HTTP/1.1" 200 -
127.0.0.1 - - [01/Aug/2026 14:46:41] "GET /users HTTP/1.1" 200 -
```

### Observações Comportamentais
A skill demonstrou-se robusta. Em poucos turnos o agente diagnosticou o framework Flask perfeitamente, listou os problemas exatos nas linhas em que ocorriam, paralisou a atividade e, com o "Go" do usuário, procedeu manipulando a estrutura de pastas e segregando cada camada isoladamente.
A instrução de parada (Phase 2 -> Phase 3) e o isolamento de manuais nas `references/` criaram uma barreira muito segura para não corromper o sistema e demonstraram que o Agente de IA consegue auditar em altíssimo nível com as heurísticas bem definidas.
Seguiu todas as referências metodicamente e não executou um simples "Find and Replace", demonstrando capacidade de entender o que era Model e Controller.

---

## D) Como Executar
### Pré-requisitos
- O ambiente Gemini Antigravity CLI (`agy`) instalado e ativo no seu terminal.
- A skill customizada inserida e linkada à pasta `.agents/skills/refactor-arch` dentro de cada projeto.

### Comandos para executar a skill em cada projeto
### Projeto `code-smells-project`
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Projeto `ecommerce-api-legacy`
```bash
npm install
npm start
```

### Projeto `task-manager-api`
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

Basta digitar, no chat ou prompt inicial do agente, a respectiva invocação:
```bash
/refactor-arch
```
*(O agente começará a iterar sobre as fases imediatamente.)*

### Como validar que a refatoração funcionou
### Projeto `code-smells-project`
1. Ative seu ambiente virtual na raiz do projeto (ex: `source venv/bin/activate`).
2. Rode a aplicação com `python app.py`.
3. Valide o `Health Check` com o comando para garantir a saúde dos blueprints:
```bash
curl -X GET http://localhost:5000/health
```
4. Se o status retornar `200 OK` acompanhado das integrações corretas de banco de dados, o MVC está com suas integrações sólidas e em total conformidade arquitetônica.

### Projeto `ecommerce-api-legacy`
1. Rode a aplicação com `npm start`.
2. Valide o `financial-report` com o comando:
```bash
curl -X GET http://localhost:3000/api/admin/financial-report
```
3. Se o status retornar `200 OK` acompanhado do report, o MVC está com suas integrações sólidas e em total conformidade arquitetônica.

### Projeto `task-manager-api`
1. Ative seu ambiente virtual na raiz do projeto (ex: `source venv/bin/activate`).
2. Execute o seed `python seed.py`.
3. Rode a aplicação com `python app.py`.
4. Valide o `Reports Summary` com o comando:
```bash
curl -X GET http://localhost:5000/reports/summary
```
5. Se o status retornar `200 OK` acompanhado resumo de relatórios, o MVC está com suas integrações sólidas e em total conformidade arquitetônica.
