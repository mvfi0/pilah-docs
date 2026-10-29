# Development Discipline

!!! success "Competency level: 3"
    Two meaningful merge requests this week, the backend and mobile halves of one QA finding:

    - [pilah-be #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137): `PATCH /onboarding/role`, 13 commits;
    - [pilah-mobile #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174): "Ganti peran" and the role page, 14 commits.

    Both come from one Linear issue I wrote from the QA note, and both use the same branch (`feature/pil-451`) off `staging`. Every commit is a scoped Conventional Commit:

    - the TDD phase is in each subject;
    - the OWASP category is in the subject where it applies;
    - the body names the design issue, the pattern and its origin.

    Each MR description has the cause, the API contract, the red/green table, the E2E results with screenshots, and the local validation. Tool findings and review findings were fixed as new commits, never force-pushed, and each review thread got a reply linking its fix. Neither MR is merged yet; they wait for approval (see [below](#status-and-what-is-left)).

## Merge requests

| MR | Opened | Size | Commits | CI / SonarCloud | Status (29 Oct) |
|---|---|---|---|---|---|
| [#137 — PIL-451: let an account change a mis-tapped role before onboarding commits it](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) | 26 Oct | +469 / −3, 11 files (with the review fixes) | 13 | green, gate passed, 0 issues | Open. Reviewed by Tristan and Pascal; P1, P2 and the nit fixed and answered on 29 Oct |
| [#174 — PIL-451: change a mis-tapped role from Lengkapi Profil](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) | 26 Oct | +630 / −12, 18 files | 14 | green, gate passed, 0 issues | Open. Must merge after #137 (it calls the new endpoint), no review yet |

Sizes and commit counts are from GitHub on 29 Oct.

## From QA note to two MRs

1. **Checked before it was called a bug.** QA suggested resetting the chosen role on the phone. Tracing it showed the role is saved on the server the moment Lanjutkan is tapped, and nothing could change it afterwards. A test pins that on purpose. So a phone-only reset couldn't work, and the fix needed both repos.
2. **Rated, not assumed:** High, not Critical. Nothing is lost or exposed, but a mis-tap is a permanent dead end on the first screen, and testers on fresh Google accounts would hit it before UAT on 6 Nov.
3. **Tracked in Linear.** I created [PIL-451](https://linear.app/pilah-2/issue/PIL-451) as a sub-issue of CPBI-34 in Cycle 3. It has the cause, the severity, backend and mobile tasks, and the tests to write, in the same layout as my earlier PIL-374.
4. **One branch name in both repos:** `feature/pil-451`, so Linear links both PRs to the issue.
5. **Test-first, in slices:** three red/green pairs plus two mutation-proven guards on the backend, four pairs and two refactors on mobile. The tables are on the [TDD page](tdd.md).
6. **CI's own checks run locally before each push:**
    - backend: ruff, `pip check`, `makemigrations --check`, migrate, `check` / `check --deploy` and mypy, then the suite on Postgres 16;
    - mobile: `flutter analyze`, `dart format`, the full suite, diff coverage, and the web build.

## Changes after the MR was open

Every change after opening was a new commit, and the description was updated to match:

- **#137:**
    - CI's mypy step caught a model missing from `api.models.__all__`. Fixed in [`8bf93cf`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8bf93cf) before review.
    - **Tristan's and Pascal's review (26 Oct), answered on 29 Oct:**
        - P2 with a coverage test, [`d83b0c1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d83b0c1);
        - P1 as a red/green pair, [`f4b663d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f4b663d) → [`df45397`](https://github.com/bank-sampah-PILAH/pilah-be/commit/df45397), plus a test `[REFACTOR]`, [`fe17440`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fe17440);
        - the nit by correcting the description.

        Each finding got a reply in its own thread, linking the commit that fixes it. The description's tests, security and validation sections were updated to match.
- **#174:**
    - SonarCloud's first run flagged S3776 on my own `build` method. Fixed with a `[REFACTOR]` commit, [`87f2f0d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/87f2f0d).
    - Coverage showed 97.1%. Fixed by covering the two lines in the test files CI runs, [`b2344b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b2344b5).
    - Both are listed in the PR description's "after the first SonarCloud run" section.

## Example commit messages

```
feat(onboarding): [GREEN] refuse a role change once onboarding has started (PIL-451, OWASP A04, A01)

change_role is now one conditional UPDATE: it only touches the row
while the profile is incomplete, there is no bank sampah (pending
included) and no linked membership. Otherwise 409 role_locked, and the
role stays.

Design issue: check-then-act. Reading the state, then saving, leaves a
window where a bank registration commits in between and is left under a
role it no longer matches.
Pattern: guarded state transition, done as a conditional UPDATE, so the
database re-checks the row as it writes it (the same technique as
_reactivate_rejected_membership). Origin: designed in.

The UPDATE does not run User.clean, so the membership condition is part
of the filter itself. The refusal is a clean 409, not the 500 that
clean's ValidationError gave (OWASP A01), and the onboarding state
machine is enforced on the server, not trusted to the client (OWASP A04).
```

```
test(onboarding): [RED] add failing test for changing role from Lengkapi Profil (PIL-451)

QA suggested a way back from Lengkapi Profil to the role choice. The
profile step must:

- name the role being registered ("Mendaftar sebagai Pengurus Bank
  Sampah") with a "Ganti peran" link that opens the role page on top,
  so back returns to the form;
- hide the link once a bank sampah exists for the account, and when
  joining through an invite (the backend refuses those anyway);
- redraw for the new role once the session switches to it: a nasabah
  gets "Pilih Bank Sampah" as step two, not "Data Bank Sampah".

Fails: there is no label or link. And with the label assertion
removed, the redraw check still fails, because the screen only listens
to the auth state and keeps drawing the old role's stepper.
```

The full subject lists read as a sequence of phases. Mobile, oldest first:

```
test(onboarding): [RED] add failing test for changing role through the data layer (PIL-451)
feat(onboarding): [GREEN] change role through PATCH onboarding/role and keep its session (PIL-451)
test(preview): cover the preview session's changeRole (PIL-451)
test(onboarding): [RED] add failing test for switching the session to a changed role (PIL-451)
feat(onboarding): [GREEN] switch the session to a changed role, or say why not (PIL-451)
test(onboarding): [RED] add failing test for picking another role from the role page (PIL-451)
feat(onboarding): [GREEN] let a signed-in account pick another role on the role page (PIL-451)
test(onboarding): [RED] add failing test for changing role from Lengkapi Profil (PIL-451)
feat(onboarding): [GREEN] name the role on Lengkapi Profil with a way to change it (PIL-451)
refactor(onboarding): [REFACTOR] name the role page's two Lanjutkan paths in _submit (PIL-451)
fix(onboarding): take the role note's text style from AppTextStyle (PIL-451)
test(onboarding): cover a malformed role-change response (PIL-451)
test(auth): cover getMe and saveToken in the files CI runs for this PR (PIL-451)
refactor(onboarding): [REFACTOR] decide the role note outside build (PIL-451, SonarCloud S3776)
```

## Status and what is left

- **#137's review findings are fixed and answered** (29 Oct). It now waits for the reviewers to re-check and approve. Nothing merges without approval.
- **#174 waits on #137.** It calls the new endpoint, so it merges second, then goes to QA.
- **Reviewers** came on their own for #137. I still have to request a review of #174 through the team's `ask-for-review` skill.
