# Commitment, Work Ethic

!!! warning "Competency level: 1"
    **8 h 15 min** of logged work across Sprint 4 Week 1 (18 – Tue 24 Nov, the IR due date), counting each minute once. That's **below the 17-hour minimum**, so this week is level 1:

    - **7 h 7 min** of measured session time;
    - **2 h 30 min** for the PPL class session on 24 Nov, 13:00–15:30 (self-reported);
    - less **1 h 22 min** counted twice: the Part A documentation work from 13:36 to 14:58 was done during the class session.

    The output was more than the hours suggest:

    - PIL-539 finished end to end: a backend MR (#185) and a test-first mobile MR (#276), both reviewed and merged;
    - five approved MRs from the week before merged;
    - a ZAP scan, which also fixed a gap in the scan tooling;
    - the Sprint 3 Week 2 and Week 3 IR pages and the Part A pages.

    But the hours fell short. 20 Nov had no PILAH work.

The rubric's level 1 is under 17 hours a week; level 3 is disciplined, quality work equivalent to 17 hours a week.

## Time allocation

The work blocks are in the Work Log: [Week of 18–24 Nov](../../logs/index.md#week-of-1824-nov-sprint-4-week-1).

| Part of the week | Logged |
|---|---|
| 18 Nov, 23:16–23:44: approved PRs merged (#137, #174, #175, #176, #177); Gabriel's comments on #175 and #176 answered; PIL-539 backend tests (#185) | 27 min |
| 19 Nov, 03:42: the 3P standup update | under 1 min |
| 19 Nov, 13:03–13:08 and 14:43–15:11: IR Part A, the TDD page | 34 min |
| 19 Nov, 13:27–14:27: IR pages for Sprint 3 Weeks 2 and 3, checked against the sources | 59 min |
| 21 Nov, 12:19–13:15: the script for presenting Sprint 3 Weeks 2 and 3, and the pages it pointed to (test doubles, before-and-after tables, dated timelines, PR links, patterns) | 56 min |
| 22 – 23 Nov, 23:04–00:55: **PIL-539 mobile (#276)**, test-first; #185 merged; **the ZAP scan**, run twice, and its report | 1 h 50 min |
| 23 Nov, 17:10–17:45: #276 retargeted, `staging` merged in, Heraldo's follow-ups answered, merged | 35 min |
| 23 Nov, 18:40–18:53: Linear checked for the next issue | 13 min |
| 24 Nov, 02:27–02:38: the 3P update; IR Part A, Team Work with Tools | 9 min |
| 24 Nov, 13:00–15:30: **PPL class session** (self-reported), with IR Part A edits from 13:36 to 14:58 inside it | 2 h 30 min |
| **Sprint 4 Week 1** | **8 h 15 min** |

The rows are rounded to the minute and add up to 8 h 13 min; the total, 8 h 15 min, is from the exact timestamps.

How the figures were measured:

- **Session time:** from the Claude Code session and commit timestamps, split into blocks at gaps over 30 minutes. Every commit this week falls inside a block.
- **Each minute once:** the class session overlaps the 24 Nov Part A edits, so that time is counted once. Added row by row, the time would be 9 h 37 min.
- **Not counted:** a 23 Nov session about a laptop driver, which isn't PILAH work.
- **The class session** is self-reported, with no session behind it.
- **Days with work:** 18, 19, 21, 22, 23 and 24 Nov.

## Output of that time

- **PIL-539, a nasabah applies to a second bank sampah:**
    - [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185): five regression tests that pin the server's rules for the flow. Approved by Heraldo and merged;
    - [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276): "Ajukan bank baru", built in four red/green pairs and a refactor, with 100% of new code covered and 0 SonarCloud issues. Approved by Heraldo and merged.
- **Merges:** [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137), [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174), [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175), [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) and [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177), on 18 Nov.
- **Security:** a ZAP scan of PIL-539 ([report](../../security/zap-2026-11-23.md)), and a fix to the scan tooling for POST-only endpoints.
- **IR documentation:** Part B and C for Sprint 3 Weeks 2 and 3, and Part A.

Details per competency are in [IR Part B, Sprint 4 Week 1](../../review-sprint-4-week-1/index.md).
