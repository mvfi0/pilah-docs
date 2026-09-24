# Team Development Management

!!! success "Competency level: 2"
    Answered eight review findings across three merge requests, each verified before being accepted and replied to inside its own thread.

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

## To do

- Give reviews on other people's merge requests this week; only one was given in [week 1](../../review/part-b/team-development-management.md) (pilah-be #22).
