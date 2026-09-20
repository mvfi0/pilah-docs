# Sprint 1 — Progress

## Status

| Linear | Title | Status | PR | Notes |
|---|---|---|---|---|
| PIL-176 | Pencatatan pencairan untuk pengurus | Backend in review | [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | CI green. Stacked on #18; mobile not started. |

## Daily Log

### 2026-09-16

- **Done:** Drafted the [task plan](tasks/PIL-176-pencatatan-pencairan-plan.md) — scope, data model, API contract, test list, and 7 open questions.
- **Next:** Get the open questions answered; fix repository access.
- **Blockers:** `git fetch` failing; questions unanswered, so coding could not start.

### 2026-09-17 – 2026-09-18

- **Done:** Nothing on PIL-176.
- **Blockers:** Same two. Backend work slipped by three days.

### 2026-09-19

- **Done:** PO answered all open questions; tech lead confirmed Q3–Q5 defaults and that transfer handling is out of scope (no payment gateway).
- **Next:** Fix access, then start the backend.

### 2026-09-20

- **Done:**
  - Fixed the fetch problem — it was a missing GitHub entry in `~/.ssh/known_hosts`, not a permissions issue. Verified the host key fingerprint against the one GitHub publishes.
  - Recorded the answers in the task plan; two changed the design (a `status` field, and nasabah-side reading arriving in Sprint 1).
  - Caught up the missed backend days: model, migration, atomic service, API, saldo-history fix, admin, README — TDD throughout, 8 new tests (39 → 47).
  - Opened [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) and self-assigned it. CI passed in 2m23s.
  - Resolved a migration clash with [#18](https://github.com/bank-sampah-PILAH/pilah-be/pull/18): both branches added an `0011_` migration from the same parent. Rebased onto #18 and renumbered to `0012_pencairan`, so the graph stays linear and no merge migration is needed.
  - Verified a from-scratch `migrate` on an empty database applies `0010 → 0011 → 0012` cleanly.
- **Next:** Get #19 reviewed; start the mobile side.
- **Blockers:** #19 cannot merge until #18 does. No reviewer assigned yet, and PIL-222 still has no owner.

## Deviations from the plan

| Planned | Actual | Why |
|---|---|---|
| Backend across 17, 18, 21 Sep | Done in one day, 20 Sep | Blocked until access and answers were sorted; compressed to protect the mobile dates |
| Branch from `staging`, expect a migration renumber later | Stacked on #18 and renumbered now | #18 hit the same migration number first; stacking resolves it immediately |
| `Pencairan` has no `status` in Sprint 1 | `status` ships with the value `tercatat` | PO listed status among the fields both roles must see |
| Nasabah-side reading deferred to Sprint 2 | In Sprint 1 scope, probably PIL-222 | PO confirmed pencairan appears in the nasabah activity history |
