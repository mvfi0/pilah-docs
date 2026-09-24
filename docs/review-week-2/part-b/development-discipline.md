# Development Discipline

!!! success "Competency level: 3"
    Two stacked merge requests for PIL-222, 17 commits in scoped Conventional Commits, plus review revisions on three PRs, all with green CI.

## Merge requests

| MR | Repo | Opened | Size | Commits | Reviewer |
|---|---|---|---|---|---|
| [#32 — PIL-222: filter riwayat pencairan by periode and nasabah name](https://github.com/bank-sampah-PILAH/pilah-be/pull/32) | pilah-be | 22 Sep | +178 / −6, 4 files | 8 | HeraldoArman |
| [#27 — PIL-222: add riwayat pencairan for the bank and per nasabah](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | pilah-mobile | 22 Sep | +1038 / −56, 21 files | 9 | HeraldoArman |

Both follow the same conventions as week 1: Linear-linked branch name (`feature/pil-222`, the team's newer `feature/<issue-id>` form, agreed on 22 Sep), `PIL-XXX:` title, a description covering summary, changes, testing commands and reviewer notes, work in an isolated worktree, review requested through the `ask-for-review` skill, and CI green first.

## Stacking

PIL-222 extends code that is not merged yet, so each MR is stacked on its PIL-176 counterpart: #32 on #19, #27 on #26. The PR descriptions state the merge order, and when the base branches gained their review fixes, the base was merged up into #27 ([`b592d99`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b592d99)) rather than rebased, so no force-push detached the review threads.

## Responding to review — 23–24 Sep

Heraldo reviewed all three open PRs and raised eight findings. Every one was verified against the code first, then fixed test-first and answered inside its own review thread:

| PR | Commits |
|---|---|
| [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | [`37ecee5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/37ecee5) → [`d1c7ba8`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d1c7ba8) |
| [pilah-mobile #27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | [`8358c87`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8358c87) → [`a6cdfe6`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a6cdfe6) |
| [pilah-be #32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32) | [`28fca9c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/28fca9c) |

```text
test(pencairan): add failing test for riwayat periode filter
feat(pencairan): filter riwayat pencairan by periode
test(pencairan): cover bank scoping of filtered riwayat (OWASP A01)
fix(pencairan): ignore stale riwayat responses and refuse a 1-char search
```

One finding was answered without a code change: the backend silently ignores an unrecognised `periode`, which is carried over from the transaksi list. Keeping the two lists consistent was worth more than rejecting the value, so it is documented in the README instead ([`28fca9c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/28fca9c)).
