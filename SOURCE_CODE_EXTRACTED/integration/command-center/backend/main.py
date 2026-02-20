#!/usr/bin/env python3
"""
Command Center - Approval workflow and system control
"""

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
from pathlib import Path
from datetime import datetime

app = FastAPI(title="NEXUS Command Center", version="1.0.0")

# Models
class Approval(BaseModel):
    action: str
    product: str
    details: dict
    priority: str = "normal"

class Decision(BaseModel):
    approval_id: int
    decision: str  # "approve" or "reject"
    notes: str = ""

# Database file
APPROVALS_FILE = Path("/root/integration/command-center/database/approvals.json")
APPROVALS_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_approvals():
    """Load approvals from file"""
    if APPROVALS_FILE.exists():
        with open(APPROVALS_FILE) as f:
            return json.load(f)
    return []

def save_approvals(approvals):
    """Save approvals to file"""
    with open(APPROVALS_FILE, "w") as f:
        json.dump(approvals, f, indent=2)

# Routes
@app.get("/")
def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NEXUS Command Center</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0; padding: 20px; color: white;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { text-align: center; font-size: 2.5em; margin-bottom: 10px; }
            .subtitle { text-align: center; margin-bottom: 30px; opacity: 0.9; }
            .stats { display: flex; gap: 20px; margin-bottom: 30px; }
            .stat-card { 
                background: rgba(255,255,255,0.1); 
                padding: 20px; 
                border-radius: 10px; 
                flex: 1; 
                backdrop-filter: blur(10px);
            }
            .stat-number { font-size: 3em; font-weight: bold; }
            .stat-label { opacity: 0.8; }
            .approval-list { background: rgba(255,255,255,0.95); color: #333; padding: 20px; border-radius: 10px; }
            .approval-item { 
                border-bottom: 1px solid #ddd; 
                padding: 15px; 
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .approval-item:last-child { border-bottom: none; }
            .approval-info { flex: 1; }
            .approval-actions { display: flex; gap: 10px; }
            button { 
                padding: 8px 20px; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                font-weight: bold;
            }
            .btn-approve { background: #10b981; color: white; }
            .btn-reject { background: #ef4444; color: white; }
            .btn-approve:hover { background: #059669; }
            .btn-reject:hover { background: #dc2626; }
            .priority-high { border-left: 4px solid #ef4444; }
            .priority-normal { border-left: 4px solid #3b82f6; }
            .status-pending { background: #fef3c7; }
            .status-approved { background: #d1fae5; }
            .status-rejected { background: #fee2e2; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👁️ NEXUS Command Center</h1>
            <p class="subtitle">Spiritual Interface - Approval & Control</p>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="pending-count">0</div>
                    <div class="stat-label">Pending Approvals</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="approved-count">0</div>
                    <div class="stat-label">Approved Today</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="rejected-count">0</div>
                    <div class="stat-label">Rejected Today</div>
                </div>
            </div>
            
            <div class="approval-list">
                <h2>⏳ Pending Decisions</h2>
                <div id="approvals-container">
                    <p>Loading approvals...</p>
                </div>
            </div>
        </div>
        
        <script>
            async function loadApprovals() {
                const response = await fetch('/api/v1/approvals');
                const data = await response.json();
                
                const pending = data.approvals.filter(a => a.status === 'pending');
                const approved = data.approvals.filter(a => a.status === 'approved');
                const rejected = data.approvals.filter(a => a.status === 'rejected');
                
                document.getElementById('pending-count').textContent = pending.length;
                document.getElementById('approved-count').textContent = approved.length;
                document.getElementById('rejected-count').textContent = rejected.length;
                
                const container = document.getElementById('approvals-container');
                if (pending.length === 0) {
                    container.innerHTML = '<p style="text-align: center; color: #888;">✅ No pending approvals</p>';
                    return;
                }
                
                container.innerHTML = pending.map(approval => `
                    <div class="approval-item priority-${approval.priority} status-${approval.status}">
                        <div class="approval-info">
                            <strong>${approval.action}</strong> on <em>${approval.product}</em><br>
                            <small>${approval.details.description || JSON.stringify(approval.details)}</small><br>
                            <small style="color: #888;">ID: ${approval.id} | Priority: ${approval.priority}</small>
                        </div>
                        <div class="approval-actions">
                            <button class="btn-approve" onclick="decide(${approval.id}, 'approve')">✓ Approve</button>
                            <button class="btn-reject" onclick="decide(${approval.id}, 'reject')">✗ Reject</button>
                        </div>
                    </div>
                `).join('');
            }
            
            async function decide(approvalId, decision) {
                const response = await fetch('/api/v1/approvals/' + approvalId + '/decide', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({decision: decision, notes: ''})
                });
                
                if (response.ok) {
                    loadApprovals();
                }
            }
            
            // Load approvals on page load
            loadApprovals();
            
            // Refresh every 5 seconds
            setInterval(loadApprovals, 5000);
        </script>
    </body>
    </html>
    """)

@app.get("/api/v1/approvals")
def get_approvals():
    """Get all approvals"""
    approvals = load_approvals()
    return {"approvals": approvals}

@app.get("/api/v1/approvals/pending")
def get_pending_approvals():
    """Get pending approvals only"""
    approvals = load_approvals()
    pending = [a for a in approvals if a.get("status") == "pending"]
    return {"approvals": pending}

@app.post("/api/v1/approvals")
def create_approval(approval: Approval):
    """Create new approval request"""
    approvals = load_approvals()
    
    new_approval = {
        "id": len(approvals) + 1,
        "action": approval.action,
        "product": approval.product,
        "details": approval.details,
        "priority": approval.priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "decided_at": None,
        "decision_notes": ""
    }
    
    approvals.append(new_approval)
    save_approvals(approvals)
    
    return {"message": "Approval created", "id": new_approval["id"]}

@app.post("/api/v1/approvals/{approval_id}/decide")
def decide_approval(approval_id: int, decision: Decision):
    """Make decision on approval"""
    approvals = load_approvals()
    
    for approval in approvals:
        if approval["id"] == approval_id:
            approval["status"] = decision.decision + "d"  # "approved" or "rejected"
            approval["decided_at"] = datetime.now().isoformat()
            approval["decision_notes"] = decision.notes
            break
    
    save_approvals(approvals)
    return {"message": f"Approval {decision.decision}d"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Command Center on http://localhost:8003")
    uvicorn.run(app, host="0.0.0.0", port=8003)
