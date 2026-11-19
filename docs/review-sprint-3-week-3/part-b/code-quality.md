# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on any of this week's merge requests. All seven pass the quality gate with 0 security hotspots, 0.0% duplication and 100% coverage on new code. The exception is #238, which changes only copy, comments and a constant, so it has no coverable lines.

    - **One tool finding, on my own code, fixed by refactoring:** `dart:S3776` (critical, cognitive complexity 17 of 15) on #174's role page, closed by Extract Method 57 minutes after it opened.
    - **A duplicated domain rule now guarded by a test:** the last hand-written "counted setoran" filter was replaced. An architecture test now fails on any new one, so this class of duplication can't come back unnoticed.
    - **Validation moved to where it belongs:** two views stopped validating raw bodies, and one viewset dropped an `update` override, leaving less code to keep correct.

## SonarCloud, per merge request

| Scope | Open issues | New-code coverage | Duplication on new code | Security hotspots | Quality gate |
|---|---|---|---|---|---|
| pilah-be [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) (PIL-482) | 0 | 100% of 15 lines | 0.0% | 0 | Passed |
| pilah-be [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) (waste categories) | 0 | 100% of 2 lines | 0.0% | 0 | Passed |
| pilah-be [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177) (NUL in a body) | 0 | 100% of 13 lines | 0.0% | 0 | Passed |
| pilah-be [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (PIL-451) | 0 | 100% of 52 lines | 0.0% | 0 | Passed |
| pilah-mobile [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (PIL-451) | 0 (1 closed by [`a363412`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a363412f)) | 100% of 96 lines | 0.0% | 0 | Passed |
| pilah-be [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) (PIL-481) | 0 | 100% of 7 lines | 0.0% | 0 | Passed |
| pilah-mobile [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) (PIL-481) | 0 | no coverable lines | 0.0% | 0 | Passed |

Read from the SonarCloud API on 19 Nov (`api/measures/component`, `api/qualitygates/project_status`, and `api/issues/search` with `statuses=CLOSED,RESOLVED` for the closed finding). On 11 Nov the cherry-picked date-test fix let #167 and #168 get their first SonarCloud verdict, which Heraldo had been unable to read on 9 Nov.

## Found and fixed

| Rule | Severity | Where | Opened | Fix |
|---|---|---|---|---|
| `dart:S3776` Cognitive Complexity | Critical | #174 `role_selection_page.dart`, after my Kembali fix put the button inline in `build` (17 of 15) | 17 Nov, 00:12 | [`a363412`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a363412f) extracts `_backToProfile`. **Closed** at 01:09 on the next analysis |

**A duplicated rule, now guarded.** `waste_categories` spelled out `transaksi__status=Transaksi.Status.TERCATAT` instead of calling `tercatat()`. SonarCloud's duplication check doesn't see a one-line filter. [`b10fffa`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b10fffaa) adds an architecture test that parses `apps/` and fails on any such filter. On `staging` it failed on exactly that line, and [`8d1a931`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8d1a9316) fixed it. Details are on the [Programming page](programming.md#a-rule-enforced-by-a-fitness-function-b10fffa-8d1a931).

**Less code doing the same job.** #177 removes the jenis sampah viewset's `update` override, `type: ignore` included, whose job the serializer now does. It also replaces the device-token view's hand-written body check with the serializer the `POST` already used. #175's refactor removes a second copy of the UUID `try/except`.

**Copy and comments kept true.** On #167 and #238, Heraldo found a docstring and two strings that still described the old behaviour. All were fixed, and the toast copy became one named constant, so the next change has one place to edit.

## Local checks before every push

| MR | Suite | Linters |
|---|---|---|
| #175, #176, #177 | The affected apps and `tests.regression` on PostgreSQL 16, plus `tests.test_architecture` and `apps.reporting` for #176 (56 passed). On #176 a full local run was cut short when the machine ran out of memory (Windows error 1455), so the full suite ran in CI: Verify passed | `ruff check .`, `ruff format --check .`, strict `mypy` on the changed modules, `makemigrations --check`: clean |
| #137 (13 Nov merge) | 345 tests across authentication, bank_sampah, nasabah and regression, on PostgreSQL 16, including the two-thread race tests | `makemigrations --check`: no changes after the renumbering |
| #174 (13 Nov merge) | 389 onboarding and authentication tests | `flutter analyze --fatal-infos`, `dart format`: clean |

The design lints always fail on Windows, so the added lines were read against them instead. The new Kembali adds no raw colour, spacing or font size: it is an `AppButton` with its neutral variant.
