# Security

!!! success "Competency level: 3"
    **Level 3: a scan, explained, with a patch plan.** Each sub-issue finished this week, PIL-428 and PIL-435, got its own **OWASP ZAP 2.17.0** scan right after the work was done. Both ran signed in, against my own local instances, and were limited to the feature's endpoints. Report: [ZAP scans per sub-issue, 2 Nov](../../security/zap-2026-11-02.md).

    - **0 High.** No alert on the features' own endpoints across about 15,000 attack requests.
    - **Every alert explained:** each Medium and Low ZAP raised is either a known finding from the [26 Oct scan](../../security/zap-2026-10-26.md), still open on `staging`, or an artifact of the local servers. The report says which, and why.
    - **Beyond ZAP's alerts:** reading every response in the scan history found a real crash ZAP doesn't flag. A NUL byte in `?search=` gives a 500 on six list endpoints. Reproduced by hand, with a test-first patch plan, plus two debug-only crashes.
    - **The void's input tested by hand:** injection payloads stored verbatim as data; a NUL byte, an over-long alasan or a blank one rejected with 422.

    The commits also guard and name **four** OWASP categories: **A01, A04, A08 and A09**. That's one short of level 2's five, so the level rests on the scan, not on the count.

## The ZAP scans

| Sub-issue | Target | In-scope requests | ZAP alerts on the feature | Found by reading the history |
|---|---|---|---|---|
| [PIL-428](https://linear.app/pilah-2/issue/PIL-428) | #145 backend, #193 web build | about 8,000 (`/transaksi` incl. `/batalkan` and `PATCH`, `/aktivitas`) | none | NUL-byte 500 on `/aktivitas`; debug-only 500s on `/aktivitas` and the setoran detail |
| [PIL-435](https://linear.app/pilah-2/issue/PIL-435) | `staging` backend, #196 web build | about 7,000 (`/aktivitas`, `/transaksi/export`) | none | The same NUL-byte 500, and the same debug-only one |

| # | Finding | OWASP | Planned fix |
|---|---|---|---|
| 1 | A NUL byte in `?search=` crashes six list endpoints (500, not 422); bodies are safe because DRF fields reject NUL | A04 / A10:2025 | Read list query text through a DRF `CharField` in one shared helper; a test per endpoint expects 422. Needs a Linear issue: it spans teammates' views |
| 2, 3 | The browsable API crashes on `/aktivitas` and on a setoran's detail (debug-only) | A05 | A queryset or JSON-only renderer; `alasan` marked write-only |

Method, every alert's explanation, the reproductions and the full plan are in the [report](../../security/zap-2026-11-02.md). The scan is one command, [`tools/zap_scan.py`](https://github.com/mvfi0/pilah-docs/blob/main/tools/zap_scan.py), plus a small per-feature drive module, so the next sub-issue gets the same scan.

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
