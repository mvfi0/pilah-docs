# Security

!!! success "Competency level: 1"
    Code prevents OWASP A01 (Broken Access Control), the risk is named in the commit messages of the tests that guard it (on PIL-222 and PIL-230), and new endpoints were checked against it before merge.

## A01 · Broken Access Control, named in the commit

[`8ee88c1 test(pencairan): cover bank scoping of filtered riwayat (OWASP A01)`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8ee88c1), in [pilah-be #32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32).

Adding `periode`, `nasabah_id` and `search` to the pencairan list is exactly where a scoping bug appears: a user-supplied filter that widens the queryset would leak another bank's payouts.

The defence is ordering. The bank filter is the **root** of the queryset, and every user-supplied filter is chained onto it, so each one can only narrow the result further:

```python title="api/views.py"
    def get_queryset(self) -> QuerySet[Pencairan]:
        qs = Pencairan.objects.filter(bank_sampah=_bank_sampah(self.request)).select_related(
            "nasabah", "bank_sampah", "dicatat_oleh"
        )
        nasabah_id = self.request.query_params.get("nasabah_id")
        search = self.request.query_params.get("search", "")
        if nasabah_id:
            qs = qs.filter(nasabah_id=nasabah_id)
        if len(search) >= 2:
            qs = qs.filter(nasabah__nama__icontains=search)
        return qs
```

`nasabah_id` is the dangerous one: it is a raw UUID from the client, and had it been applied to `Pencairan.objects` instead of to the scoped queryset, any pengurus could have read another bank's payouts by guessing an id.

The test creates a second bank with its own nasabah and pencairan, then asserts the caller sees only their own record under every filter shape — no filter, a search matching the *other* bank's nasabah name, and a periode:

```python title="api/tests.py — test_riwayat_never_shows_another_bank"
        own = self._pencairan(self.siti, timezone.now())

        for query in ("", "?search=siti", "?periode=hari_ini"):
            with self.subTest(query=query):
                self.assertEqual(self._ids(query), {str(own.id)})
```

The other bank's nasabah is deliberately named "Siti Lain" so that `?search=siti` matches it: if the scoping were wrong, this test fails rather than passing by luck.

| Control | Test |
|---|---|
| Bank scoping applied before every user filter | `test_riwayat_never_shows_another_bank` |
| A `nasabah_id` from another bank returns an empty list, not that bank's rows | same |
| A `search` matching another bank's nasabah name returns nothing | same |

The reviewer confirmed this independently: "the queryset is always rooted at `filter(bank_sampah=_bank_sampah(request))` before any filter is applied, so a `nasabah_id` or `search` matching another bank's data cannot leak".

## Why it matters here

This is the SDS rule BR-01/BR-02 in practice: one database serves every bank sampah, so a query that forgets its organisation filter returns other organisations' data without raising an error. A test is the only thing that notices.

## A01 again on PIL-230 — [`60e7256`](https://github.com/bank-sampah-PILAH/pilah-be/commit/60e7256)

`test(pencairan): cover bank scoping and pengurus-only edit and riwayat (OWASP A01)`, in [pilah-be #52](https://github.com/bank-sampah-PILAH/pilah-be/pull/52).

The edit endpoint changes money and the revision history exposes who changed what, so both need two layers: the right **role** and the right **organisation**.

| Caller | `PATCH /pencairan/:id` | `GET /pencairan/:id/riwayat` |
|---|---|---|
| Pengurus of another bank | 404 (the pencairan is outside their scoped queryset) | 404 |
| Nasabah who owns the pencairan | 403 (pengurus only) | 403 (pengurus only, per the PO) |

After both attempts the test asserts the nominal and the saldo are unchanged, so a leak that "only" returned a 200 without saving would still fail.

## Related controls from the 26 Sep review fixes

These guard real weaknesses, but they are not yet named against an OWASP category in a commit, so they are listed here and not counted toward level 2:

| Weakness | Control | Commit |
|---|---|---|
| Admin writes bypassing the service could desynchronise a money ledger | Pencairan and revisions are read-only in Django admin | [`9f4a428`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9f4a428), [`2af8c69`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2af8c69) |
| A backdated payout funded by a later deposit (business-logic flaw) | Reject a tanggal before the nasabah's last activity | [`290bb1d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/290bb1d) |
| Nasabah reading beyond their own records | Nasabah queryset rooted at `nasabah__user = request.user` | [`3c4aac0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c4aac0) |
| Money records changed without a trace | Every edit stores the replaced version, editor, time and a required reason (append-only) | [`c2ef8a4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2ef8a4) |

## To do

- Level 2 needs at least 5 of the OWASP Top 10 named and guarded; A01 and A04 are covered so far. The controls above could be named in their commits or tests as A04 (Insecure Design, the backdating flaw) and A09 (Security Logging and Monitoring Failures, the audit trail), but only once a test or commit actually says so.
