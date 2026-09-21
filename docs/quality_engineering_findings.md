# Quality Engineering Findings

**Date:** 2026-09-21
**Scope:** BugBank Quality Engineering assessment (features/quality_engineering.feature)

## Scenarios Reviewed

| Scenario | Initiative | Status | Result |
|----------|-----------|--------|--------|
| TC_13 - Financial Reconciliation Assessment | QE-01 | Implemented | Cross-account reconciliation: A (−300), B (+300 −100), C (+100); statement entries validated per account; global invariant `InitialTotal == FinalTotal` asserted |
| TC_14 - Session Integrity Assessment | QE-02 | Implemented | Logout, browser back, page refresh and direct URL access validated; protected content and login form asserted with auto-wait; per-checkpoint screenshots |
| TC_15 - Concurrent Transaction Assessment | QE-03 | **Defect found** | 5 rapid transfer confirmations produced 5 debits of R$ 50,00 (balance 1.000,00 → 750,00); deterministic failure on business validation |
| TC_16 - Data Persistence Assessment | QE-04 | Implemented | Balance and statement snapshots compared before/after logout and re-login; description + value + occurrence-count assertions; home × statement balance cross-check |

## Findings

### BUG-001 — Duplicate Financial Operation on Rapid Transfer Confirmation

- **Severity:** Critical | **Priority:** P1
- **Initiative:** QE-03 (Concurrent Transaction Assessment)
- **Symptom:** 5 rapid confirmations of a single R$ 50,00 transfer produced 5 debits; sender balance ended at R$ 750,00 instead of R$ 950,00.
- **Root cause:** no idempotency, transaction token, or in-flight submission lock on the transfer handler; the success modal overlay intercepts pointer events but does not prevent repeated activations of the button handler.
- **Report:** [BUG-001-Duplicate-Financial-Operation.md](bugs/BUG-001-Duplicate-Financial-Operation.md)
- **Evidence:** evidencias/geral/TC_15 (screenshots per step, failure capture, page.html, stacktrace.log, console.log, network.json), video recording, execution reports.

## Metrics

| Metric | Value |
|--------|-------|
| Detected Defects | 1 |
| Critical Defects | 1 |
| High Defects | 0 |
| Medium/Low Defects | 0 |
| Scenarios with business-level assertions | 4/4 |

## False Positives Eliminated

| Practice | Where applied |
|----------|---------------|
| Replaced immediate `is_visible()` checks with auto-waiting assertions (`expect().not_to_be_visible()`) to avoid false "blocked" results while DOM loads after back/refresh | TC_14 |
| Statement validation keyed on unique operation descriptions (`QE-01 A para B`, `QE-03 Concorrencia`, `QE-04 Data Persistence`) instead of the generic word "Transfer", which also matches menu labels | TC_13, TC_15, TC_16 |
| Occurrence-count assertions on statement entries (exactly 1) instead of substring presence, detecting both missing and duplicated entries | TC_13, TC_15, TC_16 |
| Numeric balance parsing (`R$ 1.000,00` → float) with exact expected-value comparison instead of visibility-only checks | TC_13, TC_15, TC_16 |
| Guard `initial_balance > 0` before validating debits, preventing a zero-balance account from silently passing debit assertions | TC_15, TC_16 |
| Cross-check between home balance and statement "Saldo disponível" to rule out cached or divergent UI values | TC_16 |
| Testability fix separated from product behavior: overlay interception resolved via DOM event dispatch, preserving real handler execution — confirmed the failure is a product defect, not a test artifact | TC_15 |

## Business Assertions Added

- Per-account final balance equals initial ± exact transferred amounts (TC_13).
- Statement contains exactly one debit/credit per operation, with value and description verified (TC_13, TC_15, TC_16).
- Global financial reconciliation: sum of initial balances equals sum of final balances across accounts A, B, C (TC_13).
- Session termination blocks protected content after logout, back navigation, refresh and direct URL access (TC_14).
- Login form is displayed whenever protected access is denied (TC_14).
- Balance updated exactly once after concurrent confirmation attempts (TC_15).
- No duplicate financial operation across sender and receiver ledgers (TC_15).
- Balance and statement entries preserved across logout and re-login, including entry-count equality to detect loss or duplication (TC_16).
- Home balance reconciles with statement available balance before and after re-login (TC_16).

## Quality Engineering Conclusions

1. **The assessment model works as intended.** A green functional suite (12/12 passing) coexisted with a critical financial-integrity defect; the QE scenarios exposed it on the first concurrency evaluation.
2. **The most valuable defect class for this product is financial**, not visual or navigational. Assertions were deliberately weighted toward balances, ledger entries and reconciliation rather than success messages.
3. **Success modals are not proof of correctness.** All QE scenarios validate persisted state (balance + statement) instead of transient UI feedback.
4. **BUG-001 should remain reproducible until fixed.** TC_15 fails deterministically and requires no retries or weakened assertions; its failure signature (balance delta + entry count) is unambiguous for triage.
5. **Evidence discipline is in place.** Every failure captures screenshots, page HTML, console and network logs, and is packaged per scenario, enabling defect documentation without re-execution.
6. **Next candidates:** extending QE-03 to receiver-side duplication evidence within the same run, and QE-05 consolidation of additional defect reports as new initiatives uncover them.

No defects were fixed. This document records findings only.
