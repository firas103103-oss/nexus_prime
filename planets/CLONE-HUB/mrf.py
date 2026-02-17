import os
import hashlib

# المسارات الحالية
MASTER_DIR = "MrF_Enterprise"
SOURCES = [d for d in os.listdir('.') if os.path.isdir(d) and d != MASTER_DIR and not d.startswith('.')]

def get_file_hash(path):
    """بصمة الملف لضمان التطابق التام"""
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except: return None

def main():
    print(f"🕵️‍♂️ بدء جرد المسارات المفقودة (302MB vs 96MB Audit)...")
    
    # 1. فهرسة كل ملفات المجلد الرئيسي
    master_hashes = set()
    for root, _, files in os.walk(MASTER_DIR):
        for f in files:
            p = os.path.join(root, f)
            h = get_file_hash(p)
            if h: master_hashes.add(h)

    # 2. البحث عن المفقودات في المصادر
    missing_assets = []
    found_heavy_junk = 0 # لحساب حجم node_modules أو الكاش
    
    for src in SOURCES:
        for root, _, files in os.walk(src):
            # هل نحن داخل مجلدات ثقيلة غير ضرورية؟
            is_junk = any(x in root for x in ['node_modules', '.git', 'build', 'dist', 'cache'])
            
            for f in files:
                p = os.path.join(root, f)
                h = get_file_hash(p)
                size = os.path.getsize(p)
                
                if h not in master_hashes:
                    if is_junk:
                        found_heavy_junk += size
                    else:
                        missing_assets.append({'file': p, 'size': size})

    # 3. التقرير النهائي
    print("\n" + "="*60)
    print(f"📊 نتائج التحليل الجنائي:")
    print(f"🔹 حجم الملفات 'المهملة' (Junk/Build/Modules): {found_heavy_junk/(1024*1024):.2f} MB")
    print(f"🔹 عدد الملفات 'المفقودة' (Potential Data Loss): {len(missing_assets)}")
    
    if missing_assets:
        print("\n⚠️ ملفات مفقودة (ليست Junk):")
        # ترتيب حسب الحجم
        missing_assets.sort(key=lambda x: x['size'], reverse=True)
        for item in missing_assets[:20]: # عرض أكبر 20 ملف
            print(f"  - [{item['size']/1024:.1f} KB] {item['file']}")
        
        if len(missing_assets) > 20:
            print(f"  ... و {len(missing_assets)-20} ملفات أخرى.")
    else:
        print("\n✅ لا يوجد فقدان في الأكواد المصدرية. الفرق ناتج كلياً عن ملفات الـ Junk والـ Modules.")
    print("="*60)

if __name__ == "__main__":
    main()