# Test Execution Strategy

This document defines how the BugBank automated suite is organized and executed, separating **stable regression scenarios** from **known defect validation scenarios**.

The goal is to prevent a confirmed defect from either blocking the regression pipeline or being silently masked. Regression must stay meaningful (green because the business rules truly hold), while the known defect scenario must keep failing on purpose until the product is actually fixed.

## Suite Organization

### Regression Suite

Tag: `@regression`

Scenarios: TC_01 through TC_14, TC_16.

These scenarios validate stable, expected business behavior (registration, login, balance, statement, transfers, session integrity, financial reconciliation, data persistence). They must remain green. A failure here represents a real regression and must be investigated immediately.

### Quality Engineering Suite

Tag: `@quality_engineering`

Scenarios: TC_13, TC_14, TC_15, TC_16.

These scenarios go beyond happy-path automation, targeting financial reconciliation, session integrity, concurrency and data persistence. Most of them also belong to the regression suite because they currently pass; TC_15 is the exception, since it validates a confirmed, unresolved defect.

### Known Defect Validation Suite

Tags: `@known_defect`, `@bug001`, `@quality_engineering`

Scenario: TC_15 - Concurrent Transaction Assessment.

This scenario reproduces **BUG-001 - Duplicate Financial Operation on Concurrent Transfer Submission**. It is expected to **fail** until the defect is fixed by the development team. The scenario must not be skipped, weakened or bypassed — its failure is the evidence that the defect is still present.

## Execution Commands

Run only the regression suite:

```bash
python -m behave --tags=@regression
```

Run only the Quality Engineering suite:

```bash
python -m behave --tags=@quality_engineering
```

Run only the BUG-001 validation (expected to fail):

```bash
python -m behave --tags=@bug001
```

Run the entire suite:

```bash
python -m behave
```

## Rules

- BUG-001 must **not** be fixed as part of test maintenance.
- TC_15 must **not** have its assertions weakened, retried or skipped.
- A failing `@known_defect` result is a valid, expected outcome and must not be masked as a false positive.
- The regression suite (`@regression`) must remain green; any failure there is treated as a real regression, not as expected defect behavior.
