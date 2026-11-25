# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on either of this week's merge requests. Both pass the quality gate with 0 security hotspots and 0.0% duplication on new code. [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) has 100% of its 72 new lines covered; [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) adds tests only, so it has no lines to cover.

    - **The design lints checked by hand,** since they fail on Windows on path separators: the new code adds no raw colour or font size, and the spacing it moved now uses `AppSpacing`.
    - **No duplicated form:** the in-app page and the onboarding step build from the same `_formFields()` and `_submitButton()`, instead of a copied screen.
    - **No new data path:** the in-app submit reuses `OnboardingNotifier.registerNasabah`, so there is no second request method to keep correct.

## SonarCloud, per merge request

| Scope | Open issues | New-code coverage | Duplication on new code | Security hotspots | Quality gate | Last analysis (WIB) |
|---|---|---|---|---|---|---|
| pilah-mobile [#276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) (PIL-539) | 0 | 100% of 72 lines | 0.0% | 0 | Passed | 23 Nov, 17:43 |
| pilah-be [#185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) (PIL-539) | 0 | no lines to cover (tests only) | 0.0% | 0 | Passed | 18 Nov, 23:48 |

Read from the SonarCloud API on 26 Nov (`api/measures/component`, `api/qualitygates/project_status` and `api/project_pull_requests/list`). Both last analyses ran before the 24 Nov deadline. For #276 it's the analysis after the `staging` merge, so it covers the code as merged.

## Kept out of the code

- **A second copy of the registration screen.** The obvious way to add an in-app form was to copy `RegisterNasabahScreen`. Instead the screen takes a mode, and both layouts share the form, so the duplication check has nothing to find and a field changes in one place.
- **A hidden rule in the client.** The app's one-bank lock is gone for this flow, and the rule it hinted at is enforced by the server only, where #185 pins it. The client keeps only what it needs for display: which banks to mark.
- **Literal spacing in touched code.** [`41a4434`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/41a44349) moved the values on the spacing scale to tokens. The two `20`s have no step on the scale, so they stay rather than shift the layout.

## Local checks before every push

| MR | Suite | Linters |
|---|---|---|
| #276 (22 Nov) | The onboarding, bank sampah approval and router tests | `flutter analyze --fatal-infos`, `dart format`: clean |
| #276 (23 Nov, after the `staging` merge) | 413 tests in `onboarding`, `bank_sampah_approval` and `core/router`: all passed | `flutter analyze`: clean |
| #185 (18 Nov) | The nasabah regression tests | CI's ruff, format and strict mypy checks: green |

The design lints always fail on Windows, so the added lines were read against them instead. Two local test failures in the profile logo tests also happen on a clean `staging` on this machine, and CI ran green.
