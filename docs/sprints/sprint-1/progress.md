# Sprint 1 — Progress

## Status

| Linear | Title | Status | PR | Notes |
|---|---|---|---|---|
| PIL-176 | Pencatatan pencairan untuk pengurus | Backend in review | [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | CI green, review findings fixed. #18 merged; #19 needs retargeting to `staging`. Mobile not started. |

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

### 2026-09-21

- **Done:**
  - Heraldo reviewed #19 with three findings, all fixed test-first and answered in their threads:
    1. **Membership gate (🟠)** — pencairan accepted any active nasabah, but setoran now also requires `status=APPROVED`. A pending or rejected nasabah could be paid out. Fixed to use the same filter.
    2. **Legacy sen (🟡)** — [#22](https://github.com/bank-sampah-PILAH/pilah-be/pull/22) rounds saldo down to whole rupiah on setoran; pencairan kept the sen. Now pencairan rounds down the same way, written inline because `api/kalkulasi.py` only exists on #22.
    3. **Same-instant ordering (🟡)** — a setoran and pencairan with the same `tanggal` were ordered inconsistently; the export sorted them by random UUID (a test against the old sort passed only 6/10 runs). Now the setoran always comes first, in both places.
  - Rebased onto Heraldo's latest commit (`3b903f1`) before fixing; no new migrations, so `0012_pencairan` still holds.
  - [#18](https://github.com/bank-sampah-PILAH/pilah-be/pull/18) merged into `staging`. Checked that #19 merges into `staging` cleanly.
  - Measured coverage on the new code alone: 99.1% (see [Testing & QA](../../testing-qa.md)).
- **Next:** Retarget #19 to `staging`; get Heraldo's re-review; start mobile.
- **Blockers:** None hard. PIL-222 is still unowned.

### 2026-09-22

- **Plan:** Retarget #19 to `staging` (GitHub did not do it automatically because #18's branch still exists), then start the mobile side of PIL-176.
- **Follow-up owed:** after #22 merges, replace the inline rounding with `kalkulasi.bulatkan_rupiah` — promised publicly in the review thread.

## Deviations from the plan

| Planned | Actual | Why |
|---|---|---|
| Backend across 17, 18, 21 Sep | Done in one day, 20 Sep | Blocked until access and answers were sorted; compressed to protect the mobile dates |
| Branch from `staging`, expect a migration renumber later | Stacked on #18 and renumbered now | #18 hit the same migration number first; stacking resolves it immediately |
| `Pencairan` has no `status` in Sprint 1 | `status` ships with the value `tercatat` | PO listed status among the fields both roles must see |
| Nasabah-side reading deferred to Sprint 2 | In Sprint 1 scope, probably PIL-222 | PO confirmed pencairan appears in the nasabah activity history |
| Saldo stays exact to the sen | Saldo rounded down to whole rupiah after a pencairan | Matches the team money rule introduced in #22; review finding 2 |
| Any active nasabah can be paid out | Only `APPROVED` members of the bank | #18 added membership approval; review finding 1 |
