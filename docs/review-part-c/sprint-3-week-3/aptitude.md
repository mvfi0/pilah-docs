# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    Two new learnings from outside the class material, each applied in the PILAH project this week (Sprint 3 Week 3, 11 – 17 Nov) and linked to the code or review that shows it:

    1. **Architecture fitness functions** written with Python's `ast` module;
    2. **Subresource Integrity:** how a browser verifies a CDN file, and how to check the hashes yourself.

The rubric's level 3 is one or two new learnings outside the class material, applied in the project. Things the course already covers are left out: basic TDD, Git branching, SonarQube.

## Learnings applied this week

| # | Learning | Applied in | Evidence |
|---|---|---|---|
| 1 | **A test that checks the architecture, not the behaviour.** The parts I learned and used: <ul><li>`ast.parse` and `ast.walk` to find every `.filter()` / `.exclude()` call in `apps/`;</li><li>reading a call's keywords to spot a hand-written status filter, which a text search would confuse with a comment;</li><li>excluding the one module that owns the rule, and the tests;</li><li>proving the test isn't vacuous by running it on `staging`, where it failed on exactly one line.</li></ul> | #176: "counted setoran" can only be read through `tercatat()` | [`b10fffa`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b10fffaa), [`8d1a931`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8d1a9316) |
| 2 | **Subresource Integrity (SRI).** The parts I learned and used: <ul><li>an `integrity="sha384-…"` attribute makes the browser refuse a CDN file whose bytes changed;</li><li>computing the hash yourself from the exact bytes the CDN serves, base64 of the SHA-384 digest;</li><li>`crossorigin="anonymous"` only works if the CDN sends `Access-Control-Allow-Origin`;</li><li>a pinned version and its hashes must move together, or the page goes blank in a browser while every server-side test passes.</li></ul> | Reviewing Gabriel's #174, which closes the 26 Oct ZAP finding 3 | [Review of #174](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#pullrequestreview-5925723761), [the non-blocking suggestion](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#discussion_r4590137599) |

## How each one changed the work

- **The fitness function turned a convention into a check.** Two weeks ago the rule got a name; this week a test makes sure nothing bypasses it. That's the difference between a reviewer remembering it, as Heraldo did on #167, and CI failing when it's forgotten.
- **Knowing how SRI works made the review concrete.** Instead of trusting the PR's screenshots, I could recompute the hashes, check the CDN's CORS header, and then break the version on purpose. That gave a real failure mode, a blank docs page with green tests, and a fix for it.

## Also used

- **Running scans within a memory budget.** After the 16 Nov attempt ran the machine out of memory: ZAP's heap capped at 1 GB, one backend at a time, and each backend started with an empty environment (`env -i`) so no secret can reach a debug page. That's operating knowledge, not a new technique, so it isn't claimed.
- **Mutation testing by hand** on Gabriel's PIL-478 pair: putting old code back one change at a time to measure a test suite. I've used it before, so it isn't claimed as new.
- **GitHub's `pull_request_review` event,** read up when asked whether the team could be notified of approvals. It wasn't applied, so it isn't claimed.
