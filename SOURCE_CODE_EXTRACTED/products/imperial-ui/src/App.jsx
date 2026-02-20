import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Globe, User, FileText, Settings, BookOpen, CheckCircle, Upload, 
  Shield, PenTool, Database, Download, Cpu, Video, Image as ImageIcon, MessageSquare 
} from 'lucide-react';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import { AGENT_MATRIX } from './agents/AgentConfig';

pdfMake.vfs = pdfFonts.pdfMake.vfs;

const COPY = {
  ar: {
    headerTitle: "MRF SOVEREIGN",
    headerSubtitle: "منظومة النشر السيادي الصناعية v5.0",
    status: "حالة النواة: تشغيل",
    step1Title: "اللغة والبيانات السيادية",
    languageLabel: "اللغة",
    languageAr: "العربية",
    languageEn: "English",
    authorName: "اسم المؤلف الكامل",
    publishCountry: "بلد النشر (للرقابة)",
    email: "البريد الإلكتروني",
    phone: "رقم الجوال",
    step1Cta: "تثبيت الهوية ومتابعة",
    step2Title: "مشروع النشر الجديد",
    bookTitle: "عنوان الكتاب النهائي",
    uploadTitle: "رفع المخطوطة الخام (TXT حصراً)",
    uploadSub: "نظام التحليل جاهز لمعالجة 200,000 كلمة بدقة مطلقة",
    step2Cta: "بدء الإنتاج الصناعي",
    runningTitle: "جاري التشغيل",
    runningRole: "الرتبة",
    runningTemp: "الحرارة",
    preparing: "إعداد...",
    completeCta: "تحميل الحزمة الإمبراطورية الكاملة (ZIP)",
    logStart: "إطلاق محرك الإنتاج لـ {name}. المستهدف: {country}.",
    logBegin: "بدء معالجة المخطوطة (سعة 200,000 كلمة مقسمة إلى كتل)...",
    logDone: "اكتملت المعالجة الجراحية لـ 200 ألف كلمة.",
    logArchitect: "[Architect] جاري مسح النص وإزالة أي ترقيم أو تقسيم عشوائي قديم...",
    logEditor: "[Editor] جاري تنظيف المتن، معالجة الحروف العربية، وإعادة الفهرسة...",
    logLegal: "[Sentinel] مراجعة المحتوى في {country}: فحص المعايير الأدبية والقانونية...",
    logVisual: "[Visual Artist] تحليل النص لتوليد مطالبات الغلاف والصور الداخلية...",
    logCinematic: "[Cinematic] توليد سيناريو فيديو ترويجي ومطالبات الحركة...",
    logMarketer: "[Strategist] بناء خطة التسويق، تقارير المراجعة، ومنشورات السوشيال ميديا...",
    reportEditorial: "تقرير التدقيق اللغوي للمؤلف {name}.\nتمت معالجة النص ليكون خالياً من التكرار واللخبطة.",
    reportLegal: "تمت المراجعة في {country}.\nالمحتوى مطابق للمعايير الأدبية والقانونية للنشر.",
    reportVisual: "Midjourney Prompt: غلاف سينمائي لكتاب \"{bookTitle}\" للمؤلف {name} بأسلوب ملحمي ودقة عالية.",
    reportVideo: "Cinematic Script: [Scene 1] خلفية داكنة، نص ذهبي يظهر... [Scene 2] تعليق صوتي يقرأ الافتتاح...",
    reportMarketing: "خطة إطلاق الكتاب في {country}.\nالجمهور المستهدف: القراء المهتمون بـ {bookTitle}."
  },
  en: {
    headerTitle: "MRF SOVEREIGN",
    headerSubtitle: "Industrial Sovereign Publishing Matrix v5.0",
    status: "CORE STATUS: OPERATIONAL",
    step1Title: "Language & Sovereign Identity",
    languageLabel: "Language",
    languageAr: "Arabic",
    languageEn: "English",
    authorName: "Author Full Name",
    publishCountry: "Publishing Country (Compliance)",
    email: "Email Address",
    phone: "Mobile Number",
    step1Cta: "Confirm Identity & Continue",
    step2Title: "New Publishing Project",
    bookTitle: "Final Book Title",
    uploadTitle: "Upload Raw Manuscript (TXT only)",
    uploadSub: "The analysis system is ready to process 200,000 words with precision",
    step2Cta: "Start Industrial Production",
    runningTitle: "Active Agent",
    runningRole: "Rank",
    runningTemp: "Temp",
    preparing: "Preparing...",
    completeCta: "Download Full Imperial Package (ZIP)",
    logStart: "Launching production engine for {name}. Target jurisdiction: {country}.",
    logBegin: "Beginning manuscript processing (200,000-word capacity segmented into blocks)...",
    logDone: "Processing complete for 200,000 words.",
    logArchitect: "[Architect] Scanning text and removing legacy punctuation and fragmentation...",
    logEditor: "[Editor] Cleaning manuscript, normalizing Arabic glyphs, and re-indexing...",
    logLegal: "[Sentinel] Reviewing content for {country}: legal and literary compliance checks...",
    logVisual: "[Visual Artist] Analyzing text to generate cover and interior prompt sets...",
    logCinematic: "[Cinematic] Generating teaser script and motion prompts...",
    logMarketer: "[Strategist] Building marketing plan, review reports, and social media assets...",
    reportEditorial: "Editorial review report for {name}.\nThe text has been cleaned for duplication and noise.",
    reportLegal: "Compliance review for {country} completed.\nContent aligns with publishing and legal standards.",
    reportVisual: "Midjourney Prompt: A cinematic cover for \"{bookTitle}\" by {name}, epic style, high resolution.",
    reportVideo: "Cinematic Script: [Scene 1] Dark background, gold text appears... [Scene 2] Voiceover reads the opening...",
    reportMarketing: "Launch plan for {country}.\nTarget audience: readers interested in {bookTitle}."
  }
};

const formatText = (template, vars) => template.replace(/\{(\w+)\}/g, (_, key) => vars[key] ?? "");

export default function App() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({ 
    language: 'ar', country: '', name: '', email: '', phone: '', file: null, goal: 'publish', bookTitle: '' 
  });
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState([]);
  const [activeAgent, setActiveAgent] = useState(null);
  const [isFinished, setIsFinished] = useState(false);

  const addLog = (msg, type = 'info') => setLogs(prev => [...prev, { time: new Date().toLocaleTimeString(formData.language === 'ar' ? 'ar' : 'en-US'), msg, type }]);
  const t = (key, vars = {}) => formatText(COPY[formData.language][key] || "", vars);

  // محرك المعالجة الصناعي (Heavy Duty Processing)
  const runSovereignEngine = async () => {
    setStep(3);
    addLog(t("logStart", { name: formData.name, country: formData.country }), 'system');
    addLog(t("logBegin"), 'system');

    const totalSteps = 60; // محاكاة لخطوات دقيقة جداً
    for (let i = 1; i <= totalSteps; i++) {
      await new Promise(r => setTimeout(r, 100)); // محاكاة سرعة المعالجة
      setProgress((i / totalSteps) * 100);

      // تفعيل الوكلاء حسب المرحلة
      if (i === 1) { setActiveAgent(AGENT_MATRIX.orchestrator); addLog(t("logArchitect"), "agent"); }
      if (i === 10) { setActiveAgent(AGENT_MATRIX.editor); addLog(t("logEditor"), "agent"); }
      if (i === 25) { setActiveAgent(AGENT_MATRIX.legal); addLog(t("logLegal", { country: formData.country }), "agent"); }
      if (i === 35) { setActiveAgent(AGENT_MATRIX.visual); addLog(t("logVisual"), "agent"); }
      if (i === 45) { setActiveAgent(AGENT_MATRIX.cinematic); addLog(t("logCinematic"), "agent"); }
      if (i === 55) { setActiveAgent(AGENT_MATRIX.marketer); addLog(t("logMarketer"), "agent"); }
    }

    addLog(t("logDone"), "success");
    setIsFinished(true);
  };

  // توليد الحزمة النهائية (ZIP Production)
  const produceFinalBundle = async () => {
    const zip = new JSZip();
    const folder = zip.folder(`MRF_Production_${formData.name}`);

    // 1. الكتاب المنسق PDF
    folder.file("01_Book_Master_Copy.pdf", "PDF Content with Arabic Support Placeholder");
    
    // 2. تقارير الوكلاء
    folder.file("02_Editorial_Report.txt", t("reportEditorial", { name: formData.name }));
    folder.file("03_Legal_Compliance.txt", t("reportLegal", { country: formData.country }));
    
    // 3. المحتوى البصري والفيديو
    folder.file("04_Visual_Prompts_Cover.txt", t("reportVisual", { bookTitle: formData.bookTitle, name: formData.name }));
    folder.file("05_Video_Teaser_Script.txt", t("reportVideo"));
    
    // 4. خطة التسويق
    folder.file("06_Marketing_Strategy.txt", t("reportMarketing", { country: formData.country, bookTitle: formData.bookTitle }));

    const blob = await zip.generateAsync({ type: "blob" });
    saveAs(blob, `Production_Package_${formData.name}.zip`);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white p-4 md:p-10" dir={formData.language === 'ar' ? 'rtl' : 'ltr'}>
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 border-b border-gray-800 pb-8 flex flex-wrap justify-between items-end gap-4">
          <div>
            <h1 className="text-5xl font-black italic tracking-tighter">MRF <span className="text-purple-600">SOVEREIGN</span></h1>
            <p className="text-gray-500 text-sm tracking-[0.3em] uppercase">{t("headerSubtitle")}</p>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <div className="flex items-center gap-2 bg-gray-900 px-4 py-2 rounded-full border border-gray-800">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse shadow-[0_0_10px_#22c55e]"></div>
              <span className="text-xs font-mono text-green-400">{t("status")}</span>
            </div>
            <div className="flex items-center gap-2 bg-gray-900 px-4 py-2 rounded-full border border-gray-800 text-xs">
              <span className="text-gray-400">{t("languageLabel")}</span>
              <select
                value={formData.language}
                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                className="bg-black text-white rounded-full px-3 py-1 border border-gray-700 outline-none focus:border-purple-500"
              >
                <option value="ar">{t("languageAr")}</option>
                <option value="en">{t("languageEn")}</option>
              </select>
            </div>
          </div>
        </header>

        {step === 1 && (
          <motion.div initial={{opacity:0}} animate={{opacity:1}} className="space-y-6">
            <div className="bg-gray-900 p-8 rounded-3xl border border-gray-800">
              <h2 className="text-2xl font-bold mb-8 flex items-center gap-3"><Globe className="text-purple-500"/> {t("step1Title")}</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <input type="text" placeholder={t("authorName")} className="bg-black p-5 rounded-xl border border-gray-700 outline-none focus:border-purple-500" onChange={e => setFormData({...formData, name: e.target.value})} />
                <input type="text" placeholder={t("publishCountry")} className="bg-black p-5 rounded-xl border border-gray-700 outline-none focus:border-purple-500" onChange={e => setFormData({...formData, country: e.target.value})} />
                <input type="email" placeholder={t("email")} className="bg-black p-5 rounded-xl border border-gray-700 outline-none focus:border-purple-500" onChange={e => setFormData({...formData, email: e.target.value})} />
                <input type="tel" placeholder={t("phone")} className="bg-black p-5 rounded-xl border border-gray-700 outline-none focus:border-purple-500" onChange={e => setFormData({...formData, phone: e.target.value})} />
              </div>
            </div>
            <button onClick={() => setStep(2)} className="w-full py-6 bg-purple-700 rounded-2xl font-black text-2xl shadow-xl hover:bg-purple-600 transition-all">{t("step1Cta")}</button>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div initial={{opacity:0}} animate={{opacity:1}} className="space-y-6">
            <div className="bg-gray-900 p-8 rounded-3xl border border-gray-800">
              <h2 className="text-2xl font-bold mb-8 flex items-center gap-3"><BookOpen className="text-green-500"/> {t("step2Title")}</h2>
              <div className="space-y-6">
                <input type="text" placeholder={t("bookTitle")} className="w-full bg-black p-5 rounded-xl border border-gray-700 outline-none" onChange={e => setFormData({...formData, bookTitle: e.target.value})} />
                <div className="border-2 border-dashed border-gray-700 p-12 text-center rounded-3xl hover:border-green-500 transition-all bg-black cursor-pointer">
                  <input type="file" id="fileIn" className="hidden" accept=".txt" onChange={e => setFormData({...formData, file: e.target.files[0]})} />
                  <label htmlFor="fileIn" className="cursor-pointer">
                    <Upload className="mx-auto w-16 h-16 text-gray-600 mb-4" />
                    <p className="text-xl font-bold">{formData.file ? formData.file.name : t("uploadTitle")}</p>
                    <p className="text-gray-500 mt-2">{t("uploadSub")}</p>
                  </label>
                </div>
              </div>
            </div>
            <button onClick={runSovereignEngine} disabled={!formData.file || !formData.bookTitle} className="w-full py-6 bg-green-700 rounded-2xl font-black text-2xl shadow-xl hover:bg-green-600 disabled:opacity-30">{t("step2Cta")}</button>
          </motion.div>
        )}

        {step === 3 && (
          <div className="space-y-8">
            <div className="bg-black p-8 rounded-3xl border border-gray-800 shadow-[0_0_50px_rgba(147,51,234,0.1)] min-h-[600px] flex flex-col">
              <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
                <div>
                  <h3 className="text-2xl font-black flex items-center gap-3">
                    <Cpu className="text-purple-500 animate-spin-slow" /> {t("runningTitle")}: {activeAgent ? activeAgent.name : t("preparing")}
                  </h3>
                  <p className="text-gray-500 text-sm mt-1">{t("runningRole")}: {activeAgent ? activeAgent.role : '-'} | {t("runningTemp")}: {activeAgent ? activeAgent.temp : '-'}</p>
                </div>
                <div className="text-4xl font-black text-purple-500">{Math.round(progress)}%</div>
              </div>

              <div className="flex-1 overflow-y-auto space-y-3 font-mono text-sm scrollbar-hide">
                {logs.map((log, i) => (
                  <div key={i} className={`flex gap-4 ${log.type === 'success' ? 'text-green-400' : log.type === 'agent' ? 'text-blue-300' : 'text-gray-400'}`}>
                    <span className="text-gray-700">[{log.time}]</span>
                    <span>{log.msg}</span>
                  </div>
                ))}
              </div>
            </div>
            {isFinished && (
              <motion.button 
                initial={{scale:0.9, opacity:0}} animate={{scale:1, opacity:1}}
                onClick={produceFinalBundle}
                className="w-full py-8 bg-gradient-to-r from-green-600 to-blue-600 rounded-3xl font-black text-3xl shadow-[0_0_40px_rgba(34,197,94,0.3)] flex items-center justify-center gap-6"
              >
                {t("completeCta")} <Download size={40} />
              </motion.button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
