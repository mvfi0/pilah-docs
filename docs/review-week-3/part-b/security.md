# Security

!!! success "Competency level: 2"
    Code that prevents five OWASP Top 10 (2021) categories (A01, A03, A04, A08 and A09), each named in the commit that adds its guard or test, and each backed by a test that fails without the guard. All of it is in [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) (PIL-304).

| OWASP category | Guard | Commits |
|---|---|---|
| **A01 Broken Access Control** | Only the owning bank's pengurus can change a price | [`c9ee023`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c9ee023) |
| **A03 Injection** | The jenis list's filter parameters are allow-listed | [`94267c8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/94267c8) → [`cef01bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cef01bb) |
| **A04 Insecure Design** | A price cannot be backdated, scheduled years out, or sent with an ambiguous time | [`1c829d6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1c829d6) → [`78f1945`](https://github.com/bank-sampah-PILAH/pilah-be/commit/78f1945) |
| **A08 Software and Data Integrity Failures** | The database rejects a price of 0 or below; recorded setoran keep their price | [`8593164`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8593164) → [`915b3d1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/915b3d1), [`90ace04`](https://github.com/bank-sampah-PILAH/pilah-be/commit/90ace04) |
| **A09 Security Logging and Monitoring Failures** | Every price version records who changed it and when | [`f0fbe9d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0fbe9d) → [`c729f7a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c729f7a) |

## A01 · Broken Access Control

The new `POST /jenis-sampah/{id}/harga` changes money-relevant data, so I checked it against the two ways it could leak: another bank's pengurus, and a nasabah. The viewset's queryset starts from the caller's own bank, and `IsActivePengelola` gates the whole viewset, so the action inherits both. The test proves it and checks that no version was written:

```python title="apps/waste_catalog/test_harga_api.py (excerpt)"
        self.auth_as(pengurus_lain)
        self.assertEqual(self.ubah_harga(jenis["id"], {"harga_per_kg": "1"}).status_code, 404)
        self.auth_as(nasabah)
        self.assertEqual(self.ubah_harga(jenis["id"], {"harga_per_kg": "1"}).status_code, 403)
        self.assertEqual(HargaSampah.objects.filter(jenis_sampah_id=jenis["id"]).count(), 1)
```

## A03 · Injection

The list passed `status` and `kategori` from the URL straight into the queryset logic. An unknown `status` was silently read as "all", and an injection-looking `kategori` such as `plastik' OR '1'='1` returned an empty list instead of an error. The ORM parameterises queries, so this was not exploitable SQL injection. Positive server-side validation is still the prevention OWASP lists for A03: only known values may reach the query. They now go through an allow-list first, and anything else gets 422:

```python title="apps/waste_catalog/serializers.py"
class FilterJenisSampahSerializer(serializers.Serializer[Any]):
    status = serializers.ChoiceField(choices=["aktif", "tidak_aktif", "semua"], default="aktif")
    kategori = serializers.ChoiceField(choices=JenisSampah.Kategori.choices, required=False)
```

The test sends both the valid values the app uses (`status=semua`) and the invalid ones, so the guard can't break the app.

## A04 · Insecure Design

BR-03 says a price change is never retroactive: a setoran must keep the price that applied when it was recorded. The endpoint enforces the rule instead of trusting the app:

```python title="apps/waste_catalog/serializers.py"
    def validate_berlaku_mulai(self, value: datetime) -> datetime:
        sekarang = timezone.now()
        if value <= sekarang:
            raise serializers.ValidationError(
                "Harga tidak boleh berlaku surut. Kosongkan untuk berlaku sekarang."
            )
        if value > sekarang + timedelta(days=BATAS_JADWAL_HARGA_HARI):
            raise serializers.ValidationError(
                f"Harga paling lambat dijadwalkan {BATAS_JADWAL_HARGA_HARI} hari dari sekarang."
            )
        return value
```

A time without a UTC offset is also rejected. A bare local time would be read as UTC and land seven hours off for a bank in WIB, which is the kind of design flaw that only shows up in production. The red test showed it: a WIB time was stored as `18:08Z` instead of `11:08Z`.

## A08 · Software and Data Integrity Failures

Two integrity guards:

- **A database check, not just the serializer.** `harga_sampah_harga_positif` rejects a price of 0 or below on every write path: the admin, the shell, or a future data migration.
- **Old transactions can't be rewritten.** Each setoran item keeps the price it used (`harga_snapshot`, SDS 7.1.2). The test records a setoran, changes the price, and checks that the old item, its subtotal and the transaksi total are unchanged, while the next setoran uses the new price.

## A09 · Security Logging and Monitoring Failures

Every price version stores `dibuat_oleh` and `created_at` (BR-11), and versions are never edited or deleted. The full price history of a jenis, including who scheduled a change and when, can always be reconstructed. That's the audit trail a pricing dispute needs.
