# AI Literacy

!!! success "Competency level: 3"
    AI used critically. Its plans were checked against the code before being acted on. Twice it caught and said that its own premise or check was wrong. The decisions that affect the team (shared CI, a teammate's code, how to restructure PRs) were put to me before anything changed.

[AI prompt history, 11–12 Oct](ai-prompt-history.html) is the evidence for this week: 10 prompts with every tool call the agent made between them, built from the session transcript. Emails, home-folder paths and tokens are removed. The earlier part of the same session (7–9 Oct) is published with [Sprint 1 Week 3](../../review-week-3/part-b/ai-literacy.md).

## How AI was used this week

- **Tool:** Claude Code as an agent in VS Code across `pilah-be`, `pilah-mobile` and `pilah-docs`, Linear through Composio, GitHub through `gh`, and the SonarQube CLI and the SonarCloud API for coverage.
- **Guardrails:**
    - the workspace skills (`ship`, `tdd`, `ask-for-review`);
    - CI's own commands, run locally before every push;
    - rules kept in memory: phase-tagged commits, replying inside review threads, never merging base branches into stacked ones without asking.
    - **New this week:** cover 100% of the code, generated code included.
- **My role:**
    - picking PIL-331;
    - deciding its open points (a fixed "kg" until PIL-305, scheduled prices shown and marked, the entry point on the harga card);
    - setting the coverage rule;
    - choosing how to land the CI fix and how to stack the PRs.

## Where verification changed the outcome

| Situation | What happened |
|---|---|
| *11 Oct:* It offered "a button in the expanded card" as the entry point for the price history, and I picked it | On reading the page, it found the card wasn't expandable: tapping it opens the edit sheet. It **told me its option had been based on a wrong premise**, then put the button in the card's info column, the closest match to my choice. |
| *11 Oct:* SonarCloud showed #62/#73 a few lines short of 100%, all in generated code | I said to always cover 100%, generated or not. Rather than add an exclusion, it traced why lcov skipped the file, and found that the graph CI builds would crash the app on launch. |
| *11 Oct:* Its first check of that crash passed | It noticed `build_runner` had skipped regenerating the file and left the hand-edited copy in place, so **the check proved nothing**. It deleted the file, regenerated it, and only then reported the crash, with the exact error. |
| *11 Oct:* The crash fix touched the team's CI and a teammate's code | It stopped and asked how to land it (separate PR, inside #62, or just report it) before changing shared workflows. |
| *12 Oct:* Tristan's 8 review notes | Each was checked against the code before anything changed. All 8 held up. One (the Sonar exclusion) showed that `staging` had moved since the branch was cut. |
| *12 Oct:* "Can we use stacked PRs for #79 and #92?" | #92 was already stacked, so the question was ambiguous. It also checked its saved rule against merging a base branch into a stacked one. It **asked which stack shape I meant**, then used a revert plus `cherry-pick -x`, not a force-push, so last week's evidence links stay valid. |
| *12 Oct:* #74's crash fix became redundant when Tristan's #71 landed the same change | It took `staging`'s version in the conflict and rewrote the PR around what was still new, instead of keeping a duplicate fix. |

## Example: covering generated code turned up a crash

The obvious response to "97.4% on SonarCloud, the gap is generated code" is an exclusion line in `sonar.yml`. Instead:

1. **The cause.** It checked why the file was missing from lcov: the generator writes `// coverage:ignore-file`.
2. **The proposal.** It proposed resolving every registration in a test.
3. **The finding.** Building that test exposed that the graph CI generates asks for a `bool` nobody registers. Every CI-built app would crash on launch, and nobody had noticed, because `flutter run` uses the hand-edited copy.
4. **My decision.** Before touching shared CI and a teammate's bloc, it laid out three ways to land the fix and waited for my choice.

The result is [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74), which keeps that class of crash out of future builds.
