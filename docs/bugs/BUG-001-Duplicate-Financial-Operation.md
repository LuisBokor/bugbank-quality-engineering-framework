# BUG-001 — Duplicate Financial Operation on Rapid Transfer Confirmation

## Identification

| Field | Value |
|-------|-------|
| Defect ID | BUG-001 |
| Title | Duplicate financial operations when the transfer confirmation is triggered multiple times in rapid succession |
| Reported by | Quality Engineering (automated assessment) |
| Date | 2026-09-21 |
| Environment | bugbank.netlify.app / Microsoft Edge (Chromium) / viewport 1440x900 |
| Severity | Critical |
| Priority | P1 |
| Status | New |

## Related Test Case

| Field | Value |
|-------|-------|
| Feature | features/quality_engineering.feature |
| Scenario | TC_15 - Concurrent Transaction Assessment |
| QE Initiative | QE-03 - Concurrent Transaction Assessment |

## Preconditions

- Sender account exists with initial balance (observed: R$ 1.000,00).
- Receiver account exists without initial balance.
- Sender is authenticated and on the transfer screen with a valid transfer of R$ 50,00 filled in (description `QE-03 Concorrencia`).

## Steps to Reproduce

1. Login with the sender account.
2. Open the transfer functionality and fill in a valid receiver account, value R$ 50,00 and a description.
3. Trigger the "Transferir agora" confirmation 5 times in rapid succession (including activations dispatched while the success modal overlay intercepts pointer events).
4. Return to the home screen and check the sender balance.
5. Open the sender statement and count the entries for the operation.

## Expected Result

- Exactly one debit of R$ 50,00 on the sender account.
- Sender final balance: R$ 950,00 (initial 1.000,00 − 50,00).
- Exactly one credit of R$ 50,00 on the receiver account.
- Exactly one statement entry per account for the operation.
- Repeated confirmation attempts are deduplicated (idempotent submission) or blocked while a transaction is in progress.

## Actual Result

- Sender final balance: **R$ 750,00** — five debits of R$ 50,00 were applied instead of one.
- Failure diagnostic produced by the automated scenario:

  `[DEFEITO QE-01] remetente_saldo_final | saldo final 750.00 diverge do esperado 950.00 (inicial 1000.00, 1 débito de 50,00). Indício de débito duplicado ou débito ausente após 5 tentativas`

## Root Cause Analysis

The transfer submission flow has no idempotency or concurrency guard:

- The success modal (`div.styles__Container-sc-8zteav-0`) overlays the form after the first submission, intercepting pointer events — real mouse clicks on the button are then physically blocked.
- However, the click handler bound to the "Transferir agora" button still executes when activated programmatically through the overlay (e.g., dispatched DOM events, keyboard activation, or rapid clicks landing before the overlay renders).
- Each activation creates an independent financial transaction: the balance is debited and a statement entry is appended per activation. There is no transaction token, request deduplication, or in-flight submission lock.

The timeout observed during test development (Locator.click intercepted by the overlay) was a testability limitation of the interaction layer, not product behavior; dispatching the activation events exposed the underlying product defect.

## Business Impact

- **Financial integrity**: multiple debits for a single intended transfer; customer funds are moved without consent.
- **Reconciliation**: sender/receiver balances and statement entries diverge from user intent, corrupting audit trails.
- **Reversibility**: BugBank offers no built-in reversal flow; each duplicate transfer requires manual correction.
- **Trust**: a balance-changing action that can be repeated by rapid interaction is a high-severity defect for any banking-like product.

## Evidence Collected

| Artifact | Location |
|----------|----------|
| Failure screenshot (balance assertion) | evidencias/geral/TC_15/falha_o_saldo_do_remetente_dever_ter_sido_debitado_exatamente_uma.png |
| Final state screenshot | evidencias/geral/TC_15/failed.png |
| Filled form screenshot | evidencias/geral/TC_15/02_preencher_uma_transfer_ncia_v_lida_de_50_reais.png |
| Per-step screenshots | evidencias/geral/TC_15/02_*.png |
| Page HTML at failure | evidencias/geral/TC_15/page.html |
| Stacktrace / failure reason | evidencias/geral/TC_15/stacktrace.log |
| Browser console log | evidencias/geral/TC_15/console.log |
| Network capture | evidencias/geral/TC_15/network.json |
| Execution video | videos/TC_15_-_Concurrent_Transaction_Assessment/ |
| Execution report | reports/json/execution_results.json |

## Quality Engineering Notes

- Defect discovered by automated assessment; no retries, workarounds, or weakened assertions were used. The scenario fails deterministically on the first business validation.
- The defect was **not** fixed; this document only records it. The failing scenario should remain red until the product is corrected.
- Suggested product-side remediation (for the development team, out of QE scope): disable the confirmation button while a submission is in flight, deduplicate submissions by transaction token, and ignore activations while the result modal is open.
- Recommended regression coverage after a fix: re-run TC_15 and confirm sender final balance equals initial − 50,00, receiver equals +50,00, and each statement holds exactly one entry.
- Related initiatives: QE-01 (Financial Reconciliation) may surface the same duplication as cross-account divergence; QE-05 (Defect Documentation Framework) is satisfied by this report.
