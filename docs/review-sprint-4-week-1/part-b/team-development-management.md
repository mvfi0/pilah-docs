# Team Development Management

!!! warning "Competency level: 1"
    **I didn't review a teammate's merge request this week** (18 – 24 Nov). The rubric scores this competency on reviews given to other members' MRs, so the week is claimed at the lowest level. The last reviews I gave were Gabriel's PIL-478 pair and his #174, in [Sprint 3 Week 3](../../review-sprint-3-week-3/part-b/team-development-management.md).

    What did happen is the other side of review: **seven review threads on my own MRs**, from Gabriel and Heraldo. Each was checked against the code and the issue's scope, then answered in place with the reason. It's recorded below for completeness, but the rubric doesn't count it.

## Review threads received and answered

| MR | Reviewer | Finding | Answer |
|---|---|---|---|
| [pilah-be #175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) | Gabriel (17 Nov, non-blocking) | `validasi_uuid`'s own test file doesn't cover another `kunci` or the `UUID` return type | Left for the first caller with a different key: every caller today passes `kunci="nasabah_id"`, and the HTTP tests cover it end to end ([reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/175#issuecomment-6984421991), 18 Nov) |
| [pilah-be #176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) | Gabriel (17 Nov, non-blocking) | The bank, type and date selection in `waste_categories` is written twice | Agreed, with permalinks to both copies. The duplication predates the PR, which only changes how the status rule is read, so extracting `_setoran_tercatat` is a separate change ([reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/176#issuecomment-6984422988), 18 Nov) |
| [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) | Heraldo ([approval](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276#pullrequestreview-6016382571), 23 Nov), five follow-ups he called non-blocking | 1. a failed silent reload shows the full error screen; 2. two read paths and two `NasabahMembershipEntity` classes; 3. a failed membership load leaves `joinedBanks` empty; 4. no in-flight guard on "Ajukan bank baru"; 5. test gaps for 1 and 3 | All five left out of the PR, each with the reason: none can create a wrong record, because the server refuses a duplicate application with 400 before any row is written, which the 23 Nov ZAP scan confirmed with 224 attacks. Each was assigned to where it fits as a follow-up ([reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276#issuecomment-7098016848), 23 Nov) |

The rule applied to all three is one I set on 12 Nov: comments after an approval are checked against the issue's scope. If they're out of scope and not needed for correctness, the PR is merged and the reason given in the thread. If they're in scope or a real bug, they're fixed first.

## Reviews of my MRs this week

| MR | Reviewer | Verdict |
|---|---|---|
| [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) | Heraldo, 19 Nov | [Approved](https://github.com/bank-sampah-PILAH/pilah-be/pull/185#pullrequestreview-5968499089): "Tests-only PR, no production code touched." He read all five tests against the real endpoints |
| [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) | Heraldo, 23 Nov | [Approved](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276#pullrequestreview-6016382571), after checking that a new application can never become the selected bank while it's pending |

## What would raise this

A review of a teammate's MR with concrete, feasible suggestions, as in earlier weeks: the code checked out and run, and each point backed by a test, a mutant or a request. In the week after this one, I'm taking on [PIL-541](https://linear.app/pilah-2/issue/PIL-541) and [PIL-542](https://linear.app/pilah-2/issue/PIL-542), stacked on Ghani's [pilah-be #184](https://github.com/bank-sampah-PILAH/pilah-be/pull/184), which gives me a reason to read his PR closely.
