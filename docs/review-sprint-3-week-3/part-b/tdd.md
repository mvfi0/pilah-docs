# Test Driven Development

!!! success "Competency level: 4"
    **Level 3 met:** every behaviour this week was built test-first, with the phase in every commit subject. The green steps came only after their `[RED]` commits, and `[REFACTOR]` commits only after green.

    - Every changed line is covered: 100% on SonarCloud for every MR with lines to cover.
    - The tests cover the positive case, each refusal and the corner cases (see [the table](#positive-negative-and-corner-cases)).
    - Guard tests that pass in their red commit are there on purpose, and the commit says so.

    **Level 4:** advanced testing methods in the commits:

    - **An architecture fitness function:** a test that parses every module under `apps/` with Python's `ast` and fails on any query that spells out the counted-setoran rule by hand. On `staging` it failed on exactly one line.
    - **A real race, made deterministic:** a two-thread `TransactionTestCase` on PostgreSQL pauses a profile completion inside `User.save`, runs a role change in between, and asserts the change waited and was refused.
    - **An HTTP contract test over three endpoints:** one test drives `/aktivitas`, `/transaksi` and `/pencairan` with the same malformed ids, as sub-tests, so a fourth list can join with one line.
    - **Mutation testing in review:** on Gabriel's PIL-478 pair I put code back on purpose (10 mutants, 6 caught) and reported, with the test that would catch each, the ones that got through. See [Team Development Management](team-development-management.md).

## Coverage proof at a glance

| MR | Work | SonarCloud new-code coverage | Quality gate |
|---|---|---|---|
| pilah-be [#175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175) | PIL-482: malformed `nasabah_id` is a 422 | [100% of 15 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=175&metric=new_coverage&view=list) | Passed |
| pilah-be [#176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176) | Waste categories through `tercatat()` | [100% of 2 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=176&metric=new_coverage&view=list) | Passed |
| pilah-be [#177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177) | NUL or padded kode in a body is a 422 | [100% of 13 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=177&metric=new_coverage&view=list) | Passed |
| pilah-be [#137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) | PIL-451, third round | [100% of 52 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=137&metric=new_coverage&view=list) | Passed |
| pilah-mobile [#174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) | PIL-451, third round | [100% of 96 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-mobile&pullRequest=174&metric=new_coverage&view=list) | Passed |
| pilah-be [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) | PIL-481, review round | [100% of 7 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=167&metric=new_coverage&view=list) | Passed |
| pilah-mobile [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) | PIL-481, review round | No coverable lines (copy, comments, a constant); pinned by widget tests | Passed |

Read from the SonarCloud API on 19 Nov, for each PR's final analysis.

## New PRs (16 Nov)

### [pilah-be #175](https://github.com/bank-sampah-PILAH/pilah-be/pull/175), PIL-482

| Step | Commit | Tests |
|---|---|---|
| Red | [`5699fff`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5699fffc) | `test_nasabah_id_bukan_uuid_ditolak_422_di_semua_endpoint` (3 endpoints × 3 malformed ids); `test_nasabah_id_uuid_tetap_menyaring`, a guard that a valid id still filters |
| Green | [`5c2f7fc`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5c2f7fc2) | `validasi_uuid` in `shared_kernel`, used by `/transaksi` and `/pencairan` |
| Refactor | [`b85819a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b85819ae) | `/aktivitas` moves onto the same helper; the same tests pass |

```python title="tests/test_nasabah_id_http.py"
ENDPOINTS = ("aktivitas", "transaksi", "pencairan")

def test_nasabah_id_bukan_uuid_ditolak_422_di_semua_endpoint(self) -> None:
    self.client.force_authenticate(self.pengurus)
    for path in ENDPOINTS:
        for raw in ("abc", "123", "00000000-0000-0000-0000-00000000000Z"):
            with self.subTest(path=path, raw=raw):
                response = self.client.get(f"/api/v1/{path}?nasabah_id={raw}")
                ...
```

`/aktivitas` already answered 422, so its sub-tests passed in the red commit. The other two failed with 500, which is the bug.

### [pilah-be #176](https://github.com/bank-sampah-PILAH/pilah-be/pull/176), the counted-setoran rule

| Step | Commit | Result |
|---|---|---|
| Red | [`b10fffa`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b10fffaa) | `test_counted_setoran_are_read_through_tercatat` fails on exactly one line: `apps/reporting/services.py:100` |
| Green | [`8d1a931`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8d1a9316) | `waste_categories` reads through `tercatat()`; the existing PIL-428 behaviour test still sees one deposit after a void |

```python title="tests/test_architecture.py"
def test_counted_setoran_are_read_through_tercatat(self) -> None:
    violations: list[str] = []
    for path in sorted(APPS_ROOT.rglob("*.py")):
        if path == TERCATAT_RULE_HOME or path.name.startswith("test_"):
            continue
        violations.extend(
            f"{path.relative_to(REPO_ROOT)}:{line}"
            for line in _spelled_out_tercatat_filters(path)
        )
    self.assertEqual(violations, [])
```

`_spelled_out_tercatat_filters` walks the syntax tree for `.filter()` and `.exclude()` calls whose keyword names `Transaksi.Status.TERCATAT` or ends in `transaksi__status`. A test that greps text would be fooled by a comment. This one is not, and because it failed on exactly the line in question, it isn't vacuous.

The green commit is named `refactor(reporting): [GREEN]`: it makes the test pass without changing behaviour, which the unchanged PIL-428 test shows.

### [pilah-be #177](https://github.com/bank-sampah-PILAH/pilah-be/pull/177), NUL and padded kode in a body

| Slice | Red | Green | Tests |
|---|---|---|---|
| Jenis sampah edit: a NUL in `kode` | [`04ab0bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/04ab0bbc) | [`e7ef617`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e7ef617b) | `test_kode_tidak_valid_ditolak_422_bukan_500` |
| Jenis sampah edit: a padded duplicate (`" HDPE "`) | [`a56eba9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/a56eba91) | (same green) | `test_kode_milik_jenis_lain_tetap_ditolak_dan_kode_sendiri_diterima` |
| Nasabah edit: both cases | [`1029701`](https://github.com/bank-sampah-PILAH/pilah-be/commit/10297010) | [`887ecf4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/887ecf45) | the same two tests for nasabah |
| `DELETE /device-tokens/`: a NUL in the token | [`d3b1bea`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d3b1beaf) | [`1a765f9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1a765f94) | `test_token_dengan_nul_ditolak_422_bukan_500` |

The padded-duplicate bug wasn't in the plan. It came up while writing the NUL slice: the uniqueness check read the raw body, while the save used the stripped value. So it got its own red commit before the shared green.

## Review rounds

| Finding | Red | Green / refactor | The red failed on |
|---|---|---|---|
| #137, Tristan P2: a profile completed next to a role change answers with a stale role and `next_step` | [`9424d9f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9424d9f2), [`870224d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/870224dc) | [`51a631e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/51a631ef) | The response's role after a role change; and, on PostgreSQL, the role change not waiting for the profile save |
| #174, Tristan P2: on web the role page has no way back to Lengkapi Profil | [`42d2020`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/42d20201) | [`ef55977`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef55977b), then [`a363412`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a363412f) | "Kembali returns to Lengkapi Profil without changing the role": no Kembali on the page |
| #238, Heraldo: the bulk dialog and toast word the void's consequence differently from the single dialog | [`5e8e160`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5e8e160d) | [`77e612e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/77e612ec) | "the success toast says the row is hidden, as the backend now does", and the bulk copy |
| #167, Heraldo: a docstring still said a void stays in the riwayat | — | [`72fc61c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/72fc61c5) `docs(ledger): [REFACTOR]` | Comment-only, so no red; the tests ran unchanged |

The race test reuses the harness from the earlier rounds. Only the paused writer is new:

```python title="tests/regression/identity/test_role_change_race.py"
def test_a_role_change_waits_for_a_profile_being_completed(self) -> None:
    # Review on #137 (Tristan P2): completing the profile commits the
    # account to its role, so a role change arriving mid-save must wait
    # for it and then be refused.
    user = User.objects.create_user(email="race-profile@example.com", role=User.Role.PENGELOLA)

    outcome = self._race(
        user,
        lambda u: OnboardingService.complete_profile(
            u, {"nama": "Ayu", "no_hp": "+628111111115"}
        ),
        (User, "save"),
        User.Role.NASABAH,
    )

    self._assert_role_kept(user, User.Role.PENGELOLA, outcome)
    self.assertTrue(user.is_profile_complete)
```

**Merges kept clean.** This week #137 took `staging` twice (13 and 16 Nov) and #174 three times (13 Nov, and twice on 16 Nov). Each merge commit carried only what already had tests, such as the migration renumbered to 0038 and then 0039, and the date-test fix. The two review fixes came afterwards, each as its own red/green pair.

## Positive, negative and corner cases

| Behaviour | Positive | Negative | Corner |
|---|---|---|---|
| `nasabah_id` filter (#175) | A valid UUID still filters all three lists | `abc`, `123` and a UUID with a bad last character get 422 with the key `nasabah_id` | `/aktivitas`, which already validated, keeps the same answer through the shared helper |
| Counted setoran (#176) | `waste_categories` counts the kept setoran | The architecture test fails on any hand-written status filter in `apps/` | The ledger model that owns the rule, and the tests, are excluded |
| Kode on edit (#177) | An item's own kode is accepted on `PUT` and `PATCH` | A NUL byte gets 422, not 500. Another item's kode gets 422 | A padded duplicate (`" HDPE "`) gets 422; the error messages stay Indonesian |
| Device token (#177) | A valid token is forgotten | A NUL token gets 422, not 500 | The delete still filters on the caller (unchanged code, not a new test) |
| Profile vs role change (#137) | A profile saved after a role change answers with the new role and `next_step` | A role change during a profile save waits, then is refused | Both orders tested, one on PostgreSQL with two threads |
| Kembali (#174) | Kembali returns to Lengkapi Profil without changing the role | Disabled while a role change is being sent | Only in account mode, where the page was pushed |
