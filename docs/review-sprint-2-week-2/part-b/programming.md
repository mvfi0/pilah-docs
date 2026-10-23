# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in the two QA fixes:

    - SOLID: single responsibility and open/closed. See [SOLID in this week's code](#solid-in-this-weeks-code).
    - Information Expert: the "is this nasabah short?" rule lives next to the ceiling it describes.
    - A derived flag computed from state, never stored.
    - Command–query separation, reached through an Extract Method refactor.
    - One lock flag driving every locked field through the same `enabled` convention.

    Each item names the design issue it addresses, the pattern or principle used, its type and where the issue came from.

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [`melebihiSaldo`](#the-rule-lives-with-the-ceiling-0511e1b) | **Duplicated business rule:** the screen needs "is this nasabah short?", and recomputing it in the UI would duplicate `hitung`'s ceiling, so the two could drift | **Information Expert** (GRASP): `JumlahUmum`, which owns the ceiling, answers the question | Principle (GRASP) | Designed in (PIL-374) |
| [`dibatasiSaldo`](#a-derived-flag-not-a-stored-one-bcde54e) | **Stale state:** a stored "capped" flag would go out of date the moment the pengurus types a nominal | **Derived state / single source of truth:** a query method computes it from the applied Nominal and the item | Technique (derived state) | Designed in (PIL-374) |
| [`_setujuSaldoKurang`](#asking-and-applying-split-450bf39) | **Long method mixing a question with an action:** `_terapkan` both built the confirmation and applied the settings, at cognitive complexity 17 of 15 | **Extract Method** (Fowler) towards **command–query separation**: one method answers "may this be applied?", the other applies | Refactoring + principle | Tool finding on my own code (SonarCloud S3776) |
| [`isi:` slot](#the-dialog-extended-not-edited-b5c6b79) | **Changing a shared dialog** to add one caller's content | **Open/closed via composition:** `showPencairanKonfirmasi` already takes an `isi` widget, so the list is passed in and the dialog is unchanged | Principle (SOLID OCP) | Designed in (PIL-374) |
| [`enabled`](#one-lock-flag-the-same-convention-6e15f8c) | **Inconsistent locked state:** one flag (`_terkunci`) disabled the Nominal, while the Tanggal only ignored taps and still looked active | **One flag through a uniform interface:** the field takes `enabled`, as Material's own fields do, and `_terkunci` drives both | Technique (consistency) | QA finding (PIL-375) |

The GoF patterns these changes sit on are listed in [GoF design patterns in this week's code](#gof-design-patterns-in-this-weeks-code).

## PIL-374: the saldo warning (21 Oct)

### The rule lives with the ceiling — [`0511e1b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/0511e1b)

`hitung` already caps a fixed rupiah at the saldo. The question "will this nasabah get less than asked?" is the same rule seen from the other side, so it sits right below it, in the same class:

```dart title="lib/features/draft_pencairan/domain/model/draft_pencairan.dart"
int hitung(int saldo) {
  switch (jenis) {
    case JumlahJenis.persen:
      return _persenDari(saldo, nilai);
    case JumlahJenis.rupiah:
      final tetap = nilai.floor();
      return tetap < saldo ? tetap : saldo;
  }
}

/// Whether a nasabah with [saldo] gets less than this asks for: a fixed
/// rupiah above their saldo, so [hitung] pays them their whole saldo.
bool melebihiSaldo(int saldo) =>
    jenis == JumlahJenis.rupiah && valid && nilai.floor() > saldo;
```

The note under the field, the confirmation, its list and each card's line all ask `melebihiSaldo`. None of them compares amounts itself. The reviewer checked the edge case: a saldo exactly equal to the Nominal is paid in full, and isn't warned about.

### A derived flag, not a stored one — [`bcde54e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bcde54e)

```dart title="lib/features/draft_pencairan/presentation/blocs/draft_editor_state.dart"
bool dibatasiSaldo(EditorItem item) {
  final jumlah = jumlahUmum;
  return jumlah != null &&
      jumlah.melebihiSaldo(item.saldo) &&
      item.nominal == item.saldo;
}
```

The card's warning is computed from what is already in the state: the applied Nominal, the item's saldo and its nominal. There is no flag to keep in sync. When the pengurus types a different nominal, the warning goes because the condition no longer holds.

### Asking and applying, split — [`450bf39`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/450bf39)

SonarCloud flagged `_terapkan` (S3776, complexity 17 of 15) once it held both the confirmation and the apply. Extracting the question gives each method one job:

```dart title="lib/features/draft_pencairan/presentation/pages/draft_editor_page.dart"
/// True when there is nothing to confirm or the pengurus says yes.
Future<bool> _setujuSaldoKurang(JumlahUmum? jumlah) async {
  final kurang = _jumlahKurang(jumlah);
  if (jumlah == null || kurang == 0) return true;
  return showPencairanKonfirmasi(
    context,
    icon: Icons.warning_amber_rounded,
    judul: 'Terapkan Nominal ${rupiah(jumlah.nilai.floor())}?',
    pesan: _pesanKurang(kurang, jumlah),
    isi: _DaftarSaldoKurang(
      items: [
        for (final item in _items)
          if (jumlah.melebihiSaldo(item.saldo)) item,
      ],
    ),
    jawaban: const KonfirmasiJawaban('Ya, terapkan'),
    nada: KonfirmasiNada.peringatan,
  );
}

Future<void> _terapkan() async {
  final jumlah = _jumlahBerubah ? _jumlah : null;
  if (!await _setujuSaldoKurang(jumlah) || !mounted) return;
  context.read<DraftEditorCubit>().terapkanUmum(
        metode: _metodeBerubah ? _metode : null,
        jumlah: jumlah,
        potongan: _potonganBerubah ? _potongan : null,
      );
  // …
}
```

The behaviour didn't change, and the same tests stayed green. SonarCloud closed the issue on the next analysis.

### The dialog extended, not edited — [`b5c6b79`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b5c6b79)

The confirmation is the shared `showPencairanKonfirmasi`, which already accepts an `isi` widget between its message and its buttons. The list of affected nasabah, with name and saldo, is a small `_DaftarSaldoKurang` widget passed into that slot. The dialog function is untouched. The other screens that use it (konfirmasi pembayaran, batalkan, buang perubahan) can't be affected.

## PIL-375: the locked Tanggal (21 Oct)

### One lock flag, the same convention — [`6e15f8c`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6e15f8c)

Edit Pencairan already had one rule for "this pencairan's amount and date are fixed": `_terkunci => potongan > 0`. It disabled the Nominal field, but the Tanggal only had a guard inside its tap handler, so it still looked editable. Now the same flag drives both, through the same `enabled` parameter Material's fields use:

```dart title="lib/features/pencairan/presentation/widgets/pencairan_form_fields.dart"
InkWell(
  key: const Key('tanggal-field'),
  onTap: enabled ? onTap : null,
  child: InputDecorator(
    decoration: appInputDecoration(
      suffixIcon: const Icon(Icons.calendar_month, color: AppColors.grey100),
      errorText: errorText,
    ).copyWith(enabled: enabled),
    // …
```

```dart title="lib/features/pencairan/presentation/pages/edit_pencairan_page.dart"
TanggalPencairanField(
  tanggal: _tanggal,
  onTap: _pickTanggal,
  errorText: state.fieldErrors['tanggal'],
  enabled: !_terkunci,
),
```

`enabled` defaults to `true`, so the field's existing callers are unchanged.

## SOLID in this week's code

| Principle | Where | How |
|---|---|---|
| **Single responsibility** | [`_setujuSaldoKurang` / `_terapkan`](#asking-and-applying-split-450bf39) | One method decides whether to proceed (and asks), the other applies. Each changes for one reason. |
| **Open/closed** | [`showPencairanKonfirmasi(isi:)`](#the-dialog-extended-not-edited-b5c6b79), [`TanggalPencairanField(enabled:)`](#one-lock-flag-the-same-convention-6e15f8c) | New behaviour arrives through a slot and a defaulted parameter. The shared dialog and the field's existing uses are not modified. |
| **Dependency inversion** (kept) | The editor's cubit | The saldo checks are plain domain methods. The cubit still depends on the `DraftPencairanRepository` interface, which is why the tests mock it. |

## GoF design patterns in this week's code

- **Observer:** the cubit emits states and `BlocBuilder` rebuilds the editor. That is how the note, the cards and the totals follow the applied Nominal without being told.
- **Strategy:** `showPencairanKonfirmasi` goes through `showAdaptiveConfirmation`, which picks the presentation (a sheet on a phone, a dialog in a browser) from the window width. The caller's code is the same either way.
