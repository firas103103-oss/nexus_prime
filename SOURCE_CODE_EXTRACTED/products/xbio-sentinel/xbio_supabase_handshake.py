import os
from supabase import create_client, Client

# تحميل الأسرار من البيئة
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE")

def start_handshake():
    if not url or not key:
        print("❌ [CRITICAL] لم يتم العثور على مفاتيح Supabase. تأكد من تشغيل 'source /root/.xbio_secrets'")
        return

    try:
        # إنشاء العميل
        supabase: Client = create_client(url, key)
        
        print(f"📡 [CONNECT] جاري فحص الجداول في: {url}")
        
        # اختبار القراءة من جدول الموظفين (Personnel) أو المهام
        # سنحاول إدراج مهمة تجريبية لنظام X-BIO
        test_mission = {
            "mission_name": "Initial Handshake",
            "assigned_to": "ARC-G-711",
            "status": "Success"
        }
        
        data = supabase.table("missions").insert(test_mission).execute()
        
        if data:
            print("✅ [HANDSHAKE] تم الاتصال وإدراج أول مهمة بنجاح!")
            print("📊 جاري قراءة حالة المنظومة من سوبابيز...")
            
            # قراءة البيانات للتأكد
            missions = supabase.table("missions").select("*").execute()
            print(f"📋 المهام النشطة حالياً: {len(missions.data)}")
            
        else:
            print("⚠️ [WARNING] تم الاتصال ولكن لم يتم إرجاع بيانات.")

    except Exception as e:
        print(f"❌ [ERROR] فشل بروتوكول المصافحة: {e}")

if __name__ == "__main__":
    start_handshake()
