# Test Driven Development

!!! success "Competency level: 4"
    Level 3 met: PIL-222 and PIL-230 built test-first with phase-tagged commits; 100% coverage of my backend changes and of the whole mobile pencairan feature; positive, negative and corner cases for every behaviour; every finding from two review rounds fixed with its failing test first. Level 4: advanced test isolation in the commits: mocks and stubs of the use-case and network layers, captured requests, `Completer`-controlled races, and stub routes in a real router.

## Backend — [pilah-be #32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32)

| Behaviour | Red | Green |
|---|---|---|
| Riwayat filtered by periode | [`cc27bae`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cc27bae) | [`cd41099`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cd41099) |
| Riwayat searched by nasabah name | [`21f893b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/21f893b) | [`b090224`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b090224) |

Two further test commits are coverage, not red-green pairs, and are labelled `test(...): cover …` rather than "failing test":

- [`b10a5b4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b10a5b4) — custom date range and its 422/400 errors.
- [`8ee88c1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8ee88c1) — another bank's pencairan stays invisible under every filter combination (see [Security](security.md)).

**Diff coverage 100%**, 68 → 72 tests, whole backend 91%.

The period tests compute their expectations from the period definitions (`prev_month <= tanggal < this_month`) instead of hard-coded dates, so they hold on a month boundary and on any weekday — the reviewer checked this explicitly against Monday and Sunday starts.

## Mobile — [pilah-mobile #27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27)

| Behaviour | Red | Green |
|---|---|---|
| Riwayat fetched with periode, nasabah and search params | [`d157f52`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d157f52) | [`b33bb52`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b33bb52) |
| Cubit loads and refilters the riwayat | [`603566c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/603566c) | [`5988f34`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5988f34) |
| Page for the whole bank and for one nasabah | [`dbe5150`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/dbe5150) | [`daf9100`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/daf9100) |
| Entry points on the dashboard and the nasabah sheet | [`27416b0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/27416b0) | [`100df90`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/100df90) |

**Diff coverage 87.5%** (CI gate 25%), 254 → 270 tests.

A widget test again caught a real defect: the detail sheet overflowed by 69 px, because a bottom sheet defaults to half the screen. It now sizes to its content and scrolls.

## Review findings, fixed test-first (23–24 Sep)

Heraldo's review of the three open PRs produced eight findings. Each fix is a failing test commit followed by the fix:

| Finding | Red | Green |
|---|---|---|
| Server nominal error stayed on the field after editing; 422 parsing; metode label (#26) | [`37ecee5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/37ecee5) | [`d1c7ba8`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d1c7ba8) |
| Stale riwayat responses, emit after close, and a 1-character search (#27) | [`8358c87`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8358c87) | [`a6cdfe6`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a6cdfe6) |

The stale-response tests drive the race deliberately with a `Completer`: one request is held open, a second is issued and completed, then the first is released and asserted not to overwrite the newer filter. 270 → 278 tests.

## Against the level-3 criteria

| Level 3 requires | Evidence |
|---|---|
| **100% coverage, without ignoring important files** | Backend: 100% of the lines I changed in [#52](https://github.com/bank-sampah-PILAH/pilah-be/pull/52) (148) and in the #19 review round (34). Mobile: 100% of all of `lib/features/pencairan` (831 lines) after [pilah-mobile #52](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/52); only generated `*.g.dart` serializers are excluded. HTML reports below. |
| **Disciplined red-green-refactor commits** | Every behaviour has a failing-test commit before its implementation; from PIL-230 on, subjects carry `[RED]`/`[GREEN]` ([tables below](#pil-230-backend-pilah-be-52-26-sep)). Tests that pass immediately are labelled `test(...): cover …` instead of pretending to be red. |
| **Positive, negative and corner cases** | See the next table. |

Level 4 adds *"relevant advanced testing methods in the commits, e.g. mock/stub for test isolation"*: see [Test isolation](#test-isolation-mocks-stubs-and-controlled-async) below.

| Behaviour | Positive | Negative | Corner |
|---|---|---|---|
| Edit a pencairan (PIL-230) | metode/keterangan/nominal edited, saldo moves | missing or blank `alasan`; nothing changed; another bank's pencairan (404); a nasabah (403) | a raise today's saldo would cover but that overdraws a **later** pencairan; editing reorders the ledger before a setoran |
| Tanggal limit (PIL-230) | moved back within 7 days | future date; 8 days back | exactly 7 days back is allowed; repeated edits measured from the **original** tanggal cannot creep back |
| Record a pencairan (PIL-176) | saldo lowered once | above saldo; invalid nominal; unapproved or other-bank nasabah | payout dated before the last setoran; legacy saldo with sen rounded down; same-instant setoran ordered first |
| Riwayat (PIL-222) | filter by periode and name | 1-letter search refused | stale response after a newer filter is ignored; month boundary |
| Mobile edit/history flow | saved edit refreshes the list | leaving without saving refreshes nothing; server 422 shown on its field | double tap sends once; history link only for edited pencairan |

!!! info "Diff-coverage reports"
    Line-by-line HTML reports, with how each was measured: [coverage evidence](../../sprints/sprint-1/evidence/PIL-230-coverage.md) ([backend #52](../../sprints/sprint-1/evidence/pil-230-be-diff-coverage.html) · [#19 review round](../../sprints/sprint-1/evidence/pil-176-review2-diff-coverage.html) · [mobile #33 as merged](../../sprints/sprint-1/evidence/pil-230-mobile-diff-coverage.html) · [**whole mobile pencairan feature, 100%**](../../sprints/sprint-1/evidence/pencairan-mobile-coverage.html)).

## PIL-230 backend — [pilah-be #52](https://github.com/bank-sampah-PILAH/pilah-be/pull/52) (26 Sep)

From this issue on, every commit subject names its phase: `test(...): [RED] …`, `feat(...): [GREEN] …`.

| Behaviour | Red | Green |
|---|---|---|
| Edit metode and keterangan, keeping the old version | [`e37bbf4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e37bbf4) | [`c2ef8a4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2ef8a4) |
| `alasan` required | [`815250f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/815250f) | [`11a24e3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/11a24e3) |
| Editing the nominal moves the saldo | [`85f2939`](https://github.com/bank-sampah-PILAH/pilah-be/commit/85f2939) | [`d1b4f51`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d1b4f51) |
| Later pencairan snapshots recomputed after an edit | [`7589ea1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7589ea1) | [`0856114`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0856114) |
| Edited nominal follows the recording rules | [`f8c0664`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f8c0664) | [`f9b70d8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f9b70d8) |
| Tanggal at most 7 days before the **original** tanggal | [`af54839`](https://github.com/bank-sampah-PILAH/pilah-be/commit/af54839) | [`f6a2ed7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f6a2ed7) |
| Revision history endpoint | [`713b61d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/713b61d) | [`f9d6ce0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f9d6ce0) |
| An edit that changes nothing is rejected | [`3461878`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3461878) | [`8feca13`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8feca13) |
| Earliest editable tanggal exposed for the app | [`f10c66d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f10c66d) | [`2e59e67`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2e59e67) |
| Revisions read-only in Django admin | [`2241206`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2241206) | [`2af8c69`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2af8c69) |
| List query count constant in the number of rows | [`0ea7252`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0ea7252) | [`7bceb58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7bceb58) |

Three more test commits are coverage, not red-green pairs, because the replay already handled them when they were written:

- [`120c28b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/120c28b) — an edit that today's saldo would cover but that overdraws a **later** pencairan is rejected.
- [`cb1901b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cb1901b) — moving a tanggal reorders the ledger, before another pencairan and before a setoran.
- [`60e7256`](https://github.com/bank-sampah-PILAH/pilah-be/commit/60e7256) — another bank's pengurus gets 404 and a nasabah 403 on edit and history (see [Security](security.md)).

**Diff coverage 100%**, 72 → 86 tests. The tests sit in their own file, `api/test_pencairan_edit.py`, to keep out of the append conflicts other PRs have in `api/tests.py`.

The query-count test ([`0ea7252`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0ea7252)) was written after noticing that `diperbarui` ran one query per row: it failed at 12 queries against 6, and the annotation fix brought both to 6.

## PIL-230 mobile — [pilah-mobile #33](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/33) (26 Sep)

| Behaviour | Red | Green |
|---|---|---|
| `diperbarui` and the edit limit mapped from the API | [`5509100`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5509100) | [`cbf6ac3`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cbf6ac3) |
| Edit sent as `PATCH` with every field and the alasan | [`f04bb89`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f04bb89) | [`6b49b25`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6b49b25) |
| Revision history parsed | [`c196e8f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c196e8f) | [`3767af1`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3767af1) |
| Edit cubit: success, field errors, other errors, double tap | [`76aa268`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/76aa268) | [`eb85f22`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/eb85f22) |
| Edit form: prefill, limit text, gating, confirm, result | [`288a78f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/288a78f) | [`c54a953`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c54a953) |
| Change history page | [`d500d13`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d500d13) | [`9f472de`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9f472de) |
| Riwayat entry points and reload after a save | [`3bfe914`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3bfe914) | [`46b272c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/46b272c) |

**Diff coverage 82.8%** (CI gate 25%), 278 → 294 tests, whole app 37.8%.

The entry-point tests pump a real `GoRouter` with stub edit and history routes, so they check what the sheet actually pushes (`extra` is the pencairan, or its id) and that the riwayat reloads only when the form pops `true`.

## Tristan's review of #19, fixed test-first (26 Sep)

| Finding | Red | Green |
|---|---|---|
| Django admin could write pencairan past the service | [`7377817`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7377817) | [`9f4a428`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9f4a428) |
| Saldo history kept the sen the pencairan rounding dropped | [`03061f4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/03061f4) | [`fd91ee8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fd91ee8) |
| A backdated payout could be funded by a later setoran | [`a314b09`](https://github.com/bank-sampah-PILAH/pilah-be/commit/a314b09) | [`290bb1d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/290bb1d) |
| Nasabah could not read their own pencairan | [`f7327fc`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f7327fc) | [`3c4aac0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c4aac0) |

Plus a coverage test that a nasabah still cannot record a pencairan once list and detail accept them ([`8287130`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8287130)). Every line the four fixes added is covered; the only uncovered lines in #19's diff come from the `staging` merge.

Each red test failed for the reason in the finding before its fix: the admin allowed `add`, history said Rp 7.001 against a stored Rp 7.000,50, a payout dated before the only setoran was accepted (201), and a nasabah got 403.

## Closing the mobile gap — [pilah-mobile #52](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/52) (28 Sep)

Mobile #27 and #33 were merged at 87.5% and 82.8%. A test-only PR brings the whole pencairan feature to 100%: [`54c6877`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/54c6877) (detail sheet edit and history links), [`348d7f2`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/348d7f2) (history refresh), [`b619aba`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b619aba) (empty-nasabah submit, back arrow). 652 → 659 tests.

## Test isolation: mocks, stubs and controlled async

The mobile tests isolate each layer from the one below it, so a failure points at one unit. 49 uses of mocks, stubs and `Completer`s across 8 pencairan test files this week:

| Technique | What it isolates | Commit |
|---|---|---|
| Mock of the use-case layer (`_MockUseCases extends Mock implements PencairanUseCases`), `when(...)` stubs, `verify(...).called(1)` | the edit cubit from the repository and network | [`76aa268`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/76aa268) |
| Mocked `NetworkService` | the repository from HTTP, capturing the exact PATCH body sent | [`f04bb89`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f04bb89), [`c196e8f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c196e8f) |
| Stubbed use cases behind real widgets, `captureAny()` | the edit form and history page from the data layer, checking the request the form builds | [`288a78f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/288a78f), [`d500d13`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d500d13) |
| `Completer`-controlled async | races: a double tap sends one edit; a slow older riwayat response cannot overwrite a newer filter | [`76aa268`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/76aa268), [`8358c87`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8358c87) |
| Stub routes in a real `GoRouter` | navigation from the real pages: what the sheet pushes (`extra`), and reloading only after a real save | [`3bfe914`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3bfe914), [`54c6877`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/54c6877) |

The backend tests deliberately do not mock: they run the API against a real test database, because the behaviour under test (row locks, the ledger replay, query counts) only exists in the database.

## Test validation

One of these tests was checked to prove it fails for the right reason, not merely passes. The first version of the short-search test used `verify` twice; because mocktail's `verify` consumes recorded calls, the second call found none and failed even though the code was already correct. Rewritten to consume the initial load and then assert `verifyNever`, it fails on the unfixed code and passes on the fix.
