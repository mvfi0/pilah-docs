# Development Discipline

!!! success "Competency level: 3"
    Three new merge requests this week, plus a second review round on last week's two:

    - [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) and [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193): the backend and mobile halves of my assigned PIL-428, 16 and 17 commits;
    - [pilah-mobile #196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196): PIL-435, 4 commits;
    - [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) and [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174): 4 and 6 new commits answering seven review findings.

    Each uses the Linear branch name (`feature/pil-428`, `feature/pil-435`) off `staging`. Every commit is a scoped Conventional Commit:

    - the TDD phase is in each subject;
    - the OWASP category is in the subject where it applies;
    - the body names the design issue, the pattern and its origin.

    Each description has the contract, the behaviour, screenshots, the E2E results and the local validation. Descriptions are kept current after merges and review rounds. Fixes came as new commits, never force-pushed, and every review thread got a reply linking its fix.

## Merge requests

| MR | Opened | Size | Commits | CI / SonarCloud | Status (3 Nov) |
|---|---|---|---|---|---|
| [#145 — void (Hapus) a setoran and keep it out of saldo and laporan](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) | 31 Oct | +748 / −40, 20 files | 16 | green, gate passed, 0 issues, 100% | Open. Reviewed by Gabriel (2 Nov): no defect found, three non-blocking points |
| [#193 — Hapus a setoran from the selection header and the web Aksi column](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) | 31 Oct | +980 / −85, 26 files | 17 | green, gate passed, 0 issues, 100% | Open. `staging` merged in on 2 Nov. Reviewed by Gabriel (2 Nov): no defect found, two non-blocking points |
| [#196 — show setoran only in Riwayat Aktivitas](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196) | 31 Oct | +277 / −65, 8 files | 4 | green, gate passed, 0 issues, 100% | Open, no review yet |
| [#137 — PIL-451 backend](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (from last week) | 26 Oct | +565 / −5, 11 files | 17 | green, gate passed, 0 issues, 100% | Second round of findings fixed and answered |
| [#174 — PIL-451 mobile](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (from last week) | 26 Oct | +757 / −32, 18 files | 20 | green, gate passed, 0 issues, 100% | Second round fixed and answered; `staging` merged in |

Sizes and commit counts are from GitHub on 2 Nov.

## From issue to merge request

1. **Design choices asked, not assumed.** PIL-428 left three choices open:
    - where Hapus lives on a phone;
    - whether the alasan is required;
    - where a voided setoran still appears.

    I picked from listed options before any code: the existing hold-to-select header, a required alasan, and Riwayat only.
2. **The CPBI read for the acceptance criteria.** PIL-435 had no description. Its parent CPBI-31 says "tidak ada menu mati", so the type selector is hidden, not left disabled. The PR says so.
3. **One branch name in both repos** (`feature/pil-428`), so Linear links both PRs to the issue. The two PRs link to each other.
4. **Test-first, in slices:** seven red/green pairs on the backend, seven on mobile, and a refactor-first change on #196. The tables are on the [TDD page](tdd.md).
5. **CI's own checks run locally before each push:**
    - backend: ruff, strict mypy, `makemigrations --check`, the suite on Postgres 16, diff coverage, and the migration on the 20 Sep production snapshot;
    - mobile: `dart format`, `flutter analyze --fatal-infos`, the full suite, diff coverage, and the web build;
    - Playwright E2E for both web PRs.
6. **Conflicts checked across every open PR.** For each one I compared touched files, ran `git merge-tree` and listed new migrations. The one real clash was two `0029` migrations on #137 and #145, which Git can't see. I flagged it on [both](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#issuecomment-6542913917) [PRs](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#issuecomment-6542914469).

## Changes after the MR was open

- **#193, after `staging` moved** (2 Nov):
    - `staging` brought PIL-453's inline setoran detail. I merged it in [`0c6f1e7`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/0c6f1e72), carrying over only behaviour that already had tests.
    - The missing Pembatalan section came as its own red/green pair, [`5af4e5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5af4e5da) → [`ef7a0b9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef7a0b96).
    - SonarCloud's S3358 on the merged code was fixed in [`ca2ec7a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca2ec7a2).
    - The screenshots and description were redone from a fresh E2E run (21/21).
- **#145:** [`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0) names the counted-setoran rule once, with a "Refactor" section added to the description.
- **#137, second round** (Tristan, Heraldo): red [`c428c32`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c428c32), green [`d19cb8d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d19cb8d), and two refactors, [`7c7c1f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7c7c1f3) and [`e077084`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e077084).
- **#174, second round** (Tristan, Scallss, Heraldo):
    - the `staging` merge [`3ec78be`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3ec78bea), which reconciled the new consent step with account mode;
    - red [`26dce38`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26dce385) and green [`3d0a81b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3d0a81b3);
    - a spacing fix, [`6eef5a4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6eef5a43);
    - a coverage test, [`240c78a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/240c78af);
    - and the S3776 refactor, [`8bdb1b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8bdb1b54).

    Each of the seven threads got a reply linking its fix ([Team Development Management](team-development-management.md#reviews-received)).

## Example commit messages

```
feat(ledger): [GREEN] enforce a complete void record in the database (OWASP A08)
```

```
refactor(ledger): [REFACTOR] read counted setoran through Transaksi.objects.tercatat() (PIL-428)

The void left the same rule, "a voided setoran counts toward nothing",
written as filter(status=Transaksi.Status.TERCATAT) in nine places
across ledger, reporting and nasabah. The next report would have to
remember it, and one that forgot would quietly count voided money.

TransaksiQuerySet.tercatat() now names the rule once and is the default
manager's queryset, so related managers (nasabah.transaksi) have it too.
...
No behaviour change: the full suite gives the same result (only the 5
known Windows deployment-script failures), diff coverage 100% of 348
lines, strict mypy and makemigrations --check clean.

Design issue: duplicated domain rule (shotgun surgery risk).
Pattern: custom QuerySet method as a named query (Query Object /
Specification, PoEAA; Principle: DRY). Origin: own refactor, found while
documenting the week.
```

```
test(onboarding): [RED] add failing tests for the Google-login membership claim racing a role change (PIL-451, OWASP A04)

Review on #137 (Tristan P1, Heraldo): login_with_google claims a
pengurus-entered membership in _sync_nasabah_prefill without the account
row lock the other three onboarding writers take.

- Race (PostgreSQL, two threads): the login pauses just before it saves
  the link, a role change to pengelola runs. The change must wait and
  then refuse with role_locked. Fails: {'changed': True,
  'waited_for_registration': False}, the role flips under the claim.
- The other ordering, single-threaded: the login read the account as
  nasabah, then the role changed. The claim must link nothing and still
  sign in. Fails: Nasabah.clean's ValidationError escapes and
  GoogleAuthView answers 401 "ID Token invalid atau expired".
```

The backend PIL-428 subjects, oldest first, read as a sequence of phases:

```
test(ledger): [RED] add failing test for voiding a setoran (OWASP A09)
feat(ledger): [GREEN] void a setoran and record who, when and why
test(ledger): cover alasan, bank scoping and pengurus-only voiding (OWASP A01)
test(ledger): [RED] add failing tests that a voided setoran is final (OWASP A04)
feat(ledger): [GREEN] refuse to void, edit or send a voided setoran
test(ledger): [RED] add failing tests for voiding money already paid out (OWASP A04)
feat(ledger): [GREEN] shift later pencairan on void and refuse paid-out setoran
test(ledger): [RED] add failing tests that voided setoran leave the saldo history
feat(ledger): [GREEN] leave voided setoran out of saldo history and summaries
test(reporting): [RED] add failing tests that laporan skip voided setoran
feat(reporting): [GREEN] leave voided setoran out of exports, dashboard and statement
test(nasabah): [RED] add failing tests for voided setoran in nasabah views
feat(nasabah): [GREEN] show voided setoran as dibatalkan and stop counting them
test(ledger): [RED] add failing test that the database refuses a half-recorded void (OWASP A08)
feat(ledger): [GREEN] enforce a complete void record in the database (OWASP A08)
refactor(ledger): [REFACTOR] read counted setoran through Transaksi.objects.tercatat() (PIL-428)
```

## Status and what is left

- **#145 and #193:** Gabriel reviewed both on 2 Nov ([#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145), [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193)). He traced every query site for a place a voided setoran still counts and found none. His points are all non-blocking:
    - #145: the enum in the constraint, an index for `Transaksi`, and how the statement PDF shows a void;
    - #193: null-safety order, and trimming the alasan.

    They're answered next. **#196** has no review yet and goes through the team's `ask-for-review` skill.
- **#137 and #174:** the reviewers need to re-check and approve. Nothing merges without approval.
- **The migration clash:** whichever of #137 and #145 merges second renumbers its `0029` to `0030`.
