# Team Development Management

!!! note "Competency level: not yet claimable"
    Reviews received and answered, and reviews requested through the team tooling, but no review of a peer's merge request given yet.

## Week of 15–21 Sep

### Issue tracking

- Work follows the Linear issue [PIL-176](https://linear.app/pilah-2/issue/PIL-176) under [PIL-140 CPBI-10](https://linear.app/pilah-2/issue/PIL-140); the branch name links it, so Linear tracks the PR automatically.

### Responding to review (received, not given)

Heraldo reviewed PR #19 with three findings; each was fixed test-first and answered in its thread:

- [Finding 1: membership gate](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062276107)
- [Finding 2: legacy sen rounding](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062584758)
- [Finding 3: same-instant ordering](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062276317)

This shows engagement with review, but the rubric measures reviews *given*.

## Week of 22–28 Sep

- Requested review from Heraldo on [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) and [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) through the team's `ask-for-review` skill, which assigns the GitHub reviewer and posts the request to Discord.

## To do

- Review [PR #22](https://github.com/bank-sampah-PILAH/pilah-be/pull/22) (PIL-168, rounding rules). A concrete finding already exists: for nasabah with legacy data, the computed saldo history keeps its sen while #22 rounds the saldo itself down, so the two can disagree.
