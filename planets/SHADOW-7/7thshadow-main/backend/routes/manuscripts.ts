import { Router } from 'express';
import { 
  createManuscript, 
  getManuscriptById, 
  updateManuscript, 
  getUserManuscripts,
  createProcessingHistory,
  updateProcessingHistory
} from '../db/supabase.js';
import { APIError } from '../middleware/errorHandler.js';

export const manuscriptsRouter = Router();

// GET /api/manuscripts - Get all user manuscripts
manuscriptsRouter.get('/', async (req, res, next) => {
  try {
    const userId = req.headers['x-user-id'] as string;
    
    if (!userId) {
      throw new APIError('User ID required', 401);
    }

    const manuscripts = await getUserManuscripts(userId);
    
    res.json({
      manuscripts,
      count: manuscripts.length
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to fetch manuscripts', 500));
  }
});

// GET /api/manuscripts/:id - Get specific manuscript
manuscriptsRouter.get('/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string;

    const manuscript = await getManuscriptById(id);
    
    if (!manuscript) {
      throw new APIError('Manuscript not found', 404);
    }

    // Check ownership
    if (manuscript.user_id !== userId && userId) {
      throw new APIError('Unauthorized', 403);
    }

    res.json({ manuscript });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to fetch manuscript', 500));
  }
});

// POST /api/manuscripts - Create new manuscript
manuscriptsRouter.post('/', async (req, res, next) => {
  try {
    const userId = req.headers['x-user-id'] as string || 'anonymous';
    const { 
      title, 
      author, 
      genre, 
      language, 
      originalText, 
      wordCount,
      metadata 
    } = req.body;

    if (!title || !originalText) {
      throw new APIError('Title and original text are required', 400);
    }

    const manuscript = await createManuscript({
      user_id: userId,
      title,
      author: author || 'Unknown',
      genre: genre || 'General',
      language: language || 'ar',
      original_text: originalText,
      word_count: wordCount || 0,
      status: 'uploaded',
      metadata: metadata || {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });

    res.status(201).json({ 
      manuscript,
      message: 'Manuscript created successfully' 
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to create manuscript', 500));
  }
});

// PATCH /api/manuscripts/:id - Update manuscript
manuscriptsRouter.patch('/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string;
    const updates = req.body;

    // Get existing manuscript
    const existing = await getManuscriptById(id);
    
    if (!existing) {
      throw new APIError('Manuscript not found', 404);
    }

    // Check ownership
    if (existing.user_id !== userId && userId) {
      throw new APIError('Unauthorized', 403);
    }

    // Update manuscript
    const manuscript = await updateManuscript(id, updates);

    res.json({ 
      manuscript,
      message: 'Manuscript updated successfully' 
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to update manuscript', 500));
  }
});

// POST /api/manuscripts/:id/process - Start processing
manuscriptsRouter.post('/:id/process', async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string || 'anonymous';
    const { step, options } = req.body;

    // Get manuscript
    const manuscript = await getManuscriptById(id);
    
    if (!manuscript) {
      throw new APIError('Manuscript not found', 404);
    }

    // Update manuscript status
    await updateManuscript(id, { status: 'processing' });

    // Create processing history entry
    const history = await createProcessingHistory({
      manuscript_id: id,
      user_id: userId,
      step: step || 'analysis',
      status: 'pending',
      progress: 0,
      started_at: new Date().toISOString()
    });

    res.json({
      message: 'Processing started',
      historyId: history.id,
      status: 'processing'
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to start processing', 500));
  }
});

// GET /api/manuscripts/:id/history - Get processing history
manuscriptsRouter.get('/:id/history', async (req, res, next) => {
  try {
    const { id } = req.params;

    // This would fetch from processing_history table
    // Simplified for now
    res.json({
      history: [],
      message: 'History endpoint - to be implemented'
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to fetch history', 500));
  }
});

export default manuscriptsRouter;
