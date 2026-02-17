import os
import datetime

# اسم المجلد الرئيسي الذي نريد فحصه
TARGET_DIR = "MrF_Enterprise"
REPORT_FILE = "FINAL_ASSET_REPORT.txt"

def get_dir_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total

def main():
    print(f"🕵️‍♂️ جاري مسح محتويات {TARGET_DIR}...")
    
    if not os.path.exists(TARGET_DIR):
        print(f"❌ خطأ: المجلد {TARGET_DIR} غير موجود بجانب السكريبت!")
        input("اضغط Enter للخروج...")
        return

    report_lines = []
    report_lines.append(f"📄 تقرير الجرد النهائي لمنظومة MrF Enterprise")
    report_lines.append(f"📅 التاريخ: {datetime.datetime.now()}")
    report_lines.append("=" * 50)

    total_project_size = 0
    total_files = 0

    # مسح الأقسام الرئيسية
    for category in sorted(os.listdir(TARGET_DIR)):
        cat_path = os.path.join(TARGET_DIR, category)
        if os.path.isdir(cat_path):
            size_bytes = get_dir_size(cat_path)
            size_mb = size_bytes / (1024 * 1024)
            total_project_size += size_bytes
            
            # عد الملفات داخل القسم
            file_count = sum([len(files) for r, d, files in os.walk(cat_path)])
            total_files += file_count
            
            report_lines.append(f"\n📂 القسم: {category}")
            report_lines.append(f"   - الحجم: {size_mb:.2f} MB")
            report_lines.append(f"   - عدد الملفات: {file_count}")
            
            # ذكر أهم المشاريع داخل القسم
            projects = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
            if projects:
                report_lines.append(f"   - المشاريع ({len(projects)}):")
                for p in projects:
                    report_lines.append(f"     * {p}")

    report_lines.append("\n" + "=" * 50)
    report_lines.append(f"📊 الخلاصة النهائية:")
    report_lines.append(f"💾 الحجم الكلي النظيف: {total_project_size / (1024 * 1024):.2f} MB")
    report_lines.append(f"🗂 العدد الكلي للملفات: {total_files}")
    report_lines.append("=" * 50)

    # حفظ التقرير
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("\n✅ تم إنشاء التقرير بنجاح!")
    print(f"📄 اقرأ الملف: {REPORT_FILE}")
    print("-" * 30)
    
    # عرض سريع للخلاصة على الشاشة
    print(f"Total Size: {total_project_size / (1024 * 1024):.2f} MB")
    print(f"Total Files: {total_files}")
    
    # أهم سطر لمنع اختفاء النافذة
    input("\n🚀 اضغط Enter لإغلاق النافذة...")

if __name__ == "__main__":
    main()