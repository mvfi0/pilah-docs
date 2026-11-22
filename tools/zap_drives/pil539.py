"""PIL-539 (a nasabah applies to a second bank sampah): the real requests.

Signed in as the seeded demo nasabah, who is approved at the seed bank. Reads
its memberships and the bank directory, applies to a second active bank (201,
pending), then repeats the application (400), applies to its own bank again
(400) and sends a malformed bank id. Finally checks that the pending
membership cannot open its saldo yet (403). So the active scan has a real
application body, a real membership id and the directory to attack.
"""

from typing import Any, Callable

Call = Callable[..., tuple[int, Any]]

SECOND_BANK = "Bank Sampah ZAP Kedua"


def _expect(status: int, wanted: tuple[int, ...], what: str) -> None:
    if status not in wanted:
        raise SystemExit(f"{what} answered {status}, expected {wanted}")


def drive(call: Call, api: str) -> None:
    status, memberships = call("GET", "/api/v1/nasabah/me")
    _expect(status, (200,), "own memberships")
    first_bank = memberships[0]["bank_sampah"]["id"] if isinstance(
        memberships[0].get("bank_sampah"), dict
    ) else memberships[0]["bank_sampah_id"]

    status, directory = call("GET", "/api/v1/bank-sampah")
    _expect(status, (200,), "bank directory")
    second = next(bank for bank in directory if bank["nama"] == SECOND_BANK)

    body = {"bank_sampah_id": second["id"]}
    _expect(call("POST", "/api/v1/onboarding/nasabah", body)[0], (201,), "apply to second bank")
    _expect(call("POST", "/api/v1/onboarding/nasabah", body)[0], (400,), "apply twice")
    _expect(
        call("POST", "/api/v1/onboarding/nasabah", {"bank_sampah_id": first_bank})[0],
        (400,),
        "apply to own bank",
    )
    _expect(
        call("POST", "/api/v1/onboarding/nasabah", {"bank_sampah_id": "bukan-uuid"})[0],
        (400, 422),
        "malformed bank id",
    )

    status, memberships = call("GET", "/api/v1/nasabah/me")
    _expect(status, (200,), "own memberships after applying")
    pending = next(row for row in memberships if row["status"] == "pending")
    _expect(
        call("GET", f"/api/v1/nasabah/me/saldo?keanggotaan_id={pending['id']}")[0],
        (403,),
        "pending membership saldo",
    )
