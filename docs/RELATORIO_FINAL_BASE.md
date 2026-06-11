# Relatório Final — Estudo de Caso DevSecOps

**Curso:** Especialização em DevSecOps — Hackers do Bem (3ª Onda)
**Aluno:** [SEU NOME]
**Data:** [DATA]

---

## 1. Introdução

Este estudo de caso teve como objetivo criar, implementar e assegurar a segurança de um sistema de gerenciamento de tarefas pessoais (TaskSec), aplicando conceitos de SDLC, DevOps, Desenvolvimento Seguro, Containers Docker e DevSecOps.

## 2. Stack Utilizada

| Componente | Tecnologia |
|------------|-----------|
| Aplicação | Python 3.12 + Flask |
| Container | python:3.12-slim + Docker Compose |
| SAST | Bandit |
| Dependency Scan | OWASP Dependency-Check |
| DAST | OWASP ZAP Baseline |
| CI/CD | GitHub Actions |
| Log | Syslog (syslog-ng) |
| Monitoramento | Fail2ban |
| Controle de versão | Git + GitHub |

## 3. Etapas Realizadas

### Etapa 1 — Planejamento e Requisitos
- Definição de requisitos funcionais e não funcionais
- Mapeamento de ameaças e mitigações
- Definição da arquitetura do sistema

### Etapa 2 — Desenvolvimento
- Aplicação Flask com autenticação obrigatória
- CRUD de tarefas com SQLite/SQLAlchemy
- Logs de segurança via syslog
- Container Docker com python:3.12-slim

### Etapa 3 — Pipeline CI/CD
- Pipeline GitHub Actions com 7 stages:
  1. Testes automatizados (Pytest)
  2. SAST com Bandit
  3. Análise de dependências com OWASP Dependency-Check
  4. Build da imagem Docker
  5. DAST com OWASP ZAP
  6. Deploy em Stage
  7. Deploy em Produção (manual)

### Etapa 4 — SAST (Bandit)
- [Print do relatório Bandit]
- Resultados: [X] alerts encontrados, [Y] corrigidos

### Etapa 5 — DAST (OWASP ZAP)
- [Print do relatório ZAP]
- Resultados: [X] alertas, [Y] de alto risco

### Etapa 6 — Entrega Contínua
- Stage: deploy automático ao fazer merge na branch staging
- Produção: deploy manual aprovado na branch main

### Etapa 7 — Monitoramento
- Fail2ban configurado para bloquear brute force
- Logs de autenticação enviados via syslog
- [Print do log de tentativas de login]

## 4. Pipeline Final (GitHub Actions)

```yaml
# Conteúdo do .github/workflows/devsecops.yml
# (incluir o conteúdo completo do arquivo aqui)
```

## 5. Pipeline Alternativo (GitLab CI)

```yaml
# Conteúdo do .gitlab-ci.yml
# (incluir o conteúdo completo do arquivo aqui)
```

## 6. Resultados

- Testes: [X] passando (coverage: Y%)
- Bandit: [X] issues encontradas
- Dependency-Check: [X] vulnerabilidades em dependências
- ZAP: [X] alertas (alto/médio/baixo)
- Docker: imagem de [X] MB

## 7. Lições Aprendidas

- A importância de integrar segurança desde o início do ciclo de desenvolvimento (Shift Left)
- Automação de testes de segurança no pipeline reduz riscos de deploy
- OWASP ZAP é eficaz para identificar vulnerabilidades web comuns
- Bandit ajuda a prevenir más práticas de segurança em Python
- Monitoramento contínuo com Fail2ban é simples e eficaz para brute force

## 8. Prints

[Lista de prints anexados:]
1. Tela inicial da aplicação
2. Dashboard com tarefas
3. Pipeline GitHub Actions executando
4. Relatório Bandit
5. Relatório Dependency-Check
6. Relatório ZAP
7. Logs de autenticação (syslog)
8. Fail2ban em ação (banimento)
