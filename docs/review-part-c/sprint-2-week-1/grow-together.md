# Grow Together, Communication, Knowledge Sharing

!!! success "Competency level: 2"
    Worked well with the team this week and caused no issues that held the project back.

The rubric's level 2 is "works well as a team; does not cause issues that hinder the project". Level 3 would add knowledge sharing or comparable team activities. I am claiming level 2 honestly: the contributions below helped the team, but I did not run a knowledge-sharing session this week.

## This week (Sprint 2 Week 1, 6–14 Oct)

- **Reviews answered where they were raised.** Tristan's eight review findings across #79, #62, #73 and #74 were each verified against the code, fixed test-first, and replied to inside their own threads ([Team Development Management](../../review-sprint-2-week-1/part-b/team-development-management.md)).
- **A review given back to the team.** Reviewed and approved Gabriel's [pilah-be #97](https://github.com/bank-sampah-PILAH/pilah-be/pull/97) (PIL-354, CORS headers) with two inline suggestions, neither blocking.
- **A team-wide problem raised, not just fixed quietly.** The generated dependency graph CI builds could not construct `AuthenticationBloc`, so any CI-built app would have crashed on launch. Before touching shared CI and a teammate's code, I asked how to land the fix, then opened [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) with a test that now protects everyone's builds.
- **No blocking of others.** Merges were left to the lead as agreed. Where PIL-331's migrations collide with Pascal's draft-pencairan stack (both add `0020`/`0021`), the conflict and the needed merge migration were flagged for coordination rather than merged unilaterally.
- **Present at the team meetings:** Sprint Planning 2 on 6 Oct, and the Discord standup on 13 Oct ([Work Log](../../logs/index.md#week-of-612-oct-sprint-2-week-1)).

## What would make this level 3

A knowledge-sharing activity for the team — for example, writing up the generated-DI-graph crash and the Metasploit scan findings as a short guide, or walking the team through the stacked-PR workflow — would move this to level 3 next week.
