# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code, all in [pilah-mobile #276](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/276) (PIL-539):

    - **One form, a layout per context:** a mode parameter chooses between the onboarding step and an in-app page, and the form fields and submit button are extracted once and shared (Extract Method).
    - **Show state, not absence:** the bank picker gets the reason a bank is unavailable together with its id, and disables the row instead of filtering it out.
    - **A narrow submit for a narrow context:** applying from inside the app sends only the application, through the notifier's existing request method.
    - **An existing convention reused:** the list reloads when the page it pushed returns `true`, as the detail page's appeal already does.
    - **The server stays the authority:** the app drops its one-bank lock for this flow, and [pilah-be #185](https://github.com/bank-sampah-PILAH/pilah-be/pull/185) pins the server rules it relies on.
    - **Design tokens** for the spacing in the code this PR moved.
    - **SOLID,** each principle with the code it applies to. See [SOLID in this week's code](#solid-in-this-weeks-code).

## The design issues in brief

- **No way in.** The backend already allowed a second membership, but an approved nasabah had no screen to apply from. *Fix:* "Ajukan bank baru" on Bank sampah saya.
- **One screen hard-wired to one context.** The registration form was an onboarding step: its stepper, its Keluar (log out) exit and its one-membership lock would all have applied to a signed-in nasabah applying from the app. *Fix:* a mode parameter, with the form shared by both layouts.
- **A picker that hid things without saying why.** Joined banks were silently dropped, so a nasabah looking for their own bank found nothing. A set of ids couldn't say why a bank was unavailable. *Fix:* pass a map from id to its status label, and disable the row.
- **One submit path shaped by onboarding.** It sent the profile draft, refreshed the session and followed the onboarding redirect, which would have moved a signed-in nasabah away from the page they came from. *Fix:* a second, narrow submit for the in-app context.
- **Literal spacing in touched code.** *Fix:* the spacing tokens, as the design guide asks for code being touched.

## Before and after

| What | Pattern | Before | After | The difference it made |
|---|---|---|---|---|
| Registration form (`8cb88a0`) | **Mode parameter** choosing the layout, with **Extract Method** (Fowler) for the shared parts | `RegisterNasabahScreen` was only an `OnboardingStepScaffold` step, with a stepper, Keluar and the lock | `RegisterNasabahMode { onboarding, additional }`. `build` picks `_additionalPage` or `_onboardingStep`; both use `_formFields()` and `_submitButton()` | The in-app page has a back button and no lock, and onboarding is unchanged: its tests didn't move |
| Bank picker (`6a4c4ed`) | No design pattern: a principle (show state; **Information Expert**) | `excludedBankIds`, a set of ids; joined banks were removed from the list | `joinedBanks`, a map from id to "Sudah tergabung", "Menunggu persetujuan" or "Pernah ditolak". The row stays, greyed, with a status badge and no `onTap` | The nasabah sees their banks and why each can't be picked again |
| Submitting from the app (`b34db8b`) | No design pattern: SRP (each context owns its after-submit step), DRY (one request method) | One `_onSubmit`: profile draft, then the application, then `refreshUser` and the onboarding redirect | In additional mode, `_applyToAnotherBank` calls `registerNasabah` only, pops `true` and toasts after navigation | No profile resent, no session touched, and the nasabah lands back where they started |
| Reloading the list (`9c7ecac`) | **Convention reuse** (push, then refresh on `true`), not a new callback | No entry point | `context.push<bool>(...).then((applied) { if (applied == true) load(silent: true); })` | The new pending application appears without a spinner, and going back without applying reloads nothing |
| Spacing (`41a4434`) | **Design tokens** | `24`, `16`, `12`, `8` written as numbers | `AppSpacing.xl`, `.lg`, `.md`, `.sm`. The two `20`s have no step on the scale, so they stay, and the layout doesn't move | The touched code follows the design guide; the 130 onboarding page tests pass before and after |

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [`_applyToAnotherBank` on the list](#refresh-on-return-a-reused-convention-9c7ecac) | **No entry point** to a flow the backend already allowed | Reuse the screen's push-then-refresh-on-`true` convention | Principle (consistency, DRY) | Designed in (PIL-539) |
| [`RegisterNasabahMode`](#one-form-a-layout-per-context-8cb88a0) | **One screen hard-wired to one context**: the onboarding lock, stepper and logout exit | A mode parameter chooses the layout; Extract Method for the shared form | Principle (SRP, OCP); Refactoring | Designed in |
| [`joinedBanks`](#the-reason-with-the-id-6a4c4ed) | **Silent filtering**: a set of ids can't say why a bank is unavailable | Pass the reason with the id, disable rather than hide | Principle (Information Expert; OCP) | Designed in (the issue asks to mark them) |
| [`_applyToAnotherBank` in the form](#a-narrow-submit-b34db8b) | **One submit path shaped by onboarding** | A second, narrow submit reusing the existing request method | Principle (SRP, DRY) | Designed in |
| [`AppSpacing`](#design-tokens-41a4434) | **Literal spacing** in touched code | Design tokens | Technique | Own refactor, from a hand check of the design lints |

## Mobile

### Refresh on return, a reused convention — [`9c7ecac`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9c7ecac2)

```dart title="lib/features/bank_sampah_approval/presentation/pages/approval_bank_sampah_list_page.dart"
/// PIL-539: the registration form, opened in-app for an account that
/// already has a membership. A submitted application pops `true`, and the
/// new one is pending, so the list is reloaded to show it.
void _applyToAnotherBank(BuildContext context, WidgetRef ref) {
  context.push<bool>(RegisterNasabahScreen.additionalRoute).then((applied) {
    if (applied == true && context.mounted) {
      ref.read(nasabahApprovalProvider.notifier).load(silent: true);
    }
  });
}
```

The list only navigates and refreshes; the form owns the application. The detail page's appeal already works this way, so there is one convention for "a page I opened changed something".

### One form, a layout per context — [`8cb88a0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/8cb88a07)

```dart title="lib/features/onboarding/presentation/pages/register_nasabah_screen.dart"
/// Where [RegisterNasabahScreen] was opened from.
enum RegisterNasabahMode {
  /// Step two of onboarding (PIL-204): the account's first application.
  onboarding,

  /// From "Bank sampah saya" (PIL-539): an account that already belongs to a
  /// bank sampah applies to another one, inside the app.
  additional,
}

bool get _isAdditional => widget.mode == RegisterNasabahMode.additional;

/// During onboarding (PIL-204) an existing membership — usually a
/// pengurus-entered record auto-linked at login — locks the picker, so the
/// step only lands the profile. Applying from inside the app (PIL-539) is
/// how a second membership is made, so it is never locked.
bool get _isLocked => !_isAdditional && _memberships.isNotEmpty;

@override
Widget build(BuildContext context) =>
    _isAdditional ? _additionalPage(context) : _onboardingStep(context);
```

`_additionalPage` is a `Scaffold` with `NasabahPageAppBar(showBack: true)` and the form inside a `ContentFrame`. `_onboardingStep` is the existing step. Both build their form from the same `_formFields()` and `_submitButton()`, so a field changes in one place. The new route, `/ajukan-bank-sampah`, sits behind the same platform guard as `/register-nasabah`.

### The reason with the id — [`6a4c4ed`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/6a4c4ed0)

```dart title="lib/features/onboarding/presentation/pages/register_nasabah_screen.dart"
/// How the picker labels a bank this account already applied to.
static String _joinedLabel(NasabahMembershipEntity membership) {
  switch (membership.status) {
    case 'pending':
      return 'Menunggu persetujuan';
    case 'rejected':
      return 'Pernah ditolak';
    default:
      return 'Sudah tergabung';
  }
}

// passed to the picker:
joinedBanks: {
  for (final membership in _memberships)
    membership.bankSampahId: _joinedLabel(membership),
},
```

```dart title="lib/features/onboarding/presentation/widgets/pilih_bank_sampah_bottom_sheet.dart"
final joinedLabel = widget.joinedBanks[bank.id];
return InkWell(
  // A bank already joined is shown but not offered again.
  onTap: joinedLabel == null ? () => context.pop(bank) : null,
  ...
      if (joinedLabel != null)
        CustomStatusBadge(
          statusText: joinedLabel,
          backgroundColor: AppColors.fill,
          textColor: AppColors.inkSoft,
        ),
```

The screen knows the memberships, so it names their status (Information Expert). The sheet renders whatever label it's given, so a new status needs no change to the sheet.

### A narrow submit — [`b34db8b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/b34db8be)

```dart title="lib/features/onboarding/presentation/pages/register_nasabah_screen.dart"
/// PIL-539: the account is signed in and onboarded, so only the
/// membership request is sent: no profile draft, no session refresh, no
/// onboarding redirect. The server owns the one-membership-per-bank rule
/// and answers a duplicate with its own reason, shown as is.
Future<void> _applyToAnotherBank() async {
  ...
  final (:result, :error) = await ref
      .read(onboardingProvider.notifier)
      .registerNasabah(RegisterNasabahRequest(bankSampahId: bank.id));
  if (!mounted) return;
  ...
  // Back to Bank sampah saya, which reloads on `true` and shows the new
  // application as pending. The toast is raised once that page is back.
  context.pop(true);
  AppNotification.afterNavigation(
    (context) => AppNotification.showSuccess(
      context,
      title: 'Pengajuan terkirim',
      message: 'Pengajuan ke ${bank.nama} menunggu persetujuan pengurus.',
    ),
  );
}
```

**The server stays the authority.** The client sends only the bank id. Who is applying comes from the session, and the one-membership-per-bank rule stays on the server, where [#185's tests](tdd.md#pilah-be-185-pil-539-backend) pin it. A refusal is shown with the server's own message.

### Design tokens — [`41a4434`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/41a44349)

The form fields and footer that #276 moved into shared methods still used bare numbers. The ones on the spacing scale became tokens: `24 → AppSpacing.xl`, `16 → lg`, `12 → md`, `8 → sm`. The two `20`s have no step on the scale and stay, so nothing moves on screen.

## SOLID in this week's code

| Principle | Where | How |
|---|---|---|
| **Single responsibility** | The list's `_applyToAnotherBank`; the form's `_applyToAnotherBank`; `_joinedLabel` | The list only navigates and refreshes. Each context's submit owns its own after-submit step. The screen maps a status to its label, and the sheet only displays it. |
| **Open/closed** | `RegisterNasabahMode`; `PilihBankSampahBottomSheet` | The in-app context was added as a new mode, leaving the onboarding step and its tests unchanged. The sheet renders any label it's given, so a new status needs no change to it. |
| **Liskov substitution** | Both layouts of `RegisterNasabahScreen` | Wherever the screen is used, it keeps one contract: it validates the picked bank, sends one application and reports the server's answer. Only the frame around the form differs. |
| **Interface segregation** | `RegisterNasabahRequest(bankSampahId:)` | The in-app submit sends only the bank id, not the profile fields the onboarding path also carries. |
| **Dependency inversion** | Both submits → `OnboardingNotifier.registerNasabah`; the list → `nasabahApprovalProvider` | The pages depend on the notifiers' methods, not on the API client, which is why the tests can mock the data source and fake the notifiers. |

## Patterns, labelled as what they are

- **Extract Method** (Fowler): `_formFields()` and `_submitButton()`, shared by both layouts.
- **A mode parameter**, not a GoF pattern: the screen chooses its layout from an enum. A Strategy object would be heavier than two layouts need.
- **Information Expert** (GRASP): the screen, which holds the memberships, names their status.
- **Design tokens:** `AppSpacing`.
- **Convention reuse:** push, then refresh on `true`. No pattern is claimed for it.
