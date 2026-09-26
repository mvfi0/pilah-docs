# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code: a deep module with a small interface, validation before any write, DRY shared rules, and an explicit fix for an N+1 query.

## 26 Sep — PIL-230, editing a pencairan

### The problem the design had to solve

Editing an old pencairan's nominal or tanggal changes the saldo *at every later point*, so every later pencairan's `saldo_sebelum`/`saldo_sesudah` receipt goes stale. The PO decided those must be recomputed. Two constraints shaped the solution:

- **Saldo cannot be replayed from zero.** PILAH 1.0 opening balances were imported into `Saldo` with no transaksi behind them, so a sum of the ledger does not equal the stored saldo.
- **"Enough saldo" must hold at every later point, not only today.** An edit that today's saldo covers can still overdraw a pencairan that happened between the edited one and now.

### Deep module: one entry point, the replay hidden behind it — [`0856114`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0856114)

The view calls one method, `PencairanService.edit_pencairan(user, pencairan, payload)`. The replay lives in a private helper:

```python title="api/services.py — PencairanService._hitung_ulang_saldo (excerpt)"
        # PILAH 1.0 opening balances have no transaksi behind them, so the replay starts
        # from a stored snapshot: the first pencairan at or after `mulai`, minus the
        # setoran ordered before it (a setoran at the same instant comes first).
        pertama = min([pencairan, *lainnya], key=lambda cair: (cair.tanggal, str(cair.pk)))
        awal = pertama.saldo_sebelum - sum(
            (nilai for _, waktu, nilai in setoran if waktu <= pertama.tanggal), Decimal(0)
        )
        ...
        akhir_lama, _ = putar(pencairan.nominal, pencairan.tanggal)
        akhir_baru, snapshot = putar(nominal, tanggal)
        ...
        saldo.total_saldo += akhir_baru - akhir_lama
```

Three decisions are in these lines:

1. **Anchor on a stored snapshot**, not on zero. The replay starts at the earliest moment the edit affects (`mulai`, the earlier of the old and new tanggal), from a `saldo_sebelum` that was exact when recorded.
2. **Replay twice, apply the difference.** `putar` runs once with the old values and once with the new ones. `Saldo` moves by `akhir_baru - akhir_lama` instead of being overwritten, so any offset the replay cannot explain (for example a legacy balance) is kept rather than silently destroyed.
3. **One ordering rule.** Events sort by `(tanggal, setoran before pencairan, id)`, the same rule the saldo history and the Excel export already use, so the recomputed receipts agree with the history screen. Each pencairan re-applies the same round-down to whole rupiah as recording does.

The overdraw rule falls out of the replay: `nilai > saldo_berjalan` is checked at every pencairan, so a later one that would be paid from too little saldo rejects the edit. The coverage test [`120c28b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/120c28b) builds exactly that case: Rp 115.600 today would cover +Rp 20.000, but the next pencairan would then be paid Rp 250.000 from Rp 245.600.

### Validate first, then write — [`8feca13`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8feca13)

The first version stored the revision and then validated the tanggal. It was correct (the transaction rolls back), but the order read wrong and made "nothing changed" impossible to reject cleanly. The service now works out the new values, rejects an empty change and an out-of-range tanggal, and only then writes the revision and the recompute, all in one `transaction.atomic` with the rows locked.

### DRY: one rule set for recording and editing — [`f9b70d8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f9b70d8), [`f6a2ed7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f6a2ed7)

The nominal rules (positive, whole rupiah) and the tanggal rule (not in the future) were methods on the create serializer. The edit serializer needed the same, so both became module functions that both serializers call, instead of copies that could drift. The 7-day limit is one constant, `BATAS_MUNDUR_TANGGAL_PENCAIRAN_HARI`, which the service, the error message and the tests all read, and the app gets the resulting date from the API (`tanggal_edit_minimum`) rather than hard-coding 7.

### N+1 found and fixed — [`0ea7252`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0ea7252) → [`7bceb58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7bceb58)

`diperbarui` and `tanggal_edit_minimum` each ran a query per row, so a page of 100 pencairan meant 200 extra queries. The list queryset now annotates both with `Exists` and a `Subquery`, and the serializer falls back to a query only for an instance that did not come from that queryset (the one an edit returns). A test pins the query count so it cannot silently grow back.

## 26 Sep — review fixes on PIL-176

### Named permission class instead of operator composition — [`3c4aac0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c4aac0)

Letting nasabah read their own pencairan needed "active pengurus **or** nasabah" on two actions. DRF's `IsActivePengelola | IsNasabah` works at runtime, but under `mypy --strict` its result is a private protocol type that `get_permissions` cannot be annotated with. A small named class, `IsActivePengelolaOrNasabah`, keeps the types honest, reads better at the call site, and is reused by PIL-230.

### Fixing the root cause, not the symptom — [`fd91ee8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fd91ee8)

Saldo history disagreed with the stored saldo after a pencairan dropped sen. Patching the displayed number would have hidden it. The cause was that history debited only `nominal`, while the saldo actually lost `nominal` plus the dropped sen. Both history paths now debit `saldo_sebelum - saldo_sesudah`, the amount that really left, which needed no new column.
