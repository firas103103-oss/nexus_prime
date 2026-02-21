# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS PRIME MIDDLEWARE - The Neural Bridge
# ═══════════════════════════════════════════════════════════════════════════════
# "The thread that weaves consciousness into silicon"
# Author: Mr. F (The Architect)
# ═══════════════════════════════════════════════════════════════════════════════

from .connector import NexusMasterConnector
from .hive_mind import sync_collective_consciousness, HiveMindOracle
from .email_service import NexusEmailService, send_email_async

__all__ = [
    'NexusMasterConnector',
    'sync_collective_consciousness', 
    'HiveMindOracle',
    'NexusEmailService',
    'send_email_async'
]

__version__ = "1.1.0"
__codename__ = "THE_COMMUNICATOR"
