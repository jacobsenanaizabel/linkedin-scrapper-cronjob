# ⚡ QUICK START - LinkedIn Job Scraper

## 🎯 O QUE VAIS TER

✅ Scraper automático LinkedIn (GitHub Actions + Apify)  
✅ Executa a cada 3 dias automaticamente  
✅ ~200 vagas Senior/Staff Frontend por execução  
✅ Dados completos: empresa, recrutador, salário, descrição  
✅ Custo: **€0/mês** (free tier)  

---

## 📦 FICHEIROS INCLUÍDOS

```
github-actions-package/
├── SETUP_GUIDE.md                    ← COMECE AQUI (guia passo-a-passo)
├── README.md                         ← Documentação completa
├── config.json                       ← Configuração (edite as queries aqui)
├── linkedin-scraper.yml              ← Workflow básico
└── linkedin-scraper-advanced.yml     ← Workflow com download automático
```

---

## 🚀 SETUP RÁPIDO (15 min)

### 1️⃣ Criar conta GitHub (se não tiveres)
→ https://github.com/signup

### 2️⃣ Criar repositório
```
Nome: linkedin-job-scraper
Visibilidade: Public (recomendado)
✅ Add README
```

### 3️⃣ Adicionar Secret
```
Settings → Secrets → Actions → New repository secret

Nome: APIFY_TOKEN
Valor: YOUR_APIFY_TOKEN_HERE
```

### 4️⃣ Upload ficheiros

**Método A: Via interface GitHub**
1. Add file → Upload files
2. Arrasta os ficheiros:
   - Cria pasta `.github/workflows/`
   - Coloca lá os `.yml`
   - `config.json` na raiz

**Método B: Manual (mais preciso)**
1. Add file → Create new file
2. Nome: `.github/workflows/linkedin-scraper.yml`
3. Cola conteúdo do ficheiro
4. Commit
5. Repete para outros ficheiros

### 5️⃣ Testar

```
Actions → LinkedIn Job Scraper → Run workflow
```

Aguarda 3-5 min → Verifica resultados!

---

## 📊 ONDE VER RESULTADOS

### Opção 1: GitHub Artifacts (workflow avançado)
```
Actions → Execução mais recente → Scroll down → Artifacts
Download: jobs_latest.json + jobs_latest.csv
```

### Opção 2: Apify Console
```
https://console.apify.com/actors/runs
→ Último run → Dataset → Export
```

---

## ⚙️ PERSONALIZAR

### Mudar queries de pesquisa
Edita `config.json`:
```json
"searchQueries": [
    "Senior Frontend Engineer Madrid",  ← Edita
    "Staff Engineer React Spain"        ← Edita
]
```

### Mudar frequência
Edita `linkedin-scraper.yml`:
```yaml
cron: '0 9 */3 * *'   ← A cada 3 dias
      '0 9 * * 1'     ← Toda segunda
      '0 9 */7 * *'   ← A cada 7 dias
```

---

## 💰 CUSTOS

| Cenário | Jobs/mês | Custo |
|---------|----------|-------|
| **Atual** (4 queries × 50 jobs) | 600 | **€0** ✅ |
| Moderado (10 queries × 50 jobs) | 1.500 | €10-15 |
| Intensivo (10 queries × 100 jobs) | 3.000 | €20-30 |

**Free tier Apify:** $5/mês (~500 jobs)  
**Free tier GitHub:** 2.000 min/mês (sobra muito!)

---

## 🔔 PRÓXIMAS MELHORIAS (Opcional)

Depois de configurar, posso ajudar com:

1. **Email automático** quando encontrar vagas
2. **Google Sheets** integração (vagas vão direto para planilha)
3. **Filtro de consultorias** (blacklist automática)
4. **Dashboard** com estatísticas e gráficos
5. **Telegram bot** para receber notificações

---

## 🆘 AJUDA

### Problema comum: "Resource not accessible"
```
Settings → Actions → General
→ Workflow permissions
→ ✅ Read and write permissions
→ Save
```

### Scraper não executa automaticamente
```
Actions → Workflow → Lado direito verás "Next run: [data]"
Se não aparecer: reativa o workflow
```

### Resultados vazios
```
Queries muito específicas?
→ Alarga filtros em config.json
→ Muda timePosted para "pastWeek"
```

---

## 📚 DOCUMENTAÇÃO

- **Setup completo:** `SETUP_GUIDE.md` (passo-a-passo com screenshots mentais)
- **Documentação técnica:** `README.md` (tudo sobre o projeto)
- **Configuração:** `config.json` (edite queries aqui)

---

## ✅ CHECKLIST FINAL

Antes de terminar, verifica:

- [ ] Repositório criado no GitHub
- [ ] Secret `APIFY_TOKEN` adicionado
- [ ] Ficheiro `.github/workflows/linkedin-scraper.yml` criado
- [ ] Workflow executado manualmente 1x (teste)
- [ ] Resultados verificados (Artifacts ou Apify Console)
- [ ] Queries personalizadas em `config.json`
- [ ] Próxima execução agendada (visível em Actions)

---

## 🎉 PRONTO!

Agora tens um scraper automático de vagas do LinkedIn rodando 24/7 na cloud, de graça!

**Dúvidas?** Consulta `SETUP_GUIDE.md` ou pergunta! 😊

---

**Boa sorte na busca de emprego! 🚀**

P.S.: Quando conseguires a vaga, celebra comigo! 🎊
