# IR Part B Sprint 2 Week 1

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 2 week 1 (6–12 Oct).

!!! note "What this page covers, and what it leaves out"
    Sprint 2 week 1 is 6–12 Oct, starting with Sprint Planning 2 on 6 Oct. The work of 7–9 Oct (PIL-304's pilah-be #79 and pilah-mobile #62, the rounding follow-up #89, and the review of Pascal's #84) is claimed in [Sprint 1 Week 3](../review-week-3/index.md), which had no development of its own. So this page covers **10–12 Oct**: PIL-331, the generated DI graph, and the round of review fixes that followed. The fixes landed in #79 and #62, but they answer a review received this week, so they are counted here as commits; the PRs themselves are not counted again.

    It also takes in four items from the days after, which the work log counts as this sprint week continued (13–19 Oct): PIL-341 slices 1 and 2 (pilah-mobile #83 and #84, 13 Oct), the reviews of Gabriel's #97 (13 Oct) and Ghani's #104 (16 Oct), and the 13 Oct conversation about Playwright.

| Competency | Level | Status (16 Oct) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | PIL-331 and every review fix built test-first; 100% of changed lines covered, generated code included; `Completer`-ordered races, a fake backend at the HTTP boundary, mutation checks and a full-graph DI test |
| [Programming](part-b/programming.md) | **3** | SOLID (SRP, OCP, DIP) with code blocks; one rule for a version's status; money kept exact without `double`; a stale-response guard |
| [Development Discipline](part-b/development-discipline.md) | **3** | Six new MRs (incl. PIL-341 slices 1–2), stacked where they depend on each other, with detailed descriptions and green CI; every review and CI finding fixed on the branch |
| [Team Development Management](part-b/team-development-management.md) | **3** | Detailed reviews of Gabriel's #97 (two suggestions, both adopted) and Ghani's #104 (a benchmarked performance suggestion); Tristan's 8 findings on my MRs verified, fixed test-first and answered; a team-wide startup crash found and raised |
| [Code Quality](part-b/code-quality.md) | **3** | No open SonarCloud issue on any of this week's MRs; generated code brought under coverage, which exposed a startup crash |
| [Security](part-b/security.md) | **3** | Metasploit scan of the backend, explained, with a test-first patch plan ([report](../security/index.md)); plus A01 guarded and named in its commit on the price-history endpoint |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Its own wrong premises and invalid checks called out, review claims verified before acting, decisions with team impact left to me; on Playwright, it said what its own run didn't test, and the result became a saved rule |

Work this week:

- **[PIL-331](https://linear.app/pilah-2/issue/PIL-331)** (price history per jenis sampah): backend [pilah-be #92](https://github.com/bank-sampah-PILAH/pilah-be/pull/92), approved by Tristan; mobile [pilah-mobile #73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73). Both are stacked on PIL-304. Every price version is listed newest first with its author and a status (scheduled, current, previous or replaced), and opened from each harga card.
- **Generated code covered**, [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74): the dependency-injection graph is built in full by a test and measured in CI. Covering it exposed a crash that CI-built apps would have hit on launch.
- **Review round (11–12 Oct):** Tristan's 8 findings on #79, #62, #73 and #74, each fixed test-first. One of them moved the jenis-filter allow-list out of #79 into [pilah-be #96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96), stacked on #92. Its commits are the ones already claimed in Sprint 1 Week 3, so #96 is listed under discipline, not as new security work.
- **[PIL-341](https://linear.app/pilah-2/issue/PIL-341) slices 1 and 2 (13 Oct):** pencairan on the web dashboard. [pilah-mobile #83](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/83) downloads exports in the browser; [#84](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/84), stacked on it and merged into it, records, edits and revises a pencairan on a desktop window. Both test-first, 100% of new code on SonarCloud ([coverage at a glance](part-b/tdd.md#coverage-proof-at-a-glance)).
- **Reviews of teammates' MRs:** Gabriel's [pilah-be #97](https://github.com/bank-sampah-PILAH/pilah-be/pull/97) (PIL-354, CORS headers) on 13 Oct, approved with two suggestions that he adopted; Ghani's [pilah-be #104](https://github.com/bank-sampah-PILAH/pilah-be/pull/104) (PIL-248, operational report) on 16 Oct, with a database-aggregate suggestion backed by a benchmark.
- **Security scan (14 Oct):** a [Metasploit scan](../security/index.md) of the backend on a local instance, explained, with a test-first patch plan. It surfaced the API schema/docs served without authentication, plus HSTS/CSP hardening gaps.

Sprint 1 Week 3 is claimed separately: [IR Part B Sprint 1 Week 3](../review-week-3/index.md).
