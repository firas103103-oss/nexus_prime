
import React, { useState, useRef } from 'react';
import { useNexusCore } from './hooks/useNexusCore.ts';
import { VoidScene } from './components/VoidScene.tsx';
import { DashboardDisplay } from './components/DashboardDisplay.tsx';
import { generateSmartHTMLReport } from './utils/reportGenerator.ts';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, FileText, Trash2 } from 'lucide-react';

function App() {
  const { language, visualMode, accentColor, overlayMessage, report, processInput, selectLanguage, purgeSystem, isProcessing, hiveDialogue } = useNexusCore();
  const [inputValue, setInputValue] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); 
    if (e.dataTransfer.files[0]) processInput("Analyze this file.", e.dataTransfer.files[0]);
  };

  const handleDownload = () => {
    if (!report || !language) return;
    // Note: Passing empty finalScript here as it might not be stored in report object, 
    // ideally it should be, but for now we follow the type signature.
    const html = generateSmartHTMLReport(report, hiveDialogue, language);
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `NEXUS_INTEL_${Date.now()}.html`;
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
  };

  return (
    <main className={`relative w-full min-h-screen bg-[#020202] text-white flex flex-col items-center justify-between overflow-hidden ${language === 'ar' ? 'font-[Cairo]' : 'font-mono'}`}
      dir={language === 'ar' ? 'rtl' : 'ltr'}
      onDragOver={(e) => e.preventDefault()} onDrop={handleDrop}
    >
      <VoidScene visualMode={visualMode} accentColor={accentColor} />
      
      {/* Intro Screen */}
      <AnimatePresence>
        {visualMode === 'INTRO_MODE' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, scale: 1.5, filter: "blur(20px)" }} className="z-50 absolute inset-0 bg-black flex flex-col items-center justify-center gap-12">
            <div className="text-center space-y-4">
                <h1 className="text-7xl md:text-9xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white via-gray-400 to-gray-900 animate-pulse">NEXUS</h1>
                <p className="text-gray-500 tracking-[0.5em] text-sm uppercase">Quantum Data Core</p>
            </div>
            <div className="flex gap-12 items-center mt-8">
              <button onClick={() => selectLanguage('ar')} className="text-4xl font-bold hover:text-cyan-400 transition-all hover:scale-110 font-[Cairo]">العربية</button>
              <div className="w-[1px] h-24 bg-white/20"></div>
              <button onClick={() => selectLanguage('en')} className="text-4xl font-bold hover:text-cyan-400 transition-all hover:scale-110 font-mono">ENGLISH</button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main UI */}
      {visualMode !== 'INTRO_MODE' && (
        <div className="z-10 w-full h-full flex flex-col justify-between py-12 px-6 pointer-events-none">
          <div className="flex justify-between w-full max-w-5xl mx-auto pointer-events-auto">
             <div className="text-xs text-gray-500">{language === 'ar' ? 'النظام: متصل' : 'SYSTEM: ONLINE'}</div>
             {report && <button onClick={purgeSystem} className="text-red-500 hover:text-red-300 transition"><Trash2 size={20} /></button>}
          </div>

          <div className="w-full max-w-5xl mx-auto flex flex-col items-center gap-6">
            <motion.div className="text-center">
              <h1 className="text-xl md:text-3xl font-light tracking-[0.2em] opacity-90 transition-colors duration-500"
                style={{ color: accentColor, textShadow: `0 0 20px ${accentColor}40`, fontFamily: language === 'ar' ? "'Cairo', sans-serif" : '' }}>
                {overlayMessage || (language === 'ar' ? "بانتظار البيانات..." : "AWAITING INPUT...")}
              </h1>
            </motion.div>

            {report && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full flex flex-col items-center pointer-events-auto bg-black/60 backdrop-blur-xl p-8 rounded-2xl border border-white/5 shadow-2xl">
                 <DashboardDisplay data={report} color={accentColor} />
                 <div className="flex justify-center mt-8 gap-6">
                    <button onClick={handleDownload} className="px-8 py-3 bg-white/5 border border-white/20 rounded-full hover:bg-white/10 transition uppercase tracking-widest text-sm flex items-center gap-2 hover:border-cyan-400 hover:text-cyan-400">
                        <Download size={18} /> {language === 'ar' ? "تحميل التقرير الذكي" : "DOWNLOAD SMART INTEL"}
                    </button>
                 </div>
              </motion.div>
            )}

            {!report && !isProcessing && (
              <div className="w-full max-w-3xl pointer-events-auto mt-4">
                 <div className="flex gap-4 items-center bg-black/40 backdrop-blur-md p-2 rounded-full border border-white/10 hover:border-white/20 transition-all hover:shadow-[0_0_20px_rgba(0,242,255,0.1)]">
                    <input type="file" ref={fileInputRef} onChange={(e) => { if(e.target.files?.[0]) processInput("Analyze this.", e.target.files[0]) }} className="hidden" />
                    <button onClick={() => fileInputRef.current?.click()} className="p-3 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 hover:text-cyan-400 transition"><FileText size={20} /></button>
                    <input type="text" value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter' && inputValue) processInput(inputValue) }}
                      placeholder={language === 'ar' ? "اكتب الأمر أو اسحب الملفات..." : "Type command or drop files..."}
                      className="flex-1 bg-transparent border-none text-center text-lg focus:outline-none placeholder-white/20 h-10" style={{ caretColor: accentColor }} autoFocus />
                 </div>
              </div>
            )}
          </div>
        </div>
      )}
    </main>
  );
}
export default App;
