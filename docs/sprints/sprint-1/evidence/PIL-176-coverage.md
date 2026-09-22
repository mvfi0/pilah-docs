# PIL-176 — Coverage of My Changes

Coverage evidence for the backend of [PIL-176](https://linear.app/pilah-2/issue/PIL-176) (pencatatan pencairan), delivered in [pilah-be PR #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19).

| Scope | Statements | Covered | Coverage |
|---|---|---|---|
| **Lines I added or changed** (application code) | **111** | **111** | **100%** |
| Whole backend, for context | 2,706 | 2,426 | 90% |

The 100% applies to my changes only. The rest of the backend is at 90%; its uncovered lines predate PIL-176 and were written by other team members (see [Cross-check with SonarQube](#cross-check-with-sonarqube)).

Measured on commit [`ad7d55f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ad7d55f0aa63ef783f16f1e36294f000330575dd), 22 Sep 2026.

## My lines, file by file

Each range links to the exact lines on GitHub at `ad7d55f`. "Statements" counts executable lines only; blank lines, comments and signatures that coverage does not track are excluded.

| File | My lines | What they are | Statements | Covered |
|---|---|---|---|---|
| `api/models.py` | [331–364](https://github.com/bank-sampah-PILAH/pilah-be/blob/ad7d55f0aa63ef783f16f1e36294f000330575dd/api/models.py#L331-L364) | `Pencairan` model | 22 | 22 |
| `api/services.py` | [404–469](https://github.com/bank-sampah-PILAH/pilah-be/blob/ad7d55f0aa63ef783f16f1e36294f000330575dd/api/services.py#L404-L469) | `BalanceService`, `PencairanService` | 37 | 37 |
| | [936–958](https://github.com/bank-sampah-PILAH/pilah-be/blob/ad7d55f0aa63ef783f16f1e36294f000330575dd/api/services.py#L936-L958) | Excel export: merge pencairan into the running saldo | | |
| | 6, 14, 33 | imports | | |
| `api/serializers.py` | [29–77](https://github.com/bank-sampah-PILAH/pilah-be/blob/ad7d55f0aa63ef783f16f1e36294f000330575dd/api/serializers.py#L29-L77) | `PencairanCreateSerializer`, `PencairanDetailSerializer` | 29 | 29 |
| | [511](https://github.com/bank-sampah-PILAH/pilah-be/blob/ad7d55f0aa63ef783f16f1e36294f000330575dd/api/serializers.py#L511) | `saldo_setelah_transaksi` now uses `BalanceService` | | |
| | 2, 8, 20, 25 | imports | | |
| `api/views.py` | [587–614](https://github.com/bank-sampah-PILAH/pilah-be/blob/ad7d55f0aa63ef783f16f1e36294f000330575dd/api/views.py#L587-L614) | `PencairanViewSet` (create, list, retrieve) | 20 | 20 |
| | 21, 37–38, 55 | imports | | |
| `api/admin.py` | 10, 79 | admin registration | 1 | 1 |
| `api/urls.py` | 18, 32 | `/api/v1/pencairan` route | 1 | 1 |
| `api/management/commands/reset_testing_data.py` | 6, 28 | reset also verifies `pencairan` is cleared | 1 | 1 |
| **Total** | | | **111** | **111** |

The migration `api/migrations/0012_pencairan.py` is also mine but is excluded, as migrations are generated code. Test code (`api/tests.py`) is excluded so that tests do not count as covering themselves.

## How it was measured

"My lines" are the lines changed between `origin/staging` and my branch (`git diff origin/staging...HEAD`), excluding tests and migrations. Their coverage was checked with two independent tools, which agree:

1. **[diff-cover](https://github.com/Bachmann1234/diff_cover)**: a standard tool that reports coverage on the lines of a diff only. Report: [pil-176-diff-coverage.html](pil-176-diff-coverage.html) (111 lines, 0 missing, 100%).
2. **coverage.py JSON + the diff**: executed and missing line numbers from `coverage json`, intersected with the diff's added lines. Same result: 111 of 111.

To reproduce, from the `pilah-be` worktree:

```bash
coverage run --source=api manage.py test
coverage xml -o htmlcov/coverage.xml
diff-cover htmlcov/coverage.xml --compare-branch=origin/staging \
  --exclude "*/tests.py" "*/migrations/*" \
  --format html:htmlcov/pil-176-diff-coverage.html
```

## Cross-check with SonarQube

The team's SonarQube (`pilah-be-staging`) measures coverage on all code changed since 10 Sep, by everyone. Its "uncovered lines on new code" were traced with `git blame`. None of them are mine:

| File | Uncovered new lines (SonarQube) | Lines | Author | Mine |
|---|---|---|---|---|
| `api/views.py` | 4 | 72, 75, 76, 335 | other team members | 0 |
| `api/serializers.py` | 2 | 266, 270 | other team member | 0 |
| `api/models.py` | 1 | 89 | other team member | 0 |

`config/settings.py` and `config/urls.py` appear at 0% because CI measures coverage with `--source=api` while SonarQube also analyses `config/`, so those lines have no coverage data at all. It is a CI configuration gap, not missing tests.

## Tests behind the coverage

11 tests in `PencairanAPITests` and 3 in `ResetTestingDataCommandTests`, written test-first (a failing `test(...)` commit, then the `feat(...)`/`fix(...)` commit that makes it pass):

- **Positive:** a pencairan lowers the saldo exactly once; the list filters by nasabah; the detail is readable within the bank.
- **Negative:** nominal above the saldo; zero, negative or decimal nominal; future `tanggal`; invalid `metode`; another bank's nasabah; an inactive, pending or rejected nasabah; outsiders get 404, superadmin 403, unauthenticated 401.
- **Corner cases:** saldo history after a pencairan (API and Excel export); a setoran and pencairan at the same instant; legacy saldo with sen rounded down to whole rupiah.

## Screenshots

### diff-cover: my lines only

![diff-cover report: 111 lines, 0 missing, 100% across 7 files](diff-cov.png)

Coverage of only the lines my branch changes against `staging`, excluding tests and migrations. Full report: [pil-176-diff-coverage.html](pil-176-diff-coverage.html).

### SonarQube: my code, with authorship

![SonarQube file view of api/services.py lines 404–426: BalanceService, with author tooltip muhammad.vegard@ui.ac.id](sonar-balanceservice-404-426.png)

`BalanceService` in `api/services.py`. The tooltip is SonarQube's own blame data: author `muhammad.vegard@ui.ac.id`, revision `765f90f`. Green bars in the margin mark covered lines; lines with no bar (docstrings, continuation lines) are not executable statements, so coverage does not track them. No line is red.

![SonarQube file view of api/services.py lines 450–469: PencairanService write path, all green; line 470 onward by another author](sonar-pencairanservice-450-469.png)

The write path of `PencairanService.create_pencairan`: saldo rounding, the `Pencairan` record, and the saldo update, all covered. At line 470 the author changes, marking where my code ends and `TransactionFilterService`, written by another team member, begins.

### SonarQube: Coverage on New Code, by file

The complete list (12 of 12 files), captured in three parts from top to bottom:

![SonarQube Measures list, part 1: Coverage on New Code 96.3% since 10 Sep; config/settings.py 0%, config/urls.py 0%, api/views.py 93.3%, api/serializers.py 95.9%](sonar-measures-1.png)

![SonarQube Measures list, part 2: models.py 98.9%, seed_testing_data.py 99.3%, then admin.py, reset_testing_data.py, services.py and two test files at 100%](sonar-measures-2.png)

![SonarQube Measures list, part 3: reset_testing_data.py, services.py, test files and urls.py at 100%; 12 of 12 shown](sonar-measures-3.png)

Four of the files I changed (`admin.py`, `reset_testing_data.py`, `services.py`, `urls.py`) are at 100%, with 0 uncovered new lines from anyone. The other three (`views.py`, `serializers.py`, `models.py`) sit higher in this list, below 100%. My lines in them are covered; their uncovered new lines belong to other authors, as traced in [Cross-check with SonarQube](#cross-check-with-sonarqube). The project total of 19 uncovered new lines equals the sum of those rows plus `config/` and `seed_testing_data.py`, none of them mine.
