# Development Discipline

!!! success "Competency level: 3"
    Four stacked merge requests (PIL-222 and PIL-230) in scoped Conventional Commits with the TDD phase in each subject, plus review revisions on four PRs, all with green CI.

## Merge requests

| MR | Repo | Opened | Size | Commits | Reviewer |
|---|---|---|---|---|---|
| [#32 — PIL-222: filter riwayat pencairan by periode and nasabah name](https://github.com/bank-sampah-PILAH/pilah-be/pull/32) | pilah-be | 22 Sep | +178 / −6, 4 files | 8 | HeraldoArman |
| [#27 — PIL-222: add riwayat pencairan for the bank and per nasabah](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | pilah-mobile | 22 Sep | +1038 / −56, 21 files | 9 | HeraldoArman |
| [#52 — PIL-230: edit pencairan with revision history](https://github.com/bank-sampah-PILAH/pilah-be/pull/52) | pilah-be | 26 Sep | +769 / −11, 8 files | 26 | — |
| [#33 — PIL-230: edit pencairan and view its change history](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/33) | pilah-mobile | 26 Sep | +1509 / −3, 24 files | 15 | — |

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

## 26 Sep — PIL-230 and the second review round on #19

### Requirements settled before code

PIL-230 arrived as "edit pencairan" with no description. Before writing code I checked it against the SDS, whose BR-08 makes transaksi append-only, and put the open questions to the PO and lead: recompute later receipts? limit on backdating? reason required? what the nasabah sees? The agreed answers went into the [Linear issue](https://linear.app/pilah-2/issue/PIL-230) the same day, so the PRs implement a written decision rather than a chat thread.

### Commits that name their phase

From PIL-230 on, each TDD commit states its phase in the subject, so the red-green sequence reads straight from `git log`:

```text
test(pencairan): [RED] add failing test for recomputing later snapshots
feat(pencairan): [GREEN] recompute later pencairan snapshots after an edit
test(pencairan): cover edits that would overdraw a later pencairan
```

Coverage tests, docs and formatting keep plain subjects (`test(...): cover …`, `docs(...)`, `style(...)`), so a tag always means a real red or green step.

### Keeping a stack mergeable

Staging moved 42 commits while #19 was in review, and gained its own `0012` merge migration next to #19's `0012_pencairan`. GitHub still showed #19 as mergeable, because the files do not conflict as text, but `migrate` would have failed with two leaf nodes. I merged `staging` into #19 and added `0013_merge_pencairan_and_nasabah_email` ([`9a89c01`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9a89c01)); CI on Postgres passed afterwards.

I then test-merged every open backend PR against #19 with `git merge-tree` and commented on the nine with a real conflict (text, migration graph or a clashing permission class), rather than on every PR that merely touches the same files. PIL-230 was stacked on #32 and #27 the same way as PIL-222, with its own migration flagged in the PR description as needing a `makemigrations --merge` once the stack is combined. Merging the stack is left to the lead.

| PR | Commits |
|---|---|
| [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) (review fixes) | [`9a89c01`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9a89c01) … [`8349b37`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8349b37), 11 commits |
| [pilah-be #52](https://github.com/bank-sampah-PILAH/pilah-be/pull/52) | [`e37bbf4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e37bbf4) … [`011fda3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/011fda3), 26 commits |
| [pilah-mobile #33](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/33) | [`5509100`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5509100) … [`4a52399`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4a52399), 15 commits |
