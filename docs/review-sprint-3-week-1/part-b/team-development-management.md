# Team Development Management

!!! success "Competency level: 3"
    Two detailed reviews of teammates' merge requests (2 Nov). Each was checked out and run before commenting, and each point carries a concrete, feasible change:

    - **Rifqi's pilah-be #144** (customer ordering and list hardening): 87 tests run on Postgres 16, and a scratch test **showed** that a database bug in the list would surface as a "temporary" 503 with no traceback anywhere. The review includes the fix, a question on the throttle backed by where else the endpoint is called, and a schema nit.
    - **Gabriel's pilah-mobile #202** (removing the Pengumuman entry points): 389 tests run, and every route into Pengumuman grepped. The review found that the "still restorable" claim had lost its route guards and their two tests, with a design that keeps them. It also answered the PR's own open question from the CPBI.

    The other side of reviewing: **seven findings from Tristan, Scallss and Heraldo on my #137 and #174**. Each was checked against the code, fixed test-first, and answered in its own thread with the fix linked.

    Coordination: a migration-number clash between #137 and #145, which Git can't see, was flagged on both PRs before either merged.

## Review given: Rifqi's [pilah-be #144](https://github.com/bank-sampah-PILAH/pilah-be/pull/144), 2 Nov

The PR adds `?urutan=` ordering to the customer list (PIL-442) and hardens the list endpoint:

- validated, bounded query inputs;
- duplicate-key rejection;
- a per-user throttle;
- `private, no-store` responses;
- sanitized rejection logs.

[Review](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#pullrequestreview-5737653085)

**Verified before commenting,** at [`774cb4a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/774cb4a66465b6e928d7d1026a42438a549fc0be):

- checked out and ran `apps.nasabah` on Postgres 16: 87 tests, all pass;
- confirmed the tie-breaker is safe: `nomor` is unique per bank (`unique_together (bank_sampah, nomor)`), so pages can't overlap;
- traced every caller of `GET /api/v1/nasabah` in the app: the Nasabah page **and** the setoran picker, both with a 300 ms debounce;
- wrote a throwaway test (never committed) that makes `get_queryset` raise `ProgrammingError`, then captured every log record.

```
STATUS 503 {'error': 'Daftar nasabah sementara tidak tersedia. Silakan coba lagi.'}
LOG apps.nasabah.security WARNING Customer list rejected: status=503  exc_info=False
LOG django.request ERROR Service Unavailable: /api/v1/nasabah        exc_info=False
```

| Point | Why it matters | Suggestion |
|---|---|---|
| [**1. A query bug becomes a 503 with no traceback**](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#discussion_r4443247233) | On `staging`, the same bug is a 500 that Django logs with its traceback. Here it reads as a temporary outage that can't be diagnosed, which undercuts the PR's own A09 goal | Keep the 503 only for `OperationalError`/`InterfaceError`, log the exception with `exc_info`, and let real bugs stay 500s. Code given, plus an `assertLogs` test to pin it |
| [**2. The 120/min budget is shared with the setoran picker**](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#discussion_r4443247245) | The core setoran flow calls the same endpoint, and a Pengurus account shared across devices at a weighing session shares one budget | Calibrate against the per-user request rate from Tristan's PIL-444 load run, check the picker's 429 message, or give the picker its own scope |
| [**3. Nit: `urutan` choices only in prose**](https://github.com/bank-sampah-PILAH/pilah-be/pull/144#discussion_r4443247255) | Swagger and the mobile PR can't see the allowed values | `enum=[...]` on the `OpenApiParameter`, keeping the deliberate fallback |

It was posted as a comment, with point 1 marked as the one to fix before merging.

## Review given: Gabriel's [pilah-mobile #202](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202), 2 Nov

The PR takes the Pengumuman entry points from "disabled but visible" (Tray's #158) to not drawn at all, as CPBI-31's "tidak ada menu mati" asks. It keeps the old URLs as redirects and leaves `lib/features/pengumuman/` untouched so the feature can be restored.

[Review](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#pullrequestreview-5737765335)

**Verified before commenting,** at [`6ad6ba2`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6ad6ba2a541560e325786ae19a02aa9e7d108d2f):

- checked out and ran every suite the PR touches, plus all of `test/features/pengumuman`: 389 pass;
- grepped `lib/` for any remaining way in (Profil, notifications, the shell): none. Only the DI registration and the session-reset cleanup remain, which is right for a restorable feature;
- compared the deleted route builders and tests with `staging`.

| Point | Why it matters | Suggestion |
|---|---|---|
| [**1. The restore path lost its guards**](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#discussion_r4443335093) | The PR rests "still restorable" on the feature's own tests. The route-level guards were deleted, though: the `state.extra` fallbacks for stale links, and the `keanggotaan_id` a nasabah with two banks needs. So were the two tests that pinned them | Keep the four original routes as an unregistered `pengumumanRoutes` list in the feature, derive the redirect paths from it, and move the two tests to mount it. Reopening becomes one line. Code given |
| [**2. The Nasabah question the PR raised**](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#discussion_r4443335120) | The description flags removing the Nasabah Beranda section as beyond the ticket | CPBI-31's criteria say "Fitur pengumuman tidak tampil di aplikasi" for everyone, so it's in scope. Quote it to settle it |
| [Positive: the redirect target](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/202#discussion_r4443335130) | Redirecting through the dashboard re-enters the role redirect, so a nasabah lands on their own home | — |

I also pointed out the same dead-control pattern in the greyed "Pencairan" menu item, which belongs to PIL-434, for whoever takes that issue.

## Reviews received

| Reviewer | Finding | Checked against the code | Status (2 Nov) |
|---|---|---|---|
| Tristan, [P1 on #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4431159076) | Google login links a pengurus-entered membership without the account lock the other writers now take | **Correct.** My race test covered three writers. This fourth one runs on every Google login | **Fixed**, red [`c428c32`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c428c32) → green [`d19cb8d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d19cb8d). [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4443157430) |
| Heraldo, [Medium on #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4434504589) | The same gap, with both orderings: a stranded pengelola, and a misleading 401 from `Nasabah.clean` | **Correct, both reproduced** by the red tests | **Fixed** in the same pair; a refactor [`e077084`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e077084) followed. [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4443157975) |
| Heraldo, [nit on #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4434504808) | `lock_account` reads the row twice | **Correct**, measured: two queries, now one | **Fixed**, [`7c7c1f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7c7c1f3). [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4443158308) |
| Scallss, [nit on #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4422171706) | Re-picking the same role drops the typed draft | **Correct**; his scratch test became a permanent one | **Fixed**, red [`26dce38`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26dce385) → green [`3d0a81b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3d0a81b3). [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4443162727) |
| Tristan, [P2 on #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4431159084) | A real role change leaves the old input in the mounted form | **Correct**: clearing the provider draft didn't reach the controllers | **Fixed** in the same pair, with a test on the fields themselves. [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4443163200) |
| Tristan, [P2 on #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4431159086) | Raw spacing values instead of `AppSpacing` | **Correct** (DESIGN.md §2) | **Fixed**, [`6eef5a4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6eef5a43). [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4443163753) |
| Heraldo, [low on #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4434501795) | The same draft issue as Scallss's, plus the remount case | **Correct** | **Fixed** in the same pair. [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4443164072) |

Two of these were found by more than one reviewer, which is why seven threads map to five fixes. I credited the reviewers' suggested approaches in the replies: the lock on the claim, and gating the draft clearing on the role.

## Asking the team

- **#145, #193 and #196:** no review yet. They go through the team's `ask-for-review` skill.
- **#137 and #174:** waiting for the reviewers to re-check after the second round.
