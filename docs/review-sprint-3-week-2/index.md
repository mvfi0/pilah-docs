# IR Part B Sprint 3 Week 2

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 3 week 2.

!!! note "What this page covers"
    [Sprint 3 Week 1](../review-sprint-3-week-1/index.md) claims work up to 3 Nov. This page covers **4 – 10 Nov**, up to the Tuesday it was due. The follow-up on these PRs from 11 Nov on is in [Sprint 3 Week 3](../review-sprint-3-week-3/index.md).

    - **[PIL-428](https://linear.app/pilah-2/issue/PIL-428), the last review round and the merge** (4 Nov). Heraldo's and Scallss's findings on [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) and [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) were fixed test-first and answered in their threads. Both PRs were approved and merged that evening. I merged [#196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196) (PIL-435) after its two approvals.
    - **[PIL-481](https://linear.app/pilah-2/issue/PIL-481), a voided setoran leaves every riwayat list** (9 Nov), built test-first in both repos: [pilah-be #167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) and [pilah-mobile #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238).
    - **[PIL-480](https://linear.app/pilah-2/issue/PIL-480), the riwayat export without the ID Aktivitas column** (9 Nov), a UAT finding: [pilah-be #168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168).
    - **UAT and usability test with the Pengurus** (6 Nov, PIL-418), run from the task script and findings form prepared last week.
    - **ZAP scans of PIL-481 and PIL-480** (9 Nov), which found a 500 on a malformed `nasabah_id`, filed as [PIL-482](https://linear.app/pilah-2/issue/PIL-482).

| Competency | Level | Status (10 Nov) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Every behaviour this week came as a `[RED]` → `[GREEN]` pair, with a refactor-first commit on #168. SonarCloud new-code coverage is 100% on every MR with lines to cover. The widget tests run on a stub API with latency, to make an in-flight request deterministic, and the #193 fixes were mutation-checked: undoing any one fails exactly its test. Playwright E2E 24/24 on PIL-481 |
| [Programming](part-b/programming.md) | **3** | One named rule (`tercatat()`) reused at each list boundary while the lookup stays unfiltered, a UI that follows the server's answer rather than the widget's lifetime, one helper that owns what reloads after a setoran changes, and an export that stops publishing an internal key. All five SOLID principles shown with code |
| [Development Discipline](part-b/development-discipline.md) | **3** | Three new MRs (#167 with 7 commits, #238 with 2, #168 with 3) and a final review round on two more (#145, #193), which merged. Each subject carries its TDD phase, and each body the design issue, pattern, origin and OWASP categories |
| [Team Development Management](part-b/team-development-management.md) | **1** | No review of a teammate's MR this week. One cross-PR heads-up to Rifqi's #212 with the fix commits, and six findings received on #145 and #193, each fixed and answered in its thread |
| [Code Quality](part-b/code-quality.md) | **3** | 0 open SonarCloud issues, 0 hotspots and 0.0% duplication on new code on all five MRs, all passing the quality gate. Two spacing values were moved to `AppSpacing` |
| [Security](part-b/security.md) | **3** | A ZAP scan of each finished sub-issue (PIL-481, PIL-480): 0 real High, the three High alerts reproduced and shown to be false positives, every 5xx read and classified, and a new finding with a test-first patch plan (PIL-482). Three OWASP categories genuinely guarded in commits (seven named; the weak labels are listed, not counted) |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims checked before acting: a third bug found while writing a test, a scan rerun rather than trusting a broken run, a "SQL injection" disproved by hand, a red CI traced to `staging` |

Work this week:

- **[PIL-428](https://linear.app/pilah-2/issue/PIL-428): the last review round** (4 Nov).
    - **Backend:** both seed commands rebuilt the saldo from every setoran, voided ones included, so re-seeding after a void put the money back (Heraldo). They now sum `tercatat()`.
    - **Mobile:** the Hapus dialog could be closed while the void was in flight and then skipped the refresh (Heraldo). Writing that test found a third bug: an answer arriving during the dialog's exit animation closed the Riwayat page underneath. A void also left the dashboard, recent activity and nasabah list stale (Scallss).
    - **Merged:** #145 and #193 by Scallss after his and Heraldo's approvals; #196 by me after its two approvals.
- **[PIL-481](https://linear.app/pilah-2/issue/PIL-481): hide a voided setoran from the lists** (9 Nov). The UAT asked for option (a): a "Hapus" should feel like a delete. Every riwayat list now reads through `tercatat()`, while the detail by id keeps the void, with who, when and why, for audit.
- **[PIL-480](https://linear.app/pilah-2/issue/PIL-480): the export without the ID Aktivitas column** (9 Nov), a UAT finding. The tests first stopped depending on that column, then it was removed.
- **UAT with the Pengurus** (6 Nov, 09:00–11:00), from the PIL-418 materials.
- **Security scans** (9 Nov): [OWASP ZAP on PIL-481 and PIL-480](../security/zap-2026-11-09.md), right after each was finished.
- **Issues I stopped rather than guessed at** (9 Nov): PIL-475, whose root cause I couldn't confirm (reproduction steps written instead), and the "Google login opens Gmail" finding on mobile web, which has no cause in the code and needs the tester's details.
