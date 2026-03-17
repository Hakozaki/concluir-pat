---
description: Workflow para automação de Git add e commit semântico em PT-BR.
---

---
name: git-semantic-commit-workflow
description: Workflow para automação de Git add e commit semântico em PT-BR.
---

# Workflow: Git Semantic Commit Pro

Este workflow automatiza o processo de staging e commit seguindo as normas de verbos no presente e prefixos específicos.

## Steps

### 1. Preparação de Contexto
- **Comando:** `git add .`
- **Ação:** Captura todas as alterações para análise de diff.

### 2. Geração da Mensagem (Prompt IA)
**Instruções para o Agente:**
> Analise o `git diff --staged`. Gere uma mensagem de commit única seguindo:
> - **Idioma:** Português do Brasil.
> - **Proibição:** Nunca usar verbos no infinitivo (ex: adicionar, implementar).
> - **Obrigação:** Usar verbos no presente/imperativo (ex: adiciona, implementa, altera, corrige, remove).
> - **Estrutura:** `<prefixo>: <descrição separada por vírgulas>`.
> - **Prefixos permitidos:** feat, fix, docs, style, refactor, test, build, chore.

### 3. Confirmação do Usuário
- **Ação:** Exibir a mensagem gerada para validação.
- **Pergunta:** "Deseja realizar o commit com a mensagem: `{{mensagem_gerada}}`?"

### 4. Execução Final
- **Comando:** `git commit -m "{{mensagem_gerada}}"`

---

## Exemplo de Saída Esperada
`feat: implementa middleware de validação JWT, integra contadores PAT no painel de controle e documenta novos endpoints da API PAT.`