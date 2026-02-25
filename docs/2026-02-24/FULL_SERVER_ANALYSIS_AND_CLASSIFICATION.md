# تحليل السيرفر الكامل — تصنيف ومقترحات

**التاريخ:** 2026-02-24  
**النطاق:** كل مجلدات وملفات السيرفر `/root`

---

## 1. غير لازم (يمكن أرشفته أو حذفه بحذر)

| العنصر | الموقع | السبب |
|--------|--------|-------|
| **duplicate_files_report.txt** | /root/ | فارغ (0 bytes) |
| **nexus_prime_backup_2026-02-24_18-18.tar.gz** | /root/ | 4.3GB — أرشيف قديم؛ يمكن نقله خارج السيرفر أو ضغطه بعد التحقق |
| **neural_spine_backup_pre_restructure** | NEXUS_PRIME_UNIFIED/ | نسخة احتياطية قبل إعادة الهيكلة — أرشفة إذا neural_spine مستقر |
| **docs/archive/** (جزء منه) | NEXUS_PRIME_UNIFIED/docs/ | أرشيفات مكررة (NEXUS_PRIME_FULL_ARCHIVE.txt في 3 نسخ) — توحيد نسخة واحدة |
| **baselines/** | NEXUS_PRIME_UNIFIED/ | لقطات قديمة — الاحتفاظ بآخر baseline فقط |
| **backups/** | NEXUS_PRIME_UNIFIED/ | نسخ docker-compose قديمة — أرشفة بعد التحقق |

---

## 2. قابل للدمج بالمنظمة

| العنصر | الموقع | المقترح |
|--------|--------|---------|
| **/root/integration** | خارج NEXUS_PRIME_UNIFIED | توحيد مع NEXUS_PRIME_UNIFIED/integration — إما symlink أو نسخ مصدر واحد |
| **/root/products** | خارج NEXUS_PRIME_UNIFIED | مُربط بالفعل عبر ecosystem_api — توثيق كمسار رسمي في docs |
| **nexus_*.sh** | /root/ | نقل إلى NEXUS_PRIME_UNIFIED/scripts/ أو توثيق كـ entry points |
| **MASTER_IGNITION.sh** | /root/ | دمجه في سكربت التشغيل الموحد |
| **planets/CLONE-HUB** | NEXUS_PRIME_UNIFIED/planets/ | منطق clone-hub في integration/ — توثيق التبعية |
| **planets/AS-SULTAN** | NEXUS_PRIME_UNIFIED/planets/ | ربط مع sovereign_gateway و sultan.mrf103.com |
| **planets/X-BIO** | NEXUS_PRIME_UNIFIED/planets/ | ربط مع xbio-sentinel و nexus_xbio |
| **planets/AI-ARCH** | NEXUS_PRIME_UNIFIED/planets/ | ربط مع arc-framework و products |
| **web-dashboards/source/** | NEXUS_PRIME_UNIFIED/ | صفحات (landing, citadel, sultan, ...) — ربطها بـ nginx routes |
| **dashboard-arc/arc_core** | NEXUS_PRIME_UNIFIED/ | التحقق من علاقته بـ arc-framework |

---

## 3. مقترحات تطوير

| البند | المقترح |
|-------|---------|
| **توحيد integration** | /root/integration و NEXUS_PRIME_UNIFIED/integration — مصدر واحد (symlink أو نسخ) |
| **سكربت تشغيل موحد** | دمج nexus_entry.sh, nexus_exit.sh, nexus_control.sh, nexus_status.sh في scripts/run.sh |
| **نسخ احتياطية** | سياسة retention: آخر 3 نسخ في nexus_prime_backups، أرشفة الأقدم خارج السيرفر |
| **أرشيف التوثيق** | توحيد docs/archive — إزالة المكررات، هيكلة حسب التاريخ |
| **products/_ORGANIZED_EXTRAS** | مراجعة المحتوى — دمج أو تصنيف |
| **LiteLLM** | إصلاح UNHEALTHY — مراجعة litellm_config.yaml |
| **K8s manifests** | k8s-manifests/ — التحقق من صلاحيتها للتشغيل على Kubernetes |

---

## 4. خريطة التبعيات

```
nexus_prime_backups (retention)
    └── nexus_prime_backup_*.tar.gz

/root/integration  ←→  NEXUS_PRIME_UNIFIED/integration  (توحيد)
/root/products     →   ecosystem_api (volume mount)

nexus_*.sh (root)  →   NEXUS_PRIME_UNIFIED/docker-compose
MASTER_IGNITION.sh →   نقطة التشغيل الرئيسية

planets/*          →   products/*, integration/*
```

---

## 5. خطة تنفيذ مقترحة (للمرحلة التالية)

| المرحلة | الإجراء | الأولوية |
|---------|---------|----------|
| 1 | توحيد integration (symlink أو نسخ) | P1 |
| 2 | نقل/توثيق nexus_*.sh في scripts/ | P2 |
| 3 | سياسة retention للنسخ الاحتياطية | P2 |
| 4 | توحيد docs/archive (إزالة مكررات) | P3 |
| 5 | حذف duplicate_files_report.txt (فارغ) | P3 |
| 6 | مراجعة neural_spine_backup — أرشفة إذا مستقر | P3 |
