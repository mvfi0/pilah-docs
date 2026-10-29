# AI Literacy

!!! success "Competency level: 3"
    AI used critically:

    - Its claims were checked against the code, a clean `staging` checkout or a control build before anything changed.
    - Its own wrong turns were caught and reported, not smoothed over: a wrong test expectation, a skill step that dirtied tracked files, a redaction pass that broke a script, a scan report that came out empty.
    - One claim it made was shown **incomplete by human reviewers**: the race fix on #137. It's recorded that way, along with the fix that followed, proven by a test that really races.

    Decisions with team or outside impact were put to me: where to point a pen test, whether to create a Linear issue, and how to post a review.

Evidence for this week:

- [Session export](ai-session-export.txt): Claude Code's own `/export` of the session behind 26–29 Oct, with home-folder paths shortened to `~`. It was taken at 22:36 on 29 Oct, so it ends before the #137 review fixes. Those are recorded in their commits and review replies.
- The PRs, review and reports linked below, each of which records the checks described here.

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code, across `pilah-be`, `pilah-mobile` and `pilah-docs`. Linear through Composio; GitHub through `gh`; SonarCloud's API; Playwright with Edge against local builds; OWASP ZAP through its API.
- **Guardrails:**
    - the workspace skills (`ship`'s layout, `tdd`), and the `code-review` skill for #178;
    - CI's own commands, run locally before every push;
    - rules kept in memory, applied without being restated:
        - the TDD phase in every commit subject;
        - the OWASP category named in the commit;
        - the design issue, pattern and origin in each commit body;
        - 100% coverage checked on SonarCloud, not only locally;
        - Playwright E2E for web UI;
        - no AI attribution in PR text.
- **My role:**
    - choosing what to work on: the QA finding this week (PIL-451), since my assigned PIL-428 is planned for Sprint 3 Week 1;
    - approving the Linear issue;
    - choosing a **local-only** pen test over scanning shared staging;
    - choosing which teammate's PR to review, and posting it as a comment rather than a change request;
    - keeping PIL-451 on Windows while moving setup to Linux.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| *26 Oct:* QA suggested a back button that resets the chosen role on the phone | Before agreeing, it traced the role to the server: saved the moment Lanjutkan is tapped, and pinned by a backend test. It **said a phone-only reset couldn't work** and rated the finding High rather than Critical, with reasons. It created the Linear issue only after I said yes. |
| *26 Oct:* Its first test expected 400 for a forbidden role | The mutation check showed the API's handler answers 422 `{"errors": …}`. It **fixed the test to the project's convention**, not the code, and said the assumption was its own. |
| *26 Oct:* The `ship` skill's ".agents copy" step | In these repos `.agents` is tracked, so copying the outdated canonical copy dirtied two tracked files in the new worktree. It **spotted that in `git status`, restored them**, and later wrote a worktree script that skips the copy when `.agents` is tracked. |
| *26 Oct:* 5 backend and 25 mobile tests failed locally | It **didn't call them pre-existing until it had run them on a clean `staging` checkout**, where they fail the same way, because of Windows paths. |
| *26 Oct:* The design lints can't run on Windows | Instead of skipping them, it **counted their patterns by hand** against the baselines and **caught its own breach**: a hard-coded font size over the allowed count. Fixed before CI. |
| *26 Oct:* SonarCloud showed 97.1% where local said 100% | It found that a PR's CI runs only the changed test files, and that two pre-existing methods counted as new lines. It **added the two tests** rather than explaining the number away. |
| *26 Oct:* "The conditional UPDATE closes the race" | **This claim was incomplete.** Tristan and Pascal showed that a registration already past its role check can still link a bank afterwards. The AI's own race test had pre-linked the bank, so it never exercised that order. On 29 Oct it **accepted the finding without arguing**, wrote a test that really races (two threads on PostgreSQL) and **watched it fail** on all three paths, including `accept_invite`, which the review hadn't named. Then it fixed all three with a shared row lock and answered each thread. |
| *29 Oct:* Making the race test fully covered | The fix left one line of the test that only runs while the bug exists. It reworked the test, then **re-ran it against the pre-fix code** to prove it still fails there, instead of assuming the change was harmless. |
| *26 Oct:* Pen test target | An active scan sends thousands of attack requests. It **asked whether to scan local or staging** and listed the trade-offs. I chose local only. |
| *26 Oct:* ZAP reported 17 Medium | It **triaged each one against the production `nginx.conf`** and the real servers, separating local artifacts from real findings. It reproduced the 500 with `curl`, and found the same crash in `terbitkan`, which ZAP had missed. |
| *26 Oct:* Its own tooling misled it twice | The ZAP report came out empty (a wrong site separator in its call), and the E2E script showed 4 "failures" (Django 6 prints a banner before the output). It **noticed both were its own mistakes, fixed them, and reran**. Neither became a reported bug. |
| *29 Oct:* A redaction pass for the Linux handover | Its automatic secret filter rewrote a harmless local test login in a copied script, which would have broken it. A **byte-for-byte comparison** against the originals caught it, and the filter was narrowed to CLI output only. |
| *29 Oct:* Reviewing #178 | It expected the CDN script to be blocked, but the browser reported `eval`. It **traced the real cause into the dependency's source**, proved the regression against a control build, and, in the review, **didn't claim** an untested alternative (`pdfrx`) would work. |

## Memory as working data

The persistent memory gets read at the start of each session and corrected as I work. This week:

- **Rules applied unprompted.** The commit conventions, coverage checks and E2E habit listed above shaped every commit and PR without my repeating them.
- **New rules saved from what went wrong:**
    - Windows-only test failures: which ones, why, and how to still check the design lints;
    - Playwright on this machine: Edge, the demo-login labels, rewriting the login for a fresh account, the screenshot branch.

    The next session starts from these instead of rediscovering them.
- **Carried to a new machine.** For the move to a dual-boot Linux setup, it bundled the memories, skills, SDS and PRD into one file. It listed which memories were Windows-specific. When the Linux session asked follow-up questions, it answered with **"not found" where things didn't exist**: a memory that was linked but never written, and a "global" skill that was never installed. It didn't invent them.
