# Development Discipline

!!! success "Competency level: 3"
    Two new merge requests this week, both merged, and five approved ones merged:

    - [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) (PIL-539, 5 commits): one regression test per commit, each naming the OWASP category it guards;
    - [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) (PIL-539, 9 commits and a `staging` merge): four red/green pairs and a refactor, each pair one behaviour;
    - #137, #174, #175, #176 and #177, approved in Sprint 3 Week 3, merged on 18 Nov after the comments that came in after their approvals were checked.

    Every commit is a scoped Conventional Commit. Each #276 subject carries its TDD phase, and each body names the design issue, the pattern, its type and origin, and the OWASP and SOLID notes. #185's subjects carry no phase, because its tests pin existing behaviour and had no red step. The merge commit says what it keeps from each side and why. Review threads got a reply each, with the reason for leaving a point when it was out of scope.

## Merge requests

| MR | Opened | Size | Commits | CI / SonarCloud | Status (24 Nov) |
|---|---|---|---|---|---|
| [#185 — PIL-539: cover a nasabah applying to a second bank end to end](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) | 18 Nov | +148 / −0, 1 file | 5 | green, gate passed, 0 issues (tests only) | Approved by Heraldo (19 Nov); **merged 23 Nov** (00:25) |
| [#276 — PIL-539: apply to another bank sampah from Bank sampah saya](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) | 23 Nov | +680 / −76, 9 files | 9 + 1 merge | green, gate passed, 0 issues, 100% of 72 lines | Approved by Heraldo (23 Nov); **merged 23 Nov** (17:44) |
| [#137 — PIL-451 backend](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (from Sprint 2) | 26 Oct | — | — | green | **Merged 18 Nov** (23:19) |
| [#174 — PIL-451 mobile](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (from Sprint 2) | 26 Oct | — | — | green | **Merged 18 Nov** (23:20) |
| [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175), [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176), [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177) (Sprint 3 Week 3) | 16 Nov | — | — | green | **Merged 18 Nov** (23:19) |

The 18 Nov merges were of PRs already counted in [Sprint 3 Week 3](../../review-sprint-3-week-3/part-b/development-discipline.md); they are listed here because the merging happened this week.

## Planning the week

1. **Approved PRs first** (18 Nov). Gabriel's non-blocking comments on #175 and #176 arrived after Heraldo's approvals. Each was checked against the issue's scope, then answered in its thread with the reason for leaving it to a follow-up ([#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175#issuecomment-6984421991), [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176#issuecomment-6984422988)), and the five PRs were merged.
2. **The server's rules before the client relies on them.** PIL-539 needed no backend code, but the app was about to drop its one-bank lock. So #185 came first: five tests that pin the server rules the app will depend on.
3. **A stacked PR, kept mergeable.** #276 was built on Gabriel's [#267](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/267) (the active bank selection), which was still open. When #267 merged on 23 Nov (16:05), #276 was retargeted to `staging` and `staging` merged in, before the merge.
4. **One behaviour per red/green pair.** The button, the in-app form, the picker and the submit are four pairs, each reviewable alone, then one refactor with no behaviour change.
5. **CI's own checks run locally before each push:** `dart format`, `flutter analyze --fatal-infos` and the affected test folders on mobile; the nasabah regression suite on the backend.
6. **A scan right after the sub-issue was finished:** [ZAP, 23 Nov](../../security/zap-2026-11-23.md).

## Keeping a stacked PR mergeable

| Date | Commit | What the merge carried |
|---|---|---|
| 23 Nov, 17:27 | [`cf89110`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cf89110f) | `staging`'s redesigned onboarding step (`OnboardingProgress`, `OnboardingActions`, the `notice` slot) and its reload of the memberships after an onboarding submit. The one conflict was in `register_nasabah_screen.dart`. Both sides were kept: `staging`'s layout for the onboarding step, and #276's in-app page as it was, with one shared review-note text. The 413 tests in the three affected folders passed, and `flutter analyze` was clean |

## Example commit messages

```
feat(onboarding): [GREEN] open the registration form in-app from Bank sampah saya (PIL-539)

RegisterNasabahScreen takes a RegisterNasabahMode. The default,
onboarding, is unchanged: the OnboardingStepScaffold with its stepper,
Keluar exit, onboarding back handling and the one-membership lock for a
pengurus-entered record auto-linked at login. additional, served at
/ajukan-bank-sampah behind the same platform guard as /register-nasabah,
is a page of the app: NasabahPageAppBar with a back button, the form in
a ContentFrame, and no lock, so an account that already belongs to a
bank sampah can pick another one.

Design issue: one screen hard-wired to a single context (the onboarding
step), so its lock, stepper and logout exit would have applied to a
signed-in nasabah applying from inside the app. Pattern: a mode
parameter chooses the layout, with the form fields and the submit button
extracted once and shared by both (Extract Method). Type: Principle
(SRP: one form, a layout per context; OCP: onboarding unchanged).
Origin: designed in.
```

```
feat(onboarding): [GREEN] apply to another bank and return to Bank sampah saya (PIL-539, OWASP A04)

...
OWASP A04 Insecure Design: the client sends only the bank id; who
applies comes from the session on the server, and the
one-membership-per-bank rule stays server-side (pilah-be #185 covers it).
```

```
refactor(onboarding): [REFACTOR] space the registration form with AppSpacing (PIL-539)

The form fields and footer this PR moved into shared methods still used
bare numbers. The ones on the spacing scale are now tokens: 24 -> xl,
16 -> lg, 12 -> md, 8 -> sm. The two 20s have no step on the scale and
are left as they are, so the layout does not move. No behaviour change:
the 130 onboarding page tests pass before and after.
```

The #185 subjects name what each test covers and the category it guards, for example `test(nasabah): cover that only the second bank's pengurus decides the application (OWASP A01)`.
