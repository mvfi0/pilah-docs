# Team Development Management

!!! success "Competency level: 2"
    Reviewed a peer's merge request with a verified finding and a feasible suggestion (pilah-be #22), alongside answering the reviews received on my own PRs.

## 15–21 Sep

### Issue tracking

- Work follows the Linear issue [PIL-176](https://linear.app/pilah-2/issue/PIL-176) under [PIL-140 CPBI-10](https://linear.app/pilah-2/issue/PIL-140); the branch name links it, so Linear tracks the PR automatically.

### Responding to review (received, not given)

Heraldo reviewed PR #19 with three findings; each was fixed test-first and answered in its thread:

- [Finding 1: membership gate](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062276107)
- [Finding 2: legacy sen rounding](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062584758)
- [Finding 3: same-instant ordering](https://github.com/bank-sampah-PILAH/pilah-be/pull/19#discussion_r4062276317)

This shows engagement with review, but the rubric measures reviews *given*.

## 22 Sep

- Requested review from Heraldo on [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) and [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) through the team's `ask-for-review` skill, which assigns the GitHub reviewer and posts the request to Discord.

### Review given: [pilah-be #22](https://github.com/bank-sampah-PILAH/pilah-be/pull/22) (PIL-168, by Twentism)

[My comment](https://github.com/bank-sampah-PILAH/pilah-be/pull/22#issuecomment-5779340630) on the rounding change:

- **Positive:** rounding down through `bulatkan_rupiah` is consistent, and pencairan in #19 now follows the same rule.
- **Finding:** `saldo.total_saldo` is rounded when touched, but `saldo_setelah_transaksi` and the export's saldo column still add up the old `total_nilai` values that carry sen. For a PILAH 1.0 nasabah the history can read a few sen above the real saldo: legacy saldo 100,75 + setoran 3.333 gives a saldo of 3.433 but a history of 3.433,75. Checked against the code on #22's head before posting.
- **Suggestion:** round in those two places too, or record it as a known issue for now.

## To do

- Review more peers' merge requests over the coming weeks.
