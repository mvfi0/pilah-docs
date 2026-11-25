# AI Literacy

!!! success "Competency level: 3"
    AI used critically:

    - **Claims checked against the sources before they were published:** the Sprint 3 Week 2 and Week 3 pages, and the script for presenting them, were checked line by line against the commits, PRs and SonarCloud. Each figure that disagreed was corrected.
    - **Failures found and fixed, not papered over:** a scan that left the endpoint under test unscanned was rerun after the tooling was fixed, and the attack count was recounted from the backend log.
    - **Limits kept:** post-approval comments were weighed against the issue's scope instead of fixed by reflex, and an honest level 1 on Commitment was kept for two weeks rather than rounded up.

    Decisions with product or team impact were put to me: which self-reported time counts, whether to publish prompt history, and when to merge.

Evidence for this week:

- The PRs, review replies and reports linked below, each of which records the checks described here. The prompts themselves aren't published.

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code, across `pilah-be`, `pilah-mobile` and `pilah-docs`. Linear through Composio; GitHub through `gh`; SonarCloud through its API; OWASP ZAP through its API; PostgreSQL 16 through `pgserver`.
- **Guardrails:** the workspace skills and the rules kept in memory:
    - the TDD phase in every commit subject;
    - the design issue, pattern, origin, OWASP and SOLID notes in each commit body;
    - a ZAP scan of each finished sub-issue;
    - replies inside each review thread, with permalinks;
    - merging only approved PRs, and checking a merge by the PR's state.
- **New this week:** a rule I gave on 19 Nov, saved to memory: don't publish prompt-history files with the AI Literacy pages; cite the PRs and reviews instead. This page follows it.
- **My role:** choosing the issue, asking for the IR pages and the presentation script, answering which self-reported time counts, and deciding when to merge.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| *18 Nov:* Gabriel's comments on #175 and #176, after Heraldo's approvals | It **applied the 12 Nov scope rule**: each point was checked against the issue and answered in its thread with the reason, with permalinks to the code in question. Then the approved PRs were merged. |
| *19 Nov:* Commitment for Sprint 3 Weeks 2 and 3 | The measured time came to 8 h 29 min and 9 h 32 min. It **wrote level 1 for both weeks** rather than rounding up, and asked me which self-reported time to add instead of assuming. |
| *19 – 21 Nov:* Checking the S3W2 and S3W3 pages and script against the sources | Wrong figures were **found and corrected before they were presented**. Examples: a count of tests that was two, not "a dozen"; merge times given in UTC instead of WIB; an OWASP category listed as guarded in a week where nothing tested it; two names used for the same teammate; a broken anchor. |
| *21 Nov:* "Which TDD work is before the deadline?" | It **dated every commit and SonarCloud analysis** against each week's due Tuesday, and checked whether any app commit sat outside a PR. The only one was a docs commit, and the page says so. |
| *23 Nov:* The first ZAP run | ZAP reported "URL Not Found in the Scan Tree" for `POST /onboarding/nasabah`, the endpoint the feature depends on. It **didn't report a clean scan.** It scanned the path by hand, fixed the driver, rebuilt the database and reran everything. |
| *23 Nov:* Counting the attacks | A first draft said 227. Recounted from the backend's own log, which sees every request ZAP sent, it was **224 attacks** plus the drive's four POSTs, and the report says 224. |
| *23 Nov:* The scratch PostgreSQL stopped | It **owned the mistake**: it had deleted the lock file of a server still in recovery. It recorded that in the report's "What went wrong" and in memory, so the next scan waits for "ready" instead. |
| *23 Nov:* Heraldo's five follow-ups on #276 | Each was **checked against the code and the issue's scope.** None could create a wrong record, because the server refuses a duplicate, which the scan had just confirmed. So none was fixed in the PR, and each got its reason in the reply. |
| *23 Nov:* The conflict after #267 landed | It **kept both sides** instead of picking one: `staging`'s new onboarding layout, and #276's in-app page. Then it reran the 413 affected tests before pushing. |

## Memory as working data

- **Rules applied unprompted:** the conventions above shaped every commit, PR, reply and scan this week.
- **Rules that changed this week's output:**
    - the 12 Nov post-approval scope rule decided how the comments on #175, #176 and #276 were handled;
    - "a ZAP scan per finished sub-issue" produced the 23 Nov report;
    - "IR weeks end on their due Tuesday" fixed the date range of every timeline on these pages.
- **Saved from what happened this week:**
    - don't publish prompt history (19 Nov);
    - who is who in the team (two names, one teammate);
    - the 23 Nov scan lessons: how to sign in as the nasabah, how POST-only paths are now scanned, and not to touch a recovering PostgreSQL's lock file.
