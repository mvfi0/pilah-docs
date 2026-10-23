# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    Two new learnings from outside the material given in class, each applied in the PILAH project this week (Sprint 2 Week 2, 16–23 Oct) and linked to the PR or commit that shows it.

The rubric's level 3 is one or two new learnings outside class material, applied in the project. Things the course already covers (basic TDD, widget tests, Git branching, SonarQube) are left out.

## New learnings applied this week

| # | Learning | Applied in | Evidence |
|---|---|---|---|
| 1 | **End-to-end testing of Flutter web through its semantics tree, with assertions.** Flutter web draws on a canvas, so a browser tool can only reach it through the accessibility (semantics) layer. Last week I only explored this: screenshots, nothing asserted. This week the checks wait on labels instead of fixed pauses, assert outcomes, measure where elements sit, and handle labels that Flutter merges into one node. | PIL-341 slice 3 (#127), and both QA fixes (#153, #154), at desktop and phone sizes against a local build and backend | [#127](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127), [#153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153), [#154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154) (E2E tables and screenshots in each description) |
| 2 | **Client-side routing state, and route parameters as untrusted input.** In go_router, `push` doesn't write to the browser URL unless `optionURLReflectsImperativeAPIs` is on, so "survives a refresh" means something different for pushed and `go` routes. And a value read from the URL that ends up in an API path can steer the user's own authenticated requests elsewhere, unless it is validated. | #127: a saved draft opens from `?id=`, and only a bare id is accepted (OWASP A01, A03). The refresh limitation was documented for the lead dev rather than worked around app-wide. | [`a491758`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a491758), [`7d938f9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7d938f9), [Security](../../review-sprint-2-week-2/part-b/security.md) |

## How each one changed the work

- **E2E with assertions** turned the Playwright runs from visual QA into checks that can fail.
    - They confirmed both QA fixes at both sizes: the note, the confirmation, the list and the locked Tanggal.
    - They caught a misaligned total in the desktop side panel. It was also wrong on phones, and was fixed test-first.
    - They surfaced a desktop dialog whose title never reaches the semantics tree. That is recorded as INFO, a likely accessibility gap, rather than marked as a pass.
- **Treating route parameters as input** changed a feature I had planned as a convenience (open a draft from its link) into one with a guard. The test sends `../nasabah`, `d-1/konfirmasi` and a space, and asserts that no request is built from them. Learning how `push` and the URL interact also stopped me from promising a refresh behaviour the app's router doesn't give.

## Also used

- **Mutation checks as a review technique.** On Ghani's #162, I put the removed code back to prove his new tests catch it (8 of 8 failed). I used mutation checks on my own tests last week. Using one to verify a teammate's claim before commenting is new, but I'm not counting it as a third learning.
