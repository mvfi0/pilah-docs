# Test Driven Development

!!! success "Competency level: 4"
    **Level 3 met:** the new behaviour this week was built test-first, with the phase in every commit subject. In [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) each `[GREEN]` commit came only after its `[RED]` commit, and the `[REFACTOR]` only after green.

    - Every changed line is covered: SonarCloud reports 100% of #276's 72 new lines. [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) adds tests only, so it has no lines to cover.
    - The tests cover the positive case, each refusal and the corner cases (see [the table](#positive-negative-and-corner-cases)).
    - **#185 has no red phase, on purpose.** Its five tests pin behaviour the backend already had, for the app to rely on. They passed when written, so their subjects carry no `[RED]` tag, and the PR description says so.

    **Level 4:** advanced testing methods, for test isolation:

    - **A mock and two fakes** (mocktail): the onboarding API client is a mock, and two request types are fakes registered as fallback values, so `any()` can match them.
    - **Two recording test notifiers:** one records each `load` call with its `silent` flag, the other each authentication call. The tests assert what was **not** called (no `refreshUser`, no `logout`), not only what was.
    - **A real router, isolated:** a `GoRouter` built on the app's own `rootNavigatorKey`, so the toast raised after navigation has a navigator, as it does in the app.

## When each piece was done

Sprint 4 Week 1 runs from **Wed 18 Nov to Tue 24 Nov** (WIB), the IR due date. Every commit and every SonarCloud analysis on this page falls inside that range.

| Date (WIB) | Work | Commits |
|---|---|---|
| Wed 18 Nov, 23:27–23:31 | [#185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185), PIL-539 backend: five regression tests | [`499b32b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/499b32bb) … [`c2014bd`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2014bd7) |
| Sun 22 Nov, 23:12–23:45 | [#276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276), PIL-539 mobile: four red/green pairs and a refactor | [`17de7e3`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17de7e3f) … [`41a4434`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/41a44349) |
| Mon 23 Nov, 17:27 | #276: `staging` merged in after #267 landed | [`cf89110`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cf89110f) |
| **Tue 24 Nov** | **Due date** | — |

**Every app commit belongs to a PR.** Each commit above was made in the PR it's listed with. The commits outside a PR are in this documentation repo, which is pushed straight to `main`: the IR pages and the [ZAP report](../../security/zap-2026-11-23.md). The ZAP driver's fix (`tools/zap_scan.py`) is checked by the rerun scan, not by a unit test.

**Not in this week:** PIL-541 and PIL-542 ([pilah-be #202](https://github.com/bank-sampah-PILAH/pilah-be/pull/202), [#203](https://github.com/bank-sampah-PILAH/pilah-be/pull/203)), committed on 25–26 Nov. They belong to the next week.

## Mocks, stubs and fakes in this week's tests

A test double stands in for a real collaborator so that a test controls it. A **stub** gives fixed answers, a **mock** is a generated stand-in for an interface, a **fake** is a working stand-in, and a **spy** records how it was called. Each double below has one job, and the code under test around it is real.

| Double | Kind | Replaces | Why it's needed | Used in |
|---|---|---|---|---|
| `_MockOnboardingDataSource` | Mock (mocktail) | `OnboardingRemoteDataSource`, the API client | Each test sets the answer to `registerNasabah` and `loadMyMemberships`: a membership list, a 201, or the server's duplicate refusal. No network is reached. `verify(...).captured.single` shows exactly one application was sent, for the picked bank, and `verifyNever(completeProfile)` that no profile was | `register_nasabah_additional_test.dart` |
| `_FakeRegisterNasabahRequest`, `_FakeCompleteProfileRequest` | Fakes (mocktail) | The two request objects | mocktail needs a fallback value of each type before `any()` can match it. Registering them is what lets one test assert that **no** profile request was sent | `register_nasabah_additional_test.dart` |
| `TestNasabahApprovalNotifier` | Fake and spy | `NasabahApprovalNotifier` | It starts from a fixed list state and records every `load`, with its `silent` flag, in `loadCalls`. The test asserts `[true]` after a submitted application and `[]` after going back without one | `ajukan_bank_baru_test.dart` |
| `TestAuthenticationNotifier` | Fake and spy | The authentication notifier | It holds a signed-in nasabah and records calls in `auth.calls`. Two tests assert that back and system back never call `logout`, and one that the in-app submit doesn't call `refreshUser` | `register_nasabah_additional_test.dart` |
| A stub route at `/ajukan-bank-sampah` | Stub route | The real registration form | It shows a "submitted" button that pops `true`. The list page's reload is tested on its own, without building the form | `ajukan_bank_baru_test.dart` |
| A `GoRouter` on `rootNavigatorKey` | The real router, built for the test | The app's router | `router.push<bool>(...)` returns the page's result to the test, as it does to Bank sampah saya. The app's `rootNavigatorKey` is needed because the "Pengajuan terkirim" toast is raised after navigation, on that navigator | `register_nasabah_additional_test.dart` |

**Where nothing is faked, on purpose.** #185 runs on a real test database and signs in with real JWTs. The rules it pins live in the database and the services: one membership row per bank, a pending membership's saldo refused, each bank's pengurus deciding only its own applications. Faking any of them would test nothing.

## Coverage proof at a glance

| MR | Work | Commits (WIB) | SonarCloud analysis (WIB) | New-code coverage | Quality gate |
|---|---|---|---|---|---|
| pilah-mobile [#276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) | PIL-539: Ajukan bank baru | 22 Nov, 23:12–23:45; merge 23 Nov, 17:27 | 23 Nov, 17:43 | [100% of 72 lines](https://sonarcloud.io/component_measures?id=bank-sampah-PILAH_pilah-mobile&pullRequest=276&metric=new_coverage&view=list) | Passed |
| pilah-be [#185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) | PIL-539: regression tests | 18 Nov, 23:27–23:31 | 18 Nov, 23:48 | No lines to cover (tests only) | Passed |

The figures are from the SonarCloud API (`api/measures/component`), read on 26 Nov, for each PR's last analysis, which in both cases ran before the 24 Nov deadline. The analysis times are from `api/project_pull_requests/list`.

## [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276), PIL-539 mobile

Committed on Sun 22 Nov, 23:12–23:45.

| Step | Commit | What the red commit's tests failed on |
|---|---|---|
| Red | [`17de7e3`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17de7e3f) | Three tests fail because Bank sampah saya has no "Ajukan bank baru" yet. The guard that an account with no membership isn't offered it passes |
| Green | [`9c7ecac`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9c7ecac2) | The button pushes the form, and a pop with `true` reloads the list silently |
| Red | [`90da8e6`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/90da8e68) | The form opened from the app is still the onboarding step: stepper, Keluar, and the one-membership lock |
| Green | [`8cb88a0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8cb88a07) | `RegisterNasabahMode.additional` at `/ajukan-bank-sampah`: an app page with a back button and no lock |
| Red | [`05c5b77`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/05c5b773) | The picker hides joined banks, so none is listed, marked or refused |
| Green | [`6a4c4ed`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6a4c4ed0) | Joined banks stay in the list, greyed, with their status, and can't be picked |
| Red | [`874d72c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/874d72c8) | Submitting from the app follows the onboarding path: profile draft, session refresh, redirect |
| Green | [`b34db8b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b34db8be) | The in-app submit sends only the application, pops `true` and shows "Pengajuan terkirim" |
| Refactor | [`41a4434`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/41a44349) | Spacing on the scale moved to `AppSpacing`; the 130 onboarding page tests pass before and after |

One existing test changed meaning, in the red commit that changes the behaviour: `pilih_bank_sampah_bottom_sheet_test.dart` pinned "hides banks the nasabah already joined". It now pins the new rule: the bank is listed, its status replaces its address, and tapping it keeps the sheet open.

```dart title="test/features/bank_sampah_approval/presentation/pages/ajukan_bank_baru_test.dart"
testWidgets('a submitted application reloads the list on the way back',
    (tester) async {
  final (notifier, _) =
      await pumpList(tester, const NasabahApprovalLoaded([_approved]));

  await tester.tap(find.text('Ajukan bank baru'));
  await tester.pumpAndSettle();
  notifier.loadCalls.clear();
  await tester.tap(find.text('submitted'));
  await tester.pumpAndSettle();

  expect(find.text('Bank Sampah Lestari'), findsOneWidget);
  expect(notifier.loadCalls, [true]);
});
```

`submitted` is a button on a stub route that stands in for the form at `/ajukan-bank-sampah`. It pops `true`, as the form does after a successful application, so the list page is tested without building the form.

```dart title="test/features/onboarding/presentation/pages/register_nasabah_additional_test.dart"
testWidgets(
    'sends only the membership request and returns to Bank sampah saya',
    (tester) async {
  when(() => dataSource.registerNasabah(any())).thenAnswer(
      (_) async => const OnboardingResult(nextStep: 'nasabah_dashboard'));
  await pumpFromList(tester);
  await pickBankB(tester);

  await tester.tap(find.text('Ajukan Pendaftaran'));
  await pumpToast(tester);

  final request = verify(() => dataSource.registerNasabah(captureAny()))
      .captured
      .single as RegisterNasabahRequest;
  expect(request.bankSampahId, 'bank-b');
  verifyNever(() => dataSource.completeProfile(any()));
  expect(find.text('BANK SAMPAH SAYA'), findsOneWidget);
  expect(find.text('Pengajuan terkirim'), findsOneWidget);
  expect(await pushed, isTrue);
  // The account is already signed in and onboarded: applying to another
  // bank does not touch its session.
  expect(auth.calls, isNot(contains('refreshUser')));
  await settleToasts(tester);
});
```

**After the `staging` merge** ([`cf89110`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cf89110f), 23 Nov). `staging` had redesigned the onboarding step in the meantime. The merge kept the new layout for onboarding and the in-app form as it was. Then the 413 tests in `onboarding`, `bank_sampah_approval` and `core/router` were run again: all passed, and `flutter analyze` was clean.

## [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185), PIL-539 backend

Committed on Wed 18 Nov, 23:27–23:31. One test per commit, each naming the OWASP category it guards.

| Commit | Test | What it pins |
|---|---|---|
| [`499b32b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/499b32bb) | `test_applying_to_a_second_bank_waits_while_the_first_stays_open` | The new membership is pending; the first bank's saldo still opens (200), the pending one's is refused (403) |
| [`b97596a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b97596a7) | `test_only_the_second_banks_pengurus_can_decide_the_application` | The first bank's pengurus gets 404 on approve and reject; the second bank's pengurus approves |
| [`261a571`](https://github.com/bank-sampah-PILAH/pilah-be/commit/261a5710) | `test_a_rejection_at_the_second_bank_leaves_the_first_open_and_can_be_appealed` | A rejection at the second bank doesn't touch the first, and reapplying makes it pending again |
| [`2abe793`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2abe7937) | `test_once_approved_the_second_bank_is_a_choice_with_its_own_saldo` | With two approved memberships, an unselected saldo is a 422 listing both; a setoran at the first bank gives "7000.00" there and leaves the second at "0.00" |
| [`c2014bd`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2014bd7) | `test_a_duplicate_application_names_the_reason` | A second application to the same bank is a 400 with "Anda sudah terdaftar sebagai nasabah di bank sampah ini" |

**Why these tests came first.** The app removes its own one-bank lock in #276. These tests make sure the server still holds every rule that lock used to hint at, before the app relies on it. Heraldo approved on 19 Nov ("Tests-only PR, no production code touched").

## Positive, negative and corner cases

| Behaviour | Positive | Negative | Corner |
|---|---|---|---|
| Ajukan bank baru (#276) | A loaded list with a membership offers the button, and a submitted application reloads it | Going back without applying doesn't reload | An account with no membership keeps its empty state and no button |
| The in-app form (#276) | Opens as a page of the app; an existing membership doesn't lock it | Back and system back return to Bank sampah saya without asking to log out | Asks for a bank before sending anything |
| The picker (#276) | A bank not joined yet can be picked | A joined bank is listed, marked and can't be picked | A pending or rejected application is marked too, with its own label |
| Submitting (#276) | Sends only the membership request, returns `true` and toasts | The server's duplicate message is shown and the form stays open | No profile request and no session refresh |
| Second bank (#185) | Applying waits as pending while the first bank stays open | The first bank's pengurus can't decide it; a duplicate is a 400 | A rejection can be appealed; two approved banks need a choice of saldo |
