# Commitment, Work Ethic

!!! warning "Competency level: 1"
    **9 h 32 min** of logged work across Sprint 3 Week 3 (11 – Tue 17 Nov, the IR due date), counting each minute once. That's **below the 17-hour minimum**, so this week is level 1:

    - **7 h 2 min** of measured session time;
    - **2 h 30 min** for the PPL class session on 17 Nov, 13:00–15:30 (self-reported).

    The output was more than the hours suggest:

    - three new merge requests (#175, #176, #177), built test-first;
    - review rounds answered on five more (#167, #238, #168, #137, #174);
    - three reviews of teammates' PRs;
    - three security scans;
    - the fix for my own leaked webhooks.

    But the hours fell short. 14 and 15 Nov had no PILAH work.

The rubric's level 1 is under 17 hours a week; level 3 is disciplined, quality work equivalent to 17 hours a week.

## Time allocation

The work blocks are in the Work Log: [Week of 11–17 Nov](../../logs/index.md#week-of-1117-nov-sprint-3-week-3).

| Part of the week | Logged |
|---|---|
| 11 Nov: Heraldo's findings on #167 and #238 fixed test-first, the date-test fix cherry-picked, replies; the docs for the 6 Nov UAT | 1 h 28 min |
| 11 – 12 Nov: **review of Gabriel's PIL-478 pair** (#169, #243), with mutants | 39 min |
| 12 Nov: the review-webhook question; PIL-451 checked for new findings; the post-approval review rule | 30 min |
| 13 Nov, 01:00–01:05: two leaked webhooks redacted from my scan evidence, the scan script hardened | 5 min |
| 13 Nov, 19:10–20:04: `staging` merged into both PIL-451 PRs; Heraldo's three comments answered | 54 min |
| 16 Nov, 17:21–17:25: open PRs checked; `staging` merged into #174 for the date-test fix | 4 min |
| 16 Nov, 18:10–20:10: #175, #176 and #177 built test-first, in parallel; the first scan attempt, which failed | 2 h |
| 16 – 17 Nov, 23:52–01:05: the three ZAP scans rerun one at a time; Tristan's third round on PIL-451 answered while they ran | 1 h 13 min |
| 17 Nov, 01:52–02:01: **review of Gabriel's #174** | 9 min |
| 17 Nov, 13:00–15:30: **PPL class session** (self-reported) | 2 h 30 min |
| **Sprint 3 Week 3** | **9 h 32 min** |

How the figures were measured:

- **Session time:** from the Claude Code session and commit timestamps, split into blocks at gaps over 30 minutes.
- **Each minute once:** on 16–17 Nov the work log lists overlapping rows, since two PRs were built side by side and the PIL-451 round was answered while the scans ran. Added row by row they make 11 h 4 min. The table above counts the wall-clock time instead: 18:10–20:10 and 23:52–01:05.
- **The class session** is self-reported, with no session behind it.
- **Days with work:** 11, 12, 13, 16 and 17 Nov.

**Reviewing other people's PRs:** 48 minutes in all, inside the rows above. The PIL-478 pair took 21:30–21:58, 23:28–23:33 and 00:32–00:38, and #174 took 01:52–02:01.

## Output of that time

- **Three new merge requests,** each built test-first, with 100% of new code covered on SonarCloud and 0 open issues: [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) (PIL-482), [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) and [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177).
- **Review rounds answered:**
    - Heraldo on [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) and [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238). All three of that pair's PRs, #168 included, were merged on 12 Nov;
    - Tristan's third round on [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) and [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174), re-approved on 17 Nov.
- **Three reviews given:** [#169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169#pullrequestreview-5862861835), [#243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243#pullrequestreview-5862862337) and [#174](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#pullrequestreview-5925723761), each run locally before posting.
- **Security:** three ZAP scans ([report](../../security/zap-2026-11-17.md)), and the leaked webhooks removed from my own evidence.

Details per competency are in [IR Part B, Sprint 3 Week 3](../../review-sprint-3-week-3/index.md).
