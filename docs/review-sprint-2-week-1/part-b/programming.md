# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code:

    - SOLID: single responsibility, open/closed and dependency inversion. See [SOLID in this week's code](#solid-in-this-weeks-code).
    - One rule for a price version's status, the same order the setoran lookup uses.
    - Money kept exact on mobile, without `double`.
    - A stale-response guard against a list-reload race.
    - Seed data written through the one approved write path.

## PIL-331 — the price history, and the review round (10–12 Oct)

### One rule for a version's status — [`601b948`](https://github.com/bank-sampah-PILAH/pilah-be/commit/601b948), [`f0b6b0d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0b6b0d)

The history marks each version `terjadwal`, `berlaku`, `sebelumnya` or `digantikan`. The rule uses the same order as `harga_berlaku` (start, then id), so the screen can never disagree with the price a setoran uses. It runs over the whole history before pagination, so a page break can't change a status:

```python title="apps/waste_catalog/api.py"
def susun_riwayat_harga(jenis: JenisSampah, pada: datetime) -> list[VersiHarga]:
    riwayat: list[VersiHarga] = []
    di_atasnya: HargaSampah | None = None
    sudah_ada_yang_berlaku = False
    for versi in jenis.riwayat_harga.select_related("dibuat_oleh").order_by(
        "-berlaku_mulai", "-id"
    ):
        status: StatusVersi
        if di_atasnya is not None and versi.berlaku_mulai == di_atasnya.berlaku_mulai:
            status = "digantikan"
        elif versi.berlaku_mulai > pada:
            status = "terjadwal"
        elif not sudah_ada_yang_berlaku:
            status = "berlaku"
            sudah_ada_yang_berlaku = True
        else:
            status = "sebelumnya"
        riwayat.append(VersiHarga(versi, status))
        di_atasnya = versi
    return riwayat
```

`digantikan` exists because correcting a scheduled price is a new version with the same start (PIL-304's append-only rule). Without it, the history would show two scheduled prices for one day.

### Money kept exact — [`4226ca5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4226ca5)

Tristan's review found that the mobile model read `3333.99` through `double` and `toInt()`, showing a price that was never stored. A version now holds its price in sen, and the backend's decimal string is cut, not parsed as a float, so no binary rounding can creep in:

```dart title="lib/features/harga/data/models/versi_harga_model.dart"
int _keSen(String angka) {
  final bagian = angka.split('.');
  final sen = (bagian.length > 1 ? bagian[1] : '').padRight(2, '0');
  return (int.tryParse(bagian[0]) ?? 0) * 100 +
      (int.tryParse(sen.substring(0, 2)) ?? 0);
}
```

### A stale response can't win — [`bd21f70`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bd21f70)

Saving a price change reloads the list twice: after the `PUT` and after the price `POST`. If the first `GET` answered last, the old price came back. Each reload is now numbered, and an answer is dropped once a newer reload has started:

```dart title="lib/features/harga/presentation/cubit/harga_cubit.dart"
  Future<void> loadHarga({bool silent = false}) async {
    final permintaan = ++_permintaanTerakhir;
    if (!silent || state is! HargaLoaded) emit(HargaLoading());
    final result = await getHargaUseCase.execute();
    // Reload yang lebih baru sudah berjalan: jawaban ini sudah usang.
    if (permintaan != _permintaanTerakhir) return;
    ...
```

### Seed data follows the same rules — [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f), [`dc29a68`](https://github.com/bank-sampah-PILAH/pilah-be/commit/dc29a68)

The seed command wrote price versions itself and priced historical setoran at today's rate, so rerunning it after a price change rewrote old totals. It now writes through `catat_harga`, the one approved write path in `AGENTS.md`, and prices each setoran at its own date (BR-03).

## SOLID in this week's code

### Single responsibility — [`601b948`](https://github.com/bank-sampah-PILAH/pilah-be/commit/601b948)

The status rule is a plain function in the catalog's port (above), with no HTTP in it. The serializer only shapes a row, and the view only wires the lookup to pagination:

```python title="apps/waste_catalog/views.py"
    @ubah_harga.mapping.get
    def riwayat_harga(self, request: Request, pk: str | None = None) -> Response:
        page = self.paginate_queryset(susun_riwayat_harga(self.get_object(), timezone.now()))
        return self.get_paginated_response(VersiHargaSerializer(page, many=True).data)
```

`@ubah_harga.mapping.get` adds the read on the same path as PIL-304's `POST`, without changing that action: **open/closed**.

### Dependency inversion — [`35e908a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/35e908a)

`RiwayatHargaCubit` knows only the use case, which knows only the `HargaRepository` interface. Tests swap the whole HTTP layer for a stub (`StubApi`) without touching the cubit:

```dart title="lib/features/harga/presentation/cubit/riwayat_harga_cubit.dart"
@injectable
class RiwayatHargaCubit extends Cubit<RiwayatHargaState> {
  final GetRiwayatHargaUseCase _getRiwayat;

  RiwayatHargaCubit(this._getRiwayat) : super(const RiwayatHargaState());
```

### Don't repeat yourself — [`2eb1bea`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2eb1bea)

The history screen first copied the pencairan revision page's private date-and-time formatter. The refactor moved it to one tested `formatTanggalJamId`, and both screens call it.

