# Programming

!!! success "Competency level: 3"
    Standard principles applied and shown in this week's code:

    - **Validation at the boundary, in one place:** a `shared_kernel` helper turns a raw query parameter into a UUID or a keyed 422, so no view hands untrusted text to the ORM.
    - **Validate first, then query:** two uniqueness checks now run on the validated value instead of the raw body, one moved into its serializer and one after validation in its view. That fixed a NUL crash and a padded-duplicate bypass together.
    - **A narrow serializer the wider one extends,** so `DELETE` validates exactly what it reads.
    - **A domain rule guarded by a test,** not by memory: an architecture test makes `tercatat()` the only way to say "counted setoran".
    - **One lock for every writer of an invariant:** profile completion became the fifth writer to take the shared account lock.
    - **A navigation policy reused,** not rewritten, and **Extract Method** from a SonarCloud finding.
    - **All five SOLID principles,** each with the code it applies to. See [SOLID in this week's code](#solid-in-this-weeks-code).

## The design issues in brief

- **One input check written three times, with two copies missing.** `nasabah_id` reached the database unchecked on two lists, so a typo was a server error. *Fix:* one validator in the shared kernel that every list calls.
- **A rule kept only by memory.** `tercatat()` names "counted setoran", but nothing stopped a new query from writing the filter by hand, and one did. *Fix:* a test that reads the source and fails on any hand-written copy.
- **Checking one value and saving another.** The duplicate-kode check read the raw request before validation, while the save used the cleaned value, so a NUL byte crashed the check and `" HDPE "` slipped past it. *Fix:* check after validation, in the serializer.
- **Two verbs validating one field two ways.** `POST` validated the device token properly; `DELETE` had a hand-written check that missed the NUL byte. *Fix:* a small serializer for `DELETE` that the `POST` one extends.
- **A writer that skipped the shared lock.** Profile completion changed the account without the lock the other four writers take, so it could answer with a stale role. *Fix:* it takes the same `lock_account`.
- **A page with no way back on web.** The role page was pushed, and a push isn't in the browser history. *Fix:* reuse the onboarding steps' existing back policy, then extract it from `build` when SonarCloud flagged the complexity.
- **One message worded three ways.** The single dialog, the bulk dialog and the toast described a void differently. *Fix:* one named constant per message.

## Before and after

What each design change did, compared with the code before it.

| What | Before | After | The difference it made |
|---|---|---|---|
| `nasabah_id` filter (#175) | `/transaksi` and `/pencairan` did `qs.filter(nasabah_id=nasabah_id)` on the raw text; `/aktivitas` had its own `try/except` | All three call `validasi_uuid(nasabah_id, kunci="nasabah_id")` from `shared_kernel` | A malformed id is a 422 with the key named, on every list. ZAP's 9 Nov scan got 226 × 500; the 17 Nov scan got 965 × 422 and no 500 |
| Duplicate kode (#177) | The jenis sampah view overrode `update` and queried `request.data.get("kode")` before validation | `validate_kode` in the serializer checks the stripped, validated value; the override is gone | A NUL byte is a 422, not a 500, and `" HDPE "` can no longer take another item's kode. `PUT` and `PATCH` follow one rule |
| Device token (#177) | `DELETE` checked `isinstance(token, str)` and the length by hand | `ForgetDeviceTokenSerializer`, which the `POST` serializer extends | Both verbs validate the token with the same field, so a NUL token is a 422 on logout too |
| Waste categories (#176) | `DetailTransaksi.objects.filter(transaksi__status=Transaksi.Status.TERCATAT, ...)`, the rule written by hand | `transaksi__in=Transaksi.objects.tercatat().filter(...)`, plus an architecture test | Same numbers, but the rule has one home, and a new hand-written copy fails CI instead of waiting for a reviewer to notice |
| Profile completion (#137) | `complete_profile` saved the request's cached `User`, without the lock | It starts with `OnboardingService.lock_account(user)` | A profile saved next to a role change answers with the current role and `next_step`, and a role change waits for it and is refused |
| Role page on web (#174) | In account mode the only visible exit was Keluar (log out); browser Back left the app | A Kembali that reuses `handleOnboardingStepPop`, extracted into `_backToProfile` | The account can go back to Lengkapi Profil without logging out, and `build` is back under SonarCloud's complexity limit (it was 17 of 15) |
| Void copy (#238) | The toast was a literal string, and the bulk dialog described the consequence in other words | `BatalkanSetoranDialog.berhasilMessage` and one shared sentence | Both flows tell the pengurus the same thing, and the next wording change is one edit |

## Design issues and the patterns that address them

| Code | Design issue | Pattern / principle | Type | Origin |
|---|---|---|---|---|
| [`validasi_uuid`](#a-boundary-validator-in-the-shared-kernel-5c2f7fc-b85819a) | **The same input rule written three times, two copies missing:** `nasabah_id` reached the ORM raw on two lists, so a typo was a 500 | **One boundary validator** in `shared_kernel`, next to `validasi_pencarian` | Principle (SRP, DRY, OCP) | **Scan finding** (ZAP, 9 Nov), filed as PIL-482 |
| [`test_counted_setoran_are_read_through_tercatat`](#a-rule-enforced-by-a-fitness-function-b10fffa-8d1a931) | **A domain rule copied as a raw filter** can drift from the named rule | **Query Object, enforced by an architecture fitness function** | Architectural (PoEAA; evolutionary architecture) | **Review defect** (Heraldo's re-review of #167 counted this path as using `tercatat()`) |
| [`JenisSampahSerializer.validate_kode`](#validate-first-then-query-e7ef617-887ecf4) | **Check and save on different values:** the uniqueness pre-check read the raw body, the save used the stripped value | **Validate first; the rule lives with the other field rules** | Principle (SRP, LSP) | Follow-up listed in Scallss's #172, plus the padded-kode bug I found while testing it |
| [`ForgetDeviceTokenSerializer`](#a-narrow-serializer-the-wider-one-extends-1a765f9) | **Two verbs validating one field two ways:** a hand-written check missed a character the database refuses | **A narrow serializer per request shape, the wider one inheriting it** | Principle (ISP, LSP) | #172 follow-up |
| [`complete_profile` lock](#a-fifth-writer-under-the-shared-lock-51a631e) | **A fifth writer of the role-lock invariant** acting on the request's cached `User` without the lock | **Pessimistic lock through the one `lock_account` entry point** the other writers share | Technique (concurrency); Principle (SRP, DIP) | **Review defect** ([Tristan P2, #137](https://github.com/bank-sampah-PILAH/pilah-be/pull/137#discussion_r4585330905)) |
| [`_backToProfile`](#a-reused-navigation-policy-and-extract-method-ef55977-a363412) | **A pushed page only the platform's back gesture could leave,** which web doesn't provide | **Reuse the onboarding step-pop policy**, then Extract Method | Principle (DRY, OCP); Refactoring | **Review defect** ([Tristan P2, #174](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/174#discussion_r4585330901)); the extract from a tool finding (S3776) |
| [`BatalkanSetoranDialog.berhasilMessage`](#one-home-for-each-message-77e612e) | **Copy drift:** one consequence worded three ways across the single dialog, the bulk dialog and the toast | **A named constant per message,** the same words in both flows | Principle (SRP, DRY) | **Review defect** ([Heraldo, #238](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/238#discussion_r4511111518)) |

## Backend

### A boundary validator in the shared kernel — [`5c2f7fc`](https://github.com/bank-sampah-PILAH/pilah-be/commit/5c2f7fc2), [`b85819a`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b85819ae)

```python title="shared_kernel/parameter.py"
"""Validasi parameter query berupa UUID (PIL-482).

Nilai mentah yang bukan UUID membuat ORM memunculkan ValidationError Django,
yang tidak ditangani DRF dan berakhir 500. Seperti `search`, `periode` dan
`tipe`, nilai yang tidak valid dijawab 422 dengan kunci parameternya.
"""

from uuid import UUID

from rest_framework import serializers


def validasi_uuid(nilai: str, *, kunci: str) -> UUID:
    try:
        hasil: UUID = serializers.UUIDField().run_validation(nilai)
    except serializers.ValidationError as exc:
        raise serializers.ValidationError({kunci: exc.detail}) from exc
    return hasil
```

```python title="apps/ledger/views.py"
qs = qs.filter(nasabah_id=validasi_uuid(nasabah_id, kunci="nasabah_id"))
```

The refactor after green moved `/aktivitas`, which had its own `try/except`, onto the same helper. All three lists now answer the same 422 for the same input, and a fourth list adds one call rather than another copy. The module sits beside `shared_kernel/pencarian.py`, which does the same job for `search`.

### A rule enforced by a fitness function — [`b10fffa`](https://github.com/bank-sampah-PILAH/pilah-be/commit/b10fffaa), [`8d1a931`](https://github.com/bank-sampah-PILAH/pilah-be/commit/8d1a9316)

Two weeks ago the counted-setoran rule was named once, as `TransaksiQuerySet.tercatat()`. A name only helps if every read uses it. Heraldo's re-review of #167 listed `waste_categories` among the `tercatat()` paths, although it spelled the filter out by hand. So the rule now has a test that reads the source:

```python title="tests/test_architecture.py"
TERCATAT_RULE_HOME = APPS_ROOT / "ledger" / "models.py"

def _spelled_out_tercatat_filters(path: Path) -> list[int]:
    lines: list[int] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"filter", "exclude"}
        ):
            continue
        for keyword in node.keywords:
            if _names_transaksi_tercatat(keyword.value) or (keyword.arg or "").endswith(
                "transaksi__status"
            ):
                lines.append(keyword.value.lineno)
    return lines
```

The fix uses the idiom `DashboardService.stats` already uses:

```python title="apps/reporting/services.py"
counted = Transaksi.objects.tercatat().filter(
    bank_sampah=bank,
    tipe=Transaksi.Tipe.SETORAN,
    tanggal__range=(start_dt, end_dt),
)
... DetailTransaksi.objects.filter(transaksi__in=counted) ...
```

Gabriel's review (17 Nov) pointed out that `counted` now repeats the selection `operational_trends` builds. That selection was already written twice before this PR, so extracting it is left for a separate change.

### Validate first, then query — [`e7ef617`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e7ef617b), [`887ecf4`](https://github.com/bank-sampah-PILAH/pilah-be/commit/887ecf45)

The jenis sampah viewset overrode `update` to check for a duplicate kode before validation, on `request.data`:

```python title="apps/waste_catalog/views.py (removed)"
def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    instance = self.get_object()
    nomor = request.data.get("kode")
    if (
        nomor
        and JenisSampah.objects.filter(bank_sampah=current_bank(request), nomor=nomor)
        .exclude(id=instance.id)
        .exists()
    ):
        return Response({"errors": {"kode": ["Kode sampah sudah digunakan"]}}, status=422)
    return super().update(request, *args, **kwargs)
```

A NUL byte reached PostgreSQL through that query (500). A padded `" HDPE "` passed it and was then stripped and saved over another item's kode. The rule now runs in the serializer, after DRF's field validators:

```python title="apps/waste_catalog/serializers.py"
def validate_kode(self, value: str) -> str:
    value = value.strip()
    # Edit: validator field DRF (termasuk penolak NUL) sudah berjalan, jadi
    # nilai ini aman dipakai untuk cek kode ganda di bank yang sama.
    jenis = self.instance
    if (
        value
        and isinstance(jenis, JenisSampah)
        and JenisSampah.objects.filter(bank_sampah_id=jenis.bank_sampah_id, nomor=value)
        .exclude(pk=jenis.pk)
        .exists()
    ):
        raise serializers.ValidationError("Kode sampah sudah digunakan")
    return value
```

With the override gone, the viewset is back to the inherited `update`, so `PUT` and `PATCH` follow the same rule. The nasabah edit keeps its check in the view, but now runs it after validation, on the validated kode, next to the view's own `no_hp` and email checks.

### A narrow serializer the wider one extends — [`1a765f9`](https://github.com/bank-sampah-PILAH/pilah-be/commit/1a765f94)

```python title="apps/notification/views.py"
class ForgetDeviceTokenSerializer(serializers.Serializer[Any]):
    # CharField brings DRF's NUL validator, so a crafted token is a 422 and
    # never reaches PostgreSQL.
    token = ...


class DeviceTokenSerializer(ForgetDeviceTokenSerializer):
    platform = ...
```

```python title="apps/notification/views.py"
data = ForgetDeviceTokenSerializer(data=request.data)
data.is_valid(raise_exception=True)
DeviceToken.objects.filter(
    user=current_user(request), token=data.validated_data["token"]
).delete()
```

`DELETE` asks for the token only. `POST` adds the platform. Both validate the token with the same field, where the hand-written check had missed the NUL byte.

### A fifth writer under the shared lock — [`51a631e`](https://github.com/bank-sampah-PILAH/pilah-be/commit/51a631ef)

```python title="apps/authentication/services.py"
# A completed profile commits the account to its role, so this takes
# the role-change lock too (PIL-451). The reload also means the
# checks below, and the role the caller answers with, are the
# account's current ones, not those of the object the request loaded.
OnboardingService.lock_account(user)
```

This is the fifth writer of "a completed profile or a linked membership locks the role". The other four already go through `lock_account`, so the lock policy stays in one method, and every writer depends on that method rather than on its own `select_for_update`.

## Mobile

### A reused navigation policy, and Extract Method — [`ef55977`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ef55977b), [`a363412`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a363412f)

```dart title="lib/features/authentication/presentation/pages/role_selection_page.dart"
secondary: account == null ? null : _backToProfile(isBusy),
...
/// Kembali for a signed-in account. Lengkapi Profil pushed this page, and on
/// web a push is not in the browser history, so the page offers the way
/// back itself: pop when the push is on the stack, else go to the profile.
Widget _backToProfile(bool isBusy) {
  return AppButton(
    label: 'Kembali',
    variant: AppButtonVariant.neutral,
    onPressed: isBusy
        ? null
        : () => handleOnboardingStepPop(
              context,
              didPop: false,
              isWizardStep: true,
            ),
  );
}
```

`handleOnboardingStepPop` is the policy the onboarding steps already use: pop when the push is on the stack, else go to the step's route. Reusing it, unchanged, means the role page behaves like every other step, on web too. The first version put the button inline in `build`, which pushed its cognitive complexity to 17 of 15 (SonarCloud S3776). The refactor extracted it the same evening.

### One home for each message — [`77e612e`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/77e612ec)

```dart title="lib/features/transaksi/presentation/widgets/batalkan_setoran_dialog.dart"
/// The success toast. It states what the backend now does: the setoran is
/// hidden from the riwayat (PIL-481), not kept there with a label.
static const berhasilMessage =
    'Setoran dihapus dan disembunyikan dari riwayat.';
```

The bulk dialog uses the same constant and the same consequence sentence ("Saldo nasabah dihitung ulang."). Its result panel now points at the setoran's detail, the one place that still shows the void.

## SOLID in this week's code

| Principle | Where | How |
|---|---|---|
| **Single responsibility** | `validasi_uuid`; `validate_kode`; `lock_account` | The helper only turns a raw parameter into a UUID or a keyed 422, and the views keep only their query. The serializer owns field rules, so the view no longer validates. The lock policy lives in one method. |
| **Open/closed** | `validasi_uuid`; `tercatat()`; `handleOnboardingStepPop` | A new list adds a call, not another `try/except`. A new counted status changes `tercatat()` only, and the fitness test makes sure nothing bypasses it. The step-pop policy is reused unchanged. |
| **Liskov substitution** | `DeviceTokenSerializer(ForgetDeviceTokenSerializer)`; the jenis sampah viewset | The wider serializer is the narrow one plus `platform`, so it validates a token exactly as `DELETE` does. With the `update` override gone, the viewset honours the inherited `ModelViewSet` contract again. |
| **Interface segregation** | `ForgetDeviceTokenSerializer` | `DELETE` asks only for the token, not for the platform it doesn't use. |
| **Dependency inversion** | Every writer of the role invariant → `OnboardingService.lock_account` | The writers depend on the one lock abstraction, not on a hand-written `select_for_update`. The race tests drive them through it. |

## Patterns, labelled as what they are

- **Query Object / Specification** (PoEAA): `tercatat()`. Its enforcement by a test is a **fitness function**, from evolutionary architecture, not a GoF pattern.
- **Pessimistic lock** (PoEAA, *Pessimistic Offline Lock*, here as a row lock inside a transaction): `lock_account`.
- **Plain inheritance** between DRF serializers: `DeviceTokenSerializer` extends the narrow one and adds a field. No design pattern is claimed for it.
- **Extract Method** (Fowler): `_backToProfile`.
