# Grow Together, Communication, Knowledge Sharing

!!! success "Competency level: 3"
    Knowledge shared with the team in writing this week, and the team's input built into my work:

    - A QA finding explained to the team, with options, before anyone treated it as a bug.
    - QA given what they need to retest a by-design behaviour correctly.
    - A teammate's PR reviewed with the method behind each point, not just a verdict.

The rubric's level 2 is working well as a team without causing issues that hinder the project. Level 3 adds knowledge sharing or comparable team activities. This week's sharing was written, in a proposal doc, Linear issues and a review, rather than a session.

## This week (Sprint 2 Week 2, 16–23 Oct)

- **A QA finding turned into a team decision.**
    - **The finding:** QA marked draft pencairan "Fail – High".
    - **My analysis:** I traced it to a deliberate ceiling rule and wrote a short proposal for the team. It covered the cause, the tests that pin the rule, three options (warn, block, or warn and confirm), and the decisions to make.
    - **The outcome:** the team chose to warn without blocking, and Pascal suggested a confirmation dialog. Both went into [pilah-mobile #153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153), and the decision is written down in [PIL-374](https://linear.app/pilah-2/issue/PIL-374).
- **QA told how to retest, not just "won't fix".** The second finding (Edit Pencairan only lets you change some fields) is a deliberate lock. [PIL-375](https://linear.app/pilah-2/issue/PIL-375) explains why the nominal and date are locked when there's a potongan, and asks QA to rerun the case on a pencairan without one and add that to its pre-condition. The fix ([#154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154)) makes the lock visible, so the next tester isn't confused the same way.
- **A review that explains its method.** On Ghani's [pilah-mobile #162](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/162#pullrequestreview-5626578469), I said how I checked his tests (restore the old code, watch the new tests fail). I listed the code his change leaves unreachable, file by file, so the planned cleanup has a ready checklist. I also explained why separate RED and GREEN commits help a reviewer.
- **Teammates' input taken in.** Aldo's notes on #153 and #154 were checked against the code and answered. On #127, Pascal and Aldo each found an issue in the desktop editor, and Pascal fixed both on my branch and merged it.
- **No blocking.** My eight approved Sprint 2 PRs were brought up to date and merged on 17 Oct, so nobody waited on them. Reviews were requested through the team's `ask-for-review` and `ask-for-qa` skills, which ping the reviewer on GitHub and Discord.
- **Present at the team meetings:** the Discord standups on 19, 21 and 23 Oct, and the Sprint 2 Review, UAT and Retrospective on 22 Oct.
