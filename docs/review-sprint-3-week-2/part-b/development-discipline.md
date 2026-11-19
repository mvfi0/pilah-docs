# Development Discipline

!!! success "Competency level: 3"
    Three new merge requests this week, plus the final review round on two more:

    - [pilah-be #167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) and [pilah-mobile #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238): the backend and mobile halves of PIL-481, 7 and 2 commits;
    - [pilah-be #168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168): PIL-480, 3 commits;
    - [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) and [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193): 2 and 5 new commits answering six review findings, then approved and merged.

    Each uses the Linear branch name (`feature/pil-481`, `feature/pil-480`) off `staging`. Every commit is a scoped Conventional Commit:

    - the TDD phase is in each subject;
    - the body names the design issue, the pattern and its origin;
    - the body lists the OWASP categories the change guards, and the SOLID principle it applies.

    Each description has the contract, the behaviour, screenshots, the E2E results and the local validation. Fixes came as new commits, never force-pushed, and every review thread got a reply linking its fix.

## Merge requests

| MR | Opened | Size | Commits this week | CI / SonarCloud | Status (10 Nov) |
|---|---|---|---|---|---|
| [#167 — hide a voided setoran from the riwayat lists](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) | 9 Nov | +97 / −41, 11 files | 7 | gate passed, 0 issues, 100% | Heraldo requested changes on 9 Nov: the code is correct, a docstring is stale. Answered on 11 Nov (Sprint 3 Week 3) |
| [#238 — Hapus dialogs say a deleted setoran is hidden](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) | 9 Nov | +51 / −15, 6 files | 2 | gate passed, 0 issues, no coverable lines | Heraldo requested changes on 9 Nov: one leftover string, two consistency gaps. Answered on 11 Nov |
| [#168 — drop the ID Aktivitas column from the export](https://github.com/bank-sampah-PILAH/pilah-be/pull/168) | 9 Nov | +38 / −10, 3 files | 3 | gate passed, 0 issues, 100% | Open, no review yet (requested on 11 Nov) |
| [#145 — PIL-428 backend](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) (from Sprint 3 Week 1) | 31 Oct | +1044 / −44, 26 files | 2 (+ a `staging` merge) | gate passed, 0 issues, 100% | **Merged 4 Nov** by Scallss, approved by Heraldo and Scallss |
| [#193 — PIL-428 mobile](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) (from Sprint 3 Week 1) | 31 Oct | +1167 / −85, 27 files | 5 (+ a `staging` merge) | gate passed, 0 issues, 100% | **Merged 4 Nov** by Scallss, approved by Heraldo and Scallss |
| [#196 — PIL-435 Riwayat setoran only](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196) (from Sprint 3 Week 1) | 31 Oct | +277 / −65, 8 files | — | gate passed, 0 issues, 100% | **Merged 4 Nov** by me, after Heraldo's and Scallss's approvals |

Sizes are the final ones on GitHub.

## From issue to merge request

1. **Scope taken from the UAT's decision, and its limits stated.** PIL-481 reverses a PIL-428 decision (a void stayed visible, labelled Dibatalkan). The issue records the UAT's choice, option (a): a "Hapus" should feel like a delete. The PR states what stays: the row, its who, when and why, and its detail by id, each pinned by a guard test.
2. **One branch name in both repos** (`feature/pil-481`), so Linear links both PRs to the issue. The two PRs link to each other.
3. **Test-first, in slices:** three red/green pairs on the backend (feed; setoran list and dashboard; nasabah views), one on mobile, and a refactor-first change on #168. The tables are on the [TDD page](tdd.md).
4. **CI's own checks run locally before each push:** ruff, strict mypy and the suite on PostgreSQL 16 on the backend; `dart format`, `flutter analyze --fatal-infos` and the transaksi tests on mobile; Playwright E2E for the web change (24/24).
5. **A scan per finished sub-issue,** right after the work: [ZAP, 9 Nov](../../security/zap-2026-11-09.md). Its one new finding went to Linear as PIL-482 rather than into an unrelated PR.
6. **Issues stopped rather than guessed at.** I stopped PIL-475 when I couldn't confirm its root cause, and wrote the reproduction steps instead. The "Google login opens Gmail on mobile web" finding has no cause in the code, so it waits for the tester's details.

## Changes after the MR was open

- **#145, Heraldo** (4 Nov): red [`743ed1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/743ed1c3), green [`abcafa3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/abcafa30), then a `staging` merge. [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#discussion_r4466534858).
- **#193, Heraldo** (4 Nov): red [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07), green [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b), then a `staging` merge. [Reply 1](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4466535388), [reply 2](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4466536023).
- **#193, Scallss** (4 Nov): red [`6979612`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/69796129), green [`be7b6d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/be7b6d06), refactor [`b815354`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b815354f). [Reply 1](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4468196683), [reply 2](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4468197124).
- **A heads-up to the PR that shares the code.** Rifqi's [#212](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/212) (bulk void) carries the same single Hapus dialog. I told him about the fix, with the commits and the merge that would bring it in ([comment](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/212#issuecomment-6628744737)).

## Example commit messages

```
fix(transaksi): [GREEN] keep the Hapus dialog open while the void is sent, and always refresh after it (PIL-428, OWASP A04)
```

```
test(ledger): [RED] setoran list and dashboard recent leave a voided setoran out (PIL-481)

Second slice of the same UAT finding: the pengurus /transaksi list and the
dashboard "transaksi terbaru" still list a dibatalkan setoran. Both new tests
fail for that reason. A third test, which already passes, pins that a voided
setoran stays reachable by its own id with who voided it and why, so an old
receipt link and the audit trail keep working.

Design issue: three list endpoints each build their own Transaksi query, so
one rule has to be applied in three places. Pattern: reuse the named
tercatat() Query Object at each list boundary, not in the shared get_queryset
that detail, edit and void also read. Origin: reversal of a PIL-428 choice.
```

```
test(reporting): [REFACTOR] identify export events without the ID Aktivitas column (PIL-480)

Two export tests counted events through the "ID Aktivitas" column (row[13]).
That column is going away, and a test that needs an internal id to count rows
would block the change. They now count an event as a row that carries a value
(a setoran puts its total on its first item row, a pencairan its nominal).
Green before and after; no behaviour change.
```

The PIL-481 backend subjects, oldest first:

```
test(ledger): [RED] riwayat feeds leave a voided setoran out (PIL-481)
fix(ledger): [GREEN] read the riwayat feed through tercatat() (PIL-481)
test(ledger): [RED] setoran list and dashboard recent leave a voided setoran out (PIL-481)
fix(ledger): [GREEN] leave voided setoran out of the setoran list and dashboard recent (PIL-481)
test(nasabah): [RED] beranda and riwayat leave a voided setoran out (PIL-481)
fix(nasabah): [GREEN] leave voided setoran out of beranda and riwayat (PIL-481)
docs(ledger): update comments that said the riwayat lists a voided setoran (PIL-481)
```

## Status and what is left (10 Nov)

- **#145, #193 and #196** are merged.
- **#167 and #238:** Heraldo's change requests are open. **#168** waits for review.
- **CI is red on #167 and #168,** and not because of them: a date-dependent export test fails on `staging` too, and its fix (PIL-239) wasn't merged yet. Diagnosed on 10 Nov; the fix was cherry-picked into both on 11 Nov.
- **PIL-482** is filed for the 500 the scan found.
