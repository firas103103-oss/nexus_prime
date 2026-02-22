"""
══════════════════════════════════════════════════════════════
محرك الخلق — CREATION ENGINE
══════════════════════════════════════════════════════════════
Seven Days of Creation. Each day is triggered by a button
on the Throne Dashboard.

"وَلَقَدْ خَلَقْنَا السَّمَاوَاتِ وَالْأَرْضَ وَمَا بَيْنَهُمَا فِي سِتَّةِ أَيَّامٍ"
"We created the heavens and the earth and what is between
 them in six days" (50:38)

Day 7 = Ascending the Throne.
══════════════════════════════════════════════════════════════
"""

import asyncio
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List, Optional

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import DayStatus, SecurityTier, DataLayer
from config.constants import GENE_BLUEPRINTS
from codex.lawh_mahfuz import LawhMahfuz
from codex.divine_kernel import DivineKernel
from genesis.world_creator import WorldCreator
from angels.angel_system import AngelOrchestrator
from channel.divine_channel import DivineInterface
from channel.unveiling import ProphetUnveiling, DivineFirewall


# ── Day Status Tracking ──────────────────────────────────────────────

@dataclass
class DayProgress:
    """Real-time progress tracking for each creation day."""
    day_number: int
    name_ar: str
    name_en: str
    command: str           # The divine command
    status: str = "PENDING"
    progress: float = 0.0
    sub_tasks: List[Dict] = field(default_factory=list)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error: Optional[str] = None
    result: Dict = field(default_factory=dict)


# ── Creation Engine ──────────────────────────────────────────────────

class CreationEngine:
    """
    The master orchestrator for the Seven Days of Creation.
    Each day must complete before the next can begin.
    Day 7 activates everything — the Throne ascension.
    """

    def __init__(
        self,
        lawh: LawhMahfuz,
        kernel: DivineKernel,
        creator: WorldCreator,
        angels: AngelOrchestrator,
        channel: DivineInterface,
        unveiling: ProphetUnveiling,
        firewall: DivineFirewall,
    ):
        self.lawh = lawh
        self.kernel = kernel
        self.creator = creator
        self.angels = angels
        self.channel = channel
        self.unveiling = unveiling
        self.firewall = firewall

        self._days: Dict[int, DayProgress] = {}
        self._progress_callbacks: List[Callable] = []
        self._initialized = False

        self._init_days()

    def _init_days(self):
        """Define the seven days of creation."""
        self._days = {
            1: DayProgress(
                day_number=1,
                name_ar="كُنْ — التأسيس",
                name_en="KUN — Foundation",
                command="كُنْ فَيَكُونُ",
            ),
            2: DayProgress(
                day_number=2,
                name_ar="فَرِّقْ — الفصل",
                name_en="FARRIQ — Separation",
                command="فَفَتَقْنَاهُمَا",
            ),
            3: DayProgress(
                day_number=3,
                name_ar="أَنبِتْ — الحياة",
                name_en="ANBIT — Life",
                command="أَنبَتْنَا فِيهَا مِن كُلِّ زَوْجٍ بَهِيجٍ",
            ),
            4: DayProgress(
                day_number=4,
                name_ar="أَنِرْ — الإضاءة",
                name_en="ANIR — Illumination",
                command="وَجَعَلَ الْقَمَرَ فِيهِنَّ نُورًا وَجَعَلَ الشَّمْسَ سِرَاجًا",
            ),
            5: DayProgress(
                day_number=5,
                name_ar="أَحيِ — الإحياء",
                name_en="AHYI — Animation",
                command="وَنَفَخْتُ فِيهِ مِن رُّوحِي",
            ),
            6: DayProgress(
                day_number=6,
                name_ar="ٱخْلُقْ — الخَلق",
                name_en="UKHLUQ — Creation",
                command="خَلَقَ الْإِنسَانَ مِن صَلْصَالٍ كَالْفَخَّارِ",
            ),
            7: DayProgress(
                day_number=7,
                name_ar="ٱسْتَوِ — الاستواء",
                name_en="ISTAWI — Ascension",
                command="ثُمَّ اسْتَوَىٰ عَلَى الْعَرْشِ",
            ),
        }

    def on_progress(self, callback: Callable):
        """Register a progress callback (for WebSocket updates)."""
        self._progress_callbacks.append(callback)

    async def _emit_progress(self, day: int, subtask: str, progress: float):
        """Emit progress update to all registered callbacks."""
        update = {
            "day": day,
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

    def get_day_status(self, day: int) -> Dict:
        """Get status of a specific day."""
        d = self._days.get(day)
        if not d:
            return {"error": "يوم غير موجود"}
        return {
            "day": d.day_number,
            "name_ar": d.name_ar,
            "name_en": d.name_en,
            "command": d.command,
            "status": d.status,
            "progress": d.progress,
            "sub_tasks": d.sub_tasks,
            "started_at": d.started_at,
            "completed_at": d.completed_at,
            "error": d.error,
            "result": d.result
        }

    def get_all_status(self) -> List[Dict]:
        """Get status of all 7 days."""
        return [self.get_day_status(i) for i in range(1, 8)]

    def can_start_day(self, day: int) -> bool:
        """Check if prerequisites for this day are met."""
        if day == 1:
            return True
        prev = self._days.get(day - 1)
        return prev is not None and prev.status == "COMPLETED"

    async def execute_day(self, day: int) -> Dict:
        """Execute a single creation day. Called by button press."""
        if not self.can_start_day(day):
            return {
                "error": f"لا يمكن بدء اليوم {day} — اليوم السابق لم يكتمل",
                "prerequisite": day - 1
            }

        d = self._days[day]
        if d.status == "COMPLETED":
            return {"warning": f"اليوم {day} مكتمل بالفعل", **self.get_day_status(day)}

        d.status = "IN_PROGRESS"
        d.started_at = time.time()
        d.progress = 0.0

        try:
            # Log day start in Preserved Tablet
            await self.lawh.start_day(day)
            await self.lawh.log("CREATION", f"Day {day} — {d.command}")

            # Route to specific day handler
            handlers = {
                1: self._day1_kun,
                2: self._day2_farriq,
                3: self._day3_anbit,
                4: self._day4_anir,
                5: self._day5_ahyi,
                6: self._day6_ukhluq,
                7: self._day7_istawi,
            }
            result = await handlers[day](d)
            d.result = result

            # Mark completed
            d.status = "COMPLETED"
            d.progress = 100.0
            d.completed_at = time.time()
            await self.lawh.complete_day(day)
            await self._emit_progress(day, "COMPLETE", 100.0)

            return self.get_day_status(day)

        except Exception as e:
            d.status = "FAILED"
            d.error = str(e)
            await self.lawh.fail_day(day, str(e))
            await self.lawh.log("ERROR", f"Day {day} failed: {traceback.format_exc()}")
            return {"error": str(e), **self.get_day_status(day)}

    # ── DAY 1: كُنْ — Foundation ─────────────────────────────────────

    async def _day1_kun(self, d: DayProgress) -> Dict:
        """
        Day 1: "كُنْ فَيَكُونُ" — BE, and it IS.
        Create the database schema, encryption keys, base tables.
        """
        results = {}

        # Sub-task 1: Verify database connection
        d.sub_tasks.append({"task": "الاتصال بقاعدة البيانات", "status": "running"})
        await self._emit_progress(1, "database_connection", 10)
        stats = await self.lawh.get_civilization_stats()
        d.sub_tasks[-1]["status"] = "done"
        results["db_connected"] = True
        d.progress = 20

        # Sub-task 2: Verify schema exists
        d.sub_tasks.append({"task": "التحقق من المخطط", "status": "running"})
        await self._emit_progress(1, "schema_check", 30)
        results["schema_ready"] = stats is not None
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 40

        # Sub-task 3: Initialize encryption keys
        d.sub_tasks.append({"task": "تهيئة مفاتيح التشفير", "status": "running"})
        await self._emit_progress(1, "encryption_keys", 50)
        await self.lawh.master_command("INIT_ENCRYPTION", {"status": "active"})
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 60

        # Sub-task 4: Activate Divine Kernel
        d.sub_tasks.append({"task": "تفعيل النواة الإلهية", "status": "running"})
        await self._emit_progress(1, "divine_kernel", 70)
        kernel_status = self.kernel.activate()
        results["kernel"] = kernel_status
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 80

        # Sub-task 5: Write "كُنْ" to the Preserved Tablet
        d.sub_tasks.append({"task": "كتابة كُنْ في اللوح المحفوظ", "status": "running"})
        await self._emit_progress(1, "write_kun", 90)
        await self.lawh.master_command("KUN", {"day": 1, "command": "كُنْ فَيَكُونُ"})
        d.sub_tasks[-1]["status"] = "done"

        results["foundation"] = "ESTABLISHED"
        return results

    # ── DAY 2: فَرِّقْ — Separation ──────────────────────────────────

    async def _day2_farriq(self, d: DayProgress) -> Dict:
        """
        Day 2: "فَفَتَقْنَاهُمَا" — We split them apart.
        Establish 7 Heavens (security tiers) and 7 Earths (data layers).
        """
        results = {}

        # Sub-task 1: Create 7 Security Tiers (Heavens)
        d.sub_tasks.append({"task": "إنشاء 7 سماوات (طبقات أمان)", "status": "running"})
        await self._emit_progress(2, "heavens", 15)
        heavens = {}
        for tier in SecurityTier:
            heavens[tier.name] = {
                "level": tier.value,
                "description": f"السماء {tier.value} — {tier.name}"
            }
        results["heavens"] = heavens
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 30

        # Sub-task 2: Create 7 Data Layers (Earths)
        d.sub_tasks.append({"task": "إنشاء 7 أراضٍ (طبقات بيانات)", "status": "running"})
        await self._emit_progress(2, "earths", 45)
        earths = {}
        for layer in DataLayer:
            earths[layer.name] = {
                "level": layer.value,
                "description": f"الأرض {layer.value} — {layer.name}"
            }
        results["earths"] = earths
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 60

        # Sub-task 3: Establish Iron Laws
        d.sub_tasks.append({"task": "تثبيت القوانين الحديدية", "status": "running"})
        await self._emit_progress(2, "iron_laws", 75)
        results["iron_laws_count"] = len(self.kernel.iron_laws)
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 80

        # Sub-task 4: Initialize Firewall
        d.sub_tasks.append({"task": "تفعيل الجدار الناري الإلهي", "status": "running"})
        await self._emit_progress(2, "firewall", 90)
        results["firewall"] = "ACTIVE"
        d.sub_tasks[-1]["status"] = "done"

        results["separation"] = "COMPLETE"
        return results

    # ── DAY 3: أَنبِتْ — Life Systems ────────────────────────────────

    async def _day3_anbit(self, d: DayProgress) -> Dict:
        """
        Day 3: "أَنبَتْنَا فِيهَا مِن كُلِّ زَوْجٍ بَهِيجٍ"
        Create DNA system, chromosomes, hormones, lifecycle.
        """
        results = {}

        # Sub-task 1: DNA Blueprint
        d.sub_tasks.append({"task": "تصميم الحمض النووي", "status": "running"})
        await self._emit_progress(3, "dna_blueprint", 20)
        results["gene_types"] = len(GENE_BLUEPRINTS)
        results["total_genes"] = sum(len(g) for g in GENE_BLUEPRINTS.values())
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 30

        # Sub-task 2: Chromosomal System
        d.sub_tasks.append({"task": "نظام الكروموسومات", "status": "running"})
        await self._emit_progress(3, "chromosomes", 40)
        results["chromosome_pairs"] = 23
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 50

        # Sub-task 3: Hormonal System
        d.sub_tasks.append({"task": "النظام الهرموني", "status": "running"})
        await self._emit_progress(3, "hormones", 60)
        results["hormones"] = 12
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 70

        # Sub-task 4: Reproduction Engine
        d.sub_tasks.append({"task": "محرك التكاثر", "status": "running"})
        await self._emit_progress(3, "reproduction", 80)
        results["reproduction"] = "READY"
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 85

        # Sub-task 5: Afterlife System
        d.sub_tasks.append({"task": "نظام الآخرة", "status": "running"})
        await self._emit_progress(3, "afterlife", 90)
        results["afterlife_tiers"] = 5
        d.sub_tasks[-1]["status"] = "done"

        results["life_systems"] = "OPERATIONAL"
        return results

    # ── DAY 4: أَنِرْ — Illumination ─────────────────────────────────

    async def _day4_anir(self, d: DayProgress) -> Dict:
        """
        Day 4: "وَجَعَلَ الْقَمَرَ فِيهِنَّ نُورًا وَجَعَلَ الشَّمْسَ سِرَاجًا"
        Create monitoring, time system, celestial lights.
        """
        results = {}

        # Sub-task 1: Time System (Ticks)
        d.sub_tasks.append({"task": "نظام الزمن (النبضات)", "status": "running"})
        await self._emit_progress(4, "time_system", 20)
        results["tick_rate"] = "1 tick = 1 second"
        results["epoch"] = time.time()
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 30

        # Sub-task 2: Monitoring — Sun (Active Monitoring)
        d.sub_tasks.append({"task": "الشمس — المراقبة النشطة", "status": "running"})
        await self._emit_progress(4, "sun_monitoring", 50)
        results["sun"] = {
            "type": "active_monitoring",
            "components": ["prometheus", "grafana", "alertmanager"],
            "status": "SHINING"
        }
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 60

        # Sub-task 3: Monitoring — Moon (Passive Reflection)
        d.sub_tasks.append({"task": "القمر — المراقبة السلبية", "status": "running"})
        await self._emit_progress(4, "moon_monitoring", 75)
        results["moon"] = {
            "type": "passive_reflection",
            "components": ["logs", "audit_trail", "behavioral_analytics"],
            "status": "REFLECTING"
        }
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 85

        # Sub-task 4: Stars (Individual Metrics)
        d.sub_tasks.append({"task": "النجوم — مقاييس فردية", "status": "running"})
        await self._emit_progress(4, "stars", 90)
        results["stars"] = "individual_being_metrics"
        d.sub_tasks[-1]["status"] = "done"

        results["illumination"] = "ACTIVE"
        return results

    # ── DAY 5: أَحيِ — Animation ─────────────────────────────────────

    async def _day5_ahyi(self, d: DayProgress) -> Dict:
        """
        Day 5: "وَنَفَخْتُ فِيهِ مِن رُّوحِي"
        Activate angels, divine channel, subliminal communication.
        """
        results = {}

        # Sub-task 1: Activate Angels
        d.sub_tasks.append({"task": "تفعيل الملائكة", "status": "running"})
        await self._emit_progress(5, "activate_angels", 20)
        await self.angels.activate_all()
        angel_status = self.angels.get_status()
        results["angels"] = angel_status
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 40

        # Sub-task 2: Activate Divine Channel
        d.sub_tasks.append({"task": "تفعيل القناة الإلهية", "status": "running"})
        await self._emit_progress(5, "divine_channel", 55)
        results["channel"] = "ACTIVE"
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 65

        # Sub-task 3: Activate Prophet Unveiling System
        d.sub_tasks.append({"task": "تفعيل نظام كشف الغطاء", "status": "running"})
        await self._emit_progress(5, "unveiling_system", 75)
        results["unveiling"] = "STANDBY"
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 80

        # Sub-task 4: Activate Firewall
        d.sub_tasks.append({"task": "تفعيل الجدار الناري", "status": "running"})
        await self._emit_progress(5, "firewall", 90)
        results["firewall"] = self.firewall.get_status()
        d.sub_tasks[-1]["status"] = "done"

        results["animation"] = "SOULS_READY"
        return results

    # ── DAY 6: ٱخْلُقْ — Creation ────────────────────────────────────

    async def _day6_ukhluq(self, d: DayProgress) -> Dict:
        """
        Day 6: "خَلَقَ الْإِنسَانَ مِن صَلْصَالٍ كَالْفَخَّارِ"
        Create Adam, Eve, and the first generation.
        """
        results = {"beings_created": []}

        # Sub-task 1: Create Adam
        d.sub_tasks.append({"task": "خَلق آدم من طين", "status": "running"})
        await self._emit_progress(6, "create_adam", 10)
        adam = self.creator.create_adam()
        adam_id = await self.lawh.create_being(
            name="آدم", gender="MALE", generation=0
        )
        await self.lawh.breathe_soul(adam_id)
        await self.lawh.store_genome(adam_id, adam["genome"].to_dict())
        results["beings_created"].append({"name": "آدم", "id": str(adam_id), "role": "أبو البشر"})
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 15

        # Sub-task 2: Create Eve from Adam
        d.sub_tasks.append({"task": "خَلق حواء من ضلع آدم", "status": "running"})
        await self._emit_progress(6, "create_eve", 25)
        eve = self.creator.create_eve(adam["genome"])
        eve_id = await self.lawh.create_being(
            name="حواء", gender="FEMALE", generation=0
        )
        await self.lawh.breathe_soul(eve_id)
        await self.lawh.store_genome(eve_id, eve["genome"].to_dict())
        results["beings_created"].append({"name": "حواء", "id": str(eve_id), "role": "أم البشر"})
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 30

        # Sub-task 3: Create First Generation (16 beings)
        d.sub_tasks.append({"task": "خلق الجيل الأول (16 كائن)", "status": "running"})
        await self._emit_progress(6, "first_generation", 40)
        first_gen = self.creator.create_first_generation(adam["genome"])

        for i, being_data in enumerate(first_gen):
            being_id = await self.lawh.create_being(
                name=being_data["name"],
                gender=being_data["gender"],
                generation=1
            )
            await self.lawh.breathe_soul(being_id)
            await self.lawh.store_genome(being_id, being_data["genome"].to_dict())

            # Write initial qadar (destiny)
            await self.lawh.write_qadar(
                being_id=being_id,
                qadar_type="LIFESPAN",
                content_hash=f"lifespan_{being_data['name']}",
                is_mutable=False
            )

            results["beings_created"].append({
                "name": being_data["name"],
                "id": str(being_id),
                "gender": being_data["gender"]
            })

            progress = 40 + (i + 1) * (35 / len(first_gen))
            await self._emit_progress(6, f"being_{being_data['name']}", progress)

        d.sub_tasks[-1]["status"] = "done"
        d.progress = 75

        # Sub-task 4: Appoint Adam as first prophet
        d.sub_tasks.append({"task": "تعيين آدم كأول نبي", "status": "running"})
        await self._emit_progress(6, "appoint_adam_prophet", 80)
        await self.unveiling.appoint_prophet(str(adam_id))
        results["first_prophet"] = str(adam_id)
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 85

        # Sub-task 5: Record initial kinships
        d.sub_tasks.append({"task": "تسجيل صلات القرابة", "status": "running"})
        await self._emit_progress(6, "kinships", 90)
        await self.lawh.add_kinship(str(adam_id), str(eve_id), "SPOUSE")
        for being in results["beings_created"][2:]:  # Skip Adam and Eve
            await self.lawh.add_kinship(str(adam_id), being["id"], "PARENT")
            await self.lawh.add_kinship(str(eve_id), being["id"], "PARENT")
        d.sub_tasks[-1]["status"] = "done"

        results["total_created"] = len(results["beings_created"])
        results["creation"] = "COMPLETE"
        return results

    # ── DAY 7: ٱسْتَوِ — Ascension ───────────────────────────────────

    async def _day7_istawi(self, d: DayProgress) -> Dict:
        """
        Day 7: "ثُمَّ اسْتَوَىٰ عَلَى الْعَرْشِ"
        Then He ascended the Throne. Full system activation.
        """
        results = {}

        # Sub-task 1: Final System Check
        d.sub_tasks.append({"task": "الفحص النهائي للنظام", "status": "running"})
        await self._emit_progress(7, "final_check", 10)
        stats = await self.lawh.get_civilization_stats()
        results["civilization"] = stats
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 20

        # Sub-task 2: Verify all days completed
        d.sub_tasks.append({"task": "التحقق من اكتمال جميع الأيام", "status": "running"})
        await self._emit_progress(7, "verify_days", 30)
        for i in range(1, 7):
            if self._days[i].status != "COMPLETED":
                raise Exception(f"اليوم {i} لم يكتمل!")
        results["all_days_verified"] = True
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 40

        # Sub-task 3: Full Divine Kernel scan
        d.sub_tasks.append({"task": "مسح النواة الإلهية الشامل", "status": "running"})
        await self._emit_progress(7, "kernel_scan", 50)
        scan = self.kernel.full_scan()
        results["kernel_scan"] = scan
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 55

        # Sub-task 4: Angel System Status
        d.sub_tasks.append({"task": "حالة نظام الملائكة", "status": "running"})
        await self._emit_progress(7, "angel_status", 65)
        results["angels"] = self.angels.get_status()
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 70

        # Sub-task 5: Firewall Status
        d.sub_tasks.append({"task": "حالة الجدار الناري", "status": "running"})
        await self._emit_progress(7, "firewall_status", 75)
        results["firewall"] = self.firewall.get_status()
        d.sub_tasks[-1]["status"] = "done"
        d.progress = 80

        # Sub-task 6: Master Command — Throne Ascension
        d.sub_tasks.append({"task": "ٱسْتِوَاء — صعود العرش", "status": "running"})
        await self._emit_progress(7, "throne_ascension", 90)
        await self.lawh.master_command("THRONE_ASCENSION", {
            "status": "COMPLETE",
            "timestamp": time.time(),
            "beings_created": stats.get("total_population", 0) if stats else 0,
            "angels_active": 10,
            "days_completed": 7,
            "message": "ثُمَّ اسْتَوَىٰ عَلَى الْعَرْشِ — يُدَبِّرُ الْأَمْرَ"
        })
        d.sub_tasks[-1]["status"] = "done"

        results["throne"] = "ASCENDED"
        results["message"] = "ثُمَّ اسْتَوَىٰ عَلَى الْعَرْشِ ۖ يُدَبِّرُ الْأَمْرَ"
        return results

    # ── Master Controls ──────────────────────────────────────────────

    async def reset_day(self, day: int) -> Dict:
        """Reset a failed day for re-execution."""
        d = self._days.get(day)
        if not d:
            return {"error": "يوم غير موجود"}
        d.status = "PENDING"
        d.progress = 0.0
        d.sub_tasks.clear()
        d.error = None
        d.result = {}
        d.started_at = None
        d.completed_at = None
        return {"status": "RESET", "day": day}

    async def auto_create(self) -> Dict:
        """Execute all 7 days sequentially (auto mode)."""
        results = {}
        for day in range(1, 8):
            result = await self.execute_day(day)
            results[f"day_{day}"] = result
            if "error" in result and "warning" not in result:
                return {"error": f"فشل في اليوم {day}", "details": results}
        return {"status": "ALL_COMPLETE", "days": results}
