import os
import json

TARGET_DIR = "MrF_Enterprise_System"

def audit_report():
    print(f"🧐 بدء التدقيق النهائي لـ {TARGET_DIR}...")
    print("="*60)
    
    report = []
    
    categories = os.listdir(TARGET_DIR)
    for cat in categories:
        cat_path = os.path.join(TARGET_DIR, cat)
        if not os.path.isdir(cat_path): continue
        
        print(f"\n📂 قطاع: {cat}")
        projects = os.listdir(cat_path)
        for proj in projects:
            proj_path = os.path.join(cat_path, proj)
            if not os.path.isdir(proj_path): continue
            
            # فحص الصحة
            health = "🟢 سليم"
            issues = []
            
            files = os.listdir(proj_path)
            
            # معايير الصحة حسب النوع
            if "backend" in cat:
                if "package.json" not in files: issues.append("مفقود: package.json")
                if "node_modules" in files: issues.append("تنبيه: مجلد node_modules موجود (يفضل حذفه قبل الرفع)")
            elif "hardware" in cat:
                if not any(f.endswith(".ino") for f in files): issues.append("مفقود: ملف .ino")
            elif "mobile" in cat:
                if not any(f.endswith(".apk") for f in files) and "build.gradle" not in files:
                    issues.append("مفقود: ملفات المشروع أو الـ APK")

            status = "🔴 مشكلة" if issues else "🟢 جاهز"
            print(f"   [{status}] {proj:<25} | {', '.join(issues) if issues else 'لا توجد ملاحظات'}")
            report.append({"project": proj, "status": status, "issues": issues})

    print("\n" + "="*60)
    print("✅ انتهى فحص الجودة. إذا كانت القائمة خضراء، فأنت جاهز للرفع.")

if __name__ == "__main__":
    audit_report()