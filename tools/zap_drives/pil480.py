"""PIL-480 (the riwayat export has no ID Aktivitas column): the requests the app makes.

The export is one endpoint, so the scan sends it with every period, type and
member filter the screen can set, plus the riwayat list it is built from. The
active scan then fuzzes those parameters and the response headers of the file.
"""

from typing import Any, Callable

Call = Callable[..., tuple[int, Any]]


def _results(data: Any) -> list[dict[str, Any]]:
    return data["results"] if isinstance(data, dict) else data


def drive(call: Call, api: str) -> None:
    _, nasabah = call("GET", "/api/v1/nasabah?status=aktif")
    nasabah_id = _results(nasabah)[0]["id"]
    for periode in ("bulan_ini", "bulan_lalu", "3_bulan", "semua"):
        call("GET", f"/api/v1/transaksi/export?periode={periode}")
    for tipe in ("semua", "setoran", "pencairan"):
        call("GET", f"/api/v1/transaksi/export?periode=semua&tipe={tipe}")
    call("GET", f"/api/v1/transaksi/export?periode=semua&nasabah_id={nasabah_id}")
    call("GET", "/api/v1/transaksi/export?periode=semua&search=Budi")
    call(
        "GET",
        "/api/v1/transaksi/export?periode=custom&dari_tanggal=2026-10-01&sampai_tanggal=2026-11-09",
    )
    call("GET", "/api/v1/transaksi/export?periode=tidak_ada")  # 400
    call("GET", "/api/v1/aktivitas?periode=semua&tipe=semua")
