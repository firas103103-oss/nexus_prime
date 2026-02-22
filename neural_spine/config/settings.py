"""
═══════════════════════════════════════════════════════
neural_spine.config.settings — Enterprise Prime Configuration
═══════════════════════════════════════════════════════
All environment-based settings for the ENTERPRISE PRIME framework.
"""

import os
import hashlib
import base64
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    """Central settings — read from environment with sane defaults."""

    # ── Database ────────────────────────────────────────────
    db_url: str = ""
    db_pool_min: int = 3
    db_pool_max: int = 15

    # ── Apex Server ──────────────────────────────────────────
    apex_host: str = "127.0.0.1"
    apex_port: int = 7777
    session_timeout: int = 900  # 15 minutes

    # ── Authentication ─────────────────────────────────────
    totp_secret: str = ""
    master_password_hash: str = ""

    # ── Timezone ───────────────────────────────────────────
    timezone: str = "Asia/Riyadh"

    def __post_init__(self):
        """Populate from environment if not set."""
        self.db_url = self.db_url or os.environ.get(
            "APEX_DB_URL",
            os.environ.get(
                "DATABASE_URL",
                "postgresql://postgres:nexus_mrf_password_2026@127.0.0.1:5432/nexus_db"
            )
        )
        # Use env var, or fall back to a deterministic secret derived from
        # a stable seed so TOTP stays stable across restarts.
        # Must be valid base32 for pyotp.
        self.totp_secret = self.totp_secret or os.environ.get(
            "APEX_TOTP_SECRET",
            base64.b32encode(
                hashlib.sha256(b"apex_totp_stable_seed_2026").digest()[:20]
            ).decode()
        )
        self.master_password_hash = self.master_password_hash or os.environ.get(
            "APEX_MASTER_HASH",
            hashlib.sha256("nexus_throne_2026".encode()).hexdigest()
        )
        self.timezone = os.environ.get("TZ", self.timezone)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton settings instance."""
    return Settings()
