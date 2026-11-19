# AI Literacy

!!! success "Competency level: 3"
    AI used critically:

    - **Claims checked before acting:** a teammate's tests were mutated rather than trusted, hashes recomputed rather than read off a screenshot, and a PR's "server-side" claim tested with a real request.
    - **Failures not papered over:** a scan attempt that ran the machine out of memory was discarded and rerun one scan at a time. A secret leaked by its own earlier work was redacted, the false claim in its report corrected, and the check that missed it extended.
    - **Limits kept:** no admin bypass of a teammate's open change request; no shared-CI change without an issue; no rewrite of git history to hide the leak.

    Decisions with product or team impact were put to me: how to plan the week's PRs, whether to post reviews as comments or approvals, and the rule for review comments after an approval.

Evidence for this week:

- The PRs, reviews and reports linked below, each of which records the checks described here. The prompts themselves aren't published.

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code, across `pilah-be`, `pilah-mobile` and `pilah-docs`. Linear through Composio; GitHub through `gh`; SonarCloud through its API; OWASP ZAP through its API; PostgreSQL 16 through `pgserver`.
- **Guardrails:** the workspace skills and rules kept in memory:
    - the TDD phase in every commit subject;
    - the design issue, pattern, origin, OWASP and SOLID notes in each commit body;
    - a ZAP scan of each finished PR;
    - replies inside each review thread, with permalinks;
    - merging only approved PRs.
- **New this week:** a rule I gave on 12 Nov, saved to memory. If review comments arrive after an approval, check each against the issue's scope. Ignore and merge when it's out of scope and not needed; fix it when it's in scope or a real bug. Either way, reply in the thread with the reason.
- **My role:** asking for the week's PRs to be planned and executed, choosing comment-only reviews for the PIL-478 pair, asking for the second ZAP attempt, and deciding when to merge.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| *11 Nov:* Red CI on #167 and #168 | It **cherry-picked the existing fix** for the date test (from PIL-239) instead of editing the test in my PRs, and said so in each thread. |
| *12 Nov:* Reviewing Gabriel's PIL-478 pair | It **sent the request the PR's claim depends on** (`PUT /onboarding/profile` as a pengelola with no date) and got 200 with the profile marked complete, so the claim was wrong. It **ran 10 mutants** to measure the tests instead of reading them: 6 caught, and the misses became concrete test suggestions. |
| *12 Nov:* "Is there a webhook for approvals?" | It checked both repos' workflows and found that the repo webhooks return 404 for my account (no admin). It **answered "no, and here is what is possible"**, and didn't open a CI change without a Linear issue. |
| *13 Nov:* The leaked webhooks | It **owned the mistake**: the redaction had missed them, and the report's "grepped for secrets" was false. It fixed the files, the report and the check, confirmed the check flags the original file, and didn't rewrite history to hide it. |
| *13 Nov:* Merging the PIL-451 PRs | Both had approvals, but Tristan's change request still stood. It **refused to use an admin bypass** and reported why. |
| *13 Nov:* Heraldo's three post-approval comments on #174 | It **applied the new scope rule**: each was checked, and the PR's description was corrected where his first comment was right. The reason for leaving each was given in its thread. On 16 Nov, when Tristan raised the first one as a P2, it was fixed. |
| *16 Nov:* The first attempt at the three scans | PostgreSQL and then ZAP died of memory exhaustion, and the disk reached 0 GB. It **stopped everything, set the evidence aside as invalid**, and reran the scans one at a time with fresh databases, a 1 GB heap cap and a clean environment. |
| *16 Nov:* Plan item 2 | Scallss had merged a NUL-safe `search` (#172) first. It **didn't duplicate his work**: #177 took his PR's listed follow-up instead. |
| *16 Nov:* Writing the NUL test for #177 | It **found a second bug**, the padded duplicate kode, and gave it its own red commit rather than folding it into the NUL fix. |
| *17 Nov:* Reviewing Gabriel's #174 | It **recomputed the three hashes** from the CDN, reverted the template to see his test fail, and then **tried a version bump with stale hashes**, which passes every test. That became the review's one suggestion. |

## Memory as working data

- **Rules applied unprompted:** the conventions above shaped every commit, PR, reply and scan this week.
- **Rules that changed this week's output:**
    - the new post-approval scope rule decided how Heraldo's comments on #174 were handled;
    - "a ZAP scan per finished sub-issue" produced the 17 Nov report.
- **Saved from what went wrong:** start the scan backends with a clean environment (13 Nov). The 16 Nov memory exhaustion, and the one-at-a-time rerun, are recorded in the report's "What went wrong".
