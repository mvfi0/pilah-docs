# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on any of this week's merge requests. All five pass the quality gate with 0 security hotspots, 0.0% duplication and 100% coverage on new code.

    Three findings did come up, all on my own new code, and all were fixed by refactoring rather than suppressed:

    - **S3776** (critical, cognitive complexity) on #193 and again on #174;
    - **S3358** (major, nested ternaries) on #193, introduced by my merge of `staging`.

    One more problem no tool flagged: a domain rule copied into nine queries. I fixed it on my own initiative.

## SonarCloud, per merge request

| Scope | Open issues | New-code coverage | Duplication on new code | Security hotspots | Quality gate |
|---|---|---|---|---|---|
| pilah-be [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) (PIL-428) | 0 | 100% of 87 lines | 0.0% | 0 | Passed |
| pilah-mobile [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) (PIL-428) | 0 (3 closed by [`ca2ec7a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca2ec7a2)) | 100% of 140 lines | 0.0% | 0 | Passed |
| pilah-mobile [#196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196) (PIL-435) | 0 | 100% of 23 lines | 0.0% | 0 | Passed |
| pilah-be [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (PIL-451) | 0 | 100% of 51 lines | 0.0% | 0 | Passed |
| pilah-mobile [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (PIL-451) | 0 | 100% of 91 lines | 0.0% | 0 | Passed |

Read from the SonarCloud API on 2 Nov (`api/measures/component` with `pullRequest=<n>`), and issues with `sonar list issues -p <project> --pull-request <n>`.

## Found and fixed

| Rule | Severity | Where | Opened | Fix |
|---|---|---|---|---|
| `dart:S3776` Cognitive Complexity | Critical | #193 `aktivitas_table.dart`, the table row's single `build` (16 of 15) | 31 Oct | `staging`'s PIL-453 split that `build` into small methods. My merge ([`0c6f1e7`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/0c6f1e72)) put the Hapus button and Dibatalkan badge into those methods, so the long method no longer exists |
| `dart:S3776` Cognitive Complexity | Critical | #174 `CompleteProfileScreen.build` (18 of 15), after my review fix added a role-change check to its `ref.listen` | 2 Nov | [`8bdb1b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8bdb1b54) moves the listener into `_onAuthChanged`. **Closed** on the next analysis: 0 issues |
| `dart:S3358` Nested ternary (×3) | Major | #193 TIPE cell, where my merge nested `staging`'s type ternaries inside the Dibatalkan ternary | 2 Nov | [`ca2ec7a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca2ec7a2) extracts `_typeBadge` with a guard clause. **Closed** on the next analysis: 0 issues |

**A duplicated rule, found without a tool.** "A voided setoran counts toward nothing" was written as `filter(status=TERCATAT)` in nine places across three apps. SonarCloud's duplication check doesn't see a one-line filter, but a tenth report could forget it and quietly count voided money. [`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0) names it once as `Transaksi.objects.tercatat()`. Details are on the [Programming page](programming.md#a-domain-rule-named-once-ae850a0).

**An unreachable branch removed, not tested around.** On #137, diff coverage showed one line no test could reach: a "record claimed meanwhile" branch. Email is unique, so only the same account could claim the record meanwhile. Rather than contrive a test, [`e077084`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e077084) reads the record once and removes the branch.

## Design lints, checked by hand

The team's `test/design/*` tests limit hard-coded colours, font sizes, radii and stock widgets per file. On Windows, 16 of them always fail, because the baseline uses `/` paths and Windows yields `\`. They fail the same way on a clean `staging` checkout, so a local run can't tell me anything.

So I matched every line each MR adds against the lints' patterns (`Color(0x…)`, `fontSize: <number>`, `Radius.circular(<number>)`, stock font weights):

- **#193:** no match. The new Pembatalan card uses `AppSpacing`, `AppRadius` and `AppColors`. `Colors.white` isn't in the colour pattern.
- **#174:** the role note's raw `EdgeInsets.fromLTRB(24, 16, 24, 0)` broke DESIGN.md §2 (spacing tokens). Tristan caught it in review, and it's now `AppSpacing.lg` ([`6eef5a4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6eef5a43)).

## Local checks before every push

**Backend (#145, #137), against Postgres 16:**

```console
$ ruff check . && ruff format --check .                        # all checks passed
$ mypy api apps config shared_kernel tests                     # no issues in 223 source files
$ python manage.py makemigrations --check --dry-run             # no changes detected
$ coverage run manage.py test && diff-cover … --compare-branch=origin/staging
    # #145: 898 tests, 100% of 348 changed lines
    # #137: 880 tests, 100% after e077084
```

The 5 failing backend tests are deployment-script tests that need bash paths and LF line endings. They fail the same way on a clean `staging` checkout on Windows, and pass in CI.

**Mobile (#193, #196, #174):**

```console
$ dart format --output=none --set-exit-if-changed lib test codegen   # 0 changed
$ flutter analyze --fatal-infos                                      # no issues
$ flutter test --coverage                                            # 2,875 passed (#193, #174); the same 22 Windows-only failures as staging
$ diff-cover lcov.info --compare-branch=origin/staging                # #193 100% of 152 lines; #196 100% of 34; #174 100%
$ flutter build web --profile -t lib/main_development.dart           # built, then driven by Playwright
```
