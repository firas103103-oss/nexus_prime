"""
═══════════════════════════════════════════════════════
neural_spine.config.settings — Runtime Configuration
═══════════════════════════════════════════════════════
All environment-based settings for the civilization engine.
"""

import os
import hashlib
from dataclasses import dataclass, field
from functools import lru_cache

import pyotp


@dataclass
class Settings:
    """Central settings — read from environment with sane defaults."""

    # ── Database ────────────────────────────────────────────
    db_url: str = ""
    db_pool_min: int = 3
    db_pool_max: int = 15

    # ── Throne Server ──────────────────────────────────────
    throne_host: str = "127.0.0.1"
    throne_port: int = 7777
    session_timeout: int = 900  # 15 minutes

    # ── Authentication ─────────────────────────────────────
    totp_secret: str = ""
    master_password_hash: str = ""

    # ── Timezone ───────────────────────────────────────────
    timezone: str = "Asia/Riyadh"

    def __post_init__(self):
        """Populate from environment if not set."""
        self.db_url = self.db_url or os.environ.get(
            "THRONE_DB_URL",
            os.environ.get(
                "DATABASE_URL",
                "postgresql://postgres:nexus_mrf_password_2026@127.0.0.1:5432/nexus_db"
            )
        )
        # Use env var, or fall back to a deterministic secret derived from
        # the master password hash so TOTP stays stable across restarts.
        self.totp_secret = self.totp_secret or os.environ.get(
            "THRONE_TOTP_SECRET",
            hashlib.sha256(b"nexus_totp_stable_seed_2026").hexdigest()[:32].upper()
        )
        self.master_password_hash = self.master_password_hash or os.environ.get(
            "THRONE_MASTER_HASH",
            hashlib.sha256("nexus_throne_2026".encode()).hexdigest()
        )
        self.timezone = os.environ.get("TZ", self.timezone)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton settings instance."""
    return Settings()
