# IR Part B Sprint 2 Week 2

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 2 week 2.

!!! note "What this page covers"
    [Sprint 2 Week 1](../review-sprint-2-week-1/index.md) claims work up to 16 Oct. This page covers **17–23 Oct**, and mainly the **two QA fixes on pencairan** (21 Oct):

    - **[PIL-374](https://linear.app/pilah-2/issue/PIL-374)**, [pilah-mobile #153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153): a general Nominal above a nasabah's saldo now warns and asks for confirmation, without blocking.
    - **[PIL-375](https://linear.app/pilah-2/issue/PIL-375)**, [pilah-mobile #154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154): Edit Pencairan shows a locked Tanggal as locked.

    PIL-341 slice 3 (#127, 17 Oct), the Sprint 2 merges (17 Oct) and the review of Ghani's #162 (23 Oct) are included where they add evidence.

| Competency | Level | Status (23 Oct) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Both fixes test-first, one behaviour per red/green pair, refactors after green; 100% of new code on SonarCloud; mocktail mocks (a fake repository behind the real cubit; captured use-case calls), viewport-driven layout tests, a proven guard, Playwright E2E through the semantics tree |
| [Programming](part-b/programming.md) | **3** | SOLID (SRP, OCP) with code blocks; Information Expert for the saldo rule; derived state instead of a stored flag; Extract Method towards command–query separation; one lock flag driving every locked field |
| [Development Discipline](part-b/development-discipline.md) | **3** | Three MRs (#153, #154, #127), each with its own Linear issue, phase-tagged commits, detailed descriptions and green CI; follow-ups as new commits, never force-pushed; 8 approved MRs brought up to date and merged |
| [Team Development Management](part-b/team-development-management.md) | **3** | Review of Ghani's #162, verified locally with a mutation check, with one question and two feasible suggestions; Aldo's nits checked against the code; Pascal's suggestion built test-first |
| [Code Quality](part-b/code-quality.md) | **3** | No open SonarCloud issue on any of the three MRs; a complexity finding on my own new code fixed by refactoring before review, not suppressed |
| [Security](part-b/security.md) | **1** | A01 and A03 guarded and named in #127's commits (a draft link accepts only a bare id); the QA fixes have no security surface |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Its claims checked against the code before acting; two of its own wrong claims corrected; a QA "Fail" traced to a deliberate rule, then fixed as the team decided; a check it could not pass reported, not worked around |

Work this week:

- **QA finding: saldo below a general Nominal** ([PIL-374](https://linear.app/pilah-2/issue/PIL-374)), [pilah-mobile #153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153): the ceiling that caused it is intended and stays; the fix shows the reason.
    - A note sits under the Nominal.
    - A confirmation on Terapkan names every affected nasabah and their saldo.
    - Each capped card carries a line.
- **QA finding: Edit Pencairan locked fields** ([PIL-375](https://linear.app/pilah-2/issue/PIL-375)), [pilah-mobile #154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154): the lock on a pencairan with a potongan is intended. The Tanggal now looks locked like the Nominal, and the note names both.
- **[PIL-341](https://linear.app/pilah-2/issue/PIL-341) slice 3**, [pilah-mobile #127](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127) (17 Oct): draft pencairan on a desktop window. A saved draft opens from its link, and only a bare id is accepted (A01, A03).
- **Merges (17 Oct):** my 8 approved Sprint 2 MRs, with conflicts resolved on each branch and stacks merged bottom first.
- **Review given:** Ghani's [pilah-mobile #162](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/162) (23 Oct).
