#!/usr/bin/env python3
"""
Ecosystem API Gateway - Central hub for all products
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI(title="NEXUS Ecosystem API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Product(BaseModel):
    name: str
    status: str
    file_count: int

class ApprovalRequest(BaseModel):
    action: str
    product: str
    details: dict

# Routes
@app.get("/")
def root():
    return {"message": "NEXUS Ecosystem API", "version": "1.0.0"}

@app.get("/api/v1/products")
def list_products():
    """List all products"""
    products_dir = Path("/root/products")
    products = []
    for p in products_dir.iterdir():
        if p.is_dir():
            products.append({
                "name": p.name,
                "status": "active",
                "file_count": len(list(p.rglob("*")))
            })
    return {"products": products}

@app.get("/api/v1/products/{product_name}")
def get_product(product_name: str):
    """Get product details"""
    product_path = Path(f"/root/products/{product_name}")
    if not product_path.exists():
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "name": product_name,
        "path": str(product_path),
        "files": len(list(product_path.rglob("*"))),
        "readme": (product_path / "README.md").exists()
    }

@app.get("/api/v1/health")
def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "services": {
            "clone_hub": "running",
            "ecosystem_api": "running",
            "nexus_prime": "running"
        }
    }

@app.post("/api/v1/approvals")
def create_approval(request: ApprovalRequest):
    """Create approval request for Command Center"""
    approvals_file = Path("/root/integration/command-center/pending_approvals.json")
    approvals_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing approvals
    if approvals_file.exists():
        with open(approvals_file) as f:
            approvals = json.load(f)
    else:
        approvals = []
    
    # Add new approval
    approval = {
        "id": len(approvals) + 1,
        "action": request.action,
        "product": request.product,
        "details": request.details,
        "status": "pending"
    }
    approvals.append(approval)
    
    # Save
    with open(approvals_file, "w") as f:
        json.dump(approvals, f, indent=2)
    
    return {"message": "Approval request created", "id": approval["id"]}

# === Stripe Payment Routes ===
import sys
sys.path.insert(0, str(Path(__file__).parent))
from payments.stripe_handler import (
    create_checkout_session, handle_webhook, get_products_catalog,
    get_customer_subscriptions, get_revenue_stats, STRIPE_PUBLISHABLE_KEY
)

class CheckoutRequest(BaseModel):
    product_id: str
    plan: str
    email: str

@app.get("/api/v1/catalog")
def get_catalog():
    """Get products catalog with pricing"""
    return {"products": get_products_catalog(), "publishable_key": STRIPE_PUBLISHABLE_KEY}

@app.post("/api/v1/checkout")
def checkout(request: CheckoutRequest):
    """Create checkout session"""
    result = create_checkout_session(request.product_id, request.plan, request.email)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/webhook/stripe")
async def stripe_webhook(request_obj=None):
    """Handle Stripe webhooks"""
    from fastapi import Request
    # In production, read raw body
    return {"status": "received"}

@app.get("/api/v1/subscriptions/{email}")
def get_subscriptions(email: str):
    """Get customer subscriptions"""
    return {"subscriptions": get_customer_subscriptions(email)}

@app.get("/api/v1/revenue")
def revenue():
    """Revenue dashboard"""
    return get_revenue_stats()

# === Lead Capture ===
class LeadRequest(BaseModel):
    email: str
    source: str = "unknown"
    product: str = ""
    plan: str = ""

@app.post("/api/v1/leads")
def capture_lead(lead: LeadRequest):
    """Capture lead from landing pages"""
    leads_file = Path("/root/integration/ecosystem-api/data/leads.json")
    leads_file.parent.mkdir(parents=True, exist_ok=True)
    
    if leads_file.exists():
        with open(leads_file) as f:
            leads = json.load(f)
    else:
        leads = []
    
    from datetime import datetime
    leads.append({
        "email": lead.email,
        "source": lead.source,
        "product": lead.product,
        "plan": lead.plan,
        "timestamp": datetime.utcnow().isoformat(),
    })
    
    with open(leads_file, "w") as f:
        json.dump(leads, f, indent=2)
    
    return {"status": "captured", "message": "Lead saved successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
