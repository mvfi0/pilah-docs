# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on any of my seven merge requests, checked directly with the new SonarQube CLI instead of the website. Both issues SonarCloud raised on my code this week were fixed on the branch, one of them test-first. Every CI quality gate passes on both repositories.

    I also found and closed a gap in the quality setup itself: the app's generated dependency graph was excluded from coverage, and it hid a startup crash. See [Raising the bar](#raising-the-bar-measuring-generated-code).

## SonarCloud, read with the SonarQube CLI

This week I set up `sonarqube-cli` (`sonar`), authenticated to SonarCloud (org `bank-sampah-pilah`). It lists issues for a project, branch or pull request from the terminal, so checking a PR no longer means opening the website:

```console
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 79
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 89
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --pull-request 62
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 92
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 96
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --pull-request 73
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --pull-request 74
$ sonar list issues -p bank-sampah-PILAH_pilah-be --branch staging
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --branch staging
```

| Scope | Open issues | Mine |
|---|---|---|
| pilah-be [#79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) (PIL-304) | 0 | 0 |
| pilah-be [#89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89) (rounding follow-up) | 0 | 0 |
| pilah-mobile [#62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) (PIL-304) | 0 (1 before the fix below) | 0 |
| pilah-be [#92](https://github.com/bank-sampah-PILAH/pilah-be/pull/92) (PIL-331) | 0 | 0 |
| pilah-be [#96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96) (filter allow-list) | 0 | 0 |
| pilah-mobile [#73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73) (PIL-331) | 0 | 0 |
| pilah-mobile [#74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) (generated DI graph) | 0 | 0 |
| pilah-be `staging` | 0 | 0 |
| pilah-mobile `staging` | 50 (13 Oct; 53 on 9 Oct) | 0: every one is authored by other members (counted by the `author` field the CLI returns) |

The SonarCloud quality gate passed on every analysis of all seven. New-code coverage on SonarCloud is 100% on #79, #89, #62, #92 and #96. #73 shows 96.2% until #74 lands, for the reason below.

## Issues raised on my code this week, and their fixes

| Rule | Where | Fix |
|---|---|---|
| `python:S9073` Split this composite assertion | `apps/waste_catalog/test_harga_versi.py`, #79 | [`fe5db58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fe5db58). `assert a is not None and b is not None` became two asserts, so a failure names the missing value. They stay plain `assert`s, because mypy narrows types on those and not on `assertIsNotNone`. |
| `dart:S3358` Extract this nested ternary operation | `tambah_jenis_sampah_bottom_sheet.dart:456`, #62 | Test-first: [`2fca502`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2fca502) `[RED]` → [`47a2160`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/47a2160) `[GREEN]` → [`2ce3dab`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2ce3dab) `[REFACTOR]`. The success message choice moved into `pesanSimpanJenis`, a pure function with its own tests; the sheet just passes what happened. |

```dart title="lib/features/harga/presentation/widgets/pesan_simpan_jenis.dart"
String pesanSimpanJenis({
  required bool isEditMode,
  required bool hargaBerubah,
  DateTime? berlakuMulai,
}) {
  if (!isEditMode) return 'Jenis sampah baru berhasil ditambahkan.';
  if (hargaBerubah && berlakuMulai != null) {
    return 'Harga baru berlaku mulai ${formatTanggalId(berlakuMulai)}.';
  }
  return 'Jenis sampah berhasil diperbarui.';
}
```

## Automated checks, all passing

- **Backend (#79, #89):** `ruff check`, `ruff format --check`, `mypy` strict over `api apps config shared_kernel tests`, `makemigrations --check`, `manage.py check --deploy`, `tests/test_architecture.py` (bounded-context imports), coverage ≥ 80% (100%) and diff coverage ≥ 80% (100%), on Postgres in CI and locally on both SQLite and Postgres 16.
- **Mobile (#62):** `dart format --set-exit-if-changed`, `flutter analyze --fatal-infos`, `flutter test --coverage` (707 tests on the branch), coverage gate 25% (69.5%) and diff coverage 100%.

## Quality beyond the tools

- **One rule, one place.** Rupiah rounding lives only in `kalkulasi.bulatkan_rupiah` after [#89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89), and price selection only in the catalog's `harga_berlaku` after [`ee9668d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ee9668d).
- **The docs stay true.** `AGENTS.md` gained an "Aturan harga jenis sampah" section, and the README lists the new endpoint and response fields ([`b024b25`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b024b25)).

## Raising the bar: measuring generated code

SonarCloud put #62 at 97.4% and #73 at 96.2%. Every uncovered line was a registration in the generated `lib/services/di.config.dart`. Generated or not, it is code that ships, so I covered it rather than explaining it away.

**Why it was invisible:**

- `injectable_generator` marks the file `// coverage:ignore-file`, so lcov leaves it out.
- `sonar.yml` also excluded it from analysis.

**What covering it found:** the graph CI builds could not create `AuthenticationBloc`, because it asked dependency injection for a `bool` nobody registers. `app.dart` creates that bloc at start-up, so CI-built apps would crash on launch. Local `flutter run` hid it, because it uses a hand-maintained copy of the file.

**The fix, [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74):**

- **A full-graph test.** `di_graph_test` builds all 92 registrations in dev and prod, and fails when a new registration is missing from its list.
- **Coverage in CI.** CI and SonarCloud now measure the file: the marker is dropped after code generation ([`941f24d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/941f24d)), and the Sonar exclusion is removed, as Tristan asked in review ([`26fcf40`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26fcf40)).
- **Result:** 223 of 223 lines covered.
- **Docs.** `AGENTS.md` now says how the generated file is committed and tested.

The crash itself reached `staging` first through Tristan's #71 (the same `@ignoreParam` fix), so #74 keeps `staging`'s version of the bloc.

