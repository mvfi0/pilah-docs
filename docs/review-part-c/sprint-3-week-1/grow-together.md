# Grow Together, Communication, Knowledge Sharing

!!! success "Competency level: 2"
    Worked well with the team this week and caused no issues that held the project back. Knowledge was shared in writing along the way:

    - **Reviews that explain how they were checked:** each finding comes with the evidence and a concrete fix.
    - **A cross-PR risk flagged** on both PRs before it could break `staging`.
    - **Teammates' findings on my PRs taken in,** each answered in its thread, with their suggested approach credited.

The rubric's level 2 is working well as a team without causing issues that hinder the project. Level 3 adds knowledge sharing or comparable team activities. I'm claiming level 2: the sharing this week was written (reviews, PR comments, thread replies), and there was no knowledge-sharing session.

## This week (Sprint 3 Week 1, 31 Oct – 3 Nov)

- **Two reviews that show their working.**
    - **On Rifqi's [pilah-be #144](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#pullrequestreview-5737653085):** I didn't just say a database bug would be hidden. I showed it with a throwaway test and the two log lines it produced. Then I gave the fix and the test that would pin it, and framed the throttle concern as a question backed by where else the endpoint is called.
    - **On Gabriel's [pilah-mobile #202](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#pullrequestreview-5737765335):** I ran 389 tests and grepped every route in, then suggested a way to keep the feature's route guards tested while it's locked. I also answered the question his own description raised, by quoting CPBI-31.
- **A risk Git can't see, flagged early.** My two open backend PRs, #137 and #145, both add migration `0029`. Git shows no conflict, but `migrate` would fail on `staging` once both merge. I found it while checking every open PR in both repos for conflicts with mine, and commented on [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#issuecomment-6542913917) and [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#issuecomment-6542914469). The comments link both files and say who renumbers, so whoever merges second knows what to do.
- **Teammates' findings taken in.**
    - Tristan, Scallss and Heraldo raised seven findings on #137 and #174. Each was checked against the code, fixed test-first, and answered in its own thread with the commit and the lines linked.
    - Where a reviewer suggested the approach, the reply credits it: the lock on the Google-login claim, and gating the draft clearing on the role.
- **Kept teammates' work in view.**
    - #193 was merged with `staging` so it carries PIL-453's new inline detail rather than fighting it.
    - My review of #202 pointed the next person at the same dead-control pattern in PIL-434.
- **Present at the team meetings:** Sprint 3 Planning, and the week's Discord standups.
