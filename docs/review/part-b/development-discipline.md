# Development Discipline

!!! success "Competency level: 3"
    Four meaningful merge requests in week 1 (15–22 Sep), across both repositories, 57 commits in scoped Conventional Commits, each MR with a detailed description.

## Merge requests

| MR | Repo | Opened | Size | Commits | Reviewer |
|---|---|---|---|---|---|
| [#19 — PIL-176: record pencairan and update nasabah saldo](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | pilah-be | 20 Sep | +763 / −17, 10 files | 27 | HeraldoArman |
| [#26 — PIL-176: add pencairan recording for pengurus](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | pilah-mobile | 22 Sep | +1501 / −0, 21 files | 14 | HeraldoArman |
| [#32 — PIL-222: filter riwayat pencairan by periode and nasabah name](https://github.com/bank-sampah-PILAH/pilah-be/pull/32) | pilah-be | 22 Sep | +178 / −6, 4 files | 7 | HeraldoArman |
| [#27 — PIL-222: add riwayat pencairan for the bank and per nasabah](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | pilah-mobile | 22 Sep | +1038 / −56, 21 files | 9 | HeraldoArman |

All four merge requests:

- **Branch** follows the Linear-linked convention, the same name in both repos, so Linear links each PR to its issue automatically: `feature/pil-176-pencatatan-pencairan-untuk-pengurus` for PIL-176, and `feature/pil-222` for PIL-222 (the team's newer `feature/<issue-id>` form).
- **Title** follows the team format `PIL-XXX: <what it does>`.
- **Description** covers the summary, key changes, testing with the exact validation commands, and notes for the reviewer: dependencies, merge order, design decisions, and anything unusual in the history, disclosed openly.
- **Worked in an isolated worktree** following the team's `ship` workflow. PIL-222 is stacked on PIL-176 (#32 on #19, #27 on #26), since it extends code that is not merged yet.
- **Review requested** from Heraldo through the team's `ask-for-review` skill, which assigns the GitHub reviewer and posts to Discord.
- **CI green** before requesting review.

## 15–21 Sep

**[pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19)**, 23 commits.

- **20 Sep (17 commits):** the PIL-176 backend, test-first. Each behaviour is a `test(pencairan): add failing test for …` commit followed by the `feat(pencairan): …` that makes it pass.
- **21 Sep (6 commits):** all three review findings fixed, each as a failing test then a fix, and answered in its review thread.
- Stacked on [#18](https://github.com/bank-sampah-PILAH/pilah-be/pull/18) to resolve a migration-number clash, with the migration renumbered in its own commit.

```text
test(pencairan): add failing test for insufficient saldo
feat(pencairan): reject nominal above nasabah saldo
fix(pencairan): require approved membership like setoran
fix(pencairan): renumber migration to follow nasabah approval
```

## 22 Sep

**Three new merge requests, and #19 revised.**

### [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26), 14 commits — PIL-176 mobile

- Scaffolded with the team's SPL CLI, then built slice by slice: validation → data layer → form state → form page → entry point, each a failing test commit then the implementation.
- Formatting kept in separate `style(...)` commits, following the repo's existing convention.
- `di.config.dart` limited to the feature's own registrations, keeping unrelated generator reordering out of the diff.

### [pilah-be #32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32), 7 commits — PIL-222 backend

- Period and name-search filters on the pencairan list, reusing the transaksi period logic instead of copying it.
- Coverage-only tests committed as `test(...): cover …`, not labelled as failing tests.

### [pilah-mobile #27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27), 9 commits — PIL-222 mobile

- Riwayat page for the bank and per nasabah, built slice by slice: data layer → cubit → page → entry points.

### [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) revised, 4 commits + 1 merge

- Removed an unreachable code branch; added a missing verification check with its failing test first; fixed a test that failed on Postgres only, after CI caught it.
- Retargeted to `staging` once #18 merged, and brought `staging` in with a merge instead of a rebase, so there was no force-push and the review comments stayed attached.

```text
chore(pencairan): scaffold feature with SPL CLI
feat(pencairan): filter riwayat pencairan by periode
test(pencairan): cover bank scoping of filtered riwayat (OWASP A01)
feat(pencairan): open riwayat pencairan from the dashboard and nasabah detail
```
