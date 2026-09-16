# Sprint 1 Plan — PIL-176 Pencatatan Pencairan untuk Pengurus

| Item | Detail |
|---|---|
| Owner | Vegard |
| Linear | [PIL-176](https://linear.app/pilah-2/issue/PIL-176) (parent: [PIL-140 CPBI-10](https://linear.app/pilah-2/issue/PIL-140)) |
| Linear branch | `feature/pil-176` |
| Sprint | Sprint 1 — 15 Sep → 1 Oct 2026 · UAT 29 Sep · Sprint Review 1 Oct |
| PRD features | F13 (pencatatan pencairan tunai/transfer), partially F14 (riwayat) |
| Repos touched | `pilah-be` (model, service, API) and `pilah-mobile` (pengurus form) |
| Status | Draft, written 16 Sep 2026 |

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
| Nasabah-side request and status tracking (F13 "pengajuan nasabah", F14) | Sprint 2 per PRD; needs the nasabah role from PIL-152 |
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
- ⚠️ **Branch divergence:** `origin/staging` is about 900 lines ahead of `main` inside `api/` (type hints, ruff, mypy, and Fly deploy). AGENTS.md says `main` is the baseline, but the team is actively working on `staging`. Confirm the base branch before starting (see §8).

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nasabah = models.ForeignKey(Nasabah, on_delete=models.PROTECT, related_name="pencairan")
    bank_sampah = models.ForeignKey(BankSampah, on_delete=models.PROTECT, related_name="pencairan")
    dicatat_oleh = models.ForeignKey(User, on_delete=models.PROTECT, related_name="pencairan_dicatat")
    tanggal = models.DateTimeField(default=timezone.now)
    nominal = models.DecimalField(max_digits=14, decimal_places=2)
    metode = models.CharField(max_length=20, choices=Metode.choices)
    keterangan = models.TextField(blank=True)
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
- No `status` field yet. In Sprint 1 a recorded pencairan is final. Sprint 2 adds status when the nasabah request flow is decided.
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
| `nominal` | required; `> 0`; max 12 integer digits; `≤ saldo` |
| `metode` | required; `tunai` or `transfer` |
| `tanggal` | optional, defaults to now; **not in the future** |
| `keterangan` | optional; max 255 chars |

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
- [ ] Nominal ≤ 0, an invalid metode, or a future tanggal returns 422.
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
| Wed 16 Sep | Close the open questions (§8) with PO/tech lead, confirm the base branch, finish SSH/`gh` setup and fetch the latest remotes | Answers recorded on PIL-176 |
| Thu 17 Sep | BE: model, migration, admin, `PencairanService` + unit tests | Local tests green |
| Fri 18 Sep | BE: serializers, viewset, URLs, isolation and permission tests | Endpoints working locally |
| Mon 21 Sep | BE: balance helper fix + regression tests; API docs; **open BE PR** | PR `feature/pil-176` (pilah-be) |
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

## 8. Open questions to resolve before coding

1. **Sprint placement.** The PRD (§2.1–2.2) puts F12–F14 (pencairan) in **Sprint 2**, and the Sprint 1 release lists only CPBI-01, 08, 11, and 20. Linear put CPBI-10 in Sprint 1. Is PIL-176 committed for the Sprint 1 review? This affects UAT scope and the ≥20% AC target.
2. **Base branch.** Should the branch come from `staging` (where CI, mypy, and deploy live) or `main` (the AGENTS.md baseline)?
3. **Inactive nasabah.** Can a nonaktif nasabah with remaining saldo still be paid out? The PRD says nasabah with saldo are deactivated, not deleted, which suggests yes. The default here is active-only, matching setoran.
4. **Backdating.** How far back may `tanggal` be set? It changes the running balance of later setoran.
5. **Minimum nominal or rounding.** Is there a minimum, or a requirement for whole rupiah (no cents)?
6. **Jadwal pencairan (F12).** Must a pencairan fall on a scheduled date? The assumption is **no** for Sprint 1, since F12 has no sub-issue.
7. **Metode transfer.** Is a reference number or bank name needed for transfers, or is `keterangan` enough?

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
