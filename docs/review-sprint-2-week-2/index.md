# IR Part B Sprint 2 Week 2

Evidence for the individual review (IR), organised by competency. Each page states the competency level and the dated evidence behind it, with commit and PR links.

Part B — Hardskills: Best Practice, for Sprint 2 week 2.

!!! note "What this page covers"
    [Sprint 2 Week 1](../review-sprint-2-week-1/index.md) claims work up to 16 Oct. This page covers **17–23 Oct**: the merges of the Sprint 2 PRs, PIL-341 slice 3, and the two QA findings on pencairan (PIL-374 and PIL-375).

| Competency | Level | Status (23 Oct) |
|---|---|---|
| [AI Literacy](part-b/ai-literacy.md) | **3** | Its claims checked against the code before acting; two of its own wrong claims corrected; a QA "Fail" traced to a deliberate rule, then fixed as the team decided; a check it could not pass reported, not worked around |

The other Part B competencies for this week are still to be written.

Work this week:

- **Merges (17 Oct):** my 8 approved PRs across pilah-be and pilah-mobile. Conflicts were resolved on each branch, CI ran green, and stacks were merged bottom first.
- **[PIL-341](https://linear.app/pilah-2/issue/PIL-341) slice 3**, [pilah-mobile #127](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127): draft pencairan on a desktop window. The editor has a side panel, the sheets become dialogs from tablet width, and lists keep to a centred column. A saved draft opens from its link, and only a bare draft id is accepted (OWASP A01, A03).
- **QA finding: saldo below a general Nominal** ([PIL-374](https://linear.app/pilah-2/issue/PIL-374)), [pilah-mobile #153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153): warn, don't block. A note sits under the Nominal, a confirmation names every affected nasabah, and each capped card carries a line.
- **QA finding: Edit Pencairan locked fields** ([PIL-375](https://linear.app/pilah-2/issue/PIL-375)), [pilah-mobile #154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154): a pencairan with a potongan now shows Tanggal as locked, like Nominal, and the note names both.
