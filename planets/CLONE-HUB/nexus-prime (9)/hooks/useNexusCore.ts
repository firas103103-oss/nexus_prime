
import { useState, useCallback, useEffect } from 'react';
import { analyzeData } from '../services/geminiService.ts';
import { NexusState, NexusReport, DialoguePacket } from '../types.ts';

export const useNexusCore = () => {
  const [language, setLanguage] = useState<'ar' | 'en' | null>(null);
  const [visualMode, setVisualMode] = useState<NexusState['visual_mode']>('INTRO_MODE');
  const [accentColor, setAccentColor] = useState('#FFFFFF');
  const [overlayMessage, setOverlayMessage] = useState('');
  const [report, setReport] = useState<NexusReport | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [hiveDialogue, setHiveDialogue] = useState<DialoguePacket[]>([]);

  // Memory persistence
  useEffect(() => {
    const savedLang = localStorage.getItem('nexus_lang');
    if (savedLang) {
        // Restore state without playing intro again if reloading
        setLanguage(savedLang as 'ar' | 'en');
        setVisualMode('VOID_IDLE');
        setAccentColor('#00F2FF');
    }
  }, []);

  const getAgentColor = (agent: string) => {
    switch(agent) {
        case 'VISUAL_CORE': return '#00F2FF'; 
        case 'SECURITY_OPS': return '#FF003C'; 
        case 'DATA_MINER': return '#FFD700';
        default: return '#FFFFFF';
    }
  };

  const speakPacket = (text: string, agent: string): Promise<void> => {
    return new Promise((resolve) => {
      if (!window.speechSynthesis) { resolve(); return; }
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = language === 'ar' ? 'ar-SA' : 'en-US';
      
      switch (agent) {
          case 'VISUAL_CORE': u.pitch = 1.2; u.rate = 1.2; break;
          case 'SECURITY_OPS': u.pitch = 0.6; u.rate = 0.9; break;
          case 'DATA_MINER': u.pitch = 1.0; u.rate = 1.1; break;
          case 'EXECUTIVE': u.pitch = 0.9; u.rate = 1.0; break;
          case 'THINKER': u.pitch = 1.1; u.rate = 1.1; break;
      }
      
      if(language === 'ar') {
         const voices = window.speechSynthesis.getVoices();
         const arVoice = voices.find(v => v.lang.includes('ar'));
         if(arVoice) u.voice = arVoice;
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
    
    const text = lang === 'ar' ? "نظام نكسوس متصل. أنا جاهز." : "NEXUS Online. Systems Ready.";
    await speakPacket(text, 'THINKER');
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve((reader.result as string).split(',')[1]);
      reader.onerror = error => reject(error);
    });
  };

  const processInput = useCallback(async (text: string, file: File | null = null) => {
    if (!language) return;
    setIsProcessing(true);
    setReport(null);
    setVisualMode('GRAVITY_WELL_ACTIVE');
    setOverlayMessage(language === 'ar' ? 'تحليل البيانات...' : 'ANALYZING...');
    
    try {
      let fileData = null;
      if (file) fileData = { base64: await fileToBase64(file), mimeType: file.type };

      const data = await analyzeData(text, fileData, language);
      setHiveDialogue(data.hive_mind_dialogue);

      for (const packet of data.hive_mind_dialogue) {
        setOverlayMessage(`[${packet.agent}] PROCESSING...`);
        setAccentColor(getAgentColor(packet.agent));
        await speakPacket(packet.text, packet.agent);
      }

      setVisualMode(data.ux_orchestration.visual_state);
      setAccentColor(data.ux_orchestration.hex_accent);
      setOverlayMessage(data.ux_orchestration.ui_message_overlay);
      setReport(data.data_payload);
      
      await speakPacket(data.final_voice_script, 'EXECUTIVE');

    } catch (e) {
      console.error(e);
      setVisualMode('VOID_IDLE');
      setOverlayMessage("SYSTEM ERROR");
      setAccentColor('#FF0000');
      await speakPacket("Error in processing.", 'SECURITY_OPS');
    } finally {
      setIsProcessing(false);
    }
  }, [language]);

  const purgeSystem = () => {
      window.speechSynthesis.cancel();
      setReport(null);
      setVisualMode('VOID_IDLE');
      setOverlayMessage("SYSTEM PURGED");
      setAccentColor('#FF0000');
      setTimeout(() => setAccentColor('#00F2FF'), 1000);
  };

  return { language, visualMode, accentColor, overlayMessage, report, processInput, isProcessing, selectLanguage, purgeSystem, hiveDialogue };
};
