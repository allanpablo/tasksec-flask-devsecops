# Checklist de Prints para o Relatório Final

## Prints Obrigatórios

### 1. Aplicação Rodando
- [ ] Tela inicial (/) — TaskSec
- [ ] Tela de registro (/auth/register)
- [ ] Tela de login (/auth/login)
- [ ] Dashboard com tarefas criadas (/dashboard)
- [ ] Criação de tarefa (/task/create)
- [ ] Detalhe da tarefa (/task/<id>)
- [ ] Edição de tarefa (/task/<id>/edit)
- [ ] Healthcheck (/health) — JSON response

### 2. Pipeline GitHub Actions
- [ ] Visão geral do pipeline completo na aba Actions
- [ ] Stage de testes (pytest) passando
- [ ] Stage Bandit (SAST) executado
- [ ] Stage Dependency-Check executado
- [ ] Stage Docker Build executado
- [ ] Stage ZAP DAST executado
- [ ] Stage Deploy Stage executado
- [ ] Job detail mostrando logs de execução

### 3. Relatórios de Segurança
- [ ] Relatório Bandit (HTML) — visão geral
- [ ] Relatório Dependency-Check (HTML) — vulnerabilidades encontradas
- [ ] Relatório ZAP (JSON ou Markdown) — alertas

### 4. Logs e Monitoramento
- [ ] Log de autenticação bem-sucedida (syslog)
- [ ] Log de tentativa de login falha (syslog)
- [ ] Fail2ban — status de jail ativo (sudo fail2ban-client status tasksec)

### 5. Opcionais (Bônus)
- [ ] Logs do container Docker
- [ ] Cobertura de testes (HTML report)
- [ ] VPS da escola rodando aplicação (se aplicável)

## Como Capturar

```bash
# Logs da aplicação
docker logs tasksec-app

# Logs de autenticação
docker exec tasksec-syslog cat /var/log/messages

# Status do Fail2ban
sudo fail2ban-client status tasksec

# Healthcheck
curl http://localhost:8080/health | python3 -m json.tool
```
