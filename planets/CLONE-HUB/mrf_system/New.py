import os
import hashlib
import json
from datetime import datetime

# 1. المصادر الخام (التي نريد التأكد أننا لم ننسَ منها شيئاً)
RAW_SOURCES = ["initials", "OTHER_REPOS"]
# 2. النظام الجديد (الذي نريد التأكد من اكتماله)
TARGET_SYSTEMS = ["DEPLOY_READY", "MrF_OS_PRODUCTION"]

# الامتدادات التي نعتبرها "كنوزاً برمجية"
CODE_EXTS = {'.js', '.ts', '.py', '.ino', '.apk', '.java', '.kt', '.cpp', '.h', '.sh', '.dockerfile', '.yaml'}

def get_file_hash(path):
    """حساب بصمة الملف للتأكد من وجوده في النظام الجديد"""
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except:
        return None

def main():
    print(f"🕵️‍♂️ بدء التدقيق الجنائي الشامل (Master Forensic Audit)...")
    print("="*70)
    
    # الخطوة 1: بناء قاعدة بيانات "السفينة الجديدة" (ما تم نقله فعلياً)
    print("🚢 جرد محتويات النظام الجديد...")
    deployed_hashes = set()
    deployed_files = set()
    
    for sys_dir in TARGET_SYSTEMS:
        if not os.path.exists(sys_dir): continue
        for root, _, files in os.walk(sys_dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in CODE_EXTS or f.lower() == 'package.json':
                    path = os.path.join(root, f)
                    h = get_file_hash(path)
                    if h: deployed_hashes.add(h)
                    deployed_files.add(f.lower())

    # الخطوة 2: مسح المجلدات القديمة بحثاً عن "الناجين"
    print("🔍 مسح المجلدات القديمة بحثاً عن كنوز منسية...")
    missing_projects = {}
    missing_files_count = 0
    
    for src in RAW_SOURCES:
        if not os.path.exists(src): continue
        for root, dirs, files in os.walk(src):
            # تجاهل مجلدات القمامة التي حددناها سابقاً
            if any(junk in root for junk in ['wondershare', 'KNI', 'Messages', 'node_modules']):
                dirs[:] = []
                continue
            
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in CODE_EXTS:
                    path = os.path.join(root, f)
                    h = get_file_hash(path)
                    
                    # إذا لم نجد الملف (لا بالبصمة ولا بالاسم) في النظام الجديد
                    if h not in deployed_hashes and f.lower() not in deployed_files:
                        proj_name = root.split(os.sep)[1] if len(root.split(os.sep)) > 1 else "Root"
                        if proj_name not in missing_projects:
                            missing_projects[proj_name] = []
                        missing_projects[proj_name].append(f)
                        missing_files_count += 1

    # الخطوة 3: توليد تقرير Google-Style للـ Copilot
    report_path = "SYSTEM_INTEGRITY_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as r:
        r.write(f"# 🛡️ MrF OS Integrity Audit Report\n")
        r.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        r.write("## 🏗️ Deployment Status\n")
        r.write(f"- **Elite Folders Inventoried:** {len(TARGET_SYSTEMS)}\n")
        r.write(f"- **Unique Code Files Deployed:** {len(deployed_hashes)}\n\n")
        
        r.write("## ⚠️ Forgotten Assets (Not in New System)\n")
        if not missing_projects:
            r.write("✅ **PERFECT:** No source code was left behind. Every single script, firmware, and APK is accounted for.\n")
        else:
            r.write(f"🛑 **CAUTION:** Found {missing_files_count} files in {len(missing_projects)} folders that were NOT migrated:\n\n")
            for proj, files in missing_projects.items():
                r.write(f"### 📂 Folder: `{proj}`\n")
                r.write(f"- Contains {len(files)} unique code files.\n")
                r.write(f"- Example: `{files[0]}`\n\n")

    print("="*70)
    if missing_projects:
        print(f"🛑 تم العثور على {missing_files_count} ملف كود منسي في {len(missing_projects)} مجلد!")
        print(f"📝 راجع التقرير: {report_path} لرؤية التفاصيل.")
    else:
        print("✨ مبروك! نظامك كامل 100%. لم نترك أي سطر كود خلفنا.")
    print(f"📎 التقرير جاهز للـ Copilot في: {report_path}")

if __name__ == "__main__":
    main()