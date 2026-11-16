"""Request-body NUL and padded kode (be PR after #172): the real requests.

Edits a jenis sampah and a nasabah (kode kept, then a NUL and a padded
duplicate kode, both 422), and registers then forgets a device token (a NUL
token is 422), so the active scan has real ids and bodies on every changed
write path.
"""

from typing import Any, Callable

Call = Callable[..., tuple[int, Any]]


def _results(data: Any) -> list[dict[str, Any]]:
    return data["results"] if isinstance(data, dict) else data


def _expect(status: int, wanted: int, what: str) -> None:
    if status != wanted:
        raise SystemExit(f"{what} answered {status}, expected {wanted}")


def drive(call: Call, api: str) -> None:
    _, jenis = call("GET", "/api/v1/jenis-sampah")
    pertama, kedua = _results(jenis)[:2]
    url = f"/api/v1/jenis-sampah/{pertama['id']}"
    _expect(call("PATCH", url, {"kode": pertama["kode"]})[0], 200, "jenis own kode")
    _expect(call("PATCH", url, {"kode": "A\x00B"})[0], 422, "jenis NUL kode")
    _expect(call("PATCH", url, {"kode": f" {kedua['kode']} "})[0], 422, "jenis padded kode")

    _, nasabah = call("GET", "/api/v1/nasabah?status=aktif")
    satu, dua = _results(nasabah)[:2]
    url = f"/api/v1/nasabah/{satu['id']}"
    _expect(call("PATCH", url, {"kode": satu["kode"]})[0], 200, "nasabah own kode")
    _expect(call("PATCH", url, {"kode": "A\x00B"})[0], 422, "nasabah NUL kode")
    _expect(call("PATCH", url, {"kode": f" {dua['kode']} "})[0], 422, "nasabah padded kode")

    token = {"token": "zap-scan-device-token", "platform": "web"}
    _expect(call("POST", "/api/v1/device-tokens/", token)[0], 200, "register token")
    _expect(call("DELETE", "/api/v1/device-tokens/", {"token": "a\x00b"})[0], 422, "NUL token")
    _expect(call("DELETE", "/api/v1/device-tokens/", {"token": token["token"]})[0], 204, "forget")
