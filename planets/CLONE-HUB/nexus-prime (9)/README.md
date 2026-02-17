# NEXUS PRIME 💠
### Quantum Data Analysis Interface | واجهة التحليل الكمي للبيانات

![Version](https://img.shields.io/badge/VERSION-2.0.0-cyan?style=for-the-badge)
![Core](https://img.shields.io/badge/CORE-GEMINI_3_PRO-orange?style=for-the-badge)
![UI](https://img.shields.io/badge/INTERFACE-SENTIENT-purple?style=for-the-badge)

**Nexus Prime** is not just a chatbot; it is a **Tier-1 Sovereign Data Organism**. It utilizes the Google Gemini API (`gemini-3-pro-preview`) to perform deep forensic analysis on text and files within an immersive, 3D reactive environment.

**نكسوس برايم** ليس مجرد روبوت محادثة؛ إنه **كيان بيانات سيادي من المستوى الأول**. يستخدم واجهة Google Gemini API لإجراء تحليل جنائي عميق للنصوص والملفات داخل بيئة ثلاثية الأبعاد تفاعلية.

---

## 🧠 The Hive Mind Architecture | هيمكلة العقل الجمعي

Nexus Prime breaks down analysis into specific "Agents", each simulating a different cognitive function. The UI visualizes this thought process in real-time.

يقوم النظام بتقسيم عملية التحليل إلى "عملاء" (Agents) متخصصين، ويقوم بتجسيد عملية التفكير هذه بصرياً وصوتياً:

1.  **👁️ VISUAL_CORE**: Scans patterns, OCR, and pixel data. (Robotic/Fast voice).
2.  **🛡️ SECURITY_OPS**: Checks for threats, compliance, and safety. (Deep/Serious voice).
3.  **💎 DATA_MINER**: Extracts hidden value and strategic insights. (Analytical voice).
4.  **⚖️ EXECUTIVE**: Delivers the final authoritative verdict. (Balanced voice).

---

## ✨ Key Features | المميزات الرئيسية

*   **🌌 Immersive 3D Core**: Built with `React Three Fiber`, the central neural core reacts to data processing states (Idle, Gravity Well, Analysis).
*   **🗣️ Multi-Agent Voice Synthesis**: Uses the Web Speech API to modulate pitch and rate, giving each AI agent a distinct "voice" personality.
*   **📄 Smart HTML Reports**: Generates a self-contained, downloadable HTML file containing the full analysis, the chat log, and an embedded script to *replay* the audio briefing offline.
*   **🌍 Bilingual Support**: Full support for Arabic (RTL, Cairo Font, Localized Dialect) and English (Tech-Ops Tone).
*   **📂 Multimodal Analysis**: Drag-and-drop support for files (Images/Text) alongside text queries.

---

## 🛠️ Tech Stack | التقنيات المستخدمة

*   **Framework**: React (Vite)
*   **Language**: TypeScript
*   **3D Engine**: Three.js / @react-three/fiber / @react-three/drei
*   **AI Backend**: Google GenAI SDK (`gemini-3-pro-preview`)
*   **Styling**: Tailwind CSS / clsx
*   **Animation**: Framer Motion
*   **Icons**: Lucide React

---

## 🚀 Installation & Setup | التثبيت والتشغيل

### 1. Clone the Repository | استنسخ المستودع
```bash
git clone https://github.com/your-username/nexus-prime.git
cd nexus-prime
```

### 2. Install Dependencies | ثبت المكتبات
This project uses a flat file structure with ESM imports, but ensure you have Node.js installed.
```bash
npm install
```

### 3. Configure API Key | إعداد مفتاح الذكاء الاصطناعي
Create a `.env` file in the root directory and add your Google Gemini API key:
قم بإنشاء ملف `.env` وأضف مفتاحك الخاص:

```env
API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
*Note: The system requires access to `gemini-3-pro-preview`.*

### 4. Run the Core | تشغيل النظام
```bash
npm run dev
```
Open `http://localhost:5173` to access the interface.

---

## 🕹️ Usage Guide | دليل الاستخدام

1.  **Initialize**: Choose your language (Arabic/English) on the intro screen.
2.  **Input Data**: 
    *   Type a command or query in the input field.
    *   **OR** Drag and drop an image/file anywhere on the screen.
3.  **Observe**: Watch the "Hive Mind" dialogue as agents analyze the data. The 3D core will pulse and change color based on the active agent.
4.  **Review**: Read the "Executive Summary" and "Deep Analysis".
5.  **Export**: Click **"Download Smart Intel"** to save a standalone HTML report.

---

## 📂 Project Structure | هيكلية الملفات

```
nexus-prime/
├── src/
│   ├── components/
│   │   ├── VoidScene.tsx       # The 3D Background & Neural Core
│   │   └── DashboardDisplay.tsx # The Analysis Result UI
│   ├── hooks/
│   │   └── useNexusCore.ts     # Main Logic, Audio, & State Management
│   ├── services/
│   │   └── geminiService.ts    # API Calls & Prompt Engineering
│   ├── utils/
│   │   └── reportGenerator.ts  # Generates the downloadable HTML
│   ├── types.ts                # TypeScript Interfaces
│   └── App.tsx                 # Main Application Entry
├── index.html                  # Import Maps & Head Config
└── package.json
```

---

<div align="center">
  <p>System Status: <strong>OPERATIONAL</strong></p>
  <p><em>"Data is the currency of the future. We are the bank." - Nexus Prime</em></p>
</div>
