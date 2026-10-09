# AI Literacy

!!! success "Competency level: 3"
    AI used critically: its claims were checked against git history, the database and the tests before being acted on. Its plans were corrected where they clashed with how the team actually works. Every outward action (pushes, PR reviews, comments) waited for my decision. The prompt history is published below with personal data removed.

Two records of the same Claude Code session:

- [AI prompt history, 7–9 Oct](ai-prompt-history.html): 23 prompts, built from the session transcript. Each tool call is one line, and personal data is removed.
- [Session export](ai-session-export.txt): Claude Code's own `/export` of the whole session, from the 2 Oct check on #64 to 9 Oct, with tool output collapsed as the export shows it. Local home-folder paths are shortened to `~`; nothing else is changed.

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code across `pilah-be`, `pilah-mobile` and `pilah-docs`, Linear through Composio, GitHub through `gh`, and, new this week, the **SonarQube CLI** (`sonar list issues`), which reads SonarCloud results directly instead of through the website.
- **Guardrails:** the workspace skills (`tdd`, `ship`), CI's own commands run locally, and the rules it keeps in memory from earlier weeks: phase-tagged commits, OWASP categories named in commits, replying inside review threads, never merging, and 3P in Bahasa.
- **My role:** choosing the issue, deciding the design questions it raised (drop the column; start at 00:00 rather than 23:59), approving each outward action, and correcting it when it worked from the wrong assumption.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| It recommended PIL-341 (pencairan on web) as my second Sprint 2 issue | The issue had to wait on teammates' web setup. I unassigned myself and told it why: in practice the team grabs issues first come, first served, so blocked issues just sit idle. It saved the rule *"recommend only issues startable now"*, and its next suggestions followed it. |
| My message said new prices could "start at every 23:59" | It asked instead of guessing: 23:59 *on* the date shifts the price by a day. The answer (00:00 local) went into the date picker and the backend's offset rule. |
| Its own plan said `PUT` with a price would return 422 | While implementing, it noticed staging deploys the backend before testers get the new app, so a 422 would break editing for them. It changed course and **said so in the summary** instead of silently deviating. |
| The tie-break test passed without any code | It didn't fake a red: it explained that SQLite returns equal rows newest first, and Postgres doesn't. The fix went in as a `[REFACTOR]` with that reason in the commit. |
| Validating on Postgres, which CI uses, with no Docker on the machine | It ran Postgres 16 from a pip package. The bundled build lacked timezone data (`invalid value for parameter "TimeZone": "UTC"`); the cause was diagnosed and fixed by copying `tzdata` in. All 464 tests and the migration ran on the same database engine as CI. |
| The migration had to be safe on real data | It restored the team's production dump into a scratch database, migrated forwards, backwards and forwards again, and compared row counts. Then it **dropped that database**, because the dump holds personal data. |
| A widget test showed the new list line overflowing at phone width | The 112 px overflow was fixed. The same check on the edit sheet showed overflows in code that predates PIL-304, partly caused by the test font's wide glyphs, so it reported them instead of "fixing" shared widgets inside an unrelated PR. |
| CI failed on `pull_request` but passed on `push`, twice | It worked out the difference: `pull_request` merges the latest `staging`. Teammates' new tests used the dropped column (backend) or the old cubit constructor (mobile). Both were fixed on the branch, not by weakening the tests. |
| A SonarCloud "composite assertion" finding | Checked first: valid, because a failure wouldn't say which value was `None`. Split into two `assert`s, keeping plain `assert` because mypy narrows types only on that. |
| Mobile diff coverage came out at 92% | It flagged that 92% wouldn't support a 100% claim and added the missing tests, instead of writing "100%" on this page. |
| A widget test couldn't see the success toast | It found the toast was raised from a context the test's router had already removed. Rather than change app code for a test-harness detail, it moved the message choice into a pure, unit-tested function. That also fixed the Sonar issue. |
| Gabriel's review on #89 said the test missed a case "only if setoran can carry sen" | It checked that legacy setoran do carry sen before adding the test, then proved the test guards the loop by moving the rounding and watching it fail. |
| Counting this week's IR evidence | It first counted week 3 as 30 Sep – 6 Oct. When I showed it the course calendar, it recomputed (29 Sep – 5 Oct) and pointed out the risk of claiming the same 29 Sep merges in both week 2 and week 3. |

## Example: "turns out we can just report this week's progress"

When I asked how to claim week 3, the AI first reported, accurately, that the week had almost no recorded development and suggested an honest "no activity" note. When I said this week's progress could be reported instead, it didn't just write pages from what existed. It checked each competency against the rubric and **stopped to ask** where the evidence was short:

- Team Development Management had no review of a teammate's MR.
- Security named four OWASP categories, where level 2 needs five.

Both gaps were closed with real work, not wording: a review of Pascal's #84 that I approved before it was posted, and an allow-list for the jenis filters (A03), written test-first.
