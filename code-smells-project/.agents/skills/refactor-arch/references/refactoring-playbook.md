# Playbook de Refatoração

Este documento detalha 8 padrões de transformação práticos para corrigir anti-patterns estruturais detectados. Utilize-os durante a Fase 3.

## 1. Desmembrando God Classes/Files
**Problema:** Um arquivo contém rotas, queries e lógica de negócio.
**Transformação:** Criar arquivos separados por domínio e camada.
*   Antes (`app.js`):
    ```javascript
    app.get('/users', (req, res) => {
        db.all("SELECT * FROM users", (err, rows) => { res.json(rows); });
    });
    ```
*   Depois:
    *   `models/user.js`: encapsula a lógica do BD (`class UserModel { static getAll() {...} }`).
    *   `controllers/user_controller.js`: gerencia a resposta HTTP (`UserController { static getAll(req, res) { UserModel.getAll().then(...) } }`).
    *   `routes/user_routes.js`: mapeia a rota (`router.get('/', UserController.getAll);`).

## 2. Removendo Hardcoded Secrets
**Problema:** Chaves secretas em texto plano no código.
**Transformação:** Utilizar variáveis de ambiente ou arquivo de configuração centralizado (ler de `.env` preferencialmente, mas no caso de refatorações simples, mover para `config/settings.py` como fallback se `.env` não estiver disponível para carregar na linguagem nativamente sem deps extras). Em Python usar `os.environ.get()`, em JS `process.env`.
*   Antes: `app.config['SECRET_KEY'] = '12345'`
*   Depois: `app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')`

## 3. Resolvendo N+1 Queries e Callback Hell
**Problema:** Loops fazendo queries assíncronas no DB causando aninhamento severo.
**Transformação:** Utilizar `JOIN`s do SQL e reescrever com `async/await` ou `Promises`.
*   Antes:
    ```javascript
    courses.forEach(c => {
        db.all("SELECT * FROM enrollments...", () => { ... db.get("users", ...) ... })
    });
    ```
*   Depois (usando `JOIN`):
    ```javascript
    const rows = await db.allAsync(`
        SELECT c.title, p.amount, u.name 
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        LEFT JOIN payments p ON p.enrollment_id = e.id AND p.status = 'PAID'
        LEFT JOIN users u ON u.id = e.user_id
    `);
    // Agrupar no código
    ```

## 4. Mitigando Arbitrary SQL Execution
**Problema:** Endpoints que aceitam SQL como string.
**Transformação:** Se a rota `/admin/query` for um endpoint real de aplicação (não de debug puro do lab), ele deve ser deletado ou restrito severamente, e queries customizadas devem usar parametros de query `WHERE foo = ?`.
*   Antes: `cursor.execute(req.body.sql)`
*   Depois: Remover endpoint perigoso, ou parametrizar e pre-definir queries baseadas em escopo restrito.

## 5. Extraindo Regras de Negócio de Rotas (Fat Controllers -> Thin Controllers)
**Problema:** Controladores enormes.
**Transformação:** Mover validações complexas e lógicas puras (cálculos) para Services ou Models.
*   Antes (Python Route):
    ```python
    @app.route('/tasks/stats')
    def stats():
        total = db.query("COUNT")
        pending = db.query("COUNT WHERE pending")
        overdue = 0
        for t in db.query("ALL"):
            if t.date < now: overdue += 1
        return {"total": total, "overdue": overdue}
    ```
*   Depois (Controller chama Model):
    ```python
    @app.route('/tasks/stats')
    def stats():
        return jsonify(TaskModel.get_stats()), 200
    ```
    (E toda lógica fica em `TaskModel.get_stats()`).

## 6. Padronização de Tratamento de Erros
**Problema:** Erros 500 inconsistentes no controlador.
**Transformação:** Extrair `try/except` grandes usando decorators (Python) ou middlewares de erro (Express).
*   Antes: Cada rota tem `try { ... } catch (err) { res.status(500).json(...) }`
*   Depois (Express): `app.use((err, req, res, next) => res.status(500).json({error: err.message}))` e as rotas chamam `next(err)`.

## 7. Padronização de Retornos
**Problema:** `res.send("Erro")` em um lugar, `res.json({"error": "Erro"})` em outro.
**Transformação:** Usar classes DTO (Data Transfer Objects) ou helpers estáticos para padronizar.
*   Sempre retornar JSON. `return jsonify({"error": "...", "status": 404}), 404`.

## 8. Evitando acoplamento direto de conexão DB
**Problema:** `import sqlite3; db = sqlite3.connect()` espalhado por vários arquivos de rotas.
**Transformação:** Criar classe de conexão central ou arquivo `database.js`/`database.py`.
*   Antes: Vários arquivos instanciando DB localmente.
*   Depois: `from config.database import get_db` e passar a instância ou utilizar Factory/Singleton de forma injetável.
