# AI Literacy

!!! success "Competency level: 3"
    AI used critically:

    - **Claims checked before acting:** by writing the failing test first, by sending an attack by hand, and by running the same check on a clean `staging`.
    - **Results not trusted when the run was broken:** a scan on a full disk was redone rather than reported, and every 5xx was classified before any was called a finding.
    - **Work stopped rather than guessed at** when the cause couldn't be confirmed (PIL-475, the Gmail finding).
    - **Its own mistake owned:** the leaked webhooks in this week's scan evidence, caught on 13 Nov, are written up, not quietly removed.

    Decisions with product or team impact were put to me: which issue to take, what PIL-481 should keep, and when to merge.

Evidence for this week:

- The PRs, reviews and reports linked below, each of which records the checks described here. The prompts themselves aren't published.

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code, across `pilah-be`, `pilah-mobile` and `pilah-docs`. Linear through Composio; GitHub through `gh`; SonarCloud through its API; Playwright against local builds; OWASP ZAP through its API; PostgreSQL 16 through `pgserver`.
- **Guardrails:** the workspace skills (`ship`'s worktree layout, `tdd`), CI's own commands run locally before every push, and rules kept in memory and applied without being restated:
    - the TDD phase in every commit subject;
    - the design issue, pattern and origin, and the OWASP categories, in each commit body;
    - a ZAP scan of each finished sub-issue;
    - replies inside each review thread, with permalinks;
    - startable issues only, when choosing what to take.
- **My role:** picking the issue (I set PIL-476 and PIL-475 aside and took PIL-481), pointing the agent at the UAT's decision and at my earlier void PR, asking for the reviews to be answered, and freeing the disk when the scan failed.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| *4 Nov:* Writing the test for Heraldo's dialog finding | A third test, written to stage the race, **found a bug nobody had reported**: an answer arriving during the dialog's exit animation closed the Riwayat page underneath. It was fixed in the same pair. Then it undid each fix in turn to check that exactly one test failed each time. |
| *4 Nov:* Scallss's stale-screens finding | It found that edit has the same gap on `staging`, and **didn't widen the PR** to fix it, since Scallss agreed it's a separate follow-up. It said so in the reply. |
| *4 Nov:* Heraldo's seed finding | Before fixing the two seeds, it **checked every other place that sums setoran** outside the tests, so the fix could say these were the only gap, not just the reported ones. |
| *9 Nov:* PIL-475 | The root cause couldn't be confirmed from the code. It **stopped and wrote reproduction steps** rather than ship a guess. |
| *9 Nov:* "Google login opens Gmail" on mobile web | Traced through the login flow, it found no code path that opens Gmail. It **said so and deferred it**, asking for the tester's device, browser and the tapped control, rather than change the login on a hunch. |
| *9 Nov:* PIL-481 scope | The issue reversed last week's design. Once I pointed it at the UAT's recorded decision, it **kept what the decision didn't remove**: the row and its detail by id, each pinned by a guard test so the fix couldn't overreach. |
| *9 Nov:* The first ZAP run | About 160 of the 5xx were `OperationalError` or `No space left on device`. It **classified them as the machine's fault**, asked me to free the disk, and re-ran both scans. The report uses only the second run. |
| *9 Nov:* Three High alerts | It **reproduced each by hand.** It sent both SQL-injection payloads itself and showed the difference came from the setoran already being voided. It traced the other two to a real 500, which became PIL-482. |
| *10 Nov:* Red CI on #167 and #168 | It **ran the failing test on a clean `staging`**, showed it fails there too (its fixture dates had aged out), and found the fix waiting in PIL-239, rather than change the PRs. |
| *9 Nov → 13 Nov:* The webhooks in the scan evidence | It had redacted the names it knew to look for and claimed a secrets check it hadn't done. When GitHub flagged the webhooks, it **corrected the report's claim**, redacted the files, and made the scan script refuse that class of secret. |

## Memory as working data

- **Rules applied unprompted:** the conventions above shaped every commit, PR, reply and scan this week without my restating them.
- **Rules that changed this week's output:**
    - "a ZAP scan per finished sub-issue" produced the 9 Nov report and PIL-482;
    - "prefer independent issues" shaped the list of what I could take on 9 Nov;
    - "reply in review threads" and "embed links" shaped all six replies on #145 and #193.
- **Saved from what went wrong:** start the scan backends with a clean environment (saved on 13 Nov, after the leak).
