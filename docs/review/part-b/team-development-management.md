# Team Development Management

**Rubric (B4 · Issue tracking and code review for other members):** comment on other members' merge requests; approve only if there are no issues; work according to the tracked issues; comment with the link to the peer MR reviewed.

| Level | Requirement |
|---|---|
| 1 | Minimal comments, only "ok"/"LGTM", or just an approval |
| 2 | Comments summarise the positive and negative points of the code |
| 3 | Detailed comments with feasible suggestions, e.g. code smells |
| 4 | Detailed comments with significant, feasible performance-related suggestions |

**Proposed level: not yet claimable.** I have not reviewed a peer's merge request yet.

## Week of 15–21 Sep

### Issue tracking

- Work follows the Linear issue [PIL-176](https://linear.app/pilah-2/issue/PIL-176) under [PIL-140 CPBI-10](https://linear.app/pilah-2/issue/PIL-140); the branch name links it, so Linear tracks the PR automatically.

### Responding to review (received, not given)

Heraldo reviewed PR #19 with three findings; each was fixed test-first and answered in its thread:

- [Finding 1: membership gate](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062276107)
- [Finding 2: legacy sen rounding](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062584758)
- [Finding 3: same-instant ordering](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062276317)

This shows engagement with review, but the rubric measures reviews *given*.

## To do

- Review [PR #22](https://github.com/bank-sampah-PILAH/pilah-be/pull/22) (PIL-168, rounding rules). A concrete finding already exists: for nasabah with legacy data, the computed saldo history keeps its sen while #22 rounds the saldo itself down, so the two can disagree.
