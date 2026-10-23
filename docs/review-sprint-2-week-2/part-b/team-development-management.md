# Team Development Management

!!! success "Competency level: 3"
    A detailed review of **Ghani's pilah-mobile #162** (23 Oct), which removes draft export from the pencairan editor:

    - its claims verified on a local checkout, including a mutation check that its new tests really guard the removal;
    - one question about the product decision behind removing a delivered feature;
    - two feasible suggestions: the dead code left behind, listed file by file for the planned cleanup, and making the red step visible in history.

    The other side of reviewing is here too:

    - **Aldo's reviews** of my two fixes, checked against the code before merging.
    - **A teammate's suggestion** during review (Pascal's confirmation dialog), built test-first into the MR.
    - **Reviewers and QA** requested through the team's skills.

## Review given: Ghani's [pilah-mobile #162](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/162), 23 Oct

Ghani's PR removes the **Ekspor** action (PDF and Excel) from the draft pencairan editor. It changes one line of the header and removes the `_export` handler, three imports and the export widget tests. It adds eight tests asserting that no export action exists on a new, saved, confirmed or cancelled draft, at phone and desktop width. The description calls it the first stage of a removal.

[Review](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/162#pullrequestreview-5626578469)

**Verified before commenting,** on the PR head [`38dc9cf`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/38dc9cf7fc594830698204ac56ce24163830e62b):

- **The suite passes:** `flutter test test/features/draft_pencairan` gives 413 passing tests.
- **Mutation check:** I restored staging's editor page, with the Ekspor button, and ran the new `draft export is unavailable` group. **8 of 8 failed.** The new tests really guard the removal; they don't pass by default.
- **No unrelated coverage lost:** only export tests were removed from `draft_editor_view_test.dart`.
- **No remaining entry point:** I searched the PR head, and nothing in the app reaches the export path any more.
- **No decision on record:** Linear has no issue for removing it. The feature was delivered under [PIL-316](https://linear.app/pilah-2/issue/PIL-316), which is Done.

| Point | Why it matters | Suggestion |
|---|---|---|
| **1. Which decision removes this?** (question) | A feature delivered and closed in PIL-316 disappears with no linked decision. QA or the sprint review could read it as a regression. | Link the standup or PO decision, or open a Linear issue for the removal. |
| **2. Track the follow-up cleanup** | After the PR, `ExportMenuButton`, `DraftPdfPreviewPage`, `simpanBerkasDraft`/`bagikanBerkasDraft`, `DraftEditorCubit.export` with `EditorPhase.exporting` and `canExport`, the repository's `exportDraft`, and the backend's `draft_export.py` are unreachable, but still compiled, tested and counted by Sonar. `canExport` still reads as if export were possible. | A Linear issue with that list, each item linked to its line on the PR head, so the second stage isn't forgotten. |
| **3. Show the RED in history** | The description walks through RED, GREEN and REFACTOR, but it is one `feat` commit, so only the mutation check above shows that the tests went red first. | Separate `[RED]`, `[GREEN]` and `[REFACTOR]` commits, as on the other pencairan PRs. |

I posted this as a comment rather than an approval: the code is right, but (1) is a product decision that should be on record first. None of the points blocks the change itself.

## Reviews received and answered

### Aldo on [#153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153) and [#154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154), 21 Oct

Aldo approved both, with a sequence diagram of the saldo flow and a list of what he verified. On #153 he raised two informational nits. I checked both against the code before merging:

| Nit | Checked | Outcome |
|---|---|---|
| A nasabah whose saldo exactly equals the Nominal is not warned | `melebihiSaldo` uses a strict `>`, and `hitung` pays exactly the Nominal in that case. Nobody gets less than asked. | Correct as is, no change |
| `floor()` in the message versus in `hitung` | `hitung`, `melebihiSaldo` and the message all use `nilai.floor()` | The amount shown always matches the amount paid, no change |

His other claims also held: dismissing the dialog counts as "no" (`return hasil == true`), Persen never triggers it, and Batal applies nothing.

### Pascal's suggestion on #153

Pascal suggested a confirmation dialog on Terapkan, so the warning can't be missed. It went into the MR as a red/green pair ([`86427cb`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/86427cb) → [`416ac45`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/416ac45)). The team had already chosen to warn without blocking, and Pascal's confirmation went on top of that. The decision is recorded in [PIL-374](https://linear.app/pilah-2/issue/PIL-374).

### On [#127](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127) (PIL-341 slice 3), 18 Oct

Pascal and Aldo each found an issue on the desktop editor:

- **Pascal:** resizing across 840 px reset the nasabah list's search and filter.
- **Aldo:** a saved draft first showed the phone layout while it loaded.

Pascal fixed both test-first on my branch, replied in both threads, and merged it.

## Asking the team

- **Reviews:** Pascal and Aldo on #153 and #154, through `ask-for-review`, which assigns the GitHub reviewer and posts a Discord ping.
- **#127 (17 Oct):** Tristan for review and Aldo for QA, through `ask-for-review` and `ask-for-qa`. The QA message lists five concrete changes and five steps to verify them.
- **The PIL-374 decision:** a short proposal doc for the team, with the cause, three options and their trade-offs, and an open-questions checklist. It recorded the decision once it was made.
