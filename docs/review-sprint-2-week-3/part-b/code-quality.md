# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on either of this week's merge requests. Both pass the quality gate with 0 security hotspots, 0.0% duplication and 100% coverage on new code.

    Two problems did come up, both on my own new code, and both were fixed before review:

    - a **critical** cognitive-complexity finding (S3776), fixed by refactoring, not suppressed;
    - a breach of the team's design-lint baseline, which I caught by hand before pushing, because those tests can't run properly on Windows.

## SonarCloud, per merge request

| Scope | Open issues | New-code coverage | Duplication on new code | Security hotspots | Quality gate |
|---|---|---|---|---|---|
| pilah-be [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (PIL-451) | 0 | 100% of 35 lines | 0.0% | 0 | Passed |
| pilah-mobile [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (PIL-451) | 0 | 100% of 68 lines | 0.0% | 0 | Passed |

Read from the SonarCloud API on 29 Oct (`api/measures/component` and `api/issues/search` with `pullRequest=<n>`).

![SonarCloud PR summary for pilah-be #137: quality gate passed, 0 new issues, 100% coverage on 35 new lines](evidence/sonar-pilah-be-137.png){ width="620" }

![SonarCloud PR summary for pilah-mobile #174: quality gate passed, 0 new issues, 100% coverage on 68 new lines](evidence/sonar-pilah-mobile-174.png){ width="620" }

## Found and fixed before review

### A critical complexity finding on my own code

| Rule | Severity | Where | Opened | Closed |
|---|---|---|---|---|
| `dart:S3776` Cognitive Complexity | Critical | `CompleteProfileScreen.build`: "reduce its Cognitive Complexity from 17 to the 15 allowed" | 26 Oct, 20:48 WIB | 26 Oct, 22:00 WIB, **fixed** |

The role note had added an `Authenticated` check and a three-part condition to a `build` method that was already near the limit. I didn't suppress the rule or ask for the threshold to be raised. [`87f2f0d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/87f2f0d) extracts the rule into `_changeableRoleTitle`, a named query, and `build` only places the note when it gets a title. The Lengkapi Profil tests passed before and after, and the next analysis closed the issue. The [Programming page](programming.md#a-rule-out-of-a-build-method-87f2f0d) has the code.

### A coverage gap that wasn't in my code

SonarCloud's first run on #174 reported 97.1%, with one uncovered line each in `auth_remote_data_sources.dart` and `auth_repository_impl.dart`. Both were the `@override` entry lines of *existing* methods, `getMe` and `saveToken`. They sit right below the `changeRole` methods I inserted, so the diff counted them as new.

Locally they were covered; on a PR, CI runs only the changed test files and their mirrors, and none of those called the real `getMe` or `saveToken`. [`b2344b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b2344b5) adds a test for each to the files CI does run. The rerun shows 100% of 68 lines.

### A design-lint breach, caught by hand

The team's `test/design/*` tests limit hard-coded colours and font sizes per file, against `*_baseline.json`. On Windows, 19 of them always fail: the baseline is keyed with `/` paths and Windows yields `\`, so every file reads "allowed 0". They fail the same way on a clean `staging` checkout, so a local run can't tell me anything.

So I checked them by hand. I grepped every line this MR adds for the lints' patterns, and counted per file against the baselines.

- My new role note's `TextStyle(fontSize: 13, …)` raised `complete_profile_screen.dart` from its allowed **1** hard-coded font size to **2**, which would have failed CI.
- [`00fec19`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/00fec19) switched it to `AppTextStyle.small`, which brought the count back to 1.
- A final scan found no other lint pattern in the added lines. CI agreed: "Format, analyze, tests & build" passed.

## Local checks before every push

These are the commands CI runs, run locally first.

**Backend (#137), against Postgres 16:**

```console
$ ruff check . && ruff format --check .                        # all checks passed
$ pip check                                                    # no broken requirements
$ python manage.py makemigrations --check --dry-run             # no changes
$ python manage.py check --deploy --fail-level ERROR           # passes (warnings only)
$ mypy api apps config shared_kernel tests                     # no issues in 221 files
$ coverage run … manage.py test && diff-cover … --compare-branch=origin/staging
                                                               # 874 tests; 100% of 115 changed lines
```

mypy caught a missing `api.models.__all__` export before the push, fixed in [`8bf93cf`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8bf93cf). The 5 failing backend tests are deployment-script tests that need bash paths and LF line endings. They fail the same way on a clean `staging` checkout on Windows, and pass in CI.

**Mobile (#174):**

```console
$ dart format --output=none --set-exit-if-changed lib test codegen   # 0 changed
$ flutter analyze                                                    # no issues
$ flutter test --coverage                                            # the same 25 Windows-only failures as staging, nothing new
$ diff-cover coverage/lcov.info --compare-branch=origin/staging      # 100% of 70 changed lines
$ flutter build web --release -t lib/main_development.dart           # built
```

The debug APK couldn't be built locally: Android's `google-services.json` isn't on this machine, and CI supplies it from a secret. PIL-451 changes no Android or native code, and CI's build passed.
