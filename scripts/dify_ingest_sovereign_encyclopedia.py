#!/usr/bin/env python3
"""
Ingest Sovereign Encyclopedia into Dify Knowledge Base.
Requires DIFY_CONSOLE_API_KEY from Dify Settings → API Keys.
Run: DIFY_CONSOLE_API_KEY=xxx python scripts/dify_ingest_sovereign_encyclopedia.py
"""
import os
import sys
import json
from pathlib import Path

DIFY_BASE = os.getenv("DIFY_BASE", "https://dify.mrf103.com")
API_KEY = os.getenv("DIFY_CONSOLE_API_KEY", "")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENCYCLOPEDIA_PATH = PROJECT_ROOT / "docs" / "SOVEREIGN_ENCYCLOPEDIA.md"
CODEX_PATH = PROJECT_ROOT / "ENTERPRISE_CODEX.yaml"


def main():
    if not API_KEY:
        print("=" * 60)
        print("DIFY SOVEREIGN ENCYCLOPEDIA INGESTION")
        print("=" * 60)
        print("\nNo DIFY_CONSOLE_API_KEY set. Manual steps:\n")
        print("1. Log in: https://dify.mrf103.com")
        print("2. Settings → API Keys → Create API Key")
        print("3. Knowledge → Create Knowledge Base")
        print("4. Name: Sovereign Encyclopedia")
        print("5. Upload:", ENCYCLOPEDIA_PATH)
        print("6. In Chat/Workflow apps, add Knowledge Retrieval node\n")
        print("To automate: DIFY_CONSOLE_API_KEY=your_key python", sys.argv[0])
        return 1

    import httpx

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # Create dataset
    print("Creating dataset 'Sovereign Encyclopedia'...")
    r = httpx.post(
        f"{DIFY_BASE}/console/api/datasets",
        headers=headers,
        json={"name": "Sovereign Encyclopedia", "indexing_technique": "high_quality"},
        timeout=30,
    )
    if r.status_code not in (200, 201):
        print(f"Error: {r.status_code} {r.text[:300]}")
        return 1
    ds = r.json()
    dataset_id = ds.get("id")
    if not dataset_id:
        print("No dataset id in response:", ds)
        return 1
    print(f"  Created dataset: {dataset_id}")

    # Upload document (Dify expects multipart/form-data with file)
    if not ENCYCLOPEDIA_PATH.exists():
        print(f"File not found: {ENCYCLOPEDIA_PATH}")
        return 1
    print(f"Uploading {ENCYCLOPEDIA_PATH.name}...")
    with open(ENCYCLOPEDIA_PATH, "rb") as f:
        files = {"file": (ENCYCLOPEDIA_PATH.name, f, "text/markdown")}
        data = {"data": json.dumps({"indexing_technique": "high_quality"})}
        r = httpx.post(
            f"{DIFY_BASE}/console/api/datasets/{dataset_id}/document/create-by-file",
            headers={"Authorization": f"Bearer {API_KEY}"},
            files=files,
            data=data,
            timeout=60,
        )
    if r.status_code not in (200, 201):
        print(f"Upload error: {r.status_code} {r.text[:300]}")
        return 1
    print("  Upload complete. Indexing may take a few minutes.")
    print("\nDone. Add this Knowledge Base to your Chat/Workflow apps.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
