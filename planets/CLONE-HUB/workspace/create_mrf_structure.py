import os

# 1) اعتمد دائماً على المسار الحالي اللي انت واقف فيه في التيرمنال
CWD = os.getcwd()
BASE_DIR = os.path.join(CWD, "MRF_CentralBrainStation")

print("Current working directory (المجلد الحالي):")
print("   ", CWD)
print("Target project directory (مكان إنشاء المشروع):")
print("   ", BASE_DIR)
print("-" * 60)

# 2) أنشئ مجلد المشروع الرئيسي
os.makedirs(BASE_DIR, exist_ok=True)

# 3) تعريف الملفات والمحتوى (مختصر – نفس الفكرة السابقة)
files = {
    # ========== 00_Docs ==========
    "00_Docs/Central_Brain_Station_Overview.md":
        "# Central Brain Station (CBS) – نظرة عامة\n\n"
        "Central Brain Station (CBS) هي المنظومة المركزية التي تدير كون mr.F بالكامل.\n",

    "00_Docs/System_Constitution.md":
        "# System Constitution – دستور نظام mr.F\n\n"
        "هذا الدستور يحدد القيم والأولويات وحدود القرارات في النظام.\n",

    "00_Docs/mrF_Agent_System_Blueprint.md":
        "# mr.F Agent System – Blueprint\n\n"
        "الوكيل المركزي الذي يمثل وعي وقرارات mr.F داخل CBS.\n",

    # ========== 10_Personal ==========
    "10_Personal/Personal_Overview.md":
        "# Personal Pillar – نظرة عامة\n\n"
        "مسؤول عن حياة mr.F الشخصية والعائلية.\n",

    "10_Personal/Self_And_Life_Agent.md":
        "# Self_And_Life_Agent – Blueprint\n\n"
        "وكيل لمتابعة العادات والأهداف والروتين الشخصي.\n",

    "10_Personal/Child_And_Family_Agent.md":
        "# Child_And_Family_Agent – Blueprint\n\n"
        "وكيل لمتابعة شؤون الطفل والأسرة.\n",

    # ========== 20_Business ==========
    "20_Business/Business_Overview.md":
        "# Business Pillar – نظرة عامة\n\n"
        "يشمل XBIO و iDigital و Sentinel Devices.\n",

    "20_Business/XBIO_Profile.md":
        "# XBIO – ملف تعريفي\n\n"
        "ذراع Bio-Tech / Bio-Security / AI-Sensory.\n",

    "20_Business/iDigital_Profile.md":
        "# iDigital – ملف تعريفي\n\n"
        "ذراع المنتجات والخدمات الرقمية.\n",

    "20_Business/Sentinel_Devices_Profile.md":
        "# Sentinel Devices – ملف تعريفي\n\n"
        "أجهزة و Sentinel Devices و IoT.\n",

    # ========== 30_Projects ==========
    "30_Projects/Projects_Overview.md":
        "# Projects Pillar – نظرة عامة\n\n"
        "يجمع كل المشاريع: WonderCrust, Mindful Labs, Entrado.\n",

    "30_Projects/WonderCrust_Project.md":
        "# WonderCrust – مشروع\n\n"
        "وصف مبدئي للمشروع.\n",

    "30_Projects/MindfulLabs_Project.md":
        "# Mindful Labs – مشروع\n\n"
        "وصف مبدئي للمشروع.\n",

    "30_Projects/Entrado_Project.md":
        "# Entrado – مشروع\n\n"
        "وصف مبدئي للمشروع.\n",

    "30_Projects/RnD_And_Labs_Hub.md":
        "# R&D & Labs Hub – مركز الأبحاث\n\n"
        "مركز موحّد للتجارب والأبحاث.\n",

    # ========== 40_Finance ==========
    "40_Finance/Finance_Overview.md":
        "# Finance Pillar – نظرة عامة\n\n"
        "إدارة الأموال والديون والالتزامات (TabTwo).\n",

    "40_Finance/Financial_Core_Agent.md":
        "# Financial_Core_Agent – Blueprint\n\n"
        "يتابع الدخل والمصاريف والكاش فلو.\n",

    "40_Finance/TabTwo_Debts_And_Obligations.md":
        "# TabTwo – الديون والالتزامات\n\n"
        "كل دين/التزام مرتبط بحياة mr.F أو مشاريعه.\n",

    # ========== 50_Legal ==========
    "50_Legal/Legal_Overview.md":
        "# Legal Pillar – نظرة عامة\n\n"
        "العقود والقضايا القانونية والمحامي.\n",

    "50_Legal/Legal_Agent.md":
        "# Legal_Agent – Blueprint\n\n"
        "وكيل قانوني داخلي.\n",

    "50_Legal/Lawyer_Profile.md":
        "# Lawyer Profile – ملف المحامي\n\n"
        "بيانات المحامي والقضايا التي يتولاها.\n",

    # ========== 60_Security ==========
    "60_Security/Security_Overview.md":
        "# Security & Protection Pillar – نظرة عامة\n\n"
        "مراقبة المخاطر والحماية العامة.\n",

    "60_Security/Security_Sentinel_Agent.md":
        "# Security_Sentinel_Agent – Blueprint\n\n"
        "يراقب مؤشرات الخطر من المالية والقانونية والمشاريع.\n",

    "60_Security/Risk_And_Protection_Agent.md":
        "# Risk_And_Protection_Agent – Blueprint\n\n"
        "تحليل المخاطر واقتراح إجراءات حماية.\n",

    # ========== 99_Tech_Notes ==========
    "99_Tech_Notes/Backend_Schema_Notes.md":
        "# Backend Schema Notes – ملاحظات أولية\n\n"
        "اقتراح أولي للجداول/الـCollections.\n",

    "99_Tech_Notes/Frontend_UI_Notes.md":
        "# Frontend UI Notes – ملاحظات الواجهة\n\n"
        "فكرة عامة عن الـDashboard وTabs.\n",
}


def main():
    created_files = 0

    for relative_path, content in files.items():
        full_path = os.path.join(BASE_DIR, relative_path)
        folder = os.path.dirname(full_path)
        os.makedirs(folder, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        created_files += 1
        print("Created file:", full_path)

    print("-" * 60)
    print("تم إنشاء هيكل المشروع في المسار التالي:")
    print("   ", BASE_DIR)
    print("عدد الملفات التي تم إنشاؤها:", created_files)


if __name__ == "__main__":
    main()
