# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code: SOLID (single responsibility, open/closed, interface segregation, dependency inversion; see [SOLID in this week's code](#solid-in-this-weeks-code)), one source of truth for prices, an append-only design that mirrors the SDS, and an N+1 query removed before it shipped.

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
