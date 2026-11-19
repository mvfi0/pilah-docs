# IR Part B Sprint 3 Week 3

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 3 week 3.

!!! note "What this page covers"
    [Sprint 3 Week 2](../review-sprint-3-week-2/index.md) claims work up to 10 Nov. This page covers **11 – 17 Nov**, up to the Tuesday it was due. The merges of these PRs on 18 Nov belong to the next week.

    - **Three new backend PRs, all test-first** (16 Nov):
        - [pilah-be #175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175), [PIL-482](https://linear.app/pilah-2/issue/PIL-482): a malformed `nasabah_id` filter answers 422, not 500. This fixes the 9 Nov ZAP finding;
        - [pilah-be #176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176): an architecture test forbids writing the counted-setoran rule by hand, and the last read that did now uses `tercatat()`;
        - [pilah-be #177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177): a NUL byte in a request body, or a padded duplicate kode, gave 500 on three edit paths; now 422.
    - **The third review round on [PIL-451](https://linear.app/pilah-2/issue/PIL-451)** ([#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137), [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174)): `staging` merged in twice, then Tristan's two P2 findings fixed test-first.
    - **The review round on PIL-481 and PIL-480** ([#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167), [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238), [#168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168)): Heraldo's findings fixed on 11 Nov; all three merged that night.
    - **Reviews given:** Gabriel's PIL-478 pair ([pilah-be #169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169), [pilah-mobile #243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243)) and his [pilah-be #174](https://github.com/bank-sampah-PILAH/pilah-be/pull/174), each checked out and run, with mutants or recomputed hashes.
    - **ZAP scans of #175, #176 and #177** (17 Nov).

| Competency | Level | Status (17 Nov) |
|---|---|---|
| [Test Driven Development](part-b/tdd.md) | **4** | Eight green steps, each after its `[RED]` commit (ten in all), across six MRs, plus refactors after green. SonarCloud new-code coverage is 100% on every MR with lines to cover. The tests include an architecture fitness function that parses the source, a two-thread race test on PostgreSQL, and an HTTP contract test over three endpoints |
| [Programming](part-b/programming.md) | **3** | A boundary validator in `shared_kernel`, validate-then-query moved into the serializers, a narrow serializer the wider one extends, one account lock for a fifth writer, a reused navigation policy, and a named constant for copy. All five SOLID principles shown with code |
| [Development Discipline](part-b/development-discipline.md) | **3** | Three new MRs (#175 with 3 commits, #176 with 2, #177 with 8), a third round on #137 and #174, and a round on #167 and #238. Every subject carries its TDD phase; every body the design issue, pattern, origin, OWASP and SOLID notes |
| [Team Development Management](part-b/team-development-management.md) | **3** | Three reviews, each verified by running the code: mutants on the PIL-478 pair (6 of 10 caught) found a server-side claim that doesn't hold; recomputed hashes on #174 found that a version bump with stale hashes passes every test. Nine review threads received, each answered in place |
| [Code Quality](part-b/code-quality.md) | **3** | 0 open SonarCloud issues, 0 hotspots and 0.0% duplication on new code on all seven MRs. One S3776 on my own code was fixed by refactoring within the hour. A duplicated domain rule is now guarded by a test |
| [Security](part-b/security.md) | **3** | ZAP scans of the three new PRs: 0 High, no new finding, and the 9 Nov finding verified fixed (965 malformed ids, all 422, none 500). Two leaked webhooks found in my own evidence were redacted and the scanner hardened. Five OWASP categories genuinely guarded in commits |
| [AI Literacy](part-b/ai-literacy.md) | **3** | Claims checked before acting: mutants instead of trusting a test suite, recomputed hashes instead of screenshots, a scan rerun when the machine failed, a false claim in my own report corrected |

Work this week:

- **Review round on PIL-481 and PIL-480** (11 Nov): Heraldo's findings fixed test-first, and the date-test fix cherry-picked so CI could run. Scallss merged all three at 01:11 on 12 Nov.
- **Reviews given:** Gabriel's PIL-478 pair (12 Nov) and his #174 (17 Nov).
- **PIL-451:** `staging` merged into both PRs (13 Nov, 16 Nov), then Tristan's third-round findings fixed (16 Nov).
- **Three test-first backend PRs** (16 Nov): #175, #176 and #177.
- **Security:** two Discord webhooks found in the 9 Nov scan evidence and redacted, with the scan script hardened (13 Nov); [ZAP scans of #175, #176 and #177](../security/zap-2026-11-17.md) (17 Nov).
