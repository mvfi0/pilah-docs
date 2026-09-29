# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    New learnings from outside the material generally given in class, each applied in the PILAH project this week (Sprint 1 Week 2, 23–29 Sep) and linked to the commit or page that shows it.

The rubric's level 3 asks for 1–2 new learnings outside class material that are applied in the project; level 4 asks for 3 or more. Basic TDD, Django CRUD and Git, which the course already covers, are deliberately left out.

## New learnings applied this week

| # | Concept | Applied in | Evidence |
|---|---|---|---|
| 1 | **Ledger replay with an append-only audit trail**: recompute derived balances by replaying events from a stored snapshot, and keep replaced versions instead of overwriting them (ideas from event sourcing and financial audit design) | PIL-230 edit pencairan: `PencairanRevisi` keeps every old version with who, when and why; editing replays the nasabah's ledger from the earliest affected moment and rewrites every later saldo snapshot, anchored on a stored snapshot because legacy balances have no transaksi behind them | [`0856114`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0856114), [`c2ef8a4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2ef8a4), [Programming page](../../review-week-2/part-b/programming.md) |
| 2 | **Diff coverage and mutation-style test validation**: measure coverage only on the lines a change touches, then deliberately break the code to prove a test can fail | TDD evidence for pilah-be #52, the #19 review round and pilah-mobile #52; mutations on the detail sheet's refresh rule, the serializer constants (pilah-be #67) and the generated `toJson` | [Coverage evidence](../../sprints/sprint-1/evidence/PIL-230-coverage.md), [pilah-be #67](https://github.com/bank-sampah-PILAH/pilah-be/pull/67) |
| 3 | **Agentic AI workflow with persistent memory and project skills**: an AI coding agent driven by the team's skill files (`tdd`, `ask-for-review` over a Discord webhook) and by rules saved after each correction, so later work follows them | the whole week: phase-tagged commits, review replies inside threads, merge checks through PR state | [AI Literacy page](../../review-week-2/part-b/ai-literacy.md) |

## How each one changed the work

- **Ledger replay** made an otherwise unsafe feature possible: editing an old payout no longer leaves later receipts wrong, and the edit is refused when it would overdraw a *later* pencairan, which a check against today's saldo alone would miss.
- **Diff coverage** replaced "the whole project is at 91%" with a precise claim about my own lines, and exposed that a moving base branch had been counting other people's merged code as mine (565 mobile lines instead of 325).
- **Persistent AI rules** stopped repeated mistakes: after one wrong "not merged" claim, merge state is always checked through the PR.
