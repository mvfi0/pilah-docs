# Security

!!! success "Competency level: 1"
    Code prevents OWASP A01 (Broken Access Control), the risk is named in the commit message of the test that guards it, and the new filters were checked against it before merge.

## A01 · Broken Access Control, named in the commit

[`8ee88c1 test(pencairan): cover bank scoping of filtered riwayat (OWASP A01)`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8ee88c1), in [pilah-be #32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32).

Adding `periode`, `nasabah_id` and `search` to the pencairan list is exactly where a scoping bug appears: a user-supplied filter that widens the queryset would leak another bank's payouts. The queryset is always rooted at `filter(bank_sampah=...)` before any filter is applied, and the test asserts that another bank's pencairan never appears — with no filter, with a search matching their nasabah's name, and with each periode.

| Control | Test |
|---|---|
| Bank scoping applied before every user filter | `test_riwayat_never_shows_another_bank` |
| A `nasabah_id` from another bank returns an empty list, not that bank's rows | same |
| A `search` matching another bank's nasabah name returns nothing | same |

The reviewer confirmed this independently: "the queryset is always rooted at `filter(bank_sampah=_bank_sampah(request))` before any filter is applied, so a `nasabah_id` or `search` matching another bank's data cannot leak".

## Why it matters here

This is the SDS rule BR-01/BR-02 in practice: one database serves every bank sampah, so a query that forgets its organisation filter returns other organisations' data without raising an error. A test is the only thing that notices.

## To do

- Level 2 needs at least 5 of the OWASP Top 10 named and guarded; A01 and A04 are covered so far.
