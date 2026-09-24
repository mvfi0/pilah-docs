# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in that week's code: single responsibility, a service layer, and extension without modifying existing consumers.

## 15–21 Sep

### Single Responsibility + DRY: `BalanceService` — [`5447710`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5447710)

Two places computed a running saldo by summing setoran only: `TransactionDetailSerializer.get_saldo_setelah_transaksi` and the Excel export. Instead of fixing the formula twice, the rule "setoran added, pencairan subtracted" lives in one class, used by both.

```python title="api/services.py"
class BalanceService:
    """Running saldo for a nasabah: setoran added, pencairan subtracted."""

    @staticmethod
    def saldo_at(
        bank_sampah: BankSampah, nasabah_id: UUID, until: datetime, until_id: UUID
    ) -> Decimal:
        setoran = Transaksi.objects.filter(bank_sampah=bank_sampah, nasabah_id=nasabah_id).filter(
            Q(tanggal__lt=until) | Q(tanggal=until, id__lte=until_id)
        )
        # At an equal tanggal a pencairan is ordered after the setoran, so it is
        # excluded here; the export's merge below applies the same rule.
        pencairan = Pencairan.objects.filter(
            bank_sampah=bank_sampah, nasabah_id=nasabah_id, tanggal__lt=until
        )
        masuk = setoran.aggregate(total=Coalesce(Sum("total_nilai"), Decimal("0.00")))["total"]
        keluar = pencairan.aggregate(total=Coalesce(Sum("nominal"), Decimal("0.00")))["total"]
        return cast(Decimal, masuk - keluar)
```

The serializer is then one line, and the export applies the same ordering rule in its own running-total pass:

```python title="api/serializers.py"
return BalanceService.saldo_at(obj.bank_sampah, obj.nasabah_id, obj.tanggal, obj.id)
```

The payoff came with review finding 3: the tie-break at an equal `tanggal` was wrong, and fixing it meant changing one rule in one place ([`765f90f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/765f90f)) instead of hunting for every place a saldo was summed.

### Service layer: `PencairanService` — [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b)

The business rule (lock the nasabah and saldo rows, check the saldo, record, deduct) sits in `PencairanService.create_pencairan`, not in the view. The whole operation is one atomic transaction, so a failure anywhere leaves neither a record nor a changed saldo.

```python title="api/services.py"
class PencairanService:
    @staticmethod
    @transaction.atomic
    def create_pencairan(user: User, payload: Mapping[str, Any]) -> Pencairan:
        bank = user.bank_sampah
        assert bank is not None  # ponytail: views gate on IsActivePengelola
        nasabah = (
            Nasabah.objects.select_for_update()
            .filter(
                id=payload["nasabah_id"],
                bank_sampah=bank,
                is_active=True,
                status=Nasabah.Status.APPROVED,
            )
            .first()
        )
        if not nasabah:
            raise serializers.ValidationError(
                {"nasabah_id": ["Nasabah tidak ditemukan atau tidak aktif"]}
            )

        saldo, _ = Saldo.objects.select_for_update().get_or_create(nasabah=nasabah)
        nominal = payload["nominal"]
        saldo_sebelum = saldo.total_saldo
        if nominal > saldo_sebelum:
            raise serializers.ValidationError({"nominal": ["Saldo nasabah tidak mencukupi"]})
        ...
```

The view stays thin: validate, delegate, respond. It holds no business rule at all, following the existing `TransactionService.create_setoran` pattern.

```python title="api/views.py"
    def create(self, request: Request) -> Response:
        serializer = PencairanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pencairan = PencairanService.create_pencairan(_user(request), serializer.validated_data)
        return Response(PencairanDetailSerializer(pencairan).data, status=status.HTTP_201_CREATED)
```

Because the saldo check happens *inside* the locked transaction, two simultaneous payouts cannot both pass it — the second waits for the row lock and then sees the reduced saldo.

### Open/Closed in practice: a separate `Pencairan` model — [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b)

Adding a `PENCAIRAN` type to `Transaksi` with a negative value would have forced changes in every consumer that assumes a transaksi has items: the list serializer, export, dashboard and WhatsApp notifier. A new model extends the system without modifying them.

```python title="api/models.py"
class Pencairan(TimestampedModel):
    class Metode(models.TextChoices):
        TUNAI = "tunai", "Tunai"
        TRANSFER = "transfer", "Transfer"

    nasabah = models.ForeignKey(Nasabah, on_delete=models.PROTECT, related_name="pencairan")
    bank_sampah = models.ForeignKey(BankSampah, on_delete=models.PROTECT, related_name="pencairan")
    dicatat_oleh = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="pencairan_dicatat"
    )
    nominal = models.DecimalField(max_digits=14, decimal_places=2)
    metode = models.CharField(max_length=20, choices=Metode.choices)
    # Receipt snapshots at record time; PIL-230 decides how edits affect them.
    saldo_sebelum = models.DecimalField(max_digits=14, decimal_places=2)
    saldo_sesudah = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = "pencairan"
        ordering = ["-tanggal"]
        indexes = [models.Index(fields=["bank_sampah", "nasabah", "tanggal"])]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nominal__gt=0), name="pencairan_nominal_positive"
            ),
        ]
```

`PROTECT` on all three foreign keys keeps a money record from losing the nasabah, bank or pengurus it refers to, and the check constraint enforces a positive nominal in the database as well as in the serializer. The trade-off is documented in the [PR description](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) and the [task plan](../../sprints/sprint-1/tasks/PIL-176-pencatatan-pencairan-plan.md).

### Consistency with existing rules — [`49cd153`](https://github.com/bank-sampah-PILAH/pilah-be/commit/49cd153)

Review finding 1 was that pencairan accepted any active nasabah, while setoran already required an approved membership — so a pending member could be paid out but not deposit. The fix makes both money flows resolve the nasabah the same way:

```python title="api/services.py — identical in create_setoran and create_pencairan"
            Nasabah.objects.select_for_update()
            .filter(
                id=payload["nasabah_id"],
                bank_sampah=bank,
                is_active=True,
                status=Nasabah.Status.APPROVED,
            )
            .first()
```

One rule, applied on both sides, rather than a second variation of "who may transact".

## 22 Sep

### Removing dead code — [`bd38dc6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/bd38dc6)

`PencairanViewSet.list` had an unpaginated fallback that could never run, because `StandardPagination` is the global default, so `paginate_queryset` never returns `None`. Six lines became two, and the reason is written down so the next reader does not restore the branch:

```diff title="api/views.py — bd38dc6"
     def list(self, request: Request) -> Response:
-        qs = self.get_queryset()
-        page = self.paginate_queryset(qs)
-        serializer = PencairanDetailSerializer(page if page is not None else qs, many=True)
-        if page is not None:
-            return self.get_paginated_response(serializer.data)
-        return Response(serializer.data)
+        # Pagination is configured globally (PAGE_SIZE), so a page always exists.
+        page = self.paginate_queryset(self.get_queryset())
+        return self.get_paginated_response(PencairanDetailSerializer(page, many=True).data)
```

The list test stayed green, which is what made the deletion safe rather than hopeful.
