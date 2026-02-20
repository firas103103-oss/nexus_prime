import os
from supabase import create_client, Client

# تحميل الأسرار
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE")

def inject_test_mission():
    print("📡 [TEST] جاري حقن مهمة اختبارية في النظام...")
    supabase: Client = create_client(url, key)
    
    new_mission = {
        "mission_name": "🛡️ Strategic Integrity Scan",
        "assigned_to": "ARC-G-711",
        "status": "RUNNING",
        "priority": 1
    }
    
    # حقن البيانات
    supabase.table("missions").insert(new_mission).execute()
    print("✅ [SUCCESS] تم إرسال الأمر. يرجى تحديث لوحة المراقبة الآن.")

if __name__ == "__main__":
    inject_test_mission()
