# Software Methodology: TDD

!!! success "Competency level: 3"
    - Three features of PILAH built test-first, each on both the backend (pilah-be) and the app (pilah-mobile, phone and web):
        - **pencairan** (PIL-176);
        - **scheduled prices** (PIL-304);
        - **void a setoran** (PIL-428).
    - **50 red → green pairs** across six merge requests: 29 on the backend, 21 on the app.
    - Changed lines covered at 100% in five of the six MRs; the sixth was closed to 100% a week later.
    - Each behaviour tested with positive, negative and corner cases.
    - Part B TDD at 3 or above for seven weeks running.
    - **11 defects caught by a failing test before merge**, each now guarded by that test.

Contents:

1. [What TDD means](#1-what-tdd-means)
2. [The three features](#2-the-three-features)
3. [TDD commit flow, with evidence of the order](#3-tdd-commit-flow-with-evidence-of-the-order)
4. [Coverage](#4-coverage)
5. [Part B record](#5-part-b-record)
6. [Positive, negative and corner cases](#6-positive-negative-and-corner-cases)
7. [Benefits of TDD, from development data](#7-benefits-of-tdd-from-development-data)
8. [Tools and methods](#8-tools-and-methods)
9. [Test isolation: stubs, mocks and dummy data](#9-test-isolation-stubs-mocks-and-dummy-data)
10. [The F.I.R.S.T. principle](#10-the-first-principle)
11. [Mapping to the rubric](#11-mapping-to-the-rubric)
12. [Appendix: test code](#appendix-test-code)

## 1. What TDD means

**Test-Driven Development** means writing the test *before* the code it tests. The test describes the behaviour I want, and the code is written only to make that test pass. Each behaviour goes through a short cycle:

1. **Red:** write a test for one behaviour and run it. It fails, because the behaviour doesn't exist yet.
2. **Green:** write the least code that makes the test pass.
3. **Refactor:** clean up the code while every test stays green.

The cycle repeats, one behaviour at a time, until the feature is done. The tests then stay in the project as a safety net: any later change that breaks a behaviour turns its test red straight away.

In PILAH each step is its own commit, so the order can be checked in the history:

- `test(...): [RED] …` adds only the failing test;
- `feat(...): [GREEN] …` or `fix(...): [GREEN] …` adds the code that makes it pass;
- `refactor(...): [REFACTOR] …` comes only after green.

The Sprint 1 commits (PIL-176) name the phase in words, as "add failing test for …"; the bracketed tags start with the next feature. A test that already passes when written is committed as a coverage test (`test(...): cover …`) with no phase tag, so it is never presented as a red.

## 2. The three features

| # | Feature | What it does | Backend MR | App MR | Built |
|---|---|---|---|---|---|
| 1 | **Pencairan** (PIL-176) | A pengurus records a payout to a nasabah. The nasabah's saldo drops by the nominal, and the saldo history and exports account for it | [pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19) | [pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26) | 20–22 Sep |
| 2 | **Scheduled prices** (PIL-304) | A jenis sampah's price becomes a history of versions. A change applies now or from a future date, and each setoran is priced at the version in effect on its date | [pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79) | [pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62) | 7–12 Oct |
| 3 | **Void a setoran** (PIL-428) | A pengurus cancels a recorded setoran with a reason. The row stays, marked "dibatalkan", and its total leaves the saldo, the history and every report | [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) | [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) | 31 Oct – 2 Nov |

## 3. TDD commit flow, with evidence of the order

Each table lists the pairs in the order they were committed. The numbers in brackets are lines added and removed by that commit, from `git show --shortstat`. Every red commit changes only test files.

### 3.1 Pencairan, backend ([pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19))

| # | Behaviour | Red | Green |
|---|---|---|---|
| 1 | Recording a pencairan lowers the saldo exactly once | [`475f2b5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/475f2b5) (+48) | [`f119442`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f119442) (+171 −1) |
| 2 | A nominal above the saldo is rejected, and the saldo is unchanged | [`cb1b774`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cb1b774) (+18) | [`1cf5641`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1cf5641) (+3) |
| 3 | A zero, negative or decimal nominal and a future `tanggal` are rejected | [`8435245`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8435245) (+40 −1) | [`6461112`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6461112) (+13) |
| 4 | The detail is readable only within the bank (404, 403, 401) | [`92b062a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/92b062a) (+83) | [`3ac5602`](https://github.com/bank-sampah-PILAH/pilah-be/commit/3ac5602) (+3) |
| 5 | The saldo history subtracts pencairan | [`55134c3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/55134c3) (+43) | [`da84166`](https://github.com/bank-sampah-PILAH/pilah-be/commit/da84166) (+114 −34) |
| 6 | The list can be filtered by nasabah | [`2c633e1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2c633e1) (+27) | [`c0fad99`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c0fad99) (+13 −1) |
| 7 | *Review finding:* a pending or rejected nasabah can't be paid out | [`8eae32e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8eae32e) (+20) | [`96be7bd`](https://github.com/bank-sampah-PILAH/pilah-be/commit/96be7bd) (+6 −1) |
| 8 | *Review finding:* a setoran and a pencairan at the same instant are ordered the same way every time | [`17a6938`](https://github.com/bank-sampah-PILAH/pilah-be/commit/17a6938) (+38) | [`1bd2a1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1bd2a1c) (+4 −2) |
| 9 | *Review finding:* a legacy saldo with sen is rounded down to whole rupiah | [`6a66617`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6a66617) (+15) | [`8801c68`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8801c68) (+6 −3) |
| 10 | The reset command reports pencairan left behind | [`cadc57e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cadc57e) (+54 −1) | [`f1c1edf`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f1c1edf) (+2 −1) |

**Refactor after green:** [`d244c36`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d244c36) removes a list branch no request could reach (+3 −6).

**The order as GitHub shows it.** Tristan rebased the branch onto `staging` before merging it on 27 Sep, so the commits carry new hashes. The hashes in the table are the ones in the [PR's commit list](https://github.com/bank-sampah-PILAH/pilah-be/pull/19/commits). The screenshot shows the review-round part of that list, pairs 7 to 10 and the refactor: each failing test comes directly before the fix that makes it pass, and the refactor comes only after green.

![The commit list of pilah-be #19, merged by TrayMachi into staging: "test(pencairan): add failing test for unapproved membership" (8eae32e) then "fix(pencairan): require approved membership like setoran" (96be7bd); the same-instant ordering pair (17a6938, 1bd2a1c); the legacy sen saldo pair (6a66617, 8801c68); "refactor(pencairan): drop unreachable unpaginated list branch" (d244c36); then "test(reset): add failing test for pencairan in reset verification" (cadc57e)](evidence/pilah-be-19-commits.png){ width="900" }

One commit sits between pair 1's red and green: [`023d070`](https://github.com/bank-sampah-PILAH/pilah-be/commit/023d070) corrects one assertion in the red test. The saldo endpoint returns `total_saldo` as the string `"265600.00"`, not a `Decimal`, so the old assertion would have failed even with correct code.

### 3.2 Pencairan, app ([pilah-mobile #26](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/26))

| # | Behaviour | Red | Green |
|---|---|---|---|
| 1 | The nominal is validated against the saldo | [`27fcd06`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/27fcd06) (+39) | [`869ae71`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/869ae71) (+14) |
| 2 | The saldo is read, and the pencairan is posted with the right body | [`02ddd84`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/02ddd84) (+146) | [`dcb7e48`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/dcb7e48) (+156 −35) |
| 3 | The form cubit loads the saldo, submits, and ignores a double tap | [`6f90aab`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6f90aab) (+179) | [`2eaca63`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2eaca63) (+100 −25) |
| 4 | The form asks for confirmation, shows a success sheet, and shows a server error inline | [`9887d7e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9887d7e) (+176) | [`e30e6ab`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/e30e6ab) (+399 −4) |
| 5 | The nasabah detail sheet opens the form, for an active nasabah only | [`add3e87`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/add3e87) (+105) | [`98e9b15`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/98e9b15) (+51) |

### 3.3 Scheduled prices, backend ([pilah-be #79](https://github.com/bank-sampah-PILAH/pilah-be/pull/79))

| # | Behaviour | Red | Green |
|---|---|---|---|
| 1 | The price in effect at a given time is the latest version that has started | [`2b0c4ab`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2b0c4ab) (+42) | [`a41b5d5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/a41b5d5) (+99 −2) |
| 2 | A setoran prices its items from the version in effect, ignoring scheduled ones | [`e6bf183`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e6bf183) (+74) | [`d111495`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d111495) (+8 −3) |
| 3 | A new jenis records its price as a first version, with its author | [`f0fbe9d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f0fbe9d) (+61) | [`c729f7a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c729f7a) (+46 −5) |
| 4 | `POST /jenis-sampah/{id}/harga` changes the price now | [`0a42f99`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0a42f99) (+17) | [`df1db9f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/df1db9f) (+40 −6) |
| 5 | A future `berlaku_mulai` schedules the price, and the current one stays | [`68a805e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/68a805e) (+22) | [`c53f1a7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c53f1a7) (+39 −9) |
| 6 | A backdated, far-future or offsetless `berlaku_mulai` is rejected | [`1c829d6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1c829d6) (+19) | [`78f1945`](https://github.com/bank-sampah-PILAH/pilah-be/commit/78f1945) (+33 −1) |
| 7 | A price changed through `PUT` (older app builds) becomes a version | [`f323911`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f323911) (+30) | [`ead26b9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ead26b9) (+17) |
| 8 | The database rejects a price of 0 or below | [`8593164`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8593164) (+8) | [`915b3d1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/915b3d1) (+12 −1) |
| 9 | The migration backfills every price and drops the old column; the reverse migration restores it | [`caaceab`](https://github.com/bank-sampah-PILAH/pilah-be/commit/caaceab) (+126) | [`ad352fb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ad352fb) (+172 −57) |
| 10 | The jenis list's query count stays constant | [`c2a7c71`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2a7c71) (+28) | [`6c0ba69`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6c0ba69) (+32 −12) |
| 11 | The list's `status` and `kategori` filters accept only known values | [`94267c8`](https://github.com/bank-sampah-PILAH/pilah-be/commit/94267c8) (+18) | [`cef01bb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cef01bb) (+32 −11) |
| 12 | *Review finding:* reseeding keeps a historical setoran at the price of its own date | [`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) (+21) | [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f) (+17 −10) |

**Refactors after green:**

- [`95a62f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/95a62f3) breaks ties on the newest row explicitly;
- [`ee9668d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ee9668d) moves price selection out of the shared `kalkulasi` module;
- [`1e7da30`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1e7da30) looks the price up at the transaksi's `tanggal`;
- [`fe5db58`](https://github.com/bank-sampah-PILAH/pilah-be/commit/fe5db58) splits an assertion SonarCloud flagged.

### 3.4 Scheduled prices, app ([pilah-mobile #62](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62))

| # | Behaviour | Red | Green |
|---|---|---|---|
| 1 | The app reads when the current price started and when the next one starts | [`bc5301e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bc5301e) (+40) | [`6884877`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6884877) (+40) |
| 2 | Local times are sent with their UTC offset | [`dce80aa`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/dce80aa) (+22) | [`2a81157`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2a81157) (+15) |
| 3 | A price change is POSTed, and the price is no longer sent with `PUT` | [`c7fa0b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c7fa0b5) (+92) | [`f62ca9b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f62ca9b) (+51 −1) |
| 4 | The harga cubit changes a price through `UbahHargaUseCase` | [`ea35ccb`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ea35ccb) (+77) | [`7729d3d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7729d3d) (+39) |
| 5 | Editing a jenis shows the BR-03 warning and the current and scheduled price | [`3a9f7e4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3a9f7e4) (+90) | [`b67d38d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b67d38d) (+90 −2) |
| 6 | A price is saved now, or from a chosen date | [`f97b492`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f97b492) (+64) | [`bb80f22`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bb80f22) (+74 −4) |
| 7 | The price list card shows an upcoming price change | [`1c28897`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/1c28897) (+55) | [`392ef5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/392ef5d) (+17) |
| 8 | *Review finding:* when only the new price fails after the other fields saved, the sheet says so and stays open | [`5a80375`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5a80375) (+28) | [`f1ea8d9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f1ea8d9) (+15) |
| 9 | *Review finding:* an older list reload that answers late can't overwrite a newer one | [`ece524b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ece524b) (+38) | [`bd21f70`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bd21f70) (+4) |

**Coverage test:** [`52ec8d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/52ec8d0) (+73 −2) covers the lines the first coverage run showed as missed (92% → 100%): the use case, a failed request, `HargaTerjadwal` equality, and two branches of the sheet.

### 3.5 Void a setoran, backend ([pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145))

| # | Behaviour | Red | Green |
|---|---|---|---|
| 1 | A void keeps the row, takes its total out of the saldo, and records who, when and why | [`f3c3db7`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f3c3db7) (+69) | [`638cb3f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/638cb3f) (+126 −3) |
| 2 | A voided setoran is final: voiding it again, editing it or resending its WhatsApp receipt gets 409 | [`997c5d0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/997c5d0) (+34) | [`b08e3eb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b08e3eb) (+27 −6) |
| 3 | Money already paid out can't be voided, and later pencairan snapshots shift | [`99de195`](https://github.com/bank-sampah-PILAH/pilah-be/commit/99de195) (+50 −1) | [`966c7ba`](https://github.com/bank-sampah-PILAH/pilah-be/commit/966c7ba) (+9 −2) |
| 4 | A voided setoran leaves the saldo history, the riwayat summary and the pencairan edit replay | [`516cc0f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/516cc0f) (+51) | [`cb0e666`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cb0e666) (+33 −18) |
| 5 | Reports leave it out: the Excel export, dashboard stats, trends, categories and the nasabah statement | [`1aa13a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1aa13a0) (+124) | [`05b3bf1`](https://github.com/bank-sampah-PILAH/pilah-be/commit/05b3bf1) (+14 −5) |
| 6 | Nasabah views show it as "dibatalkan", and the pengurus ringkasan stops counting it | [`93fd052`](https://github.com/bank-sampah-PILAH/pilah-be/commit/93fd052) (+87) | [`773d667`](https://github.com/bank-sampah-PILAH/pilah-be/commit/773d667) (+18 −10) |
| 7 | The database refuses a half-recorded void | [`31b3ee4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/31b3ee4) (+12) | [`2814ae6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2814ae6) (+43 −2) |

- **Coverage test:** [`f67aa72`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67aa72) (+41) covers three guards:
    - the alasan is required;
    - another bank's setoran gets 404;
    - a nasabah gets 403.

    The serializer, the bank-scoped queryset and the permission class already enforced these, so the tests passed when written. The commit says so.
- **Refactor after green:** [`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0) (11 files, +48 −31) routes every counted-setoran query through `Transaksi.objects.tercatat()`.

### 3.6 Void a setoran, app ([pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193))

| # | Behaviour | Red | Green |
|---|---|---|---|
| 1 | A voided setoran is marked in the riwayat feed (grey amount, "Dibatalkan") | [`fe6cb9f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/fe6cb9f) (+44) | [`ca482d2`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca482d2) (+17 −1) |
| 2 | The notifier voids through `BatalkanTransaksiUseCase` and returns the detail or the server's reason | [`d511208`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d511208) (+68) | [`5b76c4f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5b76c4f) (+96) |
| 3 | Hapus from the phone's selection header, with a required alasan | [`0e102d4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/0e102d4) (+206) | [`cd2cad4`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/cd2cad4) (+169 −27) |
| 4 | Hapus in the web Aksi column, and none on a voided row | [`65ed307`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/65ed307) (+47) | [`3db0fa9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3db0fa9) (+58 −20) |
| 5 | The detail shows who voided it, when and why | [`0ffc9d3`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/0ffc9d3) (+34) | [`24be713`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/24be713) (+56 −9) |
| 6 | *Found by E2E:* the Hapus dialog stays narrow on desktop, and a voided detail shows no saldo | [`df1fc4c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/df1fc4c) (+12) | [`4d16698`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4d16698) (+66 −55) |
| 7 | *After the staging merge:* the new inline detail shows the pembatalan | [`5af4e5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5af4e5da) (+68) | [`ef7a0b9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef7a0b96) (+43 −1) |

**Refactor after green:** [`ca2ec7a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca2ec7a2) (+18 −17) replaces three nested ternaries with a guard clause, after SonarCloud rule S3358.

### 3.7 Totals

| Feature | Pairs (backend + app) | Lines added by red commits | Lines added by green commits |
|---|---|---|---|
| Pencairan | 10 + 5 = 15 | 386 + 645 = 1,031 | 335 + 720 = 1,055 |
| Scheduled prices | 12 + 9 = 21 | 466 + 506 = 972 | 547 + 345 = 892 |
| Void a setoran | 7 + 7 = 14 | 427 + 479 = 906 | 270 + 505 = 775 |
| **Total** | **29 + 21 = 50** | **2,909** | **2,722** |

About **1.07 lines of test were written for every line of production code**, and each one before the code it tests. Refactor and coverage commits are not counted here.

## 4. Coverage

Coverage is measured on the lines each merge request changes, in two ways:

- **SonarCloud's new-code coverage**, from the MR's analysis;
- **`diff-cover` against `origin/staging`**, locally, after `coverage run manage.py test` (backend) or `flutter test --coverage` (app).

| MR | Coverage of changed lines | Evidence |
|---|---|---|
| pilah-be #19 (pencairan) | **100%** of my new code | [S1W1](../review/part-b/tdd.md#coverage-proof), [HTML report](../sprints/sprint-1/evidence/pil-176-diff-coverage.html) |
| pilah-mobile #26 (pencairan) | **88.07%** at merge. The misses were the route builder, the DI wrapper and two pass-throughs. [pilah-mobile #52](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/52) (29 Sep) took the whole `lib/features/pencairan` to **100%**, 898 lines, generated code included | [S1W1](../review/part-b/tdd.md#mobile-pilah-mobile-26), [S1W2](../review-week-2/part-b/tdd.md#closing-the-mobile-gap-pilah-mobile-52-2829-sep-merged) |
| pilah-be #79 (scheduled prices) | **100%** of 459 changed lines after the review fixes; SonarCloud 100% of 144 | [S2W1](../review-sprint-2-week-1/part-b/tdd.md#coverage-proof-at-a-glance) |
| pilah-mobile #62 (scheduled prices) | **100%** of 122 changed lines after the review fixes; SonarCloud 100% of 120 | [S2W1](../review-sprint-2-week-1/part-b/tdd.md#coverage-proof-at-a-glance) |
| pilah-be #145 (void) | **100%** of 348 changed lines, on Postgres 16; SonarCloud 100% of 87 | [S3W1](../review-sprint-3-week-1/part-b/tdd.md#coverage-proof-at-a-glance) |
| pilah-mobile #193 (void) | **100%** of 152 changed `lib/` lines; SonarCloud 100% of 140 | [S3W1](../review-sprint-3-week-1/part-b/tdd.md#coverage-proof-at-a-glance) |

## 5. Part B record

Part B TDD has been at 3 or above every week since Sprint 1 Week 1, which is more than the month the rubric asks for.

| Week | Part B TDD | Page |
|---|---|---|
| Sprint 1 Week 1 (15–22 Sep) | 4 (given by the assessor) | [TDD, S1W1](../review/part-b/tdd.md) |
| Sprint 1 Week 2 (23–29 Sep) | 4 | [TDD, S1W2](../review-week-2/part-b/tdd.md) |
| Sprint 1 Week 3 | 4 | [TDD, S1W3](../review-week-3/part-b/tdd.md) |
| Sprint 2 Week 1 (6–12 Oct) | 4 | [TDD, S2W1](../review-sprint-2-week-1/part-b/tdd.md) |
| Sprint 2 Week 2 | 4 | [TDD, S2W2](../review-sprint-2-week-2/part-b/tdd.md) |
| Sprint 2 Week 3 | 4 | [TDD, S2W3](../review-sprint-2-week-3/part-b/tdd.md) |
| Sprint 3 Week 1 (31 Oct – 3 Nov) | 4 | [TDD, S3W1](../review-sprint-3-week-1/part-b/tdd.md) |

## 6. Positive, negative and corner cases

| Case | Meaning |
|---|---|
| **Positive** | Valid input: the feature does what it should |
| **Negative** | Invalid input or a forbidden action: the feature refuses it and changes nothing |
| **Corner** | The extreme valid inputs: the very first and very last values of the allowed range, and the ones right next to them. Bugs hide at the edges, for example `<` written where `<=` was meant |

### How corner cases are chosen

Take an input that accepts whole numbers from **1 to 10**:

| Value | Case | Why it is tested |
|---|---|---|
| 5 | Positive | A normal value in the middle of the range |
| **1** and **10** | Corner | The first and last values allowed. A `<` written for `<=` rejects 10 by mistake |
| **2** and **9** | Corner | The values just inside the ends, to show the rule is not off by one |
| 0 and 11 | Negative | The values just outside the range, which must be refused |

The same rule, applied in PILAH. A pencairan's nominal must be more than 0 and at most the saldo. With a saldo of 465,600, the app's validator test ([`27fcd06`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/27fcd06), [Appendix B](#appendix-b-pencairan-nominal-at-the-edges-of-the-saldo)) checks:

| Nominal | Case | Expected |
|---|---|---|
| 200,000 | Positive | Accepted |
| **465,600** (exactly the saldo) | Corner, the top end | Accepted |
| **465,601** (one above the saldo) | Negative, just outside | "Maksimal Rp 465.600" |
| 0 and −1,000 | Negative, the bottom end | "Nominal harus lebih dari nol" |
| empty | Negative | "Nominal wajib diisi" |

### Per feature

**Pencairan**

| Positive | Negative | Corner |
|---|---|---|
| <ul><li>The saldo is lowered exactly once.</li><li>The list is filtered by nasabah.</li><li>The detail is readable within the bank.</li><li>The app reloads the saldo after success.</li></ul> | <ul><li>A nominal above the saldo, or one that is zero, negative or decimal.</li><li>A future `tanggal`, or an invalid `metode`.</li><li>Another bank's nasabah.</li><li>An inactive, pending or rejected nasabah.</li><li>An outsider gets 404, a superadmin 403, and an unauthenticated request 401.</li><li>A server 422 is shown inline in the app.</li></ul> | <ul><li>A nominal exactly equal to the saldo.</li><li>A double tap on submit records once.</li><li>A setoran and a pencairan at the same instant.</li><li>A legacy saldo with sen.</li><li>The saldo history and the Excel export after a pencairan.</li></ul> |

**Scheduled prices**

| Positive | Negative | Corner |
|---|---|---|
| <ul><li>A price changed now.</li><li>A price changed from a future date.</li><li>A setoran priced from the version in effect.</li><li>The app saves a price now or from a date.</li></ul> | <ul><li>A backdated date, a date more than 365 days ahead, or a date without a UTC offset.</li><li>Another bank gets 404; a nasabah gets 403.</li><li>A price of 0 or below is refused by the database.</li><li>An unchanged price records nothing.</li></ul> | <ul><li>Two versions starting at the same instant: the newest row wins.</li><li>A scheduled version is invisible before its start.</li><li>A `PUT` from an older app with the same price adds no version.</li><li>The migration's reverse restores the price *in effect*, ignoring a future one.</li><li>A local midnight is sent with its UTC offset.</li><li>An older reload answering last.</li></ul> |

**Void a setoran**

| Positive | Negative | Corner |
|---|---|---|
| <ul><li>Response 200, with status, who, when and why stored.</li><li>The saldo is reduced and later pencairan are shifted.</li><li>In the app, hold a row, then Hapus with an alasan.</li></ul> | <ul><li>No alasan gets 422.</li><li>Another bank's setoran gets 404; a nasabah gets 403.</li><li>Voiding again, editing, or resending the WhatsApp receipt gets 409.</li><li>Money already paid out (the saldo would go below 0) gets 409.</li><li>The app shows "Alasan pembatalan wajib diisi" and sends nothing.</li></ul> | <ul><li>Voiding the only setoran takes the saldo to **exactly 0**, which is allowed.</li><li>A void that would leave a *later* pencairan unfunded is refused, even though the final saldo stays positive.</li><li>An export period with only voided rows has no data.</li><li>A partial update straight to the database raises `IntegrityError`.</li></ul> |

## 7. Benefits of TDD, from development data

### 7.1 Defects caught by a failing test before merge

Each defect below was first reproduced by a red test, then fixed. None of them reached `staging`, and from then on each was guarded by its test, so it couldn't silently come back.

| # | Feature | Defect | How it surfaced | Data | Red → green |
|---|---|---|---|---|---|
| 1 | Pencairan | A pending or rejected nasabah could be paid out | Review | — | [`8eae32e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8eae32e) → [`96be7bd`](https://github.com/bank-sampah-PILAH/pilah-be/commit/96be7bd) |
| 2 | Pencairan | A setoran and a pencairan at the same instant came back in random order, so the saldo after a setoran was wrong some of the time | Review | Against the old sort the test passed **6 runs in 10**; against the fix, **10 in 10** | [`17a6938`](https://github.com/bank-sampah-PILAH/pilah-be/commit/17a6938) → [`1bd2a1c`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1bd2a1c) |
| 3 | Pencairan | A legacy saldo with sen left sen behind after a pencairan | Review | — | [`6a66617`](https://github.com/bank-sampah-PILAH/pilah-be/commit/6a66617) → [`8801c68`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8801c68) |
| 4 | Pencairan | The test-data reset command didn't check that pencairan were cleared | My own test | — | [`cadc57e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/cadc57e) → [`f1c1edf`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f1c1edf) |
| 5 | Pencairan | The submit button sat below the fold of the form | The widget test couldn't tap it | The page layout and the test were fixed together ([`6f4e1ea`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6f4e1ea), +10 −18) | [`9887d7e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9887d7e) → [`e30e6ab`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/e30e6ab) |
| 6 | Prices | The newest-version tie-break worked only because SQLite happened to return rows in that order. Postgres, used in production, makes no such promise | My own test passed with no code | Made explicit as a refactor, with the reason in the commit | [`95a62f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/95a62f3) |
| 7 | Prices | Reseeding repriced a historical setoran at today's price | Review | A 3,500 snapshot became **99,999** | [`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) → [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f) |
| 8 | Prices | When only the new price failed after the other fields saved, the sheet reported a total failure | Review | — | [`5a80375`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5a80375) → [`f1ea8d9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f1ea8d9) |
| 9 | Prices | An older reload answering late overwrote the newer price on screen | Review | Reproduced deterministically with `Completer`s ([Appendix D](#appendix-d-a-late-reply-made-deterministic)) | [`ece524b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ece524b) → [`bd21f70`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bd21f70) |
| 10 | Void | The Hapus dialog stretched across a desktop window, and a voided detail still showed a saldo | Playwright E2E | Screenshot run at desktop and phone sizes | [`df1fc4c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/df1fc4c) → [`4d16698`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4d16698) |
| 11 | Void | Merging `staging` replaced the detail sheet with an inline row and silently dropped the Pembatalan section | Red test after the merge | The red failed with `Found 0 widgets with text "PEMBATALAN"` | [`5af4e5d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5af4e5da) → [`ef7a0b9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef7a0b96) |

Six of the eleven came from review. Writing a failing test first made each one cheap to fix and hard to lose:

- the reviewer could see the bug reproduced, then fixed, in two commits;
- the six green commits for the review findings were between **+4 and +17 lines** each.

### 7.2 Changing existing code safely (maintenance and iteration)

Two of the three features had to change code that other features already depended on. The tests are what made those changes safe.

- **Scheduled prices replaced a column the whole setoran flow depended on.**
    - The green commit [`ad352fb`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ad352fb) touched **14 files (+172 −57)** to replace `JenisSampah.harga_per_kg` with price versions.
    - Its red test, [`caaceab`](https://github.com/bank-sampah-PILAH/pilah-be/commit/caaceab) (+126), drives the migration forwards and backwards. The same migration was also run forwards, backwards and forwards again on a restored copy of the production database.
- **Voiding changed what every report counts.**
    - The red [`1aa13a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1aa13a0) (+124) checks five existing reports: the Excel export, dashboard stats, trends, categories and the nasabah statement.
    - The green commit that made all five pass was only +14 −5.
- **Refactors with the suite as the safety net:**

    | Refactor | Size | Tests before and after |
    |---|---|---|
    | [`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0): every counted-setoran query through one `tercatat()` method | 11 files, +48 −31 | **898** backend tests, the same result before and after |
    | [`ca2ec7a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca2ec7a2): the TIPE badge without nested ternaries | +18 −17 | **321** transaksi tests, the same result before and after |
    | [`ee9668d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ee9668d): price selection out of the shared `kalkulasi` module | 2 files, +8 −20 | The #79 suite, green before and after |

- **The safety net keeps growing.** The backend suite had 68 tests after pencairan (S1W1), 464 after scheduled prices (S1W3), and 898 after void (S3W1). These are whole-suite counts and include teammates' tests. Each feature after the first was built on top of the tests of the ones before it.

### 7.3 Cost

- **Code written:** 2,909 lines of test for 2,722 lines of production code, about 1.07 to 1 (section 3.7).
- **Time:** many pairs are only a minute apart, so the timestamps show when the commits were recorded, not how long each cycle took. I make no claim about time per cycle.

What the data does support:

- each of the 11 defects in 7.1 was fixed in its own red and green commits;
- none of them needed a fix after merge.

### 7.4 Limits of this analysis

- There is no control group: I can't show how many of these defects would have reached production without TDD.
- Six of the eleven defects were spotted by a reviewer, not by my tests. TDD's part was turning each into a permanent regression test.
- The pencairan app MR merged at 88% coverage of its changed lines. The gap was closed a week later, not before merge.

## 8. Tools and methods

| Tool or method | What it adds to TDD | Where |
|---|---|---|
| **Phase-tagged commits** (`[RED]`, `[GREEN]`, `[REFACTOR]`) | The red → green order can be checked from `git log` alone | Section 3 |
| **diff-cover** | Coverage of only the lines a change touches, so a gap can't hide in a large overall percentage | Every MR, [section 4](#4-coverage) |
| **SonarCloud quality gate** | New-code coverage and code issues on every pull request, before review | Every MR |
| **Mutation checks** | When a test passes the first time, I break the code it guards and watch it fail, then revert. This proves the test can fail | PIL-304 rounding follow-up ([#89](https://github.com/bank-sampah-PILAH/pilah-be/pull/89)): `315600.75 != 315600.00` |
| **mocktail** (Flutter) | Mocks and stubs for one layer at a time, `captureAny` for the exact request sent | [Appendix C](#appendix-c-a-mock-that-captures-the-request) |
| **`Completer`s** | Decide which async call answers first, so a race is reproduced every run | [Appendix D](#appendix-d-a-late-reply-made-deterministic) |
| **`StubApi`** (a fake HTTP adapter) | The real data source, repository and notifier run against canned server responses | [Appendix F](#appendix-f-a-fake-backend-at-the-http-boundary) |
| **Django `MigrationExecutor`** | A migration tested forwards and backwards inside the test suite | [`caaceab`](https://github.com/bank-sampah-PILAH/pilah-be/commit/caaceab) |
| **`CaptureQueriesContext`** | Asserts a list costs the same number of queries for 1 row and for 5, catching N+1 queries | [`c2a7c71`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c2a7c71) |
| **The database as the oracle** | A check constraint is tested by attempting the bad write and expecting `IntegrityError` | [Appendix E](#appendix-e-the-database-as-the-test-oracle) |
| **Postgres 16 locally** (pgserver) | The suite also runs on the production database engine, not only on SQLite. Behaviour SQLite only happens to show, like the row order in 7.1 #6, can't pass by luck | PIL-304, PIL-428 |
| **Playwright E2E** | Drives the web build at desktop and phone sizes and reads the result back from the database. It found 7.1 #10 | PIL-428 |

## 9. Test isolation: stubs, mocks and dummy data

### 9.1 Stub vs mock

Both are **test doubles**: stand-ins for a real dependency, so a test can run one unit without the units it calls.

| | Stub | Mock |
|---|---|---|
| **What it does** | Returns a **prepared answer** when it is called | **Records how it was called**, so the test can check the calls |
| **What the test checks** | The *result* of the unit under test (its state or its output) | The *interaction*: was the dependency called, how often, with what arguments |
| **In mocktail (Flutter)** | `when(() => getHarga.execute()).thenAnswer(...)` | `verify(() => network.post(path, data: captureAny(named: 'data')))` and `verifyNever(...)` |
| **In Python** | `unittest.mock.patch(...)` with a `return_value` | `mock.assert_called_once_with(...)` |
| **Example** | [Appendix D](#appendix-d-a-late-reply-made-deterministic): the use case is stubbed to answer from two `Completer`s, and the test checks the price the cubit shows | [Appendix C](#appendix-c-a-mock-that-captures-the-request): the network service is mocked, and the test checks the body that was POSTed |

A third kind, a **fake**, is a light working implementation of the dependency. An example is `StubApi`, which answers HTTP requests per route ([Appendix F](#appendix-f-a-fake-backend-at-the-http-boundary)).

### 9.2 When I use each

- **A stub, when the unit needs an input from its dependency.** The price cubit needs a list of prices from the use case. The stub hands it a fixed list, and the test checks what the cubit shows.
- **A mock, when the thing I'm testing *is* the call.** The repository must send the right body to the server. The mock captures the request, and the test checks the body, down to the UTC offset of a local midnight. Another example: on invalid input nothing may be sent at all, which `verifyNever` checks.
- **Neither, when the dependency is the behaviour under test.** The backend tests run against a real test database, because row locks, check constraints and the saldo replay only exist in the database. A mocked database would pass while the real query is wrong.

### 9.3 Why use stubs and mocks

1. **Isolation.** When a test fails, the failure is in the one unit under test, not somewhere in the layers below it.
2. **No slow or unavailable dependencies.** App tests don't need a running server, a network or a signed-in Google account.
3. **Situations that are hard to make for real.** A stub can return a 409 conflict, a timeout, a malformed response, or two responses in reverse order. Defect 7.1 #9 could only be reproduced this way.
4. **Checking side effects that have no return value,** such as a request being sent once, or not at all.
5. **Building test-first, top down.** A cubit can be built and tested before the repository below it exists, by stubbing the repository.

### 9.4 Why dummy data, not real data

A test that reads real data **depends** on something it doesn't control. Real data is whatever happens to be in the production database, or on a server, right now. That dependency breaks tests in four ways:

| Problem with real data | What happens to the test | With dummy data |
|---|---|---|
| **It changes.** Someone records a setoran, and a saldo moves | The same test passes today and fails tomorrow, with no code change | The test creates its own data, so the input is always the same |
| **It may not contain the case.** No nasabah has a saldo exactly equal to the nominal I want to test | The corner case can't be tested at all | The test creates exactly the case it needs: a saldo of 465,600 and a nominal of 465,600 |
| **It belongs to others.** Tests that write would change or delete real records, and other tests share them | Tests interfere with each other and with real users | Each backend test runs in its own test database, rolled back after every test |
| **It is personal.** Real nasabah have names, phone numbers and saldo | Personal data ends up in test code, logs and CI | Dummy values: "Bank Void", nasabah "Budi", `void@example.test`, `+628111111111` |

Dummy data does for data what a stub does for code: it **removes the dependency**, so the test depends only on itself. In PILAH:

- **Backend:** each test's `setUp` creates its own bank, pengelola, nasabah and jenis sampah, then records a setoran through the API ([`test_setoran_void.py`](https://github.com/bank-sampah-PILAH/pilah-be/blob/staging/apps/ledger/test_setoran_void.py)). Everything runs in a test database Django creates fresh for the run.
- **App:** tests feed canned JSON through mocks or `StubApi`.

The one place real data is used is a manual check outside the test suite: the PIL-304 migration was run on a restored copy of the production database, because the question there was precisely "does this work on the real data?"

## 10. The F.I.R.S.T. principle

Five properties of good unit tests:

| Letter | Meaning | In PILAH |
|---|---|---|
| **F**ast | Tests run in milliseconds, so they can run after every change | App tests use mocks and `StubApi`, with no server. Backend tests roll back a transaction instead of rebuilding the database |
| **I**ndependent | No test depends on another test or on the order they run in | Each test creates its own data in `setUp` and shares nothing with the others |
| **R**epeatable | The same result every run, on any machine, at any time | <ul><li>Time is injected (`now: () => DateTime(2026, 10, 7, 10)`), so a date test doesn't depend on today.</li><li>`Completer`s fix the order of async answers instead of timing them.</li><li>The same-instant sort that passed 6 runs in 10 was made deterministic (7.1 #2).</li></ul> |
| **S**elf-validating | The test decides pass or fail by itself; nobody reads its output | Every test asserts exact values: the status code, the saldo, the request body. Mutation checks show the assertions can fail |
| **T**imely | The test is written at the right time: before the code | The red commit comes before the green one (section 3). Tests written after the code are labelled as coverage tests |

## 11. Mapping to the rubric

| Level | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | TDD on at least one feature, or explain the TDD process | [Section 1](#1-what-tdd-means), [section 3](#3-tdd-commit-flow-with-evidence-of-the-order) | Met |
| 2 | TDD on at least 3 features (backend and frontend counted separately, CRUD as 1), with positive and negative cases | 3 features × 2 sides = 6, [sections 2–3](#2-the-three-features), [section 6](#6-positive-negative-and-corner-cases) | Met |
| 2 | Explain how test cases are designed | [Section 3](#3-tdd-commit-flow-with-evidence-of-the-order) (one behaviour per pair) and [section 6](#6-positive-negative-and-corner-cases) | Met |
| 3 | Disciplined commits and high coverage; Part B TDD ≥ 3 for at least a month | [Sections 3–5](#3-tdd-commit-flow-with-evidence-of-the-order) | Met |
| 3 | Positive, negative and corner cases for every feature | [Section 6](#6-positive-negative-and-corner-cases) | Met |
| 3 | Explain how corner cases are identified | [Section 6](#how-corner-cases-are-chosen) | Met |
| 3 | Explain best practices and test isolation (mock/stub) | [Section 9](#9-test-isolation-stubs-mocks-and-dummy-data) and [section 10](#10-the-first-principle) | Met |
| 4 | A written analysis of TDD's benefits, based on concrete development data | [Section 7](#7-benefits-of-tdd-from-development-data) | Written; not claimed |
| 4 | Tools or methods that make TDD more efficient and thorough | [Section 8](#8-tools-and-methods) | Written; not claimed |

## Appendix: test code

Excerpts from the red commits, as committed. Lines removed for length are marked `…`.

### Appendix A: same-instant ordering (pencairan, backend)

From [`17a6938`](https://github.com/bank-sampah-PILAH/pilah-be/commit/17a6938). A setoran of 100,000 and a pencairan of 40,000 share one timestamp. The saldo shown after the setoran must be 100,000 every time, in the API and in the Excel export.

```python title="api/tests.py"
def test_same_instant_pencairan_is_ordered_after_setoran(self) -> None:
    Saldo.objects.filter(nasabah=self.nasabah).update(total_saldo=Decimal("0.00"))
    jenis = JenisSampah.objects.create(
        bank_sampah=self.bank,
        nomor="PLS-001",
        nama_sampah="Plastik PET",
        kategori=JenisSampah.Kategori.PLASTIK,
        harga_per_kg=Decimal("100000.00"),
    )
    setoran = self.client.post(
        "/api/v1/transaksi",
        {
            "nasabah_id": str(self.nasabah.id),
            "items": [{"jenis_sampah_id": str(jenis.id), "berat": "1.000"}],
        },
        format="json",
    )
    self.assertEqual(setoran.status_code, 201, setoran.data)
    same_instant = Transaksi.objects.get(id=setoran.data["id"]).tanggal
    pencairan = self.client.post(
        "/api/v1/pencairan",
        {
            "nasabah_id": str(self.nasabah.id),
            "nominal": "40000",
            "metode": "tunai",
            "tanggal": same_instant.isoformat(),
        },
        format="json",
    )
    self.assertEqual(pencairan.status_code, 201, pencairan.data)

    detail = self.client.get(f"/api/v1/transaksi/{setoran.data['id']}")
    self.assertEqual(detail.data["saldo_setelah_transaksi"], Decimal("100000.00"))
    export = self.client.get("/api/v1/transaksi/export?periode=bulan_ini")
    sheet = load_workbook(BytesIO(export.content), data_only=False)["Riwayat Transaksi"]
    self.assertEqual(sheet.cell(5, 10).value, 100000)
```

### Appendix B: pencairan nominal at the edges of the saldo

From [`27fcd06`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/27fcd06): the corner-case rule from section 6 applied to a saldo of 465,600.

```dart title="test/features/pencairan/domain/pencairan_validator_test.dart"
group('PencairanValidator.nominal', () {
  test('accepts a nominal within the saldo', () {
    expect(PencairanValidator.nominal(200000, saldo: 465600), isNull);
  });

  test('accepts a nominal equal to the saldo', () {
    expect(PencairanValidator.nominal(465600, saldo: 465600), isNull);
  });

  test('requires a nominal', () {
    expect(
      PencairanValidator.nominal(null, saldo: 465600),
      'Nominal wajib diisi',
    );
  });

  test('rejects zero and negative nominals', () {
    expect(
      PencairanValidator.nominal(0, saldo: 465600),
      'Nominal harus lebih dari nol',
    );
    expect(
      PencairanValidator.nominal(-1000, saldo: 465600),
      'Nominal harus lebih dari nol',
    );
  });

  test('rejects a nominal above the saldo with the maximum', () {
    expect(
      PencairanValidator.nominal(465601, saldo: 465600),
      'Maksimal Rp 465.600',
    );
  });
});
```

### Appendix C: a mock that captures the request

From [`c7fa0b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/c7fa0b5). `NetworkService` is a mocktail mock:

- `when(...)` **stubs** its answer;
- `verify(...).captured` **mocks** it, checking the exact body the repository POSTed, with no server involved.

```dart title="test/features/harga/data/harga_repository_impl_test.dart"
class _MockNetworkService extends Mock implements NetworkService {}

void main() {
  late _MockNetworkService network;
  late HargaRepositoryImpl repository;

  setUp(() {
    network = _MockNetworkService();
    repository = HargaRepositoryImpl(HargaRemoteDataSourceImpl(network));
  });

  group('ubahHarga', () {
    const path = '/api/v1/jenis-sampah/j-1/harga';

    setUp(() {
      when(() => network.post(path, data: any(named: 'data')))
          .thenAnswer((_) async => _ok(path));
    });

    test('posts a scheduled price with its local start time and offset',
        () async {
      final tengahMalam = DateTime(2026, 10, 15);

      final result = await repository.ubahHarga(
        UbahHarga(id: 'j-1', harga: 5000, berlakuMulai: tengahMalam),
      );

      expect(result, const Right<NetworkException, void>(null));
      final data = verify(
        () => network.post(path, data: captureAny(named: 'data')),
      ).captured.single;
      expect(data, {
        'harga_per_kg': '5000',
        'berlaku_mulai': isoDenganOffset(tengahMalam),
      });
    });

    test('leaves berlaku_mulai out so the price applies now', () async {
      await repository.ubahHarga(const UbahHarga(id: 'j-1', harga: 4000));

      final data = verify(
        () => network.post(path, data: captureAny(named: 'data')),
      ).captured.single;
      expect(data, {'harga_per_kg': '4000'});
    });
  });
  // … a third test checks that PUT no longer sends harga_per_kg
}
```

### Appendix D: a late reply, made deterministic

From [`ece524b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ece524b), review defect 7.1 #9. The use case is **stubbed** to answer from two `Completer`s, and the test decides the order: the newer reload answers first, the older one last. The cubit must keep the newer price.

```dart title="test/features/harga/presentation/harga_cubit_test.dart"
test('an older reload that answers late never overwrites a newer one',
    () async {
  // Saving a price change reloads after the PUT and again after the POST;
  // the first GET can answer last, with the old price.
  HargaEntity jenis(int harga) => HargaEntity(
        id: 'j-1',
        kodeSampah: 'PLS-001',
        name: 'Plastik PET',
        price: harga,
        // …
      );
  final lama = Completer<Either<NetworkException, List<HargaEntity>>>();
  final baru = Completer<Either<NetworkException, List<HargaEntity>>>();
  final jawaban = [lama, baru];
  when(() => getHarga.execute())
      .thenAnswer((_) => jawaban.removeAt(0).future);

  final pertama = cubit.loadHarga();
  final kedua = cubit.loadHarga();
  baru.complete(Right([jenis(5000)]));
  await kedua;
  lama.complete(Right([jenis(3500)]));
  await pertama;

  final loaded = cubit.state as HargaLoaded;
  expect(loaded.jenisSampahList.single.price, 5000);
});
```

### Appendix E: the database as the test oracle

From [`31b3ee4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/31b3ee4). `.update()` skips the service and the serializer, so only the database can refuse these half-recorded voids. The test is the reason the backend does *not* mock the database (section 9.2).

```python title="apps/ledger/test_setoran_void.py"
def test_database_refuses_a_void_without_who_when_and_why(self) -> None:
    setengah: list[dict[str, Any]] = [
        {"status": Transaksi.Status.DIBATALKAN},
        {"status": Transaksi.Status.DIBATALKAN, "dibatalkan_oleh": self.pengelola},
        {"alasan_batal": "x", "dibatalkan_pada": timezone.now()},
    ]
    for fields in setengah:
        with self.subTest(fields=fields), self.assertRaises(IntegrityError):
            with transaction.atomic():
                Transaksi.objects.filter(pk=self.transaksi.pk).update(**fields)
```

### Appendix F: a fake backend at the HTTP boundary

From [`d511208`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/d511208). `StubApi` is a **fake**: the real data source, repository, use case and notifier run, and only the server is replaced. The tests cover three cases:

- the positive case;
- the negative case (a 409 refusal, whose message is shown as written);
- a tercatat detail that is not voided.

```dart title="test/features/transaksi/presentation/providers/transaksi_batal_test.dart"
const _path = '/api/v1/transaksi/t1/batalkan';

void main() {
  late StubApi api;
  setUp(() => api = StubApi());

  test('voiding posts the trimmed alasan and returns the voided detail',
      () async {
    api.on('POST', _path, json: _dibatalkan());

    final result = await buildTransaksiNotifier(api)
        .batalkanTransaksi(TransaksiBatalRequest(id: 't1', alasan: ' Dobel '));

    expect(api.last.method, 'POST');
    expect(api.last.path, _path);
    expect(api.last.json, {'alasan': 'Dobel'});
    final detail = result.detail!;
    expect(result.error, isNull);
    expect(detail.isDibatalkan, isTrue);
    expect(detail.alasanBatal, 'Dobel');
    expect(detail.dibatalkanOlehNama, 'Pengelola');
    expect(detail.dibatalkanPada, DateTime.utc(2026, 10, 6, 2, 30).toLocal());
  });

  test('a refused void hands back the backend message as written', () async {
    const pesan =
        'Setoran ini tidak bisa dibatalkan karena sebagian saldonya sudah dicairkan';
    api.on('POST', _path, status: 409, json: {'error': pesan});

    final result = await buildTransaksiNotifier(api)
        .batalkanTransaksi(TransaksiBatalRequest(id: 't1', alasan: 'Dobel'));

    expect(result.detail, isNull);
    expect(result.error, pesan);
  });
}
```
