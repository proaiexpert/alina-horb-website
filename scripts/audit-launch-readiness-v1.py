#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
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
PUBLIC_ROBOTS = "index, follow, max-image-preview:large"
EXPECTED_APEX_IPS = {
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
}
ROUTES = [
    "/", "/ru/", "/about/", "/ru/about/", "/consultations/", "/ru/consultations/",
    "/notes/", "/ru/notes/", "/notes/first-consultation/", "/ru/notes/first-consultation/",
    "/notes/how-to-start-the-conversation/", "/ru/notes/how-to-start-the-conversation/",
    "/notes/when-coping-stops-helping/", "/ru/notes/when-coping-stops-helping/",
    "/notes/stress-relocation-and-lost-support/", "/ru/notes/stress-relocation-and-lost-support/",
    "/privacy/", "/ru/privacy/",
]


def fetch_text(url: str, timeout: int = 25) -> tuple[dict, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "AlinaHorbLaunchAudit/1.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(1_500_000).decode("utf-8", errors="replace")
            return ({
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type"),
                "bytes_read": len(body.encode("utf-8")),
            }, body)
    except urllib.error.HTTPError as error:
        return ({"ok": False, "status": error.code, "final_url": error.geturl(), "error": str(error)}, "")
    except Exception as error:  # noqa: BLE001
        return ({"ok": False, "status": None, "final_url": None, "error": str(error)}, "")


def fetch_json(url: str, timeout: int = 20) -> dict:
    meta, body = fetch_text(url, timeout)
    if not meta.get("ok"):
        raise RuntimeError(meta.get("error") or f"HTTP {meta.get('status')}")
    return json.loads(body)


def dns(name: str, record_type: str) -> dict:
    try:
        payload = fetch_json(f"https://dns.google/resolve?name={name}&type={record_type}")
        return {
            "status": payload.get("Status"),
            "answers": [item.get("data") for item in payload.get("Answer", [])],
            "authority": [item.get("data") for item in payload.get("Authority", [])],
        }
    except Exception as error:  # noqa: BLE001
        return {"error": str(error), "answers": []}


def first_match(pattern: str, body: str) -> str | None:
    match = re.search(pattern, body, flags=re.I | re.S)
    return match.group(1).strip() if match else None


def html_probe(url: str) -> dict:
    meta, body = fetch_text(url)
    meta.update({
        "has_expected_name": "Аліна Горб" in body or "Алина Горб" in body,
        "robots": first_match(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', body),
        "canonical": first_match(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', body),
        "hreflang_uk": first_match(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']uk["\']\s+href=["\']([^"\']+)["\']', body),
        "hreflang_ru": first_match(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']ru["\']\s+href=["\']([^"\']+)["\']', body),
        "has_global_chrome": "site.global-chrome.v1.css?v=20260717-ux1" in body,
        "has_navigation_v1": "site.navigation.v1.js?v=20260717-ux1" in body,
        "stable_font_policy": "&display=optional" in body and "&display=swap" not in body,
    })
    return meta


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


def canonical_for(route: str) -> str:
    return f"{APEX_ORIGIN}{route}"


def expected_hreflang(route: str) -> tuple[str, str]:
    clean = route.removeprefix("/ru")
    if not clean:
        clean = "/"
    return f"{APEX_ORIGIN}{clean}", f"{APEX_ORIGIN}/ru{clean}"


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
        "live_assets": {},
        "live_robots": {},
        "live_sitemap": {},
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
    except Exception as error:  # noqa: BLE001
        report["rdap"] = {"registered": None, "error": str(error)}

    for route in ROUTES:
        report["http"]["github_pages"][route] = html_probe(f"{PAGES_ORIGIN}{route}")
        report["http"]["apex"][route] = html_probe(f"{APEX_ORIGIN}{route}")

    for route in ("/", "/ru/", "/consultations/", "/notes/"):
        report["http"]["www"][route] = html_probe(f"{WWW_ORIGIN}{route}")

    config_meta, config_body = fetch_text(f"{APEX_ORIGIN}/assets/js/site-config.v2.js")
    runtime_meta, runtime_body = fetch_text(f"{APEX_ORIGIN}/assets/js/site.v2.js")
    report["live_assets"] = {
        "config": {**config_meta, "formspree": "https://formspree.io/f/mvzezana" in config_body, "public_email": "hello@alinahorb.com" in config_body},
        "runtime": {**runtime_meta, "turnstile": "turnstile" in runtime_body.lower(), "site_key": "0x4AAAAAAD2wlldaSXK8Bp9f" in runtime_body},
    }

    robots_meta, robots_body = fetch_text(f"{APEX_ORIGIN}/robots.txt")
    report["live_robots"] = {
        **robots_meta,
        "allows_all": "User-agent: *" in robots_body and "Allow: /" in robots_body and "Disallow:" not in robots_body,
        "sitemap": f"Sitemap: {APEX_ORIGIN}/sitemap.xml" in robots_body,
    }

    sitemap_meta, sitemap_body = fetch_text(f"{APEX_ORIGIN}/sitemap.xml")
    sitemap_locations = re.findall(r"<loc>([^<]+)</loc>", sitemap_body)
    report["live_sitemap"] = {
        **sitemap_meta,
        "locations": sitemap_locations,
        "expected": [canonical_for(route) for route in ROUTES],
    }

    report["tls"]["apex"] = tls_probe("alinahorb.com")
    report["tls"]["www"] = tls_probe("www.alinahorb.com")

    apex_answers = {value.rstrip(".") for value in report["dns"]["apex_A"].get("answers", [])}
    if apex_answers != EXPECTED_APEX_IPS:
        report["critical"].append(f"alinahorb.com A records mismatch: {sorted(apex_answers)}")

    www_cnames = {value.rstrip(".") for value in report["dns"]["www_CNAME"].get("answers", [])}
    if "proaiexpert.github.io" not in www_cnames:
        report["critical"].append(f"www.alinahorb.com CNAME mismatch: {sorted(www_cnames)}")

    if not report["rdap"].get("registered"):
        report["critical"].append("alinahorb.com registration could not be verified")

    for route in ROUTES:
        pages = report["http"]["github_pages"][route]
        apex = report["http"]["apex"][route]
        expected = canonical_for(route)
        uk_url, ru_url = expected_hreflang(route)
        if not pages.get("ok") or pages.get("final_url") != expected:
            report["critical"].append(f"GitHub Pages redirect failed for {route}: {pages.get('final_url')}")
        if not apex.get("ok"):
            report["critical"].append(f"Live route failed: {route}")
            continue
        if apex.get("robots") != PUBLIC_ROBOTS:
            report["critical"].append(f"{route}: live robots meta is {apex.get('robots')!r}")
        if apex.get("canonical") != expected:
            report["critical"].append(f"{route}: canonical mismatch {apex.get('canonical')!r}")
        if apex.get("hreflang_uk") != uk_url or apex.get("hreflang_ru") != ru_url:
            report["critical"].append(f"{route}: hreflang mismatch")
        if not apex.get("has_global_chrome") or not apex.get("has_navigation_v1"):
            report["critical"].append(f"{route}: current production chrome assets missing")
        if not apex.get("stable_font_policy"):
            report["critical"].append(f"{route}: unstable font loading policy")

    for route, result in report["http"]["www"].items():
        if not result.get("ok") or result.get("final_url") != canonical_for(route):
            report["critical"].append(f"www redirect failed for {route}: {result.get('final_url')}")

    if not report["live_assets"]["config"].get("ok") or not report["live_assets"]["config"].get("formspree") or not report["live_assets"]["config"].get("public_email"):
        report["critical"].append("Production form configuration is missing or stale")
    if not report["live_assets"]["runtime"].get("ok") or not report["live_assets"]["runtime"].get("turnstile") or not report["live_assets"]["runtime"].get("site_key"):
        report["critical"].append("Production Turnstile runtime is missing or stale")
    if not report["live_robots"].get("ok") or not report["live_robots"].get("allows_all") or not report["live_robots"].get("sitemap"):
        report["critical"].append("Live robots.txt is invalid")
    if report["live_sitemap"].get("locations") != report["live_sitemap"].get("expected"):
        report["critical"].append("Live sitemap route/order mismatch")

    for hostname in ("apex", "www"):
        tls = report["tls"][hostname]
        sans = set(tls.get("subject_alt_names", []))
        if not tls.get("ok") or not {"alinahorb.com", "www.alinahorb.com"}.issubset(sans):
            report["critical"].append(f"HTTPS certificate invalid for {hostname}")

    pages_redirect_active = all(item.get("final_url", "").startswith(APEX_ORIGIN) for item in report["http"]["github_pages"].values())
    if not report["cname_file"] and pages_redirect_active:
        report["warnings"].append("Repository CNAME file is intentionally absent; GitHub Pages custom-domain setting is active and verified externally")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "Alina Horb launch readiness V1",
        f"Generated: {report['generated_at']}",
        f"Live routes: {sum(1 for item in report['http']['apex'].values() if item.get('ok'))}/{len(ROUTES)} reachable",
        f"GitHub Pages redirects: {sum(1 for item in report['http']['github_pages'].values() if item.get('final_url', '').startswith(APEX_ORIGIN))}/{len(ROUTES)}",
        f"Public indexing: {sum(1 for item in report['http']['apex'].values() if item.get('robots') == PUBLIC_ROBOTS)}/{len(ROUTES)}",
        f"Apex DNS: {'ok' if apex_answers == EXPECTED_APEX_IPS else 'mismatch'}",
        f"WWW DNS: {'ok' if 'proaiexpert.github.io' in www_cnames else 'mismatch'}",
        f"Apex TLS: {'ok' if report['tls']['apex'].get('ok') else 'unavailable'}",
        f"WWW TLS: {'ok' if report['tls']['www'].get('ok') else 'unavailable'}",
        f"Formspree config: {'ok' if report['live_assets']['config'].get('formspree') else 'missing'}",
        f"Turnstile runtime: {'ok' if report['live_assets']['runtime'].get('turnstile') and report['live_assets']['runtime'].get('site_key') else 'missing'}",
        "",
        "Critical:",
        *([f"- {item}" for item in report["critical"]] or ["- none"]),
        "",
        "Notes:",
        *([f"- {item}" for item in report["warnings"]] or ["- none"]),
    ]
    (OUTPUT / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    return 1 if STRICT and report["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
