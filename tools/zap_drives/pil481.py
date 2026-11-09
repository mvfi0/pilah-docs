"""PIL-481 (a voided setoran is hidden from the riwayat lists): the real requests.

Records two setoran for an active nasabah and voids one, then reads every list
that now leaves the void out (/transaksi, /aktivitas, the dashboard's recent
transactions) and the detail of both the voided and the kept setoran, so the
active scan has real ids, filters and a voided row to attack.
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
    if len(ids) < 2:
        raise SystemExit("could not record two setoran to scan")

    call("POST", f"/api/v1/transaksi/{ids[0]}/batalkan", {"alasan": "ZAP scan (PIL-481)"})
    call("GET", f"/api/v1/transaksi/{ids[0]}")  # the void is still reachable by id
    call("GET", f"/api/v1/transaksi/{ids[1]}")
    call("GET", "/api/v1/transaksi?periode=bulan_ini")
    call("GET", f"/api/v1/transaksi?periode=semua&nasabah_id={nasabah_id}")
    call("GET", "/api/v1/transaksi?periode=semua&search=Budi")
    call("GET", "/api/v1/aktivitas?periode=bulan_ini&tipe=semua")
    call("GET", "/api/v1/aktivitas?periode=semua&tipe=setoran&page=1&page_size=20")
    call("GET", f"/api/v1/aktivitas?periode=semua&nasabah_id={nasabah_id}")
    call("GET", "/api/v1/dashboard/recent-transactions")
