# Security scan — PILAH backend, 14 Oct 2026

A dynamic security scan of the PILAH backend (`pilah-be`) with **Metasploit Framework 6.5.3**, plus targeted manual verification and a cross-check against Django's own `check --deploy`. Run for the IR Security competency (a Metasploit-or-similar scan, explained, with a patch plan).

!!! note "Scope and authorisation"
    Scanned **my own local instance only**: `manage.py runserver` on `127.0.0.1:8001`, reached from WSL at `http://172.19.64.1:8001`, against the seeded test database (no real user data). The deployed staging/production hosts were **not** scanned. The server ran with `DEBUG=true`, so some findings below are dev-only and are labelled as such — they would not appear under production settings (`DEBUG=false`).

## Method

| Step | Tool |
|---|---|
| Fingerprint, headers, robots, methods, directory enumeration | Metasploit `auxiliary/scanner/http/*` |
| Header and endpoint verification (full header set, auth checks, sensitive paths) | `curl` |
| Static configuration cross-check | `python manage.py check --deploy` |

Full Metasploit console output: [metasploit-output-2026-10-14.txt](evidence/metasploit-output-2026-10-14.txt).

## Why Metasploit found little, and why that is itself a result

Metasploit is built to exploit **known vulnerabilities in known software** — an unpatched service, a vulnerable CMS plugin, a specific library CVE. PILAH's backend is a bespoke Django / DRF application, so Metasploit has no exploit module that matches it. Its HTTP auxiliary scanners could still do reconnaissance — fingerprint the server, read the headers, enumerate directories — and confirm there is **no exploitable off-the-shelf service** here. The findings that matter are application- and configuration-level, and those came from reading the headers Metasploit dumped and from targeted manual probing. A clean Metasploit result is a meaningful result: the attack surface is a custom API, not a stack of exploitable components.

## Findings

| # | Finding | OWASP (2021) | Severity | Scope |
|---|---|---|---|---|
| 1 | API schema and Swagger UI served without authentication | A01 / A05 | **Medium** | prod + dev |
| 2 | HSTS not configured (`SECURE_HSTS_SECONDS` unset) | A05 | Low–Medium | prod |
| 3 | App-layer HTTPS redirect not enforced (`SECURE_SSL_REDIRECT` unset) | A05 | Low | prod |
| 4 | No `Content-Security-Policy` or `Permissions-Policy` header | A05 | Low | prod + dev |
| 5 | Server banner leaks framework and Python version | A05 | Info | dev (reduced in prod) |
| 6 | `DEBUG=true` error pages leak the URL configuration | A05 | Medium *if deployed* | dev-only |
| 7 | Session/CSRF cookies without the `Secure` flag | A05 | — | dev-only |

### 1. API schema and docs are public — *Medium, prod-affecting*

`GET /api/schema/` and `GET /api/docs/` both return **200 with no authentication**:

```console
$ curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/api/schema/   # 200
$ curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/api/docs/      # 200
```

Both views are registered with no permission restriction:

```python title="config/urls.py"
path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
```

`drf-spectacular` defaults to `AllowAny`, so the complete API contract — every endpoint, every parameter, every request and response schema — is published to anyone. For an application that handles customer PII and money movements, that is free reconnaissance: an attacker learns the whole surface without a single credential. This is **not** gated by `DEBUG`; it is in the main URL patterns unconditionally. **This is the one finding I would fix first.**

### 2–3. Transport hardening not set — *Low–Medium, prod*

The dynamic scan saw no `Strict-Transport-Security` header, and the static check agrees:

```console
$ python manage.py check --deploy
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting...
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True...
```

TLS is terminated by the hosting proxy (Cloud Run / Fly), and `SECURE_PROXY_SSL_HEADER` is correctly set, so traffic is encrypted. What is missing is telling the browser to *insist* on HTTPS (HSTS) and redirecting any stray HTTP request at the app layer.

### 4. No CSP / Permissions-Policy — *Low*

For the JSON API this is minor, but `/api/docs/` serves an HTML Swagger page, and that page has no `Content-Security-Policy`. The good headers that *are* present (below) cover clickjacking and MIME-sniffing; CSP and `Permissions-Policy` would complete the set for the one HTML surface.

### 5. Server banner — *Info*

```
Server: WSGIServer/0.2 CPython/3.12.10
```

The dev server names itself and the Python version. Production runs behind gunicorn, which still sends a `Server` header but less detail; suppressing it entirely is a small hardening step.

### 6–7. Dev-only, documented not actioned

- **`DEBUG=true` disclosure.** An unknown path returns Django's debug 404, which lists the whole URL map ("`tried these URL patterns`", 3.4 KB). A 500 would show a full traceback and settings. This only happens with `DEBUG=true`; `DEBUG` defaults to `false` and production sets it false, with `PILAH_ALLOW_FAKE_GOOGLE_TOKEN` guarded to refuse a non-debug boot. Real risk only if a deployment ever shipped `DEBUG=true` — worth a CI guard, not a code fix.
- **Cookies without `Secure`.** `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` are `not DEBUG`, so they are secure in production and only unset in local dev.

## What held up

The scan found no way around the access controls, and the baseline posture is sound:

- **Authentication enforced.** Every `/api/v1/*` endpoint returns `401 Unauthorized` with `WWW-Authenticate: Bearer realm="api"` when unauthenticated; `/admin/` redirects to the login page. (Cross-bank data isolation is covered by the A01 tests in the codebase.)
- **Good response headers present:** `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Cross-Origin-Opener-Policy`.
- **No low-hanging exposure:** `/.env` → 404, `/static/` → 404, no `robots.txt`, no path traversal, and only safe HTTP methods are allowed (`GET, POST, HEAD, OPTIONS` — no `PUT`/`DELETE`/`TRACE` at the surface).
- **Directory enumeration** (Metasploit `dir_scanner`, default wordlist) surfaced only `/admin/`, which is the expected Django admin login.

## Patch plan

Each fix would be a test-first change on its own branch, with the OWASP category named in the commit, and re-verified with the same scan.

1. **Restrict the schema and docs (finding 1).** Set `SPECTACULAR_SETTINGS["SERVE_PERMISSIONS"] = ["rest_framework.permissions.IsAdminUser"]` (or gate the two routes behind `IsAuthenticated`, or serve them only when `DEBUG`). Test: an unauthenticated `GET /api/schema/` and `/api/docs/` return 401/403; an admin gets 200.
2. **Enable HSTS (finding 2).** `SECURE_HSTS_SECONDS = 31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`, `SECURE_HSTS_PRELOAD = True`, all guarded by `not DEBUG`. Test: the header is present with `DEBUG=false` and absent with `DEBUG=true`.
3. **Enforce HTTPS redirect (finding 3).** `SECURE_SSL_REDIRECT = not DEBUG`, relying on the `SECURE_PROXY_SSL_HEADER` already configured. Clears `security.W008`.
4. **Add a minimal CSP / Permissions-Policy (finding 4).** A middleware or `django-csp`, scoped so the API responses and the Swagger page both get a sensible policy.
5. **Suppress the server banner (finding 5).** Strip or rewrite the `Server` header at the gunicorn/middleware layer.
6. **Guard against `DEBUG=true` in deploys (finding 6).** A CI or start-up assertion that a production build cannot boot with `DEBUG=true` (partly covered already by the fake-token guard).

Findings 1–3 are the priority: finding 1 is a real contract disclosure, and 2–3 close the two warnings `check --deploy` already raises.
