"""PIL-435 (Riwayat shows setoran only): the requests the screen makes.

The app now always sends tipe=setoran; the scan also sends the other values
so the active scan fuzzes the tipe, periode, search and page parameters of
the list and the XLSX export.
"""

from typing import Any, Callable

Call = Callable[..., tuple[int, Any]]


def drive(call: Call, api: str) -> None:
    for tipe in ("setoran", "semua", "pencairan"):
        call("GET", f"/api/v1/aktivitas?periode=bulan_ini&tipe={tipe}&page=1&page_size=20")
    call("GET", "/api/v1/aktivitas?periode=bulan_ini&tipe=setoran&search=Budi")
    call("GET", "/api/v1/aktivitas?periode=custom&tipe=setoran&dari_tanggal=2026-10-01&sampai_tanggal=2026-11-02")
    call("GET", "/api/v1/transaksi/export?periode=bulan_ini&tipe=setoran")
