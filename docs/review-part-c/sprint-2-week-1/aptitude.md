# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    New learnings from outside the material generally given in class, each applied in the PILAH project this week (Sprint 2 Week 1, 6–14 Oct) and linked to the commit, PR or report that shows it.

The rubric's level 3 asks for 1–2 new learnings outside class material that are applied in the project; level 4 asks for 3 or more. Things the course already covers (basic TDD, Django/Flutter CRUD, Git branching) are deliberately left out.

## New learnings applied this week

| # | Concept | Applied in | Evidence |
|---|---|---|---|
| 1 | **Stacked pull requests, and splitting scope without rewriting history**: keep dependent work as a chain of PRs each targeting the one below, and when a reviewer asks to move a change out of a PR, use `git revert` plus `cherry-pick -x` instead of a force-push, so existing review links and evidence stay valid | PIL-331 stacked on PIL-304 (`staging` ← #79 ← #92 ← #96); the jenis-filter allow-list reverted from #79 and re-applied as #96 | [pilah-be #96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96), [`98456ff`](https://github.com/bank-sampah-PILAH/pilah-be/commit/98456ff), [`2921a37`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2921a37), [Development Discipline](../../review-sprint-2-week-1/part-b/development-discipline.md) |
| 2 | **Testing generated / dependency-injected code**: resolve every entry of a generated DI graph inside a test so the generated file is actually exercised, not excluded from coverage — which turned up a real startup crash a hand-maintained copy had hidden | pilah-mobile #74: `di_graph_test` builds all 92 registrations in dev and prod; found that CI-built apps could not construct `AuthenticationBloc` | [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74), [`06ece1b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/06ece1b), [`320612b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/320612b), [Code Quality](../../review-sprint-2-week-1/part-b/code-quality.md) |
| 3 | **Dynamic application security testing (DAST)**: scan a running web API with Metasploit's HTTP auxiliary scanners, read the result against the application rather than expecting an off-the-shelf exploit, and cross-check the dynamic findings with a static configuration check | the backend security scan on a local instance: Metasploit + `curl` verification + `manage.py check --deploy`, with a test-first patch plan | [Security scan report](../../security/index.md), [Security page](../../review-sprint-2-week-1/part-b/security.md) |

## How each one changed the work

- **Stacked PRs** kept four interdependent changes reviewable on their own — each diff shows only its own feature — and let me answer "split this out of the PR" without breaking the links already in last week's evidence. Before this I would have force-pushed and orphaned every review thread.
- **Testing generated code** turned an awkward coverage gap (SonarCloud counting generated registrations as uncovered) into a real finding: the dependency graph CI generates could not build the app's auth bloc, so every CI-built APK or web build would have crashed on launch. Covering the file is now what guards against that class of bug.
- **Dynamic security testing** gave the project its first outside-in security read: it confirmed the access controls hold and the headers are mostly right, but also that `/api/schema/` and `/api/docs/` are public and HSTS is unset — concrete, fixable findings a code review alone had not surfaced.

## Also explored

- **Playwright driving Flutter web through the semantics tree** (how an end-to-end browser tool reaches a canvas-rendered Flutter app by its accessibility layer), used to screenshot the PIL-341 desktop layouts and catch a dialog-corner bug the widget tests missed. Kept as a local practice for now, not yet a fourth claimed learning because the scripts are not in the repo.
