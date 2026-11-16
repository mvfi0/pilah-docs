"""waste_categories reads through tercatat() (be PR after #167): the real requests.

Records two setoran for an active nasabah, voids one, then reads the dashboard
waste categories (the changed query) for today and for the month, plus the
dashboard stats and trends that share the tercatat() rule, so the active scan
has real dates and a voided row behind the aggregate.
"""

from datetime import date
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
    call("POST", f"/api/v1/transaksi/{ids[0]}/batalkan", {"alasan": "ZAP scan (tercatat)"})

    today = date.today()
    month_start = today.replace(day=1).isoformat()
    call("GET", f"/api/v1/dashboard/waste-categories?start_date={today}&end_date={today}")
    call("GET", f"/api/v1/dashboard/waste-categories?start_date={month_start}&end_date={today}")
    call(
        "GET",
        "/api/v1/dashboard/operational-trends"
        f"?start_date={month_start}&end_date={today}&granularity=day",
    )
    call("GET", "/api/v1/dashboard/stats")
