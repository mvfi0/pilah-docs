# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code:

    - **One named rule, applied at the right boundary.** "What still counts" is `Transaksi.objects.tercatat()`. This week it reached the two seed commands that bypassed it, and every riwayat list. The shared lookup that detail, edit and void read stays unfiltered, so a voided row is still reachable for audit.
    - **UI state that follows the server, not the widget.** The Hapus dialog reads what it needs before the request, applies the server's answer whether or not it is still open, and only pops itself while it is the route on top.
    - **One owner for "what reloads after a setoran changes":** a helper that the single void uses now, and edit and bulk can reuse.
    - **A report that stops publishing an internal key,** with the tests first decoupled from it.
    - **All five SOLID principles,** each with the code it applies to. See [SOLID in this week's code](#solid-in-this-weeks-code).

    Each item names the design issue it addresses, the pattern or principle used, its type and where the issue came from. The same three lines are in each commit body.

## The design issues in brief

- **A rule that two writers didn't follow.** "A voided setoran doesn't count" had one name, `tercatat()`, but two seed commands summed the raw table, so re-seeding after a void put the money back. *Fix:* the seeds call the same method as the reports.
- **One query, two different needs.** The riwayat lists must hide a void, but detail, edit and void must still find it, and filtering the shared query would make a voided setoran's detail a 404. *Fix:* each list filters; the shared lookup doesn't.
- **UI state tied to the widget, not to the server.** If the Hapus dialog was closed mid-request, the app skipped the refresh, although the server had voided the setoran, and a late `pop` could close the wrong page. *Fix:* read what's needed before the request, always apply the server's answer, and close the dialog only if it's still on top.
- **Each action refreshing its own list of screens.** The single void reloaded one screen, the bulk void four. *Fix:* one helper owns what reloads after a setoran changes, and reloads only screens already open.
- **An internal key in a user's report.** The export showed a database id no pengurus reads, and two tests depended on it. *Fix:* the tests check visible data first, then the column goes.
- **Text describing an old rule.** The dialogs said a void stays in the riwayat, which stopped being true. *Fix:* change the text next to the flow it describes, and pin it with a test.

## Before and after

What each design change did, compared with the code before it.

| What | Before | After | The difference it made |
|---|---|---|---|
| Seed commands (#145) | `Transaksi.objects.filter(...)` summed every setoran, voided ones included | `Transaksi.objects.tercatat().filter(...)`, the method the reports use | Re-seeding after a void no longer puts the voided money back into a saldo |
| Riwayat lists (#167) | `activity_sources` started from `Transaksi.objects.filter(bank_sampah=bank)`, so a void stayed listed, labelled Dibatalkan | It starts from `Transaksi.objects.tercatat()`. On the nasabah side, `activities(member).tercatat()` at the two list call sites, while the lookup returns everything | A Hapus now reads as a delete in every list, as the UAT asked, yet a voided setoran's detail still answers 200 with who, when and why |
| Hapus dialog (#193) | Any tap outside or back closed it mid-request. Everything after the request sat behind `if (!mounted) return;` | `PopScope(canPop: !_saving)`, notifiers read before the `await`, the server's answer always applied, and the pop guarded by `route.isCurrent` | A void that succeeds always refreshes the feed, and a late answer can no longer close the Riwayat page underneath |
| Reload after a void (#193) | The single void reloaded Riwayat only, so the dashboard, recent activity and nasabah saldo stayed stale. The bulk void reloaded four screens its own way | One helper, `reloadAfterSetoranChange`, owns the list and checks `container.exists` | Every screen already open shows the new totals, and no request is sent for a screen never opened |
| Export (#168) | 14 columns (`A:N`), the last an internal id; two tests counted rows through it | 13 columns (`A:M`); the tests count rows that carry a value | The pengurus's report holds only what they read, and no internal record id leaves the system in a forwarded file |

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [Seed commands](#the-named-rule-reaches-two-more-writers-abcafa3) | **A second write path that bypasses a named rule:** the seeds rebuilt the saldo from the raw table, voided setoran included | **Reuse the named query** (Specification-style QuerySet method) instead of a second ad-hoc filter | Architectural (PoEAA Query Object) | **Review defect** ([Heraldo, #145](https://github.com/bank-sampah-PILAH/pilah-be/pull/145#discussion_r4456211899)) |
| [`activity_sources`](#lists-filter-the-lookup-does-not-6995649-c3606b5) | **One shared query serving a rule it was never given:** the feed's source query never read through `tercatat()` | **Single source of truth** at the shared query, so every consumer inherits it | Principle (DRY, OCP) | Reversal of a PIL-428 design decision, asked for by the UAT |
| [List boundaries vs the lookup](#lists-filter-the-lookup-does-not-6995649-c3606b5) | **One helper serving two needs:** `activities()` and `get_queryset` back both the lists and the detail lookup, so filtering inside them would turn a voided detail into a 404 | **Filter at each list call site, keep the lookup as is** | Principle (ISP, SRP) | Designed in, while tracing PIL-481 |
| [`BatalkanSetoranDialog._hapus`](#the-dialog-follows-the-servers-answer-472c506) | **UI state tied to the widget's lifetime:** a dialog closed mid-request skipped the refresh, and a late `pop` closed the wrong route | **Capture dependencies before the async gap; apply the outcome unconditionally; guard navigation on the route, not on `mounted`** | Technique (Flutter async lifecycle) | **Review defect** ([Heraldo, #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193#discussion_r4456406981)), plus the exit-animation case I found writing its test |
| [`reloadAfterSetoranChange`](#one-owner-for-what-reloads-be7b6d0) | **Each write path refreshing its own subset of views:** the bulk void reloaded four, the single void one | **One helper owns the reload set**; screens never opened are not built | Principle (SRP, DRY) | **Review defect** ([Scallss, #193](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/193)) |
| [Export columns](#a-report-without-an-internal-key-9dbfcf2-2b1fba9) | **An internal surrogate key in a user-facing report,** and tests coupled to it | **Assert on visible data, not on a surrogate key**; the export lists only what a pengurus reads | Principle (SRP) | UAT finding (PIL-480) |
| [Hapus copy](#copy-that-follows-the-rule-ff86f6f) | **User-facing copy describing a backend rule** that PIL-481 reversed | **Change the copy next to the flow it describes,** pinned by a widget test | Technique | Found by tracing PIL-481, not named in the issue |

## Backend

### The named rule reaches two more writers — [`abcafa3`](https://github.com/bank-sampah-PILAH/pilah-be/commit/abcafa30)

Last week's refactor named the rule once. Heraldo found that two seed commands, one of them run on every production demo seeding, still summed the raw table:

```python title="api/management/commands/seed_play_demo_accounts.py"
# A voided setoran stays in the table but not in the saldo (PIL-428).
setoran = Transaksi.objects.tercatat().filter(
    ...
)
```

Both seeds now read through the same method the reports use. I checked every other place that sums setoran outside the tests: these two were the only gap.

### Lists filter, the lookup does not — [`6995649`](https://github.com/bank-sampah-PILAH/pilah-be/commit/69956494), [`c3606b5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/c3606b52)

The riwayat feed has one source query, so the rule goes there and every consumer inherits it:

```python title="apps/ledger/activity.py"
def activity_sources(...):
    """One authorization/filter policy for history, totals and exports.

    A voided setoran is not part of any of them (PIL-481): the riwayat does not list it,
    and it counts toward nothing. The row itself stays, as the audit trail.
    """
    deposits = Transaksi.objects.tercatat().filter(bank_sampah=bank)
```

On the nasabah side the same helper backs the lists and the detail lookup, so the rule goes at the two list call sites instead:

```python title="apps/nasabah/home.py"
def activities(member: Nasabah) -> TransaksiQuerySet:
    """Every setoran of the member, voided ones included: the detail lookup needs them.

    The lists read ``activities(member).tercatat()`` instead (PIL-481).
    """
    ...

"aktivitas_terbaru": activities(member).tercatat()[:5],
```

Returning `TransaksiQuerySet` rather than a plain `QuerySet[Transaksi]` is what lets the callers ask for `.tercatat()`. The pengurus side does the same: the `/transaksi` list and the dashboard's recent list filter, while `TransaksiViewSet.get_queryset`, which detail, edit and void also read, does not.

### A report without an internal key — [`9dbfcf2`](https://github.com/bank-sampah-PILAH/pilah-be/commit/9dbfcf26), [`2b1fba9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2b1fba90)

The UAT found the "ID Aktivitas" column useless to the Pengurus. Two tests used it to count rows, so they were refactored first to count rows that carry a value. Then the column went, with the title merges and widths moved from `A:N` to `A:M`. "ID Nasabah", the member number a pengurus does read, stays.

## Mobile

### The dialog follows the server's answer — [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b)

```dart title="lib/features/transaksi/presentation/widgets/batalkan_setoran_dialog.dart"
// Read before the await: the dialog may be gone when the answer arrives.
final selection = ref.read(aktivitasSelectionProvider.notifier);
final riwayat = ref.read(riwayatAktivitasProvider.notifier);
final route = ModalRoute.of(context);
...
if (result.detail != null) {
  // The setoran is voided on the server whether or not this dialog is
  // still open, so the feed and the selection always follow it.
  selection.clear();
  riwayat.load(silent: true);
}
// Closed by other means while the request was in flight. Popping now
// would close the route underneath (the Riwayat page) instead.
if (!mounted || route?.isCurrent != true) return;
```

```dart title="lib/features/transaksi/presentation/widgets/batalkan_setoran_dialog.dart"
// While the void is sent, a barrier tap or the back button must not close
// the dialog: only its answer does. Idle, both still close it.
return PopScope(
  canPop: !_saving,
  child: _dialog(context),
);
```

The old code put everything after `if (!mounted) return;`. That tied the refresh to the widget's lifetime, so a void that succeeded on the server could leave the feed showing it as recorded.

### One owner for what reloads — [`be7b6d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/be7b6d06)

```dart title="lib/features/transaksi/presentation/providers/setoran_refresh.dart"
/// Reloads every view that shows setoran totals after a setoran changed on
/// the server: Riwayat, and the dashboard, recent activity and nasabah saldo
/// when the pengurus already opened them. Screens never opened are not built.
void reloadAfterSetoranChange(ProviderContainer container) {
  container.read(riwayatAktivitasProvider.notifier).load(silent: true);
  if (container.exists(dashboardProvider)) {
    container.read(dashboardProvider.notifier).loadStats(silent: true);
  }
  if (container.exists(recentActivityProvider)) {
    container.read(recentActivityProvider.notifier).load(silent: true);
  }
  if (container.exists(nasabahProvider)) {
    container.read(nasabahProvider.notifier).loadNasabah(silent: true);
  }
}
```

`container.exists` is the point: reading a provider that was never built would build it and fire a request for a screen the pengurus never opened. Edit has the same stale-screen gap on `staging`. Scallss agreed it is a separate follow-up, so it was left out of this PR.

### Copy that follows the rule — [`ff86f6f`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ff86f6f4)

The single and bulk Hapus dialogs said the setoran "stays in the riwayat, marked dibatalkan". After PIL-481 that's false. The copy now says it is hidden from the riwayat and no longer counted, next to the flow it describes, with a widget test that pins it.

## SOLID in this week's code

| Principle | Where | How |
|---|---|---|
| **Single responsibility** | `activities()` vs its list callers; the exporter; `reloadAfterSetoranChange` | The lookup returns every row and the lists choose the counted ones. The exporter formats a report and doesn't publish keys. One helper owns the reload set, and the dialog only collects the alasan and sends it. |
| **Open/closed** | `activity_sources` | The rule sits in the shared source query, so a new consumer of the feed (a new export, a new total) gets it without being edited. |
| **Liskov substitution** | `TransaksiQuerySet` returned from `activities()` and `get_queryset` | It's a `QuerySet[Transaksi]`, so every existing caller works unchanged, while the list callers can now ask for `.tercatat()`. |
| **Interface segregation** | List endpoints vs the detail lookup | List consumers ask for the counted subset explicitly. The detail, edit and void paths keep an interface that still includes voided rows, because they need them. |
| **Dependency inversion** | The dialog → `reloadAfterSetoranChange(ProviderContainer)` | The dialog depends on the provider container it is given, not on which screens exist. Tests pass their own container with a stub API and read the providers back. |

```dart title="lib/features/transaksi/presentation/widgets/batalkan_setoran_dialog.dart"
final container = ProviderScope.containerOf(context, listen: false);
...
container.read(aktivitasSelectionProvider.notifier).clear();
reloadAfterSetoranChange(container);
```

## Patterns, labelled as what they are

- **Query Object / Specification** (PoEAA): `TransaksiQuerySet.tercatat()`, now reused by the seeds and every list.
- **Observer** (via Riverpod): the screens listen to their providers, so a reload of the notifier redraws the dashboard and the nasabah list without the dialog knowing about them.
- The dialog fix is a **technique** for Flutter's async lifecycle, not a design pattern, and is labelled that way in the commit.
