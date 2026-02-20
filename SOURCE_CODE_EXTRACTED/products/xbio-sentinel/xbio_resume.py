import requests
import json
import os

# إعدادات النواة
BASE_URL = "http://127.0.0.1:8080"

def resume_command_center():
    print("🛡️ [X-BIO] جاري تفعيل بروتوكول العودة...")
    print("-" * 50)
    
    # 1. التحقق من النواة
    try:
        status = requests.get(f"{BASE_URL}/status").json()
        print(f"✅ النواة المركزية: متصلة ({status.get('System')})")
    except:
        print("⚠️ النواة متوقفة. جاري التشغيل التلقائي عبر xbio_control.sh...")
        os.system("./xbio_control.sh start")
    
    # 2. استدعاء تقرير الموظفين
    try:
        query = {"query": "أعطني ملخصاً لحالة الأرشفة السحابية والملفات في الخزنة.", "persona": "ARC-G-711"}
        res = requests.post(f"{BASE_URL}/chat", json=query).json()
        print(f"\n👥 رد نائبك التنفيذي:\n{res['reply']}")
    except:
        print("❌ فشل التواصل مع الوكلاء.")

    # 3. عرض رابط لوحة القيادة
    print("-" * 50)
    print("🚀 لوحة القيادة جاهزة للمراقبة الحية:")
    print("🔗 http://46.224.225.96:8502")
    print("-" * 50)
    print("Welcome back, Mr. Firas. Standing by for orders.")

if __name__ == "__main__":
    resume_command_center()
