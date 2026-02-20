import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

// Client for user operations (with RLS)
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Admin client for backend operations (bypasses RLS)
export const supabaseAdmin = supabaseServiceKey 
  ? createClient(supabaseUrl, supabaseServiceKey)
  : supabase;

// Database schema types
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface Manuscript {
  id: string;
  user_id: string;
  title: string;
  author: string;
  genre: string;
  language: string;
  original_text: string;
  processed_text?: string;
  word_count: number;
  status: 'uploaded' | 'processing' | 'completed' | 'failed';
  metadata: any;
  created_at: string;
  updated_at: string;
}

export interface ProcessingHistory {
  id: string;
  manuscript_id: string;
  user_id: string;
  step: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  result?: any;
  error?: string;
  started_at: string;
  completed_at?: string;
}

// Helper functions
export async function createManuscript(data: Partial<Manuscript>) {
  const { data: manuscript, error } = await supabaseAdmin
    .from('manuscripts')
    .insert(data)
    .select()
    .single();
  
  if (error) throw error;
  return manuscript;
}

export async function getManuscriptById(id: string) {
  const { data, error } = await supabaseAdmin
    .from('manuscripts')
    .select('*')
    .eq('id', id)
    .single();
  
  if (error) throw error;
  return data;
}

export async function updateManuscript(id: string, data: Partial<Manuscript>) {
  const { data: manuscript, error } = await supabaseAdmin
    .from('manuscripts')
    .update({ ...data, updated_at: new Date().toISOString() })
    .eq('id', id)
    .select()
    .single();
  
  if (error) throw error;
  return manuscript;
}

export async function getUserManuscripts(userId: string) {
  const { data, error } = await supabaseAdmin
    .from('manuscripts')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });
  
  if (error) throw error;
  return data;
}

export async function createProcessingHistory(data: Partial<ProcessingHistory>) {
  const { data: history, error } = await supabaseAdmin
    .from('processing_history')
    .insert(data)
    .select()
    .single();
  
  if (error) throw error;
  return history;
}

export async function updateProcessingHistory(id: string, data: Partial<ProcessingHistory>) {
  const { data: history, error } = await supabaseAdmin
    .from('processing_history')
    .update(data)
    .eq('id', id)
    .select()
    .single();
  
  if (error) throw error;
  return history;
}
