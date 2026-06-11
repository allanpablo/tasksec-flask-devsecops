# Como Executar o Projeto TaskSec

## Requisitos Mínimos
- Docker e Docker Compose
- Git
- 4 GB de RAM livres

## 1. Executar Localmente com Docker

```bash
# Construir e iniciar os containers
docker compose up -d --build

# Verificar se a aplicação está saudável
curl http://localhost:8080/health

# Acessar no navegador
open http://localhost:8080
```

## 2. Fluxo de Teste da Aplicação

1. Acessar http://localhost:8080
2. Criar conta (Registrar)
3. Fazer login
4. Criar tarefas
5. Editar e excluir tarefas
6. Testar login com senha errada para gerar logs de segurança

## 3. Executar Testes Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar testes
python -m pytest tests/ -v --cov=app
```

## 4. Executar Bandit (SAST)

```bash
pip install bandit
bandit -r app/ -c .bandit.yaml
```

## 5. Executar OWASP Dependency-Check

```bash
docker run --rm -v $(pwd):/scan owasp/dependency-check:latest \
  --scan /scan --project "tasksec" --format HTML --out /scan/reports/dependency-check
```

## 6. Executar OWASP ZAP (DAST)

Com a aplicação rodando em http://localhost:8080:

```bash
docker run --rm -v $(pwd)/reports:/zap/wrk \
  -p 8081:8080 --network host \
  zaproxy/zap-stable:latest \
  zap-baseline.py -t http://localhost:8080 \
  -J zap-report.json -w zap-report.md
```

## 7. Subir no GitHub

```bash
git init
git add .
git commit -m "Entrega TaskSec DevSecOps"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/tasksec_flask_devsecops.git
git push -u origin main
```

## 8. Pipeline no GitHub Actions

Após o push, acessar a aba **Actions** do repositório no GitHub.
O pipeline executa automaticamente: testes → Bandit → Dependency-Check → Docker build → ZAP DAST.

## 9. Estrutura de Diretórios

```
tasksec_flask_devsecops/
├── app/                  # Aplicação Flask
│   ├── __init__.py       # Factory + logging syslog
│   ├── models.py         # User + Task (SQLAlchemy)
│   ├── forms.py          # WTForms
│   ├── routes.py         # Blueprints (auth, main, task)
│   ├── utils.py          # Log de segurança
│   └── templates/        # HTML (Jinja2)
├── tests/                # Testes Pytest
├── fail2ban/             # Config monitoramento
├── docs/                 # Documentação
├── .github/workflows/    # Pipeline GitHub Actions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitlab-ci.yml        # Pipeline GitLab (alternativo)
```
