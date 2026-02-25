"""
Ecosystem API — Unified entry point for mrf103.com /api/, api, platform, sultan, data, admin.
Port: 8005
"""
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NEXUS PRIME Ecosystem API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS_DIR = Path(os.getenv("PRODUCTS_DIR", "/products"))
ECOSYSTEM_DATA_DIR = Path(os.getenv("ECOSYSTEM_DATA_DIR", "/data"))


@app.get("/")
async def root():
    return {"service": "ecosystem_api", "status": "running", "port": 8005}


@app.get("/health")
async def health():
    return {"status": "healthy", "clone_hub": "running", "ecosystem_api": "running", "nexus_prime": "running"}


@app.get("/api/v1/health")
async def api_health():
    return await health()


@app.get("/api/v1/products")
async def list_products():
    products = []
    if PRODUCTS_DIR.exists():
        for d in sorted(PRODUCTS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                products.append({"name": d.name, "path": str(d)})
    return {"products": products, "count": len(products)}


@app.get("/api/v1/products/{name}")
async def get_product(name: str):
    path = PRODUCTS_DIR / name
    if not path.exists() or not path.is_dir():
        return {"error": "not_found", "name": name}
    return {"name": name, "path": str(path)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
