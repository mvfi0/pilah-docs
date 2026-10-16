# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code:

    - SOLID: single responsibility, open/closed and dependency inversion. See [SOLID in this week's code](#solid-in-this-weeks-code).
    - One rule for a price version's status, the same order the setoran lookup uses.
    - Money kept exact on mobile, without `double`.
    - A stale-response guard against a list-reload race.
    - Seed data written through the one approved write path.

    Each item names the design issue it addresses, the pattern or principle used, and its type. The GoF design patterns (Singleton, Adapter, Observer, and loosely Command) have [their own section](#gof-design-patterns-in-this-weeks-code). Three of the issues were in my own code and were found in Tristan's review; the table says which.

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [Version status](#one-rule-for-a-versions-status-601b948-f0b6b0d) | Two readers of the price history (the history screen and the setoran price lookup) that must never disagree; a status that could depend on where a page breaks | **Consistent ordering invariant**: both use the same order (start, then id), and the status is computed over the whole history before pagination | Principle (domain invariant) | Designed in (PIL-331) |
| [Money](#money-kept-exact-4226ca5) | **Primitive obsession with floating point for money**: `3333.99` read through `double` and `toInt()` showed a price that was never stored | **Money in minor units**: the price is an integer number of sen, parsed from the decimal string without a float | Technique (minor units) | Defect in my code, [Tristan's review of #73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4242248044) |
| [Stale response](#a-stale-response-cant-win-bd21f70) | **Race condition on out-of-order async responses**: an older reload answering last overwrote the newer price | **Request sequence token** ("latest request wins"): each reload is numbered and a stale answer is dropped | Technique (concurrency) | Defect in my code, [Tristan's review of #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4242257029) |
| [Seed data](#seed-data-follows-the-same-rules-f67a84f-dc29a68) | **Bypassing the domain's write path**: the seed wrote price versions itself and priced old setoran at today's rate, so its rules could drift from the app's (BR-03) | **Service layer as the single write path**: every price goes through `catat_harga`, and each setoran is priced at its own date | Architectural (PoEAA Service Layer) | Defect in my code, [Tristan's review of #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257376) ([and](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257381)) |
| [Single responsibility](#single-responsibility-601b948) | A **fat view** mixing HTTP with business rules | **SRP**: the rule is a plain port function; the serializer shapes, the view wires | Principle (SOLID) | Designed in (PIL-331) |
| [Open/closed](#single-responsibility-601b948) | Changing PIL-304's working `POST` action to add a read | **OCP**: `@ubah_harga.mapping.get` adds the read without editing the action | Principle (SOLID) | Designed in (PIL-331) |
| [Dependency inversion](#dependency-inversion-35e908a) | A cubit **coupled to the HTTP client**, untestable without a server | **Repository pattern + use case, injected (DIP)**: the cubit sees only the use case and the `HargaRepository` interface | Principle (SOLID) + Architectural (Repository) | Designed in (PIL-331) |
| [Don't repeat yourself](#dont-repeat-yourself-2eb1bea) | **Duplicated code**: my first version copied another page's private date formatter | **Extract function** into one tested shared helper | Principle (DRY) | Caught in my own `[REFACTOR]` commit |

**Type** says what kind of solution each one is. Only part of it is a GoF design pattern (creational, structural, behavioural). The rest are principles (SOLID, DRY), architectural patterns from Fowler's *Patterns of Enterprise Application Architecture* (PoEAA), or plain techniques. The GoF patterns that do appear in this week's code are listed in [GoF design patterns in this week's code](#gof-design-patterns-in-this-weeks-code).

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

**Design issue:** two readers of one history that must agree. **Pattern:** a consistent ordering invariant, computed before pagination. **Origin:** designed in.

### Money kept exact — [`4226ca5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4226ca5)

**Design issue:** primitive obsession with floating point for money. **Pattern:** money in minor units (integer sen). **Origin:** a defect in my code, found in [Tristan's review](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4242248044).

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

**Design issue:** a race condition on out-of-order async responses. **Pattern:** a request sequence token, so the latest request wins. **Origin:** a defect in my code, found in [Tristan's review](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4242257029).

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

**Design issue:** bypassing the domain's write path, so the seed's rules could drift from the app's. **Pattern:** the service layer as the single write path. **Origin:** a defect in my code, found in [Tristan's review](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257376).

The seed command wrote price versions itself and priced historical setoran at today's rate, so rerunning it after a price change rewrote old totals. It now writes through `catat_harga`, the one approved write path in `AGENTS.md`, and prices each setoran at its own date (BR-03).

## GoF design patterns in this week's code

All four are in PIL-331's mobile side ([pilah-mobile #73](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73)), in code I wrote. They follow the app's existing Clean Architecture layout.

| Category | Pattern | Where | What it does here |
|---|---|---|---|
| **Creational** | **Singleton** (container-managed) | `GetRiwayatHargaUseCase` (`@lazySingleton`), [`35e908a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/35e908a) | The injection container builds one shared instance on first use. A variant of GoF Singleton: the container, not the class, guarantees the single instance, so a test can still pass a stub. |
| **Structural** | **Adapter** | `HargaRepositoryImpl.getRiwayatHarga`, [`7077e55`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7077e55) | Adapts the data source, which throws exceptions and reads paginated JSON, to the domain's `HargaRepository` interface, which returns `Either<NetworkException, List<VersiHarga>>`. |
| **Behavioural** | **Observer** | `RiwayatHargaCubit` → `BlocBuilder` on `RiwayatHargaPage`, [`35e908a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/35e908a), [`cd41645`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cd41645) | The cubit emits a new state, and every subscribed widget rebuilds. The cubit doesn't know who is listening. |
| **Behavioural** | **Command** (loosely) | `GetRiwayatHargaUseCase implements UseCase<List<VersiHarga>, String>`, [`35e908a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/35e908a) | Each use case is one request wrapped in an object behind a uniform interface, so the cubit calls it without knowing how the request is carried out. There is no undo or queue, so it is only loosely Command. |

```dart title="lib/features/harga/data/repositories/harga_repository_impl.dart (Adapter)"
  Future<Either<NetworkException, List<VersiHarga>>> getRiwayatHarga(
      String id) async {
    try {
      return Right(await remoteDataSource.getRiwayatHarga(id));
    } on Exception catch (e) {
      return Left(NetworkException.handleException(e));
    }
  }
```

```dart title="lib/features/harga/presentation/pages/riwayat_harga_page.dart (Observer)"
      body: BlocBuilder<RiwayatHargaCubit, RiwayatHargaState>(
```

Two names to avoid mixing up. Python's `@ubah_harga.mapping.get` on the backend is a language decorator, not the GoF **Decorator** pattern. **Repository** and **Service Layer** are PoEAA patterns, not GoF.

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

**Design issue:** duplicated code. **Pattern:** extract function into a shared, tested helper. **Origin:** my own first version, fixed in its `[REFACTOR]` commit.

The history screen first copied the pencairan revision page's private date-and-time formatter. The refactor moved it to one tested `formatTanggalJamId`, and both screens call it.

