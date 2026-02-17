-- Create users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL UNIQUE,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create manuscripts table
CREATE TABLE IF NOT EXISTS public.manuscripts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  genre TEXT,
  language TEXT DEFAULT 'ar',
  original_text TEXT NOT NULL,
  processed_text TEXT,
  word_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'uploaded' CHECK (status IN ('uploaded', 'processing', 'completed', 'failed')),
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create processing_history table
CREATE TABLE IF NOT EXISTS public.processing_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  manuscript_id UUID NOT NULL REFERENCES public.manuscripts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  step TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
  progress INTEGER DEFAULT 0,
  result JSONB,
  error TEXT,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_manuscripts_user_id ON public.manuscripts(user_id);
CREATE INDEX IF NOT EXISTS idx_manuscripts_status ON public.manuscripts(status);
CREATE INDEX IF NOT EXISTS idx_manuscripts_created_at ON public.manuscripts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_processing_history_manuscript_id ON public.processing_history(manuscript_id);
CREATE INDEX IF NOT EXISTS idx_processing_history_user_id ON public.processing_history(user_id);
CREATE INDEX IF NOT EXISTS idx_processing_history_status ON public.processing_history(status);

-- Enable Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.manuscripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.processing_history ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can view own profile"
  ON public.users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.users FOR UPDATE
  USING (auth.uid() = id);

-- RLS Policies for manuscripts table
CREATE POLICY "Users can view own manuscripts"
  ON public.manuscripts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own manuscripts"
  ON public.manuscripts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own manuscripts"
  ON public.manuscripts FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own manuscripts"
  ON public.manuscripts FOR DELETE
  USING (auth.uid() = user_id);

-- RLS Policies for processing_history table
CREATE POLICY "Users can view own processing history"
  ON public.processing_history FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own processing history"
  ON public.processing_history FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Create function to automatically update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON public.users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_manuscripts_updated_at
  BEFORE UPDATE ON public.manuscripts
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Create function to sync auth.users with public.users
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, name)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'name', NEW.email)
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
