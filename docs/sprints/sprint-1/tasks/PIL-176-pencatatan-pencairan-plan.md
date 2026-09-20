# Sprint 1 Plan — PIL-176 Pencatatan Pencairan untuk Pengurus

| Item | Detail |
|---|---|
| Owner | Vegard |
| Linear | [PIL-176](https://linear.app/pilah-2/issue/PIL-176) (parent: [PIL-140 CPBI-10](https://linear.app/pilah-2/issue/PIL-140)) |
| Linear branch | `feature/pil-176-pencatatan-pencairan-untuk-pengurus` (from `staging`) |
| Sprint | Sprint 1 — 15 Sep → 1 Oct 2026 · UAT 29 Sep · Sprint Review 1 Oct |
| PRD features | F13 (pencatatan pencairan tunai/transfer), partially F14 (riwayat) |
| Repos touched | `pilah-be` (model, service, API) and `pilah-mobile` (pengurus form) |
| Status | Backend done and in review ([pilah-be #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19), CI green); mobile not started. Updated 20 Sep 2026. |

---

## 1. Goal

A pengurus can record a cash-out (pencairan) for a nasabah: **nominal, tanggal, metode (tunai/transfer), keterangan**.
The nasabah's saldo drops **exactly once**, never below zero, and the record can be read back later for the riwayat pencairan.

PIL-176 description:

> Membuat pencatatan realisasi pencairan yang dilakukan oleh pengurus yang isinya termasuk: nominal, tanggal, metode pencairan, keterangan tambahan. Data dapat dilihat kembali oleh pengurus dan nasabah melalui riwayat pencairan.

These acceptance criteria from CPBI-10 and PRD §3.13 apply to this task:

- [ ] Pengurus records nominal, tanggal, metode (tunai / transfer), and keterangan.
- [ ] Pencairan is only allowed if the saldo is sufficient (validated against the membership's saldo).
- [ ] Saldo and history update exactly once, atomically.
- [ ] Each record stores who recorded it and when (audit).
- [ ] Only the pengurus of that bank sampah can create or read it (data isolation).
- [ ] No payment gateway: the app only records the payout.

---

## 2. Scope

### In scope (PIL-176)

- Backend `Pencairan` model, migration, and admin registration.
- Atomic `PencairanService.create_pencairan` with saldo validation and row locking.
- API: `POST /api/v1/pencairan`, `GET /api/v1/pencairan/{id}`, and a minimal `GET /api/v1/pencairan` list filtered by nasabah.
- Fix the existing "saldo setelah transaksi" calculations so they subtract pencairan (see §4.3).
- Mobile pengurus flow: entry point → form → confirmation → success sheet → saldo refreshed.
- Backend and mobile tests that keep the CI coverage gates green.

### Out of scope (sibling or later issues)

| Work | Where |
|---|---|
| Full riwayat pencairan screen for pengurus | [PIL-222](https://linear.app/pilah-2/issue/PIL-222) (unassigned) |
| Editing a recorded pencairan | [PIL-230](https://linear.app/pilah-2/issue/PIL-230) (unassigned) |
| Jadwal pencairan (F12) | CPBI-10 AC #1, which has no sub-issue yet |
| Nasabah-side **request/approval** (F13 "pengajuan nasabah") | Sprint 2 per PRD. Nasabah may only *view*, never request or approve (§8 Q9). |
| Nasabah-side **read** of riwayat pencairan | In Sprint 1 scope per §8 Q9, but likely PIL-222 rather than PIL-176 — confirm the owner. |
| WhatsApp or push notification on pencairan | CPBI-14 / F16 |
| Pencairan rows in the Excel export | Follow-up; only the running balance is fixed here |

The API should be designed so that PIL-222 and PIL-230 can build on it without breaking changes.

---

## 3. Codebase findings

### 3.1 Backend (`pilah-be`, Django 6 + DRF)

- **No pencairan code exists** (model, API, or UI). The Linear notes on CPBI-10 say the same.
- `Saldo` is a one-to-one row per `Nasabah` (`total_saldo`, Decimal 14,2). `Nasabah` is already scoped per bank sampah, so it effectively acts as the membership today.
- `Transaksi.Tipe` only has `SETORAN`. Every setoran has `DetailTransaksi` items, and the list serializer, export, and dashboard all assume items exist.
- `TransactionService.create_setoran` (`api/services.py`) is the pattern to follow: it is `@transaction.atomic`, uses `select_for_update()` on the nasabah and saldo, scopes by `user.bank_sampah`, and raises `serializers.ValidationError`.
- **Two places compute a historical balance by summing `Transaksi.total_nilai` only:**
  - `TransactionDetailSerializer.get_saldo_setelah_transaksi` (`api/serializers.py`)
  - `_saldo_after_by_transaction` (`api/services.py`, used by the Excel export)

  Once pencairan exists, both will overstate the balance for any setoran recorded after a pencairan. **This must be fixed in the same PR.**
- Permission `IsActivePengelola` gates every pengurus endpoint. Superadmin is already rejected (covered by tests).
- Error format comes from `api/exceptions.py`: validation errors become **422** `{"errors": {...}}`, and 404 becomes `{"error": "Resource tidak ditemukan"}`.
- CI (`.github/workflows/ci.yml` on `staging`) runs `ruff check`, `ruff format --check`, `makemigrations --check`, tests with **coverage ≥ 80%**, `manage.py check --deploy`, **mypy strict**, and SonarQube.
- ✅ **Base branch resolved (20 Sep):** `staging` is the baseline for every repo; AGENTS.md and the `ship` skill now say so explicitly. `origin/staging` is 11 commits ahead of `main`.
- ✅ **PIL-152 merged** into `staging` on 20 Sep (`ad1c1f6`). `Nasabah` stays the per-bank membership, so the FK target was unchanged.
- ⚠️ **Stacked on PIL-188 (#18):** both branches added an `0011_` migration from the same parent, which would have left Django with two leaf nodes. PR #19 is rebased onto #18 and renumbered to `0012_pencairan`, keeping the graph linear. #18 must merge first; GitHub then retargets #19 to `staging`.
- ~~**PIL-152 lands first:**~~ [PR #15](https://github.com/bank-sampah-PILAH/pilah-be/pull/15) (In Review) adds migrations `0005`–`0010`, `Nasabah.user`, bank hierarchy, and one-membership-per-bank. `Nasabah` stays the per-bank membership, so the FK target is unchanged, but the pencairan migration must be renumbered after it merges. The PR still targets `main` and needs retargeting to `staging`.

### 3.2 Mobile (`pilah-mobile`, Flutter 3.41 / Dart 3.11)

- Clean-architecture feature folders (`data/`, `domain/`, `presentation/`), Cubit state, `injectable` DI, and `dartz` `Either<NetworkException, T>` repositories.
- New features are scaffolded with the SPL CLI: `dart run codegen/spl_manager.dart add <name> --state cubit`. Don't hand-edit `spl.yaml`.
- Code to reuse:
  - `features/transaksi` is the closest template: remote data source, repository, `TransaksiBaruPage`, and `TransaksiBerhasilBottomSheet`.
  - `PilihNasabahBottomSheet` is the nasabah picker and already fetches the nasabah list.
  - `DetailNasabahBottomSheet` shows saldo and has action buttons, which makes it a natural entry point.
  - Design system: toast, confirmation modal ("Konfirmasi pencairan" is already in the PRD's design system), and `CustomPrimaryButton`.
- Pengurus bottom navigation: Dashboard · Nasabah · Harga · Laporan. Only the pengurus and superadmin apps exist; there is no nasabah app yet.
- CI runs `dart format` check, `flutter analyze --fatal-infos`, and `flutter test` with **coverage ≥ 25%**.

---

## 4. Technical design

### 4.1 Decision: a separate `Pencairan` model, not `Transaksi(tipe=PENCAIRAN)`

| Option | Pros | Cons |
|---|---|---|
| **A. New `Pencairan` model** ✅ | Clear fields (metode, keterangan); no fake `DetailTransaksi`; setoran list, export, dashboard, and WA code stay untouched; room for Sprint 2 status/request lifecycle and PIL-230 edit audit | Balance-history helpers must union two tables |
| B. Add `PENCAIRAN` to `Transaksi.Tipe` with a negative `total_nilai` | Existing running-balance sums "just work" | Every consumer that assumes items breaks (`jenis_sampah_utama`, `total_berat_kg`, export sheet, dashboard `total_nilai_bulan_ini`, recent activity, WA notify); negative "nilai" is confusing; hard to add status later |

**Recommendation: A.** Confirm with the backend reviewer before writing the migration.

### 4.2 Data model (`api/models.py`)

```python
class Pencairan(TimestampedModel):
    class Metode(models.TextChoices):
        TUNAI = "tunai", "Tunai"
        TRANSFER = "transfer", "Transfer"

    class Status(models.TextChoices):
        TERCATAT = "tercatat", "Tercatat"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nasabah = models.ForeignKey(Nasabah, on_delete=models.PROTECT, related_name="pencairan")
    bank_sampah = models.ForeignKey(BankSampah, on_delete=models.PROTECT, related_name="pencairan")
    dicatat_oleh = models.ForeignKey(User, on_delete=models.PROTECT, related_name="pencairan_dicatat")
    tanggal = models.DateTimeField(default=timezone.now)
    nominal = models.DecimalField(max_digits=14, decimal_places=2)
    metode = models.CharField(max_length=20, choices=Metode.choices)
    keterangan = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TERCATAT)
    saldo_sebelum = models.DecimalField(max_digits=14, decimal_places=2)
    saldo_sesudah = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = "pencairan"
        ordering = ["-tanggal"]
        indexes = [models.Index(fields=["bank_sampah", "nasabah", "tanggal"])]
        constraints = [
            models.CheckConstraint(condition=models.Q(nominal__gt=0), name="pencairan_nominal_positive"),
        ]
```

Notes:

- `saldo_sebelum` / `saldo_sesudah` are receipt snapshots at record time, matching the PRD "Detail Setoran" pattern. PIL-230 will define how edits affect them.
- `status` ships with the single value `tercatat` (§8 Q8). A recorded pencairan is final in Sprint 1; Sprint 2 adds the request lifecycle and PIL-230 adds edits. Shipping the field now keeps the payload stable for both.
- The migration is purely additive and safe on the existing data.
- Register it in `api/admin.py`, and add it to the verification counts in `reset_testing_data`.

### 4.3 Service (`api/services.py`)

`PencairanService.create_pencairan(user, payload) -> Pencairan`, wrapped in `@transaction.atomic`:

1. Lock the nasabah with `Nasabah.objects.select_for_update().filter(id=..., bank_sampah=user.bank_sampah, is_active=True)`. If none is found, return 422 on `nasabah_id`.
2. Lock the saldo with `Saldo.objects.select_for_update().get_or_create(nasabah=nasabah)`.
3. If `nominal > saldo.total_saldo`, return 422 on `nominal` with "Saldo nasabah tidak mencukupi".
4. Create the `Pencairan` with `saldo_sebelum` / `saldo_sesudah`.
5. Run `saldo.total_saldo -= nominal` and save with `update_fields`.

The row locks serialize concurrent requests, so two quick pencairan can't both pass the saldo check.

**Balance helper fix.** Add one shared helper, e.g. `BalanceService.saldo_at(nasabah, bank, until_dt, until_id)`, that returns Σ setoran − Σ pencairan up to a point in time. Use it in:

- `TransactionDetailSerializer.get_saldo_setelah_transaksi`
- `_saldo_after_by_transaction` (export). Subtract the pencairan per nasabah that fall inside the running window.

### 4.4 API

All endpoints use `permission_classes = [IsActivePengelola]` and are scoped to `request.user.bank_sampah`. Add a `PencairanViewSet` registered as `pencairan`.

**`POST /api/v1/pencairan`**

```json
{
  "nasabah_id": "uuid",
  "nominal": "200000.00",
  "metode": "tunai",
  "tanggal": "2026-09-22T10:15:00+07:00",
  "keterangan": "Diambil pagi"
}
```

| Field | Rule |
|---|---|
| `nasabah_id` | required UUID; active nasabah of the pengurus' bank |
| `nominal` | required; `> 0`; **whole rupiah, no decimals** (§8 Q5); max 12 integer digits; `≤ saldo` |
| `metode` | required; `tunai` or `transfer` (no transfer reference fields, §8 Q7) |
| `tanggal` | optional, defaults to now; **not in the future** (§8 Q4) |
| `keterangan` | optional; max 255 chars |
| `status` | not accepted on input; always written as `tercatat` (§8 Q8) |

Returns **201** with the detail payload below. Returns **422** `{"errors": {...}}` on validation failure.

**`GET /api/v1/pencairan/{id}`** returns the detail:

```json
{
  "id": "uuid",
  "nasabah_id": "uuid",
  "nasabah_nama": "Sari Rahayu",
  "bank_sampah_id": "uuid",
  "dicatat_oleh": "uuid",
  "dicatat_oleh_nama": "Ibu Sari",
  "tanggal": "2026-09-22T10:15:00+07:00",
  "nominal": "200000.00",
  "metode": "tunai",
  "keterangan": "Diambil pagi",
  "status": "tercatat",
  "saldo_sebelum": "465600.00",
  "saldo_sesudah": "265600.00",
  "created_at": "..."
}
```

**`GET /api/v1/pencairan?nasabah_id=&periode=`** is a paginated list. It reuses the `periode` filtering from `TransactionFilterService.apply_period`, generalized to take a date field. It is kept minimal here and extended in PIL-222.

Update `reference/PILAH_API_Documentation` or the README with these endpoints.

### 4.5 Mobile flow (pengurus)

Scaffold the feature with `dart run codegen/spl_manager.dart add pencairan --state cubit`.

```
features/pencairan/
  data/datasources/pencairan_remote_data_source(_impl).dart
  data/repositories/pencairan_repository_impl.dart
  domain/entities/pencairan_entity.dart        # PencairanRequest, PencairanCreated
  domain/repositories/pencairan_repository.dart
  domain/use_cases/add_pencairan_usecase.dart
  presentation/cubit/pencairan_form_cubit.dart (+ state)
  presentation/pages/catat_pencairan_page.dart
  presentation/widgets/metode_pencairan_chips.dart
  presentation/widgets/pencairan_berhasil_bottom_sheet.dart
```

The screen follows PRD Gambar 5.3.29 ("Ajukan Pencairan"), adapted for the pengurus:

1. **Entry points:** a "Catat Pencairan" button in `DetailNasabahBottomSheet` (nasabah preselected), plus an optional dashboard action next to "Setoran Baru".
2. **Pilih nasabah:** reuse `PilihNasabahBottomSheet` and show the current saldo.
3. **Nominal:** rupiah-formatted input with inline "Maksimal Rp …" validation.
4. **Metode:** Tunai / Transfer chips (design-system filter chips).
5. **Tanggal:** date picker, default today, future dates disabled.
6. **Keterangan:** optional multiline field.
7. **Summary:** saldo sekarang, dicairkan, **sisa saldo**.
8. **Confirmation modal:** "Pencairan Rp X akan dicatat sebagai pembayaran tunai."
9. **Submit:** disable the button while loading (double-submit guard). On success, show the success sheet with nominal and saldo sesudah, then refresh `NasabahCubit` and the dashboard.
10. **Errors:** map a 422 on `nominal` to an inline field error, and anything else to an `AppNotification` toast.

Add `pencairan = "/api/v1/pencairan"` to `core/constants/endpoints.dart` and register the route in `app_router_config.dart`.

---

## 5. Test plan

### Backend (`api/tests.py`, keep coverage ≥ 80%)

- [ ] Creating a pencairan reduces saldo by the nominal and stores both snapshots and `dicatat_oleh`.
- [ ] A nominal equal to the saldo succeeds and leaves saldo at 0.
- [ ] A nominal greater than the saldo returns 422, and **saldo and row count are unchanged**.
- [ ] Nominal ≤ 0, a nominal with decimals, an invalid metode, or a future tanggal returns 422.
- [ ] A created pencairan has `status == "tercatat"`, and a `status` sent in the request body is ignored.
- [ ] A nasabah from another bank sampah returns 422 (no data leak).
- [ ] An inactive nasabah returns 422 (see open question Q3).
- [ ] Two sequential pencairan whose sum exceeds the saldo: the second fails.
- [ ] Superadmin gets 403, unauthenticated gets 401, pending-bank pengurus gets 403.
- [ ] List and detail are scoped to the bank: an id from another bank returns 404.
- [ ] **Regression:** a setoran recorded after a pencairan reports the correct `saldo_setelah_transaksi`.
- [ ] **Regression:** the Excel export's "Saldo Setelah Transaksi" accounts for pencairan.
- [ ] `makemigrations --check`, `ruff`, and `mypy api config` all pass.

### Mobile (keep coverage ≥ 25%)

- [ ] `PencairanFormCubit`: success, 422 mapped to a field error, network error.
- [ ] Remote data source: request body shape and response mapping.
- [ ] Widget test: submit is disabled while nominal is empty, 0, or above saldo; the sisa-saldo summary updates.
- [ ] Widget test: metode chips toggle, and the future date is not selectable.
- [ ] `flutter analyze --fatal-infos` and `dart format` pass.

### Manual (staging, before UAT 29 Sep)

- [ ] Record a setoran, then a pencairan, then another setoran. Check the saldo on the nasabah list, detail, transaction detail, and export.
- [ ] Double-tap submit on a slow network: only one record is created.

---

## 6. Timeline

Weekends are 19–20 and 26–27 Sep.

| Date | Work | Output |
|---|---|---|
| Wed 16 Sep | Close the open questions (§8) with PO/tech lead, confirm the base branch, finish SSH/`gh` setup and fetch the latest remotes | ✅ Answers recorded 19 Sep (§8); base branch is `staging`; SSH fixed 20 Sep (missing `known_hosts` entry, not access) |
| Thu 17 – Fri 18 Sep | _Not worked: blocked on SSH access and open questions_ | — |
| **Sat 20 Sep** (catch-up) | ✅ All backend work in one day: model, migration, admin, service, serializers, viewset, URLs, balance-helper fix, regression tests, README. 8 new tests (39 → 47), 87% coverage. **BE PR opened and self-assigned**, then rebased onto #18 and renumbered to `0012_pencairan`. | [PR #19](https://github.com/bank-sampah-PILAH/pilah-be/pull/19), CI green in 2m23s |
| Sun 21 Sep | Freed up — originally the third backend day. Use it to start mobile early, or to address review on #19. | — |
| Tue 22 Sep | Mobile: scaffold feature, data layer, cubit + tests | — |
| Wed 23 Sep | Mobile: form page, nasabah picker, validation, confirmation modal | Screen working against local BE |
| Thu 24 Sep | Mobile: success sheet, refresh saldo, entry points, widget tests; **open mobile PR** | PR `feature/pil-176` (pilah-mobile) |
| Fri 25 Sep | Address review on both PRs, merge BE first | BE merged |
| Mon 28 Sep | Deploy to staging, manual test checklist, fix bugs, merge mobile | Staging build ready |
| **Tue 29 Sep** | **UAT** | UAT notes |
| Wed 30 Sep | UAT fixes; help with PIL-222 if time allows | — |
| **Thu 1 Oct** | **Sprint Review**: demo record pencairan → saldo updated | — |

**Suggested estimate:** 3 points. Linear currently shows 0 for all sub-issues.

---

## 7. Dependencies and coordination

| With | Why | Action |
|---|---|---|
| **Tristan — PIL-152** (roles/schema, *In Progress*) | May introduce a membership/keanggotaan model. `Pencairan` FKs to `Nasabah` today. | Ask whether `Nasabah` stays the per-bank membership entity in Sprint 1. |
| **Heraldo — PIL-154** (add nasabah by email) | Changes the `Nasabah` model, so migrations will conflict. | Agree on merge order, and rebase and regenerate the migration number before merging. |
| **Melanton — PIL-168 / PIL-224** (price source, rounding, setoran validation) | Edits `TransactionService` and transaction serializers, the same files as the balance helper fix. | Keep pencairan code in a separate class and at the end of the files; sync before touching `get_saldo_setelah_transaksi`. |
| **UI/UX** | The PRD only has the nasabah "Ajukan Pencairan" screen, not a pengurus one. | Ask for or confirm a pengurus variant in Figma, or approve reusing the 5.3.29 layout. |
| **PIL-222 / PIL-230 owners** (unassigned) | They build on this API. | Share the endpoint contract as soon as the BE PR is open. |

---

## 8. Open questions — answered 19 Sep (PM) and 20 Sep (tech lead)

1. **Sprint placement.** ✅ Committed to Sprint 1. Linear has PIL-176 in cycle Sprint 1 under EPIC04. CPBI-10 counts as done only once pencatatan, pembaruan saldo, **and** riwayat all work, so PIL-222 must be picked up by someone this sprint.
2. **Base branch.** ✅ `staging`, for every repository. The `ship` skill defaults to it and must never infer `main`. PR #15 (PIL-152) targets `main` only because it predates the guide.
3. **Inactive nasabah.** ✅ Active only. A nonaktif nasabah cannot be paid out; the remaining saldo stays stored.
4. **Backdating.** ✅ `tanggal` is the real payout date or the scheduled date. Since no schedule model exists yet, Sprint 1 accepts any past date and **rejects future dates**.
5. **Minimum nominal or rounding.** ✅ `> 0`, `≤ saldo`, **whole rupiah with no decimals** in Sprint 1. The column stays `Decimal(14,2)`; the serializer rejects cents.
6. **Jadwal pencairan (F12).** ✅ Belongs to CPBI-10, not CPBI-07 (which covers jadwal kegiatan/penimbangan). It still has no sub-issue, so it stays out of PIL-176. Pengurus record payouts against an existing schedule informally.
7. **Metode transfer.** ✅ There is no payment gateway, so transfer handling is outside our scope. Keep `metode` and an **optional** `keterangan`; no reference number or bank fields.
8. **Status.** ✅ New requirement: pengurus and nasabah see nominal, tanggal, metode, **status**, and keterangan. Sprint 1 records one value (`tercatat`); the Sprint 2 request flow and PIL-230 extend it.
9. **Nasabah visibility.** ✅ Pencairan appears in the nasabah's riwayat aktivitas in Sprint 1, but nasabah can neither request nor approve. PIL-152 gives nasabah accounts a login, so a nasabah-scoped read is now in sprint scope — **open: does it belong to PIL-176 or PIL-222?**
10. **Nasabah membership.** ✅ Sprint 1 keeps one nasabah in one bank sampah. "Di setiap bank sampah" means each bank sees only its own nasabah and pencairan.
11. **Immutability.** ✅ Once saved, a pencairan is a valid record. Changes only happen through PIL-230, by authorized users.

---

## 9. Definition of Done (from CPBI-10)

- [ ] Design finalized (open questions answered, Figma confirmed)
- [ ] Code implemented (BE + mobile)
- [ ] CI/CD passed (ruff, mypy, coverage ≥ 80% BE / ≥ 25% mobile, analyze)
- [ ] Code reviewed (1 PR per repo, same branch name)
- [ ] QA passed (§5 checklists)
- [ ] Deployed to staging
- [ ] Internal testing done before UAT 29 Sep
- [ ] Deployed to production (after Sprint Review, per team process)

## 10. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Balance history wrong after pencairan | Nasabah or pengurus see incorrect "saldo setelah" | Shared helper + regression tests (§5) |
| Migration conflicts with PIL-152/154 | Broken CI or deploy | Small, additive migration; rebase before merge |
| Scope creep into edit/history/schedule | Misses UAT | Hold the §2 boundary; hand off to PIL-222/230 |
| Sprint placement mismatch (Q1) | Demoing a feature the PO didn't plan | Confirm on 16 Sep |
