# Command Center 👁️

**Spiritual Interface** - Approval workflow and control dashboard where creator reviews and approves/rejects all major system actions.

## Purpose

This is the "divine connection" - every significant action (deployment, marketing campaign, code change, financial transaction) comes here for human approval before execution.

## Features

- **Approval Queue**: All pending actions displayed
- **Real-time Dashboard**: Auto-refreshes every 5 seconds
- **Priority System**: High/normal/low priority actions
- **Decision History**: Track approved and rejected actions
- **WebSocket Support**: Live updates (future)

## Architecture

```
CLONE HUB → generates action → Command Center → human approval → execution
                                       ↓
                              Creator sees & decides
```

## Usage

```bash
# Start Command Center
python3 backend/main.py

# Access dashboard
open http://localhost:8003
```

## API Endpoints

- `GET /` - Dashboard UI
- `GET /api/v1/approvals` - All approvals
- `GET /api/v1/approvals/pending` - Pending only
- `POST /api/v1/approvals` - Create approval
- `POST /api/v1/approvals/{id}/decide` - Approve/reject

## Integration

Used by:
- CLONE HUB (to request approvals)
- Ecosystem API (to forward decisions)
- All products (for critical actions)

## Philosophy

This dashboard embodies the vision: **"Self-perceiving, self-updating system connected spiritually to creator"**

The AI can think, analyze, and propose - but the human creator has final say on all major decisions.
