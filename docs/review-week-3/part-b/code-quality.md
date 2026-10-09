# Code Quality

!!! success "Competency level: 3"
    No open SonarCloud issue on any of my three merge requests, checked directly with the new SonarQube CLI instead of the website. Both issues SonarCloud raised on my code this week were fixed on the branch, one of them test-first. Every CI quality gate passes on both repositories.

## SonarCloud, read with the SonarQube CLI

This week I set up `sonarqube-cli` (`sonar`), authenticated to SonarCloud (org `bank-sampah-pilah`). It lists issues for a project, branch or pull request from the terminal, so checking a PR no longer means opening the website:

```console
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 79
$ sonar list issues -p bank-sampah-PILAH_pilah-be --pull-request 89
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --pull-request 62
$ sonar list issues -p bank-sampah-PILAH_pilah-be --branch staging
$ sonar list issues -p bank-sampah-PILAH_pilah-mobile --branch staging
```

| Scope | Open issues | Mine |
|---|---|---|
| pilah-be [#79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) (PIL-304) | 0 | 0 |
| pilah-be [#89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89) (rounding follow-up) | 0 | 0 |
| pilah-mobile [#62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) (PIL-304) | 0 (1 before the fix below) | 0 |
| pilah-be `staging` | 0 | 0 |
| pilah-mobile `staging` | 53 | 0: every one is authored by other members (counted by the `author` field the CLI returns) |

The SonarCloud quality gate also passed on every analysis of #79 and #89.

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
