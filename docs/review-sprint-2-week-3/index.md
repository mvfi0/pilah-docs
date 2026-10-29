# IR Part B Sprint 2 Week 3

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 2 week 3.

!!! note "What this page covers"
    [Sprint 2 Week 2](../review-sprint-2-week-2/index.md) claims work up to 23 Oct. This page covers **24–30 Oct**:

    - **[PIL-451](https://linear.app/pilah-2/issue/PIL-451)**, a QA finding on registration: a Google account that tapped the wrong role could never choose again. I opened the Linear issue (26 Oct) and built both halves test-first:
        - [pilah-be #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137): `PATCH /onboarding/role`, guarded, audited and reissuing the session;
        - [pilah-mobile #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174): "Ganti peran" on Lengkapi Profil and a role page for signed-in accounts.
    - **An OWASP ZAP scan** of my local backend and web build (26 Oct), explained, with a patch plan: [ZAP scan report](../security/zap-2026-10-26.md).
    - **Review given:** Pascal's [pilah-mobile #178](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/178) (29 Oct), verified signed in under the PR's CSP.

| Competency | Level | Status (29 Oct) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Both MRs test-first, one behaviour per `[RED]` → `[GREEN]` pair, `[REFACTOR]` after green; 100% of new code on SonarCloud (35 and 68 lines); mocktail mocks and captured arguments, a stale-object race test, guard tests proven by mutation, Playwright E2E with database checks |
| [Programming](part-b/programming.md) | **3** | All five SOLID principles with code blocks; a guarded state transition as one conditional UPDATE; an append-only audit log; session renewal on a privilege change; one page serving two entry states; Extract Method from a SonarCloud finding |
| [Development Discipline](part-b/development-discipline.md) | **3** | Two MRs from one Linear issue I wrote from the QA finding: 9 and 14 commits, each subject tagged with its TDD phase and, where it applies, its OWASP category; descriptions with cause, contract, tests, E2E and screenshots; tool findings fixed as new commits |
| [Team Development Management](part-b/team-development-management.md) | **3** | A review of Pascal's #178, verified signed in under its CSP: 8 pages clean, one regression found and pinned to its cause with a control build, three feasible fixes and one hardening suggestion |
| [Code Quality](part-b/code-quality.md) | **3** | 0 open SonarCloud issues and 0% duplication on both MRs; a critical complexity finding on my own code fixed by refactoring, not suppressed; a design-lint breach caught by hand before CI |
| [Security](part-b/security.md) | **3** | A new ZAP scan, explained, with a patch plan; four OWASP categories (A01, A04, A07, A09) guarded and named in this week's commits |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims checked against code, clean `staging` and control builds before acting; its own wrong turns caught and reported; a fix it claimed was complete was shown incomplete by reviewers, and is recorded as such |

Work this week:

- **[PIL-451](https://linear.app/pilah-2/issue/PIL-451): change a mis-tapped role** (26 Oct).
    - The cause: the role is saved the moment Lanjutkan is tapped, and nothing could change it.
    - The backend endpoint may change it only while onboarding has committed nothing for that role. Every change is logged.
    - The app links back from Lengkapi Profil and redraws the form for the new role.
    - Playwright: 14/14 checks at desktop and phone size, including database checks.
- **ZAP scan** (26 Oct): 0 High. Four real findings, each with a planned fix; the rest traced to the local setup.
- **Review given:** [pilah-mobile #178](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/178#pullrequestreview-5700286157) (29 Oct).
- **Reviews received:** Tristan and Pascal on #137 (26 Oct). Their P1 (a race between a role change and a registration already in progress) and P2 (success tests for every role) are **still open** at the time of writing; see [Team Development Management](part-b/team-development-management.md#reviews-received-on-137).
