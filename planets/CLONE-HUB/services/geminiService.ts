
import { GoogleGenAI, Type, Modality } from "@google/genai";
import type { AIResponse } from '../types.ts';

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

const schema = {
  type: Type.OBJECT,
  properties: {
    ux_orchestration: {
      type: Type.OBJECT,
      properties: {
        visual_state: { type: Type.STRING, enum: ["VOID_IDLE", "GRAVITY_WELL_ACTIVE", "PANORAMIC_DASHBOARD"] },
        hex_accent: { type: Type.STRING },
        ui_message_overlay: { type: Type.STRING }
      },
      required: ["visual_state", "hex_accent", "ui_message_overlay"]
    },
    hive_mind_dialogue: {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          agent: { type: Type.STRING, enum: ['VISUAL_CORE', 'SECURITY_OPS', 'DATA_MINER', 'EXECUTIVE'] },
          text: { type: Type.STRING }
        },
        required: ["agent", "text"]
      }
    },
    final_voice_script: { type: Type.STRING },
    data_payload: {
      type: Type.OBJECT,
      properties: {
        title: { type: Type.STRING },
        executive_summary: { type: Type.STRING },
        deep_analysis_markdown: { type: Type.STRING },
        professional_verdict: { type: Type.STRING }
      },
      required: ["title", "executive_summary", "deep_analysis_markdown", "professional_verdict"]
    }
  },
  required: ["ux_orchestration", "hive_mind_dialogue", "final_voice_script", "data_payload"]
};

interface SmartFileData {
    type: 'binary' | 'text';
    data: string;
    mimeType: string;
}

/**
 * Helper to wrap API calls with retry logic for 429 errors
 */
async function callWithRetry(fn: () => Promise<any>, retries = 3, delay = 2000): Promise<any> {
    try {
        return await fn();
    } catch (error: any) {
        const isQuotaError = error?.message?.includes('429') || error?.message?.includes('RESOURCE_EXHAUSTED');
        if (isQuotaError && retries > 0) {
            console.warn(`Quota exceeded. Retrying in ${delay}ms... (${retries} left)`);
            await new Promise(res => setTimeout(res, delay));
            return callWithRetry(fn, retries - 1, delay * 2); // Exponential backoff
        }
        throw error;
    }
}

export async function analyzeData(input: string, file: SmartFileData | null, lang: 'ar' | 'en'): Promise<AIResponse> {
  const langInstruction = lang === 'ar' 
    ? "Language: Arabic (Modern Tech Dialect). Tone: Strategic Expert. Use natural, human expressions."
    : "Language: English (Tech Ops). Tone: Cyber Commander.";

  return callWithRetry(async () => {
    const contentParts: any[] = [];
    let promptText = `INPUT COMMAND: "${input}". ${langInstruction}`;

    if (file) {
        if (file.type === 'text') {
            promptText += `\n\n[ATTACHED FILE CONTENT - ${file.mimeType}]:\n${file.data}\n[END OF FILE]`;
        } else {
            contentParts.push({ inlineData: { data: file.data, mimeType: file.mimeType } });
        }
    }
    contentParts.push({ text: promptText });

    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview", // Switched to Flash for higher quota/speed
      contents: { parts: contentParts },
      config: {
        responseMimeType: "application/json",
        responseSchema: schema,
        systemInstruction: `You are NEXUS PRIME. Perform DEEP FORENSIC ANALYSIS. Deliver professional, human-sounding reports.`
      },
    });

    if (!response.text) throw new Error("Empty response from AI core");
    return JSON.parse(response.text.trim()) as AIResponse;
  });
}

export async function generateHighQualitySpeech(text: string, lang: 'ar' | 'en'): Promise<string> {
    return callWithRetry(async () => {
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash-preview-tts",
            contents: [{ parts: [{ text: `${lang === 'ar' ? 'بصوت واثق وفصيح: ' : 'In a confident and professional voice: '}${text}` }] }],
            config: {
                responseModalities: [Modality.AUDIO],
                speechConfig: {
                    voiceConfig: {
                        prebuiltVoiceConfig: { voiceName: lang === 'ar' ? 'Kore' : 'Charon' },
                    },
                },
            },
        });

        const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
        if (!base64Audio) throw new Error("No audio data returned");
        return base64Audio;
    });
}
