-- =============================================================
-- NEXUS CORTEX — المركز العصبي المركزي
-- Schema: nexus_core
-- المسؤولية: تسجيل الوكلاء، توجيه الأوامر، مراقبة الحركة
-- =============================================================

CREATE SCHEMA IF NOT EXISTS nexus_core;

-- ---------------------------------------------------------------
-- 1. سجل الوكلاء (Agent Registry)
--    كل وكيل/كوكب يسجل نفسه هنا مع قدراته
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nexus_core.agents (
  id           SERIAL PRIMARY KEY,
  name         TEXT UNIQUE NOT NULL,          -- PLANET-NAME e.g. "X-BIO", "SHADOW-7"
  display_name TEXT,
  agent_type   TEXT NOT NULL,                 -- 'planet' | 'service' | 'human'
  capabilities JSONB DEFAULT '[]',            -- ["scan","report","publish",...]
  endpoint     TEXT,                          -- http://service:port
  status       TEXT DEFAULT 'offline',        -- 'online' | 'offline' | 'busy' | 'error'
  last_seen    TIMESTAMPTZ DEFAULT now(),
  metadata     JSONB DEFAULT '{}',
  created_at   TIMESTAMPTZ DEFAULT now()
);

-- ---------------------------------------------------------------
-- 2. جدول الأوامر (Command Queue)
--    كل أمر يمر من هنا — من الإنسان أو وكيل لوكيل
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nexus_core.commands (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  command_type  TEXT NOT NULL,                -- 'scan' | 'report' | 'publish' | 'alert' | ...
  origin        TEXT NOT NULL DEFAULT 'human',-- من أصدر الأمر
  target_agent  TEXT,                         -- اسم الوكيل المستهدف (NULL = broadcast)
  payload       JSONB DEFAULT '{}',           -- تفاصيل الأمر
  priority      INTEGER DEFAULT 5,            -- 1=critical, 10=low
  status        TEXT DEFAULT 'queued',        -- 'queued'|'dispatched'|'running'|'done'|'failed'
  result        JSONB,
  error_msg     TEXT,
  dispatched_at TIMESTAMPTZ,
  completed_at  TIMESTAMPTZ,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_commands_status ON nexus_core.commands(status);
CREATE INDEX IF NOT EXISTS idx_commands_target ON nexus_core.commands(target_agent);
CREATE INDEX IF NOT EXISTS idx_commands_created ON nexus_core.commands(created_at DESC);

-- ---------------------------------------------------------------
-- 3. سجل الأحداث (Event Log)
--    كل وكيل يرسل أحداثه هنا — مصدر الحقيقة الوحيد
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nexus_core.events (
  id           BIGSERIAL PRIMARY KEY,
  agent_name   TEXT NOT NULL,
  event_type   TEXT NOT NULL,                 -- 'heartbeat'|'alert'|'result'|'error'|'info'
  severity     TEXT DEFAULT 'info',           -- 'critical'|'high'|'medium'|'low'|'info'
  title        TEXT,
  body         JSONB DEFAULT '{}',
  command_id   UUID REFERENCES nexus_core.commands(id) ON DELETE SET NULL,
  created_at   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_events_agent ON nexus_core.events(agent_name);
CREATE INDEX IF NOT EXISTS idx_events_type  ON nexus_core.events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_time  ON nexus_core.events(created_at DESC);

-- ---------------------------------------------------------------
-- 4. الحالة اللحظية للوكلاء (Agent Live State)
--    snapshot مباشر لحالة كل وكيل (upsert باستمرار)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nexus_core.agent_state (
  agent_name   TEXT PRIMARY KEY,
  status       TEXT DEFAULT 'offline',
  current_task TEXT,
  metrics      JSONB DEFAULT '{}',            -- cpu, memory, requests/min ...
  last_command UUID REFERENCES nexus_core.commands(id) ON DELETE SET NULL,
  updated_at   TIMESTAMPTZ DEFAULT now()
);

-- ---------------------------------------------------------------
-- 5. قواعد التوجيه (Routing Rules)
--    أي نوع أمر يروح لأي وكيل تلقائياً
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nexus_core.routing_rules (
  id            SERIAL PRIMARY KEY,
  command_type  TEXT NOT NULL,
  target_agent  TEXT NOT NULL,
  conditions    JSONB DEFAULT '{}',           -- شروط إضافية على الـ payload
  priority      INTEGER DEFAULT 5,
  is_active     BOOLEAN DEFAULT true,
  created_at    TIMESTAMPTZ DEFAULT now()
);

-- ---------------------------------------------------------------
-- 6. سجل الوصول البشري (Human Sessions)
--    متى دخل الإنسان وأصدر أوامر
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS nexus_core.human_sessions (
  id         BIGSERIAL PRIMARY KEY,
  session_id TEXT,
  action     TEXT,
  metadata   JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- =============================================================
-- بيانات أولية — تسجيل الكواكب الـ 12
-- =============================================================
INSERT INTO nexus_core.agents (name, display_name, agent_type, capabilities, status) VALUES
  ('X-BIO',       'X-BIO Sentinel',         'planet',  '["biometric_scan","health_monitor","alert"]', 'online'),
  ('SHADOW-7',    'Shadow Seven Publisher',  'planet',  '["publish","manuscript","compliance","cover"]', 'online'),
  ('AS-SULTAN',   'AlSultan Intelligence',   'planet',  '["quran","knowledge","query"]', 'offline'),
  ('AI-ARCH',     'AI Architect',            'planet',  '["design","architecture","planning"]', 'offline'),
  ('CLONE-HUB',   'Clone Hub',               'planet',  '["intelligence","analysis","clone"]', 'offline'),
  ('NAV-ORACLE',  'Navigation Oracle',       'planet',  '["routing","navigation","maps"]', 'offline'),
  ('NEXUS-ANALYST','Nexus Data Analyst',     'planet',  '["analytics","reports","visualization"]', 'offline'),
  ('N-TARGET',    'Target Intelligence',     'planet',  '["targeting","market","leads"]', 'offline'),
  ('RAG-CORE',    'RAG Knowledge Core',      'planet',  '["rag","search","context","llm"]', 'offline'),
  ('OPS-CTRL',    'Operations Control',      'planet',  '["ops","deploy","monitor","orchestrate"]', 'offline'),
  ('SEC-GUARD',   'Security Guardian',       'planet',  '["security","audit","threat","protect"]', 'offline'),
  ('LEGAL-EAGLE', 'Legal Eagle',             'planet',  '["legal","contracts","compliance"]', 'offline')
ON CONFLICT (name) DO UPDATE SET display_name = EXCLUDED.display_name, capabilities = EXCLUDED.capabilities;

-- تسجيل الخدمات الأساسية
INSERT INTO nexus_core.agents (name, display_name, agent_type, capabilities, endpoint, status) VALUES
  ('nexus_db',       'NEXUS Database (Moon)',  'service', '["storage","query","persistence"]', NULL, 'online'),
  ('nexus_ollama',   'Ollama LLM Engine',      'service', '["inference","llm","embeddings"]',  'http://nexus_ollama:11434', 'online'),
  ('nexus_flow',     'n8n Automation',         'service', '["workflow","automation","trigger"]','http://nexus_flow:5678', 'online'),
  ('nexus_ai',       'Open WebUI',             'service', '["chat","ui","model_management"]',  'http://nexus_ai:8080', 'online'),
  ('nexus_voice',    'Voice Engine',           'service', '["tts","voice","audio"]',           'http://nexus_voice:8000', 'online'),
  ('nexus_boardroom','Cognitive Boardroom',    'service', '["dashboard","ai","analytics"]',    'http://nexus_boardroom:8501', 'online'),
  ('nexus_xbio',     'X-BIO Container',        'service', '["biometric","health","security"]', 'http://nexus_xbio:8080', 'online'),
  ('shadow_postgrest','PostgREST API',         'service', '["rest_api","shadow_seven_db"]',    'http://shadow_postgrest:3000', 'online'),
  ('nexus_cortex',   'NEXUS Cortex (Brain)',   'service', '["command","route","dispatch","monitor"]', 'http://nexus_cortex:8090', 'online')
ON CONFLICT (name) DO UPDATE SET status = EXCLUDED.status, endpoint = EXCLUDED.endpoint;

-- قواعد التوجيه الافتراضية
INSERT INTO nexus_core.routing_rules (command_type, target_agent, priority) VALUES
  ('scan',       'X-BIO',         1),
  ('publish',    'SHADOW-7',      1),
  ('compliance', 'SHADOW-7',      1),
  ('query',      'AS-SULTAN',     1),
  ('analytics',  'NEXUS-ANALYST', 1),
  ('security',   'SEC-GUARD',     1),
  ('ops',        'OPS-CTRL',      1),
  ('rag',        'RAG-CORE',      1),
  ('legal',      'LEGAL-EAGLE',   1),
  ('clone',      'CLONE-HUB',     1)
ON CONFLICT DO NOTHING;

-- =============================================================
-- View: لوحة التحكم المركزية
-- =============================================================
CREATE OR REPLACE VIEW nexus_core.cortex_dashboard AS
SELECT
  a.name,
  a.display_name,
  a.agent_type,
  a.status,
  a.last_seen,
  s.current_task,
  s.metrics,
  (SELECT COUNT(*) FROM nexus_core.commands c WHERE c.target_agent = a.name AND c.status IN ('queued','running')) AS pending_commands,
  (SELECT COUNT(*) FROM nexus_core.events e WHERE e.agent_name = a.name AND e.created_at > now() - INTERVAL '1 hour') AS events_last_hour
FROM nexus_core.agents a
LEFT JOIN nexus_core.agent_state s ON s.agent_name = a.name
ORDER BY a.agent_type, a.name;

-- NOTIFY للـ real-time pub/sub
CREATE OR REPLACE FUNCTION nexus_core.notify_command_change()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify('nexus_command_' || NEW.target_agent, row_to_json(NEW)::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_command_notify ON nexus_core.commands;
CREATE TRIGGER trg_command_notify
  AFTER INSERT OR UPDATE ON nexus_core.commands
  FOR EACH ROW EXECUTE FUNCTION nexus_core.notify_command_change();
