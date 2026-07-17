#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "qa" / "launch-readiness"
STRICT = os.environ.get("AUDIT_STRICT") == "1"
PAGES_ORIGIN = "https://proaiexpert.github.io/alina-horb-website"
APEX_ORIGIN = "https://alinahorb.com"
WWW_ORIGIN = "https://www.alinahorb.com"
ROUTES = [
    "/", "/ru/", "/about/", "/ru/about/", "/consultations/", "/ru/consultations/",
    "/notes/", "/ru/notes/", "/notes/first-consultation/", "/ru/notes/first-consultation/",
    "/notes/how-to-start-the-conversation/", "/ru/notes/how-to-start-the-conversation/",
    "/notes/when-coping-stops-helping/", "/ru/notes/when-coping-stops-helping/",
    "/notes/stress-relocation-and-lost-support/", "/ru/notes/stress-relocation-and-lost-support/",
    "/privacy/", "/ru/privacy/",
]


def fetch_json(url: str, timeout: int = 20) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "AlinaHorbLaunchAudit/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def dns(name: str, record_type: str) -> dict:
    url = f"https://dns.google/resolve?name={name}&type={record_type}"
    try:
        payload = fetch_json(url)
        return {
            "status": payload.get("Status"),
            "answers": [item.get("data") for item in payload.get("Answer", [])],
            "authority": [item.get("data") for item in payload.get("Authority", [])],
        }
    except Exception as error:  # noqa: BLE001
        return {"error": str(error), "answers": []}


def http_probe(url: str, timeout: int = 25) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "AlinaHorbLaunchAudit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(512_000).decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type"),
                "has_expected_name": "Аліна Горб" in body or "Алина Горб" in body,
                "bytes_read": len(body.encode("utf-8")),
            }
    except urllib.error.HTTPError as error:
        return {"ok": False, "status": error.code, "final_url": error.geturl(), "error": str(error)}
    except Exception as error:  # noqa: BLE001
        return {"ok": False, "status": None, "final_url": None, "error": str(error)}


def tls_probe(hostname: str) -> dict:
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=15) as connection:
            with context.wrap_socket(connection, server_hostname=hostname) as secure:
                certificate = secure.getpeercert()
        return {
            "ok": True,
            "issuer": dict(item[0] for item in certificate.get("issuer", [])),
            "subject": dict(item[0] for item in certificate.get("subject", [])),
            "not_before": certificate.get("notBefore"),
            "not_after": certificate.get("notAfter"),
            "subject_alt_names": [value for kind, value in certificate.get("subjectAltName", []) if kind == "DNS"],
        }
    except Exception as error:  # noqa: BLE001
        return {"ok": False, "error": str(error)}


def main() -> int:
    report: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "proaiexpert/alina-horb-website",
        "pages_origin": PAGES_ORIGIN,
        "custom_domain": "alinahorb.com",
        "cname_file": (ROOT / "CNAME").read_text(encoding="utf-8").strip() if (ROOT / "CNAME").is_file() else None,
        "dns": {
            "apex_A": dns("alinahorb.com", "A"),
            "apex_AAAA": dns("alinahorb.com", "AAAA"),
            "apex_NS": dns("alinahorb.com", "NS"),
            "www_CNAME": dns("www.alinahorb.com", "CNAME"),
            "www_A": dns("www.alinahorb.com", "A"),
        },
        "rdap": None,
        "http": {"github_pages": {}, "apex": {}, "www": {}},
        "tls": {},
        "critical": [],
        "warnings": [],
    }

    try:
        rdap = fetch_json("https://rdap.verisign.com/com/v1/domain/alinahorb.com")
        report["rdap"] = {
            "registered": True,
            "ldh_name": rdap.get("ldhName"),
            "status": rdap.get("status", []),
            "nameservers": [item.get("ldhName") for item in rdap.get("nameservers", [])],
            "events": rdap.get("events", []),
        }
    except urllib.error.HTTPError as error:
        report["rdap"] = {"registered": error.code != 404, "http_status": error.code, "error": str(error)}
    except Exception as error:  # noqa: BLE001
        report["rdap"] = {"registered": None, "error": str(error)}

    for route in ROUTES:
        report["http"]["github_pages"][route] = http_probe(f"{PAGES_ORIGIN}{route}")

    for key, origin in (("apex", APEX_ORIGIN), ("www", WWW_ORIGIN)):
        for route in ("/", "/ru/", "/consultations/#contact", "/notes/"):
            report["http"][key][route] = http_probe(f"{origin}{route}")

    report["tls"]["apex"] = tls_probe("alinahorb.com")
    report["tls"]["www"] = tls_probe("www.alinahorb.com")

    failed_pages = [route for route, result in report["http"]["github_pages"].items() if not result.get("ok")]
    if failed_pages:
        report["critical"].append(f"GitHub Pages routes failed: {', '.join(failed_pages)}")

    if not report["dns"]["apex_A"].get("answers"):
        report["critical"].append("alinahorb.com has no public A records")
    if not report["dns"]["www_CNAME"].get("answers") and not report["dns"]["www_A"].get("answers"):
        report["critical"].append("www.alinahorb.com has no public CNAME/A record")
    if report["cname_file"] != "alinahorb.com":
        report["warnings"].append("Repository CNAME is not configured for alinahorb.com")
    if not report["tls"]["apex"].get("ok"):
        report["critical"].append("HTTPS certificate is not available for alinahorb.com")
    if not report["tls"]["www"].get("ok"):
        report["critical"].append("HTTPS certificate is not available for www.alinahorb.com")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "Alina Horb launch readiness V1",
        f"Generated: {report['generated_at']}",
        f"GitHub Pages routes: {len(ROUTES) - len(failed_pages)}/{len(ROUTES)} reachable",
        f"CNAME file: {report['cname_file'] or 'missing'}",
        f"Apex A: {', '.join(report['dns']['apex_A'].get('answers', [])) or 'missing'}",
        f"WWW CNAME: {', '.join(report['dns']['www_CNAME'].get('answers', [])) or 'missing'}",
        f"Apex TLS: {'ok' if report['tls']['apex'].get('ok') else 'unavailable'}",
        f"WWW TLS: {'ok' if report['tls']['www'].get('ok') else 'unavailable'}",
        "",
        "Critical:",
        *([f"- {item}" for item in report["critical"]] or ["- none"]),
        "",
        "Warnings:",
        *([f"- {item}" for item in report["warnings"]] or ["- none"]),
    ]
    (OUTPUT / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    return 1 if STRICT and report["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
