# Programming

**Rubric (B2 · Best practice, OO, Data Structure, Design Pattern, SOLID):** commit link plus the principle applied, in the week's comment.

| Level | Requirement |
|---|---|
| 2 | No special attention to principles, but no violations |
| 3 | Applies standard principles and can show them in that week's code |
| 4 | Advanced principles that account for further development or maintenance; testable and demonstrable |

**Proposed level: 3**

## Week of 15–21 Sep

### Single Responsibility + DRY: `BalanceService` — [`5447710`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5447710)

Two places computed a running saldo by summing setoran only: `TransactionDetailSerializer.get_saldo_setelah_transaksi` and the Excel export. Instead of fixing the formula twice, the rule "setoran added, pencairan subtracted" lives in one class, `BalanceService.saldo_at`, used by both. When review finding 3 later changed the ordering rule, it was fixed in one place ([`765f90f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/765f90f)).

### Service layer: `PencairanService` — [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b)

The business rule (lock the nasabah and saldo rows, check the saldo, record, deduct) sits in `PencairanService.create_pencairan`, not in the view. The view only validates input and returns a response, following the existing `TransactionService.create_setoran` pattern.

### Open/Closed in practice: a separate `Pencairan` model — [`fbab07b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fbab07b)

Adding a `PENCAIRAN` type to `Transaksi` with a negative value would have forced changes in every consumer that assumes a transaksi has items: the list serializer, export, dashboard and WhatsApp notifier. A new model extends the system without modifying them. The trade-off is documented in the [PR description](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) and the [task plan](../../sprints/sprint-1/tasks/PIL-176-pencatatan-pencairan-plan.md).

### Consistency with existing rules — [`49cd153`](https://github.com/bank-sampah-PILAH/pilah-be/commit/49cd153)

Pencairan uses the same membership filter as setoran (`is_active=True, status=APPROVED`), so both money flows apply one rule.

## Week of 22–28 Sep

### Removing dead code — [`bd38dc6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/bd38dc6)

`PencairanViewSet.list` had an unpaginated fallback that could never run, because pagination is configured globally. Removed; the list test stayed green.
