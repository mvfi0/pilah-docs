# Security

!!! success "Competency level: 3"
    **Level 3: a scan, explained, with a patch plan.** Each new PR this week, #175, #176 and #177, got its own **OWASP ZAP 2.17.0** scan, run one at a time after the first attempt ran out of memory. They ran signed in, against my own local instances, with fresh seeded databases and backends started with an empty environment. Report: [ZAP scans per sub-issue, 17 Nov](../../security/zap-2026-11-17.md).

    - **0 High and no new finding.** Every alert is one already on record, and the report says which.
    - **The 9 Nov finding verified fixed, not assumed:** ZAP sent 965 malformed `nasabah_id` values to `/transaksi` and `/pencairan`. All 965 got 422, none 500, where the 9 Nov scan had 226 500s. The two false High alerts they caused didn't come back.
    - **Every 5xx in the three backend logs read and classified:** the only 500s were the known debug-only browsable-API crash.
    - **A limit reported, not hidden:** `DELETE /device-tokens/` couldn't be actively scanned (ZAP has no GET node for it). Its NUL case is covered by the drive module and #177's tests, and the tooling fix is in the plan.

    **Level 2 is also met by the commits:** five OWASP categories are genuinely guarded, each with a test or a check behind it: **A03, A04, A05, A08 and A09**.

    **My own leak, found and fixed** (13 Nov): two Discord webhooks in my 9 Nov scan evidence were redacted, and the scan script now refuses to finish when it finds a secret.

## The ZAP scans

| PR | Target | What the scan shows |
|---|---|---|
| [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175), PIL-482 | `feature/pil-482` at `b85819a`, database `zap482` | 965 malformed `nasabah_id` → all 422. Another 1,067 422s carried a valid id while ZAP attacked `periode`, `tipe` and the dates. An empty `nasabah_id=` means no filter (200). `/aktivitas`: 487 malformed ids, all 422 as before |
| [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176), waste categories | `fix/waste-categories-tercatat` at `8d1a931`, database `zapwaste` | 1,056 requests on `/dashboard/waste-categories`: 1,003 × 400 (invalid date or range), 50 × 200, 3 × 404. No 5xx. The PR changes which rows count, not the response, so the job here was to show nothing new opened |
| [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177), NUL in a body | `fix/nul-in-request-body` at `7b7841d`, database `zapnul` | The attacks on the real jenis's and nasabah's `PATCH` got 200, 422 or 405, never 500. On `staging` a NUL or a padded duplicate kode in that body is a 500 |

| Earlier finding | Status after this scan |
|---|---|
| 9 Nov 1: malformed `nasabah_id` is a 500 on `/transaksi` | **Fixed by #175**, verified above |
| 9 Nov 2 / 2 Nov 1: a NUL in `search` is a 500 | **Fixed on `staging`** by Scallss's #172 (16 Nov). **#177** fixes the request-body case #172 left open |
| 9 Nov 3: the browsable API crashes on `/aktivitas` | Still open, debug-only; seen again. Patch plan item 2 |
| 26 Oct 3: `/api/docs/` loads CDN scripts without integrity hashes | **Fixed by Gabriel's #174**, merged 17 Nov, which I reviewed and approved ([review](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#pullrequestreview-5925723761)) |
| 26 Oct 2: CSP wildcard directive | Still open |

The patch plan, the method and every alert's explanation are in the [report](../../security/zap-2026-11-17.md).

## My own leak, and what changed (13 Nov)

The 9 Nov scan caught a Django debug page that lists the whole environment of the dev machine, and that environment held two Discord webhooks (`DISCORD_REVIEW_WEBHOOK_URL`, `DISCORD_QA_WEBHOOK_URL`). I had redacted the computer and user names from the evidence, not these, and the report said I had grepped for secrets, which wasn't true for webhooks. GitHub's secret scanning found them, and Discord revoked both.

[`2197468`](https://github.com/mvfi0/pilah-docs/commit/2197468) (pilah-docs):

- **The evidence:** the two PIL-481 files carry `[REDACTED]`, and the JSON stays valid. The other credentials in the dump were already masked by Django. The other reports' evidence is clean.
- **The check:** `tools/zap_scan.py` now refuses to finish on Discord and Slack webhooks, GitHub, Google and Slack tokens, and database URLs with a password, not only bearer tokens and JWTs. I confirmed it flags the original file and none of the current evidence.
- **The cause:** from the 17 Nov scans on, each backend starts with an empty environment (`env -i` plus only the variables it needs), so no secret of the machine can reach a debug page.
- **The record:** the report's false claim is corrected, and the leak is in its "What went wrong" section. The old commit still holds the dead URLs, since history wasn't rewritten.

## OWASP guards in this week's code

| OWASP category | Guard | Test or check | Commits |
|---|---|---|---|
| **A03 Injection** | Untrusted input is validated before it reaches a query: a `nasabah_id` must be a UUID, and a kode or device token can't carry a NUL byte into PostgreSQL | 3 endpoints × 3 malformed ids → 422; a NUL in kode on two edit paths and in the token → 422 | [`5699fff`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5699fffc), [`5c2f7fc`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5c2f7fc2), [`04ab0bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/04ab0bbc), [`d3b1bea`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d3b1beaf), [`1a765f9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1a765f94) |
| **A04 Insecure Design** | Malformed input is a client error, not a crash. A completed profile and a role change can't interleave: profile completion takes the same account lock as every other writer of the invariant | The 422 tests; a two-thread race test on PostgreSQL, and the reverse ordering single-threaded | [`9424d9f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9424d9f2), [`870224d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/870224dc), [`51a631e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/51a631ef) |
| **A05 Security Misconfiguration** | No secret of the machine reaches published evidence: the scan backends run with an empty environment, and the scan fails if a secret pattern appears in its output | The scan script flags the original leaked file and passes the current evidence | [`2197468`](https://github.com/mvfi0/pilah-docs/commit/2197468) (pilah-docs) |
| **A08 Software and Data Integrity Failures** | Every total reads the same counted subset, enforced by a test that reads the source. A padded duplicate kode can no longer slip past the uniqueness check and overwrite another item's kode | The architecture test (fails on any hand-written filter); the padded-duplicate tests on both edit paths | [`b10fffa`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b10fffaa), [`8d1a931`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8d1a9316), [`a56eba9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/a56eba91), [`e7ef617`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e7ef617b) |
| **A09 Security Logging and Monitoring Failures** | The role-change audit trail holds only changes that happened: a role change refused under the lock writes no `UserRoleChangeLog` row | The race harness asserts no log row after a refused change | [`870224d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/870224dc), [`51a631e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/51a631ef) |

**Labels I don't count.** The commits also name:

- **A01:** "the filter still runs inside the bank scope", "the delete stays limited to the caller's tokens". That scoping is unchanged code, and no new test asserts it.
- **A07:** "the logout path that forgets a push token cannot be made to crash". That's a robustness fix more than an authentication control.
- **A02:** in the leak fix. The control there is the A05 one above.

## Security in review

- **Given, on Gabriel's #174** (A08): I recomputed the three Subresource Integrity hashes and showed his test catches a missing one. I also showed that a version bump with stale hashes passes every test, which would ship a blank docs page, and suggested keying the hashes by version. Details are on [Team Development Management](team-development-management.md#review-given-gabriels-pilah-be-174-17-nov).
- **Given, on Gabriel's #169:** the server accepts a pengelola's profile with no birth date and marks it complete, although both PRs say the server requires it. This is a broken business rule rather than an OWASP item, but it's the kind of claim that only a request to the server can check.
- **Received, on my #137:** Tristan found a fifth writer of the role-lock invariant. It's fixed, with a race test that failed before the fix.
