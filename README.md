# Task Manager using Flask — Estudo de Caso DevSecOps

Este repositorio usa como base o projeto indicado no enunciado do professor:

```text
https://github.com/AdityaBagad/Task-Manager-using-Flask
```

A aplicacao original foi mantida como um gerenciador simples de tarefas com Flask, autenticacao de usuarios e CRUD de tarefas. Para o estudo de caso, a base foi adaptada para execucao em container Docker e recebeu controles de seguranca, testes automatizados, pipeline CI/CD, SAST, analise de dependencias, DAST e logs via syslog.

## Stack

- Aplicacao: Python 3.12 + Flask + Gunicorn
- Banco: SQLite via Flask-SQLAlchemy
- Autenticacao: Flask-Login + Flask-Bcrypt
- Formularios: Flask-WTF
- Container: Docker + Docker Compose
- CI/CD: GitHub Actions e GitLab CI
- SAST: Bandit
- Analise de dependencias: OWASP Dependency-Check e pip-audit
- DAST: OWASP ZAP Baseline
- Logs: syslog-ng
- Monitoramento: Fail2ban

## Execucao Local

```bash
docker compose up -d --build
curl http://localhost:8080/health
```

Acesse:

```text
http://localhost:8080
```

## Rotas Principais

- `/register`: cadastro de usuario
- `/login`: autenticacao
- `/logout`: encerramento de sessao
- `/all_tasks`: listagem de tarefas autenticada
- `/add_task`: criacao de tarefa
- `/all_tasks/<id>/update_task`: atualizacao de tarefa
- `/all_tasks/<id>/delete_task`: exclusao de tarefa
- `/account`: configuracoes da conta
- `/health`: healthcheck do container/pipeline

## Testes e Validacoes Locais

```bash
python -m pytest tests/ -v --cov=todo_project.todo_project --cov-report=term
python -m bandit -r todo_project/todo_project -c .bandit.yaml
python -m pip_audit -r requirements.txt --no-deps --disable-pip
```

Observacao: a validacao local de Bandit foi executada em Python 3.11 porque a versao local Python 3.14 apresentou incompatibilidade interna do Bandit. A esteira usa Python 3.12.

## Pipeline

O pipeline executa:

1. Testes automatizados com cobertura.
2. Bandit SAST.
3. OWASP Dependency-Check.
4. pip-audit para dependencias Python.
5. Build Docker.
6. OWASP ZAP Baseline.
7. Deploy stage/homologacao simulado nas branches `homolog`, `staging` e `main`.
8. Deploy producao condicionado a branch `main`.

Branches previstas:

- `develop`
- `homolog`
- `staging`
- `main`

## Estrutura

```text
.
├── todo_project/                  # Codigo base adaptado do projeto original
│   ├── run.py
│   └── todo_project/
│       ├── __init__.py
│       ├── forms.py
│       ├── models.py
│       ├── routes.py
│       ├── static/
│       └── templates/
├── tests/                         # Testes automatizados
├── fail2ban/                      # Configuracao de monitoramento
├── .github/workflows/             # GitHub Actions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitlab-ci.yml
```

## Itens Locais

Documentacao de entrega, evidencias, PDFs, instrucoes do professor e relatorios ficam apenas localmente e nao devem ser enviados como arquivos separados no repositorio remoto.
