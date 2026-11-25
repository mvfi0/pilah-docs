# Security

!!! success "Competency level: 3"
    **Level 3: a scan, explained, with a patch plan.** PIL-539 got its own **OWASP ZAP 2.17.0** scan right after it was finished, on 23 Nov. It's the first scan signed in as a **nasabah** rather than the demo Pengurus, because the flow is the nasabah's. It ran against my own local instance, with a fresh seeded database and a backend started with an empty environment. Report: [ZAP scan of PIL-539, 23 Nov](../../security/zap-2026-11-23.md).

    - **0 High and no new finding.** Every alert is one already on record, and the report says which.
    - **The endpoint that matters was actually attacked:** 224 attacks on `POST /api/v1/onboarding/nasabah`, with the real body. None got a 5xx, and none created a membership: afterwards the nasabah has exactly the two rows the drive made.
    - **A gap in the tooling found and fixed:** the first run left that endpoint unscanned, because ZAP can't find a path that only ever saw POST. `tools/zap_scan.py` now scans such a path from its recorded request. This closes the limit reported on 17 Nov.
    - **Every 5xx in the backend log read and classified:** the debug-only browsable-API crash (already on record, now seen on the nasabah's riwayat) and the local Google sign-in, which has no client id.

    **The commits name what they guard:** #185's tests name **A01** (only the second bank's pengurus decides; a pending membership opens no saldo) and **A04** (one membership per bank, enforced on the server). #276 names **A04**: the client sends only a bank id, and who applies comes from the session.

## The ZAP scan

| | |
|---|---|
| Target | `staging` at [`80a30aa`](https://github.com/bank-sampah-PILAH/pilah-be/commit/80a30aa), the #185 merge, on `127.0.0.1:8539` |
| Database | Scratch PostgreSQL 16 database `zap539`, created fresh and filled by `seed_testing_data`, plus a second active bank sampah to apply to. No real user data |
| Signed in as | `customer.demo@example.com`, the seeded nasabah, approved at one bank |
| Environment | `DEBUG=true`, started with `env -i` plus only the variables it needs |

The drive module sends the flow's real requests through ZAP's proxy, so the active scan has real ids and a real body to attack:

| Request | Answer |
|---|---|
| `GET /api/v1/nasabah/me` | 200, one approved membership |
| `GET /api/v1/bank-sampah` | 200, the directory |
| `POST /api/v1/onboarding/nasabah` with the second bank | **201**, pending |
| the same again; then the nasabah's own bank | 400, "Anda sudah terdaftar sebagai nasabah di bank sampah ini" |
| with `bank_sampah_id: "bukan-uuid"` | 422 |
| `GET /api/v1/nasabah/me/saldo?keanggotaan_id=<pending>` | **403**: a pending membership can't open its saldo |

## What the scan shows on the feature's paths

| Path | Requests | Answers |
|---|---|---|
| `POST /api/v1/onboarding/nasabah` | 228: 224 attacks and the drive's four | 207 × 422, 19 × 400, 1 × 404 and one 201, the drive's own. No 5xx and no extra membership |
| `/api/v1/nasabah/me` and children | about 4,000 | 200, 403, 404, 405, 422 and 3 × 429 (the per-user throttle). 3 × 500, the known debug-only crash |
| `/api/v1/bank-sampah` and children | about 2,490 | Every write a nasabah tried was refused: 1,926 × 403 on `PUT` and 6 on `POST` |

| Earlier finding | Status after this scan |
|---|---|
| 9 Nov 3 / 2 Nov 2: the browsable API crashes on list views without a `queryset` | Still open, debug-only. Seen again on `NasabahHistoryView`; it joins patch plan item 1 |
| 26 Oct 2: CSP wildcard directive | Still open |
| 17 Nov limit: a POST- or DELETE-only path can't be actively scanned | **Fixed in the tooling** in this scan |

## Patch plan

| # | Fix | Test first | OWASP | Status (24 Nov) |
|---|---|---|---|---|
| 1 | `renderer_classes = [JSONRenderer]` on the nasabah history view | `Accept: text/html` on `/nasabah/me/riwayat` under `DEBUG=True` gets 200 or 406, not 500 | A05 | Planned, low priority (debug-only) |
| 2 | `tools/zap_scan.py` scans a POST- or DELETE-only path from its recorded request | Rescan: the path is attacked (224 attack requests in the log) | — | **Done** (23 Nov) |
| — | 26 Oct finding 2 | As in [that plan](../../security/zap-2026-10-26.md#patch-plan) | A05 | Still open on `staging` |

## What went wrong on the way

- **The first run left the endpoint that matters unscanned.** ZAP refused it with "URL Not Found in the Scan Tree". I started that scan by hand through ZAP's API with the method and body, then fixed the script to do it itself, rebuilt the database and reran everything. The report is from the rerun.
- **The driver's log line was wrong.** It always said it had signed in as the demo Pengurus. It now names the account the token belongs to.
- **I stopped the scratch PostgreSQL by mistake** by deleting its lock file while it was recovering. It restarted cleanly, with its log outside the data directory, before any scan request was sent.

## OWASP categories in this week's commits

| Category | Guarded by | Check |
|---|---|---|
| **A01 Broken Access Control** | [#185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) [`b97596a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b97596a7), [`499b32b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/499b32bb), [`2abe793`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2abe7937) | The first bank's pengurus gets 404 deciding the second bank's application; a pending membership's saldo is 403; each approved bank's saldo is its own |
| **A04 Insecure Design** | #185 [`261a571`](https://github.com/bank-sampah-PILAH/pilah-be/commit/261a5710), [`c2014bd`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2014bd7); #276 [`874d72c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/874d72c8), [`b34db8b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b34db8be) | One membership per bank is enforced on the server (400 on a duplicate), and the app sends only a bank id, so removing the client's lock opens nothing |

Two categories this week, both with a test behind them. Level 2 (five categories) isn't met by this week's commits alone. Level 3 rests on the scan.
