# Development Discipline

!!! success "Competency level: 2 (15–21 Sep) · 3 (22–28 Sep)"
    One merge request in the first week; two merge requests worked in the second (pilah-mobile #26 opened, pilah-be #19 revised after review), all with descriptive Conventional Commits.

## Merge requests

| MR | Repo | Opened | Size | Commits | Reviewer |
|---|---|---|---|---|---|
| [#19 — PIL-176: record pencairan and update nasabah saldo](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | pilah-be | 20 Sep | +763 / −17, 10 files | 27 | HeraldoArman |
| [#26 — PIL-176: add pencairan recording for pengurus](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | pilah-mobile | 22 Sep | +1501 / −0, 21 files | 14 | HeraldoArman |

Both merge requests:

- **Branch** follows the Linear-linked convention, the same name in both repos: `feature/pil-176-pencatatan-pencairan-untuk-pengurus`. Linear links both PRs to PIL-176 automatically.
- **Title** follows the team format `PIL-XXX: <what it does>`.
- **Description** covers the summary, key changes, testing with the exact validation commands, and notes for the reviewer: dependencies, design decisions, and anything unusual in the history, disclosed openly.
- **Worked in an isolated worktree** off `staging`, following the team's `ship` workflow.
- **Review requested** from Heraldo through the team's `ask-for-review` skill, which assigns the GitHub reviewer and posts to Discord.
- **CI green** before requesting review.

## Week of 15–21 Sep

**One merge request: [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19)**, 23 commits.

- **20 Sep (17 commits):** the backend feature, test-first. Each behaviour is a `test(pencairan): add failing test for …` commit followed by the `feat(pencairan): …` that makes it pass.
- **21 Sep (6 commits):** all three review findings fixed, each as a failing test then a fix, and answered in its review thread.
- Stacked on [#18](https://github.com/bank-sampah-PILAH/pilah-be/pull/18) to resolve a migration-number clash, with the migration renumbered in its own commit.

Example commit messages:

```text
test(pencairan): add failing test for insufficient saldo
feat(pencairan): reject nominal above nasabah saldo
fix(pencairan): require approved membership like setoran
fix(pencairan): renumber migration to follow nasabah approval
```

## Week of 22–28 Sep

**Two merge requests worked.**

### New: [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26), 14 commits

- Scaffolded with the team's SPL CLI, then built slice by slice: validation → data layer → form state → form page → entry point. Each slice is a failing test commit, then the implementation.
- Formatting kept in separate `style(...)` commits, following the repo's existing convention.
- `di.config.dart` limited to the feature's own registrations (+17 lines), keeping unrelated generator reordering out of the diff.

```text
chore(pencairan): scaffold feature with SPL CLI
test(pencairan): add failing test for the pencairan form cubit
feat(pencairan): manage saldo loading and submission in the form cubit
feat(pencairan): open catat pencairan from the nasabah detail sheet
```

### Revised: [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19), 4 commits + 1 merge

- Removed an unreachable code branch and added a missing verification check (with its failing test first).
- Fixed a test that failed on Postgres only, after CI caught it.
- Retargeted to `staging` once #18 merged, and brought `staging` in with a merge instead of a rebase, so there was no force-push and the review comments stayed attached.

```text
refactor(pencairan): drop unreachable unpaginated list branch
test(reset): add failing test for pencairan in reset verification
fix(reset): run reset command tests outside a transaction for postgres
```
