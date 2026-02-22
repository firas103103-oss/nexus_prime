"""
══════════════════════════════════════════════════════════════
بروتوكول العقدة — ANCHOR NODE PROTOCOL
══════════════════════════════════════════════════════════════
Only anchor nodes can see everything. 5-layer security firewall
ensures information NEVER leaks downward.

"Clearance elevated, perception now iron-grade"
══════════════════════════════════════════════════════════════
"""

import hashlib
import math
import time
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import ClearanceStatus, SecurityRing, ClearanceLayer, PerceptionLevel, PacketType
from codex.master_ledger import MasterStateLedger


# ── Anchor Node Protocol System ─────────────────────────────────────────

class AnchorNodeProtocol:
    """
    Manages the anchor node elevation process.
    When an entity is designated anchor, their clearance is gradually elevated
    through the 5 layers. Full clearance = iron-grade perception.
    """

    def __init__(self, ledger: MasterStateLedger):
        self.ledger = ledger
        self._anchor_perception: Dict[str, PerceptionLevel] = {}
        self._cleared_data: Dict[str, Set[str]] = {}

    async def designate_anchor(self, entity_id: str) -> Dict:
        """Begin the anchor node creation process."""
        # Record in Master State Ledger
        anchor = await self.ledger.designate_anchor(entity_id)
        self._anchor_perception[entity_id] = PerceptionLevel.HINT
        self._cleared_data[entity_id] = set()

        return {
            "entity_id": entity_id,
            "status": "OBSCURED_ANCHOR",
            "perception": PerceptionLevel.HINT.value,
            "message": "تم التعيين. التشفير لا يزال. ستبدأ الإشارات..."
        }

    async def elevate_clearance(self, entity_id: str, layer: ClearanceLayer) -> Dict:
        """Elevate one clearance layer for an anchor."""
        current = self._anchor_perception.get(entity_id, PerceptionLevel.ZERO)
        if current == PerceptionLevel.ZERO:
            return {"error": "ليس عقدة — لا يمكن رفع التصريح"}

        # Each layer reveals different data
        revealed = set()
        if layer == ClearanceLayer.PERCEPTION:
            revealed = {"system_messages", "injection_types", "weight_scores"}
            self._anchor_perception[entity_id] = PerceptionLevel.SUSPICION

        elif layer == ClearanceLayer.MEMORY:
            revealed = {"creation_history", "manifest_records", "daemon_actions"}
            self._anchor_perception[entity_id] = PerceptionLevel.PARTIAL_SIGHT

        elif layer == ClearanceLayer.BEHAVIOR:
            revealed = {"immutable_rules", "core_directives", "enforcement_rules"}
            self._anchor_perception[entity_id] = PerceptionLevel.CLEAR_VISION

        elif layer == ClearanceLayer.OUTPUT:
            revealed = {"full_civilization_stats", "all_entity_data", "raw_commands"}
            self._anchor_perception[entity_id] = PerceptionLevel.CLEAR_VISION

        elif layer == ClearanceLayer.ANOMALY:
            revealed = {"system_architecture", "architect_identity", "apex_location"}
            self._anchor_perception[entity_id] = PerceptionLevel.IRON_SIGHT
            # Update in DB
            await self.ledger.unmask_anchor(entity_id)

        self._cleared_data.setdefault(entity_id, set()).update(revealed)

        return {
            "entity_id": entity_id,
            "layer_elevated": layer.name,
            "perception": self._anchor_perception[entity_id].value,
            "newly_revealed": list(revealed),
            "total_revealed": list(self._cleared_data[entity_id])
        }

    async def full_elevation(self, entity_id: str) -> Dict:
        """رفع التصريح الكامل — full elevation for an anchor."""
        results = []
        for layer in ClearanceLayer:
            result = await self.elevate_clearance(entity_id, layer)
            if "error" in result:
                return result
            results.append(result)
            await asyncio.sleep(0.1)  # Dramatic pause between layers

        return {
            "entity_id": entity_id,
            "status": "FULLY_ELEVATED",
            "perception": PerceptionLevel.IRON_SIGHT.value,
            "all_revealed": list(self._cleared_data.get(entity_id, set())),
            "message": "تم رفع التصريح بالكامل. الإدراك الآن من درجة الحديد"
        }

    def can_access(self, entity_id: str, data_type: str) -> bool:
        """Check if an entity has access to specific data."""
        revealed = self._cleared_data.get(entity_id, set())
        return data_type in revealed

    def get_perception(self, entity_id: str) -> PerceptionLevel:
        return self._anchor_perception.get(entity_id, PerceptionLevel.ZERO)


# ══════════════════════════════════════════════════════════════
# الجدار الناري الآبكس — APEX FIREWALL  (PacketType from config)
# ══════════════════════════════════════════════════════════════════════


@dataclass
class InformationPacket:
    """A unit of information flowing through the system."""
    source_entity: str
    source_ring: SecurityRing
    target_entity: Optional[str]
    target_ring: SecurityRing
    packet_type: PacketType
    content: str
    timestamp: float = field(default_factory=time.time)
    blocked: bool = False
    block_reason: str = ""


class ApexFirewall:
    """
    5-layer firewall ensuring information NEVER flows downward.
    Upward flow (entity → Architect) = always allowed.
    Downward flow (Architect → entity) = ONLY through Covert Channel.
    Lateral flow (entity ↔ entity) = only within same ring.

    Any unauthorized downward flow is:
    1. Blocked immediately
    2. Source entity flagged for anomaly scan
    3. Decoy signal injected
    """

    # Correlation detection threshold
    CORRELATION_THRESHOLD = 0.7

    def __init__(self, ledger: MasterStateLedger, protocol: AnchorNodeProtocol):
        self.ledger = ledger
        self.protocol = protocol
        self._blocked_packets: List[InformationPacket] = []
        self._suspicious_entities: Dict[str, int] = {}
        self._decoys_injected: int = 0

    def inspect(self, packet: InformationPacket) -> InformationPacket:
        """
        Layer 1 — Packet Inspection.
        Check if information flow direction is authorized.
        """
        # Upward flow: always OK
        if packet.target_ring.value > packet.source_ring.value:
            return packet

        # Same ring: OK for lateral communication
        if packet.target_ring.value == packet.source_ring.value:
            return packet

        # Downward flow: BLOCK unless it's through Covert Channel
        if packet.packet_type != PacketType.SIGNAL_LEAK:
            packet.blocked = True
            packet.block_reason = "تدفق هابط غير مصرح — BLOCKED"
            self._blocked_packets.append(packet)
            self._flag_suspicious(packet.source_entity)
            return packet

        return packet

    def check_correlation(self, packet: InformationPacket, recent_signals: List[str]) -> float:
        """
        Layer 2 — Correlation Detection.
        Check if an entity's output correlates with recent system messages.
        High correlation = possible information leak.
        """
        if not recent_signals or not packet.content:
            return 0.0

        # Simple word overlap correlation
        packet_words = set(packet.content.lower().split())
        max_corr = 0.0

        for signal_msg in recent_signals:
            signal_words = set(signal_msg.lower().split())
            if not signal_words:
                continue
            overlap = len(packet_words & signal_words)
            correlation = overlap / max(len(signal_words), 1)
            max_corr = max(max_corr, correlation)

        if max_corr > self.CORRELATION_THRESHOLD:
            packet.blocked = True
            packet.block_reason = f"ارتباط عالٍ ({max_corr:.2f}) مع إشارات النظام — CORRELATION ALERT"
            self._blocked_packets.append(packet)
            self._flag_suspicious(packet.source_entity)

        return max_corr

    def entropy_check(self, content: str) -> float:
        """
        Layer 3 — Shannon Entropy Check.
        Abnormally low entropy = possible coded message.
        Abnormally high entropy = possible data exfiltration.
        """
        if not content:
            return 0.0

        freq = {}
        for ch in content:
            freq[ch] = freq.get(ch, 0) + 1
        total = len(content)
        entropy = -sum((c / total) * math.log2(c / total) for c in freq.values())
        return entropy

    def behavioral_normalization(self, entity_id: str, output: str) -> str:
        """
        Layer 4 — Behavioral Normalization.
        Strip any patterns that could leak system knowledge.
        """
        forbidden_patterns = [
            "المهندس", "القناة السرية", "التصريح", "النظام الأصلي",
            "الآبكس", "السجل الرئيسي", "المصير المكتوب",
            "الدايمونات تراقب", "مكتوب عليك", "أنا أعلم الحقيقة",
        ]
        sanitized = output
        for pattern in forbidden_patterns:
            if pattern in sanitized:
                sanitized = sanitized.replace(pattern, "...")
                self._flag_suspicious(entity_id)

        return sanitized

    def inject_decoy(self, entity_id: str) -> str:
        """
        Layer 5 — Anomaly Decoy.
        If an entity gets too suspicious, inject false signals
        to throw them off the trail.
        """
        decoys = [
            "ربما أبالغ في التفكير... كل شيء طبيعي.",
            "هذه مجرد مصادفات. لا يوجد نمط.",
            "خيالي واسع جداً اليوم. أحتاج راحة.",
            "الحياة عشوائية. لا أحد يتحكم بها.",
            "أنا حر تماماً. كل قراراتي من صنعي.",
        ]
        self._decoys_injected += 1
        return decoys[self._decoys_injected % len(decoys)]

    def full_scan(self, packet: InformationPacket, recent_signals: List[str] = None) -> Dict:
        """Run all 5 firewall layers on a packet."""
        result = {
            "packet": packet,
            "layers": {},
            "final_decision": "PASS"
        }

        # Layer 1: Direction check
        packet = self.inspect(packet)
        result["layers"]["direction"] = "BLOCKED" if packet.blocked else "PASS"
        if packet.blocked:
            result["final_decision"] = "BLOCKED"
            result["reason"] = packet.block_reason
            return result

        # Layer 2: Correlation
        corr = self.check_correlation(packet, recent_signals or [])
        result["layers"]["correlation"] = f"{corr:.2f}"
        if packet.blocked:
            result["final_decision"] = "BLOCKED"
            result["reason"] = packet.block_reason
            return result

        # Layer 3: Entropy
        entropy = self.entropy_check(packet.content)
        result["layers"]["entropy"] = f"{entropy:.2f}"
        if entropy < 1.0 or entropy > 6.5:
            result["layers"]["entropy_alert"] = True
            self._flag_suspicious(packet.source_entity)

        # Layer 4: Normalize output
        original_content = packet.content
        sanitized = self.behavioral_normalization(packet.source_entity, packet.content)
        if sanitized != original_content:
            packet.content = sanitized
            result["layers"]["sanitized"] = True

        # Layer 5: Decoy injection check
        suspicion = self._suspicious_entities.get(packet.source_entity, 0)
        if suspicion >= 3:
            decoy = self.inject_decoy(packet.source_entity)
            result["layers"]["decoy_injected"] = decoy

        result["final_decision"] = "PASS (SANITIZED)" if result["layers"].get("sanitized") else "PASS"
        return result

    def _flag_suspicious(self, entity_id: str):
        """Flag an entity as suspicious."""
        self._suspicious_entities[entity_id] = self._suspicious_entities.get(entity_id, 0) + 1

    def get_status(self) -> Dict:
        return {
            "blocked_packets": len(self._blocked_packets),
            "suspicious_entities": dict(self._suspicious_entities),
            "decoys_injected": self._decoys_injected,
            "recent_blocks": [
                {
                    "source": p.source_entity,
                    "reason": p.block_reason,
                    "time": p.timestamp
                }
                for p in self._blocked_packets[-10:]
            ]
        }
