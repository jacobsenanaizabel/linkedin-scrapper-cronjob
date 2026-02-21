# 📝 GUIA PASSO-A-PASSO - SETUP COMPLETO

## ⏱️ Tempo estimado: 15-20 minutos

---

## 🎯 PASSO 1: CRIAR CONTA GITHUB (5 min)

### Se já tens conta GitHub → Pula para Passo 2

### Se NÃO tens conta:

1. **Vai a:** https://github.com/signup
2. **Preenche:**
   ```
   Email: jacobsenanaizabel@gmail.com
   Password: [escolhe uma senha forte]
   Username: anaizabeljacobsen (ou outro)
   ```
3. **Verifica o email** que GitHub enviar
4. **Login:** https://github.com/login

✅ **Pronto! Conta criada.**

---

## 🗂️ PASSO 2: CRIAR REPOSITÓRIO (3 min)

1. **Login no GitHub** → https://github.com

2. **Clica no botão `+`** (canto superior direito) → `New repository`

3. **Preenche o formulário:**
   ```
   Repository name: linkedin-job-scraper
   Description: Automated LinkedIn job scraper for Senior Frontend positions
   
   Visibilidade:
   ⚪ Public (RECOMENDADO - grátis, workflows ilimitados)
   ○ Private (também grátis, mas com limite de minutos)
   
   Inicialização:
   ✅ Add a README file
   ✅ Add .gitignore → seleciona "Python"
   ○ Choose a license (opcional)
   ```

4. **Clica** `Create repository` (botão verde)

✅ **Repositório criado!** URL será algo como:
```
https://github.com/anaizabeljacobsen/linkedin-job-scraper
```

---

## 🔐 PASSO 3: ADICIONAR APIFY TOKEN (2 min)

1. **No teu repositório**, clica no tab **Settings** (🔧)

2. **Menu lateral esquerdo** → **Secrets and variables** → **Actions**

3. **Clica** botão verde `New repository secret`

4. **Preenche:**
   ```
   Name: APIFY_TOKEN
   
   Secret: YOUR_APIFY_TOKEN_HERE
   ```

5. **Clica** `Add secret`

✅ **Secret configurado!** Aparecerá na lista como `APIFY_TOKEN`

---

## 📄 PASSO 4: ADICIONAR FICHEIROS (5 min)

Vais adicionar 3 ficheiros ao repositório:

### 4.1 Criar estrutura de pastas

1. **No repositório**, clica `Add file` → `Create new file`

2. **Nome do ficheiro:**
   ```
   .github/workflows/linkedin-scraper.yml
   ```
   
   ⚠️ **IMPORTANTE:** Escreve EXATAMENTE assim, com os `/`
   
   O GitHub vai criar automaticamente as pastas `.github` e `workflows`

3. **Cola o conteúdo:**
   - Abre o ficheiro `linkedin-scraper.yml` que te dei
   - Copia TODO o conteúdo
   - Cola na caixa de texto

4. **Scroll down** → Clica `Commit new file` (botão verde)

✅ **Workflow básico criado!**

---

### 4.2 (OPCIONAL) Adicionar workflow avançado

Se quiseres download automático dos resultados:

1. **Clica** `Add file` → `Create new file`

2. **Nome:**
   ```
   .github/workflows/linkedin-scraper-advanced.yml
   ```

3. **Cola o conteúdo** do ficheiro `linkedin-scraper-advanced.yml`

4. **Commit new file**

✅ **Workflow avançado criado!**

---

### 4.3 Adicionar ficheiro de configuração

1. **Clica** `Add file` → `Create new file`

2. **Nome:**
   ```
   config.json
   ```

3. **Cola o conteúdo** do ficheiro `config.json`

4. **Commit new file**

✅ **Configuração criada!**

---

## ✅ PASSO 5: ATIVAR GITHUB ACTIONS (1 min)

1. **Clica no tab** `Actions` (▶️)

2. Se aparecer mensagem de confirmação:
   - **Clica** `I understand my workflows, go ahead and enable them`

3. Verás a lista de workflows:
   - `LinkedIn Job Scraper` (básico)
   - `LinkedIn Scraper + Results Download` (avançado) - se criaste

✅ **Actions ativado!**

---

## 🚀 PASSO 6: TESTAR (PRIMEIRA EXECUÇÃO) (5 min)

Vamos executar manualmente para testar:

1. **No tab Actions**, clica em **`LinkedIn Job Scraper`** (ou o avançado)

2. **Lado direito**, clica botão `Run workflow`

3. **Dropdown** que aparece → **Branch: main** → Clica `Run workflow` (verde)

4. **Aguarda 5-10 segundos** → Refresh a página

5. Verás uma nova execução aparecer (bolinha amarela 🟡 = running)

6. **Clica na execução** para ver logs em tempo real

7. **Aguarda 3-5 minutos** → Status muda para ✅ (sucesso) ou ❌ (erro)

---

### 📊 Ver Resultados (se usaste workflow avançado):

1. **Scroll down** na página da execução

2. Secção **Artifacts** → Verás:
   ```
   📦 linkedin-jobs-[número]
   ```

3. **Clica** para fazer download (ZIP)

4. **Descompacta** → Terás:
   - `jobs_latest.json` - Dados completos
   - `jobs_latest.csv` - Para Excel
   - `summary.json` - Estatísticas

---

### 🔗 Ver Resultados na Apify Console:

1. **Nos logs** da execução, procura:
   ```
   📊 Monitor: https://console.apify.com/actors/runs/[ID]
   ```

2. **Clica no link** → Abre Apify Console

3. **Dataset** tab → **Export** → Escolhe formato

✅ **Primeira execução concluída!**

---

## 🔄 PASSO 7: CONFIGURAR EXECUÇÃO AUTOMÁTICA

Já está configurado! 🎉

O workflow vai executar **automaticamente**:
- ⏰ **Quando:** A cada 3 dias
- 🕐 **Hora:** 09:00 UTC (10:00 em Portugal)
- 🤖 **Sem fazer nada**

Para **verificar próxima execução**:
1. Tab **Actions**
2. Workflow → Lado direito verás "Next run: [data/hora]"

---

## ⚙️ PASSO 8: PERSONALIZAR (OPCIONAL)

### Alterar as queries de pesquisa:

**Opção A: Editar config.json**

1. No repositório, clica em `config.json`
2. Clica no ✏️ (Edit this file)
3. Altera as queries:
   ```json
   "searchQueries": [
       "Senior Frontend Engineer Madrid",  ← Edita aqui
       "Tua query aqui",                   ← Adiciona mais
   ]
   ```
4. **Commit changes**

**Opção B: Editar workflow diretamente**

1. `.github/workflows/linkedin-scraper.yml`
2. Editar → Procura `searchQueries`
3. Altera
4. Commit

---

### Alterar frequência:

1. Edita `.github/workflows/linkedin-scraper.yml`
2. Procura linha:
   ```yaml
   cron: '0 9 */3 * *'
   ```
3. Altera para:
   - `'0 9 * * 1'` - Todas as segundas
   - `'0 9 */7 * *'` - A cada 7 dias
   - `'0 9 1 * *'` - Dia 1 do mês

Use: https://crontab.guru para ajudar

---

## 🎉 CONCLUÍDO!

Tudo configurado! Agora:

✅ Scraper roda automaticamente a cada 3 dias  
✅ Podes executar manualmente quando quiseres  
✅ Resultados ficam disponíveis por 90 dias  
✅ Custo: €0/mês (free tier)  

---

## 📧 PRÓXIMOS PASSOS (OPCIONAL)

Quer receber notificações por email? Consulta o README.md secção "Notificações"

Quer integrar com Google Sheets? Posso ajudar!

Quer filtrar consultorias? Edita `excludeKeywords` no config.json

---

## 🐛 PROBLEMAS?

### Workflow não aparece em Actions
→ Verifica se criaste o ficheiro no caminho correto:
   `.github/workflows/linkedin-scraper.yml`

### "Resource not accessible by integration"
→ Settings → Actions → General → Workflow permissions → Read and write

### Scraper falha
→ Verifica:
1. Secret `APIFY_TOKEN` está correto?
2. Tem crédito na Apify? https://console.apify.com/billing

### Dúvidas?
→ Envia mensagem! 😊

---

**Boa sorte na busca de emprego! 🚀**
