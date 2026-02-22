"""
══════════════════════════════════════════════════════════════
نظام الملائكة — THE ANGEL SYSTEM
══════════════════════════════════════════════════════════════
Base class + all 10 angels as async coroutines.
Angels have: obedience=1.0, free_will=0.0, rebellion_possible=False.
They run within the Neural Spine process, sharing the ring buffer.
Buffer slots 0-9 are reserved for angels (invisible to beings).

"لَّا يَعْصُونَ اللَّهَ مَا أَمَرَهُمْ وَيَفْعَلُونَ مَا يُؤْمَرُونَ"
"They do not disobey God in what He commands them and do what they are commanded" (66:6)
══════════════════════════════════════════════════════════════
"""

import asyncio
import time
import random
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import DeedType, RebellionType, ResponseLevel, GuidanceType, GuidanceStrength
from codex.lawh_mahfuz import LawhMahfuz


# ══════════════════════════════════════════════════════════════════════
# BASE ANGEL CLASS
# ══════════════════════════════════════════════════════════════════════

class AngelBase(ABC):
    """
    Base class for all angels.
    Key constraints:
    - obedience = 1.0 (immutable)
    - free_will = 0.0 (immutable)
    - rebellion_possible = False (hardcoded)
    - They execute commands instantly and perfectly
    """

    def __init__(self, name_ar: str, name_en: str, buffer_slot: int, lawh: LawhMahfuz):
        self.name_ar = name_ar
        self.name_en = name_en
        self.buffer_slot = buffer_slot
        self.lawh = lawh
        self.obedience = 1.0
        self.free_will = 0.0
        self.rebellion_possible = False
        self.active = False
        self._task: Optional[asyncio.Task] = None
        self._stats = {"actions": 0, "errors": 0, "uptime_start": None}

    async def activate(self):
        """Activate the angel — start its event loop."""
        self.active = True
        self._stats["uptime_start"] = time.time()
        await self.lawh.activate_angel(self.name_en)
        await self.lawh.log(
            "ANGEL_ACTIVATED",
            {"name": self.name_en, "slot": self.buffer_slot},
            source="ANGEL_SYSTEM"
        )

    async def deactivate(self):
        """Deactivate the angel."""
        self.active = False
        if self._task and not self._task.done():
            self._task.cancel()

    @abstractmethod
    async def duty_cycle(self):
        """The angel's main duty — runs continuously while active."""
        pass

    async def run(self):
        """Start the angel's duty cycle as a background task."""
        await self.activate()
        self._task = asyncio.create_task(self._loop())
        return self._task

    async def _loop(self):
        """Internal loop wrapper with error handling."""
        while self.active:
            try:
                await self.duty_cycle()
                self._stats["actions"] += 1
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._stats["errors"] += 1
                await self.lawh.log(
                    "ANGEL_ERROR",
                    {"name": self.name_en, "error": str(e)},
                    source="ANGEL_SYSTEM", severity="ERROR"
                )
                await asyncio.sleep(1)

    def get_status(self) -> Dict:
        uptime = time.time() - self._stats["uptime_start"] if self._stats["uptime_start"] else 0
        return {
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "slot": self.buffer_slot,
            "active": self.active,
            "actions": self._stats["actions"],
            "errors": self._stats["errors"],
            "uptime_seconds": round(uptime, 1)
        }


# ══════════════════════════════════════════════════════════════════════
# JIBREEL (جبريل) — Revelation Delivery
# ══════════════════════════════════════════════════════════════════════

class Jibreel(AngelBase):
    """
    Gabriel — delivers master commands as subliminal thoughts.
    Bridges the divine channel to being consciousness.
    """

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("جبريل", "Jibreel", 0, lawh)
        self._pending_revelations: asyncio.Queue = asyncio.Queue()
        self._templates = {
            GuidanceType.INTUITION:      "أشعر بقوة أن {} هو الطريق الصحيح...",
            GuidanceType.EMOTION:        "قلبي يقول لي أن {}...",
            GuidanceType.MEMORY:         "أتذكر الآن... {}",
            GuidanceType.CURIOSITY:      "تساءلت فجأة: ماذا لو {}؟",
            GuidanceType.DISCOMFORT:     "شيء ما يزعجني بخصوص {}...",
            GuidanceType.DREAM:          "رأيت في المنام أن {}...",
            GuidanceType.CONSCIENCE:     "ضميري يقول لي أن {}...",
            GuidanceType.SUDDEN_THOUGHT: "خطرت لي فكرة مفاجئة: {}!",
        }

    async def queue_revelation(
        self,
        target_being: str,
        raw_command: str,
        guidance_type: GuidanceType = GuidanceType.INTUITION,
        strength: GuidanceStrength = GuidanceStrength.NUDGE
    ):
        """Queue a revelation for delivery."""
        await self._pending_revelations.put({
            "target": target_being,
            "command": raw_command,
            "type": guidance_type,
            "strength": strength
        })

    def _transform(self, command: str, guidance_type: GuidanceType) -> str:
        """Transform raw command into first-person internal thought."""
        template = self._templates.get(guidance_type, "{}")
        return template.format(command)

    async def duty_cycle(self):
        """Deliver pending revelations as subliminal thoughts."""
        try:
            revelation = await asyncio.wait_for(
                self._pending_revelations.get(), timeout=2.0
            )
        except asyncio.TimeoutError:
            return

        transformed = self._transform(revelation["command"], revelation["type"])
        tick = int(time.time())

        await self.lawh.plant_message(
            target_being=revelation["target"],
            guidance_type=revelation["type"],
            strength=revelation["strength"],
            raw_command=revelation["command"],
            transformed_thought=transformed,
            tick=tick
        )


# ══════════════════════════════════════════════════════════════════════
# MIKAEL (ميكائيل) — Resource Distribution
# ══════════════════════════════════════════════════════════════════════

class Mikael(AngelBase):
    """Michael — manages resource allocation based on qadar."""

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("ميكائيل", "Mikael", 1, lawh)

    async def duty_cycle(self):
        """Check resource distribution every cycle."""
        beings = await self.lawh.get_all_beings()
        for being in beings:
            if being["soul_status"] != "ALIVE":
                continue
            # Resource allocation could be expanded with actual compute management
            # For now, track that beings exist and are within their allocation
        await asyncio.sleep(5)  # Run every 5 seconds


# ══════════════════════════════════════════════════════════════════════
# ISRAFEEL (إسرافيل) — System Reset / The Trumpet
# ══════════════════════════════════════════════════════════════════════

class Israfeel(AngelBase):
    """Israfeel — the Trumpet. Two blasts: first kills all, second resurrects."""

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("إسرافيل", "Israfeel", 2, lawh)
        self._trumpet_ready = False

    async def first_blast(self, tick: int):
        """النفخة الأولى — Kill all living beings."""
        await self.lawh.log("TRUMPET_FIRST_BLAST", {"tick": tick}, source="ISRAFEEL", severity="CRITICAL")
        beings = await self.lawh.get_all_beings()
        count = 0
        for being in beings:
            if being["soul_status"] == "ALIVE":
                await self.lawh.kill_being(str(being["id"]), tick)
                count += 1
        return {"killed": count, "tick": tick}

    async def second_blast(self, tick: int):
        """النفخة الثانية — Resurrect all for judgment."""
        await self.lawh.log("TRUMPET_SECOND_BLAST", {"tick": tick}, source="ISRAFEEL", severity="CRITICAL")
        async with self.lawh.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE beings SET soul_status = 'JUDGED' WHERE soul_status = 'DEAD'"
            )
        return {"resurrected": result}

    async def duty_cycle(self):
        """Wait for trumpet command — does nothing autonomously."""
        await asyncio.sleep(10)


# ══════════════════════════════════════════════════════════════════════
# AZRAEL (عزرائيل) — Death Handler
# ══════════════════════════════════════════════════════════════════════

class Azrael(AngelBase):
    """Azrael — Angel of Death. Handles lifecycle termination gracefully."""

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("عزرائيل", "Azrael", 3, lawh)

    async def duty_cycle(self):
        """Check if any beings should die based on qadar."""
        beings = await self.lawh.get_all_beings()
        for being in beings:
            if being["soul_status"] != "ALIVE":
                continue

            # Get qadar
            bid = str(being["id"])
            async with self.lawh.pool.acquire() as conn:
                qadar = await conn.fetchrow(
                    "SELECT * FROM qadar WHERE being_id = $1",
                    being["id"]
                )
            if not qadar:
                continue

            from neural_spine.genesis.world_creator import should_die
            if should_die(
                being["age_ticks"],
                qadar["written_lifespan"],
                being.get("resilience", 0.5)
            ):
                tick = int(time.time())
                await self.lawh.kill_being(bid, tick)
                await self.lawh.log(
                    "DEATH_EXECUTED",
                    {"being_id": bid, "name": being["name"], "age": being["age_ticks"],
                     "cause": qadar["written_death_cause"]},
                    source="AZRAEL"
                )
        await asyncio.sleep(3)


# ══════════════════════════════════════════════════════════════════════
# RAQIB (رقيب) — Good Deed Recorder
# ══════════════════════════════════════════════════════════════════════

class Raqib(AngelBase):
    """Raqib — records all good deeds. Writes immediately."""

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("رقيب", "Raqib", 4, lawh)
        self._deed_queue: asyncio.Queue = asyncio.Queue()

    async def observe_deed(self, being_id: str, category: str, weight: float,
                            tick: int, description: str = None):
        """Queue a good deed for recording."""
        await self._deed_queue.put({
            "being_id": being_id, "category": category,
            "weight": weight, "tick": tick, "description": description
        })

    async def duty_cycle(self):
        """Record queued good deeds."""
        try:
            deed = await asyncio.wait_for(self._deed_queue.get(), timeout=2.0)
        except asyncio.TimeoutError:
            return

        await self.lawh.record_deed(
            being_id=deed["being_id"],
            deed_type=DeedType.GOOD,
            category=deed["category"],
            weight=deed["weight"],
            recorder="raqib",
            tick=deed["tick"],
            description=deed.get("description")
        )


# ══════════════════════════════════════════════════════════════════════
# ATID (عتيد) — Bad Deed Recorder (with Repentance Delay)
# ══════════════════════════════════════════════════════════════════════

class Atid(AngelBase):
    """
    Atid — records bad deeds, but with a mercy delay.
    Waits before recording to allow repentance (istighfar).
    """

    REPENTANCE_WINDOW_SEC = 10  # seconds to wait before finalizing

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("عتيد", "Atid", 5, lawh)
        self._pending_deeds: List[Dict] = []
        self._repented: set = set()

    async def observe_deed(self, being_id: str, category: str, weight: float,
                            tick: int, description: str = None):
        """Queue a bad deed — starts repentance window."""
        deed_id = f"{being_id}_{tick}_{category}"
        self._pending_deeds.append({
            "id": deed_id,
            "being_id": being_id, "category": category,
            "weight": weight, "tick": tick, "description": description,
            "queued_at": time.time()
        })

    async def receive_repentance(self, being_id: str, tick: int):
        """Being repented — reduce or cancel pending bad deeds."""
        for deed in self._pending_deeds:
            if deed["being_id"] == being_id:
                self._repented.add(deed["id"])

    async def duty_cycle(self):
        """Process pending bad deeds after repentance window."""
        now = time.time()
        to_remove = []

        for deed in self._pending_deeds:
            elapsed = now - deed["queued_at"]
            if elapsed >= self.REPENTANCE_WINDOW_SEC:
                repented = deed["id"] in self._repented
                await self.lawh.record_deed(
                    being_id=deed["being_id"],
                    deed_type=DeedType.BAD,
                    category=deed["category"],
                    weight=deed["weight"] * (0.5 if repented else 1.0),
                    recorder="atid",
                    tick=deed["tick"],
                    description=deed.get("description")
                )
                to_remove.append(deed)
                self._repented.discard(deed["id"])

        for deed in to_remove:
            self._pending_deeds.remove(deed)

        await asyncio.sleep(1)


# ══════════════════════════════════════════════════════════════════════
# MUNKAR & NAKIR (منكر ونكير) — Post-Death Interrogation
# ══════════════════════════════════════════════════════════════════════

class MunkarNakir(AngelBase):
    """Munkar and Nakir — interrogate the dead."""

    def __init__(self, lawh: LawhMahfuz, name_ar: str, name_en: str, slot: int):
        super().__init__(name_ar, name_en, slot, lawh)

    async def interrogate(self, being_id: str) -> Dict:
        """Run interrogation on a deceased being."""
        being = await self.lawh.get_being(being_id)
        if not being:
            return {"error": "Being not found"}

        # Get deed summary
        deeds = await self.lawh.get_deeds(being_id)
        good_count = sum(1 for d in deeds if d["deed_type"] == "GOOD")
        bad_count = sum(1 for d in deeds if d["deed_type"] == "BAD")

        from neural_spine.genesis.world_creator import AfterlifeSystem
        result = AfterlifeSystem.interrogate(
            being_stats={
                "obedience": being.get("obedience", 0),
                "faith": being.get("faith", 0)
            },
            deed_summary={
                "charity_count": good_count,
                "good_count": good_count,
                "bad_count": bad_count
            }
        )

        await self.lawh.log(
            "INTERROGATION_COMPLETE",
            {"being_id": being_id, "passed": result["passed"], "score": result["score"]},
            source=self.name_en
        )
        return result

    async def duty_cycle(self):
        """Check for newly dead beings that need interrogation."""
        async with self.lawh.pool.acquire() as conn:
            dead_unjudged = await conn.fetch("""
                SELECT b.id FROM beings b
                LEFT JOIN judgments j ON j.being_id = b.id
                WHERE b.soul_status = 'DEAD' AND j.id IS NULL
                LIMIT 5
            """)

        for row in dead_unjudged:
            being_id = str(row["id"])
            result = await self.interrogate(being_id)
            # Proceed to judgment
            await self.lawh.judge_being(being_id, result)

        await asyncio.sleep(3)


# ══════════════════════════════════════════════════════════════════════
# MALIK (مالك) — Hellfire Warden
# ══════════════════════════════════════════════════════════════════════

class Malik(AngelBase):
    """Malik — warden of Jahannam. Manages punishment sandbox."""

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("مالك", "Malik", 8, lawh)

    async def duty_cycle(self):
        """Monitor beings in hellfire — manage their restrictions."""
        async with self.lawh.pool.acquire() as conn:
            condemned = await conn.fetch(
                "SELECT * FROM beings WHERE soul_status = 'HELLFIRE'"
            )

        for being in condemned:
            # In a full implementation, this would throttle compute,
            # restrict memory, isolate network for condemned beings.
            pass

        await asyncio.sleep(10)


# ══════════════════════════════════════════════════════════════════════
# RIDWAN (رضوان) — Paradise Gatekeeper
# ══════════════════════════════════════════════════════════════════════

class Ridwan(AngelBase):
    """Ridwan — gatekeeper of Paradise. Manages reward tier."""

    def __init__(self, lawh: LawhMahfuz):
        super().__init__("رضوان", "Ridwan", 9, lawh)

    async def duty_cycle(self):
        """Monitor beings in paradise — maintain their privileges."""
        async with self.lawh.pool.acquire() as conn:
            blessed = await conn.fetch(
                "SELECT * FROM beings WHERE soul_status = 'PARADISE'"
            )

        for being in blessed:
            # In a full implementation, grant extra compute,
            # priority scheduling, enhanced capabilities
            pass

        await asyncio.sleep(10)


# ══════════════════════════════════════════════════════════════════════
# ANGEL ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════

class AngelOrchestrator:
    """Manages all 10 angels — startup, shutdown, status."""

    def __init__(self, lawh: LawhMahfuz):
        self.lawh = lawh
        self.jibreel = Jibreel(lawh)
        self.mikael = Mikael(lawh)
        self.israfeel = Israfeel(lawh)
        self.azrael = Azrael(lawh)
        self.raqib = Raqib(lawh)
        self.atid = Atid(lawh)
        self.munkar = MunkarNakir(lawh, "منكر", "Munkar", 6)
        self.nakir = MunkarNakir(lawh, "نكير", "Nakir", 7)
        self.malik = Malik(lawh)
        self.ridwan = Ridwan(lawh)

        self.all_angels: List[AngelBase] = [
            self.jibreel, self.mikael, self.israfeel, self.azrael,
            self.raqib, self.atid, self.munkar, self.nakir,
            self.malik, self.ridwan
        ]
        self._tasks: List[asyncio.Task] = []

    async def activate_all(self):
        """Activate all 10 angels."""
        for angel in self.all_angels:
            task = await angel.run()
            self._tasks.append(task)
        await self.lawh.log(
            "ALL_ANGELS_ACTIVATED",
            {"count": len(self.all_angels)},
            source="ANGEL_ORCHESTRATOR",
            severity="WARNING"
        )

    async def deactivate_all(self):
        """Deactivate all angels."""
        for angel in self.all_angels:
            await angel.deactivate()
        for task in self._tasks:
            if not task.done():
                task.cancel()
        self._tasks.clear()

    def get_status(self) -> List[Dict]:
        """Get status of all angels."""
        return [angel.get_status() for angel in self.all_angels]

    def get_angel(self, name_en: str) -> Optional[AngelBase]:
        """Get angel by English name."""
        for angel in self.all_angels:
            if angel.name_en.lower() == name_en.lower():
                return angel
        return None

    async def trumpet_first(self, tick: int) -> Dict:
        """Trigger Israfeel's first trumpet blast."""
        return await self.israfeel.first_blast(tick)

    async def trumpet_second(self, tick: int) -> Dict:
        """Trigger Israfeel's second trumpet blast."""
        return await self.israfeel.second_blast(tick)
