"""Scan one PILAH feature with a local OWASP ZAP daemon.

Run after a Linear sub-issue is finished, against *local* instances only: the
backend on the feature branch (scratch database plus seed data) and,
optionally, its web build. Never point it at shared staging or production.

    python tools/zap_scan.py --label PIL-428 --api http://127.0.0.1:8451 \
        --web http://127.0.0.1:8452 --drive tools/zap_drives/pil428.py \
        --scope /api/v1/transaksi/ --out docs/security/evidence

Steps:
1. Sign in as the seeded demo Pengurus and add a ZAP replacer rule, so every
   backend request ZAP sends carries the bearer token.
2. Import the OpenAPI schema, so every documented endpoint is known.
3. Run the feature's drive module: its real requests go through ZAP's proxy,
   so the active scan attacks real ids and bodies, not schema placeholders.
4. Spider the API and the web build, wait for the passive scan, then run an
   active scan limited to the feature's `--scope` paths.
5. Write HTML and JSON reports, then refuse to finish if either holds a
   bearer token or a JWT.

The ZAP daemon must already be running with its API on --zap, started with
`-daemon -host 127.0.0.1 -port 8090 -config api.disablekey=true`. In Git Bash
on Windows, prefix the command with MSYS_NO_PATHCONV=1, or --scope paths get
rewritten into Windows paths.
"""

from __future__ import annotations

import argparse
import http.client
import importlib.util
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any


def log(message: str) -> None:
    print(time.strftime("%H:%M:%S"), message, flush=True)


class Zap:
    def __init__(self, base: str) -> None:
        self.base = base.rstrip("/")
        parsed = urllib.parse.urlparse(self.base)
        self.host, self.port = parsed.hostname or "127.0.0.1", parsed.port or 8090

    def api(self, path: str, **params: object) -> dict[str, Any]:
        query = urllib.parse.urlencode({k: str(v) for k, v in params.items()})
        try:
            with urllib.request.urlopen(f"{self.base}{path}?{query}", timeout=600) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            raise SystemExit(f"ZAP {path} failed: {exc.code} {exc.read().decode(errors='ignore')}")

    def wait(self, path: str, scan_id: str, label: str) -> None:
        while True:
            status = int(self.api(path, scanId=scan_id)["status"])
            log(f"{label}: {status}%")
            if status >= 100:
                return
            time.sleep(20)

    def proxied(
        self, method: str, url: str, token: str, body: object | None = None
    ) -> tuple[int, Any]:
        """Send one request through ZAP's proxy (absolute-URI form), so it
        lands in ZAP's history; urllib may bypass a proxy for 127.0.0.1."""
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        payload = None
        if body is not None:
            payload = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        conn = http.client.HTTPConnection(self.host, self.port, timeout=120)
        conn.request(method, url, body=payload, headers=headers)
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        try:
            data: Any = json.loads(raw) if raw else None
        except ValueError:
            data = raw[:200]
        return response.status, data


def sign_in(api: str, id_token: str) -> str:
    request = urllib.request.Request(
        f"{api}/api/v1/auth/google",
        data=json.dumps({"id_token": id_token}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        return str(json.load(response)["access_token"])


def load_drive(path: str) -> Callable[..., None]:
    spec = importlib.util.spec_from_file_location("zap_drive", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load drive module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.drive  # type: ignore[no-any-return]


SECRET = re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--label", required=True, help="Linear issue, e.g. PIL-428")
    parser.add_argument("--api", required=True, help="local backend base URL")
    parser.add_argument("--web", action="append", default=[], help="local web build URL")
    parser.add_argument("--zap", default="http://127.0.0.1:8090")
    parser.add_argument("--drive", help="module with drive(call, api) sending the feature's requests")
    parser.add_argument("--scope", action="append", default=[], help="API path prefix to active-scan")
    parser.add_argument("--minutes", type=int, default=30, help="active scan time limit")
    parser.add_argument("--id-token", default="dev:pengurus.demo@example.com:Pengurus")
    parser.add_argument("--out", required=True, help="directory for the reports")
    args = parser.parse_args()

    for prefix in args.scope:
        # Git Bash rewrites a leading "/" into a Windows path; run it with
        # MSYS_NO_PATHCONV=1 there.
        if not prefix.startswith("/api/"):
            raise SystemExit(f"--scope must be an API path like /api/v1/x, got {prefix!r}")
    for url in [args.api, *args.web]:
        if urllib.parse.urlparse(url).hostname not in {"127.0.0.1", "localhost"}:
            raise SystemExit(f"refusing to scan a non-local target: {url}")

    zap = Zap(args.zap)
    api = args.api.rstrip("/")
    token = sign_in(api, args.id_token)
    log("signed in as the seeded demo Pengurus")

    # A rule from an earlier run would hold an old token, so replace it.
    try:
        urllib.request.urlopen(f"{zap.base}/JSON/replacer/action/removeRule/?description=pilah-bearer")
    except urllib.error.HTTPError:
        pass
    zap.api(
        "/JSON/replacer/action/addRule/",
        description="pilah-bearer",
        enabled="true",
        matchType="REQ_HEADER",
        matchRegex="false",
        matchString="Authorization",
        replacement=f"Bearer {token}",
        url=re.escape(api) + "/.*",
    )
    host = urllib.parse.urlparse(api).netloc
    zap.api("/JSON/openapi/action/importUrl/", url=f"{api}/api/schema/", hostOverride=host)
    log("bearer rule added; OpenAPI schema imported")

    if args.drive:
        def call(method: str, path: str, body: object | None = None) -> tuple[int, Any]:
            status, data = zap.proxied(method, f"{api}{path}", token, body)
            log(f"  drive {method} {path.split('?')[0]} -> {status}")
            return status, data

        load_drive(args.drive)(call, api)
        log("feature requests driven through the proxy")

    for target in [*args.web, f"{api}/api/"]:
        scan = zap.api("/JSON/spider/action/scan/", url=target, maxChildren=50)["scan"]
        zap.wait("/JSON/spider/view/status/", scan, f"spider {target}")
    while int(zap.api("/JSON/pscan/view/recordsToScan/")["recordsToScan"]) > 0:
        time.sleep(5)
    log("passive scan done")

    zap.api("/JSON/ascan/action/setOptionMaxScanDurationInMins/", Integer=args.minutes)
    zap.api("/JSON/ascan/action/setOptionMaxRuleDurationInMins/", Integer=5)
    zap.api("/JSON/ascan/action/setOptionThreadPerHost/", Integer=4)
    # A context limits the active scan to the feature's paths. Scanning a path
    # directly needs an exact node in ZAP's tree, which a URL only seen with
    # a query string doesn't have.
    context = zap.api("/JSON/context/action/newContext/", contextName=args.label)["contextId"]
    for prefix in args.scope or ["/"]:
        regex = re.escape(f"{api}{prefix}") + ".*"
        zap.api("/JSON/context/action/includeInContext/", contextName=args.label, regex=regex)
    # Each prefix node is scanned recursively, which covers its children
    # (ids, POST actions, PATCH) with their own methods. Query-string variants
    # are siblings of that node, not children, so each recorded one is
    # scanned on its own. ZAP can't look up an id path by URL, so those rely on
    # the recursion.
    def start_scan(url: str, recurse: bool, label: str, **extra: str) -> tuple[str, str] | None:
        params = {"url": url, "recurse": str(recurse).lower(), "contextId": context, **extra}
        try:
            query = urllib.parse.urlencode(params)
            with urllib.request.urlopen(f"{zap.base}/JSON/ascan/action/scan/?{query}") as response:
                return json.load(response)["scan"], label
        except urllib.error.HTTPError as exc:
            log(f"  skipped {label}: {exc.read().decode(errors='ignore')}")
            return None

    started: list[tuple[str, str]] = []
    for prefix in args.scope or ["/"]:
        scan = start_scan(f"{api}{prefix}", True, f"{prefix} (recursive)")
        if scan:
            started.append(scan)
        messages = zap.api(
            "/JSON/core/view/messages/", baseurl=f"{api}{prefix}", start=0, count=1000
        )["messages"]
        variants = {}
        for message in messages:
            method, url = message["requestHeader"].split(" ", 2)[:2]
            if url.startswith(f"{api}{prefix}?"):
                variants.setdefault((method, url), message.get("requestBody", ""))
        for (method, url), body in sorted(variants.items()):
            extra = {"method": method, **({"postData": body} if body else {})}
            scan = start_scan(url, False, f"{method} {url[len(api):]}", **extra)
            if scan:
                started.append(scan)
    log(f"active scan: {len(started)} scans started")
    for scan_id, label in started:
        zap.wait("/JSON/ascan/view/status/", scan_id, f"active scan {label}")

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stem = f"zap-{args.label.lower()}-{time.strftime('%Y-%m-%d')}"
    # ZAP's report API separates sites with "|"; ";" makes one site that
    # matches nothing and an empty report.
    sites = "|".join([api, *[w.rstrip("/") for w in args.web]])
    for template, suffix in (("traditional-html", "html"), ("traditional-json", "json")):
        zap.api(
            "/JSON/reports/action/generate/",
            title=f"PILAH local scan ({args.label})",
            template=template,
            reportDir=str(out),
            reportFileName=f"{stem}.{suffix}",
            sites=sites,
        )
    report = json.loads((out / f"{stem}.json").read_text(encoding="utf-8"))
    if not any(site.get("alerts") for site in report.get("site", [])):
        log("the JSON report has no alerts: check the sites filter before trusting it")
        return 1
    leaked = [p.name for p in out.glob(f"{stem}.*") if SECRET.search(p.read_text(errors="ignore"))]
    if leaked:
        log(f"token found in {leaked}: redact before publishing")
        return 1
    log(f"alerts: {zap.api('/JSON/alert/view/alertsSummary/')}")
    log(f"reports: {out / stem}.html and .json, checked for tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
