"""
Sovereign Analytics — Traffic tracking (Google Analytics–style)
═══════════════════════════════════════════════════════════════
Self-hosted page views & events. No external deps.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import asyncpg


ANALYTICS_SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS analytics.tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL CHECK (event_type IN ('pageview', 'event')),
    path TEXT NOT NULL,
    event_name TEXT,
    event_params JSONB DEFAULT '{}'::jsonb,
    referrer TEXT,
    session_id TEXT,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_tracking_created ON analytics.tracking(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tracking_path ON analytics.tracking(path);
"""


async def ensure_analytics_schema(pool: asyncpg.Pool) -> None:
    """Ensure analytics schema exists."""
    try:
        await pool.execute(ANALYTICS_SCHEMA_SQL)
    except Exception:
        pass


async def track(
    pool: asyncpg.Pool,
    event_type: str,
    path: str,
    event_name: Optional[str] = None,
    event_params: Optional[Dict[str, Any]] = None,
    referrer: Optional[str] = None,
    session_id: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> None:
    """Log a pageview or event."""
    try:
        params_json = json.dumps(event_params or {}) if isinstance(event_params, dict) else "{}"
        await pool.execute("""
            INSERT INTO analytics.tracking (event_type, path, event_name, event_params, referrer, session_id, user_agent)
            VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7)
        """, event_type, path, event_name or "", params_json, referrer or "", session_id or "", (user_agent or "")[:500])
    except Exception:
        pass  # Don't fail requests if analytics table missing


async def get_stats(
    pool: asyncpg.Pool,
    hours: int = 24,
) -> Dict[str, Any]:
    """Aggregate stats for dashboard (like GA overview)."""
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    try:
        # Total pageviews
        pv = await pool.fetchval(
            "SELECT COUNT(*) FROM analytics.tracking WHERE event_type = 'pageview' AND created_at >= $1",
            since,
        ) or 0

        # Unique sessions (approx)
        sessions = await pool.fetchval(
            "SELECT COUNT(DISTINCT session_id) FROM analytics.tracking WHERE session_id != '' AND created_at >= $1",
            since,
        ) or 0

        # Top pages
        top_pages = await pool.fetch("""
            SELECT path, COUNT(*) as views
            FROM analytics.tracking
            WHERE event_type = 'pageview' AND created_at >= $1
            GROUP BY path
            ORDER BY views DESC
            LIMIT 10
        """, since)

        # Top events
        top_events = await pool.fetch("""
            SELECT event_name, COUNT(*) as count
            FROM analytics.tracking
            WHERE event_type = 'event' AND event_name != '' AND created_at >= $1
            GROUP BY event_name
            ORDER BY count DESC
            LIMIT 10
        """, since)

        # Hourly trend (last 24h)
        hourly = await pool.fetch("""
            SELECT date_trunc('hour', created_at) as hour, COUNT(*) as views
            FROM analytics.tracking
            WHERE event_type = 'pageview' AND created_at >= $1
            GROUP BY date_trunc('hour', created_at)
            ORDER BY hour
        """, since)

        return {
            "period_hours": hours,
            "pageviews": pv,
            "sessions": sessions,
            "top_pages": [{"path": r["path"], "views": r["views"]} for r in top_pages],
            "top_events": [{"event": r["event_name"], "count": r["count"]} for r in top_events],
            "hourly": [{"hour": str(r["hour"]), "views": r["views"]} for r in hourly],
        }
    except Exception:
        return {
            "period_hours": hours,
            "pageviews": 0,
            "sessions": 0,
            "top_pages": [],
            "top_events": [],
            "hourly": [],
            "error": "analytics schema not initialized",
        }
