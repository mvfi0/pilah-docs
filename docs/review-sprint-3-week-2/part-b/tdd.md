# Test Driven Development

!!! success "Competency level: 4"
    **Level 3 met:** every behaviour this week was built test-first, one behaviour per `[RED]` → `[GREEN]` pair, with the phase in every commit subject. A refactor came first where it made the change one edit (#168), and after green where cleanup was useful (#193).

    - Every changed line is covered: 100% on SonarCloud for every MR with lines to cover. #238 changes only copy and comments, so it has no coverable lines; its copy is pinned by a widget test.
    - The tests cover the positive case, the refusals and the corner cases (see [the table](#positive-negative-and-corner-cases)).
    - Tests that pass when written are labelled as such, never tagged `[RED]`.

    **Level 4:** advanced testing methods in the commits:

    - **A stub API with latency, to make a race deterministic:** the page tests run on a `StubApi` that answers per route, and a one-second `latency` holds the void in flight while the test taps outside, presses back, or closes the dialog by other means.
    - **Mutation checks on the review fixes:** on #193, undoing any one of the three dialog fixes makes exactly one test fail, so each test pins its own fix.
    - **Provider state asserted directly:** the tests read the Riverpod `ProviderContainer` after the void, including that screens never opened were never built.
    - **E2E with database checks:** Playwright drives the PIL-481 web build at desktop and phone sizes and reads the result back from the backend: 24/24.

## When each piece was done

Sprint 3 Week 2 runs from **Wed 4 Nov to Tue 10 Nov** (WIB), the IR due date. Every commit on this page was made on 4 or 9 Nov, before that deadline.

| Date (WIB) | Work | Commits |
|---|---|---|
| Wed 4 Nov, 17:20–17:31 | PIL-428, Heraldo's findings: the seed fix ([#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145)) and the in-flight dialog ([#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193)) | [`743ed1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/743ed1c3), [`abcafa3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/abcafa30), [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07), [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b) |
| Wed 4 Nov, 20:29–20:36 | PIL-428, Scallss's findings: the reload after a void and the spacing token ([#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193)) | [`6979612`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/69796129), [`be7b6d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/be7b6d06), [`b815354`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b815354f) |
| Mon 9 Nov, 14:58–15:04 | PIL-481 backend, three red/green pairs ([#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167)) | [`8143807`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8143807d) … [`646c0d1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/646c0d1c) |
| Mon 9 Nov, 15:16–15:24 | PIL-481 mobile copy ([#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238)) | [`da003a1`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/da003a1b), [`ff86f6f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ff86f6f4) |
| Mon 9 Nov, 16:16–16:18 | PIL-480, refactor first, then red and green ([#168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168)) | [`9dbfcf2`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9dbfcf26), [`3d83377`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3d833773), [`2b1fba9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2b1fba90) |
| **Tue 10 Nov** | **Due date** | — |

**Every commit belongs to a PR.** Each commit above was made in the PR it's listed with; none was pushed outside one.

**Not in this week:** Heraldo's fixes on [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) and [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) ([`72fc61c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/72fc61c5), [`5e8e160`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5e8e160d), [`77e612e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/77e612ec), 11 Nov) and the date-test cherry-pick. They are in [Sprint 3 Week 3](../../review-sprint-3-week-3/part-b/tdd.md).

**One date to know about the coverage proof.** SonarCloud couldn't analyse [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167), [#168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168) and [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) before the deadline, because their CI was red on a date-dependent test that also failed on `staging`. Their first analysis ran on 11 Nov, after the fix was cherry-picked. The coverage they show is still the 9 Nov code's: the 11 Nov commits changed only a docstring ([#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167)), the copy ([#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238)) and a test file, none of them coverable lines.

## Mocks, stubs and fakes in this week's tests

A test double stands in for a real collaborator so that a test controls it. A **stub** gives fixed answers, a **mock** is a generated stand-in for an interface, and a **fake** or **spy** is a small working version that also records what was done to it. Each double below has one job, and the code under test around it is real.

| Double | Kind | Replaces | Why it's needed | Used in |
|---|---|---|---|---|
| `StubApi` | Stub, at the HTTP boundary (Dio's `HttpClientAdapter`) | The backend | It answers each `METHOD path` with fixed JSON, and with `latency` set it delays every answer. The real network service, data sources, repositories, use cases and notifiers all still run, so only the server is fake. The one-second latency holds a void in flight while the test taps outside, presses back or closes the dialog | The three in-flight dialog tests and the reload tests on #193 |
| `_Feed` | Fake and spy (a subclass of `RiwayatAktivitasNotifier`) | The Riwayat feed | It starts with fixed rows and counts its `load()` calls. That lets a test assert the feed reloads exactly once after a void (`expect(feed.loads, 1)`), even when the dialog closed before the answer arrived | The #193 dialog tests |
| `_MockGetAktivitas`, `_MockExport` | Mocks (mocktail) | The two use cases the feed is built with | `_Feed` never calls them, but its constructor needs them. A mock fills the slot without a network | The #193 dialog tests |
| `dashboardProvider.overrideWith(...)`, `recentActivityProvider.overrideWith(...)` | Riverpod provider overrides, built on `StubApi` | The real wiring of the dashboard and recent-activity notifiers | The test decides which screens exist in the container, so it can check that open screens reload and that a screen never opened is never built | "a void also reloads the dashboard, recent activity and nasabah", "a void does not load screens that were never opened" |

**Where nothing is faked, on purpose.** The backend tests (#145, #167, #168) run on a real test database through Django's test client. What they check lives in the queries themselves: which rows a list returns, what a seed sums, what columns an export writes. A mocked ORM would only test the mock.

## Coverage proof at a glance

| MR | Work | Commits (WIB) | SonarCloud analysis (WIB) | New-code coverage | Quality gate |
|---|---|---|---|---|---|
| pilah-be [#145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) | PIL-428, final round (seed fix) | 4 Nov, 17:20–17:21 | 4 Nov, 20:20 | [100% of 95 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=145&metric=new_coverage&view=list) | Passed |
| pilah-mobile [#193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) | PIL-428, final round (dialog and reload) | 4 Nov, 17:29–20:36 | 4 Nov, 20:52 | [100% of 154 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-mobile&pullRequest=193&metric=new_coverage&view=list) | Passed |
| pilah-be [#167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167) | PIL-481: lists leave a void out | 9 Nov, 14:58–15:04 | 11 Nov, 20:21 (CI blocked until then) | [100% of 7 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=167&metric=new_coverage&view=list) | Passed |
| pilah-mobile [#238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238) | PIL-481: the Hapus copy | 9 Nov, 15:16–15:24 | 11 Nov, 20:45 | No coverable lines (copy and comments only); pinned by a widget test | Passed |
| pilah-be [#168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168) | PIL-480: export without ID Aktivitas | 9 Nov, 16:16–16:18 | 11 Nov, 20:39 (CI blocked until then) | [100% of 2 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-be&pullRequest=168&metric=new_coverage&view=list) | Passed |

The figures are from the SonarCloud API (`api/measures/component` with `pullRequest=<n>`), read on 19 Nov; the analysis times are from `api/project_pull_requests/list`. #145 and #193 add the 4 Nov commits to the coverage shown in [Sprint 3 Week 1](../../review-sprint-3-week-1/part-b/tdd.md).

## PIL-428, the final review round (4 Nov)

Committed on Wed 4 Nov, 17:20–20:36.

| Finding | Red | Green | What the red asserts |
|---|---|---|---|
| Re-seeding after a void puts the voided money back into the saldo (Heraldo, #145) | [`743ed1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/743ed1c3) | [`abcafa3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/abcafa30) | For each seed command, `test_reseed_leaves_a_voided_setoran_out_of_the_saldo`: seed, void a seeded setoran, seed again, and the saldo still equals the counted setoran only |
| The Hapus dialog can be closed while the void is in flight, then skips the refresh (Heraldo, #193) | [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07) | [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b) | Three tests, below |
| A void leaves the dashboard, recent activity and nasabah list stale (Scallss, #193) | [`6979612`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/69796129) | [`be7b6d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/be7b6d06) | "a void also reloads the dashboard, recent activity and nasabah", and "a void does not load screens that were never opened" |

**Refactor after green:** [`b815354`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b815354f) replaces a bare `12` with `AppSpacing.md` (Scallss's nit).

**A third bug, found by writing the test.** Heraldo found two problems; the red commit has three tests. The third came from writing the second: if the server answers while the dialog is still animating closed, the dialog's `Navigator.pop` closes the Riwayat page underneath it. The green guards the pop on the route still being on top.

```dart title="test/features/transaksi/presentation/widgets/batalkan_setoran_flow_test.dart"
testWidgets(
    'while the void is in flight, a tap outside or back keeps the dialog',
    (tester) async {
  api
    ..latency = const Duration(seconds: 1)
    ..on('POST', _batalkan, json: _dibatalkan());
  await pumpFeed(tester);
  await openHapus(tester);
  await tester.enterText(
      find.byKey(BatalkanSetoranDialog.alasanKey), 'Dobel');
  await tester.tap(confirm());
  await tester.pump(const Duration(milliseconds: 100));

  await tester.tapAt(const Offset(5, 5));
  await tester.pump(const Duration(milliseconds: 300));
  await tester.binding.handlePopRoute();
  // Past any dialog exit animation, before the answer arrives.
  await tester.pump(const Duration(milliseconds: 300));

  expect(find.text('Hapus Setoran?'), findsOneWidget);
  await tester.pumpAndSettle(const Duration(seconds: 1));
  expect(find.text('Hapus Setoran?'), findsNothing);
  expect(feed.loads, 1);
  expect(find.byType(AktivitasListView), findsOneWidget);
});
```

The `latency` on the stub API is what makes this deterministic. Without it the answer would arrive in the same frame as the tap, and the race could not be staged.

## PIL-481: a voided setoran leaves every list (9 Nov)

Committed on Mon 9 Nov, 14:58–15:24.

Backend, [pilah-be #167](https://github.com/bank-sampah-PILAH/pilah-be/pull/167):

| Behaviour | Red | Green | Tests |
|---|---|---|---|
| The riwayat feed leaves a voided setoran out, and its summary is unchanged | [`8143807`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8143807d) | [`6995649`](https://github.com/bank-sampah-PILAH/pilah-be/commit/69956494) | `test_riwayat_leaves_the_voided_setoran_out_and_the_summary_stays_the_same`, `test_nasabah_riwayat_with_a_type_filter_leaves_the_voided_setoran_out` |
| The setoran list and the dashboard's recent list leave it out; its detail by id still shows the void | [`7d0922d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7d0922d7) | [`4738088`](https://github.com/bank-sampah-PILAH/pilah-be/commit/47380886) | `test_setoran_list_leaves_the_voided_setoran_out`, `test_recent_transactions_leave_the_voided_setoran_out`, `test_a_voided_setoran_stays_reachable_by_its_id_with_its_void` |
| The nasabah beranda and riwayat leave it out; the nasabah can still open it by id | [`4401e4e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/4401e4e2) | [`c3606b5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c3606b52) | `test_nasabah_beranda_leaves_the_voided_setoran_out`, `test_nasabah_riwayat_without_a_type_filter_leaves_the_voided_setoran_out`, `test_nasabah_can_still_open_the_voided_setoran_by_its_id` |

The "still reachable by id" tests are guards that passed in their red commits on purpose. They are there so the fix can't overreach by filtering the shared lookup that detail, edit and void also read. The commits say so.

Mobile, [pilah-mobile #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238): red [`da003a1`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/da003a1b), green [`ff86f6f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ff86f6f4). The single and bulk Hapus dialogs and the toast now say the setoran is hidden from the riwayat, not kept there with a label.

## PIL-480: the export without ID Aktivitas (9 Nov)

Committed on Mon 9 Nov, 16:16–16:18.

[pilah-be #168](https://github.com/bank-sampah-PILAH/pilah-be/pull/168), refactor first, so the change is one edit:

| Step | Commit | Result |
|---|---|---|
| Refactor the tests: two export tests counted events through the ID Aktivitas column (`row[13]`). They now count an event as a row that carries a value | [`9dbfcf2`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9dbfcf26) | Green before and after, no behaviour change |
| Red: `test_raw_sheet_leaves_out_the_activity_id_and_keeps_the_other_columns` pins the 13 remaining headers in order, the title rows merged over `A:M`, and no setoran or pencairan id in any cell | [`3d83377`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3d833773) | Fails while the sheet still ends with "ID Aktivitas" |
| Green: drop the column, and move the title merges and widths from `A:N` to `A:M` | [`2b1fba9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2b1fba90) | Passes |

Without the refactor, removing the column would also have broken two tests that used it only to count rows, mixing an unrelated failure into the red step.

## Positive, negative and corner cases

| Behaviour | Positive | Negative | Corner |
|---|---|---|---|
| Re-seed after a void (#145) | The saldo equals the counted setoran | The voided total is not added back | Both seed commands, each with its own test |
| Hapus while in flight (#193) | The answer closes the dialog and refreshes once | A barrier tap or the back button does nothing while sending | The dialog closed by other means still refreshes on success; an answer during the exit animation leaves the Riwayat page open |
| Reload after a void (#193) | The dashboard, recent activity and nasabah list reload when open | — | Screens never opened are not built (`container.exists`) |
| Lists leave a void out (#167) | Feed, setoran list, dashboard recent, nasabah beranda and riwayat omit it | The summaries are unchanged; a nasabah sees only their own rows | The detail by id still answers 200 with the void's who, when and why, for the pengurus and the nasabah |
| Export (#168) | 13 columns, no ID Aktivitas | — | All three row shapes (pencairan, setoran without items, item rows) carry 13 values; the titles merge over `A1:M1` |

## E2E (Playwright)

PIL-481, **24/24 checks**, run against `flutter build web --profile` and the #167 backend, at 1440×900 and 390×844. Each run creates two fresh setoran and voids one through the UI. It checks the dialog wording, that the voided row leaves the riwayat while the other stays, and that no row is labelled Dibatalkan. Then, through the API and the database, it checks who voided it, the saldo, that the lists omit it, and that its detail by id still answers with the void. The screenshots are in the [#238 description](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238).
