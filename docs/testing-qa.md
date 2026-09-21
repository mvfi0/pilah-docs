# Testing & QA

## Strategy

- **Backend** — integration-style tests through the public API (`APITestCase`), not the internal service classes, so they survive refactors. Written test-first: one failing behaviour test, then the smallest change that makes it pass. CI gates on ruff, ruff format, a missing-migration check, tests with coverage at or above 80%, `check --deploy`, and mypy strict.
- **Mobile** — cubit tests for success, validation error and network failure, plus widget tests for the form. CI gates on `dart format`, `flutter analyze --fatal-infos`, and coverage at or above 25%.
- **UAT** — a manual pass on staging before 29 Sep, following the checklist in each task plan.

## Test Results by Sprint

| Sprint | Backend tests | Mobile tests | Coverage | UAT result |
|---|---|---|---|---|
| Sprint 1 | 56 passing (11 added for PIL-176) | not started | 88% backend overall · 99.1% of PIL-176's new code | pending 29 Sep |

## Coverage Detail — Sprint 1

CI gates the **whole backend** at 80%. That figure mostly reflects pre-existing code, so the coverage of the lines a PR adds is measured separately.

### PIL-176 new code (PR #19): 99.1%

| File | New statements | Uncovered |
|---|---|---|
| `api/services.py` — service, `BalanceService`, export fix | 37 | 0 |
| `api/serializers.py` — validation, detail | 29 | 0 |
| `api/views.py` — `PencairanViewSet` | 24 | 1 |
| `api/models.py` — `Pencairan` | 22 | 0 |
| `api/admin.py`, `api/urls.py` | 2 | 0 |
| **Total** | **114** | **1** |

The one uncovered line is the non-paginated fallback in `PencairanViewSet.list`. It can never run, because pagination is on globally (`PAGE_SIZE: 20`); the pattern was copied from `TransaksiViewSet.list`, which has the same dead branch. Deleting it would bring new-code coverage to 100%.

### Whole backend: 88% (2,448 statements, 297 uncovered)

The uncovered 12% predates PIL-176:

| File | Coverage | Mostly untested |
|---|---|---|
| `management/commands/createsuperadmin.py` | 0% | CLI command, no tests |
| `management/commands/reset_testing_data.py` | 0% | CLI command, no tests |
| `api/validators.py` | 71% | phone-number edge cases |
| `api/views.py` | 74% | Google OAuth start/callback, error paths |
| `api/services.py` | 85% | WhatsApp/Twilio sending branches |

The two management commands at 0% are the cheapest wins for raising the overall number.

## Bugs Found

| ID | Description | Severity | Status |
|---|---|---|---|
| — | `saldo_setelah_transaksi` and the export's saldo column summed setoran only, so any setoran after a pencairan overstated the balance | High (found while building PIL-176, before pencairan shipped) | Fixed in [#19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) via a shared `BalanceService`, with regression tests |
| — | Pencairan accepted pending or rejected nasabah, while setoran requires an approved membership | Medium (code review, Heraldo) | Fixed in #19 |
| — | Setoran and pencairan with the same `tanggal` were ordered randomly in the export, so the saldo column was nondeterministic | Low (code review, Heraldo) | Fixed in #19 |
| — | Pencairan kept legacy sen in the saldo while #22's setoran rounds them away | Low (code review, Heraldo) | Fixed in #19; switch to `bulatkan_rupiah` after #22 merges |
