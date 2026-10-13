# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on any of this week's four merge requests, checked with the SonarQube CLI, and the quality gate passed on all four. Every CI quality gate passes on both repositories.

    I also found and closed a gap in the quality setup itself: the app's generated dependency graph was excluded from coverage, and it hid a startup crash. See [Raising the bar](#raising-the-bar-measuring-generated-code).

## SonarCloud, read with the SonarQube CLI

```console
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 92
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 96
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --pull-request 73
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --pull-request 74
```

| Scope | Open issues | New-code coverage (SonarCloud) |
|---|---|---|
| pilah-be [#92](https://github.com/bank-sampah-PILAH/pilah-be/pull/92) (PIL-331) | 0 | 100% |
| pilah-be [#96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96) (filter allow-list) | 0 | 100% |
| pilah-mobile [#73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73) (PIL-331) | 0 | 96.5% |
| pilah-mobile [#74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) (generated DI graph) | 0 | 100% |

#73's 3.5% is the two registrations it adds to the generated `di.config.dart`:

- **Covered locally:** they are covered by a test ([`eb9b20f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/eb9b20f)), and diff-cover counts 100% of #73's 141 changed lines with the generator's marker dropped.
- **Not yet on SonarCloud:** #73's branch predates #74, so its CI still leaves the file out of lcov while Sonar analyses it.
- **When it clears:** the number follows once #74 is merged and the stack takes `staging`.

The section below is what #74 changes.

## Raising the bar: measuring generated code

SonarCloud put #62 at 97.4% and #73 at 96.2%. Every uncovered line was a registration in the generated `lib/services/di.config.dart`. Generated or not, it is code that ships, so I covered it rather than explaining it away.

**Why it was invisible:**

- `injectable_generator` marks the file `// coverage:ignore-file`, so lcov leaves it out.
- `sonar.yml` also excluded it from analysis.

**What covering it found:** the graph CI builds could not create `AuthenticationBloc`, because it asked dependency injection for a `bool` nobody registers. `app.dart` creates that bloc at start-up, so CI-built apps would crash on launch. Local `flutter run` hid it, because it uses a hand-maintained copy of the file.

**The fix, [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74):**

- **A full-graph test.** `di_graph_test` builds every registration in dev and prod, and fails when a new registration is missing from its list.
- **Coverage in CI.** CI and SonarCloud now measure the file: the marker is dropped after code generation ([`941f24d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/941f24d)), and the Sonar exclusion is removed, as Tristan asked in review ([`26fcf40`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26fcf40)).
- **Result:** every executable line of the file is covered.
- **Docs.** `AGENTS.md` now says how the generated file is committed and tested.

The crash itself reached `staging` first through Tristan's #71 (the same `@ignoreParam` fix), so #74 keeps `staging`'s version of the bloc.

## Automated checks, all passing

- **Backend (#92, #96, and the #79 fixes):** `ruff check`, `ruff format --check`, `mypy` strict, `makemigrations --check`, `tests/test_architecture.py`, coverage 100% and diff coverage 100%.
- **Mobile (#73, #74, and the #62 fixes):** `dart format --set-exit-if-changed`, `flutter analyze --fatal-infos`, `flutter test --coverage`, and diff coverage 100% with generated code included.
