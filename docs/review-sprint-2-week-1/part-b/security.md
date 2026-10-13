# Security

!!! success "Competency level: 3"
    A dynamic security scan of the backend with **Metasploit Framework 6.5.3**, explained, with a test-first patch plan: [Security scan report](../../security/index.md). The scan was run against my own local instance and cross-checked against `python manage.py check --deploy`.

    Alongside the scan, this week's new code guards **A01 Broken Access Control** on the new price-history endpoint (named in its commit and tested), with two more OWASP behaviours (A08, A09) tested but not named in their commits.

## Security scan (level 3)

Ran [Metasploit](../../security/index.md) against the backend on a local instance (`manage.py runserver`, seeded test DB; staging and production were not touched). Method: Metasploit `auxiliary/scanner/http/*` for fingerprinting, headers, directory enumeration and method discovery, then `curl` to verify, then `check --deploy` as a static cross-check.

**Explained — why a generic exploit framework finds little here.** Metasploit exploits *known* vulnerabilities in *known* software. PILAH's backend is a bespoke Django/DRF app, so no exploit module matches it; its scanners confirmed there is no exploitable off-the-shelf service, and the findings that matter are application- and configuration-level. That clean result is itself a finding.

**Findings (full detail and evidence in the [report](../../security/index.md)):**

| # | Finding | OWASP | Severity | Scope |
|---|---|---|---|---|
| 1 | `/api/schema/` and `/api/docs/` served without authentication — full API contract disclosed | A01 / A05 | Medium | prod + dev |
| 2 | HSTS not configured (`SECURE_HSTS_SECONDS` unset; `security.W004`) | A05 | Low–Med | prod |
| 3 | App-layer HTTPS redirect not enforced (`security.W008`) | A05 | Low | prod |
| 4 | No `Content-Security-Policy` / `Permissions-Policy` | A05 | Low | prod + dev |
| 5 | Server banner leaks framework and Python version | A05 | Info | dev |
| 6 | `DEBUG=true` error pages leak the URL configuration | A05 | Med *if deployed* | dev-only |

**Patch plan (priority first), each a test-first change naming its OWASP category:**

1. Restrict the schema/docs behind `IsAdminUser` (or `IsAuthenticated`), so an unauthenticated request gets 401/403.
2. Enable HSTS (`SECURE_HSTS_SECONDS`, include-subdomains, preload) guarded by `not DEBUG`.
3. `SECURE_SSL_REDIRECT = not DEBUG`, using the proxy header already set.
4. Add a minimal CSP / Permissions-Policy, scoped to the API and the Swagger page.
5. Suppress the `Server` banner at the gunicorn/middleware layer.
6. A CI/start-up guard that a production build cannot boot with `DEBUG=true`.

**What held up.** Every `/api/v1/*` endpoint returns `401` without a token; `/admin/` redirects to login; `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy` and COOP are all present; `/.env` is 404, there is no path traversal, and only safe HTTP methods are allowed.

## OWASP guards in this week's new code

| OWASP category | Guard | Commit | Named in the commit |
|---|---|---|---|
| **A01 Broken Access Control** | Only the owning bank's pengurus can read a jenis's price history | [`8bc2be8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8bc2be8) | yes |
| A08 Software and Data Integrity Failures | Rerunning the seed no longer rewrites historical setoran snapshots | [`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) → [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f) | no |
| A09 Security Logging and Monitoring Failures | The price history shows who recorded each version | [`1f43102`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1f43102) → [`50d9392`](https://github.com/bank-sampah-PILAH/pilah-be/commit/50d9392) | no |

### A01 · Broken Access Control

PIL-331's `GET /jenis-sampah/{id}/harga` exposes every past price of a jenis — business data — so I checked it against the two ways it could leak:

```python title="apps/waste_catalog/test_riwayat_harga.py (excerpt)"
        self.auth_as(pengurus_lain)
        self.assertEqual(self.riwayat(jenis["id"]).status_code, 404)
        self.auth_as(nasabah)
        self.assertEqual(self.riwayat(jenis["id"]).status_code, 403)
```

The action reuses the viewset's bank-scoped `get_object` and `IsActivePengelola`, so the test passed when written. I proved it guards something by swapping in an unscoped lookup, seeing another bank read the prices and the test fail, then restoring the code. The commit names the category: "(OWASP A01, BR-01)".

### Also tested this week

- **A08, data integrity.** Each seeded setoran must keep the price of its own date (BR-03). The red test recorded a price change taking effect now and reran the seed; a historical snapshot went from 3,500 to 99,999. The fix prices each setoran at its stored `tanggal`.
- **A09, audit trail.** The price history makes `dibuat_oleh` readable to the pengurus (`null` for prices backfilled by the migration).
