# PIL-230 and PIL-176 Review Round — Coverage of My Changes

Diff-coverage evidence for the week-2 TDD claim: how much of the code I **added or changed** is executed by the tests. Each report is an HTML page from [diff-cover](https://github.com/Bachmann1234/diff_cover), listing every changed line and whether a test ran it.

| Change | PR | Measured at | Changed lines | Covered | Report |
|---|---|---|---|---|---|
| PIL-230 backend: edit pencairan, revision history | [pilah-be #52](https://github.com/bank-sampah-PILAH/pilah-be/pull/52) | [`011fda3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/011fda3) vs its base [`28fca9c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/28fca9c) | 148 | **100%** | [pil-230-be-diff-coverage.html](pil-230-be-diff-coverage.html) |
| PIL-176 second review round (Tristan's 4 findings) | [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | [`8349b37`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8349b37) vs the staging merge [`9a89c01`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9a89c01) | 34 | **100%** | [pil-176-review2-diff-coverage.html](pil-176-review2-diff-coverage.html) |
| PIL-230 mobile: edit form, change history, entry points | [pilah-mobile #33](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/33) | [`4a52399`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4a52399) vs its base [`a6cdfe6`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a6cdfe6) | 325 | **82.8%** (CI gate 25%) | [pil-230-mobile-diff-coverage.html](pil-230-mobile-diff-coverage.html) |

Measured 28 Sep 2026. Test code, migrations and generated files (`*.freezed.dart`, `*.g.dart`) are excluded, so tests never count as covering themselves.

## Why each report compares against a fixed commit

These PRs were stacked (#19 → #32 → #52, and #26 → #27 → #33) and have since been squash-merged. After the merges the base branches moved on: `origin/feature/pil-222` now points at `07d19d2` (backend) and `64a2735` (mobile). Comparing against the moving branch counted other people's merged code as mine (565 mobile lines instead of 325). Each report therefore compares against the exact commit the PR was built on:

- **#52** against `28fca9c`, the head of #32 when PIL-230 branched from it.
- **#19 review round** against `9a89c01`, the commit that merged `staging` into #19. Everything after it is my four fixes and their docs; the staging merge itself (other members' code) is left out.
- **#33** against `a6cdfe6`, the head of #27.

## Where the lines are

**PIL-230 backend** (`011fda3`):

| File | Changed ranges | What they are |
|---|---|---|
| `api/models.py` | [365–391](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/models.py#L365-L391) | `PencairanRevisi` (append-only) |
| `api/services.py` | [425–429](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/services.py#L425-L429), [475–615](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/services.py#L475-L615) | 7-day constant, `edit_pencairan`, the ledger replay, revision annotations |
| `api/serializers.py` | [30–43](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/serializers.py#L30-L43), [54–77](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/serializers.py#L54-L77), [113–141](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/serializers.py#L113-L141) | shared validators, `PencairanEditSerializer`, `diperbarui`, `tanggal_edit_minimum`, revision serializer |
| `api/views.py` | [603](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/views.py#L603), [624–642](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/views.py#L624-L642) | `partial_update` (PATCH), `riwayat` action |
| `api/admin.py` | [82–100](https://github.com/bank-sampah-PILAH/pilah-be/blob/011fda3/api/admin.py#L82-L100) | read-only `PencairanRevisiAdmin` |

**PIL-176 review round** (`8349b37`):

| File | Changed ranges | Finding |
|---|---|---|
| `api/admin.py` | [80–92](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/admin.py#L80-L92) | admin writes bypassed the service |
| `api/services.py` | [623–627](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/services.py#L623-L627), [1174–1175](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/services.py#L1174-L1175) | history debits the rounding adjustment |
| | [652–666](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/services.py#L652-L666) | reject a pencairan dated before the last activity |
| `api/permissions.py`, `api/views.py` | [21–27](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/permissions.py#L21-L27), [52–60](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/permissions.py#L52-L60), [651–663](https://github.com/bank-sampah-PILAH/pilah-be/blob/8349b37/api/views.py#L651-L663) | nasabah read their own pencairan |

**PIL-230 mobile**: the cubits, repository, remote data source, mapper, validator and the riwayat entry points are at 100%. The 56 uncovered lines are wiring rather than behaviour:

| Uncovered | Lines | Why no test reaches it |
|---|---|---|
| Date picker callback in `edit_pencairan_page.dart` | 70–89 | widget tests don't open the platform date picker; the bounds it uses (`tanggal_edit_minimum`, today) are covered through the view |
| `EditPencairanPage` / `RevisiPencairanPage` wrappers | 22–28 / 18–24, 32 | they only resolve the cubit from dependency injection; tests build the views with their own cubit |
| Route registrations in `app_router_config.dart` | 135–145 | the entry-point tests use a stub router |
| `props` getters of `RevisiPencairan`, `RiwayatRevisiPencairan`, `EditPencairanRequest` | `revisi_pencairan.dart` 31–42, 54–55; `pencairan.dart` 53–54 | equality is never compared on these objects in tests |
| `PencairanInteractor` pass-throughs | 32–42 | cubit tests mock the use-case interface directly |

The report lists every missed line.

## How to reproduce

Backend, from the PR's worktree:

```bash
coverage run --source=api manage.py test
coverage xml -o cov.xml
diff-cover cov.xml --compare-branch=28fca9c \
  --exclude "*/tests.py" "*/test_*.py" "*/migrations/*" \
  --format html:pil-230-be-diff-coverage.html
```

Mobile (Flutter 3.38.3, the CI version):

```bash
flutter test --coverage
# Windows writes backslashes into lcov.info; normalise them to / first
diff-cover coverage/lcov.info --compare-branch=a6cdfe6 \
  --exclude "*.freezed.dart" "*.g.dart" \
  --format html:pil-230-mobile-diff-coverage.html
```
