
import type { NexusReport, DialoguePacket } from '../types.ts';

/**
 * Generates a standalone HTML report with embedded high-quality audio briefing.
 */
export const generateSmartHTMLReport = (report: NexusReport, dialogue: DialoguePacket[], language: 'ar' | 'en', hqAudioBase64?: string) => {
  const isAr = language === 'ar';
  const fontFamily = isAr ? "'Cairo', sans-serif" : "'Courier New', monospace";
  const dir = isAr ? "rtl" : "ltr";
  const accentColor = '#00F2FF'; 

  // Helper to escape strings for JavaScript embedding
  const escapeJS = (str: string) => {
    return str
      .replace(/\\/g, '\\\\')
      .replace(/'/g, "\\'")
      .replace(/"/g, '\\"')
      .replace(/\n/g, '\\n')
      .replace(/\r/g, '\\r');
  };

  const escapedDialogue = JSON.stringify(dialogue);
  const escapedHqAudio = hqAudioBase64 || "";

  return `<!DOCTYPE html>
<html lang="${language}" dir="${dir}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS INTEL - ${report.title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --accent: ${accentColor}; --bg: #050505; --card: rgba(255,255,255,0.03); }
        body { background: var(--bg); color: #e0e0e0; font-family: ${fontFamily}; margin: 0; padding: 40px; display: flex; justify-content: center; }
        .container { max-width: 900px; w-full: 100%; }
        .header { border-bottom: 2px solid var(--accent); padding-bottom: 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .logo { font-size: 28px; color: var(--accent); letter-spacing: 6px; font-weight: bold; text-transform: uppercase; }
        .timestamp { font-family: monospace; opacity: 0.5; font-size: 12px; }
        .section { background: var(--card); border: 1px solid #333; padding: 30px; margin-top: 20px; border-radius: 16px; backdrop-filter: blur(10px); }
        .label { color: var(--accent); font-size: 11px; letter-spacing: 3px; display: block; margin-bottom: 15px; text-transform: uppercase; opacity: 0.8; }
        .verdict { border: 2px solid var(--accent); color: var(--accent); padding: 20px; text-align: center; font-weight: bold; font-size: 1.5em; border-radius: 12px; background: rgba(0,242,255,0.05); }
        .summary { font-size: 1.2em; line-height: 1.6; font-weight: 300; }
        .chat-entry { padding: 12px; border-inline-start: 4px solid var(--accent); background: rgba(255,255,255,0.02); margin-bottom: 8px; border-radius: 4px; font-size: 14px; }
        .chat-entry strong { color: var(--accent); margin-inline-end: 10px; }
        pre { white-space: pre-wrap; color: #aaa; font-family: monospace; font-size: 13px; line-height: 1.8; padding: 15px; background: #000; border-radius: 8px; border: 1px solid #222; }
        .btn { background: var(--accent); color: #000; border: none; padding: 20px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 30px; font-family: inherit; font-size: 18px; border-radius: 12px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); text-transform: uppercase; letter-spacing: 2px; }
        .btn:hover { background: #fff; box-shadow: 0 0 30px var(--accent); transform: scale(1.01); }
        .btn:active { transform: scale(0.99); }
        .audio-status { text-align: center; font-size: 12px; color: var(--accent); margin-top: 10px; opacity: 0; transition: opacity 0.3s; }
        .audio-playing .audio-status { opacity: 1; }
    </style>
</head>
<body class="${hqAudioBase64 ? 'has-audio' : ''}">
    <div class="container">
        <div class="header">
            <div class="logo">NEXUS PRIME</div>
            <div class="timestamp">SECURE_INTEL // ${new Date().toLocaleString()}</div>
        </div>

        <div class="section">
            <span class="label">${isAr ? "الحكم النهائي" : "PROFESSIONAL VERDICT"}</span>
            <div class="verdict">${report.professional_verdict}</div>
        </div>

        <div class="section">
            <span class="label">${isAr ? "ملخص الإدارة التنفيذية" : "EXECUTIVE SUMMARY"}</span>
            <div class="summary">${report.executive_summary}</div>
        </div>

        <div class="section">
            <span class="label">${isAr ? "سجل تحليل الوكلاء" : "AGENT ANALYSIS LOG"}</span>
            <div id="dialogue-container">
                ${dialogue.map(t => `<div class="chat-entry"><strong>${t.agent}:</strong> ${t.text}</div>`).join('')}
            </div>
        </div>

        <div class="section">
            <span class="label">${isAr ? "البيانات الفنية العميقة" : "DEEP TECHNICAL DATA"}</span>
            <pre>${report.deep_analysis_markdown}</pre>
        </div>

        <button id="play-btn" class="btn" onclick="toggleAudio()">
            🔊 ${isAr ? "تشغيل الإيجاز الصوتي البشري" : "PLAY HUMAN AUDIO BRIEFING"}
        </button>
        <div id="status" class="audio-status">${isAr ? "يتم الآن تشغيل الصوت عالي الجودة..." : "Streaming High-Quality Neural Audio..."}</div>
    </div>

    <script>
        const audioBase64 = "${escapedHqAudio}";
        let audioContext;
        let audioBuffer;
        let currentSource;

        // Optimized Decoder for Raw PCM (Gemini TTS Format)
        function decodeAudio(base64) {
            const binaryString = atob(base64);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            return bytes;
        }

        async function createAudioBuffer(data, ctx) {
            const dataInt16 = new Int16Array(data.buffer);
            const numChannels = 1;
            const sampleRate = 24000;
            const frameCount = dataInt16.length / numChannels;
            const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);
            const channelData = buffer.getChannelData(0);
            for (let i = 0; i < frameCount; i++) {
                channelData[i] = dataInt16[i] / 32768.0;
            }
            return buffer;
        }

        async function toggleAudio() {
            const btn = document.getElementById('play-btn');
            const status = document.getElementById('status');
            
            if (currentSource) {
                currentSource.stop();
                currentSource = null;
                btn.innerHTML = "🔊 ${isAr ? 'إعادة تشغيل الإيجاز الصوتي' : 'REPLAY AUDIO BRIEFING'}";
                document.body.classList.remove('audio-playing');
                return;
            }

            try {
                if (!audioContext) {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
                }
                
                if (!audioBuffer) {
                    const rawData = decodeAudio(audioBase64);
                    audioBuffer = await createAudioBuffer(rawData, audioContext);
                }

                currentSource = audioContext.createBufferSource();
                currentSource.buffer = audioBuffer;
                currentSource.connect(audioContext.destination);
                
                currentSource.onended = () => {
                    currentSource = null;
                    btn.innerHTML = "🔊 ${isAr ? 'إعادة تشغيل الإيجاز الصوتي' : 'REPLAY AUDIO BRIEFING'}";
                    document.body.classList.remove('audio-playing');
                };

                currentSource.start();
                btn.innerHTML = "⏹️ ${isAr ? 'إيقاف الصوت' : 'STOP AUDIO'}";
                document.body.classList.add('audio-playing');
            } catch (e) {
                console.error("Audio playback error:", e);
                alert("${isAr ? 'حدث خطأ أثناء تشغيل الصوت.' : 'Error playing audio briefing.'}");
            }
        }
    </script>
</body>
</html>`;
};
