# Test Driven Development

!!! success "Competency level: 3"
    PIL-222 built test-first in both repositories, 100% diff coverage on the backend and 87.5% on mobile, and every review finding fixed with its failing test first.

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

## Test validation

One of these tests was checked to prove it fails for the right reason, not merely passes. The first version of the short-search test used `verify` twice; because mocktail's `verify` consumes recorded calls, the second call found none and failed even though the code was already correct. Rewritten to consume the initial load and then assert `verifyNever`, it fails on the unfixed code and passes on the fix.
