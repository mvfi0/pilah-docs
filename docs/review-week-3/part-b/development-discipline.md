# Development Discipline

!!! success "Competency level: 3"
    Seven merge requests this week: PIL-304 and PIL-331 on both repositories, a follow-up that kept a review promise, a scope split asked for in review, and a fix to the app's generated dependency graph. All use scoped Conventional Commits with the TDD phase in each subject. Each has a detailed description and green CI. Every review or CI finding was fixed on the branch and answered in its thread.

## Merge requests

| MR | Repo | Opened | Size | Commits | Review |
|---|---|---|---|---|---|
| [#79 — PIL-304: versioned jenis sampah prices with an effective date](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) | pilah-be | 7 Oct | +1094 / −104, 27 files | 37 | waiting |
| [#62 — PIL-304: change a price now or from a date, with the BR-03 warning](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) | pilah-mobile | 7 Oct | +892 / −7, 23 files | 18 | waiting |
| [#89 — refactor(pencairan): round pencairan saldo through kalkulasi.bulatkan_rupiah](https://github.com/bank-sampah-PILAH/pilah-be/pull/89) | pilah-be | 8 Oct | +57 / −6, 2 files | 4 | Twentism (Gabriel) |
| [#92 — PIL-331: price history per jenis sampah](https://github.com/bank-sampah-PILAH/pilah-be/pull/92) | pilah-be | 11 Oct | +195 / −4, 5 files | 8 | approved by TrayMachi (Tristan) |
| [#73 — PIL-331: price history per jenis sampah](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73) | pilah-mobile | 11 Oct | +797 / −6, 24 files | 22 | TrayMachi (Tristan), 2 findings fixed |
| [#74 — fix(di): cover the generated DI graph](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) | pilah-mobile | 11 Oct | +381 / −8, 7 files | 12 | TrayMachi (Tristan), conflict and 1 finding fixed |
| [#96 — Allow-list the jenis list filters (OWASP A03)](https://github.com/bank-sampah-PILAH/pilah-be/pull/96) | pilah-be | 12 Oct | +46 / −10, 3 files | 2 | waiting |

Sizes and commit counts are from GitHub: 9 Oct for the first three, 13 Oct for the rest. Tristan reviewed #79 and #62 on 11 Oct (3 and 2 findings, all fixed on 12 Oct).

**Conventions followed on all three:**

- **Branches:** the issue's Linear branch (`feature/pil-304`), or a derived `fix/…` name when there is no issue.
- **Worktrees:** a separate worktree per branch, so `staging` stays clean.
- **Commits:** scoped Conventional Commits with `[RED]`/`[GREEN]`/`[REFACTOR]` in the subject, and a body when the *why* isn't obvious.
- **PR descriptions:** summary, API changes, security, migration safety and the exact validation commands, with permalinks to the lines that matter.
- **Ownership:** assigned to myself; the merge is left to the lead.

## Why seven, and how they stack

- **#79 and #62 are one feature split by repository.** The descriptions link each other, and #79 says which merges first. It can go first because older app builds keep working against it.
- **PIL-331 stacks on PIL-304** because it reads PIL-304's version table: #92 targets `feature/pil-304`, and #73 targets #62's branch. Each PR's diff therefore shows only its own feature, and they merge in order.
- **#96 was split out in review.** Tristan noted the filter allow-list was outside PIL-304's scope. Instead of force-pushing #79, I reverted it there ([`98456ff`](https://github.com/bank-sampah-PILAH/pilah-be/commit/98456ff)) and re-applied the same two commits with `cherry-pick -x` as #96, stacked on #92: `staging` ← #79 ← #92 ← #96. The history and the commit links in last week's evidence stay valid.
- **#74 fixes something the coverage work uncovered.** It touches the app's dependency graph and CI, not PIL-304 or PIL-331, so it has its own branch off `staging`.
- **#89 is a follow-up I promised** in Heraldo's review thread on PIL-176 ([#19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4061633460)): replace the inline rounding with `kalkulasi.bulatkan_rupiah` once #22 landed. It touches unrelated code, so it got its own branch instead of riding on #79. The #19 thread has a reply linking it ([reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4215462955)).

## Example commit messages

```
test(harga): [RED] add failing test for rejecting backdated or ambiguous berlaku_mulai (OWASP A04)
feat(harga): [GREEN] reject backdated, far-future and offsetless berlaku_mulai (OWASP A04)

A price change can only start now or later (BR-03: no retroactive
prices), at most 365 days ahead, and berlaku_mulai must carry its UTC
offset: a bare local time would be read as UTC and land hours off for a
bank sampah in WIB, WITA or WIT.
```

```
refactor(harga): [REFACTOR] break berlaku_mulai ties on the newest row explicitly

The id is a BigAutoField, so "-id" is insertion order on every database.
Without it Postgres may return either of two versions that start at the
same time.
```

## Keeping the branch mergeable

- **The `pull_request` CI failed** with 13 errors after Pascal's [#74](https://github.com/bank-sampah-PILAH/pilah-be/pull/74) landed on `staging` with new tests that set the dropped `harga_per_kg` column. I merged `staging` in rather than rebasing, so no review thread lost its anchor. Then [`b18b50f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b18b50f) moved those tests onto price versions. One test needed a rewrite, not a rename: a price can no longer be 0, so "a jenis without a price" now means "no version in effect".
- **SonarCloud findings were fixed on the branch** before review: a composite assertion on #79 ([`fe5db58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fe5db58)) and a nested ternary on #62 ([`2ce3dab`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2ce3dab)). See [Code Quality](code-quality.md).
- **Gabriel's review on #89** was answered with a test and a comment fix ([`3c806e5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c806e5), [`29dc7e7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/29dc7e7)) and a [reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/89#issuecomment-6076869250).
- **Tristan's review round (11–12 Oct)** had 8 findings over #79, #62, #73 and #74. Each was checked against the code first, then fixed test-first, then answered in its own thread with the commit links. Examples: the seed repricing historical setoran ([thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247272237)), and a list reload race ([thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4247489545)). See [Team Development Management](team-development-management.md).
- **#74 kept up with `staging`.** `staging` moved twice while #74 was open. I merged it in both times, resolved the conflict in favour of Tristan's identical fix from #71, and added the new registrations to the dependency-graph test.
- **Every push was validated locally first**, with CI's own commands. Backend: ruff, ruff format, mypy strict, the migration check, tests on SQLite and on Postgres 16, coverage and diff-cover. Mobile: `dart format`, `flutter analyze --fatal-infos`, `flutter test --coverage` and diff-cover, on the Flutter version CI pins (3.41.3).
