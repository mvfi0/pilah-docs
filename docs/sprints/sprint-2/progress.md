# Sprint 2 — Progress

## Status

| Linear | Title | Status | PR | Notes |
|---|---|---|---|---|
| PIL-304 | Versioning dan effective date harga sampah (BE dan UI pengaturan harga) | In review | [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79), [pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) | CI green; 100% of changed lines covered on both. Merge #79 first. Its migrations collide with Pascal's draft-pencairan stack (both add `0020`/`0021`), so the second to merge needs a merge migration. |
| — | Rounding follow-up from the PIL-176 review | In review | [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89) | Gabriel's review answered with a new test and a comment fix. |
| PIL-341 | Pencairan Pengurus di web | Unassigned | — | Taken on 7 Oct, released the same week: it has to wait for the web base (PIL-322, PIL-334, PIL-293) and the draft-pencairan stack. |

## Daily Log

### 2026-10-07

- **Done:**
  - Chose Sprint 2 work from Linear: took PIL-304, the only fit that no teammate's work blocks. PIL-341 was released because it depends on others' web setup.
  - Agreed two design decisions: drop `JenisSampah.harga_per_kg` so prices have one source of truth, and start a scheduled price at 00:00 local time on its date.
  - Built PIL-304 test-first on both sides and opened both PRs:
    - Backend: a `HargaSampah` version table, lookup by transaction time, `POST /jenis-sampah/{id}/harga`, and a backfill migration.
    - Mobile: "Berlaku mulai" (Sekarang or a date), the BR-03 warning, and the scheduled price on the list card.
  - Ran the backend on Postgres 16 locally, with no Docker: all tests passed, and the migration was checked forwards and backwards on a copy of the production database. The copy was dropped afterwards because it holds personal data.
  - Fixed the `pull_request` CI: Pascal's #74 had added tests that still set the dropped column.
- **Next:** Get #79/#62 reviewed; the pending rounding follow-up from #19.
- **Blockers:** none.

### 2026-10-08

- **Done:**
  - Opened [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89): pencairan rounding through `bulatkan_rupiah`, with a new test that pins the edit replay. Replied in the #19 thread that asked for it.
  - Released PIL-341 in Linear (blocked by others' work).
- **Next:** IR documentation for the week; reviews.
- **Blockers:** waiting for reviews on #79, #62 and #89.

### 2026-10-09

- **Done:**
  - Installed and authenticated the SonarQube CLI. Checked all three PRs: one issue on #62 (a nested ternary), fixed test-first.
  - Added an allow-list for the jenis list's filters (OWASP A03) to #79.
  - Reviewed Pascal's [pilah-be #84](https://github.com/bank-sampah-PILAH/pilah-be/pull/84) (PIL-300): a migration collision, an error under the wrong field, and DB-level idempotency.
  - Answered Gabriel's review on #89 with a per-step rounding test.
  - Brought #62's diff coverage from 92% to 100%. Fixed its `pull_request` CI: a new shared test helper on `staging` built the cubit without the new use case.
  - Wrote the IR Part B pages for the week.
- **Next:** Agree the migration merge order of #79 and Pascal's stack with Tristan; respond to reviews.
- **Blockers:** reviews pending on #79, #62 and #89.
