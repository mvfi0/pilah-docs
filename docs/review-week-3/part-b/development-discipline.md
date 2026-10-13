# Development Discipline

!!! success "Competency level: 3"
    Three merge requests this week (PIL-304 on both repositories, plus a follow-up that kept a review promise), in scoped Conventional Commits with the TDD phase in each subject. Each has a detailed description and green CI, and every review or CI finding was fixed on the branch before asking for merge.

## Merge requests

| MR | Repo | Opened | Size | Commits | Review |
|---|---|---|---|---|---|
| [#79 — PIL-304: versioned jenis sampah prices with an effective date](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) | pilah-be | 7 Oct | +1094 / −104, 27 files | 37 | waiting |
| [#62 — PIL-304: change a price now or from a date, with the BR-03 warning](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) | pilah-mobile | 7 Oct | +892 / −7, 23 files | 18 | waiting |
| [#89 — refactor(pencairan): round pencairan saldo through kalkulasi.bulatkan_rupiah](https://github.com/bank-sampah-PILAH/pilah-be/pull/89) | pilah-be | 8 Oct | +57 / −6, 2 files | 4 | Twentism (Gabriel) |

Sizes and commit counts are from GitHub on 9 Oct.

**Conventions followed on all three:**

- **Branches:** the issue's Linear branch (`feature/pil-304`), or a derived `fix/…` name when there is no issue.
- **Worktrees:** a separate worktree per branch, so `staging` stays clean.
- **Commits:** scoped Conventional Commits with `[RED]`/`[GREEN]`/`[REFACTOR]` in the subject, and a body when the *why* isn't obvious.
- **PR descriptions:** summary, API changes, security, migration safety and the exact validation commands, with permalinks to the lines that matter.
- **Ownership:** assigned to myself; the merge is left to the lead.

## Why three, and why the third is separate

- **#79 and #62 are one feature split by repository.** The descriptions link each other, and #79 says which merges first. It can go first because older app builds keep working against it.
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
- **Every push was validated locally first**, with CI's own commands. Backend: ruff, ruff format, mypy strict, the migration check, tests on SQLite and on Postgres 16, coverage and diff-cover. Mobile: `dart format`, `flutter analyze --fatal-infos`, `flutter test --coverage` and diff-cover, on the Flutter version CI pins (3.41.3).
