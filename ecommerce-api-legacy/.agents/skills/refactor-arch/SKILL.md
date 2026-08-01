---
name: refactor-arch
description: Refatora um projeto legado (agnóstico de tecnologia) para a arquitetura MVC, auditando anti-patterns e separando responsabilidades.
---

# Refatoração Arquitetural Automatizada (refactor-arch)

Esta skill permite analisar, auditar e refatorar qualquer projeto (independente de linguagem ou framework) para o padrão de arquitetura MVC (Model-View-Controller).

A execução é dividida em 3 fases sequenciais. Você deve realizar cada fase rigorosamente seguindo as instruções abaixo e consultando os arquivos de referência apropriados.

## Phase 1: Project Analysis

1.  **Objetivo**: Detectar a linguagem, o framework, as dependências, mapear o domínio e a arquitetura atual do projeto.
2.  **Como**: Explore os arquivos do diretório atual. Leia o `package.json`, `requirements.txt` ou equivalentes para identificar a stack.
3.  **Referência**: Leia o arquivo `references/analysis-heuristics.md` para entender como extrair essas informações.
4.  **Saída**: Imprima um resumo da análise no terminal exatamente neste formato:
    ```
    ================================
    PHASE 1: PROJECT ANALYSIS
    ================================
    Language:      <Linguagem detectada>
    Framework:     <Framework detectado com versão>
    Dependencies:  <Principais libs>
    Domain:        <Descrição do negócio ex: E-commerce API (produtos, pedidos, usuários)>
    Architecture:  <Resumo da estrutura atual ex: Monolítica — tudo em 4 arquivos>
    Source files:  <Quantidade> files analyzed
    DB tables:     <Tabelas ou modelos detectados>
    ================================
    ```
5.  Em seguida, inicie a Fase 2 automaticamente.

## Phase 2: Architecture Audit

1.  **Objetivo**: Cruzar o código atual com um catálogo de anti-patterns arquiteturais e gerar um relatório estruturado.
2.  **Como**: Leia o código fonte da aplicação identificada na Fase 1. Para cada arquivo relevante, verifique a ocorrência de problemas.
3.  **Referências**:
    *   Leia `references/anti-patterns-catalog.md` para conhecer a lista de code smells, severidades (CRITICAL, HIGH, MEDIUM, LOW) e APIs deprecated a buscar.
    *   Leia `references/audit-report-template.md` para formatar a sua saída.
4.  **Saída**:
    *   **CRÍTICO/OBRIGATÓRIO**: Identifique **pelo menos 5 problemas**. A sua resposta será rejeitada se não contiver a distribuição exata ou superior de: 1 CRITICAL ou HIGH, 2 MEDIUM e 2 LOW.
    *   Apresente o relatório final da auditoria imprimindo no terminal o conteúdo baseado em `references/audit-report-template.md`.
5.  **Confirmação do Usuário**: Após imprimir o relatório de auditoria, você **DEVE PAUSAR** a execução e perguntar ao usuário: `Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]`. Prossiga para a Fase 3 **apenas se** o usuário confirmar com `y` ou `yes`.
6.  Antes de solicitar a **Confirmação do usuário**, verifique se realmente identificou **pelo menos 5 problemas**, incluindo no mínimo: 1 CRITICAL ou HIGH, 2 MEDIUM e 2 LOW. Caso a quantidade de findings de algum tipo não tenha sido atingido, analisar novamente para identificar.

## Phase 3: Refactoring

1.  **Objetivo**: Reestruturar o projeto para o padrão MVC alvo, corrigindo todos os anti-patterns listados no relatório da Fase 2, e garantir que a aplicação inicie e que as rotas funcionem.
2.  **Referências**:
    *   Leia `references/mvc-guidelines.md` para entender as regras da arquitetura MVC de destino (separação em Models, Views/Routes, Controllers).
    *   Leia `references/refactoring-playbook.md` para aplicar os padrões corretos de transformação de código para cada problema.
3.  **Como**:
    *   Extraia hardcoded secrets para arquivos de configuração adequados ou variáveis de ambiente.
    *   Separe regras de negócio em Controllers.
    *   Mova a lógica de acesso a dados (SQL/ORM) para Models/Repositórios.
    *   Deixe as rotas/views encarregadas apenas de receber requests e despachar para os Controllers.
    *   Centralize o tratamento de erros.
    *   Mantenha a mesma funcionalidade original.
    *   Faça as alterações nos arquivos correspondentes (crie as pastas `controllers`, `models`, `routes`, etc., conforme necessário pela linguagem/framework atual).
4.  **Validação**: Teste ou verifique cuidadosamente seu código para garantir que ele esteja sintaticamente correto.
5.  **Saída**: Após concluir as alterações no código, imprima:
    ```
    ================================
    PHASE 3: REFACTORING COMPLETE
    ================================
    ## New Project Structure
    <árvore de diretórios resultante>

    ## Validation
      ✓ Application boots without errors
      ✓ All endpoints respond correctly
      ✓ Zero anti-patterns remaining
    ================================
    ```

## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados (OBRIGATÓRIO: pelo menos 1 CRITICAL ou HIGH, 2 MEDIUM e 2 LOW)
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente