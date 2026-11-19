# Grow Together, Communication, Knowledge Sharing

!!! success "Competency level: 2"
    Worked well with the team this week and caused no issues that held the project back. Knowledge was shared in writing along the way:

    - **Reviews that show how they were checked:** mutants, recomputed hashes and real requests, each with the evidence and a concrete fix.
    - **A teammate's open request respected:** no admin bypass on Tristan's change request.
    - **A teammate's work built on, not duplicated:** #177 took the follow-up Scallss's #172 listed.

The rubric's level 2 is working well as a team without causing issues that hinder the project. Level 3 adds knowledge sharing or comparable team activities. I'm claiming level 2: the sharing this week was written (reviews, PR comments, thread replies), and there was no knowledge-sharing session.

## This week (Sprint 3 Week 3, 11 – 17 Nov)

- **Three reviews that show their working.**
    - **On Gabriel's PIL-478 pair ([#169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169#pullrequestreview-5862861835), [#243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243#pullrequestreview-5862862337)):** I named the mutants his tests caught, then the ones they missed, each with the test that would catch it. I also showed with a real request that the server doesn't require a pengelola's birth date, and gave both ways to resolve it. The CI failure I traced to an unrelated test, with the commit that fixes it.
    - **On Gabriel's [#174](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#pullrequestreview-5925723761):** I explained how I verified each claim (hashes, template, tests), then showed the one gap with a concrete version, and suggested a fix he could take as a follow-up.
- **Respecting a teammate's open request.** On 13 Nov both PIL-451 PRs had two approvals but still carried Tristan's change request. I didn't bypass it. I re-requested his review, he raised two more points, I fixed them, and he approved on 17 Nov.
- **Building on a teammate's PR.** Scallss's #172 fixed a NUL byte in `search` first and listed the request-body case under "Not in this PR". #177 took exactly that.
- **Reviewers' findings taken in.** Heraldo's findings on #167 and #238 and Tristan's on #137 and #174 were answered in their threads, with the fix linked. Heraldo's three post-approval comments on #174 got the reason for leaving each, and the PR description was corrected where he was right.
- **A risk to the team's tooling recorded.** The leaked webhooks were the review and QA channels' Discord webhooks, which Discord revoked, so notifications that rely on them (as Rifqi's #173 would) need new ones. The [report](../../security/zap-2026-11-09.md#what-went-wrong-on-the-way) records the leak.
