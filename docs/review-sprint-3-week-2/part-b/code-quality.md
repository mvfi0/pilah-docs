# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on any of this week's merge requests. All five pass the quality gate with 0 security hotspots, 0.0% duplication and 100% coverage on new code. The exception is #238, which changes only copy and comments, so it has no coverable lines.

    No tool finding was raised on this week's code. The quality work was done by hand:

    - **Two spacing values moved to `AppSpacing`** on #193, after DESIGN.md (Scallss's nit).
    - **Stale comments and docstrings corrected** in the same PR as the behaviour they describe (#167, #238).
    - **Tests decoupled from an internal id** before the column they used was removed (#168).

## SonarCloud, per merge request

| Scope | Open issues | New-code coverage | Duplication on new code | Security hotspots | Quality gate |
|---|---|---|---|---|---|
| pilah-be [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) (PIL-428, final round) | 0 | 100% of 95 lines | 0.0% | 0 | Passed |
| pilah-mobile [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) (PIL-428, final round) | 0 | 100% of 154 lines | 0.0% | 0 | Passed |
| pilah-be [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) (PIL-481) | 0 | 100% of 7 lines | 0.0% | 0 | Passed |
| pilah-mobile [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) (PIL-481) | 0 | no coverable lines | 0.0% | 0 | Passed |
| pilah-be [#168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168) (PIL-480) | 0 | 100% of 2 lines | 0.0% | 0 | Passed |

Read from the SonarCloud API on 19 Nov (`api/measures/component` and `api/qualitygates/project_status` with `pullRequest=<n>`). No issue was opened and closed on these PRs between 4 and 10 Nov (`api/issues/search` with `statuses=CLOSED,RESOLVED`).

**Why #167 and #168 had no SonarCloud verdict on 9–10 Nov.** Their Verify check was red, so the analysis that depends on it couldn't report. The cause was a date-dependent export test that also fails on a clean `staging` (diagnosed on 10 Nov). The fix from PIL-239 was cherry-picked on 11 Nov, and the numbers above are from the analysis after that.

## Found and fixed by hand

| What | Where | Fix |
|---|---|---|
| Bare spacing number (`12`) in new code, against DESIGN.md §2 | #193, the Hapus dialog | `const SizedBox(height: AppSpacing.md)`, [`b815354`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b815354f) |
| Comments that still said a voided setoran stays in the riwayat | #167, `apps/ledger` | [`646c0d1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/646c0d1c), in the same PR as the change. Heraldo found one more docstring, fixed on 11 Nov |
| Two tests that counted export rows through an internal id column | #168, `apps/reporting` tests | [`9dbfcf2`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9dbfcf26): they count rows that carry a value |

**Still open after the merge:** Heraldo's 🔵 on #193's detail sheet (`EdgeInsets.all(16)` and `SizedBox(height: 8)`), posted with his approval and merged before I saw it. The design ratchet doesn't fail on it. See [Team Development Management](team-development-management.md#reviews-received).

## Local checks before every push

The figures each PR's description records:

| MR | Suite | Diff coverage against `origin/staging` | Linters |
|---|---|---|---|
| #145 (4 Nov round) | 953 tests on PostgreSQL 16; only the 5 known Windows deployment-script failures | 100% | `ruff check`, `ruff format --check`, strict `mypy`, `makemigrations --check`: clean |
| #193 (4 Nov round) | 357 transaksi tests and 355 design and services tests pass | no uncovered new line | `flutter analyze --fatal-infos`, `dart format`: clean |
| #167 | 999 tests (SQLite). 17 not passing, none from this change: the Windows-only load-runner and deployment tests, plus a file-mode assertion and the aged date test that also fail on a clean `staging` | 100% of 45 lines | ruff and `makemigrations --check` clean; strict `mypy` has 4 errors, all in `tests/load` (POSIX-only calls), none in changed files |
| #168 | 572 tests (SQLite) and 388 on PostgreSQL 16; the one failure is the aged date test | 100% of 12 lines, on PostgreSQL 16 | ruff and `mypy` on the changed module: clean |
| #238 | `flutter test test/features/transaksi`: 499 passed | no coverable lines | `flutter analyze --fatal-infos`, `dart format`: clean on the changed folders |

On Windows, the team's `test/design/*` lints always fail, because their baselines use `/` paths, so I matched the added lines against their patterns by hand. The only hit was the bare `12` above.
