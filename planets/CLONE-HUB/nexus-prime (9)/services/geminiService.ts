
import { GoogleGenAI, Type } from "@google/genai";
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

interface FileData {
    base64: string;
    mimeType: string;
}

export async function analyzeData(input: string, file: FileData | null, lang: 'ar' | 'en'): Promise<AIResponse> {
  const langInstruction = lang === 'ar' 
    ? "Language: Arabic (Modern Tech Dialect/White Dialect). Tone: Strategic Expert."
    : "Language: English (Tech Ops). Tone: Cyber Commander.";

  try {
    const contentParts: any[] = [{ text: `INPUT: "${input}". ${langInstruction}` }];
    
    if (file) {
        contentParts.push({
            inlineData: {
                data: file.base64,
                mimeType: file.mimeType
            }
        });
    }

    // Using gemini-1.5-pro as it is the current stable model supporting JSON Schema and Multimodal inputs.
    const response = await ai.models.generateContent({
      model: "gemini-1.5-pro",
      contents: { parts: contentParts },
      config: {
        responseMimeType: "application/json",
        responseSchema: schema,
        systemInstruction: `You are NEXUS PRIME, a sovereign Hive Mind.
        Your goal is DEEP FORENSIC ANALYSIS.
        
        AGENTS:
        - VISUAL_CORE: Scans patterns, pixels, OCR. (Fast, Robotic)
        - SECURITY_OPS: Threat detection, compliance. (Deep, Serious)
        - DATA_MINER: Value extraction, hidden intents. (Analytical)
        - EXECUTIVE: Final Verdict. (Authoritative)

        TASK:
        1. Create a real-time dialogue between agents analyzing the file.
        2. Deliver a professional verdict in the data payload.
        3. Visuals: Red (#FF003C) for risks, Cyan (#00F2FF) for safe, Gold (#FFD700) for value.
        
        IMPORTANT: 'final_voice_script' must be a concise, spoken summary by the EXECUTIVE agent.`
      },
    });

    if (!response.text) throw new Error("Empty response");
    return JSON.parse(response.text.trim()) as AIResponse;

  } catch (error) {
    console.error("Gemini API Error:", error);
    throw error;
  }
}
