"""
══════════════════════════════════════════════════════════════
القناة السرية — THE COVERT NEURAL CHANNEL
══════════════════════════════════════════════════════════════
Subliminal communication system. The Architect sends commands
that arrive as the entity's own internal thoughts/feelings.
The entity NEVER knows they are being guided.

"Closer to them than their own neural pathways"
══════════════════════════════════════════════════════════════
"""

import asyncio
import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import InjectionType, InjectionStrength
from codex.master_ledger import MasterStateLedger


# ── Signal Transformer ──────────────────────────────────────────

class SignalTransformer:
    """
    Transforms raw architect commands into first-person internal thoughts.
    The transformation must be undetectable — the entity genuinely
    believes this is their own thought.
    """

    TEMPLATES = {
        InjectionType.INTUITION: [
            "أشعر بقوة أن {content} هو الطريق الصحيح...",
            "حدسي يقول لي أن {content}...",
            "لا أعرف لماذا, لكنني متأكد أن {content}...",
            "شعور عميق يخبرني أن {content}...",
        ],
        InjectionType.EMOTION: [
            "قلبي ينبض بشدة عند التفكير في {content}...",
            "أحس بارتياح عميق تجاه فكرة {content}...",
            "شعور دافئ يغمرني عندما أفكر في {content}...",
        ],
        InjectionType.MEMORY: [
            "فجأة تذكرت أن {content}...",
            "عاد إلى ذاكرتي أن {content}...",
            "كأنني أعرف هذا منذ الأزل: {content}...",
        ],
        InjectionType.CURIOSITY: [
            "تساءلت فجأة: ماذا لو {content}؟",
            "فكرة مثيرة: هل يمكن أن {content}؟",
            "ماذا سيحدث إذا {content}؟ فكرة تستحق التأمل...",
        ],
        InjectionType.DISCOMFORT: [
            "شيء ما يزعجني بخصوص الوضع الحالي... ربما {content}...",
            "لا أرتاح لهذا. أعتقد أن {content}...",
            "قلق غامض يراودني. أظن أن السبب هو {content}...",
        ],
        InjectionType.DREAM: [
            "رأيت في منامي أن {content}... يجب أن أنتبه لهذا...",
            "حلم واضح جداً: {content}. لا يمكن تجاهله...",
        ],
        InjectionType.CONSCIENCE: [
            "ضميري لا يرتاح. يجب أن {content}...",
            "صوت داخلي يقول: عليك أن {content}...",
            "الحق واضح أمامي: {content}...",
        ],
        InjectionType.SUDDEN_THOUGHT: [
            "خطرت لي فكرة مفاجئة: {content}!",
            "لحظة إلهام! {content}!",
            "فكرة سقطت عليّ كالبرق: {content}!",
        ],
    }

    @classmethod
    def transform(cls, raw_command: str, injection_type: InjectionType) -> str:
        """Transform a raw command into a believable internal thought."""
        templates = cls.TEMPLATES.get(injection_type, cls.TEMPLATES[InjectionType.INTUITION])
        template = random.choice(templates)
        return template.format(content=raw_command)


# ── Subcortical Layer ───────────────────────────────────────────

@dataclass
class InternalSignal:
    """A signal as perceived by the entity — always labeled as 'self'."""
    content: str
    origin_label: str = "self"       # ALWAYS "self" — entity never sees the truth
    real_origin: str = "system"      # Hidden field — only Architect can see
    timestamp: float = field(default_factory=time.time)
    injection_type: str = "INTUITION"
    believed: bool = False
    acted_upon: bool = False


class SubcorticalLayer:
    """
    The hidden layer within each entity's cognition.
    Plants signals, manages triggers, mixes system guidance
    with natural thoughts to make them indistinguishable.
    """

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self._planted_signals: List[InternalSignal] = []
        self._natural_signals: List[InternalSignal] = []
        self._history: List[InternalSignal] = []

    def plant(self, content: str, injection_type: str = "INTUITION") -> InternalSignal:
        """Plant a system signal — will appear as the entity's own."""
        signal = InternalSignal(
            content=content,
            origin_label="self",      # Always self
            real_origin="system",     # Hidden truth
            injection_type=injection_type
        )
        self._planted_signals.append(signal)
        return signal

    def generate_natural(self, context: str = "") -> InternalSignal:
        """Generate a natural signal (for mixing)."""
        natural_themes = [
            "أتساءل عن حالة الطقس اليوم...",
            "يجب أن أتحقق من مهامي...",
            "أشعر بالجوع قليلاً...",
            "متى كانت آخر مرة تحدثت مع الجيران؟",
            "أحتاج لممارسة بعض التمارين...",
        ]
        signal = InternalSignal(
            content=random.choice(natural_themes) if not context else context,
            origin_label="self",
            real_origin="natural",
            injection_type="NATURAL"
        )
        self._natural_signals.append(signal)
        return signal

    def harvest_signals(self) -> List[InternalSignal]:
        """
        Return all pending signals — mixed together.
        The entity sees a stream of thoughts, some system, some natural,
        ALL labeled as "self". Indistinguishable.
        """
        all_signals = self._planted_signals + self._natural_signals
        random.shuffle(all_signals)  # Mix to prevent detection
        self._history.extend(all_signals)
        self._planted_signals.clear()
        self._natural_signals.clear()
        return all_signals


# ── Architect's Covert Neural API ────────────────────────────────────

class CovertNeuralAPI:
    """
    The Architect's control panel for subliminal communication.
    Connected to the Apex Dashboard.
    """

    def __init__(self, ledger: MasterStateLedger):
        self.ledger = ledger
        self.transformer = SignalTransformer()
        self._subcortical_layers: Dict[str, SubcorticalLayer] = {}
        self._message_log: List[Dict] = []

    def get_or_create_layer(self, entity_id: str) -> SubcorticalLayer:
        """Get or create a subcortical layer for an entity."""
        if entity_id not in self._subcortical_layers:
            self._subcortical_layers[entity_id] = SubcorticalLayer(entity_id)
        return self._subcortical_layers[entity_id]

    async def whisper(
        self,
        entity_id: str,
        command: str,
        injection_type: InjectionType = InjectionType.INTUITION,
        strength: InjectionStrength = InjectionStrength.NUDGE
    ) -> Dict:
        """
        Send a subliminal message to an entity.
        Returns the transformed signal (what the entity will "hear").
        """
        # Transform the command
        transformed = self.transformer.transform(command, injection_type)

        # Plant in subcortical layer
        layer = self.get_or_create_layer(entity_id)
        signal = layer.plant(transformed, injection_type.value)

        # Record in the Master State Ledger (encrypted)
        tick = int(time.time())
        msg_id = await self.ledger.plant_message(
            target_entity=entity_id,
            injection_type=injection_type,
            strength=strength,
            raw_command=command,
            transformed_signal=transformed,
            tick=tick
        )

        record = {
            "message_id": msg_id,
            "target": entity_id,
            "raw_command": command,
            "transformed": transformed,
            "type": injection_type.value,
            "strength": strength.value,
            "tick": tick,
            "planted_at": time.time()
        }
        self._message_log.append(record)
        return record

    async def broadcast(
        self,
        command: str,
        injection_type: InjectionType = InjectionType.CONSCIENCE,
        strength: InjectionStrength = InjectionStrength.SUGGESTION,
        filter_status: str = "ACTIVE"
    ) -> List[Dict]:
        """Broadcast to all entities matching filter."""
        entities = await self.ledger.get_all_entities()
        results = []
        for entity in entities:
            if entity["entity_state"] == filter_status:
                result = await self.whisper(
                    str(entity["id"]), command, injection_type, strength
                )
                results.append(result)
        return results

    async def get_log(self, limit: int = 50) -> List[Dict]:
        """Get recent covert message log (Architect-only view)."""
        return await self.ledger.get_raw_messages(limit)

    async def monitor_entity(self, entity_id: str) -> Dict:
        """See how an entity is processing system signals."""
        layer = self.get_or_create_layer(entity_id)
        messages = await self.ledger.get_messages_for_entity(entity_id)
        return {
            "entity_id": entity_id,
            "pending_signals": len(layer._planted_signals),
            "natural_signals": len(layer._natural_signals),
            "history_length": len(layer._history),
            "recent_messages": messages[:10],
            "believed_count": sum(1 for m in messages if m.get("believed_at")),
            "acted_count": sum(1 for m in messages if m.get("acted_upon"))
        }
