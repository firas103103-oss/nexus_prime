import { Router } from 'express';
import { supabase } from '../db/supabase.js';
import { APIError } from '../middleware/errorHandler.js';

export const authRouter = Router();

// POST /api/auth/signup
authRouter.post('/signup', async (req, res, next) => {
  try {
    const { email, password, name } = req.body;

    if (!email || !password) {
      throw new APIError('Email and password are required', 400);
    }

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          name: name || email.split('@')[0]
        }
      }
    });

    if (error) {
      throw new APIError(error.message, 400);
    }

    res.status(201).json({
      user: data.user,
      session: data.session,
      message: 'User created successfully'
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Signup failed', 500));
  }
});

// POST /api/auth/login
authRouter.post('/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      throw new APIError('Email and password are required', 400);
    }

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) {
      throw new APIError(error.message, 401);
    }

    res.json({
      user: data.user,
      session: data.session,
      message: 'Login successful'
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Login failed', 500));
  }
});

// POST /api/auth/logout
authRouter.post('/logout', async (req, res, next) => {
  try {
    const { error } = await supabase.auth.signOut();

    if (error) {
      throw new APIError(error.message, 500);
    }

    res.json({
      message: 'Logout successful'
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Logout failed', 500));
  }
});

// GET /api/auth/user
authRouter.get('/user', async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new APIError('No token provided', 401);
    }

    const token = authHeader.substring(7);
    
    const { data, error } = await supabase.auth.getUser(token);

    if (error) {
      throw new APIError(error.message, 401);
    }

    res.json({
      user: data.user
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Failed to get user', 500));
  }
});

// POST /api/auth/refresh
authRouter.post('/refresh', async (req, res, next) => {
  try {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      throw new APIError('Refresh token required', 400);
    }

    const { data, error } = await supabase.auth.refreshSession({
      refresh_token
    });

    if (error) {
      throw new APIError(error.message, 401);
    }

    res.json({
      session: data.session,
      message: 'Token refreshed successfully'
    });
  } catch (error: any) {
    next(new APIError(error.message || 'Token refresh failed', 500));
  }
});

export default authRouter;
