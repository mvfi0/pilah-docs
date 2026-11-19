# Software Methodology: TDD

!!! success "Competency level: 3"
    - Part B TDD at 3 or above for seven weeks running, 15 Sep – 3 Nov.
    - Three features built test-first, on both the backend and the app.
    - Each behaviour tested with positive, negative and corner cases.
    - Mocks, stubs and dummy data used for test isolation, following F.I.R.S.T.

## What TDD means

**Test-Driven Development** means writing the test *before* the code it tests. The test describes the behaviour I want, and the code is written only to make that test pass. Each behaviour goes through a short cycle:

1. **Red:** write a test for one behaviour and run it. It fails, because the behaviour doesn't exist yet.
2. **Green:** write the least code that makes the test pass.
3. **Refactor:** clean up the code while every test stays green.

The tests then become a safety net: any later change that breaks a behaviour turns its test red straight away. In PILAH each step is its own commit, tagged in the subject: `test(...): [RED] …`, `feat(...): [GREEN] …`, `refactor(...): [REFACTOR] …`.

## Part B TDD: 3 or above for over a month

| Week | Part B TDD | Page |
|---|---|---|
| Sprint 1 Week 1 (15–22 Sep) | 4 (given by the assessor) | [TDD, S1W1](../review/part-b/tdd.md) |
| Sprint 1 Week 2 (23–29 Sep) | 4 | [TDD, S1W2](../review-week-2/part-b/tdd.md) |
| Sprint 1 Week 3 | 4 | [TDD, S1W3](../review-week-3/part-b/tdd.md) |
| Sprint 2 Week 1 (6–12 Oct) | 4 | [TDD, S2W1](../review-sprint-2-week-1/part-b/tdd.md) |
| Sprint 2 Week 2 | 4 | [TDD, S2W2](../review-sprint-2-week-2/part-b/tdd.md) |
| Sprint 2 Week 3 | 4 | [TDD, S2W3](../review-sprint-2-week-3/part-b/tdd.md) |
| Sprint 3 Week 1 (31 Oct – 3 Nov) | 4 | [TDD, S3W1](../review-sprint-3-week-1/part-b/tdd.md) |

## Three features built with TDD

| Feature | Backend | App | Red → green commits |
|---|---|---|---|
| **1. Pencairan** (PIL-176): record a payout, lowering the nasabah's saldo | [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | [S1W1, backend](../review/part-b/tdd.md#backend-pilah-be-19) |
| **2. Scheduled prices** (PIL-304): change a jenis sampah's price now or from a future date | [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) | [pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) | [S1W3, backend](../review-week-3/part-b/tdd.md#backend-pil-304-pilah-be-79) · [S1W3, app](../review-week-3/part-b/tdd.md#mobile-pil-304-pilah-mobile-62) |
| **3. Void a setoran** (PIL-428): cancel a recorded setoran, with who, when and why | [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) | [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) | [S3W1, backend](../review-sprint-3-week-1/part-b/tdd.md#backend-pilah-be-145) · [S3W1, app](../review-sprint-3-week-1/part-b/tdd.md#mobile-pilah-mobile-193) |

## Positive, negative and corner cases

| Case | Meaning |
|---|---|
| **Positive** | Valid input: the feature does what it should |
| **Negative** | Invalid input or a forbidden action: the feature refuses it and changes nothing |
| **Corner** | The extreme valid inputs: the very first and very last values of the allowed range, and the ones right next to them. Bugs hide at the edges, for example `<` written where `<=` was meant |

**Example.** An input accepts whole numbers from **1 to 10**:

- **Positive:** a normal value such as 5.
- **Negative:** values outside the range, such as 0 and 11.
- **Corner:** the two ends, **1 and 10**, and the values just inside them, **2 and 9**.

In PILAH:

| Feature | Positive | Negative | Corner |
|---|---|---|---|
| Pencairan, where the nominal must be between 1 and the saldo ([S1W1 backend](../review/part-b/tdd.md#backend-test-cases), [app](../review/part-b/tdd.md#mobile-test-cases)) | A normal nominal is recorded and the saldo drops once | A nominal of 0, below 0, or above the saldo is refused, and the saldo is unchanged | A nominal **exactly equal to the saldo** is accepted (the top end of the range) |
| Price history ([S2W1](../review-sprint-2-week-1/part-b/tdd.md#positive-negative-and-corner-cases)) | Versions listed newest first | Another bank's jenis gets 404; a nasabah gets 403 | **No versions at all** (the start of the range) and **more than 100 versions** (the far end) |
| Void a setoran ([S3W1](../review-sprint-3-week-1/part-b/tdd.md#positive-negative-and-corner-cases)) | Void recorded, saldo reduced | No alasan gets 422; a setoran already voided gets 409; money already paid out (the saldo would go below 0) gets 409 | Voiding the only setoran takes the saldo to **exactly 0**, which is allowed. A void that would leave a *later* pencairan unfunded is refused, even though the final saldo stays positive |

## Stub vs mock

Both are **test doubles**: stand-ins for a real dependency, so a test can run one unit without the units it calls.

| | Stub | Mock |
|---|---|---|
| **What it does** | Returns a **prepared answer** when it is called | **Records how it was called**, so the test can check the calls |
| **What the test checks** | The *result* of the unit under test (its state or its output) | The *interaction*: was the dependency called, how often, with what arguments |
| **In mocktail (Flutter)** | `when(() => repo.getHistory(...)).thenAnswer((_) async => versions)` | `verify(() => network.patch(captureAny())).called(1)` and `verifyNever(...)` |
| **In Python** | `unittest.mock.patch(...)` with a `return_value` | `mock.assert_called_once_with(...)` |

### When I use each

- **A stub, when the unit needs an input from its dependency.** For example, the price-history cubit needs a list of versions from the use case. The stub hands it a fixed list, and the test checks what the cubit shows.
- **A mock, when the thing I'm testing *is* the call.** For example, the repository must send the right PATCH body to the server. The mock captures the request, and the test checks its body, including the UTC offset of a local midnight ([`f04bb89`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f04bb89)). Another example: on invalid input, nothing may be sent, which `verifyNever` checks.
- **Neither, when the dependency is the behaviour under test.** The backend tests run against a real test database, because row locks, check constraints and the saldo replay only exist in the database. A mocked database would pass while the real query is wrong.

## Why use stubs and mocks

1. **Isolation.** When a test fails, the failure is in the one unit under test, not somewhere in the layers below it.
2. **No slow or unavailable dependencies.** App tests don't need a running server, a network or a signed-in Google account.
3. **Situations that are hard to make for real.** A stub can return a 409 conflict, a timeout, a malformed response, or two responses in reverse order. In the PIL-304 app, `Completer`s answer the newer request first, to prove an old reload can't overwrite a newer price ([#62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62)).
4. **Checking side effects that have no return value,** such as a request being sent once, or not at all.
5. **Building test-first, top down.** A cubit can be built and tested before the repository below it exists, by stubbing the repository.

## Why dummy data, not real data

A test that reads real data **depends** on something it doesn't control. Real data is whatever happens to be in the production database, or on a server, right now. That dependency breaks tests in four ways:

| Problem with real data | What happens to the test | With dummy data |
|---|---|---|
| **It changes.** Someone records a setoran, and a saldo moves | The same test passes today and fails tomorrow, with no code change | The test creates its own data, so the input is always the same |
| **It may not contain the case.** No nasabah has a saldo exactly equal to the nominal I want to test | The corner case can't be tested at all | The test creates exactly the case it needs: a saldo of 50,000 and a nominal of 50,000 |
| **It belongs to others.** Tests that write would change or delete real records, and other tests share them | Tests interfere with each other and with real users | Each backend test runs in its own test database, rolled back after every test |
| **It is personal.** Real nasabah have names, phone numbers and saldo | Personal data ends up in test code, logs and CI | Dummy values: "Bank Void", nasabah "Budi", `void@example.test`, `+628111111111` |

Dummy data does for data what a stub does for code: it **removes the dependency**, so the test depends only on itself. In PILAH:

- **Backend:** each test's `setUp` creates its own bank, pengelola, nasabah and jenis sampah, then records a setoran through the API ([`test_setoran_void.py`](https://github.com/bank-sampah-PILAH/pilah-be/blob/staging/apps/ledger/test_setoran_void.py)). Everything runs in a test database Django creates fresh for the run.
- **App:** tests feed canned JSON through mocks or a stub API.

The one place real data is used is a manual check outside the test suite. A migration was run forwards, backwards and forwards again on a restored copy of the production database, because the question there was precisely "does this work on the real data?"

## The F.I.R.S.T. principle

Five properties of good unit tests:

| Letter | Meaning | In PILAH |
|---|---|---|
| **F**ast | Tests run in milliseconds, so they can run after every change | App tests use mocks and stub APIs, with no server. Backend tests roll back a transaction instead of rebuilding the database |
| **I**ndependent | No test depends on another test or on the order they run in | Each test creates its own data, for example a fresh user per test, and shares nothing with the others |
| **R**epeatable | The same result every run, on any machine, at any time | <ul><li>Time is injected (`now: () => DateTime(2026, 10, 7, 10)`), so a date test doesn't depend on today.</li><li>`Completer`s fix the order of async answers instead of timing them.</li><li>A sort that passed only 6 runs in 10 was made deterministic and then passed 10 in 10 ([`7ff2cdf`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7ff2cdf) → [`765f90f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/765f90f)).</li></ul> |
| **S**elf-validating | The test decides pass or fail by itself; nobody reads its output | Every test asserts exact values: the status code, the saldo, the request body. A test that passed when written was proven by breaking the code and watching it fail |
| **T**imely | The test is written at the right time: before the code | The `[RED]` commit is pushed before the `[GREEN]` one. Tests written after the code are labelled as coverage tests, not presented as TDD |
