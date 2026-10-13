# IR Part B Sprint 1 Week 3

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 1 week 3.

!!! note "Which dates this page covers"
    On the course calendar, Sprint 1 week 3 is 29 Sep – 5 Oct: UAT (29 Sep) and Sprint Review 1 (1 Oct). My Sprint 1 issues were already merged by then, so it had no development of mine. The only item from it is the 2 Oct verification on pilah-be #64. As agreed for this slot, the page reports **this week's progress (6–12 Oct)**: the work started at Sprint Planning 2 on 6 Oct and was done 7–9 and 11–12 Oct.

| Competency | Level | Status (12 Oct) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Test-first with phase-tagged commits, review fixes included; 100% of changed lines covered in all seven MRs; mocks, stubs, `Completer`-ordered races, mutation checks, migration tests and a full-graph DI test |
| [Programming](part-b/programming.md) | **3** | SOLID (SRP, OCP, ISP, DIP) with code blocks; one source of truth for prices; N+1 removed; exact money without `double`; a stale-response guard |
| [Development Discipline](part-b/development-discipline.md) | **3** | Seven MRs, stacked where they depend on each other, with detailed descriptions and green CI; every review and CI finding fixed on the branch |
| [Team Development Management](part-b/team-development-management.md) | **3** | Review of Pascal's #84 with three feasible findings; scope claim on #64 verified; Gabriel's and Tristan's reviews (9 findings) answered with tests in their threads |
| [Code Quality](part-b/code-quality.md) | **3** | No open SonarCloud issue on any of my seven MRs; the two findings raised fixed; generated code brought under coverage, which exposed a startup crash |
| [Security](part-b/security.md) | **2** | Five OWASP categories (A01, A03, A04, A08, A09) prevented in code, each named in its commit and tested |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims verified before acting, its own wrong premises and checks called out, plan deviations reported, prompt history published |

Work this week:

- **[PIL-304](https://linear.app/pilah-2/issue/PIL-304)** (versioned jenis sampah prices with an effective date): backend [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79), mobile [pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62). Prices became a versioned history, as the SDS's `waste_prices` table describes. Pengurus can change a price now or schedule it from a date, setoran use the price in effect at their own time, and old setoran never change.
- **Rounding follow-up**, [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89): the pencairan code now rounds through `kalkulasi.bulatkan_rupiah`, as promised in the PIL-176 review.
- **[PIL-331](https://linear.app/pilah-2/issue/PIL-331)** (price history per jenis sampah): backend [pilah-be #92](https://github.com/bank-sampah-PILAH/pilah-be/pull/92), approved by Tristan; mobile [pilah-mobile #73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73). Both are stacked on PIL-304. Every price version is listed newest first with its author and a status (scheduled, current, previous or replaced), and opened from each harga card.
- **Scope split:** the jenis-filter allow-list moved out of #79 into [pilah-be #96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96), stacked on #92, after Tristan's review.
- **Generated code covered**, [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74): the dependency-injection graph is built in full by a test and measured in CI. Covering it exposed a crash that CI-built apps would have hit on launch.
- **Reviews:** Pascal's [pilah-be #84](https://github.com/bank-sampah-PILAH/pilah-be/pull/84) (PIL-300) reviewed. Gabriel's review of #89 and Tristan's review of #79, #62, #73 and #74 answered.

Week 2 is claimed separately: [IR Part B Sprint 1 Week 2](../review-week-2/index.md).
