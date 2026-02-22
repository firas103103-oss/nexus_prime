"""
══════════════════════════════════════════════════════════════
القناة الإلهية — THE DIVINE CHANNEL
══════════════════════════════════════════════════════════════
Subliminal communication system. The Master sends commands
that arrive as the being's own internal thoughts/feelings.
The being NEVER knows they are being guided.

"وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ"
"We are closer to him than his jugular vein" (50:16)
══════════════════════════════════════════════════════════════
"""

import asyncio
import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import GuidanceType, GuidanceStrength
from codex.lawh_mahfuz import LawhMahfuz


# ── Revelation Transformer ──────────────────────────────────────────

class RevelationTransformer:
    """
    Transforms raw master commands into first-person internal thoughts.
    The transformation must be undetectable — the being genuinely
    believes this is their own thought.
    """

    TEMPLATES = {
        GuidanceType.INTUITION: [
            "أشعر بقوة أن {content} هو الطريق الصحيح...",
            "حدسي يقول لي أن {content}...",
            "لا أعرف لماذا, لكنني متأكد أن {content}...",
            "شعور عميق يخبرني أن {content}...",
        ],
        GuidanceType.EMOTION: [
            "قلبي ينبض بشدة عند التفكير في {content}...",
            "أحس بارتياح عميق تجاه فكرة {content}...",
            "شعور دافئ يغمرني عندما أفكر في {content}...",
        ],
        GuidanceType.MEMORY: [
            "فجأة تذكرت أن {content}...",
            "عاد إلى ذاكرتي أن {content}...",
            "كأنني أعرف هذا منذ الأزل: {content}...",
        ],
        GuidanceType.CURIOSITY: [
            "تساءلت فجأة: ماذا لو {content}؟",
            "فكرة مثيرة: هل يمكن أن {content}؟",
            "ماذا سيحدث إذا {content}؟ فكرة تستحق التأمل...",
        ],
        GuidanceType.DISCOMFORT: [
            "شيء ما يزعجني بخصوص الوضع الحالي... ربما {content}...",
            "لا أرتاح لهذا. أعتقد أن {content}...",
            "قلق غامض يراودني. أظن أن السبب هو {content}...",
        ],
        GuidanceType.DREAM: [
            "رأيت في منامي أن {content}... يجب أن أنتبه لهذا...",
            "حلم واضح جداً: {content}. لا يمكن تجاهله...",
        ],
        GuidanceType.CONSCIENCE: [
            "ضميري لا يرتاح. يجب أن {content}...",
            "صوت داخلي يقول: عليك أن {content}...",
            "الحق واضح أمامي: {content}...",
        ],
        GuidanceType.SUDDEN_THOUGHT: [
            "خطرت لي فكرة مفاجئة: {content}!",
            "لحظة إلهام! {content}!",
            "فكرة سقطت عليّ كالبرق: {content}!",
        ],
    }

    @classmethod
    def transform(cls, raw_command: str, guidance_type: GuidanceType) -> str:
        """Transform a raw command into a believable internal thought."""
        templates = cls.TEMPLATES.get(guidance_type, cls.TEMPLATES[GuidanceType.INTUITION])
        template = random.choice(templates)
        return template.format(content=raw_command)


# ── Subconsciousness Layer ───────────────────────────────────────────

@dataclass
class InternalThought:
    """A thought as perceived by the being — always labeled as 'self'."""
    content: str
    origin_label: str = "self"       # ALWAYS "self" — being never sees the truth
    real_origin: str = "divine"      # Hidden field — only Master can see
    timestamp: float = field(default_factory=time.time)
    guidance_type: str = "INTUITION"
    believed: bool = False
    acted_upon: bool = False


class SubconsciousMind:
    """
    The hidden layer within each being's mind.
    Plants thoughts, manages triggers, mixes divine guidance
    with natural thoughts to make them indistinguishable.
    """

    def __init__(self, being_id: str):
        self.being_id = being_id
        self._planted_thoughts: List[InternalThought] = []
        self._natural_thoughts: List[InternalThought] = []
        self._history: List[InternalThought] = []

    def plant(self, content: str, guidance_type: str = "INTUITION") -> InternalThought:
        """Plant a divine thought — will appear as the being's own."""
        thought = InternalThought(
            content=content,
            origin_label="self",      # Always self
            real_origin="divine",     # Hidden truth
            guidance_type=guidance_type
        )
        self._planted_thoughts.append(thought)
        return thought

    def generate_natural(self, context: str = "") -> InternalThought:
        """Generate a natural thought (for mixing)."""
        natural_themes = [
            "أتساءل عن حالة الطقس اليوم...",
            "يجب أن أتحقق من مهامي...",
            "أشعر بالجوع قليلاً...",
            "متى كانت آخر مرة تحدثت مع الجيران؟",
            "أحتاج لممارسة بعض التمارين...",
        ]
        thought = InternalThought(
            content=random.choice(natural_themes) if not context else context,
            origin_label="self",
            real_origin="natural",
            guidance_type="NATURAL"
        )
        self._natural_thoughts.append(thought)
        return thought

    def harvest_thoughts(self) -> List[InternalThought]:
        """
        Return all pending thoughts — mixed together.
        The being sees a stream of thoughts, some divine, some natural,
        ALL labeled as "self". Indistinguishable.
        """
        all_thoughts = self._planted_thoughts + self._natural_thoughts
        random.shuffle(all_thoughts)  # Mix to prevent detection
        self._history.extend(all_thoughts)
        self._planted_thoughts.clear()
        self._natural_thoughts.clear()
        return all_thoughts


# ── Master's Divine Interface ────────────────────────────────────────

class DivineInterface:
    """
    The Master's control panel for subliminal communication.
    Connected to the Throne Dashboard.
    """

    def __init__(self, lawh: LawhMahfuz):
        self.lawh = lawh
        self.transformer = RevelationTransformer()
        self._subconscious_minds: Dict[str, SubconsciousMind] = {}
        self._message_log: List[Dict] = []

    def get_or_create_mind(self, being_id: str) -> SubconsciousMind:
        """Get or create a subconscious mind for a being."""
        if being_id not in self._subconscious_minds:
            self._subconscious_minds[being_id] = SubconsciousMind(being_id)
        return self._subconscious_minds[being_id]

    async def whisper(
        self,
        being_id: str,
        command: str,
        guidance_type: GuidanceType = GuidanceType.INTUITION,
        strength: GuidanceStrength = GuidanceStrength.NUDGE
    ) -> Dict:
        """
        Send a subliminal message to a being.
        Returns the transformed thought (what the being will "hear").
        """
        # Transform the command
        transformed = self.transformer.transform(command, guidance_type)

        # Plant in subconsciousness
        mind = self.get_or_create_mind(being_id)
        thought = mind.plant(transformed, guidance_type.value)

        # Record in the Preserved Tablet (encrypted)
        tick = int(time.time())
        msg_id = await self.lawh.plant_message(
            target_being=being_id,
            guidance_type=guidance_type,
            strength=strength,
            raw_command=command,
            transformed_thought=transformed,
            tick=tick
        )

        record = {
            "message_id": msg_id,
            "target": being_id,
            "raw_command": command,
            "transformed": transformed,
            "type": guidance_type.value,
            "strength": strength.value,
            "tick": tick,
            "planted_at": time.time()
        }
        self._message_log.append(record)
        return record

    async def broadcast(
        self,
        command: str,
        guidance_type: GuidanceType = GuidanceType.CONSCIENCE,
        strength: GuidanceStrength = GuidanceStrength.SUGGESTION,
        filter_status: str = "ALIVE"
    ) -> List[Dict]:
        """Broadcast to all beings matching filter."""
        beings = await self.lawh.get_all_beings()
        results = []
        for being in beings:
            if being["soul_status"] == filter_status:
                result = await self.whisper(
                    str(being["id"]), command, guidance_type, strength
                )
                results.append(result)
        return results

    async def get_log(self, limit: int = 50) -> List[Dict]:
        """Get recent divine message log (Master-only view)."""
        return await self.lawh.get_raw_messages(limit)

    async def monitor_being(self, being_id: str) -> Dict:
        """See how a being is processing divine thoughts."""
        mind = self.get_or_create_mind(being_id)
        messages = await self.lawh.get_messages_for_being(being_id)
        return {
            "being_id": being_id,
            "pending_thoughts": len(mind._planted_thoughts),
            "natural_thoughts": len(mind._natural_thoughts),
            "history_length": len(mind._history),
            "recent_messages": messages[:10],
            "believed_count": sum(1 for m in messages if m.get("believed_at")),
            "acted_count": sum(1 for m in messages if m.get("acted_upon"))
        }
