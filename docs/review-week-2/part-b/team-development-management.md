# Team Development Management

!!! success "Competency level: 2"
    Answered twelve review findings across four merge requests, each verified before being accepted and replied to inside its own thread, and coordinated merge conflicts with nine other open PRs.

## Reviews received and answered — 23–24 Sep

Heraldo reviewed all three open PRs. Each finding was checked against the code first, then fixed test-first and answered in the thread it was raised in, naming the fix commit.

| PR | Finding | Reply |
|---|---|---|
| [#26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | Server nominal error stayed on the field after the value changed | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26#discussion_r4085517879) |
| [#26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | Private 422 parser duplicating `NetworkException.fieldError` | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26#discussion_r4085518062) |
| [#26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | Raw enum name in the confirmation dialog | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26#discussion_r4085518278) |
| [#27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | Out-of-order responses could show rows for a deselected filter | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27#discussion_r4085520383) |
| [#27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | A 1-character search was sent and silently ignored by the API | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27#discussion_r4085520582) |
| [#27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) | An active search survived a periode change with no indicator | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27#discussion_r4085520795) |
| [#32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32) | Short search: fix belongs on the mobile side | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/32#discussion_r4085521025) |
| [#32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32) | Unrecognised `periode` silently ignored | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/32#discussion_r4085521420) |

## Cross-PR coordination

Two findings crossed repository boundaries: the reviewer raised the 2-character search rule on the backend PR, but the fix belonged in the mobile client, which was sending the short value. The change went to [pilah-mobile #27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27) and the rule was documented in the backend README, so the contract is written down where the next client will read it rather than left in a review thread.

## Reviews received and answered — 26 Sep

Tristan (lead) reviewed [#19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19). All four findings held up when checked against the code; each was fixed test-first and answered where it was raised, then the threads were resolved as the reviewers had asked.

| Finding | Reply |
|---|---|
| Nasabah could not read their payout history | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4111612893) |
| A backdated payout was checked against today's saldo | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4111612938) |
| Saldo history ignored the rounding adjustment | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4111612993) |
| Default Django admin could write pencairan past the service | [comment](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#issuecomment-5846946874) (no inline thread) |

For the backdating finding the reviewer offered two fixes. I brought the trade-off to a decision rather than picking silently: validating at the payout date would leave later receipts stale until PIL-230, while rejecting dates before the nasabah's last activity keeps every snapshot exact. The second was chosen.

## Coordinating conflicts across the team — 26 Sep

After updating #19, I test-merged it against every open backend PR and left a heads-up on the nine that will conflict, each naming the exact files, the migration leaves involved and how to resolve them:

- [#22](https://github.com/bank-sampah-PILAH/pilah-be/pull/22#issuecomment-5846920437) (Gabriel) — `api/tests.py` append conflict, and confirming I will adopt his `bulatkan_rupiah` once it merges.
- [#26](https://github.com/bank-sampah-PILAH/pilah-be/pull/26#issuecomment-5846920660) (Tristan, stack of three) — `0012_jadwalkegiatan` becomes a second migration leaf.
- [#30](https://github.com/bank-sampah-PILAH/pilah-be/pull/30#issuecomment-5846920826) (Pascal) — both PRs define `IsNasabah`, with different meanings.
- [#33](https://github.com/bank-sampah-PILAH/pilah-be/pull/33#issuecomment-5846921039), [#34](https://github.com/bank-sampah-PILAH/pilah-be/pull/34#issuecomment-5846921187), [#37](https://github.com/bank-sampah-PILAH/pilah-be/pull/37#issuecomment-5846921416), [#38](https://github.com/bank-sampah-PILAH/pilah-be/pull/38#issuecomment-5846921713) (alghani46) — a second `0013` merge migration and a near-duplicate `IsActiveNasabah`; I offered to switch #19 to theirs if it lands first.
- [#48](https://github.com/bank-sampah-PILAH/pilah-be/pull/48#issuecomment-5846921976) (Heraldo's modular refactor) — the list of pencairan code that would need to move into the new layout.

## Clarifying requirements with the PO and lead — 25–26 Sep

PIL-230 had no description. I raised the open questions (recompute, backdating limit, reason, what the nasabah sees) in the team channel. The PO and the lead disagreed on one of them: whether nasabah see old versions. I laid out both positions and the scope each implies, the team settled on the PO's version, and I wrote the decisions into the Linear issue so the PRs point to one written source.

## To do

- Give reviews on other people's merge requests this week; only one was given in [week 1](../../review/part-b/team-development-management.md) (pilah-be #22). The conflict heads-ups above are coordination, not code review, so they do not count toward this.
