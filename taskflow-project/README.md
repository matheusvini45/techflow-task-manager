# 📋 TaskFlow – Sistema de Gerenciamento de Tarefas

> **TechFlow Solutions** | Disciplina: Engenharia de Software | UniFECAF

[![CI](https://github.com/seu-usuario/taskflow/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/taskflow/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)

---

## 🎯 Objetivo

Sistema de gerenciamento de tarefas desenvolvido para uma startup de logística,
permitindo acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas
e monitorar o progresso da equipe com base em metodologias ágeis.

---

## 📦 Escopo do Projeto

**Escopo inicial:**
- CRUD completo de tarefas (criar, listar, editar, excluir)
- Quadro Kanban com 3 colunas: *A Fazer*, *Em Progresso*, *Concluído*
- Priorização de tarefas (Baixa / Média / Alta)
- Persistência local em JSON

**Mudança de escopo (Sprint 2):**
> Foi identificada a necessidade de um **filtro por status** e **edição de prioridade** já
> durante o desenvolvimento. Essas funcionalidades foram adicionadas na tela de listagem
> e no menu de edição, pois o cliente relatou dificuldade em visualizar apenas as tarefas
> em progresso. A mudança foi de baixo impacto técnico e não alterou a arquitetura base,
> sendo incorporada sem atraso na entrega.

---

## 🏗️ Metodologia

Utilizamos **Kanban** como metodologia ágil principal:

- Fluxo contínuo de tarefas sem sprints fixos
- Quadro no GitHub Projects com colunas: **To Do → In Progress → Done**
- Commits semânticos a cada funcionalidade entregue
- Pipeline de CI via GitHub Actions para garantir qualidade contínua

---

## 📁 Estrutura de Diretórios

```
taskflow/
├── src/
│   └── task_manager.py      # Modelos, repositório e serviço
├── tests/
│   └── test_task_manager.py # Testes automatizados (pytest)
├── docs/
│   └── diagramas/           # Diagramas UML (casos de uso, classes)
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline GitHub Actions
├── main.py                  # Ponto de entrada (CLI)
├── tasks.json               # Banco de dados local (gerado em runtime)
└── README.md
```

---

## 🚀 Como Executar

**Pré-requisitos:** Python 3.11+

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/taskflow.git
cd taskflow

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Execute o sistema
python main.py
```

---

## 🧪 Testes Automatizados

```bash
# Instalar pytest
pip install pytest pytest-cov

# Rodar todos os testes
pytest tests/ -v

# Rodar com relatório de cobertura
pytest tests/ -v --cov=src --cov-report=term-missing
```

Os testes cobrem:
- Criação de tarefas (validações de título, prioridade)
- Leitura (listagem, busca por ID e status)
- Atualização (edição de campos, movimentação no Kanban)
- Exclusão (com verificação de existência)
- Persistência (dados salvos e recuperados entre instâncias)

---

## ⚙️ CI/CD – GitHub Actions

O workflow em `.github/workflows/ci.yml` é acionado em todo `push` e `pull request`
para `main`, executando automaticamente:
1. Instalação das dependências
2. Rodando os testes com pytest
3. Verificando cobertura mínima de 80%

---

## 📌 Histórico de Commits (resumo)

| Commit | Descrição |
|--------|-----------|
| `feat: estrutura inicial do projeto` | Criação das pastas e arquivos base |
| `feat: modelo Task com serialização JSON` | Classe Task com to_dict/from_dict |
| `feat: TaskRepository com CRUD completo` | Persistência em arquivo JSON |
| `feat: TaskService com regras de negócio` | Validações e lógica de domínio |
| `feat: CLI interativa com menu` | Interface de linha de comando |
| `test: testes unitários para CRUD` | Suite completa de testes com pytest |
| `ci: pipeline GitHub Actions` | Workflow de integração contínua |
| `feat: filtro por status no Kanban` | Mudança de escopo – Sprint 2 |
| `feat: edição de prioridade` | Melhoria solicitada pelo cliente |
| `docs: README.md completo` | Documentação final do projeto |
