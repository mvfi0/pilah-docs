# Development Discipline

!!! success "Competency level: 3"
    Three new merge requests this week, plus review rounds on five more:

    - [pilah-be #175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) (PIL-482, 3 commits), [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) (2 commits) and [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177) (8 commits), each with one responsibility;
    - [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) and [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174), PIL-451's third round: `staging` merged in twice and three times, then Tristan's two P2 findings fixed;
    - [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167), [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) and [#168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168): Heraldo's findings fixed and CI unblocked, then merged.

    Every commit is a scoped Conventional Commit. The TDD phase is in each subject, and each body names the design issue, the pattern and its origin, the OWASP categories and the SOLID principle. Merge commits say what they carry and why (a renumbered migration, a test fix). Fixes came as new commits, never force-pushed, and every review thread got a reply linking its fix, or the reason for leaving it.

## Merge requests

| MR | Opened | Size | Commits this week | CI / SonarCloud | Status (17 Nov) |
|---|---|---|---|---|---|
| [#175 — 422 for a malformed `nasabah_id` filter (PIL-482)](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) | 16 Nov | +75 / −8, 4 files | 3 | green, gate passed, 0 issues, 100% | Approved by Heraldo (16 Nov); Gabriel's non-blocking comment (17 Nov) |
| [#176 — waste categories through `tercatat()`](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) | 16 Nov | +49 / −6, 2 files | 2 | green, gate passed, 0 issues, 100% | Approved by Heraldo; Gabriel's non-blocking comment |
| [#177 — validate kode and device token before querying](https://github.com/bank-sampah-PILAH/pilah-be/pull/177) | 16 Nov | +140 / −25, 5 files | 8 | green, gate passed, 0 issues, 100% | Approved by Heraldo; Gabriel: "Nothing blocking" |
| [#137 — PIL-451 backend](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (from Sprint 2) | 26 Oct | +607 / −5, 11 files | 2 merges + 3 | green, gate passed, 0 issues, 100% | Third round fixed and answered; Tristan re-approved on 17 Nov |
| [#174 — PIL-451 mobile](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (from Sprint 2) | 26 Oct | +800 / −37, 19 files | 3 merges + 3 | green, gate passed, 0 issues, 100% | Third round fixed and answered; Tristan re-approved on 17 Nov |
| [#167 — PIL-481 backend](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) | 9 Nov | +97 / −41, 11 files | 1 + the date-test fix | green, gate passed, 0 issues, 100% | **Merged 12 Nov** (01:12) by Scallss, approved by Heraldo and Scallss |
| [#238 — PIL-481 mobile](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) | 9 Nov | +51 / −15, 6 files | 2 | green, gate passed, 0 issues | **Merged 12 Nov** (01:11) by Scallss |
| [#168 — PIL-480](https://github.com/bank-sampah-PILAH/pilah-be/pull/168) | 9 Nov | +38 / −10, 3 files | the date-test fix | green, gate passed, 0 issues, 100% | **Merged 12 Nov** (01:11) by Scallss |

#137, #174, #175, #176 and #177 were merged on 18 Nov, after this week's due date.

## Planning the week

1. **A plan agreed before coding** (12 Nov): no splitting of the already-reviewed PIL-481 PRs, but new, separate work, each small and independently reviewable:
    - the 9 Nov scan finding (PIL-482);
    - Heraldo's note on #167 about the rule written by hand;
    - the request-body case Scallss's #172 listed under "Not in this PR".
2. **A plan item dropped when someone else did it.** The plan had a NUL-safe `search` as item 2. Scallss merged it first as #172, so #177 took his PR's open follow-up instead, and the description says so.
3. **One PR, one responsibility.** #175 validates one parameter, #176 guards one rule, and #177 validates one class of input in three places. None depends on another, so they could be reviewed and merged in any order.
4. **CI's own checks run locally before each push:** ruff, strict mypy, `makemigrations --check` and the affected suites on PostgreSQL 16 on the backend; `dart format`, `flutter analyze --fatal-infos` and the onboarding and authentication tests on mobile.
5. **A scan of each new PR** right after it was finished: [ZAP, 17 Nov](../../security/zap-2026-11-17.md).

## Keeping long-running PRs mergeable

PIL-451's PRs have been open since 26 Oct. This week they needed `staging` merged in three times:

| Date | Commit | What the merge carried |
|---|---|---|
| 13 Nov | be [`12b8983`](https://github.com/bank-sampah-PILAH/pilah-be/commit/12b89834), mobile [`2ef6259`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2ef6259b) | The role-change migration renumbered 0029 → 0038 behind `staging`'s 0037, flagged as a clash on 31 Oct. Additive conflicts kept on both sides. 345 backend and 389 mobile tests passed |
| 16 Nov | mobile [`f03cd4b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f03cd4bc) | The date-test fix (#249) that had turned "Test shard 1" red. Only that test file changed |
| 16 Nov | be [`918363f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/918363f1), mobile [`535e34c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/535e34cf) | The Pengelola Induk removal (#178, #251); the migration moves to 0039 |

Each merge carried only what already had tests. The two review fixes came after them as their own red/green pairs ([TDD](tdd.md#review-rounds)).

**Not merged on 13 Nov, deliberately.** Both PRs had two approvals, but Tristan's change request from 31 Oct still stood, although I had answered all his points on 2 Nov. Only an admin bypass would have got past it, and I didn't use one on a teammate's open request. I asked for his re-review instead. His new round on 16 Nov raised two more points, fixed the same evening, and he approved on 17 Nov.

## Example commit messages

```
fix(onboarding): [GREEN] lock and reload the account before completing the profile (PIL-451)

...
Design issue: a fifth writer of the role-lock invariant (profile
completion) that acted on the request's cached User without the lock.
Pattern: Pessimistic Offline Lock on the account row, through the one
lock_account entry point the other writers share (Principle: SRP, the
lock policy lives in one method; DIP, writers depend on that abstraction,
not on a hand-written select_for_update).
```

```
test(reporting): [RED] counted setoran are read only through tercatat()

PIL-428 made TransaksiQuerySet.tercatat() the one named rule for "setoran
that still count", so a new report cannot forget to leave a void out. One
read still spells the rule out by hand: DashboardService.waste_categories
filters transaksi__status=Transaksi.Status.TERCATAT. The new architecture
test walks apps/ (tests and the ledger model that owns the rule excluded)
and fails on exactly that line, apps/reporting/services.py:100.
```

The #177 subjects, oldest first, one slice per edit path:

```
test(waste-catalog): [RED] a NUL byte in kode on edit is rejected with 422
test(waste-catalog): [RED] a padded duplicate kode on edit is rejected with 422
fix(waste-catalog): [GREEN] check a duplicate kode on validated data, in the serializer
test(nasabah): [RED] a NUL or padded duplicate kode on edit is rejected with 422
fix(nasabah): [GREEN] check a duplicate kode after validation on edit
test(notification): [RED] a NUL byte in the device token to forget is rejected with 422
fix(notification): [GREEN] validate the device token to forget with a serializer
style(waste-catalog): drop the blank first line left by the removed import
```

## Status and what is left (17 Nov)

- **#167, #168 and #238** are merged.
- **#175, #176 and #177** have Heraldo's approval and Gabriel's comments (17 Nov, non-blocking), to be answered next week.
- **#137 and #174** have every approval, including Tristan's, and green CI.
