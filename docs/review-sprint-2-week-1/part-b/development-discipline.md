# Development Discipline

!!! success "Competency level: 3"
    Four new merge requests this week:

    - PIL-331 on both repositories;
    - a fix to the app's generated dependency graph;
    - a scope split asked for in review.

    All use scoped Conventional Commits with the TDD phase in each subject, a detailed description and green CI, and all four are approved. Where one depends on another, it is stacked on it, so each diff shows only its own change. Every finding from the week's review round was fixed on its branch and answered in its thread.

## Merge requests

| MR | Repo | Opened | Size | Commits | Review |
|---|---|---|---|---|---|
| [#92 — PIL-331: price history per jenis sampah](https://github.com/bank-sampah-PILAH/pilah-be/pull/92) | pilah-be | 11 Oct | +195 / −4, 5 files | 8 | approved |
| [#73 — PIL-331: price history per jenis sampah](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73) | pilah-mobile | 11 Oct | +797 / −6, 24 files | 22 | approved, after 2 findings fixed |
| [#74 — fix(di): cover the generated DI graph](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) | pilah-mobile | 11 Oct | +381 / −8, 7 files | 12 | approved, after a conflict and 1 finding |
| [#96 — Allow-list the jenis list filters (OWASP A03)](https://github.com/bank-sampah-PILAH/pilah-be/pull/96) | pilah-be | 12 Oct | +46 / −10, 3 files | 2 | approved |

Sizes and commit counts are from GitHub on 14 Oct.

The review fixes on 12 Oct also went into [#79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) and [#62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62). Those PRs are claimed in Sprint 1 Week 3, so here they count only as this week's commits.

## How they fit together

- **PIL-331 stacks on PIL-304.** It reads PIL-304's price-version table, so #92 targets `feature/pil-304` and #73 targets #62's branch. Each diff shows only PIL-331, and they merge in order.
- **#96 was split out in review.** Tristan noted the filter allow-list was outside PIL-304's scope. Instead of force-pushing #79, I reverted it there ([`98456ff`](https://github.com/bank-sampah-PILAH/pilah-be/commit/98456ff)) and re-applied the same two commits with `cherry-pick -x` as #96, stacked on #92: `staging` ← #79 ← #92 ← #96. History stays intact, and the commit links in last week's evidence keep working.
- **#74 has its own branch off `staging`.** It fixes something the coverage work uncovered, in the app's dependency graph and CI, not in PIL-304 or PIL-331.

## Example commit messages

```
test(seed): [RED] add failing test for keeping historical setoran prices on reseed

Rerunning the seed after a price change takes effect now rewrites old
setoran snapshots and totals at today's price (3500 -> 99999 here).
```

```
fix(harga): [GREEN] ignore a list reload that a newer one has replaced

loadHarga numbers each request and drops an answer when a newer reload
has started since, so the reload after the price POST always wins over
the one after the PUT, whichever answers first.
```

```
revert(harga): move the jenis filter allow-list out of PIL-304

Reverts 94267c8 and cef01bb. Tristan's review on #79 noted the 422 for
unknown status/kategori filters changes GET /jenis-sampah beyond
PIL-304's price versioning. The same change comes back unchanged as its
own PR stacked on top of PIL-331 (#92).
```

## Keeping the branches mergeable

- **The review round, 11–12 Oct.** Tristan's 8 findings over #79, #62, #73 and #74 were each:
    - checked against the code first;
    - fixed test-first;
    - answered in their own thread with the commit links.

  See [Team Development Management](team-development-management.md).
- **#74 kept up with `staging`.** `staging` moved while #74 was open. I merged it in, resolved the conflict in favour of Tristan's identical fix from #71, and added the new registrations to the dependency-graph test.
- **Validated locally before every push**, with CI's own commands:
    - backend: ruff, mypy strict, the migration check, the full suite with coverage, and diff-cover;
    - mobile: `dart format`, `flutter analyze --fatal-infos`, `flutter test --coverage` with the generated-code marker dropped (as CI now does), and diff-cover.
