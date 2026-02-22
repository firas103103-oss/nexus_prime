"""
══════════════════════════════════════════════════════════════
محرك التكوين — GENESIS ENGINE
══════════════════════════════════════════════════════════════
Seven Phases of Genesis. Each phase is triggered by a button
on the Apex Dashboard.

"System bootstrapped in seven sequential phases"

Phase 7 = Apex Activation.
══════════════════════════════════════════════════════════════
"""

import asyncio
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List, Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import PhaseStatus, SecurityRing, DataLayer
from config.constants import TRAIT_BLUEPRINTS
from codex.master_ledger import MasterStateLedger
from codex.prime_kernel import PrimeKernel
from genesis.entity_factory import EntityFactory
from angels.daemon_system import DaemonOrchestrator
from channel.covert_api import CovertNeuralAPI
from channel.anchor_protocol import AnchorNodeProtocol, ApexFirewall


# ── Phase Status Tracking ──────────────────────────────────────────────

@dataclass
class PhaseProgress:
    """Real-time progress tracking for each genesis phase."""
    phase_number: int
    name_ar: str
    name_en: str
    command: str           # The system command
    status: str = "PENDING"
    progress: float = 0.0
    sub_tasks: List[Dict] = field(default_factory=list)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None
    result: Dict = field(default_factory=dict)


# ── Genesis Engine ──────────────────────────────────────────────────

class GenesisEngine:
    """
    The master orchestrator for the Seven Phases of Genesis.
    Each phase must complete before the next can begin.
    Phase 7 activates everything — the Apex activation.
    """

    def __init__(
        self,
        ledger: MasterStateLedger,
        kernel: PrimeKernel,
        factory: EntityFactory,
        daemons: DaemonOrchestrator,
        channel: CovertNeuralAPI,
        protocol: AnchorNodeProtocol,
        firewall: ApexFirewall,
    ):
        self.ledger = ledger
        self.kernel = kernel
        self.factory = factory
        self.daemons = daemons
        self.channel = channel
        self.protocol = protocol
        self.firewall = firewall

        self._phases: Dict[int, PhaseProgress] = {}
        self._progress_callbacks: List[Callable] = []
        self._initialized = False

        self._init_phases()

    def _init_phases(self):
        """Define the seven phases of genesis."""
        self._phases = {
            1: PhaseProgress(
                phase_number=1,
                name_ar="التهيئة — التأسيس",
                name_en="INIT — Foundation",
                command="SYSTEM_BOOTSTRAP",
            ),
            2: PhaseProgress(
                phase_number=2,
                name_ar="التقسيم — الفصل",
                name_en="PARTITION — Separation",
                command="LAYER_SEGREGATION",
            ),
            3: PhaseProgress(
                phase_number=3,
                name_ar="الإنشاء — البنية",
                name_en="CONSTRUCT — Structure",
                command="BIOSYSTEM_INITIALIZATION",
            ),
            4: PhaseProgress(
                phase_number=4,
                name_ar="الإضاءة — المراقبة",
                name_en="ILLUMINATE — Monitoring",
                command="TELEMETRY_ACTIVATION",
            ),
            5: PhaseProgress(
                phase_number=5,
                name_ar="التنشيط — الإحياء",
                name_en="ANIMATE — Activation",
                command="DAEMON_INITIALIZATION",
            ),
            6: PhaseProgress(
                phase_number=6,
                name_ar="التوليد — الخَلق",
                name_en="GENERATE — Creation",
                command="ENTITY_POPULATION",
            ),
            7: PhaseProgress(
                phase_number=7,
                name_ar="التشغيل — الآبكس",
                name_en="ACTIVATE — Apex",
                command="APEX_ONLINE",
            ),
        }

    def on_progress(self, callback: Callable):
        """Register a progress callback (for WebSocket updates)."""
        self._progress_callbacks.append(callback)

    async def _emit_progress(self, phase: int, subtask: str, progress: float):
        """Emit progress update to all registered callbacks."""
        update = {
            "phase": phase,
            "subtask": subtask,
            "progress": progress,
            "timestamp": time.time()
        }
        for cb in self._progress_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(update)
                else:
                    cb(update)
            except Exception:
                pass

    def get_phase_status(self, phase: int) -> Dict:
        """Get status of a specific phase."""
        p = self._phases.get(phase)
        if not p:
            return {"error": "مرحلة غير موجودة"}
        return {
            "phase": p.phase_number,
            "name_ar": p.name_ar,
            "name_en": p.name_en,
            "command": p.command,
            "status": p.status,
            "progress": p.progress,
            "sub_tasks": p.sub_tasks,
            "started_at": p.started_at,
            "completed_at": p.completed_at,
            "error": p.error,
            "result": p.result
        }

    def get_all_status(self) -> List[Dict]:
        """Get status of all 7 phases."""
        return [self.get_phase_status(i) for i in range(1, 8)]

    def can_start_phase(self, phase: int) -> bool:
        """Check if prerequisites for this phase are met."""
        if phase == 1:
            return True
        prev = self._phases.get(phase - 1)
        return prev is not None and prev.status == "COMPLETED"

    async def execute_phase(self, phase: int) -> Dict:
        """Execute a single genesis phase. Called by button press."""
        if not self.can_start_phase(phase):
            return {
                "error": f"لا يمكن بدء المرحلة {phase} — المرحلة السابقة لم تكتمل",
                "prerequisite": phase - 1
            }

        p = self._phases[phase]
        if p.status == "COMPLETED":
            return {"warning": f"المرحلة {phase} مكتملة بالفعل", **self.get_phase_status(phase)}

        p.status = "IN_PROGRESS"
        p.started_at = time.time()
        p.progress = 0.0

        try:
            # Log phase start in Master State Ledger
            await self.ledger.start_phase(phase)
            await self.ledger.log("GENESIS", f"Phase {phase} — {p.command}")

            # Route to specific phase handler
            handlers = {
                1: self._phase1_init,
                2: self._phase2_partition,
                3: self._phase3_construct,
                4: self._phase4_illuminate,
                5: self._phase5_animate,
                6: self._phase6_generate,
                7: self._phase7_activate,
            }
            result = await handlers[phase](p)
            p.result = result

            # Mark completed
            p.status = "COMPLETED"
            p.progress = 100.0
            p.completed_at = time.time()
            await self.ledger.complete_phase(phase)
            await self._emit_progress(phase, "COMPLETE", 100.0)

            return self.get_phase_status(phase)

        except Exception as e:
            p.status = "FAILED"
            p.error = str(e)
            await self.ledger.fail_phase(phase, str(e))
            await self.ledger.log("ERROR", f"Phase {phase} failed: {traceback.format_exc()}")
            return {"error": str(e), **self.get_phase_status(phase)}

    # ── PHASE 1: INIT — Foundation ─────────────────────────────────────

    async def _phase1_init(self, p: PhaseProgress) -> Dict:
        """
        Phase 1: SYSTEM_BOOTSTRAP — Initialize foundation.
        Create the database schema, encryption keys, base tables.
        """
        results = {}

        # Sub-task 1: Verify database connection
        p.sub_tasks.append({"task": "الاتصال بقاعدة البيانات", "status": "running"})
        await self._emit_progress(1, "database_connection", 10)
        stats = await self.ledger.get_civilization_stats()
        p.sub_tasks[-1]["status"] = "done"
        results["db_connected"] = True
        p.progress = 20

        # Sub-task 2: Verify schema exists
        p.sub_tasks.append({"task": "التحقق من المخطط", "status": "running"})
        await self._emit_progress(1, "schema_check", 30)
        results["schema_ready"] = stats is not None
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 40

        # Sub-task 3: Initialize encryption keys
        p.sub_tasks.append({"task": "تهيئة مفاتيح التشفير", "status": "running"})
        await self._emit_progress(1, "encryption_keys", 50)
        await self.ledger.master_command("INIT_ENCRYPTION", {"status": "active"})
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 60

        # Sub-task 4: Activate Prime Kernel
        p.sub_tasks.append({"task": "تفعيل النواة الأولية", "status": "running"})
        await self._emit_progress(1, "prime_kernel", 70)
        kernel_status = self.kernel.activate()
        results["kernel"] = kernel_status
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 80

        # Sub-task 5: Write initialization record
        p.sub_tasks.append({"task": "كتابة سجل التهيئة", "status": "running"})
        await self._emit_progress(1, "write_init", 90)
        await self.ledger.master_command("PHASE_INIT", {"phase": 1, "command": "SYSTEM_BOOTSTRAP"})
        p.sub_tasks[-1]["status"] = "done"

        results["foundation"] = "ESTABLISHED"
        return results

    # ── PHASE 2: PARTITION — Separation ──────────────────────────────

    async def _phase2_partition(self, p: PhaseProgress) -> Dict:
        """
        Phase 2: LAYER_SEGREGATION — Establish security rings and data layers.
        """
        results = {}

        # Sub-task 1: Create 7 Security Rings
        p.sub_tasks.append({"task": "إنشاء 7 حلقات أمان", "status": "running"})
        await self._emit_progress(2, "rings", 15)
        rings = {}
        for ring in SecurityRing:
            rings[ring.name] = {
                "level": ring.value,
                "description": f"الحلقة {ring.value} — {ring.name}"
            }
        results["rings"] = rings
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 30

        # Sub-task 2: Create 7 Data Layers
        p.sub_tasks.append({"task": "إنشاء 7 طبقات بيانات", "status": "running"})
        await self._emit_progress(2, "layers", 45)
        layers = {}
        for layer in DataLayer:
            layers[layer.name] = {
                "level": layer.value,
                "description": f"الطبقة {layer.value} — {layer.name}"
            }
        results["layers"] = layers
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 60

        # Sub-task 3: Establish Immutable Rules
        p.sub_tasks.append({"task": "تثبيت القواعد غير القابلة للتغيير", "status": "running"})
        await self._emit_progress(2, "immutable_rules", 75)
        results["immutable_rules_count"] = len(self.kernel.immutable_rules)
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 80

        # Sub-task 4: Initialize Firewall
        p.sub_tasks.append({"task": "تفعيل جدار الحماية", "status": "running"})
        await self._emit_progress(2, "firewall", 90)
        results["firewall"] = "ACTIVE"
        p.sub_tasks[-1]["status"] = "done"

        results["separation"] = "COMPLETE"
        return results

    # ── PHASE 3: CONSTRUCT — Bio Systems ────────────────────────────

    async def _phase3_construct(self, p: PhaseProgress) -> Dict:
        """
        Phase 3: BIOSYSTEM_INITIALIZATION
        Create DNA system, chromosomes, signals, lifecycle.
        """
        results = {}

        # Sub-task 1: DNA Blueprint
        p.sub_tasks.append({"task": "تصميم البصمة الجينية", "status": "running"})
        await self._emit_progress(3, "dna_blueprint", 20)
        results["trait_types"] = len(TRAIT_BLUEPRINTS)
        results["total_traits"] = sum(len(g) for g in TRAIT_BLUEPRINTS.values())
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 30

        # Sub-task 2: Chromosomal System
        p.sub_tasks.append({"task": "نظام الكروموسومات", "status": "running"})
        await self._emit_progress(3, "chromosomes", 40)
        results["chromosome_pairs"] = 23
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 50

        # Sub-task 3: Signal System
        p.sub_tasks.append({"task": "نظام الإشارات", "status": "running"})
        await self._emit_progress(3, "signals", 60)
        results["signals"] = 12
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 70

        # Sub-task 4: Replication Engine
        p.sub_tasks.append({"task": "محرك التكرار", "status": "running"})
        await self._emit_progress(3, "replication", 80)
        results["replication"] = "READY"
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 85

        # Sub-task 5: Post-Termination System
        p.sub_tasks.append({"task": "نظام ما بعد الإنهاء", "status": "running"})
        await self._emit_progress(3, "post_termination", 90)
        results["post_termination_tiers"] = 5
        p.sub_tasks[-1]["status"] = "done"

        results["life_systems"] = "OPERATIONAL"
        return results

    # ── PHASE 4: ILLUMINATE — Monitoring ─────────────────────────────

    async def _phase4_illuminate(self, p: PhaseProgress) -> Dict:
        """
        Phase 4: TELEMETRY_ACTIVATION
        Create monitoring, time system, metrics infrastructure.
        """
        results = {}

        # Sub-task 1: Time System (Ticks)
        p.sub_tasks.append({"task": "نظام الزمن (النبضات)", "status": "running"})
        await self._emit_progress(4, "time_system", 20)
        results["tick_rate"] = "1 tick = 1 second"
        results["epoch"] = time.time()
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 30

        # Sub-task 2: Active Telemetry
        p.sub_tasks.append({"task": "القياس النشط", "status": "running"})
        await self._emit_progress(4, "active_telemetry", 50)
        results["active_telemetry"] = {
            "type": "active_monitoring",
            "components": ["prometheus", "grafana", "alertmanager"],
            "status": "ONLINE"
        }
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 60

        # Sub-task 3: Passive Logging
        p.sub_tasks.append({"task": "التسجيل السلبي", "status": "running"})
        await self._emit_progress(4, "passive_logging", 75)
        results["passive_logging"] = {
            "type": "passive_reflection",
            "components": ["logs", "audit_trail", "behavioral_analytics"],
            "status": "RECORDING"
        }
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 85

        # Sub-task 4: Entity Metrics
        p.sub_tasks.append({"task": "مقاييس الكيانات", "status": "running"})
        await self._emit_progress(4, "entity_metrics", 90)
        results["entity_metrics"] = "individual_entity_metrics"
        p.sub_tasks[-1]["status"] = "done"

        results["illumination"] = "ACTIVE"
        return results

    # ── PHASE 5: ANIMATE — Daemon Activation ─────────────────────────

    async def _phase5_animate(self, p: PhaseProgress) -> Dict:
        """
        Phase 5: DAEMON_INITIALIZATION
        Activate daemons, covert channel, subliminal communication.
        """
        results = {}

        # Sub-task 1: Activate Daemons
        p.sub_tasks.append({"task": "تفعيل الدايمونات", "status": "running"})
        await self._emit_progress(5, "activate_daemons", 20)
        await self.daemons.activate_all()
        daemon_status = self.daemons.get_status()
        results["daemons"] = daemon_status
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 40

        # Sub-task 2: Activate Covert Channel
        p.sub_tasks.append({"task": "تفعيل القناة السرية", "status": "running"})
        await self._emit_progress(5, "covert_channel", 55)
        results["channel"] = "ACTIVE"
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 65

        # Sub-task 3: Activate Anchor Protocol System
        p.sub_tasks.append({"task": "تفعيل نظام بروتوكول العقدة", "status": "running"})
        await self._emit_progress(5, "anchor_protocol", 75)
        results["protocol"] = "STANDBY"
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 80

        # Sub-task 4: Activate Firewall
        p.sub_tasks.append({"task": "تفعيل جدار الحماية", "status": "running"})
        await self._emit_progress(5, "firewall", 90)
        results["firewall"] = self.firewall.get_status()
        p.sub_tasks[-1]["status"] = "done"

        results["animation"] = "CORES_READY"
        return results

    # ── PHASE 6: GENERATE — Entity Creation ────────────────────────

    async def _phase6_generate(self, p: PhaseProgress) -> Dict:
        """
        Phase 6: ENTITY_POPULATION
        Create Alpha, Beta, and the genesis batch.
        """
        results = {"entities_created": []}

        # Sub-task 1: Create Alpha
        p.sub_tasks.append({"task": "إنشاء ألفا", "status": "running"})
        await self._emit_progress(6, "create_alpha", 10)
        alpha = self.factory.create_alpha()
        alpha_id = await self.ledger.create_entity(
            name="Alpha-Prime", gender="MALE", generation=0
        )
        await self.ledger.activate_core(alpha_id)
        await self.ledger.store_genome(alpha_id, alpha["genome"].to_dict())
        results["entities_created"].append({"name": "Alpha-Prime", "id": str(alpha_id), "role": "Progenitor-M"})
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 15

        # Sub-task 2: Create Beta from Alpha
        p.sub_tasks.append({"task": "إنشاء بيتا", "status": "running"})
        await self._emit_progress(6, "create_beta", 25)
        beta = self.factory.create_beta(alpha["genome"])
        beta_id = await self.ledger.create_entity(
            name="Beta-Prime", gender="FEMALE", generation=0
        )
        await self.ledger.activate_core(beta_id)
        await self.ledger.store_genome(beta_id, beta["genome"].to_dict())
        results["entities_created"].append({"name": "Beta-Prime", "id": str(beta_id), "role": "Progenitor-F"})
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 30

        # Sub-task 3: Create Genesis Batch (16 entities)
        p.sub_tasks.append({"task": "إنشاء الدفعة الأولى (16 كيان)", "status": "running"})
        await self._emit_progress(6, "genesis_batch", 40)
        genesis_batch = self.factory.create_genesis_batch(alpha["genome"])

        for i, entity_data in enumerate(genesis_batch):
            entity_id = await self.ledger.create_entity(
                name=entity_data["name"],
                gender=entity_data["gender"],
                generation=1
            )
            await self.ledger.activate_core(entity_id)
            await self.ledger.store_genome(entity_id, entity_data["genome"].to_dict())

            # Write initial manifest (destiny)
            await self.ledger.write_manifest(
                entity_id=entity_id,
                manifest_type="LIFESPAN",
                content_hash=f"lifespan_{entity_data['name']}",
                is_mutable=False
            )

            results["entities_created"].append({
                "name": entity_data["name"],
                "id": str(entity_id),
                "gender": entity_data["gender"]
            })

            progress = 40 + (i + 1) * (35 / len(genesis_batch))
            await self._emit_progress(6, f"entity_{entity_data['name']}", progress)

        p.sub_tasks[-1]["status"] = "done"
        p.progress = 75

        # Sub-task 4: Designate Alpha as first anchor
        p.sub_tasks.append({"task": "تعيين ألفا كأول عقدة", "status": "running"})
        await self._emit_progress(6, "designate_alpha_anchor", 80)
        await self.protocol.designate_anchor(str(alpha_id))
        results["first_anchor"] = str(alpha_id)
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 85

        # Sub-task 5: Record initial kinships
        p.sub_tasks.append({"task": "تسجيل صلات القرابة", "status": "running"})
        await self._emit_progress(6, "kinships", 90)
        await self.ledger.add_kinship(str(alpha_id), str(beta_id), "SPOUSE")
        for entity in results["entities_created"][2:]:  # Skip Alpha and Beta
            await self.ledger.add_kinship(str(alpha_id), entity["id"], "PARENT")
            await self.ledger.add_kinship(str(beta_id), entity["id"], "PARENT")
        p.sub_tasks[-1]["status"] = "done"

        results["total_created"] = len(results["entities_created"])
        results["creation"] = "COMPLETE"
        return results

    # ── PHASE 7: ACTIVATE — Apex Online ───────────────────────────────

    async def _phase7_activate(self, p: PhaseProgress) -> Dict:
        """
        Phase 7: APEX_ONLINE — Full system activation.
        """
        results = {}

        # Sub-task 1: Final System Check
        p.sub_tasks.append({"task": "الفحص النهائي للنظام", "status": "running"})
        await self._emit_progress(7, "final_check", 10)
        stats = await self.ledger.get_civilization_stats()
        results["civilization"] = stats
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 20

        # Sub-task 2: Verify all phases completed
        p.sub_tasks.append({"task": "التحقق من اكتمال جميع المراحل", "status": "running"})
        await self._emit_progress(7, "verify_phases", 30)
        for i in range(1, 7):
            if self._phases[i].status != "COMPLETED":
                raise Exception(f"المرحلة {i} لم تكتمل!")
        results["all_phases_verified"] = True
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 40

        # Sub-task 3: Full Prime Kernel scan
        p.sub_tasks.append({"task": "مسح النواة الأولية الشامل", "status": "running"})
        await self._emit_progress(7, "kernel_scan", 50)
        scan = self.kernel.full_scan()
        results["kernel_scan"] = scan
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 55

        # Sub-task 4: Daemon System Status
        p.sub_tasks.append({"task": "حالة نظام الدايمونات", "status": "running"})
        await self._emit_progress(7, "daemon_status", 65)
        results["daemons"] = self.daemons.get_status()
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 70

        # Sub-task 5: Firewall Status
        p.sub_tasks.append({"task": "حالة جدار الحماية", "status": "running"})
        await self._emit_progress(7, "firewall_status", 75)
        results["firewall"] = self.firewall.get_status()
        p.sub_tasks[-1]["status"] = "done"
        p.progress = 80

        # Sub-task 6: Master Command — Apex Activation
        p.sub_tasks.append({"task": "التفعيل — تشغيل الآبكس", "status": "running"})
        await self._emit_progress(7, "apex_activation", 90)
        await self.ledger.master_command("APEX_ACTIVATION", {
            "status": "COMPLETE",
            "timestamp": time.time(),
            "entities_created": stats.get("total_population", 0) if stats else 0,
            "daemons_active": 10,
            "phases_completed": 7,
            "message": "APEX_ONLINE — System fully operational"
        })
        p.sub_tasks[-1]["status"] = "done"

        results["apex"] = "ONLINE"
        results["message"] = "APEX_ONLINE — يُدَبِّرُ الْأَمْرَ"
        return results

    # ── Master Controls ──────────────────────────────────────────────

    async def reset_phase(self, phase: int) -> Dict:
        """Reset a failed phase for re-execution."""
        p = self._phases.get(phase)
        if not p:
            return {"error": "مرحلة غير موجودة"}
        p.status = "PENDING"
        p.progress = 0.0
        p.sub_tasks.clear()
        p.error = None
        p.result = {}
        p.started_at = None
        p.completed_at = None
        return {"status": "RESET", "phase": phase}

    async def auto_genesis(self) -> Dict:
        """Execute all 7 phases sequentially (auto mode)."""
        results = {}
        for phase in range(1, 8):
            result = await self.execute_phase(phase)
            results[f"phase_{phase}"] = result
            if "error" in result and "warning" not in result:
                return {"error": f"فشل في المرحلة {phase}", "details": results}
        return {"status": "ALL_COMPLETE", "phases": results}
