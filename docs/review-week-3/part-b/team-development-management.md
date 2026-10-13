# Team Development Management

!!! success "Competency level: 3"
    A detailed review of Pascal's PIL-300 merge request, with three inline findings that each carry a feasible fix: a migration collision between two stacks, a validation error under the wrong field, and a database-level idempotency constraint from the SDS. Also: Pascal's scope claim on Heraldo's refactor verified against git history. Gabriel's review of my MR was answered with a new test that proves his point. Tristan's review of four of my MRs (8 findings) was verified, fixed test-first and answered in every thread.

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

## Review received and answered: Tristan on #79, #62, #73 and #74, 11–12 Oct

Tristan reviewed four of my MRs on 11 Oct (and approved #92). I checked every finding against the code before changing anything; all 8 held up. Each fix went in test-first, and each thread got a reply with the commits.

| MR | Finding | What I did | Reply |
|---|---|---|---|
| #79 | [The seed writes price versions itself](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257376), outside the approved write paths | Routed it through `catat_harga` ([`dc29a68`](https://github.com/bank-sampah-PILAH/pilah-be/commit/dc29a68)) | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247271876) |
| #79 | [Rerunning the seed reprices historical setoran](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257381) at today's rate | Red test showed 3,500 becoming 99,999. Each setoran is now priced at its own date ([`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) → [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f)) | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247272237) |
| #79 | [The filter allow-list is outside PIL-304](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257383) | Reverted here and re-applied unchanged as [#96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96), stacked on #92 | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247272434) |
| #62 | [A partial save is reported as a failure](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4242257026) | The sheet now says the other fields saved and the price didn't, and stays open; retrying is safe ([`5a80375`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5a80375) → [`f1ea8d9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f1ea8d9)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4247489293) |
| #62 | [An older list reload can overwrite a newer one](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4242257029) | Reloads are numbered and a stale answer is dropped ([`ece524b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ece524b) → [`bd21f70`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bd21f70)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4247489545) |
| #73 | [`toInt()` drops a price's sen](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4242248044) | Prices are held in sen and parsed without `double` ([`de18bfc`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/de18bfc) → [`4226ca5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4226ca5)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4258201362) |
| #73 | [Versions past the first 100 disappear](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4242248049) | The history follows `next` to the last page ([`9ad13dd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9ad13dd) → [`510f02a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/510f02a)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4258201663) |
| #74 | [The Sonar exclusion still hides the DI graph](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74#discussion_r4242254526), plus a merge conflict | Removed the exclusion ([`26fcf40`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26fcf40)). Merged `staging` and took Tristan's identical bloc fix from #71 | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74#discussion_r4258097139), [comment](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74#issuecomment-6144632095) |

Two findings had a cheaper but worse fix that I chose not to take, and the replies say why:

- **#62, the partial save.** Making the two writes atomic would need a backend endpoint that takes both. The API keeps the price separate on purpose, so that every change is a version. So the fix makes the state explicit and the retry safe instead.
- **#79, the filter split.** Force-pushing #79 would have broken last week's evidence links. A revert plus `cherry-pick -x` keeps the history intact.

## Raising a team-wide problem: CI-built apps would crash on launch, 11 Oct

While covering the generated dependency graph, I found that the graph CI and CD build could not create `AuthenticationBloc`, which `app.dart` creates at start-up. It had been that way since PIL-334. The next staging APK or web build would have crashed on launch; local `flutter run` hid it.

- **Reproduced first.** I regenerated the graph, built the bloc from it in a test, and got the exact error before reporting it.
- **Asked before touching shared code.** The fix touches the team's CI and a teammate's code, so I asked how to land it, then opened [#74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) against `staging`.
- **Outcome.** The same one-line fix also reached `staging` through Tristan's #71. #74 kept what was still new: a test that builds every registration, so this class of crash fails CI instead of the app.

## Keeping a promise from an earlier review

During the PIL-176 review I promised Heraldo the inline rounding would move to `kalkulasi.bulatkan_rupiah` once #22 landed. #89 does it, and I [replied in that thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4215462955) with the PR, both lines and the new test, so the thread closes with the follow-up linked.
