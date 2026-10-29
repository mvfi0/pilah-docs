# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in PIL-451's two MRs:

    - All five SOLID principles, each with the code it applies to. See [SOLID in this week's code](#solid-in-this-weeks-code).
    - A guarded state transition done as one conditional `UPDATE`, instead of check-then-save.
    - An append-only audit log for a privilege change.
    - Session renewal when the privilege level changes.
    - One page serving two entry states, decided once.
    - A single source of truth for role titles.
    - Extract Method, once from a SonarCloud finding and once on my own initiative.

    Each item names the design issue it addresses, the pattern or principle used, its type and where the issue came from.

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [`change_role`](#a-guarded-transition-in-one-statement-52f087f) | **Check-then-act race:** reading the onboarding state, then saving the role, leaves a window in which a bank registration commits and is stranded under the wrong role | **Guarded state transition** as a single conditional `UPDATE`: the database re-checks the row as it writes it | Technique (concurrency) | Designed in. Incomplete: reviewers found the other side of the race, still open ([TDM](team-development-management.md#reviews-received-on-137)) |
| [`role=previous`](#the-log-cannot-lie-2c591c5) | **A double tap could log a transition that never happened** (`from_role` read, then changed by another request) | **Compare-and-set** on the role read in the same transaction | Technique (optimistic check) | Designed in, while writing the audit slice |
| [`UserRoleChangeLog`](#the-log-cannot-lie-2c591c5) | **No accountability** for a privilege change | **Audit Log** (Fowler): an append-only row per change, written in the same transaction, same shape as `BankSampahApprovalLog` | Architectural | Designed in (OWASP A09) |
| [`_session_response`](#a-new-session-for-a-new-privilege-13c1a44) | **A stale privilege in the token:** the access token carries a `role` claim | **Renew the session on a privilege change** (OWASP Session Management) | Principle (security) | Designed in (OWASP A07) |
| [The role page](#one-page-two-entry-states-9517dbd) | **A create-only screen:** the role page could only create an account, so a role saved on the server had no way back from the client | **One page, two entry states,** decided once in `initState`; submit and listener branch on it, with no second page duplicating the cards | Technique | QA finding (PIL-451) on PIL-180's design |
| [`titleFor`](#role-titles-from-one-place-a1b49bd) | **Duplicated knowledge:** Lengkapi Profil needs the role's display title, which the role page's options already define | **Single source of truth (DRY):** a static query over the same `_roleOptions` the cards are drawn from | Principle | Designed in |
| [`ref.watch`](#the-screen-follows-the-session-a1b49bd) | **A stale screen:** after a role change, go_router returns to the same `/complete-profile` State, which still drew the old role's form | **Observer:** the screen subscribes to the auth state and rebuilds when it changes | GoF Behavioural (via Riverpod) | Found by the red test in [`9e83120`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9e83120) |
| [`_changeableRoleTitle`](#a-rule-out-of-a-build-method-87f2f0d) | **A long method mixing layout with a business rule:** `build` at cognitive complexity 17 of 15 | **Extract Method** (Fowler): a query method that names the rule | Refactoring | Tool finding on my own code (SonarCloud S3776) |
| [`_submit`](#a-rule-out-of-a-build-method-87f2f0d) | **A nested ternary** choosing between two actions inside `onPressed` | **Extract Method** | Refactoring | My own `[REFACTOR]` |

## Backend: [pilah-be #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137) (26 Oct)

### A guarded transition in one statement — [`52f087f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/52f087f)

A role may change only while onboarding has committed nothing for it. Reading those conditions and then saving would leave a window, so the conditions are part of the `UPDATE` itself:

```python title="apps/authentication/services.py"
with transaction.atomic():
    previous = User.objects.filter(pk=user.pk).values_list("role", flat=True).get()
    updated = User.objects.filter(
        pk=user.pk,
        role=previous,
        is_profile_complete=False,
        bank_sampah__isnull=True,
        keanggotaan_nasabah__isnull=True,
    ).update(role=role, updated_at=timezone.now())
    if updated == 0:
        raise AuthServiceError(
            "Peran tidak dapat diganti setelah pendaftaran berjalan.",
            code="role_locked",
            status_code=409,
        )
```

The `UPDATE` also replaces a 500. `User.clean` used to be the only thing stopping a member from changing role, and its `ValidationError` escaped unhandled. The membership condition is now in the filter, and the refusal is a clean 409.

**What it doesn't cover.** Tristan (P1) and Pascal pointed out the other side of the race. `register_bank_sampah` checks `user.role`, then saves `user.bank_sampah` later with no lock, so a role change committing in between still slips through. The fix needs both paths to lock the user row. It's open, and recorded on the [TDM page](team-development-management.md#reviews-received-on-137).

### The log cannot lie — [`2c591c5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2c591c5)

The audit row follows the project's existing approval logs: append-only, written only by the service, in the same transaction as the change. The `role=previous` condition above means a concurrent change updates 0 rows instead of logging a `from_role` the account no longer had.

```python title="apps/authentication/models.py"
class UserRoleChangeLog(models.Model):
    """A role an account switched away from during onboarding (PIL-451).

    Written only by AuthService.change_role, in the same transaction as the
    change; rows are never edited.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="role_change_logs")
    from_role = models.CharField(max_length=20, choices=User.Role.choices)
    to_role = models.CharField(max_length=20, choices=User.Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)
```

### A new session for a new privilege — [`13c1a44`](https://github.com/bank-sampah-PILAH/pilah-be/commit/13c1a44)

The endpoint answers with the same session payload as a Google login, built by the existing `AuthService._session_response`. So the new access token names the new role, and the client routes on `next_step` exactly as it does after registering.

Pascal noted that the *old* tokens aren't revoked: the access token lasts 24 h and the refresh token 30 d. Nothing reads a role from the token today, so it's harmless, but my PR description overstated it. That correction is open with his review.

## Mobile: [pilah-mobile #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174) (26 Oct)

### One page, two entry states — [`9517dbd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9517dbd)

The role page served only a fresh Google registration, holding a registration token. Rather than copying its role cards into a second page, it decides once which kind of visit this is:

```dart title="lib/features/authentication/presentation/pages/role_selection_page.dart"
@override
void initState() {
  super.initState();
  final state = ref.read(authenticationProvider);
  _registration = _registrationFrom(state);
  if (_registration == null &&
      state is Authenticated &&
      state.authEntity.nextStep == 'complete_profile') {
    _account = state.authEntity;
    _selectedRole = GoogleRegistrationRole.values
        .where((role) => role.wireValue == state.authEntity.role)
        .firstOrNull;
  }
}
```

A success returns as a new `Authenticated` session, which the page's existing listener already routes through `locationForAuthStep`. A refusal comes back as a message, so the notifier never replaces the signed-in state with a failure state.

### Role titles from one place — [`a1b49bd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a1b49bd)

```dart title="lib/features/authentication/presentation/pages/role_selection_page.dart"
static String? titleFor(String? role) => _roleOptions
    .where((option) => option.value.wireValue == role)
    .firstOrNull
    ?.title;
```

### The screen follows the session — [`a1b49bd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a1b49bd)

Lengkapi Profil used to only *listen* to the auth state, to catch a logout. After a role change, go_router returns to the same `/complete-profile` page with its State intact. So the screen now also *watches* the auth state, and redraws the new role's stepper and fields. The red test proved this before the change, with the label assertion removed.

### A rule out of a build method — [`87f2f0d`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/87f2f0d)

SonarCloud flagged `build` (S3776, complexity 17 of 15) after the role note added an `Authenticated` check and a three-part condition. The rule now has a name:

```dart title="lib/features/onboarding/presentation/pages/complete_profile_screen.dart"
/// The title of the role this account registers as, while it may still be
/// changed (PIL-451): the role was saved on the role page and stays
/// changeable until a bank sampah is registered for it. An invite fixes the
/// role, so it gets none. Null when the note should not show.
String? _changeableRoleTitle(AuthenticationStates state) {
  if (_isInviteMode || state is! Authenticated) return null;
  if (state.authEntity.bankSampahStatus != null) return null;
  return RoleSelectionPage.titleFor(state.authEntity.role);
}
```

`build` now only places the note when it gets a title. In the same spirit, [`2589b0b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/2589b0b) moved the role page's register-or-change choice out of `onPressed` into `_submit`.

## SOLID in this week's code

| Principle | Where | How |
|---|---|---|
| **Single responsibility** | `RoleChangeView`, `RoleChangeSerializer`, `AuthService.change_role` | The view speaks HTTP, the serializer validates the one input, and the service owns the rule, the update and the log. Each changes for one reason. On mobile, `_changeableRoleTitle` decides and `build` lays out. |
| **Open/closed** | The new endpoint and `UserRoleChangeLog` | Role changes arrive as an addition. `register_with_google`, `GoogleRegistrationView` and `IsRegistrationRole` are untouched, and the existing `_session_response` is reused, not edited. |
| **Liskov substitution** | Every `AuthRepository` implementation | `AuthRepositoryImpl`, the offline preview session and the test doubles all gained `changeRole` with the same contract: a session on success, a failure on refusal. Any of them can stand in for the real one, which is what lets the page and notifier tests run without a server. |
| **Interface segregation** | `RoleChangeSerializer`, `AuthRemoteDataSources.changeRole(String role)` | A client changing a role sends one field. It doesn't go through the registration serializer, which also needs a `registration_token`. |
| **Dependency inversion** | `AuthenticationNotifier` → `LoginWithGoogleUseCase` → `AuthRepository` | The notifier depends on the use case, and the use case on the repository *interface*. Tests inject mocktail mocks at each level. |

```dart title="lib/features/authentication/presentation/providers/authentication_provider.dart"
/// Switches a registering account to [role]. Returns null once the session
/// for the new role is in place, or the server's reason when the change is
/// refused, in which case the current session is left as it was.
Future<String?> changeRole(GoogleRegistrationRole role) async {
  final result = await _loginWithGoogleUseCase.changeRole(role);
  return result.fold(
    (failure) => failure.displayMessage,
    (entity) {
      _emitAuthenticated(entity);
      return null;
    },
  );
}
```

## GoF design patterns in this week's code

| Category | Pattern | Where + commit | What it does |
|---|---|---|---|
| Behavioural | **Observer** (via Riverpod) | `ref.watch(authenticationProvider)` in Lengkapi Profil, [`a1b49bd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a1b49bd) (mine). It joins the role page's `ref.listen`, which Tristan's Riverpod migration introduced ([`efd6748`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/efd6748), #160, 24 Oct) | One state change, a new session, reaches every subscribed screen. The role page routes on it, and Lengkapi Profil redraws for it. |

The other structures this work builds on aren't GoF, so they're labelled as what they are:

- **Repository** (Architectural, PoEAA): `AuthRepository` dates from the 2024 template (`d2c9eb3`). This week extends it.
- **Use case / Interactor** (Architectural, Clean Architecture): `LoginWithGoogleUseCase` dates from June (`910bad8`). This week extends it.
- **Audit Log** (Architectural): new this week in [`2c591c5`](https://github.com/bank-sampah-PILAH/pilah-be/commit/2c591c5), shaped like the initial backend's approval logs.
