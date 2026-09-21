# Defect Report

## Identification

| Field | Value |
|-------|-------|
| Defect ID | BUG-YYYY-NNN |
| Title | Short and objective defect description |
| Reported by | QA Engineer name |
| Date | YYYY-MM-DD |
| Environment | bugbank.netlify.app / browser / viewport |
| Build / Version | Commit hash or release identifier |
| Severity | Critical / High / Medium / Low |
| Priority | P1 / P2 / P3 / P4 |
| Status | New / Triaged / In Progress / Fixed / Retested / Closed |

## Business Impact

Describe how the defect affects business rules, financial integrity, user trust or regulatory concerns.

## Related Test Case

| Field | Value |
|-------|-------|
| Feature | e.g. features/quality_engineering.feature |
| Scenario | e.g. TC_14 - Session Integrity Assessment |
| QE Initiative | QE-01 / QE-02 / QE-03 / QE-04 / QE-05 |

## Preconditions

- Test data, account state and configuration required before execution.

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Expected Result

Behavior defined by business rules and acceptance criteria.

## Actual Result

Observed behavior, including messages, values and navigation outcomes.

## Evidence

- [ ] Screenshots (evidencias/<scenario>/)
- [ ] Video (videos/<scenario>/)
- [ ] Execution logs (logs/<scenario>/)
- [ ] Network capture (logs/network.json)
- [ ] HTML capture (reports/html/)
- [ ] Dashboard record (reports/dashboard/)

## Root Cause Analysis

Technical hypothesis for the failure (session handling, state persistence, race condition, etc.).

## Reproducibility

| Field | Value |
|-------|-------|
| Frequency | Always / Intermittent / Rare |
| Retry affected result? | Yes / No |
| False positive ruled out? | Yes / No — justification |

## Suggested Fix

Recommended correction and areas to regression test.

## Notes

Additional observations, related defects and references.
