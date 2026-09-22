# AI Literacy

**Rubric (Responsible use of AI):** show the type of AI used during development, with the prompt history as evidence.

| Level | Requirement |
|---|---|
| 2 | AI used mostly copy-paste or instant help, without adequate analysis and verification |
| 3 | AI used critically and responsibly; its responses are analysed and critiqued to improve the work |
| 4 | AI used strategically, backed by data; usage patterns tracked and used to improve the workflow |

**Proposed level: 3**

## How AI was used

- **Tool:** Claude Code as an agent in VS Code, working in the repository: reading code, running tests and checks, committing, and opening the PR.
- **Guardrails:** the team's workspace skills (`ship` for the branch/worktree/PR workflow, `tdd` for red-green commits) and CI (ruff, mypy strict, coverage, SonarQube).
- **My role:** deciding scope and priorities, relaying team decisions (stacking on #18, the rounding rule), approving outward actions (force-pushes, PR comments), and asking for verification before trusting results.

## Week of 15–21 Sep — where verification changed the outcome

| Situation | What verification found |
|---|---|
| Asked to renumber the migration to `0012` before #18 merged | It would reference a migration that did not exist yet (`NodeNotFoundError`) and break every test; we stacked on #18 instead |
| "Re-check before making the PR" | Confirmed the branch was current with `staging`, the diff held only the intended files, and no secrets were committed; found a second PR using the same migration number |
| A test written after its fix | Proved it catches the bug by disabling the fix and watching it fail |
| An ordering bug that "seemed fine" | Showed it was nondeterministic: 6 of 10 runs passed before the fix, 10 of 10 after |
| Production environment values considered for local testing | Not used: they would break tests and point local runs at the production database |
| AI's claim that PR #22's rounding needed a PO decision | Corrected after reading #22's code: the policy was already set there |

## Week of 22–28 Sep

| Situation | What verification found |
|---|---|
| All tests passed locally on SQLite | CI on Postgres failed: a `flush` inside a transaction is rejected by Postgres. Diagnosed from the CI log and fixed in [`ad7d55f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ad7d55f). Lesson: local SQLite is not proof; wait for CI |
| A test failed after merging `staging` | Diagnosed as a local `.env` artifact rather than "fixing" the test; confirmed by rerunning the way CI does |
| "100% coverage" | Separated precisely: 100% of my new code vs 90% of the project, measured by two tools that agree |

## Prompt history

!!! note "To attach"
    Export of the Claude Code session (`/export`) as the required prompt-history evidence.
