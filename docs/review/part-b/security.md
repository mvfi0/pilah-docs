# Security

!!! success "Competency level: 1"
    Code prevents OWASP A01 (Broken Access Control) and A04 (Insecure Design), and A01 is named in the commit message of the test that guards it.

## 15–21 Sep

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

## 22 Sep

### A01 named in a commit message

[`8ee88c1 test(pencairan): cover bank scoping of filtered riwayat (OWASP A01)`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8ee88c1), in [pilah-be #32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32): another bank's pencairan never appears in the riwayat list, with or without the new period and search filters. The bank filter is applied before any user-supplied filter, so no filter combination can widen the result beyond the pengurus' own bank.

## To do

- Keep naming the OWASP item in security-relevant commit messages; level 2 needs at least 5 of the Top 10.
