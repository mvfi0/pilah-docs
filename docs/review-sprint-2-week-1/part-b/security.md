# Security

!!! success "Competency level: 1"
    One OWASP Top 10 (2021) category guarded in this week's new code, named in its commit and tested: **A01 Broken Access Control** on the new price-history endpoint. The week also has tests for two more categories (A08, A09), but their commits don't name OWASP, so they aren't counted toward the five that level 2 needs.

    The A03 allow-list moved into [#96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96) this week, but its commits are the ones claimed in [Sprint 1 Week 3](../../review-week-3/part-b/security.md), so it isn't counted again.

| OWASP category | Guard | Commit | Named in the commit |
|---|---|---|---|
| **A01 Broken Access Control** | Only the owning bank's pengurus can read a jenis's price history | [`8bc2be8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8bc2be8) | yes |
| A08 Software and Data Integrity Failures | Rerunning the seed no longer rewrites historical setoran snapshots | [`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) → [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f) | no |
| A09 Security Logging and Monitoring Failures | The price history shows who recorded each version | [`1f43102`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1f43102) → [`50d9392`](https://github.com/bank-sampah-PILAH/pilah-be/commit/50d9392) | no |

## A01 · Broken Access Control

PIL-331's `GET /jenis-sampah/{id}/harga` exposes every past price of a jenis. A bank's prices are business data, so I checked the endpoint against the two ways it could leak: another bank's pengurus, and a nasabah.

```python title="apps/waste_catalog/test_riwayat_harga.py (excerpt)"
        self.auth_as(pengurus_lain)
        self.assertEqual(self.riwayat(jenis["id"]).status_code, 404)
        self.auth_as(nasabah)
        self.assertEqual(self.riwayat(jenis["id"]).status_code, 403)
```

- **Why it passes:** the action reuses the viewset's bank-scoped `get_object` and `IsActivePengelola`, so the test passed when written.
- **Proof it guards something:** I swapped in an unscoped lookup, saw another bank read the prices and the test fail, then restored the code. The commit message names the category: "(OWASP A01, BR-01)".

## Also tested this week, not counted

- **A08, data integrity.** Each seeded setoran must keep the price of its own date (BR-03). The red test recorded a price change taking effect now and reran the seed. A historical snapshot went from 3,500 to 99,999. The fix prices each setoran at its stored `tanggal`.
- **A09, audit trail.** Versions already stored `dibuat_oleh`. PIL-331 makes that trail readable to the pengurus: each row carries its author, `null` for prices backfilled by the migration.

To reach level 2 next week, new guards need to name their category in the commit message, as the rubric asks.
