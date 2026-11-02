# Security

!!! warning "Competency level: 1"
    This week's code guards and names **four** OWASP Top 10 categories in its commits: **A01, A04, A08 and A09**, each with tests. Level 2 needs at least five named in one week's commits, so this week claims level 1, as last week did. I didn't stretch a fifth label to fill the gap.

    New this week is **A08**: a database constraint that refuses a half-recorded void, proven by attempting one. Review work also touched A09 in a teammate's code (see below), but that isn't counted here, because it isn't my commit.

## OWASP guards in this week's code

| OWASP category | Guard | Tests | Commits |
|---|---|---|---|
| **A01 Broken Access Control** | Only an active pengurus of the setoran's own bank can void it: another bank's setoran is 404, and a nasabah account gets 403. The nasabah DTO gains only `status`, not who voided it or why. On PIL-451, a pengelola account can no longer end up holding a nasabah membership | 404, 403, and DTO field-set contract tests; the stale-login test | [`f67aa72`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67aa72), [`d19cb8d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d19cb8d) |
| **A04 Insecure Design** | A void can't take money already paid out, even when the final saldo would stay positive but a later pencairan would have been unfunded. A voided setoran is final: no second void, no edit, no WhatsApp resend. On PIL-451, the role-change invariant holds on the Google-login path too | 409s with nothing changed; a two-thread race test on PostgreSQL | [`997c5d0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/997c5d0), [`b08e3eb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b08e3eb), [`99de195`](https://github.com/bank-sampah-PILAH/pilah-be/commit/99de195), [`c428c32`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c428c32), [`d19cb8d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d19cb8d) |
| **A08 Software and Data Integrity Failures** | Check constraint `transaksi_batal_lengkap`: a dibatalkan row must carry who, when and a non-empty alasan, and a tercatat row carries none of them. It holds for every write path, not only the service | Three partial `.update()`s each raise `IntegrityError` | [`31b3ee4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/31b3ee4), [`2814ae6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2814ae6) |
| **A09 Security Logging and Monitoring Failures** | Every void records who, when and why on the row, in the same transaction as the saldo change. The mobile detail shows that record where the Pengurus reads the setoran | The audit fields asserted after a void; the inline detail shows "Dibatalkan oleh … • …" and the alasan | [`f3c3db7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f3c3db7), [`638cb3f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/638cb3f), [`ef7a0b9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef7a0b96) |

The migration adding the constraint was applied to the 20 Sep production snapshot before the PR opened. Every existing row passes it, and the user and bank sampah counts were unchanged. The snapshot database holds personal data, so it was dropped afterwards.

## Security in review

- **Given, on Rifqi's #144:** the PR's hardening aims at A09, but a database bug on the customer list would surface as a "temporary" 503 with no traceback in any log. I showed it with a throwaway test and suggested the fix: log with `exc_info`, and keep the 503 for connection errors only. Details are on [Team Development Management](team-development-management.md#review-given-rifqis-pilah-be-144-2-nov).
- **Received, on my #137:** Tristan and Heraldo found that my A04 guard from last week missed a fourth writer. It's fixed, with a race test that failed before the fix.
