# IR Part B Sprint 1 Week 3

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 1 week 3.

!!! note "Which dates this page covers"
    On the course calendar, Sprint 1 week 3 is 29 Sep – 5 Oct: UAT (29 Sep) and Sprint Review 1 (1 Oct). My Sprint 1 issues were already merged by then, so it had no development of mine. The only item from it is the 2 Oct verification on pilah-be #64. As agreed for this slot, the page reports **this week's progress (6–12 Oct)**: the work started at Sprint Planning 2 on 6 Oct and was done 7–9 Oct.

| Competency | Level | Status (9 Oct) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Test-first with phase-tagged commits; 100% of changed lines covered in all three MRs; mocks, stubs, mutation checks and migration tests |
| [Programming](part-b/programming.md) | **3** | SOLID (SRP, OCP, ISP, DIP) with code blocks; one source of truth for prices; N+1 removed |
| [Development Discipline](part-b/development-discipline.md) | **3** | Three MRs, detailed descriptions, green CI, review and CI findings fixed on the branch |
| [Team Development Management](part-b/team-development-management.md) | **3** | Review of Pascal's #84 with three feasible findings; scope claim on #64 verified against git history; Gabriel's review answered with a test |
| [Code Quality](part-b/code-quality.md) | **3** | No open SonarCloud issue on any of my three MRs, checked with the Sonar CLI; the two findings raised this week fixed |
| [Security](part-b/security.md) | **2** | Five OWASP categories (A01, A03, A04, A08, A09) prevented in code, each named in its commit and tested |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims verified before acting, plan deviations reported, prompt history published |

Work this week:

- **[PIL-304](https://linear.app/pilah-2/issue/PIL-304)** (versioned jenis sampah prices with an effective date): backend [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79), mobile [pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62). Prices became a versioned history, as the SDS's `waste_prices` table describes. Pengurus can change a price now or schedule it from a date, setoran use the price in effect at their own time, and old setoran never change.
- **Rounding follow-up**, [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89): the pencairan code now rounds through `kalkulasi.bulatkan_rupiah`, as promised in the PIL-176 review.
- **Reviews:** Pascal's [pilah-be #84](https://github.com/bank-sampah-PILAH/pilah-be/pull/84) (PIL-300) reviewed. Gabriel's review of #89 answered.

Week 2 is claimed separately: [IR Part B Sprint 1 Week 2](../review-week-2/index.md).
