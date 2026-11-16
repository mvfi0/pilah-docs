"""PIL-482 (a malformed nasabah_id gives 422, not 500): the real requests.

Reads the three ledger lists that take a nasabah_id filter, once with a real
member id and once with a malformed one, so the active scan has both the
valid and the rejected shape of the parameter to attack.
"""

from typing import Any, Callable

Call = Callable[..., tuple[int, Any]]


def _results(data: Any) -> list[dict[str, Any]]:
    return data["results"] if isinstance(data, dict) else data


def drive(call: Call, api: str) -> None:
    _, nasabah = call("GET", "/api/v1/nasabah?status=aktif")
    nasabah_id = _results(nasabah)[0]["id"]
    for path in ("/api/v1/transaksi", "/api/v1/pencairan", "/api/v1/aktivitas"):
        status, _ = call("GET", f"{path}?periode=semua&nasabah_id={nasabah_id}")
        if status != 200:
            raise SystemExit(f"{path} with a real nasabah_id answered {status}")
        status, _ = call("GET", f"{path}?periode=semua&nasabah_id=abc")
        if status != 422:
            raise SystemExit(f"{path} with nasabah_id=abc answered {status}, expected 422")
