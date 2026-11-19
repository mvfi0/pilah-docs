# Team Development Management

!!! warning "Competency level: 1"
    **No review of a teammate's merge request this week (4 – 10 Nov).** The rubric scores reviewing other members' MRs, so I'm not claiming above level 1 here. The reviews I gave resumed on 11 Nov: see [Sprint 3 Week 3](../../review-sprint-3-week-3/part-b/team-development-management.md).

    What this week does have, on the team side of reviewing:

    - **A cross-PR heads-up** to Rifqi's [#212](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/212). It carries the same Hapus dialog Heraldo found a bug in on my #193, so I told him about the fix, with the commits and the merge that brings it in.
    - **Six findings received on #145 and #193,** from Heraldo and Scallss. Each was checked against the code, fixed test-first, and answered in its own thread with the fix linked.
    - **The UAT with the Pengurus** (6 Nov), run with the team from the PIL-418 materials I prepared.

## Cross-PR heads-up: Rifqi's [pilah-mobile #212](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/212), 4 Nov

Rifqi's PR (PIL-429, bulk void) carries my single Hapus dialog, `batalkan_setoran_dialog.dart`. Heraldo's review of #193 found that this dialog could be closed by a barrier tap or back while the void was in flight, then skipped the feed refresh. [My comment](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/212#issuecomment-6628744737) links:

- the fix, [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b), and its tests, [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07);
- the thread with the details;
- the merge commit, `90ad319d`, that brings it into `feature/pil-429`.

It also says the change only touches that dialog and its flow test, so it shouldn't collide with his bulk dialog.

This is not a review of #212, so it isn't counted as one.

## Reviews received

| Reviewer | Finding | Checked against the code | Status |
|---|---|---|---|
| Heraldo, [on #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#discussion_r4456211899) | Both seed commands rebuild the saldo from raw sums, voided setoran included | **Correct.** Each red test re-seeds after a void and fails as he described. No other place outside the tests sums setoran without `tercatat()` | **Fixed**, red [`743ed1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/743ed1c3) → green [`abcafa3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/abcafa30). [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#discussion_r4466534858) |
| Heraldo, [🟠 on #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4456406981) | The dialog can be dismissed while the void is in flight | **Correct**: `barrierDismissible` defaults to true, and the route had no `PopScope` | **Fixed**, red [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07) → green [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b). [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4466535388) |
| Heraldo, [🟠 on #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4456408828) | A void that succeeds after a dismissal skips the clear and the reload | **Correct**, and writing its test found a third bug: an answer during the exit animation closed the Riwayat page | **Fixed** in the same pair. [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4466536023) |
| Scallss, [🟡 on #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4467432062) | A void leaves the dashboard, recent activity and nasabah list stale | **Correct**: #212's bulk void already reloads them | **Fixed**, red [`6979612`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/69796129) → green [`be7b6d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/be7b6d06). Edit's same gap left as an agreed follow-up. [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4468196683) |
| Scallss, [🔵 on #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4467432084) | A bare `12` instead of `AppSpacing.md` | **Correct** (DESIGN.md) | **Fixed**, [`b815354`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b815354f). [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4468197124) |

**Not answered before the merge.** On 4 Nov Heraldo approved #145 at 20:50 and #193 at 20:54, each with two new non-blocking points. Scallss merged both at 21:10, after my session had ended, so none of the four got a reply:

- 🟡 [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#discussion_r4468324019): `0029` shared with #137 and #132. The coordination was already flagged on 31 Oct; #137 renumbered to 0038 when it merged `staging` (13 Nov).
- 🔵 [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#discussion_r4468324482): the WhatsApp receipt is sent inside the row lock. He marked it deliberate, with "no change requested".
- 🔵 [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4468384271): `_hapus` itself doesn't check `_saving`. Two taps in the same frame could send two POSTs. The second POST would get a 409 (a voided setoran is final), so no money moves twice, but a one-line guard is still a fair follow-up.
- 🔵 [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4468384728): bare spacing numbers in the detail sheet.

**Received on 9 Nov, answered next week:** Heraldo's change requests on [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) (a stale docstring) and [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) (one leftover string, two consistency gaps). They were fixed test-first on 11 Nov, in [Sprint 3 Week 3](../../review-sprint-3-week-3/part-b/team-development-management.md).

## Working with the team

- **The UAT with the Pengurus** (6 Nov, 09:00–11:00): ibu-ibu pengurus of the partner bank sampah, run from the task script and findings form I prepared for PIL-418 in Sprint 3 Week 1. Two of its findings became this week's PIL-481 and PIL-480.
- **Merging after approval:** I merged #196 myself after Heraldo's and Scallss's approvals, under the team's rule that an approved PR may be merged by its author.
