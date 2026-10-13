# Team Development Management

!!! success "Competency level: 3"
    A detailed review of Pascal's PIL-300 merge request, with three inline findings that each carry a feasible fix: a migration collision between two stacks, a validation error under the wrong field, and a database-level idempotency constraint from the SDS. Also: Pascal's scope claim on Heraldo's refactor verified against git history, and Gabriel's review of my own MR answered with a new test that proves his point.

## Review given: Pascal's [pilah-be #84](https://github.com/bank-sampah-PILAH/pilah-be/pull/84) (PIL-300), 9 Oct

PIL-300 confirms a draft pencairan into saldo. It builds on the `PencairanService` I wrote for PIL-176/230, so I reviewed it with a focus on the ledger.

[Review](https://github.com/bank-sampah-PILAH/pilah-be/pull/84#pullrequestreview-5467271780) · inline: [migration](https://github.com/bank-sampah-PILAH/pilah-be/pull/84#discussion_r4227849312), [edit guard](https://github.com/bank-sampah-PILAH/pilah-be/pull/84#discussion_r4227849326), [idempotency](https://github.com/bank-sampah-PILAH/pilah-be/pull/84#discussion_r4227849333)

| Finding | Why it matters | Suggested fix |
|---|---|---|
| **Migration collision.** Both #84's stack and my #79 add a `0020` and a `0021` on top of `0019`. | Whichever merges second leaves two leaf nodes, and `migrate` stops with *Conflicting migrations detected*. That's a broken deploy if nobody notices before merge. | An empty merge migration (`makemigrations --merge`) in whichever branch merges second; agree the order with the lead. I offered to write it if #79 goes second. |
| **Error under the wrong field.** Changing only the `tanggal` of a pencairan with potongan is rejected under the `nominal` key. | The app shows the error on a field the user didn't touch. | Key the error by the field that changed, or use `non_field_errors`; add a test for the tanggal-only change. |
| **Idempotency only in the app** (SDS 7.1.4, BR-04). A second confirmation is stopped by the draft row lock and its status check. | The SDS puts the guarantee in the database, so a future code path can't double-debit. | A partial `UniqueConstraint(draft, nasabah)` on `Pencairan`, mirroring `draft_item_nasabah_unik`. It's cheap while the migration is unmerged. |

The review also names what works, so it reads as a review and not a list of complaints:

- rows locked in id order, so confirmations can't deadlock;
- every item re-checked against the current saldo, with all failures reported before anything is written;
- one shared debit path;
- per-item rounding of potongan;
- a failure-halfway test using a mocked `create`.

**One suspicion checked and dropped.** I suspected two items for the same nasabah could each pass the saldo check and together overdraw. Reading the draft model in #82 showed a unique `(draft, nasabah)` constraint, so it can't happen, and it isn't in the review.

**Coordination.** The review also points out that #84 and my [#89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89) both change the same rounding line, and says how the second to merge should resolve it.

## Verification on Heraldo's [pilah-be #64](https://github.com/bank-sampah-PILAH/pilah-be/pull/64), 2 Oct

Pascal's review of #64 claimed the #50 files (`scripts/scrub-prod-dump.py`, `db/fixtures/prod-anonymized.sql`, `.github/workflows/migration-prod.yml`) were missing, and tagged me. Before agreeing, I checked it against the history rather than the PR text:

- #50 was merged at `864ba42` and reverted five minutes later at `36a68d9`.
- #64 branches from after the revert and never re-applies it.

The [comment](https://github.com/bank-sampah-PILAH/pilah-be/pull/64#issuecomment-5950650947) confirms the claim with those links, gives Heraldo two options (revert the revert, or correct the description), and flags that the description's list of contexts didn't match the branch.

## Review received and answered: Gabriel on [pilah-be #89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89), 8–9 Oct

Gabriel ([review](https://github.com/bank-sampah-PILAH/pilah-be/pull/89#pullrequestreview-5455262911)) pointed out that my new test couldn't tell rounding per pencairan from rounding once at the end. He noted it only matters if setoran can carry sen.

I checked that first: PILAH 1.0 transaksi *can* carry sen (`test_saldo_riwayat_ikut_dibulatkan`). So the point stood, and I added his scenario as a test ([`3c806e5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3c806e5)). The test fails if the rounding is moved out of the loop. I also trimmed the comment he flagged ([`29dc7e7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/29dc7e7)) and [replied](https://github.com/bank-sampah-PILAH/pilah-be/pull/89#issuecomment-6076869250) with both commits.

## Keeping a promise from an earlier review

During the PIL-176 review I promised Heraldo the inline rounding would move to `kalkulasi.bulatkan_rupiah` once #22 landed. #89 does it, and I [replied in that thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4215462955) with the PR, both lines and the new test, so the thread closes with the follow-up linked.
