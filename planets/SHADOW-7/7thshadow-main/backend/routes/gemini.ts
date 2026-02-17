import { Router } from 'express';
import { GoogleGenAI } from '@google/genai';
import { APIError } from '../middleware/errorHandler.js';

export const geminiRouter = Router();

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

if (!GEMINI_API_KEY) {
  console.error('⚠️ GEMINI_API_KEY is not set!');
}

const ai = GEMINI_API_KEY ? new GoogleGenAI({ apiKey: GEMINI_API_KEY }) : null;

// POST /api/gemini/generate - Unified endpoint
geminiRouter.post('/generate', async (req, res, next) => {
  try {
    if (!ai) {
      throw new APIError('Gemini API not configured', 503);
    }

    const { prompt, model = 'gemini-3-flash-preview' } = req.body;

    if (!prompt) {
      throw new APIError('Prompt is required', 400);
    }

    const response = await ai.models.generateContent({
      model,
      contents: [{ text: prompt }]
    });
    
    res.json({
      result: response.text || '',
      metadata: {
        model,
        timestamp: new Date().toISOString()
      }
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Generation failed', 500));
  }
});

export default geminiRouter;
