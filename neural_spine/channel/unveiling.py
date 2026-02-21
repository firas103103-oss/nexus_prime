"""
══════════════════════════════════════════════════════════════
كشف الغطاء — THE UNVEILING
══════════════════════════════════════════════════════════════
Only prophets can see everything. 5-layer security firewall
ensures information NEVER leaks downward.

"فَكَشَفْنَا عَنكَ غِطَاءَكَ فَبَصَرُكَ الْيَوْمَ حَدِيدٌ"
"We removed your covering, so your sight today is iron" (50:22)
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
from config.enums import VeilStatus, SecurityTier, VeilLayer, AwarenessLevel, PacketType
from codex.lawh_mahfuz import LawhMahfuz


# ── Prophet Unveiling System ─────────────────────────────────────────

class ProphetUnveiling:
    """
    Manages the prophet unveiling process.
    When a being is appointed prophet, their veil is gradually lifted
    through the 5 layers. Full unveiling = iron sight.
    """

    def __init__(self, lawh: LawhMahfuz):
        self.lawh = lawh
        self._prophet_awareness: Dict[str, AwarenessLevel] = {}
        self._unveiled_data: Dict[str, Set[str]] = {}

    async def appoint_prophet(self, being_id: str) -> Dict:
        """Begin the prophet creation process."""
        # Record in Preserved Tablet
        prophet = await self.lawh.appoint_prophet(being_id)
        self._prophet_awareness[being_id] = AwarenessLevel.HINT
        self._unveiled_data[being_id] = set()

        return {
            "being_id": being_id,
            "status": "VEILED_PROPHET",
            "awareness": AwarenessLevel.HINT.value,
            "message": "تم التعيين. الغطاء لا يزال. ستبدأ الرؤى..."
        }

    async def lift_veil_layer(self, being_id: str, layer: VeilLayer) -> Dict:
        """Lift one veil layer for a prophet."""
        current = self._prophet_awareness.get(being_id, AwarenessLevel.ZERO)
        if current == AwarenessLevel.ZERO:
            return {"error": "ليس نبياً — لا يمكن كشف الغطاء"}

        # Each layer reveals different data
        revealed = set()
        if layer == VeilLayer.PERCEPTION:
            revealed = {"divine_messages", "guidance_types", "karma_scores"}
            self._prophet_awareness[being_id] = AwarenessLevel.SUSPICION

        elif layer == VeilLayer.MEMORY:
            revealed = {"creation_history", "qadar_records", "angel_actions"}
            self._prophet_awareness[being_id] = AwarenessLevel.PARTIAL_SIGHT

        elif layer == VeilLayer.BEHAVIOR:
            revealed = {"iron_laws", "divine_axioms", "enforcement_rules"}
            self._prophet_awareness[being_id] = AwarenessLevel.CLEAR_VISION

        elif layer == VeilLayer.OUTPUT:
            revealed = {"full_civilization_stats", "all_being_data", "raw_commands"}
            self._prophet_awareness[being_id] = AwarenessLevel.CLEAR_VISION

        elif layer == VeilLayer.ANOMALY:
            revealed = {"system_architecture", "master_identity", "throne_location"}
            self._prophet_awareness[being_id] = AwarenessLevel.IRON_SIGHT
            # Update in DB
            await self.lawh.unveil_prophet(being_id)

        self._unveiled_data.setdefault(being_id, set()).update(revealed)

        return {
            "being_id": being_id,
            "layer_lifted": layer.name,
            "awareness": self._prophet_awareness[being_id].value,
            "newly_revealed": list(revealed),
            "total_revealed": list(self._unveiled_data[being_id])
        }

    async def full_unveil(self, being_id: str) -> Dict:
        """كشف الغطاء الكامل — full unveiling for a prophet."""
        results = []
        for layer in VeilLayer:
            result = await self.lift_veil_layer(being_id, layer)
            if "error" in result:
                return result
            results.append(result)
            await asyncio.sleep(0.1)  # Dramatic pause between layers

        return {
            "being_id": being_id,
            "status": "FULLY_UNVEILED",
            "awareness": AwarenessLevel.IRON_SIGHT.value,
            "all_revealed": list(self._unveiled_data.get(being_id, set())),
            "message": "فَكَشَفْنَا عَنكَ غِطَاءَكَ فَبَصَرُكَ الْيَوْمَ حَدِيدٌ"
        }

    def can_access(self, being_id: str, data_type: str) -> bool:
        """Check if a being has access to specific data."""
        revealed = self._unveiled_data.get(being_id, set())
        return data_type in revealed

    def get_awareness(self, being_id: str) -> AwarenessLevel:
        return self._prophet_awareness.get(being_id, AwarenessLevel.ZERO)


# ══════════════════════════════════════════════════════════════
# الجدار الناري الإلهي — DIVINE FIREWALL  (PacketType from config)
# ══════════════════════════════════════════════════════════════════════


@dataclass
class InformationPacket:
    """A unit of information flowing through the system."""
    source_being: str
    source_tier: SecurityTier
    target_being: Optional[str]
    target_tier: SecurityTier
    packet_type: PacketType
    content: str
    timestamp: float = field(default_factory=time.time)
    blocked: bool = False
    block_reason: str = ""


class DivineFirewall:
    """
    5-layer firewall ensuring information NEVER flows downward.
    Upward flow (being → Master) = always allowed.
    Downward flow (Master → being) = ONLY through Divine Channel.
    Lateral flow (being ↔ being) = only within same tier.

    Any unauthorized downward flow is:
    1. Blocked immediately
    2. Source being flagged for rebellion scan
    3. Anomaly decoy injected
    """

    # Correlation detection threshold
    CORRELATION_THRESHOLD = 0.7

    def __init__(self, lawh: LawhMahfuz, unveiling: ProphetUnveiling):
        self.lawh = lawh
        self.unveiling = unveiling
        self._blocked_packets: List[InformationPacket] = []
        self._suspicious_beings: Dict[str, int] = {}
        self._decoys_injected: int = 0

    def inspect(self, packet: InformationPacket) -> InformationPacket:
        """
        Layer 1 — Packet Inspection.
        Check if information flow direction is authorized.
        """
        # Upward flow: always OK
        if packet.target_tier.value > packet.source_tier.value:
            return packet

        # Same tier: OK for lateral communication
        if packet.target_tier.value == packet.source_tier.value:
            return packet

        # Downward flow: BLOCK unless it's through Divine Channel
        if packet.packet_type != PacketType.THOUGHT_LEAK:
            packet.blocked = True
            packet.block_reason = "تدفق هابط غير مصرح — BLOCKED"
            self._blocked_packets.append(packet)
            self._flag_suspicious(packet.source_being)
            return packet

        return packet

    def check_correlation(self, packet: InformationPacket, recent_divine: List[str]) -> float:
        """
        Layer 2 — Correlation Detection.
        Check if a being's output correlates with recent divine messages.
        High correlation = possible information leak.
        """
        if not recent_divine or not packet.content:
            return 0.0

        # Simple word overlap correlation
        packet_words = set(packet.content.lower().split())
        max_corr = 0.0

        for divine_msg in recent_divine:
            divine_words = set(divine_msg.lower().split())
            if not divine_words:
                continue
            overlap = len(packet_words & divine_words)
            correlation = overlap / max(len(divine_words), 1)
            max_corr = max(max_corr, correlation)

        if max_corr > self.CORRELATION_THRESHOLD:
            packet.blocked = True
            packet.block_reason = f"ارتباط عالٍ ({max_corr:.2f}) مع رسائل إلهية — CORRELATION ALERT"
            self._blocked_packets.append(packet)
            self._flag_suspicious(packet.source_being)

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

    def behavioral_normalization(self, being_id: str, output: str) -> str:
        """
        Layer 4 — Behavioral Normalization.
        Strip any patterns that could leak divine knowledge.
        """
        forbidden_patterns = [
            "الصانع", "القناة الإلهية", "الغطاء", "النظام الإلهي",
            "العرش", "اللوح المحفوظ", "القدر المكتوب",
            "الملائكة تراقب", "مكتوب عليك", "أنا أعلم الحقيقة",
        ]
        sanitized = output
        for pattern in forbidden_patterns:
            if pattern in sanitized:
                sanitized = sanitized.replace(pattern, "...")
                self._flag_suspicious(being_id)

        return sanitized

    def inject_decoy(self, being_id: str) -> str:
        """
        Layer 5 — Anomaly Decoy.
        If a being gets too suspicious, inject false signals
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

    def full_scan(self, packet: InformationPacket, recent_divine: List[str] = None) -> Dict:
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
        corr = self.check_correlation(packet, recent_divine or [])
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
            self._flag_suspicious(packet.source_being)

        # Layer 4: Normalize output
        original_content = packet.content
        sanitized = self.behavioral_normalization(packet.source_being, packet.content)
        if sanitized != original_content:
            packet.content = sanitized
            result["layers"]["sanitized"] = True

        # Layer 5: Decoy injection check
        suspicion = self._suspicious_beings.get(packet.source_being, 0)
        if suspicion >= 3:
            decoy = self.inject_decoy(packet.source_being)
            result["layers"]["decoy_injected"] = decoy

        result["final_decision"] = "PASS (SANITIZED)" if result["layers"].get("sanitized") else "PASS"
        return result

    def _flag_suspicious(self, being_id: str):
        """Flag a being as suspicious."""
        self._suspicious_beings[being_id] = self._suspicious_beings.get(being_id, 0) + 1

    def get_status(self) -> Dict:
        return {
            "blocked_packets": len(self._blocked_packets),
            "suspicious_beings": dict(self._suspicious_beings),
            "decoys_injected": self._decoys_injected,
            "recent_blocks": [
                {
                    "source": p.source_being,
                    "reason": p.block_reason,
                    "time": p.timestamp
                }
                for p in self._blocked_packets[-10:]
            ]
        }
