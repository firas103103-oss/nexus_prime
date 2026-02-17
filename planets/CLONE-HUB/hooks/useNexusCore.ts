
import { useState, useCallback, useEffect, useRef } from 'react';
import { analyzeData, generateHighQualitySpeech } from '../services/geminiService.ts';
import { NexusState, NexusReport, DialoguePacket } from '../types.ts';

function decodeBase64(base64: string) {
  const binaryString = atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes;
}

async function decodeAudioData(
  data: Uint8Array,
  ctx: AudioContext,
  sampleRate: number = 24000,
  numChannels: number = 1,
): Promise<AudioBuffer> {
  const dataInt16 = new Int16Array(data.buffer);
  const frameCount = dataInt16.length / numChannels;
  const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);

  for (let channel = 0; channel < numChannels; channel++) {
    const channelData = buffer.getChannelData(channel);
    for (let i = 0; i < frameCount; i++) {
      channelData[i] = dataInt16[i * numChannels + channel] / 32768.0;
    }
  }
  return buffer;
}

export const useNexusCore = () => {
  const [language, setLanguage] = useState<'ar' | 'en' | null>(null);
  const [visualMode, setVisualMode] = useState<NexusState['visual_mode']>('INTRO_MODE');
  const [accentColor, setAccentColor] = useState('#FFFFFF');
  const [overlayMessage, setOverlayMessage] = useState('');
  const [report, setReport] = useState<NexusReport | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [hiveDialogue, setHiveDialogue] = useState<DialoguePacket[]>([]);
  const [lastHqAudio, setLastHqAudio] = useState<string | null>(null);
  
  const audioContextRef = useRef<AudioContext | null>(null);

  useEffect(() => {
    const savedLang = localStorage.getItem('nexus_lang');
    if (savedLang) {
        setLanguage(savedLang as 'ar' | 'en');
        setVisualMode('VOID_IDLE');
        setAccentColor('#00F2FF');
    }
    return () => { if(audioContextRef.current) audioContextRef.current.close(); };
  }, []);

  const getAgentColor = (agent: string) => {
    switch(agent) {
        case 'VISUAL_CORE': return '#00F2FF'; 
        case 'SECURITY_OPS': return '#FF003C'; 
        case 'DATA_MINER': return '#FFD700';
        default: return '#FFFFFF';
    }
  };

  const playHumanVoice = async (base64Audio: string) => {
      if (!audioContextRef.current) {
          audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
      }
      const ctx = audioContextRef.current;
      const audioBytes = decodeBase64(base64Audio);
      const audioBuffer = await decodeAudioData(audioBytes, ctx, 24000, 1);
      
      const source = ctx.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(ctx.destination);
      
      return new Promise<void>((resolve) => {
          source.onended = () => resolve();
          source.start();
      });
  };

  const speakPacket = (text: string, agent: string): Promise<void> => {
    return new Promise((resolve) => {
      if (!window.speechSynthesis) { resolve(); return; }
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = language === 'ar' ? 'ar-SA' : 'en-US';
      switch (agent) {
          case 'VISUAL_CORE': u.pitch = 1.3; u.rate = 1.2; break;
          case 'SECURITY_OPS': u.pitch = 0.5; u.rate = 0.8; break;
          case 'DATA_MINER': u.pitch = 1.0; u.rate = 1.1; break;
          case 'EXECUTIVE': u.pitch = 0.8; u.rate = 1.0; break;
          case 'THINKER': u.pitch = 1.1; u.rate = 1.1; break;
      }
      u.onend = () => resolve();
      u.onerror = () => resolve();
      window.speechSynthesis.speak(u);
    });
  };

  const selectLanguage = async (lang: 'ar' | 'en') => {
    setLanguage(lang);
    localStorage.setItem('nexus_lang', lang);
    setVisualMode('VOID_IDLE');
    setAccentColor('#00F2FF');
    const welcome = lang === 'ar' ? "نظام نكسوس متصل. بانتظار أوامرك." : "NEXUS Online. Systems Ready.";
    await speakPacket(welcome, 'THINKER');
  };

  const smartReadFile = (file: File): Promise<{ type: 'binary' | 'text', data: string, mimeType: string }> => {
    return new Promise((resolve, reject) => {
      const MAX_SIZE = 10 * 1024 * 1024;
      if (file.size > MAX_SIZE) {
          reject(new Error(language === 'ar' ? "الملف كبير جداً" : "File too large"));
          return;
      }
      const SUPPORTED_BINARY_MIMES = ['application/pdf', 'image/png', 'image/jpeg', 'image/webp', 'image/heic', 'image/heif', 'audio/wav', 'audio/mp3', 'audio/mpeg', 'video/mp4'];
      let mimeType = file.type;
      const isStrictBinary = SUPPORTED_BINARY_MIMES.includes(mimeType);
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          if (!isStrictBinary) resolve({ type: 'text', data: reader.result, mimeType: mimeType || 'text/plain' });
          else resolve({ type: 'binary', data: reader.result.split(',')[1], mimeType: mimeType });
        } else reject(new Error("Read failed"));
      };
      if (!isStrictBinary) reader.readAsText(file);
      else reader.readAsDataURL(file);
    });
  };

  const processInput = useCallback(async (text: string, file: File | null = null) => {
    if (!language || isProcessing) return;
    setIsProcessing(true);
    setReport(null);
    setLastHqAudio(null);
    setVisualMode('GRAVITY_WELL_ACTIVE');
    setOverlayMessage(language === 'ar' ? 'بدء التحليل...' : 'INITIATING...');
    
    try {
      let fileData = null;
      if (file) {
          setOverlayMessage(language === 'ar' ? 'فحص الملف...' : 'SCANNING FILE...');
          fileData = await smartReadFile(file);
      }

      const data = await analyzeData(text, fileData, language);
      setHiveDialogue(data.hive_mind_dialogue);

      for (const packet of data.hive_mind_dialogue) {
        setOverlayMessage(`[${packet.agent}] PROCESSING...`);
        setAccentColor(getAgentColor(packet.agent));
        await speakPacket(packet.text, packet.agent);
      }

      setOverlayMessage(language === 'ar' ? 'توليد الإيجاز الصوتي...' : 'GENERATING BRIEFING...');
      const hqAudioBase64 = await generateHighQualitySpeech(data.final_voice_script, language);
      setLastHqAudio(hqAudioBase64);

      setVisualMode(data.ux_orchestration.visual_state);
      setAccentColor(data.ux_orchestration.hex_accent);
      setOverlayMessage(data.ux_orchestration.ui_message_overlay);
      setReport(data.data_payload);
      
      await playHumanVoice(hqAudioBase64);

    } catch (e: any) {
      console.error(e);
      setVisualMode('VOID_IDLE');
      setAccentColor('#FF0000');
      
      const isQuota = e?.message?.includes('429') || e?.message?.includes('RESOURCE_EXHAUSTED');
      if (isQuota) {
          setOverlayMessage(language === 'ar' ? "نفدت حصة الاستخدام. انتظر دقيقة." : "QUOTA EXCEEDED. WAIT 1 MIN.");
          await speakPacket(language === 'ar' ? "تم تجاوز حدود الاستخدام، يرجى المحاولة بعد دقيقة واحدة." : "Usage limit exceeded, please try again in one minute.", 'SECURITY_OPS');
      } else {
          setOverlayMessage("ANALYSIS FAILED");
          await speakPacket("Error detected in neural link.", 'SECURITY_OPS');
      }
    } finally {
      setIsProcessing(false);
    }
  }, [language, isProcessing]);

  const purgeSystem = () => {
      window.speechSynthesis.cancel();
      if(audioContextRef.current) audioContextRef.current.suspend();
      setReport(null);
      setLastHqAudio(null);
      setVisualMode('VOID_IDLE');
      setOverlayMessage("SYSTEM RESET");
      setAccentColor('#00F2FF');
  };

  return { language, visualMode, accentColor, overlayMessage, report, processInput, isProcessing, selectLanguage, purgeSystem, hiveDialogue, lastHqAudio };
};
