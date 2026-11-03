# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    Two new learnings from outside the class material, each applied in the PILAH project this week (Sprint 3 Week 1, 31 Oct – 3 Nov) and linked to the code or report that shows it:

    1. **Automating OWASP ZAP through its API** to scan one feature at a time;
    2. **Database-enforced invariants and row locks** in Django on PostgreSQL.

The rubric's level 3 is one or two new learnings outside the class material, applied in the project. Things the course already covers are left out: basic TDD, widget tests, Git branching, SonarQube.

## Learnings applied this week

| # | Learning | Applied in | Evidence |
|---|---|---|---|
| 1 | **Driving OWASP ZAP from a script instead of its GUI.** The parts I learned and used: <ul><li>headless `-daemon` mode and its JSON API;</li><li>a replacer rule that signs every request in;</li><li>importing the OpenAPI schema;</li><li>sending real requests through ZAP's proxy so the active scan attacks real ids and bodies;</li><li>a scan context that limits the active scan to one feature;</li><li>the report API.</li></ul> I also learned where ZAP's alerts stop: it doesn't raise a 500 as an alert, so the scan history has to be read for crashes. | A scan of each sub-issue right after it was finished (PIL-428, PIL-435), from one reusable command | [`tools/zap_scan.py`](https://github.com/mvfi0/pilah-docs/blob/main/tools/zap_scan.py), [ZAP report, 2 Nov](../../security/zap-2026-11-02.md) |
| 2 | **Invariants the database enforces, and locks that serialize writers.** The parts I learned and used: <ul><li>a `CheckConstraint` so a void can't be half-recorded by any write path, proven by attempting one and expecting `IntegrityError`;</li><li>a fixed lock order (saldo, then setoran) shared by void and edit;</li><li>`refresh_from_db(from_queryset=select_for_update())` (Django 5.1) to lock and reload in one query;</li><li>a custom `QuerySet` method to name a domain rule once;</li><li>PostgreSQL refusing NUL bytes in text, which explained the crash the scan found.</li></ul> | PIL-428 (#145); the second PIL-451 review round (#137) | [`2814ae6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2814ae6), [`d19cb8d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d19cb8d), [`7c7c1f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7c7c1f3), [`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0) |

## How each one changed the work

- **Scripted ZAP turned security from a one-off into a routine.** Scanning a feature now takes one command and a small file of that feature's real requests, so every finished sub-issue gets a scan, not one scan a sprint.
    - **What it found:** reading the history found a real crash no alert showed. A NUL byte in `?search=` gives a 500 on six list endpoints, now in the patch plan.
    - **What it took to get right:** three mistakes of my own were caught before any result was trusted. Git Bash rewrote the scope paths, id paths couldn't be scanned by URL, and the report filter used the wrong separator.
- **The database as the last guard** changed how PIL-428 was built.
    - The rule "a voided setoran carries who, when and why" lives in a constraint, not only in the service, so a direct `.update()` can't break it.
    - On PIL-451, the review showed a fourth writer racing a role change. I knew which tool fixes that class of bug: the same row lock, then a re-check. The two-thread test proves it.

## Also used

- **Release toggles as named constants** (PIL-435): closing a feature by configuring a widget rather than editing it, so reopening is one edit and a release.
- **Reading a merge for lost behaviour.** When `staging` replaced the detail sheet with an inline row (PIL-453), I checked which of my feature's behaviour the merge silently dropped (the Pembatalan section), and rebuilt it test-first. That's a habit rather than a new learning, so it isn't claimed.

## Also read

- **The Metasploit Framework and how it works** (30 min). This was read, not yet applied in PILAH, so it isn't claimed as a learning this week.
