# Commitment, Work Ethic

!!! warning "Competency level: 1"
    **8 h 29 min** of logged work across Sprint 3 Week 2 (4 – Tue 10 Nov, the IR due date). That's **below the 17-hour minimum**, so this week is level 1:

    - **3 h 59 min** of measured session time;
    - **2 h** for the UAT and usability test with the Pengurus on 6 Nov (self-reported);
    - **2 h 30 min** for the PPL class session on 10 Nov, 13:00–15:30 (self-reported).

    The output was still complete for what was taken on:

    - the last PIL-428 review round, answered and merged;
    - three new merge requests (#167, #238, #168), built test-first;
    - the UAT, from materials prepared the week before;
    - two security scans, with a new finding filed as PIL-482.

    But the hours fell short. 5 – 8 Nov had no PILAH work apart from the UAT.

The rubric's level 1 is under 17 hours a week; level 3 is disciplined, quality work equivalent to 17 hours a week.

## Time allocation

The work blocks are in the Work Log: [Week of 4–10 Nov](../../logs/index.md#week-of-410-nov-sprint-3-week-2).

| Part of the week | Logged |
|---|---|
| 4 Nov: the last PIL-428 review round. Heraldo's and Scallss's findings on #145 and #193 fixed test-first, `staging` merged into both, each thread answered, a heads-up on Rifqi's #212 | 49 min |
| 6 Nov, 09:00–11:00: **UAT and usability test with the Pengurus** (self-reported) | 2 h |
| 9 Nov: picked the next issues; stopped PIL-475 and the Gmail finding; built PIL-481 in both repos and PIL-480 test-first; three PRs; ZAP scans of both, rerun after the disk was freed; PIL-482 filed | 3 h 10 min |
| 10 Nov, 13:00–15:30: **PPL class session** (self-reported). The 3P and the red-CI diagnosis (13:41–13:51) were done during it, so they count once, here | 2 h 30 min |
| **Sprint 3 Week 2** | **8 h 29 min** |

How the figures were measured:

- **Session time:** from the Claude Code session and commit timestamps, split into blocks at gaps over 30 minutes.
- **The UAT and the class session** are self-reported, with no session behind them.
- **Not counted:** a session on 5 Nov (19:49–20:44) about my CV, not PILAH, and a 4 Nov 22:43 prompt that ended on a billing error without any work.
- **Days with work:** 4, 6, 9 and 10 Nov.

## Output of that time

- **PIL-428 finished:** six review findings on [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) and [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) fixed test-first and answered. Both were approved and merged on 4 Nov, and I merged [#196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196) after its two approvals.
- **Three new merge requests,** each built test-first, with 100% of new code covered on SonarCloud and 0 open issues:
    - [pilah-be #167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) and [pilah-mobile #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238): PIL-481;
    - [pilah-be #168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168): PIL-480.
- **The UAT with the Pengurus** (6 Nov). Two of its findings became PIL-481 and PIL-480 three days later.
- **Two security scans:** OWASP ZAP on PIL-481 and PIL-480, right after each was finished ([report](../../security/zap-2026-11-09.md)), with PIL-482 filed for the new finding.

Details per competency are in [IR Part B, Sprint 3 Week 2](../../review-sprint-3-week-2/index.md).
