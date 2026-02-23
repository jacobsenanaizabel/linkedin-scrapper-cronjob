# 🤖 LinkedIn Job Scraper - Automated

Scraper automático de vagas no LinkedIn usando GitHub Actions + Apify.

## 🎯 O que faz

- ✅ Executa **automaticamente a cada 3 dias**
- ✅ Procura vagas Senior/Staff Frontend Engineer em Madrid/Remoto
- ✅ Extrai ~200 vagas por execução
- ✅ Inclui detalhes da empresa + info dos recrutadores
- ✅ Gera JSON + CSV para download
- ✅ **Custo: €0** (dentro do free tier da Apify)

## 📋 Setup Inicial

### 1. Fork/Clone este repo

```bash
# Se ainda não fizeste:
# 1. Cria conta no GitHub
# 2. Cria novo repo "linkedin-job-scraper"
# 3. Adiciona estes ficheiros
```

### 2. Configurar Apify Token

1. Vai a **Settings** → **Secrets and variables** → **Actions**
2. Clica **New repository secret**
3. Nome: `APIFY_TOKEN`
4. Valor: `YOUR_APIFY_TOKEN_HERE`
5. **Add secret**

### 3. Ativar GitHub Actions

1. Vai ao tab **Actions**
2. Se pedir, clica **I understand my workflows, go ahead and enable them**

## 🚀 Como Usar

### Execução Automática

O scraper roda **automaticamente**:
- **Frequência:** A cada 3 dias
- **Hora:** 09:00 UTC (10:00 em Portugal)
- **Sem fazer nada!**

### Execução Manual

Para executar agora (sem esperar 3 dias):

1. Vai ao tab **Actions**
2. Clica no workflow **"LinkedIn Job Scraper"**
3. Clica **Run workflow** → **Run workflow**
4. Aguarda 3-5 minutos

## 📥 Como Obter os Resultados

### Opção 1: Via GitHub (Recomendado)

**Para o workflow avançado** (`linkedin-scraper-advanced.yml`):

1. Vai ao tab **Actions**
2. Clica na execução mais recente
3. Scroll down até **Artifacts**
4. Download:
   - `jobs_latest.json` - Dados completos
   - `jobs_latest.csv` - Para Excel/Sheets
   - `summary.json` - Estatísticas rápidas

**Ficheiros expiram em 90 dias**

### Opção 2: Via Apify Console

1. Vai a https://console.apify.com/actors/runs
2. Procura pelo run mais recente
3. **Dataset** → **Export** → JSON/CSV/Excel

## ⚙️ Configuração

### Alterar Queries de Pesquisa

Edita o ficheiro `.github/workflows/linkedin-scraper.yml`:

```python
"searchQueries": [
    "Senior Frontend Engineer Madrid",      # ← Edita aqui
    "Staff Engineer React Spain Remote",    # ← Edita aqui
    "Frontend Lead Next.js Madrid",         # ← Edita aqui
    "Full Stack Engineer Node.js Madrid"    # ← Edita aqui
],
```

### Alterar Frequência

No mesmo ficheiro, muda o cron:

```yaml
schedule:
  - cron: '0 9 */4 * *'  # A cada 4 dias às 09:00 UTC
```

Exemplos:
- `'0 9 * * 1'` - Todas as segundas às 09:00
- `'0 9 */7 * *'` - A cada 7 dias às 09:00
- `'0 9 1 * *'` - Dia 1 de cada mês às 09:00

**Calculadora de Cron:** https://crontab.guru

### Alterar Número de Resultados

```python
"maxResults": 50,  # ← 50 jobs por query
```

**Atenção:** 
- Mais resultados = mais custo
- Free tier: ~500 jobs/mês
- 4 queries × 50 jobs = 200 total (OK para free tier)

### Alterar Filtros

```python
"filters": {
    "timePosted": "past24Hours",           # past24Hours, pastWeek, pastMonth
    "experienceLevel": ["MID_SENIOR", "DIRECTOR"],  # ENTRY_LEVEL, ASSOCIATE, etc.
    "jobType": ["FULL_TIME"],              # PART_TIME, CONTRACT, TEMPORARY, INTERNSHIP
    "remote": ["REMOTE", "HYBRID"]         # ON_SITE, REMOTE, HYBRID
}
```

## 📊 Custos

### Free Tier (Atual)

- **Apify:** $5 crédito/mês
- **GitHub Actions:** 2.000 min/mês
- **Configuração atual:** ~500 jobs/mês
- **Custo:** **€0/mês** ✅

### Se Ultrapassar Free Tier

Se quiseres mais resultados:

| Jobs/mês | Custo Apify |
|----------|-------------|
| 500 | €0 (free) |
| 1.000 | €10-15 |
| 2.000 | €20-30 |

## 🔔 Notificações

### Receber Email quando executar

Adiciona no final do workflow:

```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.GMAIL_USER }}
    password: ${{ secrets.GMAIL_PASSWORD }}
    subject: 🎯 LinkedIn Jobs - New Results
    body: Check GitHub Actions for results!
    to: jacobsenanaizabel@gmail.com
```

**Secrets necessários:**
- `GMAIL_USER`: teu Gmail
- `GMAIL_PASSWORD`: App Password do Gmail

## 📚 Estrutura dos Ficheiros

```
linkedin-job-scraper/
├── .github/
│   └── workflows/
│       ├── linkedin-scraper.yml           # Workflow básico
│       └── linkedin-scraper-advanced.yml  # Com download automático
├── README.md                              # Este ficheiro
└── jobs_latest.json                       # Gerado automaticamente
```

## 🐛 Troubleshooting

### Workflow não executa automaticamente

1. Vai a **Settings** → **Actions** → **General**
2. Scroll down até **Workflow permissions**
3. Ativa **Read and write permissions**
4. **Save**

### "Resource not accessible by integration"

Mesmo que acima - permissões insuficientes.

### Scraper falha

Verifica:
1. Apify token está correto?
2. Tens crédito suficiente? (https://console.apify.com/billing)
3. Query syntax está correta?

### Resultados vazios

Possíveis causas:
- Queries muito específicas
- Filtros muito restritivos
- Período de tempo muito curto (`past24Hours`)

**Solução:** Alarga os filtros ou muda `timePosted` para `pastWeek`.

## 📖 Links Úteis

- **Apify Console:** https://console.apify.com
- **GitHub Actions Logs:** https://github.com/SEU-USERNAME/linkedin-job-scraper/actions
- **Apify Scraper Docs:** https://apify.com/curious_coder/linkedin-jobs-scraper
- **Cron Calculator:** https://crontab.guru

## 💡 Próximos Passos

Depois de configurar, podes:

1. **Integrar com Google Sheets** (via Google Apps Script)
2. **Filtrar por empresa** (adicionar blacklist de consultorias)
3. **Email automático** com vagas novas
4. **Dashboard** com estatísticas


**Feito com ❤️ para automatizar a busca de emprego**
