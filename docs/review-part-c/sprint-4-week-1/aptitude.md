# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    Two new learnings from outside the class material, each applied in the PILAH project this week (Sprint 4 Week 1, 18 – 24 Nov) and linked to the code or report that shows it:

    1. **Returning a result from a pushed route** in go_router, and showing a toast after the navigation it triggers;
    2. **How ZAP's active scan finds its targets,** and how to attack an endpoint that only ever receives POST.

The rubric's level 3 is one or two new learnings outside the class material, applied in the project. Things the course already covers are left out: basic TDD, Git branching, SonarQube.

## Learnings applied this week

| # | Learning | Applied in | Evidence |
|---|---|---|---|
| 1 | **A pushed page that answers its caller.** The parts I learned and used: <ul><li>`context.push<bool>(route)` returns a `Future` that completes with whatever the page pops, so the caller decides what to do next;</li><li>`context.pop(true)` on success, and a plain back resolving to `null`, so "applied" and "went back" are told apart;</li><li>checking `context.mounted` before acting on the result, since the page may be gone by then;</li><li>a toast raised after navigation needs a navigator that outlives the popped page: here the app's `rootNavigatorKey`, which the test router has to use too.</li></ul> | #276: Bank sampah saya reloads only when an application was sent | [`9c7ecac`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9c7ecac2), [`b34db8b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b34db8be) |
| 2 | **ZAP's site tree and the active scan.** The parts I learned and used: <ul><li>the active scan attacks nodes of ZAP's site tree, and looking up a URL finds the GET node;</li><li>so a path that only ever saw POST answers "URL Not Found in the Scan Tree", even though ZAP recorded the request;</li><li>the fix: find the recorded message for that method and URL, and start the scan with its method and body;</li><li>signing the scan in as a different role (a nasabah) by passing that account's token to the bearer rule.</li></ul> | The 23 Nov scan of PIL-539: `POST /onboarding/nasabah`, the endpoint the feature depends on | [ZAP report, 23 Nov](../../security/zap-2026-11-23.md), [`tools/zap_scan.py`](https://github.com/mvfi0/pilah-docs/blob/main/tools/zap_scan.py) |

## How each one changed the work

- **The route result removed a whole class of bugs.** Without it, the list would either reload every time it's shown, or need a callback passed into the form. With `push<bool>`, the list reloads exactly when an application was sent, and the test can assert both cases: `[true]` and `[]`.
- **Knowing why the scan skipped the endpoint turned a clean-looking report into a real one.** The first run looked fine but had never attacked the one path that mattered. After the fix, 224 attacks hit it, and the 17 Nov limit on `DELETE /device-tokens/` is closed for every later scan.

## Also used

- **Scanning within a memory budget,** learned on 16–17 Nov: ZAP's heap capped at 1 GB, one backend at a time, each started with an empty environment. Used again, so it isn't claimed.
- **Merging a long-lived stacked branch:** retargeting #276 after #267 landed, then resolving the conflict by keeping both sides. That's Git practice the course covers, so it isn't claimed.
