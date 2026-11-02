# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code:

    - **A void as an audited state change,** not a delete, so the ledger stays append-only. A database check constraint means it can't be half-recorded.
    - **Concurrency handled explicitly:** the void locks the saldo, then the setoran, in the same order as an edit. On PIL-451, one more writer now joins the shared account lock.
    - **A domain rule named once:** "a voided setoran counts toward nothing" is a QuerySet method rather than nine copies of a filter.
    - **A hardcoded release toggle** read through a configured widget, so closing or reopening a feature is one edit.
    - **Extract Method** twice from SonarCloud findings, and once more as my own refactor.
    - **All five SOLID principles,** each with the code it applies to. See [SOLID in this week's code](#solid-in-this-weeks-code).

    Each item names the design issue it addresses, the pattern or principle used, its type and where the issue came from.

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [`batalkan_setoran`](#a-void-is-a-state-change-not-a-delete-638cb3f-966c7ba) | **Destructive delete in a ledger:** deleting a setoran would lose the record, break later pencairan snapshots and leave no trace of who removed money | **Soft delete with audit fields:** the row stays; `status`, `alasan_batal`, `dibatalkan_oleh` and `dibatalkan_pada` record the void | Technique (follows the SDS "append-only transaksi" rule) | Designed in |
| [`transaksi_batal_lengkap`](#the-database-refuses-a-half-recorded-void-2814ae6) | **An invariant enforced only in code:** `.update()`, the admin or a future script could write `dibatalkan` without who or why | **Database-level integrity constraint** (`CheckConstraint`) | Technique | Designed in (SDS: DB-level integrity), OWASP A08 |
| [`batalkan_setoran` locks](#a-void-is-a-state-change-not-a-delete-638cb3f-966c7ba) | **Lost update:** a void racing an edit, a second void or a pencairan could each read a stale saldo | **Pessimistic locking in a fixed order** (saldo, then the setoran via `_kunci_tercatat`), shared with `edit_setoran` | Technique (concurrency) | Designed in |
| [`_geser_pencairan`](#a-void-is-a-state-change-not-a-delete-638cb3f-966c7ba) | **Duplicated knowledge:** an edit already shifts later pencairan snapshots by a delta | **Reuse:** a void is an edit by `−total`, so it calls the same method | Principle (DRY) | Designed in, reusing PIL-427's method |
| [`TransaksiQuerySet.tercatat()`](#a-domain-rule-named-once-ae850a0) | **Duplicated domain rule:** `filter(status=TERCATAT)` in nine places, so the next report could forget it and count voided money | **Named query on a custom QuerySet** (Query Object / Specification) | Architectural (PoEAA) | My own refactor, found while documenting the week |
| [`aktivitasTipeTersedia`](#a-release-toggle-in-one-place-b577c7c-1b52638) | **A closed feature left reachable:** three hardcoded segments and a "semua" default spread over three places | **Hardcoded release toggle** plus a constructor parameter, so the widget is configured, not edited | Technique; Principle (OCP) | Own refactor before the change |
| [`_sync_nasabah_prefill`](#one-more-writer-under-the-shared-lock-d19cb8d) | **Check-then-act on a stale account:** the fourth writer of the role-change invariant had no lock | The **same pessimistic row lock** as the other writers, then a re-check | Technique (concurrency) | **My own defect, found in review** ([Tristan P1](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4431159076), [Heraldo](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4434504589)) |
| [`lock_account`](#one-more-writer-under-the-shared-lock-d19cb8d) | **A redundant round trip:** lock by pk, then reload | **Single locking read** (`refresh_from_db(from_queryset=select_for_update())`) | Technique | Review nit ([Heraldo](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4434504808)) |
| [`_resetForNewRole`](#the-form-follows-a-real-role-change-3d0a81b) | **Two copies of the same input** (the provider's draft and the mounted controllers), only one invalidated, and on every session | **Observer** (`ref.listen`) on the one event that invalidates the input; the screen owning the controllers resets them | GoF Behavioural (via Riverpod); Principle (SRP) | **My own defects, found in review** on #174 |
| [`_onAuthChanged`](#extract-method-from-two-tool-findings-8bdb1b5-ca2ec7a) | **A long `build`** (cognitive complexity 18 of 15) | **Extract Method** | Refactoring | Tool finding (SonarCloud S3776) |
| [`_typeBadge`](#extract-method-from-two-tool-findings-8bdb1b5-ca2ec7a) | **Nested ternaries** in a widget tree after a merge | **Extract Method with a guard clause** | Refactoring | Tool finding (SonarCloud S3358) on my merge |

## Backend: [pilah-be #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145) (31 Oct)

### A void is a state change, not a delete — [`638cb3f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/638cb3f), [`966c7ba`](https://github.com/bank-sampah-PILAH/pilah-be/commit/966c7ba)

```python title="apps/ledger/services.py"
@staticmethod
def batalkan_setoran(user: User, transaksi: Transaksi, alasan: str) -> Transaksi:
    """Void a setoran: keep the row, mark it cancelled, take its total out of the saldo.

    `transaksi` comes from the caller's bank-scoped queryset; it is re-read under lock.
    """
    saldo = Saldo.objects.select_for_update().get(nasabah_id=transaksi.nasabah_id)
    transaksi = TransactionService._kunci_tercatat(transaksi)
    saldo_baru = bulatkan_rupiah(saldo.total_saldo - transaksi.total_nilai)
    sesudahnya = TransactionService._geser_pencairan(transaksi, -transaksi.total_nilai)
    if saldo_baru < 0 or any(cair.saldo_sesudah < 0 for cair in sesudahnya):
        raise SaldoTidakCukup(
            "Setoran ini tidak bisa dibatalkan karena sebagian saldonya sudah dicairkan"
        )
    transaksi.status = Transaksi.Status.DIBATALKAN
    transaksi.alasan_batal = alasan
    transaksi.dibatalkan_oleh = user
    transaksi.dibatalkan_pada = timezone.now()
    ...
```

- **Fixed lock order:** the saldo row is locked first, then the setoran is re-read under lock. `edit_setoran` takes the same two locks in the same order, so a void and an edit can't deadlock or see each other half-done. `_kunci_tercatat` also refuses a setoran voided meanwhile, which is what makes a void final.
- **Paid-out money:** a void is an edit by `−total`, so it reuses `_geser_pencairan` to shift every later pencairan's snapshot. Then it refuses if any of them would have been paid from money that no longer existed, even when the final saldo stays positive.

### The database refuses a half-recorded void — [`2814ae6`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2814ae6)

```python title="apps/ledger/models.py"
models.CheckConstraint(
    condition=(
        models.Q(
            status="tercatat",
            alasan_batal="",
            dibatalkan_oleh__isnull=True,
            dibatalkan_pada__isnull=True,
        )
        | (
            models.Q(
                status="dibatalkan",
                dibatalkan_oleh__isnull=False,
                dibatalkan_pada__isnull=False,
            )
            & ~models.Q(alasan_batal="")
        )
    ),
    name="transaksi_batal_lengkap",
),
```

The service always writes all four fields together. The constraint makes that true for every other path too. The migration was applied to the 20 Sep production snapshot, and the existing rows pass it.

### A domain rule named once — [`ae850a0`](https://github.com/bank-sampah-PILAH/pilah-be/commit/ae850a0)

While writing this page, I counted the void's "leave it out" rule written as `filter(status=Transaksi.Status.TERCATAT)` in nine places: saldo replay, saldo-after, ringkasan, export, operational summary, dashboard stats, trends and the statement. A tenth report would have to remember it. So it now has a name:

```python title="apps/ledger/models.py"
class TransaksiQuerySet(models.QuerySet["Transaksi"]):
    def tercatat(self) -> "TransaksiQuerySet":
        """Setoran that still count: everything but a void (PIL-428).

        Saldo, laporan, exports and summaries read through this, so a new
        report cannot forget to leave voided setoran out. The riwayat feeds
        list voided rows on purpose and do not.
        """
        return self.filter(status=Transaksi.Status.TERCATAT)


class Transaksi(TimestampedModel):
    objects = TransaksiQuerySet.as_manager()
```

```python title="apps/reporting/statement.py"
setoran = Transaksi.objects.tercatat().filter(
    nasabah=member, bank_sampah=member.bank_sampah
)
```

As the default manager's queryset, it also reaches related managers (`nasabah.transaksi.tercatat()`). One lookup across a relation (`DetailTransaksi` by `transaksi__status`) keeps the field filter, and the commit says so. There's no behaviour change: the full suite gives the same result, strict mypy is clean, and diff coverage is 100% of 348 lines.

## Mobile: [pilah-mobile #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193) and [#196](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/196)

### A release toggle in one place — [`b577c7c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b577c7c), [`1b52638`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/1b52638)

CPBI-31 closes Pencairan by a hardcoded lock, and reopening means a new release. I named the offered and default types first, with no behaviour change. Then the change itself was one edit:

```dart title="lib/features/transaksi/presentation/states/riwayat_aktivitas_state.dart"
/// Tipe yang bisa dipilih Pengurus di Riwayat. Pencairan ditutup dulu
/// (CPBI-31), jadi hanya setoran dan pemilih tipe tidak ditampilkan. Membuka
/// kembali Semua dan Pencairan berarti menambahkannya di sini, mengembalikan
/// [aktivitasTipeBawaan] ke semua, lalu merilis ulang aplikasi.
const aktivitasTipeTersedia = {AktivitasTipeFilter.setoran};

/// Tipe saat Riwayat dibuka dan setelah Reset.
const aktivitasTipeBawaan = AktivitasTipeFilter.setoran;
```

`AktivitasFilterBar` takes the offered types as a parameter, defaulting to that constant, and hides the selector when there's only one choice. The tests pass every type explicitly, so the three-way selector stays tested for the day Pencairan reopens.

## PIL-451, second review round (2 Nov)

### One more writer under the shared lock — [`d19cb8d`](https://github.com/bank-sampah-PILAH/pilah-be/commit/d19cb8d)

Last week's fix made every writer of "a linked membership locks the role" take the account row lock. Tristan and Heraldo found a fourth writer: Google login claims a pengurus-entered membership. It now does what the other three do:

```python title="apps/authentication/services.py"
# Read before the lock: email is unique, so only this same account can
# claim the record meanwhile, and linking it to itself again is harmless.
with transaction.atomic():
    OnboardingService.lock_account(user)
    if user.role != User.Role.NASABAH:
        return
    nasabah.user = user
    nasabah.save(update_fields=["user", "updated_at"])
```

`lock_account` itself became one query ([`7c7c1f3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/7c7c1f3)), as Heraldo suggested:

```python title="apps/authentication/services.py"
user.refresh_from_db(from_queryset=User.objects.select_for_update())
```

### The form follows a real role change — [`3d0a81b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3d0a81b3)

```dart title="lib/features/onboarding/presentation/pages/complete_profile_screen.dart"
static bool _roleChanged(
  AuthenticationStates? previous,
  AuthenticationStates current,
) =>
    previous is Authenticated &&
    current is Authenticated &&
    previous.authEntity.role != current.authEntity.role;
```

The screen owns the text controllers, so it resets them itself, then refills from the account's saved profile. The role page drops the banked draft only when `state.authEntity.role != account.role`.

### Extract Method from two tool findings — [`8bdb1b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8bdb1b54), [`ca2ec7a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ca2ec7a2)

- **S3776 on `CompleteProfileScreen.build`** (complexity 18 of 15): the two reactions to the auth state moved into `_onAuthChanged`, which `build` passes to `ref.listen`.
- **S3358 on the TIPE cell** after my staging merge:

```dart title="lib/features/transaksi/presentation/widgets/aktivitas_table.dart"
/// A voided setoran reads Dibatalkan in place of its type (PIL-428).
Widget _typeBadge(bool expandable) {
  if (_dibatalkan) {
    return const CustomStatusBadge(
      statusText: 'Dibatalkan',
      backgroundColor: AppColors.fill,
      textColor: AppColors.grey100,
    );
  }
  return CustomStatusBadge(
    statusText: expandable ? 'Setoran' : 'Pencairan',
    backgroundColor: expandable ? AppColors.greenLight : AppColors.warningLight,
    textColor: expandable ? AppColors.greenDark : AppColors.warning,
  );
}
```

## SOLID in this week's code

| Principle | Where | How |
|---|---|---|
| **Single responsibility** | `TransactionBatalSerializer`, the `batalkan` action, `TransactionService.batalkan_setoran` | The serializer validates the alasan, the view speaks HTTP (200, or 409 for `SaldoTidakCukup` and `SetoranDibatalkan`), and the service owns the rule, the locks and the saldo. On mobile, `BatalkanSetoranDialog` collects the alasan and shows errors, and `TransaksiNotifier` calls the use case. |
| **Open/closed** | `TransaksiQuerySet`, `AktivitasFilterBar(tipeTersedia:)` | New behaviour arrives as additions: a queryset method the reports read through, and a parameter the filter bar is configured with. Reopening Pencairan edits a constant, not the widget. |
| **Liskov substitution** | `TransaksiQuerySet` | It's a `QuerySet[Transaksi]`, so every function still typed against the base (the exporter's sheet builders, `apply_period`) takes it unchanged, while the reporting entry points call `.tercatat()` on it. |
| **Interface segregation** | `TransactionBatalSerializer`; the nasabah DTO | A client voiding a setoran sends one field and doesn't go through the edit serializer. The nasabah history DTO gains only `status`, not who voided it or why. |
| **Dependency inversion** | `TransaksiNotifier` → `BatalkanTransaksiUseCase` → `TransaksiRepository` | The notifier depends on the use case, and the use case on the repository interface, all injected by `injectable`. Tests swap the network for a `StubApi`. |

```dart title="lib/features/transaksi/domain/use_cases/batalkan_transaksi_usecase.dart"
@lazySingleton
class BatalkanTransaksiUseCase
    implements UseCase<TransaksiDetailEntity, TransaksiBatalRequest> {
  final TransaksiRepository repository;

  BatalkanTransaksiUseCase(this.repository);

  @override
  Future<Either<NetworkException, TransaksiDetailEntity>> execute(
      [TransaksiBatalRequest? args]) {
    return repository.batalkanTransaksi(args!);
  }
}
```

## GoF design patterns in this week's code

| Category | Pattern | Where + commit | What it does |
|---|---|---|---|
| Behavioural | **Observer** (via Riverpod) | `ref.listen(authenticationProvider, _onAuthChanged)` in Lengkapi Profil, [`3d0a81b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/3d0a81b3) and [`8bdb1b5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8bdb1b54) | One state change, a session with a new role, reaches the screen that owns the form, which resets itself |
| Behavioural | **Command** (loosely) | `BatalkanTransaksiUseCase.execute(TransaksiBatalRequest)`, [`5b76c4f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5b76c4f) | One request object, one `execute`, behind the project's `UseCase` interface. It's loosely Command: there's no undo or queue |

The other structures this week are labelled as what they are: the QuerySet method is a **Query Object / Specification** (PoEAA), the repository and use case are **Repository** and **Interactor** (Architectural), and the void is a **soft delete with audit fields** (Technique).
