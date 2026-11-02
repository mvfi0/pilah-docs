"""PIL-428 (void a setoran): the real requests ZAP should attack.

Records two setoran for an active nasabah, voids one with an alasan, then
reads the list, the detail and the riwayat, so the active scan has real ids
and bodies for /transaksi/{id}/batalkan, the detail and the edit.
"""

from typing import Any, Callable

Call = Callable[..., tuple[int, Any]]


def _results(data: Any) -> list[dict[str, Any]]:
    return data["results"] if isinstance(data, dict) else data


def drive(call: Call, api: str) -> None:
    _, nasabah = call("GET", "/api/v1/nasabah?status=aktif")
    _, jenis = call("GET", "/api/v1/jenis-sampah")
    nasabah_id = _results(nasabah)[0]["id"]
    jenis_id = next(j["id"] for j in _results(jenis) if j.get("is_active", True))
    setoran = {"nasabah_id": nasabah_id, "items": [{"jenis_sampah_id": jenis_id, "berat": "2"}]}

    ids = []
    for _ in range(2):
        status, created = call("POST", "/api/v1/transaksi", setoran)
        if status in (200, 201):
            ids.append(created["id"])
    if not ids:
        raise SystemExit("could not record a setoran to scan")

    call("POST", f"/api/v1/transaksi/{ids[0]}/batalkan", {"alasan": "ZAP scan (PIL-428)"})
    call("POST", f"/api/v1/transaksi/{ids[0]}/batalkan", {"alasan": "again"})  # 409
    call("POST", f"/api/v1/transaksi/{ids[-1]}/batalkan", {"alasan": ""})  # 422
    call("GET", f"/api/v1/transaksi/{ids[0]}")
    call("PATCH", f"/api/v1/transaksi/{ids[0]}", {"alasan": "edit a void", "items": setoran["items"]})
    call("GET", "/api/v1/transaksi?periode=bulan_ini")
    call("GET", "/api/v1/aktivitas?periode=bulan_ini&tipe=semua")
