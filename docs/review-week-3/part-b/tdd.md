# Test Driven Development

!!! success "Competency level: 4"
    **Level 3 met:** PIL-304 and PIL-331 were built test-first on both sides, with `[RED]`/`[GREEN]`/`[REFACTOR]` in every commit subject. Every review finding Tristan raised on 12 Oct was fixed the same way: a failing test first. Changed lines are 100% covered in all seven merge requests, and each behaviour is tested with positive, negative and corner cases.

    **Level 4:** advanced testing methods in the commits:

    - **Mocks and stubs for isolation:** mocktail, `MockCubit`, `Completer`s that control which request answers first, an injected clock, a stub router, and a fake backend at the HTTP boundary.
    - **Migration tests:** the backend migration is tested forwards and backwards.
    - **Mutation checks:** tests that passed when written were proven to guard their code by breaking the code and watching them fail.
    - **Full-graph test:** a test builds the app's whole generated dependency graph in both environments.

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
| *Review, 12 Oct:* a reseeded setoran keeps the price of its own date, not today's | [`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) | [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f) |
| The jenis list's query count stays constant | [`c2a7c71`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2a7c71) | [`6c0ba69`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6c0ba69) |
| The list's `status`/`kategori` filters accept only known values (moved to #96 on 12 Oct, see below) | [`94267c8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/94267c8) | [`cef01bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cef01bb) |

**Refactors after green:**

- [`95a62f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/95a62f3): makes the tie-break explicit.
- [`ee9668d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ee9668d): moves price selection out of `kalkulasi`.
- [`1e7da30`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1e7da30): prices at the transaksi's `tanggal`.
- [`fe5db58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fe5db58): splits an assertion SonarCloud flagged.

Tests that passed when written are labelled `test(...): cover …`, not `[RED]`. Examples: access by another bank (A01), recorded setoran staying untouched (A08), a jenis with no price in effect (UC-11 A2), and a jenis created without a price.

**An honest red that wasn't:** the tie-break test passed on SQLite without any code, because SQLite happens to return the newest of two equal rows first. Postgres makes no such promise, so the explicit ordering went in as a `[REFACTOR]` with the reason in its message ([`baf5504`](https://github.com/bank-sampah-PILAH/pilah-be/commit/baf5504), [`95a62f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/95a62f3)), instead of a fake red.

**Coverage:** **100% of the 459 changed lines** ([report](evidence/pilah-be-79-diff-coverage.html), 12 Oct, after the review fixes and with the filter moved out), 464 tests, whole backend 100%. Tests also ran on Postgres 16. The seed now writes its price through `catat_harga` ([`dc29a68`](https://github.com/bank-sampah-PILAH/pilah-be/commit/dc29a68)), a refactor the existing seed tests cover.

## Backend: PIL-331, [pilah-be #92](https://github.com/bank-sampah-PILAH/pilah-be/pull/92), stacked on #79

| Behaviour | Red | Green |
|---|---|---|
| `GET /jenis-sampah/{id}/harga` lists every version newest first, with price, unit, start and author | [`1f43102`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1f43102) | [`50d9392`](https://github.com/bank-sampah-PILAH/pilah-be/commit/50d9392) |
| Each version is marked `terjadwal`, `berlaku`, `sebelumnya` or `digantikan` (a corrected scheduled price) | [`97a6632`](https://github.com/bank-sampah-PILAH/pilah-be/commit/97a6632) | [`601b948`](https://github.com/bank-sampah-PILAH/pilah-be/commit/601b948) |

**Refactor after green:** [`f0b6b0d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0b6b0d) replaces a re-scan with a flag and names the price unit once.

**Pinned, then proven:** [`8bc2be8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8bc2be8) covers three behaviours: another bank's pengurus (404) and a nasabah (403) can't read the history (A01), a jenis with no versions has an empty history, and a backfilled version has no author. They passed when written, because the endpoint reuses the viewset's scoping. So I broke each piece once (an unscoped lookup; dropping `allow_null`) and watched the tests fail before keeping them.

**Coverage:** **100% of the 93 changed lines** ([report](evidence/pilah-be-92-diff-coverage.html)), 469 tests.

## Backend: the jenis filter allow-list, [pilah-be #96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96), stacked on #92

Tristan's review noted that the allow-list was outside PIL-304's scope. [`98456ff`](https://github.com/bank-sampah-PILAH/pilah-be/commit/98456ff) reverts it in #79, and #96 brings the same `[RED]` and `[GREEN]` pair back with `cherry-pick -x`:

- [`44dfafd`](https://github.com/bank-sampah-PILAH/pilah-be/commit/44dfafd) (originally `94267c8`);
- [`2921a37`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2921a37) (originally `cef01bb`).

**Coverage:** **100% of the 28 changed lines** ([report](evidence/pilah-be-96-diff-coverage.html)), 470 tests.

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
| *Review, 12 Oct:* when only the price fails after the fields saved, the sheet says so and stays open | [`5a80375`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5a80375) | [`f1ea8d9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f1ea8d9) |
| *Review, 12 Oct:* an older list reload that answers late can't overwrite a newer one | [`ece524b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ece524b) | [`bd21f70`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bd21f70) |

A widget test caught a real layout bug: at a 360 dp phone width, the scheduled price overflowed the card's trailing price column by 112 px. The line moved to the column that can wrap ([`392ef5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/392ef5d)).

**Coverage:** **100% of changed lines** ([report](evidence/pilah-mobile-62-diff-coverage.html), 13 Oct, after the review fixes), **generated code included**: [`726df68`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/726df68) builds `HargaCubit` through the real DI graph, so the lines #62 adds to the generated `di.config.dart` run too. Before the review round it was 114 lines over 707 tests, with the whole app at 69.5% (CI gate 25%). The first run showed 92%. [`52ec8d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/52ec8d0) covered the rest: the use case, a failed request, `HargaTerjadwal` equality, and two branches of the sheet.

## Mobile: PIL-331, [pilah-mobile #73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73), stacked on #62

| Behaviour | Red | Green |
|---|---|---|
| The repository reads a jenis's versions with unit, start, author and status | [`c1088ee`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c1088ee) | [`7077e55`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7077e55) |
| `RiwayatHargaCubit` loads them, or reports why it couldn't | [`345f853`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/345f853) | [`35e908a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/35e908a) |
| The screen shows each version's price, local start, author and status badge | [`a2a36ba`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a2a36ba) | [`cd41645`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cd41645) |
| A jenis with no versions shows an empty state | [`4c9a443`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4c9a443) | [`328fe5c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/328fe5c) |
| A failed load says why and can be retried | [`4544b2b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4544b2b) | [`6621a7d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6621a7d) |
| Each harga card opens its history, not the edit sheet | [`e376a74`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/e376a74) | [`e4276fd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/e4276fd) |
| `/riwayat-harga` without a jenis (a refreshed web tab) falls back to the list instead of crashing | [`afb0795`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/afb0795) | [`097785a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/097785a) |
| *Review, 12 Oct:* a price with sen (3333.99) is shown exactly, not truncated | [`de18bfc`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/de18bfc) | [`4226ca5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4226ca5) |
| *Review, 12 Oct:* a history longer than one page is read to the end | [`9ad13dd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9ad13dd) | [`510f02a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/510f02a) |

**Refactor after green:** [`2eb1bea`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2eb1bea) shares one date-and-time formatter with the pencairan revision page.

**Caught by tests:**

- **Button overflow:** at 360 dp the new button overflowed the card by 1.3 px. The existing phone-width test caught it, and the icon was dropped.
- **Route crash leaking:** a routing test showed that the route crashed without a jenis, and that the crash leaked into the next test through the shared router. That became its own red/green pair.

**Coverage:** **100% of changed lines** ([report](evidence/pilah-mobile-73-diff-coverage.html)), **generated code included**. With the generator's coverage marker dropped, the two registrations #73 adds to `di.config.dart` first showed as missing (98%). [`eb9b20f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/eb9b20f) builds `RiwayatHargaCubit` through the real graph and covers them.

## Mobile: the generated DI graph, [pilah-mobile #74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74)

SonarCloud showed #62 and #73 a few lines short of 100%. Every missing line was a registration in the generated `di.config.dart`, which the generator marks `coverage:ignore-file`.

Covering it for real turned up a bug: CI-built apps could not build `AuthenticationBloc`, because the generated graph asked dependency injection for a `bool`.

- **The crash:** [`af350f0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/af350f0) `[RED]` reproduced it, and [`320612b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/320612b) `[GREEN]` fixed it. `staging` later got the same fix from Tristan's #71, so #74 now takes `staging`'s version.
- **The whole graph:** [`06ece1b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/06ece1b) adds `di_graph_test`, which builds all 92 registrations in dev and prod. A second test fails if a new registration is missing from its list.
- **Coverage in CI:** [`941f24d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/941f24d) and [`26fcf40`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26fcf40) make CI and SonarCloud measure the file instead of excluding it. Result: **223/223 lines of `di.config.dart` covered.**

## Positive, negative and corner cases

| Behaviour | Positive | Negative | Corner |
|---|---|---|---|
| Price lookup | latest started version wins | none started yet → setoran rejected | two versions starting at the same instant: newest row wins; a scheduled version is invisible before its start |
| Change a price | now; from a future date | backdated; > 365 days ahead; no UTC offset; another bank (404); a nasabah (403); price ≤ 0 (DB check) | `PUT` from an older app with the same price adds no version |
| Migration 0021 | every jenis gets a starting version, sen kept | — | starts from the first setoran if older than the last edit; reverse restores the price *in effect*, ignoring a future one; a re-run adds no duplicates |
| Rounding (#89) | legacy sen dropped on edit | — | sen that re-enters between two pencairan is dropped at each step |
| Mobile save | price now; from a date | unchanged price records nothing; the price POST fails after the PUT saved | picking a date then switching back to Sekarang; a price with no known start date; an older reload answering last |
| Price history (BE) | versions newest first with status | another bank (404); a nasabah (403) | no versions at all; a backfilled version without an author; two versions on the same start (`digantikan`) |
| Price history (mobile) | rows with price, start, author, badge | failed load, retried | empty history; a status the app doesn't know (read as "sebelumnya"); a price with sen; more than 100 versions; a 360 dp phone; the route without a jenis |
| Seed rerun | — | — | a price change made today must not reprice historical setoran |

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
- **Controlled ordering with `Completer`s (mobile, #62).** The race test hands the cubit two pending requests, answers the newer one first and the older one last, and checks the newer price stays.
- **A fake backend at the HTTP boundary (mobile, #73).** `StubApi` replaces Dio's adapter, so the real data source, repository, use case and cubit run against canned responses. Failures are injected at the transport level (`api.fail`).
- **Full-graph resolution (mobile, #74).** `di_graph_test` builds every registration of the generated dependency graph in dev and prod. That is the test that would have caught the startup crash before a build shipped.
