"""
Sovereign Dify Bridge — Configuration
══════════════════════════════════════
God Mode & God Creation Center — NEXUS PRIME Integration
"""
import os
from typing import Optional

# MSL / Nexus
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:nexus_mrf_password_2026@nexus_db:5432/nexus_db"
)
NERVE_URL: str = os.getenv("NERVE_URL", "http://nexus_nerve:8200")
GATEWAY_URL: str = os.getenv("GATEWAY_URL", "http://sovereign_gateway:9999")
ORACLE_URL: str = os.getenv("ORACLE_URL", "http://nexus_oracle:8100")
MEMORY_KEEPER_URL: str = os.getenv("MEMORY_KEEPER_URL", "http://nexus_memory_keeper:9000")
LITELLM_URL: str = os.getenv("LITELLM_URL", "http://nexus_litellm:4000")

# Dify
DIFY_API_URL: str = os.getenv("DIFY_API_URL", "http://dify_api:5001")
DIFY_API_KEY: str = os.getenv("DIFY_API_KEY", "")
DIFY_APP_WORKFLOW_ID: str = os.getenv("DIFY_APP_WORKFLOW_ID", "")  # Defensive workflow
DIFY_DEFENSIVE_WORKFLOW_ID: str = os.getenv("DIFY_DEFENSIVE_WORKFLOW_ID", "")

# Hormonal thresholds — trigger defensive workflow when exceeded
CORTISOL_SPIKE_THRESHOLD: float = float(os.getenv("CORTISOL_SPIKE_THRESHOLD", "0.6"))
ADRENALINE_SPIKE_THRESHOLD: float = float(os.getenv("ADRENALINE_SPIKE_THRESHOLD", "0.5"))
HORMONAL_POLL_INTERVAL_SEC: int = int(os.getenv("HORMONAL_POLL_INTERVAL_SEC", "10"))

# X-BIO / VOC
XBIO_WEBHOOK_SECRET: str = os.getenv("XBIO_WEBHOOK_SECRET", "nexus_xbio_sentinel")
VOC_ANOMALY_THRESHOLD: float = float(os.getenv("VOC_ANOMALY_THRESHOLD", "0.8"))

# Sovereign entity for action_ledger
SOVEREIGN_ENTITY_NAME: str = os.getenv("SOVEREIGN_ENTITY_NAME", "AS-SULTAN")
