# Security

!!! success "Competency level: 3"
    **Level 3: a scan, explained, with a patch plan.** Each sub-issue finished this week, PIL-481 and PIL-480, got its own **OWASP ZAP 2.17.0** scan right after the work was done (9 Nov). Both ran signed in, against my own local instances, and were limited to the feature's endpoints. Report: [ZAP scans per sub-issue, 9 Nov](../../security/zap-2026-11-09.md).

    - **0 real High.** ZAP raised three High alerts (SQL injection, Server Side Include, Padding Oracle). Each was checked by hand and is a false positive. The "SQL injection" on the void's `alasan` was disproved by sending both payloads myself.
    - **A new finding behind two of them:** a malformed `nasabah_id` on `GET /transaksi` is a 500, while `/aktivitas` answers 422. Reproduced by hand, given a test-first patch plan, and filed as [PIL-482](https://linear.app/pilah-2/issue/PIL-482). It was fixed in Sprint 3 Week 3.
    - **Every 5xx in ZAP's history read and classified,** not only its alerts: 268 in the PIL-481 scan and 5 in PIL-480, sorted into real, debug-only and local.
    - **A broken run replaced, not trusted.** The first run hit a full disk and an out-of-memory database, so both scans were run again once the disk was freed. The report uses the second run.

    The commits name seven OWASP categories, but only three are genuine guards with a test behind them: **A04, A08 and A09**. The other four labels are weak (see [below](#owasp-guards-in-this-weeks-code)). Three is short of level 2's five, so the level rests on the scan.

## The ZAP scans

| Sub-issue | Target | In-scope requests | ZAP alerts on the feature | Found by reading the history |
|---|---|---|---|---|
| [PIL-481](https://linear.app/pilah-2/issue/PIL-481) | #167 backend, #238 web build | 7,590 on `/transaksi` (444 on `/batalkan`), 3,774 on `/aktivitas`, 28 on the dashboard list | none real; three false High alerts | 226 × 500 on a malformed `nasabah_id` (new); the known NUL-in-`search` and debug-only 500s |
| [PIL-480](https://linear.app/pilah-2/issue/PIL-480) | #168 backend | 4,835 on the export, 2,189 on `/aktivitas` | none | The known NUL-in-`search` 500, now also on the export |

| # | Finding | OWASP | Planned fix | Status |
|---|---|---|---|---|
| 1 | A malformed `nasabah_id` on `GET /transaksi` is a 500 | A04; A10:2025 | Validate it as `/aktivitas` does, and answer 422; a test per endpoint | Filed as PIL-482 (9 Nov). **Fixed** by [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) in Sprint 3 Week 3, and verified by the 17 Nov scan: 965 malformed ids, all 422 |
| 2 | A NUL byte in `?search=` is a 500, now also on the export | A04; A10:2025 | One shared helper that reads `search` through a DRF `CharField` | Fixed on `staging` by Scallss's #172 (16 Nov) |
| 3 | The browsable API crashes on `/aktivitas` and a setoran's detail | A05 | A JSON-only renderer | Planned, low priority (debug-only) |
| 4 | With `DEBUG=true` the 500 page lists the whole process environment | A05 | Nothing in code: `DEBUG` is off in staging and production. Keep scan reports redacted | Closed, but see the next section |

### The "SQL injection" on `alasan`, disproved by hand

| Request | Result |
|---|---|
| `alasan = John Doe' AND '1'='1' -- ` | 200, voided |
| `alasan = John Doe' AND '1'='2' -- ` | 200, voided |
| the same setoran voided again | 409 |

Both payloads behave the same, and the stored `alasan` is the payload text. ZAP's "different pages" came from a state change: the first request voided the setoran (200), and every attack after it hit an already-voided one (409). The ORM parameterises the value.

### What went wrong: the evidence leaked two webhooks

Finding 4's debug page also held two Discord webhook URLs from the dev machine's environment. I had redacted the computer name and my user name from the saved report files, but not these, and they were published with the report on 9 Nov. GitHub's secret scanning found them, and Discord revoked both.

This was caught and fixed on **13 Nov** (Sprint 3 Week 3), in pilah-docs [`2197468`](https://github.com/mvfi0/pilah-docs/commit/2197468):

- the two files now carry `[REDACTED]`;
- the scan script refuses webhooks, GitHub, Google and Slack tokens, and database URLs with a password;
- the report's false claim that I had "grepped for secrets" is corrected.

From the 17 Nov scans on, the backends start with an empty environment, so no secret can reach a debug page. It's recorded here because the mistake was made in this week's work.

## OWASP guards in this week's code

| OWASP category | Guard | Tests | Commits |
|---|---|---|---|
| **A04 Insecure Design** | Re-seeding can't put voided money back into a saldo. A void in flight can't be dismissed half-done, and a successful void always refreshes the UI. Hiding a void is a filter, not a delete | Reseed tests per seed command; three in-flight dialog tests; "still reachable by id" guards | [`743ed1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/743ed1c3), [`abcafa3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/abcafa30), [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07), [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b), [`7d0922d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7d0922d7) |
| **A08 Software and Data Integrity Failures** | Every list and total reads the same `tercatat()` subset, so the summary can't disagree with the list it sums. The export's 13 columns and their order are pinned | Summary totals asserted unchanged after a void; the export header and `max_column == 13` | [`8143807`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8143807d), [`3d83377`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3d833773) |
| **A09 Security Logging and Monitoring Failures** | Hiding a void never loses the audit trail: the row, who voided it, when and why stay, and its detail by id still shows them, to the pengurus and the nasabah | `test_a_voided_setoran_stays_reachable_by_its_id_with_its_void`, `test_nasabah_can_still_open_the_voided_setoran_by_its_id` | [`7d0922d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7d0922d7), [`4401e4e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/4401e4e2) |

**Labels I don't count.** The PIL-481 and PIL-480 commit bodies also name:

- **A01:** "a nasabah only ever sees their own membership's rows". True, but that scoping predates this change, which reads through the existing `/me` endpoints, and no new test asserts another member's rows are left out.
- **A02:** "no staff-only void fields are added to the nasabah DTO", "no internal record ids in a forwarded file". That is data minimisation, closer to A01 than to cryptography.
- **A03:** for a filter on a fixed status value, there's no untrusted input to inject.
- **A05:** "no new query flag or toggle", "the sheet layout is pinned". That's the absence of a change, not a guard.

They are honest descriptions of what the change doesn't break, but not controls, so they aren't claimed here.
