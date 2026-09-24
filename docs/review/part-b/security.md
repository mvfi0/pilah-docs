# Security

!!! success "Competency level: 1"
    Code prevents OWASP A01 (Broken Access Control) and A04 (Insecure Design), each control guarded by a test.

## 15–21 Sep

### The two controls in code

Every pencairan endpoint carries the permission class, and every query is rooted at the caller's own bank sampah, taken from the session rather than from the request body:

```python title="api/views.py"
class PencairanViewSet(viewsets.GenericViewSet):
    permission_classes = [IsActivePengelola]
    serializer_class = PencairanDetailSerializer

    def get_queryset(self) -> QuerySet[Pencairan]:
        qs = Pencairan.objects.filter(bank_sampah=_bank_sampah(self.request)).select_related(
            "nasabah", "bank_sampah", "dicatat_oleh"
        )
```

`_bank_sampah` reads the bank off the authenticated user, so a caller cannot name someone else's bank:

```python title="api/views.py"
def _bank_sampah(request: Request) -> BankSampah:
    bank = _user(request).bank_sampah
    assert bank is not None  # ponytail: IsActivePengelola guarantees bank membership
    return bank
```

Because the filter is part of the base queryset, `retrieve` on another bank's pencairan finds nothing and returns **404 rather than 403** — the record's existence is never confirmed.

```python title="api/tests.py — test_pencairan_detail_is_scoped_to_bank_sampah"
        self.assertEqual(
            self.client.get(f"/api/v1/pencairan/{created.data['id']}").status_code, 404
        )
        ...
        self.assertEqual(self.client.post("/api/v1/pencairan", {}, format="json").status_code, 403)

        self.client.credentials()
        self.assertEqual(self.client.post("/api/v1/pencairan", {}, format="json").status_code, 401)
```

**No mass assignment:** the write serializer accepts five fields and nothing else. `bank_sampah`, `dicatat_oleh`, `status` and both saldo snapshots are set by the service, so a crafted request body cannot book a payout against another bank or forge a receipt.

```python title="api/serializers.py"
class PencairanCreateSerializer(serializers.Serializer[Any]):
    nasabah_id = serializers.UUIDField(required=True)
    nominal = serializers.DecimalField(max_digits=14, decimal_places=2, required=True)
    metode = serializers.ChoiceField(choices=Pencairan.Metode.choices, required=True)
    tanggal = serializers.DateTimeField(required=False)
    keterangan = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, max_length=255
    )
```

The money rules are enforced twice, in the serializer and again in the database:

```python title="api/serializers.py"
    def validate_nominal(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Nominal harus lebih dari nol")
        if value != value.to_integral_value():
            raise serializers.ValidationError("Nominal harus dalam rupiah bulat tanpa desimal")
        return value
```

```python title="api/models.py"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nominal__gt=0), name="pencairan_nominal_positive"
            ),
        ]
```

And the A04 control — the saldo check runs inside the same locked transaction that writes the record, so two concurrent payouts cannot both pass it:

```python title="api/services.py"
        saldo, _ = Saldo.objects.select_for_update().get_or_create(nasabah=nasabah)
        nominal = payload["nominal"]
        saldo_sebelum = saldo.total_saldo
        if nominal > saldo_sebelum:
            raise serializers.ValidationError({"nominal": ["Saldo nasabah tidak mencukupi"]})
```

### A01 · Broken Access Control

| Control | Commit | Test |
|---|---|---|
| Every pencairan endpoint requires an active pengurus (`IsActivePengelola`); superadmin gets 403, unauthenticated 401 | [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b) | `test_pencairan_detail_is_scoped_to_bank_sampah` |
| Queries scoped to the pengurus' own bank sampah; another bank's pencairan returns 404, not 403, so their existence is not revealed | [`cb9da4a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cb9da4a) | same |
| Cannot pay out another bank's nasabah | [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b) | `test_pencairan_is_scoped_to_own_active_nasabah` |
| Only approved members can be paid out | [`49cd153`](https://github.com/bank-sampah-PILAH/pilah-be/commit/49cd153) | `test_pencairan_requires_approved_membership` |
| `status`, `dicatat_oleh`, `bank_sampah` and the saldo snapshots are set by the server, never from request input (no mass assignment) | [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b) | — |

### A04 · Insecure Design (business logic integrity)

| Control | Commit |
|---|---|
| Row locks (`select_for_update`) on the nasabah and saldo, so two simultaneous payouts cannot both pass the saldo check | [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b) |
| Saldo can never go negative: the service rejects any nominal above the saldo, inside the locked transaction | [`e65ff1d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e65ff1d) |
| A zero or negative nominal is rejected twice: by the serializer and by a database constraint (`pencairan_nominal_positive`) | [`6615dc8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6615dc8), [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b) |

## 22 Sep — mobile

The mobile form sends no security-relevant field of its own: `bank_sampah`, `dicatat_oleh`, `status` and the saldo snapshots are all set by the server, and the entry point is shown only for an active nasabah of the pengurus' own bank ([`98e9b15`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/98e9b15)). The client's validation is a convenience; every rule is enforced again in the backend, and the tests assert both sides.

## To do

- Naming the OWASP item in the commit message is done in [week 2](../../review-week-2/part-b/security.md); level 2 needs at least 5 of the Top 10.
