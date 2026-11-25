# IR Part B Sprint 4 Week 1

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 4 week 1.

!!! note "What this page covers"
    [Sprint 3 Week 3](../review-sprint-3-week-3/index.md) claims work up to 17 Nov. This page covers **Wed 18 – Tue 24 Nov**, up to the Tuesday it was due. PIL-541 and PIL-542 (pilah-be #202 and #203, 25–26 Nov) belong to the next week.

    - **[PIL-539](https://linear.app/pilah-2/issue/PIL-539): a nasabah applies to a second bank sampah**, from end to end:
        - [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) (18 Nov): five regression tests for the flow on the existing endpoints. The backend already allowed it; the tests pin the rules the app will rely on;
        - [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) (22–23 Nov): "Ajukan bank baru" on Bank sampah saya, built test-first in four red/green pairs and a refactor.
    - **Merges:** the five PRs approved in Sprint 3 Week 3 (#137, #174, #175, #176, #177) on 18 Nov, then #185 and #276 once approved. #276 needed a merge of `staging` first, after the PR it was stacked on (#267) landed.
    - **A ZAP scan of PIL-539** (23 Nov), the first one signed in as a nasabah. It also fixed a gap in the scan tooling: an endpoint that only ever receives POST can now be actively scanned.
    - **Review threads answered:** Gabriel's non-blocking comments on #175 and #176 (18 Nov) and Heraldo's five follow-ups on #276 (23 Nov), each with the reason.

| Competency | Level | Status (24 Nov) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | #276: four `[RED]` commits, each followed by its `[GREEN]`, then a `[REFACTOR]`. SonarCloud new-code coverage 100% of 72 lines. #185 adds five regression tests for behaviour that already existed, so they had no red phase, and the PR says so. Test isolation through mocktail mocks, fakes and two recording test notifiers |
| [Programming](part-b/programming.md) | **3** | One form with a layout per context (a mode parameter plus Extract Method), a picker that says why a bank is unavailable instead of hiding it, a narrow submit for the in-app context, the screen's existing refresh-on-return convention reused, and spacing moved to design tokens. SOLID shown with code |
| [Development Discipline](part-b/development-discipline.md) | **3** | Two new MRs (#185 with 5 commits, #276 with 9 and a merge), each with one responsibility, plus five approved MRs merged. Every #276 subject carries its TDD phase; every body names the design issue, pattern, origin and the OWASP and SOLID notes |
| [Team Development Management](part-b/team-development-management.md) | **1** | **No review of a teammate's MR this week.** Review threads received on my own MRs were each answered with a reason, which the rubric doesn't count |
| [Code Quality](part-b/code-quality.md) | **3** | 0 open SonarCloud issues, 0 hotspots and 0.0% duplication on new code on both new MRs, and the quality gate passed. The design lints, which fail on Windows, were checked by hand |
| [Security](part-b/security.md) | **3** | ZAP scan of PIL-539 as a nasabah: 0 High, no new finding, 224 attacks on the application endpoint with no 5xx and no extra membership. A tooling gap found and fixed. Every 5xx classified |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims checked before they were published: the S3W2 and S3W3 pages and script corrected wherever they disagreed with the sources, the ZAP attack count recounted, and a scan rerun when it left the endpoint that mattered unscanned |

Work this week:

- **Merges and review replies** (18 Nov): #137, #174, #175, #176 and #177 merged; Gabriel's comments on #175 and #176 answered.
- **PIL-539, backend:** #185, five regression tests (18 Nov), approved by Heraldo on 19 Nov and merged on 23 Nov.
- **PIL-539, mobile:** #276, test-first (22 Nov), merged on 23 Nov after Heraldo's approval and a `staging` merge.
- **Security:** [ZAP scan of PIL-539](../security/zap-2026-11-23.md) (23 Nov).
- **IR documentation:** Sprint 3 Week 2 and Week 3 Part B and C (19–21 Nov) and Part A (19 and 24 Nov).
