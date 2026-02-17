
import type { NexusReport, DialoguePacket } from '../types.ts';

export const generateSmartHTMLReport = (report: NexusReport, dialogue: DialoguePacket[], language: 'ar' | 'en', finalScript?: string) => {
  const isAr = language === 'ar';
  const fontFamily = isAr ? "'Cairo', sans-serif" : "'Courier New', monospace";
  const dir = isAr ? "rtl" : "ltr";
  
  // Safe stringification for embedding
  const dialogueJSON = JSON.stringify(dialogue).replace(/\\/g, '\\\\').replace(/"/g, '&quot;');
  const safeFinalScript = (finalScript || '').replace(/\\/g, '\\\\').replace(/"/g, '\\"');
  
  // Extract accent color from context or default
  // Note: In a real app we might pass the actual color used, here we default to Cyan if not found in report data structure which is strictly the payload
  const accentColor = '#00F2FF'; 

  return `<!DOCTYPE html>
<html lang="${language}" dir="${dir}">
<head>
    <meta charset="UTF-8">
    <title>NEXUS INTEL - ${new Date().toLocaleDateString()}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { background: #050505; color: #e0e0e0; font-family: ${fontFamily}; margin: 40px; }
        .header { border-bottom: 2px solid ${accentColor}; padding-bottom: 20px; display: flex; justify-content: space-between; }
        .logo { font-size: 24px; color: ${accentColor}; letter-spacing: 4px; font-weight: bold; }
        .section { background: rgba(255,255,255,0.03); border: 1px solid #333; padding: 20px; margin-top: 20px; border-radius: 8px; }
        .label { color: ${accentColor}; font-size: 12px; letter-spacing: 2px; display: block; margin-bottom: 10px; border-bottom: 1px solid #333; }
        .verdict { border: 1px solid ${accentColor}; color: ${accentColor}; padding: 15px; text-align: center; font-weight: bold; font-size: 1.2em; }
        .chat-entry { padding: 8px; border-left: 3px solid #444; background: rgba(0,0,0,0.3); margin-bottom: 5px; }
        .btn { background: ${accentColor}; color: #000; border: none; padding: 15px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 20px; font-family: inherit; font-size: 16px; }
        .btn:hover { background: #fff; box-shadow: 0 0 15px ${accentColor}; }
        pre { white-space: pre-wrap; color: #aaa; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">NEXUS PRIME</div>
        <div>CONFIDENTIAL // ${new Date().toLocaleString()}</div>
    </div>
    <div class="section">
        <span class="label">${isAr ? "الحكم النهائي" : "VERDICT"}</span>
        <div class="verdict">${report.professional_verdict}</div>
    </div>
    <div class="section">
        <span class="label">${isAr ? "الملخص" : "SUMMARY"}</span>
        <p>${report.executive_summary}</p>
    </div>
    <div class="section">
        <span class="label">${isAr ? "سجل العقل الجمعي" : "HIVE MIND LOG"}</span>
        ${dialogue.map(t => `<div class="chat-entry"><strong style="color:${accentColor}">${t.agent}:</strong> ${t.text}</div>`).join('')}
    </div>
    <div class="section">
        <span class="label">${isAr ? "التحليل التقني" : "DEEP ANALYSIS"}</span>
        <pre>${report.deep_analysis_markdown}</pre>
    </div>
    <button class="btn" onclick="playBriefing()">${isAr ? "🔊 تشغيل الإيجاز الصوتي" : "🔊 REPLAY AUDIO BRIEFING"}</button>
    <script>
        const dialogue = JSON.parse("${dialogueJSON}");
        const finalScript = "${safeFinalScript}";
        
        function playBriefing() {
            window.speechSynthesis.cancel();
            let chain = Promise.resolve();
            dialogue.forEach(p => chain = chain.then(() => speak(p.text, p.agent)));
            chain.then(() => speak(finalScript, 'EXECUTIVE'));
        }
        function speak(text, agent) {
            return new Promise(resolve => {
                const u = new SpeechSynthesisUtterance(text);
                u.lang = '${language}' === 'ar' ? 'ar-SA' : 'en-US';
                if (agent === 'VISUAL_CORE') { u.rate = 1.3; u.pitch = 1.2; }
                else if (agent === 'SECURITY_OPS') { u.rate = 0.9; u.pitch = 0.6; }
                else if (agent === 'EXECUTIVE') { u.rate = 1.0; u.pitch = 0.9; }
                u.onend = resolve; u.onerror = resolve;
                window.speechSynthesis.speak(u);
            });
        }
    </script>
</body>
</html>`;
};
