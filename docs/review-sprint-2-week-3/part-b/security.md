# Security

!!! warning "Competency level: 1"
    This week's code guards and names **four** OWASP Top 10 categories in its commits: **A01, A04, A07 and A09**, each with tests. Level 2 needs at least five named in one week's commits, so this week claims level 1. I didn't stretch a fifth label to fill the gap.

    This week's security work also includes a new dynamic scan with **OWASP ZAP 2.17.0**, explained, with a test-first patch plan: [ZAP scan report, 26 Oct](../../security/zap-2026-10-26.md). It ran signed in, against my own local backend and web build, with every documented endpoint imported from the OpenAPI schema. It is recorded below, but not claimed as a level.

## The ZAP scan

**0 High.** Four real findings, each with a planned fix (full detail in the [report](../../security/zap-2026-10-26.md)):

| # | Finding | OWASP | Severity | Planned fix |
|---|---|---|---|---|
| 1 | `tarik` and `terbitkan` crash (500) on a missing or malformed id. I reproduced it by hand; ZAP only caught `tarik` | A04 | Low–Medium | Load through the bank-scoped `get_object()` (404), test-first |
| 2 | The backend CSP allows any HTTPS origin (`script-src 'self' https:` and three more directives) | A05 | Medium | `default-src 'none'` for JSON; exact origins for the docs page and the OAuth popup |
| 3 | Swagger UI loads `@latest` from jsDelivr with no SRI | A08 | Low (debug-only) | Pin it and add hashes, or serve it locally |
| 4 | The web app shell has no `script-src` | A05 | Low–Medium | In progress as Pascal's #178; [my review](team-development-management.md#review-given-pascals-pilah-mobile-178-29-oct) found one regression in it |

**Explained, not just listed.** Of 15 alert types, the missing clickjacking and `nosniff` headers and the version-leaking `Server` header are **local artifacts**. Production nginx already sends those headers, and production doesn't run the dev servers. The report says why for each one, so the patch plan holds only real work.

## OWASP guards in this week's code

| OWASP category | Guard | Tests | Commits |
|---|---|---|---|
| **A01 Broken Access Control** | Only registering roles may change a role; superadmin can be neither left nor reached; a linked member can't leave the bank's scope | Anonymous 401, superadmin 403, asking for superadmin 422, linked member 409 (once an unhandled 500) | [`e227286`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e227286), [`52f087f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/52f087f), [`cafba5a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cafba5a). The superadmin guards are mutation-proven |
| **A04 Insecure Design** | The onboarding state machine is enforced on the server; role changes and registrations serialize on the account row | A completed profile, a pending bank or a linked membership gets 409; a two-thread race test on PostgreSQL for the bank, membership and invite paths | [`e227286`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e227286), [`52f087f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/52f087f), [`bf3a529`](https://github.com/bank-sampah-PILAH/pilah-be/commit/bf3a529), [`f4b663d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f4b663d), [`df45397`](https://github.com/bank-sampah-PILAH/pilah-be/commit/df45397) |
| **A07 Identification and Authentication Failures** | A role change answers with a new session, so new tokens carry the new role | The token's `role` claim is checked after the switch | [`a23ba21`](https://github.com/bank-sampah-PILAH/pilah-be/commit/a23ba21), [`13c1a44`](https://github.com/bank-sampah-PILAH/pilah-be/commit/13c1a44) |
| **A09 Security Logging and Monitoring Failures** | Every role change is written to `user_role_change_log` (account, from, to, when) in the same transaction | One row per real change, none for a refusal or a re-pick | [`62e79e1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/62e79e1), [`2c591c5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2c591c5) |

## What review changed

- **The A04 guard was incomplete, and is now fixed.** Tristan's P1 showed that a registration whose role check ran *before* the role change could still link a bank afterwards. The fix ([`df45397`](https://github.com/bank-sampah-PILAH/pilah-be/commit/df45397)) makes every writer lock the account row; `accept_invite` turned out to have the same gap and got the same fix ([details](team-development-management.md#reviews-received-on-137)).
- **The A07 guard is about new tokens only.** The old access token (24 h) and refresh token (30 d) still carry the old role. Pascal noted it's harmless today, because nothing reads a role from the token. My PR description had overclaimed it, and now states the limit. Blacklisting the old refresh token is offered as a follow-up.
