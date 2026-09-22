# Development Discipline

**Rubric (B3 · Daily commit and merge request following Git Flow):** descriptive commit messages; a complete merge request before merging; comment with the commit or MR link.

| Level | Requirement |
|---|---|
| 2 | Messages not very descriptive; only one merge request per week |
| 3 | Good messages, standard quality, reasonable quantity; **at least two merge requests** |
| 4 | Very helpful, detailed messages; above-average quality and quantity; more than two merge requests |

A merge request only counts if it is meaningful and beneficial to the project.

**Proposed level: 2 for 15–21 Sep** (one MR). Level 3 needs a second MR in the week of 22–28 Sep.

## Week of 15–21 Sep

- **One merge request:** [pilah-be PR #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19). Its description covers the summary, key changes, the design decision, out-of-scope items, and the exact validation commands.
- **Conventional Commits, scoped and imperative**, e.g. `test(pencairan): add failing test for insufficient saldo`, `feat(pencairan): reject nominal above nasabah saldo`.
- **Branch naming** follows the Linear-linked convention: `feature/pil-176-pencatatan-pencairan-untuk-pengurus`.
- **Work in an isolated worktree** off `staging`, following the team workflow.

## Week of 22–28 Sep

- PR #19 retargeted to `staging` after #18 merged; `staging` merged in instead of force-pushing, so review comments stay attached.
- Second MR: _pending_ (mobile side of PIL-176, or a smaller fix).
