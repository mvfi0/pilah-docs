# IR Part B Sprint 3 Week 1

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 3 week 1.

!!! note "What this page covers"
    [Sprint 2 Week 3](../review-sprint-2-week-3/index.md) claims work up to 30 Oct. This page covers **31 Oct – 3 Nov**, up to the Tuesday it's due.

    - **[PIL-428](https://linear.app/pilah-2/issue/PIL-428), "Hapus" (void) a setoran.** This is my assigned Sprint 3 issue, under CPBI-30. A void keeps the row and takes it out of every saldo and laporan. It took two MRs, both built test-first:
        - [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145): `POST /transaksi/{id}/batalkan`, guarded, audited, and enforced by a database constraint;
        - [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193): Hapus from the phone's selection header and the web's Aksi column.
    - **[PIL-435](https://linear.app/pilah-2/issue/PIL-435), Riwayat shows setoran only** (CPBI-31): [pilah-mobile #196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196).
    - **Second review round on PIL-451** ([#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137), [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174)): seven findings fixed test-first, each answered in its thread.
    - **Reviews given:** Rifqi's [pilah-be #144](https://github.com/bank-sampah-PILAH/pilah-be/pull/144) and Gabriel's [pilah-mobile #202](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202), both checked out and run before commenting.

| Competency | Level | Status (3 Nov) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Five MRs touched this week, all test-first, with the phase in every commit subject. 100% of new code is covered on SonarCloud. The tests include mocks and stub APIs, a database constraint proven by `IntegrityError`, a two-thread race test on PostgreSQL, and Playwright E2E with database checks (21/21 and 18/18) |
| [Programming](part-b/programming.md) | **3** | A void kept as an audited state change rather than a delete, enforced by a check constraint. The domain rule is named once as a QuerySet method. Row locks are shared by every writer. A hardcoded release toggle drives a configured widget. All five SOLID principles are shown with code |
| [Development Discipline](part-b/development-discipline.md) | **3** | Three new MRs (#145 with 16 commits, #193 with 17, #196 with 4) and a second round on two more. Each subject is tagged with its TDD phase and OWASP category. Descriptions carry the contract, tables, E2E and screenshots, and are kept current after merges |
| [Team Development Management](part-b/team-development-management.md) | **3** | Two reviews, each verified by running the code. On #144, a scratch test showed a logging gap: a database bug would hide as a 503 with no traceback. On #202, the restore path had lost its route guards and tests, with a concrete fix. Seven findings received on #137 and #174 were fixed and answered in their threads |
| [Code Quality](part-b/code-quality.md) | **3** | 0 open SonarCloud issues on all five MRs. Three findings on my own code (two S3776, one S3358) were fixed by refactoring, not suppressed. A duplicated domain rule was removed on my own initiative |
| [Security](part-b/security.md) | **3** | A ZAP scan per finished sub-issue (PIL-428, PIL-435), signed in and limited to the feature: 0 High, every alert explained. Reading the scan history found a NUL-byte 500 on six list endpoints, with a test-first patch plan. Four OWASP categories named in commits |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims checked by running the code before acting: on reviews, before blaming the app in E2E, and before calling failures pre-existing. Its own wrong turns are reported. A test-first discipline was kept even inside merge commits |

Work this week:

- **[PIL-428](https://linear.app/pilah-2/issue/PIL-428): Hapus a setoran** (31 Oct).
    - **Design choices:** I picked three options when asked: Hapus in the existing hold-to-select header, a required alasan, and voided rows shown in Riwayat only.
    - **Backend:** the void reverses the saldo, shifts later pencairan snapshots, and refuses money already paid out. Who, when and why are recorded, and a check constraint makes a half-recorded void impossible.
    - **After staging moved** (2 Nov): merged staging's inline setoran detail (PIL-453) into #193 and carried the Pembatalan section onto it test-first. Re-ran Playwright: 21/21.
- **[PIL-435](https://linear.app/pilah-2/issue/PIL-435): Riwayat setoran only** (31 Oct). The type selector is hidden, not left as a dead control. The default and the reopen path are named in one place. Playwright: 18/18.
- **Reviews received and answered** (2 Nov):
    - Tristan and Heraldo on #137: the Google-login membership claim was the fourth writer of the role-change invariant, and it lacked the row lock. Fixed with a race test.
    - Tristan, Scallss and Heraldo on #174: draft and form handling on a role change, and spacing tokens. Fixed after merging staging's redesigned onboarding.
- **Reviews given** (2 Nov): [pilah-be #144](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#pullrequestreview-5737653085) and [pilah-mobile #202](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#pullrequestreview-5737765335).
- **Coordination:** flagged a migration-number clash between #137 and #145 on both PRs (31 Oct).
- **Security scans** (2 Nov): [OWASP ZAP on PIL-428 and PIL-435](../security/zap-2026-11-02.md), each right after the sub-issue was finished.
