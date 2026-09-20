# Testing & QA

## Strategy

- **Backend** — integration-style tests through the public API (`APITestCase`), not the internal service classes, so they survive refactors. Written test-first: one failing behaviour test, then the smallest change that makes it pass. CI gates on ruff, ruff format, a missing-migration check, tests with coverage at or above 80%, `check --deploy`, and mypy strict.
- **Mobile** — cubit tests for success, validation error and network failure, plus widget tests for the form. CI gates on `dart format`, `flutter analyze --fatal-infos`, and coverage at or above 25%.
- **UAT** — a manual pass on staging before 29 Sep, following the checklist in each task plan.

## Test Results by Sprint

| Sprint | Backend tests | Mobile tests | Coverage | UAT result |
|---|---|---|---|---|
| Sprint 1 | 47 passing (8 added for PIL-176) | not started | 88% backend | pending 29 Sep |

## Bugs Found

| ID | Description | Severity | Status |
|---|---|---|---|
| — | `saldo_setelah_transaksi` and the export's saldo column summed setoran only, so any setoran after a pencairan overstated the balance | High (found while building PIL-176, before pencairan shipped) | Fixed in [#19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) via a shared `BalanceService`, with regression tests |
