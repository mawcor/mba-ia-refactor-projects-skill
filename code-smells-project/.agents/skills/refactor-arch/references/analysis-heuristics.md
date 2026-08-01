# Project Analysis Heuristics

Este documento fornece diretrizes para detectar a stack tecnológica, frameworks, dependências e arquitetura atual de um projeto durante a Fase 1 da skill de refatoração arquitetural.

## 1. Detecção de Linguagem e Dependências Principais

*   **Identificação pela Extensão de Arquivo:**
    *   **Heurística:** Procure pelas extensões de código-fonte mais presentes no diretório raiz ou nas pastas `/src`, `/app` e `/lib` (ex: `.js`/`.ts` para Node, `.py` para Python, `.java` para Java, `.php` para PHP, `.rb` para Ruby, `.go` para Go, `.cs` para C#).

*   **Identificação pelos Gerenciadores de Dependência (Manifestos):**
    *   **Heurística:** Leia o arquivo principal de configuração de pacotes na raiz do projeto para determinar não apenas a linguagem, mas o framework web e as bibliotecas de persistência.
    *   **Node.js / JavaScript / TypeScript:** Buscar por `package.json`. Verificar campo "dependencies" (ex: "express", "nestjs", "sequelize", "mongoose").
    *   **Python:** Buscar por `requirements.txt`, `Pipfile`, `pyproject.toml`. Verificar bibliotecas (ex: "flask", "django", "fastapi", "sqlalchemy").
    *   **Java / Kotlin:** Buscar por `pom.xml` (Maven) ou `build.gradle` (Gradle). Verificar artefatos (ex: "spring-boot-starter-web", "hibernate").
    *   **PHP:** Buscar por `composer.json`. Verificar campo "require" (ex: "laravel/framework", "symfony/http-foundation").
    *   **Ruby:** Buscar por `Gemfile`. Verificar gems (ex: "rails", "sinatra", "activerecord").
    *   **Go:** Buscar por `go.mod`. Verificar require (ex: "gin-gonic/gin", "gorm.io/gorm").
    *   **C# / .NET:** Buscar por `*.csproj` ou `*.sln`. Verificar "PackageReference" (ex: "Microsoft.AspNetCore.Mvc", "Entity Framework").

*   **Identificação de Conexão com Banco de Dados vs ORM:**
    *   **Heurística:** Se não encontrar bibliotecas de ORM declaradas, busque no código fonte por imports/requires padrão de bibliotecas nativas de SQL da respectiva linguagem (ex: `java.sql.*`, `database/sql` no Go, `sqlite3` no Node/Python, funções `mysqli_*` ou `PDO` no PHP).

## 2. Detecção de Arquitetura e Estrutura

*   **Monolítica / Arquivo Único (God File):**
    *   **Sinal:** Grande parte da lógica (rotas, queries BD, regras de negócio) concentra-se em 1 ou poucos arquivos grandes (ex: `app.py`, `app.js`, `AppManager.js`, `models.py` fazendo papel de controller).
*   **Organização Parcial / Separação por Pastas:**
    *   **Sinal:** Presença de pastas como `routes/`, `controllers/`, `models/`, ou `services/`.
    *   **Heurística:** Analisar se a separação é efetiva. Muitas vezes as rotas contêm lógica de negócio pesada, o que indica que, apesar de pastas existirem, a arquitetura MVC está corrompida.

## 3. Mapeamento de Domínio e Banco de Dados

*   **Sinal:** Nomes das tabelas em comandos SQL (`CREATE TABLE`, `SELECT FROM`) ou definição de Models ORM.
*   **Heurística:**
    *   Procurar por `cursor.execute("SELECT ... FROM x")` ou `db.run("... TABLE x")`.
    *   Exemplo: Se o sistema tem tabelas `produtos`, `usuarios`, `pedidos`, o domínio é "E-commerce API (produtos, pedidos, usuários)".
    *   Exemplo: Se o sistema tem `tasks`, o domínio é "Task Manager API".
