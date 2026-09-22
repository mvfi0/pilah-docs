# Sprint 1 Plan — PIL-222 View Riwayat Pencairan untuk Pengurus

| Item | Detail |
|---|---|
| Owner | Vegard |
| Linear | [PIL-222](https://linear.app/pilah-2/issue/PIL-222) (parent: [PIL-140 CPBI-10](https://linear.app/pilah-2/issue/PIL-140)) |
| Branch | `feature/pil-222` in both repos (new `feature/<issue-id>` convention) |
| Base | Stacked on PIL-176: `feature/pil-176-pencatatan-pencairan-untuk-pengurus` in each repo, since [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) and [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) are not merged yet. Retarget to `staging` once they merge. |
| Status | Planned 22 Sep 2026 |

## Goal

A pengurus can look back at pencairan that were recorded: across the whole bank for a period, and for one nasabah. Each entry shows **nominal, tanggal, metode, status, and keterangan** (PO answer, 19 Sep).

CPBI-10 is only done once pencatatan, saldo update, **and riwayat** work, so this closes the loop PIL-176 opened.

The Linear issue has no description; this scope was agreed on 22 Sep.

## Scope

| In scope | Out of scope |
|---|---|
| Bank-wide riwayat screen with period filter and nasabah search | Editing a pencairan (PIL-230) |
| Per-nasabah riwayat, opened from the nasabah detail sheet | Nasabah-side view (needs the nasabah app) |
| Backend: `periode` and `search` filters on the list endpoint | Pencairan rows in the Excel export |

## API contract

Extends `GET /api/v1/pencairan` from #19. The response shape is unchanged: paginated `{count, next, previous, results}`, each result being the existing pencairan detail (`id`, `nasabah_id`, `nasabah_nama`, `dicatat_oleh_nama`, `tanggal`, `nominal`, `metode`, `keterangan`, `status`, `saldo_sebelum`, `saldo_sesudah`, `created_at`), newest first.

| Query parameter | Values | Behaviour |
|---|---|---|
| `periode` | `hari_ini`, `minggu_ini`, `bulan_ini`, `bulan_lalu`, `custom` | Same vocabulary as the transaksi list. **When omitted, no date filter (all time)** — unlike transaksi, which defaults to `hari_ini` — so #19's behaviour and the per-nasabah history are unchanged. |
| `dari_tanggal`, `sampai_tanggal` | `YYYY-MM-DD` | Required with `periode=custom`; missing → 422, end before start → 400, matching transaksi. |
| `nasabah_id` | UUID | Existing filter from #19. |
| `search` | text, 2+ characters | Nasabah name contains, case-insensitive, matching transaksi. |

Scoping is unchanged: only the pengurus' own bank, `IsActivePengelola`.

## Backend (`pilah-be`)

- Reuse the transaksi period logic for pencairan rather than copying it: generalise `TransactionFilterService.apply_period` so it can filter any queryset by `tanggal`, with the default period as a parameter (transaksi keeps `hari_ini`; pencairan passes none).
- Tests first: each period value, custom range errors, search, all-time default, combined with `nasabah_id`, bank scoping still holding.

## Mobile (`pilah-mobile`)

- **`RiwayatPencairanPage`**, one page serving both views:
    - Bank-wide: period chips (reuse `TimeFilterChips`) and search; entries grouped by day.
    - Per-nasabah: opened with a nasabah, filtered to them, all time.
- Each entry: nasabah name, nominal, metode, tanggal and time, status, keterangan. Tapping shows the full record, including saldo sebelum/sesudah and who recorded it.
- Entry points: a **Riwayat Pencairan** action on the dashboard (bank-wide) and on the nasabah detail sheet next to **Catat Pencairan** (per-nasabah).
- Built on the pencairan feature from #26: extend its data layer, use cases and a new list cubit.
- Tests first: cubit (load, filter change, search, empty, error, pagination), widget (grouping, entry content, both entry points).

## Order

1. Backend first: it defines the filters the mobile app sends.
2. Mobile second, stacked on #26.
3. One PR per repo, both targeting their PIL-176 branch until PIL-176 merges.
