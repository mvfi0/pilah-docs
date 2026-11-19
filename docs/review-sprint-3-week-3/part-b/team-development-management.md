# Team Development Management

!!! success "Competency level: 3"
    Three detailed reviews of teammates' merge requests. Each was checked out and run before commenting, and each point carries a concrete, feasible change:

    - **Gabriel's PIL-478 pair** ([pilah-be #169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169), [pilah-mobile #243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243), 12 Nov): I put code back on purpose (10 mutants) to see whether the tests notice, and 6 were caught. That showed a claim in both PRs doesn't hold: the server doesn't require a pengelola's birth date. It also showed two behaviours with no test, with the test that would pin each.
    - **Gabriel's [pilah-be #174](https://github.com/bank-sampah-PILAH/pilah-be/pull/174)** (Swagger UI integrity hashes, 17 Nov): I recomputed all three hashes from the files the CDN serves, then reverted the template to show his test catches it. I also showed that a version bump with the old hashes still passes every test, and suggested keying the hashes by version. Approved.

    The other side of reviewing: **nine review threads on my PRs**, from Heraldo and Tristan. Each was checked against the code, then fixed test-first or answered with the reason for leaving it, in its own thread.

## Review given: Gabriel's PIL-478 pair, 12 Nov

The pair makes the tanggal lahir optional for a nasabah: the backend accepts a `null` date ([#169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169)), and the app lets a nasabah leave it empty or clear it ([#243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243)).

[Review of #169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169#pullrequestreview-5862861835), [review of #243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243#pullrequestreview-5862862337)

**Verified before commenting:**

- checked both branches out and ran them: `apps` and `tests.regression`, 634 tests on the backend;
- traced the red backend CI to `test_export_metadata_names_the_actual_selected_period`, the date test that also fails on `staging`, and pointed at the fix in [`fc792c0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fc792c07c656aef923338f64b8a570feed6ef4dd);
- sent `PUT /api/v1/onboarding/profile` as a pengelola, with `tanggal_lahir: null` and with the key omitted;
- ran 10 mutants, putting the old code back one change at a time; 6 were caught. The eight named in the reviews:

| Mutant | Caught? |
|---|---|
| Backend: the `None` guard removed | Yes, 4 of the 8 new tests fail |
| Backend: the future-date check removed from `me/profil` | Yes, 1 fails |
| Mobile: `''` sent instead of `null` | Yes, 3 fail |
| Mobile: the date made optional for everyone | Yes, 2 fail, including "a pengelola is still asked for one" |
| Mobile: `toJson` sending `''` | Yes, 2 fail |
| Backend: the old check put back in `UserProfileSerializer`, the path mobile onboarding actually uses | **No** |
| Mobile: `onClear` removed from the edit sheet | **No** |
| Mobile: the old restored-draft behaviour put back | **No** |

| Point | Why it matters | Suggestion |
|---|---|---|
| **1. A pengelola's birth date isn't gated server-side (medium)** | Both PRs say the server still requires it. `PUT /onboarding/profile` answers 200 with `is_profile_complete=True` for a null or missing date, because [`complete_profile`](https://github.com/bank-sampah-PILAH/pilah-be/blob/b8c48bf6557fb3910c2b40c106d44167b34138f3/apps/authentication/services.py#L454) sets the flag unconditionally. So the mobile guard is the only guard | Require the date for non-nasabah roles in `UserProfileSerializer.validate`, with a test, or correct the claim in both PRs |
| [**2. The onboarding path has no backend test (medium)**](https://github.com/bank-sampah-PILAH/pilah-be/pull/169#discussion_r4541179824) | All 8 new tests go through the other two serializers | One test through `PUT /onboarding/profile` for a nasabah without a date |
| [**3. The clear button has no test**](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243#discussion_r4541180244) | It's half of the issue ("data a nasabah would rather not have"), covered only by screenshots | A widget test that taps clear and checks the payload |
| [**4. The restored-draft change is untested**](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243#discussion_r4541180253) | The old behaviour passes everything | One test that restores a draft with no date over a form that has one |
| Nits ([#169](https://github.com/bank-sampah-PILAH/pilah-be/pull/169#discussion_r4541179838), [#243](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/243#discussion_r4541180277)) | An uncovered `raise NotImplementedError`; a doubled doc comment | `abc.abstractmethod`; drop the old line |

Both were posted as comment-only reviews, as I chose, each also saying what held up.

**Outcome:** Scallss merged #169 39 minutes and #243 55 minutes after the reviews, with no new commit. The points weren't answered in the PRs, so the server-side gap in point 1 was merged as it stood.

## Review given: Gabriel's [pilah-be #174](https://github.com/bank-sampah-PILAH/pilah-be/pull/174), 17 Nov

The PR pins the Swagger UI files the API docs page loads from jsdelivr, and adds Subresource Integrity hashes (OWASP A08). This closes the 26 Oct ZAP finding 3.

[Review](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#pullrequestreview-5925723761)

**Verified before approving:**

- **Hashes:** recomputed all three from the bytes jsdelivr serves for `swagger-ui-dist@5.35.0`. All match [`SWAGGER_UI_SRI`](https://github.com/bank-sampah-PILAH/pilah-be/blob/7661166b98a5ab251ca024f1bcb0545794304593/config/settings.py#L256-L260). jsdelivr sends `Access-Control-Allow-Origin: *`, so `crossorigin="anonymous"` works. 5.35.0 is still npm's latest, so the pin changes nothing served today.
- **Template:** compared the new `body` block with drf-spectacular 0.29.0's. The only differences are the integrity attributes and an unused fallback branch, which is harmless.
- **Tests:** merged his head into current `staging`. It merges cleanly, and the 20 CSP tests pass. With only the template reverted, [his new test](https://github.com/bank-sampah-PILAH/pilah-be/blob/7661166b98a5ab251ca024f1bcb0545794304593/tests/regression/identity/test_csp.py#L269) fails once per tag, so it catches what it's meant to.

| Point | Why it matters | Suggestion |
|---|---|---|
| [**A version bump without new hashes still passes every test** (non-blocking)](https://github.com/bank-sampah-PILAH/pilah-be/pull/174#discussion_r4590137599) | I tried it: `SWAGGER_UI_VERSION = "5.32.0"` with the 5.35.0 hashes. All 20 tests pass, but a browser would block every file and show a blank docs page | Store the hashes per version, so a bump without new hashes fails when Django loads its settings. Fine as a follow-up |

**Outcome:** merged on 17 Nov.

## Reviews received

| Reviewer | Finding | Checked against the code | Status |
|---|---|---|---|
| Heraldo, [on #167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167#discussion_r4511126273) | The `batalkan` docstring still says a void stays in the riwayat; it also feeds the API description | **Correct** | **Fixed**, [`72fc61c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/72fc61c5), with the nasabah test docstring. [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/167#discussion_r4538357384) |
| Heraldo, [🟠 on #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4511111331) | The bulk result panel still promises the riwayat keeps the void | **Correct**: after #167 only the detail does | **Fixed**, red [`5e8e160`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5e8e160d) → green [`77e612e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/77e612ec). [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4538357720) |
| Heraldo, [🟡 on #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4511111518) | The bulk confirmation states a different consequence than the single dialog | **Correct** | **Fixed** in the same pair. [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4538358081) |
| Heraldo, [🟡 on #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4511111712) | A doc comment still contradicts the fixed one | **Correct** | **Fixed** in the same pair. [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4538358368) |
| Heraldo, 3 Nov, three comments on #174 after his approval: [no way back](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4456461966), [a flag reset](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4456462207), [a dead-end link](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4456462501) | Non-blocking, outside PIL-451's scope | Checked each. The first was right about the PR's claim, so I corrected the description | **Answered on 13 Nov** with the reason for leaving each. [Reply 1](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4563572503), [2](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4563572848), [3](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4563573223) |
| Tristan, [P2 on #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4585330905) | `complete_profile` saves the request's cached `User` without the lock, so it can answer a stale role | **Correct**: it was a fifth writer of the invariant | **Fixed**, red [`9424d9f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9424d9f2) and [`870224d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/870224dc) → green [`51a631e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/51a631ef). [Reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4589406317) |
| Tristan, [P2 on #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4585330901) | On web the role page has no way back | **Correct** | **Fixed**, red [`42d2020`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/42d20201) → green [`ef55977`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef55977b) → refactor [`a363412`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a363412f). [Reply](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4589406686) |

**A call I made that was reversed.** On 13 Nov I left Heraldo's "no way back" comment as outside PIL-451's scope and corrected the PR's claim instead. On 16 Nov Tristan raised the same gap as a P2, so the lead developer counted it in scope, and I fixed it that evening.

**Received on 17 Nov, answered next week:** Gabriel's non-blocking comments on #175 and #176, and his "Nothing blocking" on #177.

## Working with the team

- **Not bypassing a teammate's open request.** On 13 Nov both PIL-451 PRs had two approvals but still carried Tristan's change request from 31 Oct. I didn't use an admin merge. I re-requested his review, and he approved on 17 Nov.
- **An idea, not a change:** asked whether the project notifies the team on approvals, I checked (12 Nov). Nothing does, and repo webhooks need admin rights. So I outlined a GitHub Actions workflow on `pull_request_review` that could reuse the Discord secrets of Rifqi's #173. I didn't open it, since it touches shared CI and needs a Linear issue first.
