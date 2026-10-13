# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code:

    - SOLID: single responsibility, open/closed, interface segregation and dependency inversion. See [SOLID in this week's code](#solid-in-this-weeks-code).
    - One source of truth for prices, in an append-only design that mirrors the SDS.
    - An N+1 query removed before it shipped.
    - For PIL-331: one rule for a version's status, money kept exact without `double`, and a stale-response guard against a reload race.

## PIL-304 — versioned prices with an effective date

### The problem the design had to solve

A jenis sampah had one `harga_per_kg` column. Changing it changed the price at once, and nothing recorded the old price, who changed it, or when. The client wanted pengurus to schedule a price change (for example, from the 15th). The SDS (7.1.2) already described the target: prices kept as a history with their validity, and each transaksi keeping its own copy of the price it used (BR-03).

### One source of truth — [`ad352fb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ad352fb)

Prices now live only in `HargaSampah`, one row per version. The old column was **dropped**, not kept beside it. Kept, it would go stale the moment a scheduled price started, because nothing runs at midnight to update it. Migration 0021 moves every price into a starting version first, and its reverse rebuilds the column from the price in effect. I tested both directions on a copy of the production database.

Rows are never updated. A correction to a scheduled price is a new row, and the lookup breaks ties by the newest row:

```python title="apps/waste_catalog/api.py"
def versi_berlaku(jenis: JenisSampah, pada: datetime) -> HargaSampah | None:
    """Versi harga ``jenis`` yang berlaku pada waktu ``pada``."""
    return (
        HargaSampah.objects.filter(jenis_sampah=jenis, berlaku_mulai__lte=pada)
        .order_by("-berlaku_mulai", "-id")
        .first()
    )
```

### N+1 removed before it shipped — [`6c0ba69`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6c0ba69)

The app loads up to 100 jenis per page. Reporting the current and the next scheduled price per jenis cost two queries each, and a test caught it (14 queries against 6). The list now prefetches every jenis's history, and one pure function picks both versions in memory, with the same tie-break as the database lookup:

```python title="apps/waste_catalog/api.py"
def ringkas_harga(
    riwayat: Iterable[HargaSampah], pada: datetime
) -> tuple[HargaSampah | None, HargaSampah | None]:
    berlaku: HargaSampah | None = None
    terjadwal: HargaSampah | None = None
    for versi in riwayat:
        if versi.berlaku_mulai <= pada:
            if berlaku is None or (versi.berlaku_mulai, versi.id) > (
                berlaku.berlaku_mulai,
                berlaku.id,
            ):
                berlaku = versi
        elif terjadwal is None or (versi.berlaku_mulai, -versi.id) < (
            terjadwal.berlaku_mulai,
            -terjadwal.id,
        ):
            terjadwal = versi
    return berlaku, terjadwal
```

Two implementations of one rule can drift apart, so [`194c3d6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/194c3d6) tests that both pick the same versions, ties included.

### Backward compatibility as a design input

Staging deploys the backend as soon as it merges, but testers keep the old app for a while, and that build sends `harga_per_kg` on every edit. Rejecting it with 422 would have broken editing for them. Instead, `PUT` with a changed price records a version that starts now, through the same `catat_harga` path, so it is still audited ([`ead26b9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ead26b9)). The new app sends price changes to the new endpoint.

## PIL-331 — the price history, and the review round

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

### Single responsibility — [`ee9668d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ee9668d)

`shared_kernel/kalkulasi.py` used to both do rupiah arithmetic and decide which price applies. Choosing a price needs the catalog's tables, so it moved behind the catalog's public port. `kalkulasi` now does arithmetic only:

```python title="shared_kernel/kalkulasi.py"
def hitung_subtotal(harga: Decimal, berat: Decimal) -> Decimal:
    """Nilai satu item setoran, dibulatkan ke bawah ke rupiah penuh."""
    return bulatkan_rupiah(harga * berat)
```

In [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89), the pencairan code stopped rounding inline and calls the same helper, so the rupiah rule exists in exactly one place.

### Open/closed — [`7729d3d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7729d3d)

On mobile, changing a price is a **new** use case, not an extra branch in `UpdateHargaUseCase`. Editing a jenis and changing its price follow different rules (a price change can be scheduled and is never sent with `PUT`), and the existing use case did not change:

```dart title="lib/features/harga/domain/use_cases/ubah_harga_usecase.dart"
@lazySingleton
class UbahHargaUseCase implements UseCase<void, UbahHarga> {
  final HargaRepository repository;

  UbahHargaUseCase(this.repository);

  @override
  Future<Either<NetworkException, void>> execute([UbahHarga? args]) {
    return repository.ubahHarga(args!);
  }
}
```

### Interface segregation — [`c53f1a7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c53f1a7), [`cef01bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cef01bb)

Each request has its own narrow input contract instead of growing the jenis serializer. The price-change endpoint accepts exactly a price and an optional start time, and the list's filters have their own allow-list:

```python title="apps/waste_catalog/serializers.py"
class HargaBaruSerializer(serializers.Serializer[Any]):
    harga_per_kg = serializers.DecimalField(max_digits=11, decimal_places=2)
    berlaku_mulai = WaktuBerzonaField(required=False)


class FilterJenisSampahSerializer(serializers.Serializer[Any]):
    status = serializers.ChoiceField(choices=["aktif", "tidak_aktif", "semua"], default="aktif")
    kategori = serializers.ChoiceField(choices=JenisSampah.Kategori.choices, required=False)
```

### Dependency inversion — [`d111495`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d111495)

The ledger context does not reach into the catalog's models to find a price. It depends on the catalog's public port, which `tests/test_architecture.py` enforces:

```python title="apps/ledger/services.py"
from apps.waste_catalog.api import get_active_jenis, harga_berlaku
...
            harga = harga_berlaku(jenis, transaksi.tanggal)
            if harga is None:
                raise serializers.ValidationError(
                    {f"items[{index}].jenis_sampah_id": ["Harga jenis sampah belum diatur"]}
                )
```

How prices are stored (versions, ties, prefetching) can change without touching setoran.

### Single responsibility, PIL-331 — [`601b948`](https://github.com/bank-sampah-PILAH/pilah-be/commit/601b948)

The status rule is a plain function in the catalog's port (above), with no HTTP in it. The serializer only shapes a row, and the view only wires the lookup to pagination:

```python title="apps/waste_catalog/views.py"
    @ubah_harga.mapping.get
    def riwayat_harga(self, request: Request, pk: str | None = None) -> Response:
        page = self.paginate_queryset(susun_riwayat_harga(self.get_object(), timezone.now()))
        return self.get_paginated_response(VersiHargaSerializer(page, many=True).data)
```

`@ubah_harga.mapping.get` adds the read on the same path as PIL-304's `POST`, without changing that action: **open/closed**.

### Dependency inversion, PIL-331 mobile — [`35e908a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/35e908a)

`RiwayatHargaCubit` knows only the use case, which knows only the `HargaRepository` interface. Tests swap the whole HTTP layer for a stub (`StubApi`) without touching the cubit:

```dart title="lib/features/harga/presentation/cubit/riwayat_harga_cubit.dart"
@injectable
class RiwayatHargaCubit extends Cubit<RiwayatHargaState> {
  final GetRiwayatHargaUseCase _getRiwayat;

  RiwayatHargaCubit(this._getRiwayat) : super(const RiwayatHargaState());
```

### Don't repeat yourself — [`2eb1bea`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2eb1bea)

The history screen first copied the pencairan revision page's private date-and-time formatter. The refactor moved it to one tested `formatTanggalJamId`, and both screens call it.

