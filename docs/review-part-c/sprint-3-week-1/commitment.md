# Commitment, Work Ethic

!!! success "Competency level: 3"
    **18 h 10 min** of logged work across Sprint 3 Week 1 (31 Oct – Tue 3 Nov, the IR due date), above the 17-hour minimum:

    - **6 h 25 min** of measured session time;
    - **6 h** for the 3 Nov evening session, 17:00–23:00 (self-reported);
    - **2 h 30 min** for the PPL class session on 3 Nov, 13:00–15:30 (self-reported);
    - **2 h 45 min** of self-reported meetings: Sprint 3 Planning and the week's standups;
    - **30 min** of reading on the Metasploit Framework (self-reported).

    The work was spread over all four days of a short week (Saturday 31 Oct to the Tuesday it was due), with attendance at Sprint 3 Planning and the standups. The output:

    - **three new merge requests:** #145, #193 and #196;
    - **a second review round** answered on #137 and #174, and Rifqi's and Gabriel's reviews answered on #145 and #193;
    - **the UAT materials** for 6 Nov (PIL-418);
    - **two reviews** of teammates' PRs;
    - **two security scans;**
    - **all of Sprint 3 Week 1's Part B pages.**

The rubric's level 1 is under 17 hours a week; level 3 is disciplined, quality work equivalent to 17 hours a week.

## Time allocation

The hours and every work block are in the Work Log: [Week of 31 Oct – 3 Nov](../../logs/index.md#week-of-31-oct-3-nov-sprint-3-week-1).

| Part of the week | Logged |
|---|---|
| Sprint 3 Planning with the team (self-reported) | 2 h |
| Daily standups on Discord, the week's total (self-reported) | 45 min |
| 31 Oct: PIL-428 built test-first in both repos, PRs #145 and #193 opened, every open PR checked for conflicts, the migration clash flagged on #137 and #145 | 2 h 23 min |
| 31 Oct – 1 Nov: picked the next startable issue, built PIL-435 test-first and opened #196 | 43 min |
| 2 Nov: seven review findings on #137 and #174 fixed and answered; `staging` merged into #193 and #174; **reviews of Rifqi's #144 and Gabriel's #202** (20:50–21:07, below); SonarCloud findings fixed; Sprint 3 Week 1 Part B pages; ZAP scans of PIL-428 and PIL-435 | 3 h 17 min |
| 3 Nov, early: session export published, 3P | 4 min |
| 3 Nov, 13:00–15:30: **PPL class session** (self-reported); the S2W3 Security claim and these Part C pages were written during it, so they count once, here | 2 h 30 min |
| 3 Nov, 17:00–23:00 (self-reported): Rifqi's and Gabriel's findings on #145 and #193 fixed test-first (a lock-order deadlock, a receipt race, the OpenAPI contract, a guard test); presentation scripts for Part B; change requests checked on every open PR; PIL-418 UAT script and findings form; the next sub-issue picked | 6 h |
| Reading on the Metasploit Framework and how it works (self-reported) | 30 min |
| **Sprint 3 Week 1** | **18 h 10 min** |

**Reviewing other people's PRs.** Both reviews were done in the 2 Nov session, with checkout, tests and a scratch test before posting. They took about 17 minutes of it: from listing the teammates' open PRs at 20:50, to the #144 review at 20:58 and the #202 review at 21:06. The #202 suite run and its write-up followed. This time is counted inside the 2 Nov row above, not on top of it. No other reviews by me on teammates' PRs were posted between 30 Oct and 3 Nov.

How the figures were measured:

- **Session time:** from the Claude Code session and commit timestamps, split into blocks at gaps over 45 minutes, as in earlier weeks.
- **Meetings:** Sprint 3 Planning (2 h) and the standups (45 min in total) are self-reported, with no session behind them.
- **The 3 Nov class and evening sessions, and the reading,** are self-reported. The evening session's commits (17:45–18:36 on #145 and #193) fall inside its 17:00–23:00 window. The measured session from 13:25 to 14:02 fell inside the class, so those 37 minutes are counted once, under the class.
- **Days with work:** 31 Oct, 1 Nov, 2 Nov and 3 Nov.

## Meetings

- **Sprint 3 Planning** with the team, about 2 h.
- **Daily standups on Discord:** 45 min in total this week.

## Output of that time

- **Three new merge requests,** each built test-first with 100% of new code covered on SonarCloud and 0 open issues:
    - [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) and [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193): my assigned PIL-428;
    - [pilah-mobile #196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196): PIL-435, picked as the next issue that could start immediately.
- **A second review round answered:** seven findings from Tristan, Scallss and Heraldo on [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) and [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174), fixed test-first and answered in each thread.
- **Two reviews given:** [Rifqi's #144](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#pullrequestreview-5737653085) and [Gabriel's #202](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#pullrequestreview-5737765335), each run locally before commenting.
- **Two security scans:** OWASP ZAP on PIL-428 and PIL-435, right after each was finished ([report](../../security/zap-2026-11-02.md)).
- **Coordination:** a migration-number clash between #137 and #145 flagged on both PRs before either merged.

Details per competency are in [IR Part B, Sprint 3 Week 1](../../review-sprint-3-week-1/index.md).
