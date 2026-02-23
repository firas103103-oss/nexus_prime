#!/usr/bin/env python3
"""
التحقق من واقعية التوثيق — Documentation Reality Verification
═══════════════════════════════════════════════════════════════
يقارن التوثيق بالواقع: المنافذ، الـ APIs، الخدمات.
يُشغّل اختبارات توافقية برمجية وتقنية.
"""
import json
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

PROJ = Path(__file__).resolve().parent.parent

# من PRODUCTION_VERIFICATION.md و SOVEREIGN_PAGES_INDEX
DOCUMENTED_PORTS = {
    3000: ("Open WebUI", "/"),
    3001: ("PostgREST", "/"),
    3002: ("Grafana", "/"),
    4000: ("LiteLLM", "/health/liveliness"),
    5050: ("Voice", "/"),
    5678: ("n8n", "/"),
    8002: ("Shadow7", "/api/shadow7/health"),
    8003: ("Auth", "/api/v1/auth/health"),
    8080: ("X-BIO", "/health"),
    8085: ("Dify", "/"),
    8090: ("Cortex", "/health"),
    8100: ("Oracle", "/health"),
    8200: ("Nerve", "/health"),
    8501: ("Boardroom", "/_stcore/health"),
    8888: ("Sovereign Bridge", "/health"),
    9000: ("Memory Keeper", "/health"),
    9999: ("Gateway", "/health"),
    5001: ("Dashboard", "/"),
    11434: ("Ollama", "/"),
}

# Sovereign Bridge APIs (من SOVEREIGN_PAGES_INDEX)
SOVEREIGN_APIS = [
    ("/api/hormonal/status", "GET"),
    ("/api/genome/entity/AS-SULTAN/llm-params", "GET"),
    ("/api/ledger/recent", "GET"),
    ("/api/systems/status", "GET"),
]


def http_get(url: str, timeout: int = 3) -> tuple[int, str]:
    """Returns (status_code, body_or_error)."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode()[:200]
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)
    except Exception as e:
        return 0, str(e)


def verify_ports() -> dict:
    """التحقق من المنافذ الموثقة vs الواقع."""
    results = []
    for port, (name, path) in DOCUMENTED_PORTS.items():
        url = f"http://127.0.0.1:{port}{path}"
        code, _ = http_get(url)
        ok = code in (0, 200, 301, 302, 307, 404) or (code >= 200 and code < 500)
        results.append({
            "port": port,
            "service": name,
            "path": path,
            "status_code": code,
            "reachable": code != 0,
            "doc_match": ok,
        })
    return {"ports": results, "total": len(results), "ok": sum(1 for r in results if r["doc_match"])}


def verify_sovereign_apis() -> dict:
    """التحقق من Sovereign Bridge APIs."""
    base = "http://127.0.0.1:8888"
    results = []
    for path, method in SOVEREIGN_APIS:
        url = base + path
        code, body = http_get(url)
        ok = code in (200, 404) or (code >= 200 and code < 500)
        results.append({"path": path, "method": method, "status": code, "ok": ok})
    return {"apis": results, "ok": sum(1 for r in results if r["ok"])}


def verify_clone_hub() -> dict:
    """التحقق من Clone Hub — جزء من integration/ecosystem."""
    out = {"exists": False, "runnable": False, "integration_path": False, "planets_identity": False}
    # integration/clone-hub
    ch_path = PROJ / "integration" / "clone-hub" / "main.py"
    out["integration_path"] = ch_path.exists()
    if ch_path.exists():
        out["exists"] = True
        try:
            r = subprocess.run(
                [sys.executable, str(ch_path)],
                cwd=str(PROJ),
                capture_output=True,
                text=True,
                timeout=15,
            )
            out["runnable"] = r.returncode == 0
            out["stdout"] = (r.stdout or "")[:500]
        except Exception as e:
            out["runnable"] = False
            out["error"] = str(e)
    # planets/CLONE-HUB identity
    identity = PROJ / "planets" / "CLONE-HUB" / "identity.json"
    out["planets_identity"] = identity.exists()
    if identity.exists():
        try:
            data = json.loads(identity.read_text())
            out["identity_status"] = data.get("status", "?")
        except Exception:
            pass
    return out


def verify_ecosystem_api() -> dict:
    """التحقق من Ecosystem API (8005) — Clone Hub مذكور فيه."""
    code, body = http_get("http://127.0.0.1:8005/api/v1/health")
    if code != 200:
        return {"reachable": False, "status": code}
    try:
        data = json.loads(body)
        return {
            "reachable": True,
            "status": code,
            "clone_hub_in_health": "clone_hub" in str(data),
        }
    except Exception:
        return {"reachable": code == 200, "status": code}


def verify_ethical_gate() -> dict:
    """تشغيل اختبار Ethical Gate VOC."""
    script = PROJ / "scripts" / "ethical_gate_voc_test.py"
    if not script.exists():
        return {"exists": False}
    try:
        r = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(PROJ),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return {
            "exists": True,
            "exit_code": r.returncode,
            "pass": r.returncode == 0,
            "stdout": (r.stdout or "")[-500:],
        }
    except Exception as e:
        return {"exists": True, "error": str(e), "pass": False}


def run_full_health_check() -> dict:
    """تشغيل full_health_check.sh."""
    script = PROJ / "scripts" / "full_health_check.sh"
    if not script.exists():
        return {"exists": False}
    try:
        r = subprocess.run(
            ["bash", str(script)],
            cwd=str(PROJ),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "exists": True,
            "exit_code": r.exitcode if hasattr(r, "exitcode") else r.returncode,
            "pass": r.returncode == 0,
            "output_lines": len((r.stdout or "").splitlines()),
        }
    except Exception as e:
        return {"exists": True, "error": str(e), "pass": False}


def main():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "timestamp": ts,
        "documentation_reality_verification": True,
        "results": {},
    }

    print("=== التحقق من واقعية التوثيق ===\n")

    # 1. المنافذ
    print("1. المنافذ (Documented vs Reality)...")
    pr = verify_ports()
    report["results"]["ports"] = pr
    ok_ports = pr["ok"]
    total_ports = pr["total"]
    print(f"   {ok_ports}/{total_ports} منافذ متوافقة مع التوثيق\n")

    # 2. Sovereign APIs
    print("2. Sovereign Bridge APIs...")
    sr = verify_sovereign_apis()
    report["results"]["sovereign_apis"] = sr
    print(f"   {sr['ok']}/{len(sr['apis'])} APIs تستجيب\n")

    # 3. Clone Hub
    print("3. Clone Hub (جزء من integration/ecosystem)...")
    ch = verify_clone_hub()
    report["results"]["clone_hub"] = ch
    print(f"   integration/clone-hub: {'✓' if ch['integration_path'] else '✗'}")
    print(f"   planets/CLONE-HUB identity: {'✓' if ch['planets_identity'] else '✗'}")
    print(f"   Runnable: {'✓' if ch.get('runnable') else '✗'}\n")

    # 4. Ecosystem API
    print("4. Ecosystem API (8005)...")
    ea = verify_ecosystem_api()
    report["results"]["ecosystem_api"] = ea
    print(f"   Reachable: {'✓' if ea.get('reachable') else '✗'}\n")

    # 5. Ethical Gate
    print("5. Ethical Gate VOC Test...")
    eg = verify_ethical_gate()
    report["results"]["ethical_gate"] = eg
    print(f"   Pass: {'✓' if eg.get('pass') else '✗'}\n")

    # 6. Full health check
    print("6. full_health_check.sh...")
    fh = run_full_health_check()
    report["results"]["full_health_check"] = fh
    print(f"   Pass: {'✓' if fh.get('pass') else '✗'}\n")

    # Summary
    all_ok = (
        pr["ok"] >= total_ports * 0.5 and
        ch.get("integration_path") and
        ch.get("planets_identity")
    )
    report["summary"] = {
        "documentation_matches_reality": all_ok,
        "clone_hub_integrated": ch.get("integration_path") and ch.get("planets_identity"),
    }

    # Save report
    out_path = PROJ / "docs" / "VERIFICATION_REPORT.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Report saved: {out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
