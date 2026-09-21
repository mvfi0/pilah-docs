# Sprint 1 — Plan

| Item | Detail |
|---|---|
| Dates | 15 Sep → 1 Oct 2026 |
| UAT | 29 Sep 2026 |
| Sprint Review | 1 Oct 2026 |
| Sprint Goal | A pengurus can record a pencairan for a nasabah, with the saldo and its history staying correct. |

## Committed Backlog

| Linear | Title | Repo | Estimate | Plan |
|---|---|---|---|---|
| PIL-176 | Pencatatan pencairan untuk pengurus | be + mobile | 3 pts (Linear shows 0) | [Task plan](tasks/PIL-176-pencatatan-pencairan-plan.md) |

## Approach

Backend first, then mobile, because the mobile form depends on the API contract.

1. **Backend** — `Pencairan` model and migration, an atomic service that locks the nasabah and saldo rows, then the endpoints. Fix the two places that compute a running balance from setoran alone, since they would otherwise overstate the saldo after a pencairan.
2. **Mobile** — scaffold the feature, data layer and cubit, then the form, confirmation and success sheet.
3. Merge backend first, deploy to staging, then merge mobile.

### Dependencies

| On | Why it matters |
|---|---|
| PIL-152 (Tristan) | Added `Nasabah.user` and the role hierarchy. Merged into `staging` on 20 Sep; `Nasabah` stays the per-bank membership, so the pencairan foreign key is unaffected. |
| PIL-188 (Heraldo) | Added an `0011_` migration from the same parent as mine; #19 was stacked on it and renumbered to `0012`. **#18 merged 21 Sep**; #19 retargeted to `staging` on 22 Sep. |
| PIL-168 (Twentism, #22) | Sets the money rule: whole rupiah, rounded down. Pencairan follows it inline for now; swap to `bulatkan_rupiah` once #22 merges. Expect a small `api/tests.py` conflict with #19. |
| PIL-222 (unassigned) | CPBI-10 is only done once riwayat works, and nobody owns it yet. |

### Risks

| Risk | Mitigation |
|---|---|
| Saldo history wrong after a pencairan | Shared `BalanceService.saldo_at` plus regression tests for both the API and the Excel export |
| #19 blocked behind #18 | Resolved — #18 merged 21 Sep; #19 retargeted to `staging` on 22 Sep and mergeable |
| Mobile squeezed by the three lost backend days | Backend was compressed into 20 Sep, so the mobile dates are unchanged |
| PIL-222 unowned, so CPBI-10 cannot close | Raise it with the team; the API is built so PIL-222 can reuse it |

## Definition of Done

- [x] Acceptance criteria met (backend)
- [x] Tests written and passing (backend — 68 tests, 90% overall and 100% of new code, CI green)
- [ ] PR reviewed and merged
- [ ] Deployed / demoable for UAT
