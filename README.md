# TaskFlow – Sistema de Gerenciamento de Tarefas Ágil

**TechFlow Solutions | Disciplina: Engenharia de Software | UniFECAF**

## Objetivo do Projeto
Este sistema foi desenvolvido para uma startup de logística que necessita gerenciar seu fluxo de trabalho em tempo real, priorizando tarefas críticas e monitorando o desempenho da equipe de forma ágil e integrada.

## Metodologia Adotada
Utilizamos a metodologia Ágil Kanban para garantir flexibilidade e entregas contínuas. O controle de tarefas é documentado de forma transparente e visual através da aba Projects do GitHub, utilizando a divisão clássica em colunas: A Fazer, Em Progresso e Concluído.

## Escopo do Projeto

### Escopo Inicial:
* CRUD completo de tarefas (criar, listar, editar e excluir) via interface de linha de comando (CLI).
* Quadro Kanban estruturado em 3 colunas (A Fazer, Em Progresso, Concluído).
* Atribuição de níveis de prioridade (🟢 Baixa, 🟡 Média, 🔴 Alta) para triagem de criticidade.
* Persistência de dados local automática utilizando arquivos no formato JSON.
* Configuração de Pipeline de Integração Contínua (CI) via GitHub Actions para execução de testes unitários automatizados.

### Gestão de Mudanças (Sprint 2):
Durante o desenvolvimento, o cliente relatou dificuldade em visualizar especificamente as demandas que já estavam sendo executadas pela equipe. Diante disso, foi solicitada uma mudança de escopo de baixo impacto técnico: a implementação de um filtro dinâmico por status na listagem e a funcionalidade de edição de prioridade de tarefas existentes. As alterações foram incorporadas com sucesso, demonstrando a adaptabilidade do modelo ágil.

---

## Instruções de Execução

### Pré-requisitos
Certifique-se de ter o Python 3.11 ou superior instalado em sua máquina.

### 1. Instalação das Dependências
```bash
pip install pytest pytest-cov
```
2. Executando o Sistema
Para iniciar a interface interativa no seu terminal, execute:
```bash
python main.py
```
3. Executando os Testes Automatizados e Cobertura (Coverage)
Para rodar os 22 testes unitários do projeto e validar a cobertura de código das regras de negócio, execute o comando abaixo:
```bash
pytest tests/ -v --cov=src
```
