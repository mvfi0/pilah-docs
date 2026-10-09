# Test Driven Development

!!! success "Competency level: 4"
    **Level 3 met:** PIL-304 was built test-first on both sides, with `[RED]`/`[GREEN]`/`[REFACTOR]` in every commit subject. 100% of changed lines are covered in all three merge requests, and each behaviour is tested with positive, negative and corner cases.

    **Level 4:** advanced testing methods in the commits. Mobile uses mocks and stubs for isolation (mocktail, `MockCubit`, captured requests, an injected clock, a stub router). The backend migration is tested forwards and backwards. Two backend tests were proven to guard their code by deliberately breaking the code and watching them fail.

## Backend: PIL-304, [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79)

| Behaviour | Red | Green |
|---|---|---|
| The price in effect at a given time is the latest version that has started | [`2b0c4ab`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2b0c4ab) | [`a41b5d5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/a41b5d5) |
| A setoran prices its items from the version in effect, ignoring scheduled ones | [`e6bf183`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e6bf183) | [`d111495`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d111495) |
| A new jenis records its price as a first version, with its author | [`f0fbe9d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0fbe9d) | [`c729f7a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c729f7a) |
| `POST /jenis-sampah/{id}/harga` changes the price now | [`0a42f99`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0a42f99) | [`df1db9f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/df1db9f) |
| A future `berlaku_mulai` schedules the price; the current one stays | [`68a805e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/68a805e) | [`c53f1a7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c53f1a7) |
| A backdated, far-future or offsetless `berlaku_mulai` is rejected | [`1c829d6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1c829d6) | [`78f1945`](https://github.com/bank-sampah-PILAH/pilah-be/commit/78f1945) |
| A price changed through `PUT` (older app builds) becomes a version | [`f323911`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f323911) | [`ead26b9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ead26b9) |
| The database rejects a price of 0 or below | [`8593164`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8593164) | [`915b3d1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/915b3d1) |
| Migration backfills every price and drops the column; reverse restores it | [`caaceab`](https://github.com/bank-sampah-PILAH/pilah-be/commit/caaceab) | [`ad352fb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ad352fb) |
| The jenis list's query count stays constant | [`c2a7c71`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2a7c71) | [`6c0ba69`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6c0ba69) |
| The list's `status`/`kategori` filters accept only known values | [`94267c8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/94267c8) | [`cef01bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cef01bb) |

**Refactors after green:**

- [`95a62f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/95a62f3): makes the tie-break explicit.
- [`ee9668d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ee9668d): moves price selection out of `kalkulasi`.
- [`1e7da30`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1e7da30): prices at the transaksi's `tanggal`.
- [`fe5db58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fe5db58): splits an assertion SonarCloud flagged.

Tests that passed when written are labelled `test(...): cover …`, not `[RED]`. Examples: access by another bank (A01), recorded setoran staying untouched (A08), a jenis with no price in effect (UC-11 A2), and a jenis created without a price.

**An honest red that wasn't:** the tie-break test passed on SQLite without any code, because SQLite happens to return the newest of two equal rows first. Postgres makes no such promise, so the explicit ordering went in as a `[REFACTOR]` with the reason in its message ([`baf5504`](https://github.com/bank-sampah-PILAH/pilah-be/commit/baf5504), [`95a62f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/95a62f3)), instead of a fake red.

**Coverage:** **100% of the 469 changed lines** ([report](evidence/pilah-be-79-diff-coverage.html)), 464 tests, whole backend 100%, on SQLite and on Postgres 16.

## Backend: rounding follow-up, [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89)

A behaviour-preserving refactor needs its behaviour pinned first:

1. [`5978aec`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5978aec): pins the edit replay's rounding of legacy sen.
2. [`84f8a85`](https://github.com/bank-sampah-PILAH/pilah-be/commit/84f8a85) `[REFACTOR]`: swaps the inline `ROUND_DOWN` for `bulatkan_rupiah`.
3. [`3c806e5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c806e5): after Gabriel's review, pins that the rounding happens per pencairan, not once at the end.

**Coverage:** **100% of changed lines** ([report](evidence/pilah-be-89-diff-coverage.html)), 451 tests.

## Mobile: PIL-304, [pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62)

| Behaviour | Red | Green |
|---|---|---|
| The model reads when the current price started and the next scheduled price | [`bc5301e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bc5301e) | [`6884877`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6884877) |
| Local times are sent as ISO 8601 with their UTC offset | [`dce80aa`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/dce80aa) | [`2a81157`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2a81157) |
| A price change is posted to the new endpoint, and `PUT` no longer sends the price | [`c7fa0b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c7fa0b5) | [`f62ca9b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f62ca9b) |
| The cubit changes a price through `UbahHargaUseCase` and reloads | [`ea35ccb`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ea35ccb) | [`7729d3d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7729d3d) |
| The edit sheet shows the BR-03 warning and the current and scheduled price | [`3a9f7e4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3a9f7e4) | [`b67d38d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b67d38d) |
| Saving applies the price now, or from local midnight of a chosen date | [`f97b492`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f97b492) | [`bb80f22`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bb80f22) |
| The list card shows an upcoming price change | [`1c28897`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/1c28897) | [`392ef5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/392ef5d) |
| The save confirmation names a scheduled price's start date | [`2fca502`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2fca502) | [`47a2160`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/47a2160) |

A widget test caught a real layout bug: at a 360 dp phone width, the scheduled price overflowed the card's trailing price column by 112 px. The line moved to the column that can wrap ([`392ef5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/392ef5d)).

**Coverage:** **100% of the 114 changed lines** ([report](evidence/pilah-mobile-62-diff-coverage.html)), 707 tests, whole app 69.5% (CI gate 25%). The first run showed 92%. [`52ec8d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/52ec8d0) covered the rest: the use case, a failed request, `HargaTerjadwal` equality, and two branches of the sheet.

## Positive, negative and corner cases

| Behaviour | Positive | Negative | Corner |
|---|---|---|---|
| Price lookup | latest started version wins | none started yet → setoran rejected | two versions starting at the same instant: newest row wins; a scheduled version is invisible before its start |
| Change a price | now; from a future date | backdated; > 365 days ahead; no UTC offset; another bank (404); a nasabah (403); price ≤ 0 (DB check) | `PUT` from an older app with the same price adds no version |
| Migration 0021 | every jenis gets a starting version, sen kept | — | starts from the first setoran if older than the last edit; reverse restores the price *in effect*, ignoring a future one; a re-run adds no duplicates |
| Rounding (#89) | legacy sen dropped on edit | — | sen that re-enters between two pencairan is dropped at each step |
| Mobile save | price now; from a date | unchanged price records nothing | picking a date then switching back to Sekarang; a price with no known start date |

## Advanced testing methods

- **Mocks and stubs for isolation (mobile).**
    - `NetworkService` is mocked with mocktail, and the exact payload is captured with `captureAny`, including the UTC offset of a local midnight.
    - The cubit is a `MockCubit` in widget tests.
    - The use case is tested against a mocked repository.
    - The clock is injected (`now: () => DateTime(2026, 10, 7, 10)`), so the date picker test always expects 8 October.
    - The sheet is opened inside a real `GoRouter` with a stub home route, so `context.pop()` after saving has somewhere to go.
- **Mutation checks (backend).** In both #89 tests, I removed or moved the rounding they guard and confirmed the test failed (`315600.75 != 315600.00`) before restoring the code. The verified failures are quoted in the commit messages.
- **Migration testing.** `api/test_migration_0021_harga_backfill.py` drives Django's `MigrationExecutor` to 0020, seeds old-schema rows, migrates to 0021, checks the backfill, then migrates back and checks the restored column. The same migration was also run forwards, backwards and forwards again on a restored copy of the production database (Postgres 16).
- **Query-count assertions.** `CaptureQueriesContext` proves the jenis list costs the same number of queries for one jenis and for five.
