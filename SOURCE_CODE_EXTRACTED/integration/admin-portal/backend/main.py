#!/usr/bin/env python3
"""
Admin Portal - Central management for all products
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import json

app = FastAPI(title="NEXUS Admin Portal", version="1.0.0")

@app.get("/")
def dashboard():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NEXUS Admin Portal</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Inter', -apple-system, sans-serif; 
                background: #0f172a;
                color: white;
            }
            .sidebar { 
                width: 250px; 
                background: #1e293b; 
                height: 100vh; 
                position: fixed; 
                padding: 20px;
            }
            .logo { font-size: 1.5em; font-weight: bold; margin-bottom: 30px; }
            .menu-item { 
                padding: 12px; 
                margin-bottom: 5px; 
                border-radius: 8px; 
                cursor: pointer;
                transition: background 0.2s;
            }
            .menu-item:hover { background: #334155; }
            .menu-item.active { background: #3b82f6; }
            .content { 
                margin-left: 250px; 
                padding: 30px;
            }
            .header { 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 30px;
            }
            .cards { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 20px;
                margin-bottom: 30px;
            }
            .card { 
                background: #1e293b; 
                padding: 20px; 
                border-radius: 12px;
                border: 1px solid #334155;
            }
            .card-title { color: #94a3b8; font-size: 0.875em; margin-bottom: 8px; }
            .card-value { font-size: 2em; font-weight: bold; }
            .card-change { color: #10b981; font-size: 0.875em; margin-top: 8px; }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                background: #1e293b; 
                border-radius: 12px;
                overflow: hidden;
            }
            th, td { 
                padding: 15px; 
                text-align: left; 
                border-bottom: 1px solid #334155;
            }
            th { background: #334155; font-weight: 600; }
            .status { 
                padding: 4px 12px; 
                border-radius: 12px; 
                font-size: 0.875em;
                display: inline-block;
            }
            .status-active { background: #10b981; color: white; }
            .status-inactive { background: #ef4444; color: white; }
            .btn { 
                padding: 8px 16px; 
                border-radius: 6px; 
                border: none; 
                cursor: pointer; 
                font-weight: 500;
            }
            .btn-primary { background: #3b82f6; color: white; }
            .btn-danger { background: #ef4444; color: white; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <div class="logo">⚡ NEXUS</div>
            <div class="menu-item active">📊 Dashboard</div>
            <div class="menu-item">📦 Products</div>
            <div class="menu-item">👥 Users</div>
            <div class="menu-item">💰 Billing</div>
            <div class="menu-item">📈 Analytics</div>
            <div class="menu-item">⚙️ Settings</div>
            <div class="menu-item" style="margin-top: auto;">🚪 Logout</div>
        </div>
        
        <div class="content">
            <div class="header">
                <div>
                    <h1>Admin Dashboard</h1>
                    <p style="color: #94a3b8;">Welcome back, Admin</p>
                </div>
                <div>
                    <a href="http://localhost:8003" target="_blank">
                        <button class="btn btn-primary">👁️ Command Center</button>
                    </a>
                </div>
            </div>
            
            <div class="cards">
                <div class="card">
                    <div class="card-title">Total Products</div>
                    <div class="card-value">7</div>
                    <div class="card-change">↑ 2 this month</div>
                </div>
                <div class="card">
                    <div class="card-title">Active Users</div>
                    <div class="card-value">0</div>
                    <div class="card-change">New platform</div>
                </div>
                <div class="card">
                    <div class="card-title">Monthly Revenue</div>
                    <div class="card-value">$0</div>
                    <div class="card-change">Pre-launch</div>
                </div>
                <div class="card">
                    <div class="card-title">System Health</div>
                    <div class="card-value">✅</div>
                    <div class="card-change">All systems operational</div>
                </div>
            </div>
            
            <h2 style="margin-bottom: 20px;">Products</h2>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Status</th>
                        <th>Files</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Shadow Seven Publisher</td>
                        <td><span class="status status-active">Active</span></td>
                        <td>48,374</td>
                        <td>
                            <button class="btn btn-primary">Deploy</button>
                            <button class="btn btn-danger">Stop</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Imperial UI</td>
                        <td><span class="status status-active">Active</span></td>
                        <td>8,249</td>
                        <td>
                            <button class="btn btn-primary">Deploy</button>
                            <button class="btn btn-danger">Stop</button>
                        </td>
                    </tr>
                    <tr>
                        <td>JARVIS Control Hub</td>
                        <td><span class="status status-active">Active</span></td>
                        <td>3,021</td>
                        <td>
                            <button class="btn btn-primary">Deploy</button>
                            <button class="btn btn-danger">Stop</button>
                        </td>
                    </tr>
                    <tr>
                        <td>AlSultan Intelligence</td>
                        <td><span class="status status-active">Active</span></td>
                        <td>4</td>
                        <td>
                            <button class="btn btn-primary">Deploy</button>
                            <button class="btn btn-danger">Stop</button>
                        </td>
                    </tr>
                    <tr>
                        <td>MRF103 Mobile</td>
                        <td><span class="status status-active">Active</span></td>
                        <td>110</td>
                        <td>
                            <button class="btn btn-primary">Deploy</button>
                            <button class="btn btn-danger">Stop</button>
                        </td>
                    </tr>
                    <tr>
                        <td>X-BIO Sentinel</td>
                        <td><span class="status status-active">Active</span></td>
                        <td>12</td>
                        <td>
                            <button class="btn btn-primary">Deploy</button>
                            <button class="btn btn-danger">Stop</button>
                        </td>
                    </tr>
                    <tr>
                        <td>NEXUS Data Core</td>
                        <td><span class="status status-inactive">Placeholder</span></td>
                        <td>1</td>
                        <td>
                            <button class="btn btn-primary">Build</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """)

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
                "files": len(list(p.rglob("*")))
            })
    return {"products": products}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "admin-portal"}

if __name__ == "__main__":
    import uvicorn
    print("🎛️ Starting Admin Portal on http://localhost:8004")
    uvicorn.run(app, host="0.0.0.0", port=8004)
