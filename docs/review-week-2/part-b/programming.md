# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code: SOLID (single responsibility, open/closed, interface segregation, dependency inversion; see [SOLID in this week's code](#solid-in-this-weeks-code)), a deep module with a small interface, validation before any write, DRY shared rules, and an explicit fix for an N+1 query.

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

## SOLID in this week's code

### Single Responsibility: one permission class per access rule — [`3c4aac0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c4aac0)

Each permission class answers one question, and the view only picks which one applies to an action. The combined rule reuses the two existing classes instead of repeating their checks.

```python
class IsNasabah(BasePermission):
    message = "Endpoint ini hanya untuk nasabah"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated and request.user.role == User.Role.NASABAH


class IsActivePengelolaOrNasabah(BasePermission):
    message = "Endpoint ini hanya untuk pengelola aktif atau nasabah"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return IsActivePengelola().has_permission(request, view) or IsNasabah().has_permission(
            request, view
        )
```

```python
    def get_permissions(self) -> list[BasePermission]:
        # Recording stays pengurus-only; nasabah may read their own riwayat.
        if self.action in ("list", "retrieve"):
            return [IsActivePengelolaOrNasabah()]
        return [IsActivePengelola()]
```

### Open/Closed: edit history as a new table, `Pencairan` unchanged — [`f0afdef`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0afdef)

PIL-230 needed an audit trail for edits. Instead of adding version columns to `Pencairan`, which every existing reader (list, detail, saldo history, admin) would then have to account for, the history lives in a new append-only model. Existing code keeps working unmodified; only the new `riwayat` endpoint reads it.

```python
class PencairanRevisi(models.Model):
    """A replaced version of a pencairan (PIL-230). Append-only: never edited or deleted."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pencairan = models.ForeignKey(Pencairan, on_delete=models.PROTECT, related_name="revisi")
    versi = models.PositiveIntegerField()
    ...
    # Why this version was replaced, by whom and when.
    alasan = models.CharField(max_length=255)
    diubah_oleh = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="pencairan_revisi_dibuat"
    )
    diubah_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pencairan_revisi"
        ordering = ["pencairan", "versi"]
        constraints = [
            models.UniqueConstraint(fields=["pencairan", "versi"], name="pencairan_revisi_unik"),
        ]
```

### Interface Segregation: an edit contract separate from the create contract — [`f0afdef`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0afdef), [`f9b70d8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f9b70d8)

An edit client should not have to send (or be able to change) the nasabah or bank sampah. `PencairanEditSerializer` exposes only the editable fields, all optional, plus the required `alasan`, while the validation rules are shared with the create serializer rather than copied.

```python
class PencairanEditSerializer(serializers.Serializer[Any]):
    nominal = serializers.DecimalField(max_digits=14, decimal_places=2, required=False)
    metode = serializers.ChoiceField(choices=Pencairan.Metode.choices, required=False)
    tanggal = serializers.DateTimeField(required=False)
    keterangan = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, max_length=255
    )
    alasan = serializers.CharField(required=True, max_length=255, ...)

    def validate_nominal(self, value: Decimal) -> Decimal:
        return _validate_nominal_pencairan(value)

    def validate_tanggal(self, value: datetime) -> datetime:
        return _validate_tanggal_pencairan(value)
```

### Dependency Inversion: the cubit depends on an abstraction — [`1c2b0f2`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/1c2b0f2), [`76aa268`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/76aa268)

On mobile, `EditPencairanCubit` depends on the abstract `PencairanUseCases`, not on the repository or HTTP client. The concrete implementation is supplied by dependency injection (`injectable`), so the test replaces it with a mocktail mock.

```dart
abstract class PencairanUseCases {
  ...
  Future<Either<NetworkException, Pencairan>> editPencairan(
    EditPencairanRequest request,
  );
}
```

```dart
@Injectable()
class EditPencairanCubit extends Cubit<EditPencairanState> {
  final PencairanUseCases _useCases;

  EditPencairanCubit(this._useCases) : super(const EditPencairanState());
```

```dart
class _MockUseCases extends Mock implements PencairanUseCases {}
...
      when(() => useCases.editPencairan(_request))
```

Liskov Substitution is the same boundary seen from the test side: any `PencairanUseCases` implementation, real or mocked, can be passed to the cubit without it behaving differently.
