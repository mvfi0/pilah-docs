# AI Literacy

!!! success "Competency level: 3"
    AI used critically:

    - **Claims checked before acting:** by running the code, a clean `staging` checkout, a scratch test or a screenshot. That applies to teammates' code under review, and to its own E2E failures before blaming the app.
    - **Its own wrong turns reported, not smoothed over:** three E2E script mistakes in a row, a test-data side effect, and code it merged that SonarCloud then flagged.
    - **Discipline kept where it's easy to drop:** review fixes kept out of merge commits so each gets its own red/green pair, and an untestable branch removed rather than covered with a contrived test.

    Decisions with product or team impact were put to me: the three PIL-428 design choices, which issue to take next, and which PRs to review.

Evidence for this week:

- The PRs, reviews and replies linked below, each of which records the checks described here.
- [Session export](ai-session-export.txt): Claude Code's own `/export` of the session behind 31 Oct – 3 Nov. It starts after the PIL-428 build, when the context was summarised, and runs from the PR conflict check through the reviews, these docs and the ZAP scans. Before publishing, I scanned it for emails, tokens, JWTs, student and Discord IDs, webhooks and home-folder paths: none found. The only matches were three fake phone numbers from test fixtures.

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code, across `pilah-be`, `pilah-mobile` and `pilah-docs`. Linear through Composio; GitHub through `gh`; SonarCloud through its API and the `sonar` CLI; Playwright with Edge against local builds; PostgreSQL 16 through `pgserver`.
- **Guardrails:** the workspace skills (`ship`'s worktree layout, `tdd`), CI's own commands run locally before every push, and rules kept in memory and applied without being restated:
    - the TDD phase in every commit subject;
    - the OWASP category in the commit;
    - the design issue, pattern and origin in each commit body;
    - 100% coverage checked on SonarCloud, not only locally;
    - Playwright E2E for web UI;
    - replies inside each review thread, with permalinks;
    - no AI attribution in PR text. A harness default asked for a "Generated with Claude Code" line in PR bodies; the saved rule takes precedence, so it was left out.
- **My role:**
    - choosing PIL-435 from the agent's list of startable issues, ranked by my "prefer independent issues" rule;
    - picking the three PIL-428 design options;
    - asking for the week's reviews and docs;
    - deciding when to request re-review.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| *31 Oct:* PIL-428 left three product choices open | It **asked before coding**, with a recommended option for each: where Hapus lives, whether the alasan is required, and where voided rows still appear. |
| *31 Oct:* The first PIL-428 E2E run | Playwright found two UI problems the widget tests missed: a full-width dialog on desktop, and a misleading "Saldo Setelah Transaksi Rp 0" on a voided detail. Both were **fixed test-first**, not just patched. |
| *31 Oct:* Checking open PRs for conflicts | Many PRs showed conflicts. It **compared each against plain `staging`** and found them pre-existing (stale branches), so it didn't comment on them. It flagged the one real clash, two `0029` migrations that Git can't see. |
| *31 Oct:* PIL-435 had no description | It read the parent CPBI's acceptance criteria ("tidak ada menu mati") and **hid** the selector rather than disabling it. It said so in the PR. |
| *31 Oct:* An unexpected red failure on PIL-435 | A large-text layout test failed. It **traced it to its own new test row** pushing a name off screen, and fixed the test data rather than the app. |
| *31 Oct:* A PIL-435 E2E check failed on the phone | Before calling it a bug, it **looked at the screenshot**: the app was right, and the selector missed a name that wraps onto two lines. |
| *2 Nov:* PostgreSQL wouldn't start | The log said `could not open directory "pg_notify"`. It found the cause: the Temp-folder cleanup had removed Postgres's empty directories. It recreated them instead of re-initialising, which would have lost the E2E data. |
| *2 Nov:* Merging `staging` into #174 | `staging` had added a consent step to the role page. It **decided account mode skips it**, since the account agreed when it registered, and wrote that reasoning into the merge commit. It kept the reviewers' fixes out of the merge, so each got its own red/green pair. |
| *2 Nov:* Merging `staging` into #193 | It noticed PIL-453 had stopped opening the detail sheet in Riwayat, so the Pembatalan section **would silently disappear**. It added it to the inline detail test-first. |
| *2 Nov:* Re-running the PIL-428 E2E after that merge | One phone check failed. It **wrote a separate debug script** that showed the app works. **Its own two "fixes" to the check were wrong**: the second click collapsed the row its hold had already expanded. It reported that, then restored the original check with a settle delay. 21/21. |
| *2 Nov:* Diff coverage 96.4% on #137 | It recognised the missing line as a branch no test could reach. It **removed the branch with a reasoned refactor** rather than contriving a test to cover it. |
| *2 Nov:* After each push | It **read SonarCloud again** rather than assume green. That found two issues introduced by its own changes (S3776 on #174, S3358 on its #193 merge). Both were fixed by refactoring. |
| *2 Nov:* Reviewing #144 | It **proved the logging gap with a throwaway test** before claiming it. It framed the throttle concern as a question with evidence (the setoran picker calls the same endpoint), not as a defect. |
| *2 Nov:* Reviewing #202 | It **ran the 389 tests the PR touches and grepped every route in** before commenting. That's how it found that the "still restorable" claim had lost its route-level guards and tests. |
| *2 Nov:* Writing this page set | While documenting, it noticed its own PR repeated a domain rule nine times. It **fixed it in the PR** ([`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0)) rather than describe it as fine. |
| *2 Nov:* Re-requesting reviews | The tool call was **blocked by a permission rule**. It reported that and left it to me, rather than work around it. |

## Memory as working data

- **Rules applied unprompted.** The conventions listed above shaped every commit, PR, reply and review this week without my repeating them.
- **Rules that changed this week's output:**
    - "prefer independent issues" shaped the list of what I could take next;
    - "reply in review threads" and "embed links" shaped all seven review replies;
    - "full coverage including generated code" sent it back to SonarCloud after each push.
- **Saved from what went wrong:** the Temp cleanup that breaks the local Postgres, and how to recover it.
