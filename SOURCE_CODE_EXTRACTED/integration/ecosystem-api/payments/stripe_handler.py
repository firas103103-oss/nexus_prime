#!/usr/bin/env python3
"""
Stripe Payment Integration for NEXUS PRIME
Handles subscriptions, one-time payments, and webhooks
"""

import os
import json
import hmac
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

# Stripe will be imported when key is set
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False


# === Configuration ===
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")

if STRIPE_AVAILABLE and STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# Products & Pricing
PRODUCTS = {
    "shadow-seven": {
        "name": "Shadow Seven Publisher",
        "prices": {
            "starter": {"amount": 9900, "interval": "month", "currency": "usd"},
            "pro": {"amount": 19900, "interval": "month", "currency": "usd"},
            "annual": {"amount": 99900, "interval": "year", "currency": "usd"},
        }
    },
    "alsultan": {
        "name": "AlSultan Intelligence",
        "prices": {
            "starter": {"amount": 4900, "interval": "month", "currency": "usd"},
            "pro": {"amount": 9900, "interval": "month", "currency": "usd"},
            "annual": {"amount": 49900, "interval": "year", "currency": "usd"},
        }
    },
    "jarvis": {
        "name": "JARVIS Control Hub",
        "prices": {
            "starter": {"amount": 14900, "interval": "month", "currency": "usd"},
            "pro": {"amount": 29900, "interval": "month", "currency": "usd"},
        }
    },
    "imperial": {
        "name": "Imperial UI",
        "prices": {
            "starter": {"amount": 19900, "interval": "month", "currency": "usd"},
            "pro": {"amount": 39900, "interval": "month", "currency": "usd"},
        }
    },
    "xbio": {
        "name": "X-BIO Sentinel",
        "prices": {
            "starter": {"amount": 7900, "interval": "month", "currency": "usd"},
        }
    },
    "data-core": {
        "name": "NEXUS Data Core",
        "prices": {
            "starter": {"amount": 12900, "interval": "month", "currency": "usd"},
        }
    },
    "bundle-pro": {
        "name": "Professional Bundle (5 products)",
        "prices": {
            "monthly": {"amount": 39900, "interval": "month", "currency": "usd"},
            "annual": {"amount": 399900, "interval": "year", "currency": "usd"},
        }
    },
    "bundle-enterprise": {
        "name": "Enterprise Bundle (All 7)",
        "prices": {
            "monthly": {"amount": 99900, "interval": "month", "currency": "usd"},
            "annual": {"amount": 999900, "interval": "year", "currency": "usd"},
        }
    },
}

# === Data Store ===
DATA_DIR = Path("/root/integration/ecosystem-api/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(filename: str) -> list:
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return []


def _save_json(filename: str, data: list):
    filepath = DATA_DIR / filename
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


# === Stripe Operations ===

def create_checkout_session(product_id: str, plan: str, customer_email: str, success_url: str = None, cancel_url: str = None) -> dict:
    """Create a Stripe Checkout Session for subscription"""
    if not STRIPE_AVAILABLE or not STRIPE_SECRET_KEY:
        return {"error": "Stripe not configured", "mode": "demo", "checkout_url": f"https://mrf103.com/demo-checkout?product={product_id}&plan={plan}"}
    
    product = PRODUCTS.get(product_id)
    if not product:
        return {"error": f"Product {product_id} not found"}
    
    price_info = product["prices"].get(plan)
    if not price_info:
        return {"error": f"Plan {plan} not available for {product_id}"}
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email=customer_email,
            line_items=[{
                "price_data": {
                    "currency": price_info["currency"],
                    "unit_amount": price_info["amount"],
                    "recurring": {"interval": price_info["interval"]},
                    "product_data": {"name": product["name"]},
                },
                "quantity": 1,
            }],
            success_url=success_url or f"https://mrf103.com/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=cancel_url or "https://mrf103.com/#pricing",
            metadata={
                "product_id": product_id,
                "plan": plan,
            }
        )
        
        # Log the session
        sessions = _load_json("checkout_sessions.json")
        sessions.append({
            "session_id": session.id,
            "product_id": product_id,
            "plan": plan,
            "email": customer_email,
            "status": "created",
            "created_at": datetime.utcnow().isoformat(),
        })
        _save_json("checkout_sessions.json", sessions)
        
        return {"checkout_url": session.url, "session_id": session.id}
    
    except Exception as e:
        return {"error": str(e)}


def handle_webhook(payload: bytes, sig_header: str) -> dict:
    """Handle Stripe webhook events"""
    if not STRIPE_AVAILABLE or not STRIPE_WEBHOOK_SECRET:
        return {"status": "skipped", "reason": "Stripe not configured"}
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return {"error": str(e)}
    
    event_type = event["type"]
    data = event["data"]["object"]
    
    # Log all events
    events = _load_json("webhook_events.json")
    events.append({
        "event_id": event["id"],
        "type": event_type,
        "created_at": datetime.utcnow().isoformat(),
    })
    _save_json("webhook_events.json", events)
    
    # Handle specific events
    if event_type == "checkout.session.completed":
        return _handle_checkout_completed(data)
    elif event_type == "customer.subscription.updated":
        return _handle_subscription_updated(data)
    elif event_type == "customer.subscription.deleted":
        return _handle_subscription_cancelled(data)
    elif event_type == "invoice.payment_succeeded":
        return _handle_payment_succeeded(data)
    elif event_type == "invoice.payment_failed":
        return _handle_payment_failed(data)
    
    return {"status": "received", "type": event_type}


def _handle_checkout_completed(session) -> dict:
    """Handle successful checkout"""
    customer_email = session.get("customer_email", "")
    product_id = session.get("metadata", {}).get("product_id", "")
    plan = session.get("metadata", {}).get("plan", "")
    subscription_id = session.get("subscription", "")
    
    # Create/update customer record
    customers = _load_json("customers.json")
    customer = next((c for c in customers if c["email"] == customer_email), None)
    
    if customer:
        customer["subscriptions"].append({
            "product_id": product_id,
            "plan": plan,
            "subscription_id": subscription_id,
            "status": "active",
            "started_at": datetime.utcnow().isoformat(),
        })
    else:
        customers.append({
            "email": customer_email,
            "created_at": datetime.utcnow().isoformat(),
            "subscriptions": [{
                "product_id": product_id,
                "plan": plan,
                "subscription_id": subscription_id,
                "status": "active",
                "started_at": datetime.utcnow().isoformat(),
            }]
        })
    
    _save_json("customers.json", customers)
    
    # Log invoice
    invoices = _load_json("invoices.json")
    invoices.append({
        "customer_email": customer_email,
        "product": product_id,
        "plan": plan,
        "amount": PRODUCTS.get(product_id, {}).get("prices", {}).get(plan, {}).get("amount", 0),
        "status": "paid",
        "date": datetime.utcnow().isoformat(),
    })
    _save_json("invoices.json", invoices)
    
    return {"status": "success", "action": "subscription_created", "email": customer_email, "product": product_id}


def _handle_subscription_updated(subscription) -> dict:
    """Handle subscription update"""
    return {"status": "received", "action": "subscription_updated"}


def _handle_subscription_cancelled(subscription) -> dict:
    """Handle subscription cancellation"""
    customers = _load_json("customers.json")
    for customer in customers:
        for sub in customer.get("subscriptions", []):
            if sub.get("subscription_id") == subscription.get("id"):
                sub["status"] = "cancelled"
                sub["cancelled_at"] = datetime.utcnow().isoformat()
    _save_json("customers.json", customers)
    return {"status": "received", "action": "subscription_cancelled"}


def _handle_payment_succeeded(invoice) -> dict:
    """Handle successful payment"""
    invoices = _load_json("invoices.json")
    invoices.append({
        "invoice_id": invoice.get("id"),
        "customer_email": invoice.get("customer_email", ""),
        "amount": invoice.get("amount_paid", 0),
        "status": "paid",
        "date": datetime.utcnow().isoformat(),
    })
    _save_json("invoices.json", invoices)
    return {"status": "received", "action": "payment_succeeded"}


def _handle_payment_failed(invoice) -> dict:
    """Handle failed payment"""
    return {"status": "received", "action": "payment_failed"}


# === API Helpers ===

def get_products_catalog() -> list:
    """Get all products with pricing"""
    catalog = []
    for product_id, product in PRODUCTS.items():
        catalog.append({
            "id": product_id,
            "name": product["name"],
            "plans": [
                {"plan": plan, "amount": f"${info['amount']/100:.2f}", "interval": info["interval"]}
                for plan, info in product["prices"].items()
            ]
        })
    return catalog


def get_customer_subscriptions(email: str) -> list:
    """Get customer's active subscriptions"""
    customers = _load_json("customers.json")
    customer = next((c for c in customers if c["email"] == email), None)
    if customer:
        return [s for s in customer.get("subscriptions", []) if s["status"] == "active"]
    return []


def get_revenue_stats() -> dict:
    """Get revenue statistics"""
    invoices = _load_json("invoices.json")
    customers = _load_json("customers.json")
    
    total_revenue = sum(inv.get("amount", 0) for inv in invoices if inv.get("status") == "paid")
    active_subs = sum(
        1 for c in customers 
        for s in c.get("subscriptions", []) 
        if s.get("status") == "active"
    )
    
    return {
        "total_revenue_cents": total_revenue,
        "total_revenue": f"${total_revenue/100:.2f}",
        "total_customers": len(customers),
        "active_subscriptions": active_subs,
        "total_invoices": len(invoices),
    }


# === Test ===
if __name__ == "__main__":
    print("🔧 NEXUS PRIME - Stripe Payment Module")
    print(f"   Stripe SDK: {'✅ Available' if STRIPE_AVAILABLE else '❌ Not installed (pip install stripe)'}")
    print(f"   API Key: {'✅ Set' if STRIPE_SECRET_KEY else '⚠️  Not set (STRIPE_SECRET_KEY env var)'}")
    print(f"   Products: {len(PRODUCTS)}")
    print(f"   Catalog:")
    for product in get_products_catalog():
        plans = ", ".join(f"{p['plan']}: {p['amount']}/{p['interval']}" for p in product["plans"])
        print(f"     • {product['name']}: {plans}")
    print(f"\n   Revenue: {get_revenue_stats()}")
    print("   ✅ Module ready!")
