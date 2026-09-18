## Results

Latest full execution:

- Features: 4
- Scenarios: 12
- Steps: 81
- Passed: 12
- Failed: 0
- Success Rate: 100%
- Average Duration: 12.08s
- Total Duration: 386.08s
- Quality Score: 100 (Excellent)

Artifacts generated during execution:

- Executive Dashboard
- Executive Report
- Detailed Report
- JSON Report
- CSV Export
- XLSX Export
- Videos
- Screenshots
- Execution Logs
- HTML Capture

## Executive Dashboard

The framework automatically generates an Executive Dashboard designed for QA Managers, Tech Leads and stakeholders.

<<<<<<< HEAD
Dashboard capabilities:

- Quality Score calculation
- Pass × Fail visualization
- Functional coverage analysis
- Execution time metrics
- Scenario drill-down
- Screenshot gallery
- Video playback
- Execution logs
- Test data inspection
- HTML capture access

> Add screenshots of the dashboard below.

### Dashboard Preview

docs/images/dashboard.png

### Executive Report

docs/images/executive-report.png

### Detailed Report

docs/images/detailed-report.png

## False Positive Assessment
=======
```mermaid
flowchart LR
    F[features/*.feature] --> S[steps/*_steps.py]
    S --> P[pages/*_page.py]
    P --> PW[Playwright]
    H[environment.py hooks]*--> R[utils/observability.py<br/>ScenarioRecorder]
    H --> K[utils/evidence_packager.py<br/>consolidação de artefatos]
    R --> E[evidencias/]
    R --> L[logs/]
    K -->*V[videos/<cenário>/]
    H --> G[generate_reports]
    G --> RP[reports/<br/>dashboard, html, json, csv, xlsx, graphs]
```

## Casos de tes*e (12 cenários)

| ID | Cenário | *uncionalidade |
|---|---|---|
| TC*01 | Criar Conta | Cadastro |
| TC*02 | Acessar a Conta | Login |
| T*_03 | Criar Conta com Saldo Inicia* | Cadastro |
| TC_04 | Validar Ca*pos Obrigatórios do Cadastro | Cad*stro |
| TC_05 | Cadastrar Conta c*m E-mail Já Utilizado | Cadastro |*| TC_06 | Cadastrar Conta com Conf*rmação de Senha Divergente | Cadas*ro |
| TC_07 | Realizar Login com *enha Inválida | Login |
| TC_08 | *ealizar Logout da Aplicação | Logi* |
| TC_09 | Consultar Saldo da Co*ta | Extrato |
| TC_10 | Realizar *ransferência sem Saldo Suficiente * Transferência |
| TC_11 | Fluxo E*E de Cadastro, Login e Transferênc*a entre Contas | E2E |
| TC_12 | F*uxo E2E Completo de Transferência,*Extrato, Saldo e Logout | E2E |

#* Evidências por cenário

Cada cená*io gera automaticamente:

- **Scre*nshots**: `01_inicio.png` (início)* `02_<step>.png` (antes de cada aç*o), `03_sucesso.png` ou `failed.pn*` (final).
- **Vídeo**: consolidad* em `videos/<cenário>/video.webm`.*- **Logs**: `execution.log` (metad*dos + console do navegador), `cons*le.log`, `network.json`.
- **Massa*de teste**: `test_data.json` (cont* gerada via Faker, senha mascarada*.
- **HTML**: `html/page_source.ht*l` (DOM final da página).
- Em fal*as: `page.html` e `stacktrace.log`*na pasta de evidências.

## Dashbo*rd e relatórios

| Artefato | Desc*ição |
|---|---|
| reports/dashboa*d/index.html | Dashboard executivo* KPIs, Quality Score, gráficos Plo*ly e galeria por cenário (vídeo, s*reenshots, logs, massa, HTML) |
| *eports/html/executive_report.html * Resumo executivo com KPIs e gráfi*o Pass × Fail |
| reports/html/det*iled_report.html | Detalhe por cen*rio: ID, nome, funcionalidade, sta*us, tempo, data, evidências, vídeo* logs, massa |
| reports/json/exec*tion_results.json | Resultado estr*turado da execução |
| reports/jso*/execution_history.json | Históric* das últimas 20 execuções |
| repo*ts/csv/execution_results.csv | Exp*rtação CSV |
| reports/xlsx/execut*on_results.xlsx | Exportação Excel*(Resumo + Cenários) |
| reports/gr*phs/ | Gráficos Plotly: pass/fail,*cobertura por funcionalidade, temp* por cenário, histórico |

## Resu*ts

Latest full execution:

- Feat*res: 4
- Scenarios: 12
- Steps: 81*- Passed: 12
- Failed: 0
- Success*Rate: 100%
- Average Duration: 12.*8s
- Total Duration: 386.08s
- Qua*ity Score: 100 (Excellent)

Artifa*ts generated during execution:

- *xecutive Dashboard
- Executive Rep*rt
- Detailed Report
- JSON Report*- CSV Export
- XLSX Export
- Video*
- Screenshots
- Execution Logs
- *TML Capture

## Executive Dashboar*

The framework automatically gene*ates an Executive Dashboard design*d for QA Managers, Tech Leads and *takeholders.

Dashboard capabiliti*s:

- Quality Score calculation
- *ass × Fail visualization
- Functio*al coverage analysis
- Execution t*me metrics
- Scenario drill-down
-*Screenshot gallery
- Video playbac*
- Execution logs
- Test data insp*ction
- HTML capture access

### D*shboard Preview

> Add dashboard s*reenshot here

### Executive Repor*

> Add executive report screensho* here

### Detailed Report

> Add *etailed report screenshot here

##* Quality Score

`score = taxa_de_s*cesso - min(10, falhas × 2)`, clas*ificado como **Excellent** (≥90), **Good** (≥75), **Fair** (≥50) ou **Poor** (<50).
>>>>>>> 8c8b45a (docs: improve README with results, dashboard and quality engineering assessment)

BugBank is intentionally designed as a QA training application containing known defects and unexpected behaviors.

<<<<<<< HEAD
Although the automated suite achieved a 100% success rate during the latest execution, an additional validation phase was identified as necessary to evaluate:
=======
`*`powershell
py -m venv .env
.\.env*Scripts\Activate.ps1
python -m pip*install -r requirements.txt
python*-m playwright install msedge
behav*
```
>>>>>>> 8c8b45a (docs: improve README with results, dashboard and quality engineering assessment)

- Assertion strength
- Business rule coverage
- Potential false positives
- Reliability of automated validations
- Effects of retry mechanisms on defect detection

<<<<<<< HEAD
This initiative reflects a Quality Engineering mindset where a fully green test suite is not automatically interpreted as a 
=======
```power*hell
$env:HEADLESS='1'
behave
```
*Variáveis de ambiente: `HEADLESS` *0/1), `BROWSER_CHANNEL` (padrão `m*edge`), `TEST_ENVIRONMENT` (rótulo*exibido nos relatórios).

## Estru*ura de diretórios

```text
BugBank*
├── features/          # Gherkin *cadastro, login, transferência, ex*rato)
├── steps/             # Ste* definitions Behave
├── pages/    *        # Page Objects (base, cada*tro, login, home, transferência, e*trato)
├── utils/             # ob*ervability, evidence_packager, log*er, screenshot_manager,
│         *            # account_context, fak*r_utils
├── evidencias/        # s*reenshots, console, network por ce*ário
├── videos/            # vide*.webm + screenshots/ + html/ + exe*ution.log + test_data.json
├── log*/              # logs técnicos da *xecução
├── reports/           # d*shboard, html, json, csv, xlsx, gr*phs, logs
├── environment.py     #*hooks Behave
└── playwright.config*py
```

## Diferenciais técnicos

* **Observabilidade completa**: con*ole, pageerror, network e screensh*ts capturados por listeners do Pla*wright, sem poluir steps.
- **Cons*lidação de artefatos**: `evidence_*ackager` organiza vídeo, screensho*s, logs, massa e HTML por cenário *ia `pathlib`/`shutil`, isolado por*try/except (nunca quebra a suíte).*- **Massa isolada e rastreável**: *ada cenário usa conta Faker própri*, persistida em `test_data.json` c*m senha mascarada.
- **Reporting e* camadas**: JSON/CSV/XLSX para int*gração, HTML detalhado para QA, da*hboard executivo para gestão.
- ***lean Code/SOLID**: responsabilidad*s separadas entre hooks, recorder,*packager e geradores de relatório;*hooks reutilizados sem alterar tes*es.

## False Positive Assessment
*BugBank is intentionally designed *s a QA training application containing known defects and unexpected behaviors.

Although the automated suite achieved a 100% success rate during the latest execution, an additional validation phase was identified as necessary to evaluate:

- Assertion strength
- Business rule coverage
- Potential false positives
- Reliability of automated validations
- Effects of retry mechanisms on defect detection

This initiative reflects a Quality Engineering mindset where a fully green test suite is not automatically interpreted as a defect-free application.

Future work includes:

- Strengthening scenario assertions
- Expanding business-rule validations
- Reviewing retry strategies
- Investigating false positives
- Increasing confidence in automated outcomes

## Future Improvements

Planned next steps:

- CI/CD integration with GitHub Actions
- Automated execution scheduling
- Historical trend analysis
- Test result notifications
- Enhanced dashboard filtering
- Defect correlation metrics
- False positive assessment initiative
- Expanded reporting capabilities
>>>>>>> 8c8b45a (docs: improve README with results, dashboard and quality engineering assessment)
