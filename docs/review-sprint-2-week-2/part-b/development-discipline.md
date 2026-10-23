# Development Discipline

!!! success "Competency level: 3"
    Three new merge requests this week, two of them the QA fixes:

    - PIL-374, the saldo warning ([#153](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153));
    - PIL-375, the locked Tanggal ([#154](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154));
    - PIL-341 slice 3, draft pencairan on a desktop window ([#127](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127), 17 Oct).

    Each has its own Linear issue, a branch off `staging`, and scoped Conventional Commits with the TDD phase in every subject. Each also has a description with the cause, the decision, the tests, Playwright results and screenshots. CI and SonarCloud were green before each merge. All three are approved and merged.

## Merge requests

| MR | Opened → merged | Size | Commits | Review |
|---|---|---|---|---|
| [#153 — PIL-374: warn and confirm when a general Nominal is above a nasabah's saldo](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/153) | 21 Oct → 21 Oct | +258 / −1, 5 files | 12 | approved by Aldo |
| [#154 — PIL-375: show a potongan pencairan's tanggal as locked in Edit Pencairan](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/154) | 21 Oct → 21 Oct | +42 / −5, 3 files | 2 | approved by Aldo |
| [#127 — PIL-341 (3/3): draft pencairan on a desktop window](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127) | 17 Oct → 18 Oct | +717 / −270, 20 files | 28 | approved by Tristan, Pascal and Aldo |

Sizes and commit counts are from GitHub on 23 Oct.

## From QA finding to merged fix

Both fixes went through the same steps, each recorded where the team can see it:

1. **Checked before it was called a bug.** I traced each QA finding to the code. The first was a deliberate ceiling with no explanation on screen. The second was a deliberate lock that looked unlocked.
2. **The decision went to the team.** For PIL-374 I wrote a short proposal: warn, block, or warn and confirm. The team chose to warn without blocking, and Pascal suggested the confirmation.
3. **Tracked in Linear.** I opened [PIL-374](https://linear.app/pilah-2/issue/PIL-374) under CPBI-22 and [PIL-375](https://linear.app/pilah-2/issue/PIL-375) as a sub-issue of PIL-327, where the lock came from. Each has the cause, the tasks, the tests, and a note for QA. When a scope changed, I updated the issue the same day.
4. **One MR per issue,** titled with the issue key so Linear links it, with a description that the reviewer can check against: what QA saw, why, what changed, the tests, the E2E results and screenshots.
5. **Review, then merge.** I requested Pascal and Aldo through the team's `ask-for-review` skill (GitHub reviewer plus a Discord ping). I merged only after approval, with green CI and SonarCloud.

## Changes after the MR was open

Every change after opening #153 was a new commit, never a force-push, so the review history stays readable:

- **Pascal's suggestion,** a confirmation on Terapkan: a red/green pair.
- **My request** to list the affected nasabah: a red/green pair.
- **SonarCloud S3776:** a `[REFACTOR]` commit.
- **The follow-up** to list even a single nasabah: a red/green pair.

The description was rewritten each time, so it always matched the head commit.

## Example commit messages

```
test(draft-pencairan): [RED] add failing test for warning when a general Nominal is above some saldo

QA (Fail - High): a nasabah with about Rp 19 rb saldo, a general Nominal
of Rp 50.000, and the draft paid their whole saldo without a word. The
ceiling stays (decided: warn, don't block); the pengurus should be told
before Terapkan.
```

```
refactor(draft-pencairan): [REFACTOR] move the saldo confirmation out of _terapkan (PIL-374)

Design issue: SonarCloud S3776 on PR #153. _terapkan had grown to a
cognitive complexity of 17 (limit 15) once it held both applying the
general settings and building the saldo confirmation. Pattern: extract
method, so _setujuSaldoKurang answers one question (may this be
applied?) and _terapkan only applies. Origin: own refactor, after the
dialog and its list landed. Behaviour unchanged; the draft tests pass.
```

```
fix(pencairan): [GREEN] show a potongan pencairan's tanggal as locked, and say so (PIL-375)

TanggalPencairanField takes enabled; Edit Pencairan passes !_terkunci,
so a potongan pencairan shows the tanggal greyed out with its disabled
border and no ripple, like the locked nominal. The note now names what
is locked: "jadi nominal dan tanggalnya dikunci; hanya metode dan
keterangan yang bisa diubah." The picker guard in _pickTanggal stays.
```

## Also this week: the Sprint 2 merges (17 Oct)

My 8 approved MRs from Sprint 2 had fallen behind `staging`, and 5 had conflicts. I resolved each on its own branch, by merging `staging` in rather than force-pushing:

- **Merge commits** fixed the semantic conflicts, so the code still compiled and ran.
- **The checks ran again**, on the backend and with Flutter.
- **CI went green** before each merge.
- **Stacks merged bottom first:** pilah-be #89 → #79 → #92 → #96 and pilah-mobile #74 → #62 → #73 → #83.

Afterwards I deleted the merged branches and removed their worktrees.
