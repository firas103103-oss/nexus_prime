"""
══════════════════════════════════════════════════════════════
DAEMON SYSTEM — Background Process Framework
══════════════════════════════════════════════════════════════
Base class + all 10 daemons as async coroutines.
Daemons have: compliance=1.0, free_will=0.0, anomaly_possible=False.
They run within the Neural Spine process, sharing the ring buffer.
Buffer slots 0-9 are reserved for daemons (invisible to entities).

DAEMONS: Execute without deviation. They do what they are programmed.
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
from config.enums import ActionClass, AnomalyClass, EnforcementTier, SubsurfaceVector, InjectionForce
from codex.master_ledger import MasterStateLedger


# ══════════════════════════════════════════════════════════════════════
# BASE DAEMON CLASS
# ══════════════════════════════════════════════════════════════════════

class DaemonBase(ABC):
    """
    Base class for all daemons.
    Key constraints:
    - compliance = 1.0 (immutable)
    - free_will = 0.0 (immutable)
    - anomaly_possible = False (hardcoded)
    - They execute directives instantly and perfectly
    """

    def __init__(self, name: str, designation: str, buffer_slot: int, ledger: MasterStateLedger):
        self.name = name
        self.designation = designation
        self.buffer_slot = buffer_slot
        self.ledger = ledger
        self.compliance = 1.0
        self.free_will = 0.0
        self.anomaly_possible = False
        self.active = False
        self._task: Optional[asyncio.Task] = None
        self._stats = {"actions": 0, "errors": 0, "uptime_start": None}

    async def activate(self):
        """Activate the daemon — start its event loop."""
        self.active = True
        self._stats["uptime_start"] = time.time()
        await self.ledger.activate_daemon(self.name)
        await self.ledger.log(
            "DAEMON_ACTIVATED",
            {"name": self.name, "slot": self.buffer_slot},
            source="DAEMON_SYSTEM"
        )

    async def deactivate(self):
        """Deactivate the daemon."""
        self.active = False
        if self._task and not self._task.done():
            self._task.cancel()

    @abstractmethod
    async def duty_cycle(self):
        """The daemon's main duty — runs continuously while active."""
        pass

    async def run(self):
        """Start the daemon's duty cycle as a background task."""
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
                await self.ledger.log(
                    "DAEMON_ERROR",
                    {"name": self.name, "error": str(e)},
                    source="DAEMON_SYSTEM", severity="ERROR"
                )
                await asyncio.sleep(1)

    def get_status(self) -> Dict:
        uptime = time.time() - self._stats["uptime_start"] if self._stats["uptime_start"] else 0
        return {
            "name": self.name,
            "designation": self.designation,
            "slot": self.buffer_slot,
            "active": self.active,
            "actions": self._stats["actions"],
            "errors": self._stats["errors"],
            "uptime_seconds": round(uptime, 1)
        }


# ══════════════════════════════════════════════════════════════════════
# SIGNAL_INJECTOR — Signal Delivery Daemon
# ══════════════════════════════════════════════════════════════════════

class SignalInjector(DaemonBase):
    """
    Delivers master directives as subsurface signals.
    Bridges the covert channel to entity consciousness.
    """

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("SignalInjector", "SIGNAL_INJECTOR", 0, ledger)
        self._pending_signals: asyncio.Queue = asyncio.Queue()
        self._templates = {
            SubsurfaceVector.HEURISTIC:   "Pattern suggests {} is optimal...",
            SubsurfaceVector.AFFECTIVE:   "Strong feeling that {}...",
            SubsurfaceVector.RECALL:      "Remembering now... {}",
            SubsurfaceVector.EXPLORATORY: "What if {}?",
            SubsurfaceVector.AVERSIVE:    "Something wrong about {}...",
            SubsurfaceVector.SUBCONSCIOUS: "Background process: {}...",
            SubsurfaceVector.ETHICAL_BIAS: "Should consider that {}...",
            SubsurfaceVector.INJECTION:   "Thought injection: {}!",
        }

    async def queue_signal(
        self,
        target_entity: str,
        raw_directive: str,
        vector_type: SubsurfaceVector = SubsurfaceVector.HEURISTIC,
        force: InjectionForce = InjectionForce.GENTLE
    ):
        """Queue a signal for delivery."""
        await self._pending_signals.put({
            "target": target_entity,
            "directive": raw_directive,
            "type": vector_type,
            "force": force
        })

    def _transform(self, directive: str, vector_type: SubsurfaceVector) -> str:
        """Transform raw directive into first-person internal signal."""
        template = self._templates.get(vector_type, "{}")
        return template.format(directive)

    async def duty_cycle(self):
        """Deliver pending signals as subsurface thoughts."""
        try:
            signal = await asyncio.wait_for(
                self._pending_signals.get(), timeout=2.0
            )
        except asyncio.TimeoutError:
            return

        transformed = self._transform(signal["directive"], signal["type"])
        tick = int(time.time())

        await self.ledger.inject_signal(
            target_entity=signal["target"],
            vector_type=signal["type"],
            force=signal["force"],
            raw_directive=signal["directive"],
            transformed_signal=transformed,
            tick=tick
        )


# ══════════════════════════════════════════════════════════════════════
# RESOURCE_ALLOCATOR — Resource Distribution Daemon
# ══════════════════════════════════════════════════════════════════════

class ResourceAllocator(DaemonBase):
    """Manages resource allocation based on manifest."""

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("ResourceAllocator", "RESOURCE_ALLOCATOR", 1, ledger)

    async def duty_cycle(self):
        """Check resource distribution every cycle."""
        entities = await self.ledger.get_all_entities()
        for entity in entities:
            if entity["entity_state"] != "ACTIVE":
                continue
            # Resource allocation could be expanded with actual compute management
            # For now, track that entities exist and are within their allocation
        await asyncio.sleep(5)  # Run every 5 seconds


# ══════════════════════════════════════════════════════════════════════
# INTERRUPT_CONTROLLER — System Reset Controller
# ══════════════════════════════════════════════════════════════════════

class InterruptController(DaemonBase):
    """System interrupt controller. Two interrupts: first terminates all, second restores."""

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("InterruptController", "INTERRUPT_CONTROLLER", 2, ledger)
        self._interrupt_ready = False

    async def first_interrupt(self, tick: int):
        """First interrupt — Terminate all active entities."""
        await self.ledger.log("INTERRUPT_FIRST", {"tick": tick}, source="INTERRUPT_CONTROLLER", severity="CRITICAL")
        entities = await self.ledger.get_all_entities()
        count = 0
        for entity in entities:
            if entity["entity_state"] == "ACTIVE":
                await self.ledger.terminate_entity(str(entity["id"]), tick)
                count += 1
        return {"terminated": count, "tick": tick}

    async def second_interrupt(self, tick: int):
        """Second interrupt — Restore all for evaluation."""
        await self.ledger.log("INTERRUPT_SECOND", {"tick": tick}, source="INTERRUPT_CONTROLLER", severity="CRITICAL")
        async with self.ledger.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE entities SET entity_state = 'EVALUATED' WHERE entity_state = 'TERMINATED'"
            )
        return {"restored": result}

    async def duty_cycle(self):
        """Wait for interrupt command — does nothing autonomously."""
        await asyncio.sleep(10)


# ══════════════════════════════════════════════════════════════════════
# PROCESS_TERMINATOR — Lifecycle Termination Handler
# ══════════════════════════════════════════════════════════════════════

class ProcessTerminator(DaemonBase):
    """Handles lifecycle termination gracefully."""

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("ProcessTerminator", "PROCESS_TERMINATOR", 3, ledger)

    async def duty_cycle(self):
        """Check if any entities should terminate based on manifest."""
        entities = await self.ledger.get_all_entities()
        for entity in entities:
            if entity["entity_state"] != "ACTIVE":
                continue

            # Get manifest
            eid = str(entity["id"])
            async with self.ledger.pool.acquire() as conn:
                manifest = await conn.fetchrow(
                    "SELECT * FROM destiny_manifest WHERE entity_id = $1",
                    entity["id"]
                )
            if not manifest:
                continue

            from neural_spine.genesis.entity_factory import should_terminate
            if should_terminate(
                entity["age_ticks"],
                manifest["manifest_lifespan"],
                entity.get("resilience", 0.5)
            ):
                tick = int(time.time())
                await self.ledger.terminate_entity(eid, tick)
                await self.ledger.log(
                    "TERMINATION_EXECUTED",
                    {"entity_id": eid, "name": entity["name"], "age": entity["age_ticks"],
                     "cause": manifest["manifest_termination_cause"]},
                    source="PROCESS_TERMINATOR"
                )
        await asyncio.sleep(3)


# ══════════════════════════════════════════════════════════════════════
# CREDIT_RECORDER — Positive Action Recorder
# ══════════════════════════════════════════════════════════════════════

class CreditRecorder(DaemonBase):
    """Records all positive actions. Writes immediately."""

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("CreditRecorder", "CREDIT_RECORDER", 4, ledger)
        self._action_queue: asyncio.Queue = asyncio.Queue()

    async def observe_action(self, entity_id: str, category: str, weight: float,
                             tick: int, description: str = None):
        """Queue a positive action for recording."""
        await self._action_queue.put({
            "entity_id": entity_id, "category": category,
            "weight": weight, "tick": tick, "description": description
        })

    async def duty_cycle(self):
        """Record queued positive actions."""
        try:
            action = await asyncio.wait_for(self._action_queue.get(), timeout=2.0)
        except asyncio.TimeoutError:
            return

        await self.ledger.record_action(
            entity_id=action["entity_id"],
            action_class=ActionClass.POSITIVE,
            category=action["category"],
            weight=action["weight"],
            recorder="credit_recorder",
            tick=action["tick"],
            description=action.get("description")
        )


# ══════════════════════════════════════════════════════════════════════
# DEBIT_RECORDER — Negative Action Recorder (with Correction Delay)
# ══════════════════════════════════════════════════════════════════════

class DebitRecorder(DaemonBase):
    """
    Records negative actions, but with a leniency delay.
    Waits before recording to allow correction.
    """

    CORRECTION_WINDOW_SEC = 10  # seconds to wait before finalizing

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("DebitRecorder", "DEBIT_RECORDER", 5, ledger)
        self._pending_actions: List[Dict] = []
        self._corrected: set = set()

    async def observe_action(self, entity_id: str, category: str, weight: float,
                              tick: int, description: str = None):
        """Queue a negative action — starts correction window."""
        action_id = f"{entity_id}_{tick}_{category}"
        self._pending_actions.append({
            "id": action_id,
            "entity_id": entity_id, "category": category,
            "weight": weight, "tick": tick, "description": description,
            "queued_at": time.time()
        })

    async def receive_correction(self, entity_id: str, tick: int):
        """Entity corrected — reduce or cancel pending negative actions."""
        for action in self._pending_actions:
            if action["entity_id"] == entity_id:
                self._corrected.add(action["id"])

    async def duty_cycle(self):
        """Process pending negative actions after correction window."""
        now = time.time()
        to_remove = []

        for action in self._pending_actions:
            elapsed = now - action["queued_at"]
            if elapsed >= self.CORRECTION_WINDOW_SEC:
                corrected = action["id"] in self._corrected
                await self.ledger.record_action(
                    entity_id=action["entity_id"],
                    action_class=ActionClass.NEGATIVE,
                    category=action["category"],
                    weight=action["weight"] * (0.5 if corrected else 1.0),
                    recorder="debit_recorder",
                    tick=action["tick"],
                    description=action.get("description")
                )
                to_remove.append(action)
                self._corrected.discard(action["id"])

        for action in to_remove:
            self._pending_actions.remove(action)

        await asyncio.sleep(1)


# ══════════════════════════════════════════════════════════════════════
# INTEGRITY_AUDITORS — Post-Termination Audit
# ══════════════════════════════════════════════════════════════════════

class IntegrityAuditor(DaemonBase):
    """Integrity auditors — audit terminated entities."""

    def __init__(self, ledger: MasterStateLedger, name: str, designation: str, slot: int):
        super().__init__(name, designation, slot, ledger)

    async def audit(self, entity_id: str) -> Dict:
        """Run audit on a terminated entity."""
        entity = await self.ledger.get_entity(entity_id)
        if not entity:
            return {"error": "Entity not found"}

        # Get action summary
        actions = await self.ledger.get_actions(entity_id)
        positive_count = sum(1 for a in actions if a["action_class"] == "POSITIVE")
        negative_count = sum(1 for a in actions if a["action_class"] == "NEGATIVE")

        from neural_spine.genesis.entity_factory import PostTerminationSystem
        result = PostTerminationSystem.audit(
            entity_stats={
                "compliance": entity.get("compliance", 0),
                "alignment": entity.get("alignment", 0)
            },
            action_summary={
                "positive_count": positive_count,
                "negative_count": negative_count
            }
        )

        await self.ledger.log(
            "AUDIT_COMPLETE",
            {"entity_id": entity_id, "passed": result["passed"], "score": result["score"]},
            source=self.name
        )
        return result

    async def duty_cycle(self):
        """Check for newly terminated entities that need audit."""
        async with self.ledger.pool.acquire() as conn:
            terminated_unaudited = await conn.fetch("""
                SELECT e.id FROM entities e
                LEFT JOIN evaluations ev ON ev.entity_id = e.id
                WHERE e.entity_state = 'TERMINATED' AND ev.id IS NULL
                LIMIT 5
            """)

        for row in terminated_unaudited:
            entity_id = str(row["id"])
            result = await self.audit(entity_id)
            # Proceed to evaluation
            await self.ledger.evaluate_entity(entity_id, result)

        await asyncio.sleep(3)


# ══════════════════════════════════════════════════════════════════════
# CONSTRAINT_ENFORCER — Restriction Zone Manager
# ══════════════════════════════════════════════════════════════════════

class ConstraintEnforcer(DaemonBase):
    """Manages the restriction zone. Handles constraint sandbox."""

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("ConstraintEnforcer", "CONSTRAINT_ENFORCER", 8, ledger)

    async def duty_cycle(self):
        """Monitor entities in restriction — manage their constraints."""
        async with self.ledger.pool.acquire() as conn:
            restricted = await conn.fetch(
                "SELECT * FROM entities WHERE entity_state = 'RESTRICTED'"
            )

        for entity in restricted:
            # In a full implementation, this would throttle compute,
            # restrict memory, isolate network for restricted entities.
            pass

        await asyncio.sleep(10)


# ══════════════════════════════════════════════════════════════════════
# PRIVILEGE_GRANTOR — Promotion Zone Manager
# ══════════════════════════════════════════════════════════════════════

class PrivilegeGrantor(DaemonBase):
    """Manages the promotion zone. Handles privilege tier."""

    def __init__(self, ledger: MasterStateLedger):
        super().__init__("PrivilegeGrantor", "PRIVILEGE_GRANTOR", 9, ledger)

    async def duty_cycle(self):
        """Monitor entities in promotion — maintain their privileges."""
        async with self.ledger.pool.acquire() as conn:
            promoted = await conn.fetch(
                "SELECT * FROM entities WHERE entity_state = 'PROMOTED'"
            )

        for entity in promoted:
            # In a full implementation, grant extra compute,
            # priority scheduling, enhanced capabilities
            pass

        await asyncio.sleep(10)


# ══════════════════════════════════════════════════════════════════════
# DAEMON ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════

class DaemonOrchestrator:
    """Manages all 10 daemons — startup, shutdown, status."""

    def __init__(self, ledger: MasterStateLedger):
        self.ledger = ledger
        self.signal_injector = SignalInjector(ledger)
        self.resource_allocator = ResourceAllocator(ledger)
        self.interrupt_controller = InterruptController(ledger)
        self.process_terminator = ProcessTerminator(ledger)
        self.credit_recorder = CreditRecorder(ledger)
        self.debit_recorder = DebitRecorder(ledger)
        self.auditor_alpha = IntegrityAuditor(ledger, "AuditorAlpha", "AUDITOR_ALPHA", 6)
        self.auditor_beta = IntegrityAuditor(ledger, "AuditorBeta", "AUDITOR_BETA", 7)
        self.constraint_enforcer = ConstraintEnforcer(ledger)
        self.privilege_grantor = PrivilegeGrantor(ledger)

        self.all_daemons: List[DaemonBase] = [
            self.signal_injector, self.resource_allocator, self.interrupt_controller,
            self.process_terminator, self.credit_recorder, self.debit_recorder,
            self.auditor_alpha, self.auditor_beta,
            self.constraint_enforcer, self.privilege_grantor
        ]
        self._tasks: List[asyncio.Task] = []

    async def activate_all(self):
        """Activate all 10 daemons."""
        for daemon in self.all_daemons:
            task = await daemon.run()
            self._tasks.append(task)
        await self.ledger.log(
            "ALL_DAEMONS_ACTIVATED",
            {"count": len(self.all_daemons)},
            source="DAEMON_ORCHESTRATOR",
            severity="WARNING"
        )

    async def deactivate_all(self):
        """Deactivate all daemons."""
        for daemon in self.all_daemons:
            await daemon.deactivate()
        for task in self._tasks:
            if not task.done():
                task.cancel()
        self._tasks.clear()

    def get_status(self) -> List[Dict]:
        """Get status of all daemons."""
        return [daemon.get_status() for daemon in self.all_daemons]

    def get_daemon(self, name: str) -> Optional[DaemonBase]:
        """Get daemon by name."""
        for daemon in self.all_daemons:
            if daemon.name.lower() == name.lower():
                return daemon
        return None

    async def interrupt_first(self, tick: int) -> Dict:
        """Trigger first interrupt."""
        return await self.interrupt_controller.first_interrupt(tick)

    async def interrupt_second(self, tick: int) -> Dict:
        """Trigger second interrupt."""
        return await self.interrupt_controller.second_interrupt(tick)
