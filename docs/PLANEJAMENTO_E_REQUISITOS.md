# Planejamento e Requisitos — TaskSec

## 1. Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF01 | Autenticação de usuários (registro, login, logout) | Alta |
| RF02 | Gerenciamento de tarefas (CRUD: criar, editar, excluir, visualizar) | Alta |
| RF03 | Pesquisa de tarefas por palavra-chave | Média |
| RF04 | Paginação na listagem de tarefas | Média |
| RF05 | Healthcheck da aplicação (endpoint /health) | Alta |
| RF06 | Logs de autenticação via syslog (sucesso/falha) | Alta |

## 2. Requisitos Não Funcionais

| ID | Requisito | Descrição |
|----|-----------|-----------|
| RNF01 | Container Docker | Aplicação empacotada em container Docker |
| RNF02 | SAST (Bandit) | Análise estática de segurança no código Python |
| RNF03 | Dependency Scan | OWASP Dependency-Check para bibliotecas |
| RNF04 | DAST (ZAP) | Teste dinâmico de segurança com OWASP ZAP |
| RNF05 | CI/CD Automatizado | Pipeline com GitHub Actions |
| RNF06 | Logs de Segurança | Syslog para eventos de autenticação |
| RNF07 | Monitoramento | Fail2ban para detecção de brute force |

## 3. Arquitetura

```
[Usuário] → [Navegador] → [Flask/Gunicorn :8080] → [SQLite]
                                │
                                ↓
                           [Syslog]
                                │
                                ↓
                           [Fail2ban]
```

## 4. Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.12 |
| Framework | Flask 3.1 |
| Servidor WSGI | Gunicorn |
| ORM | SQLAlchemy |
| Templates | Jinja2 + Bootstrap 5 |
| Container | python:3.12-slim |
| Orquestração | Docker Compose |
| CI/CD | GitHub Actions |
| SAST | Bandit |
| Dependências | OWASP Dependency-Check |
| DAST | OWASP ZAP |
| Log | Syslog (syslog-ng) |
| Monitoramento | Fail2ban |

## 5. Pipeline CI/CD (GitHub Actions)

```
push/PR → Test → Bandit → Dependency-Check → Docker Build → ZAP DAST → Stage → Produção
```

## 6. Ameaças e Mitigações

| Ameaça | Mitigação |
|--------|-----------|
| Ataque de força bruta | Fail2ban analisando logs, bloqueio por 1h após 5 falhas |
| Injeção SQL | SQLAlchemy ORM (parametrização) |
| XSS | Jinja2 autoescaping |
| CSRF | Flask-WTF com tokens CSRF |
| Dependências vulneráveis | OWASP Dependency-Check no pipeline |
| Código inseguro | Bandit (SAST) no pipeline |
| Senhas fracas | Hash com Werkzeug (bcrypt) |
| Acesso não autenticado | Flask-Login com @login_required |
