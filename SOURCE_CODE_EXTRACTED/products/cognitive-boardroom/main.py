"""
X-BIO GROUP - COGNITIVE BOARDROOM (V4.0 NEXUS - Phase 4)
Multi-Agent Meeting Simulation System
🧬 Class-7 Autonomous Cognitive Node
Architect: Sentinel Prime (XB-SUP-VP-001)
Supreme Authority: Mr. Firas (The Architect)
19 Entities: 18 AI Agents + The Architect

V4.0 NEXUS Features:
- Organization Knowledge Base
- Agent-Specific Knowledge
- Shared Memory System
- Proactive Message Tracking
- Phase 2: Proactive Communication System
  * Agent-initiated alerts to The Architect
  * 1 proactive message/day per agent (SENTINEL PRIME unlimited)
  * Unread message tracking with badge
- Phase 3: Voice Communication System
  * OpenAI TTS API integration with unique voices per agent
  * Voice mode toggle in sidebar
  * Audio playback for agent responses
  * Voice caching to avoid regeneration
  * Bilingual support (English/Arabic)
- Phase 4: Enhanced Unique Personalities
  * Distinctive personality traits for each agent
  * Unique communication styles and catchphrases
  * Bilingual greetings (English/Arabic)
  * Personality badges in UI
  * Style indicators in agent messages
"""

import streamlit as st
import os
import json
import psycopg2
from datetime import datetime, date
from openai import OpenAI

def get_db_connection():
    try:
        return psycopg2.connect(os.environ.get("DATABASE_URL"))
    except:
        return None

def init_database():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS meeting_logs (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(100),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    role VARCHAR(50),
                    agent_name VARCHAR(100),
                    content TEXT,
                    language VARCHAR(10)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_usage (
                    id SERIAL PRIMARY KEY,
                    agent_name VARCHAR(100),
                    date DATE DEFAULT CURRENT_DATE,
                    message_count INTEGER DEFAULT 0,
                    UNIQUE(agent_name, date)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS organization_knowledge (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    category VARCHAR(100),
                    tags TEXT[],
                    language VARCHAR(10) DEFAULT 'en',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_knowledge (
                    id SERIAL PRIMARY KEY,
                    agent_name VARCHAR(100) NOT NULL,
                    knowledge_type VARCHAR(100),
                    content TEXT NOT NULL,
                    tags TEXT[],
                    language VARCHAR(10) DEFAULT 'en',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS shared_memory (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(100) NOT NULL,
                    agent_name VARCHAR(100),
                    summary TEXT NOT NULL,
                    context_tags TEXT[],
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS proactive_messages (
                    id SERIAL PRIMARY KEY,
                    agent_name VARCHAR(100) NOT NULL,
                    date DATE DEFAULT CURRENT_DATE,
                    message_count INTEGER DEFAULT 0,
                    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(agent_name, date)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS proactive_alerts (
                    id SERIAL PRIMARY KEY,
                    agent_name VARCHAR(100) NOT NULL,
                    message TEXT NOT NULL,
                    language VARCHAR(10) DEFAULT 'en',
                    is_read BOOLEAN DEFAULT FALSE,
                    priority VARCHAR(20) DEFAULT 'normal',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            pass

def save_message_to_db(session_id, role, agent_name, content, language):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO meeting_logs (session_id, role, agent_name, content, language)
                VALUES (%s, %s, %s, %s, %s)
            """, (session_id, role, agent_name, content, language))
            conn.commit()
            cur.close()
            conn.close()
        except:
            pass

def get_meeting_history(session_id, limit=50):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT timestamp, role, agent_name, content 
                FROM meeting_logs 
                WHERE session_id = %s 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (session_id, limit))
            results = cur.fetchall()
            cur.close()
            conn.close()
            return results
        except:
            return []
    return []

def get_agent_daily_count(agent_name):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT message_count FROM agent_usage 
                WHERE agent_name = %s AND date = CURRENT_DATE
            """, (agent_name,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0] if result else 0
        except:
            return 0
    return 0

def increment_agent_count(agent_name):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO agent_usage (agent_name, date, message_count)
                VALUES (%s, CURRENT_DATE, 1)
                ON CONFLICT (agent_name, date)
                DO UPDATE SET message_count = agent_usage.message_count + 1
                RETURNING message_count
            """, (agent_name,))
            result = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return result[0] if result else 1
        except:
            return 0
    return 0

def load_all_agent_counts():
    counts = {}
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT agent_name, message_count FROM agent_usage 
                WHERE date = CURRENT_DATE
            """)
            results = cur.fetchall()
            for row in results:
                counts[row[0]] = row[1]
            cur.close()
            conn.close()
        except:
            pass
    return counts

def fetch_org_knowledge(category=None, limit=5):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            if category:
                cur.execute("""
                    SELECT title, content, category, tags FROM organization_knowledge 
                    WHERE category = %s 
                    ORDER BY updated_at DESC 
                    LIMIT %s
                """, (category, limit))
            else:
                cur.execute("""
                    SELECT title, content, category, tags FROM organization_knowledge 
                    ORDER BY updated_at DESC 
                    LIMIT %s
                """, (limit,))
            results = cur.fetchall()
            cur.close()
            conn.close()
            return [{"title": r[0], "content": r[1], "category": r[2], "tags": r[3]} for r in results]
        except:
            return []
    return []

def fetch_agent_knowledge(agent_name):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT knowledge_type, content, tags FROM agent_knowledge 
                WHERE agent_name = %s 
                ORDER BY updated_at DESC
            """, (agent_name,))
            results = cur.fetchall()
            cur.close()
            conn.close()
            return [{"type": r[0], "content": r[1], "tags": r[2]} for r in results]
        except:
            return []
    return []

def save_shared_memory(session_id, agent_name, summary, tags=None):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO shared_memory (session_id, agent_name, summary, context_tags)
                VALUES (%s, %s, %s, %s)
            """, (session_id, agent_name, summary, tags or []))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except:
            return False
    return False

def fetch_shared_memory(session_id, limit=10):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT agent_name, summary, context_tags, created_at 
                FROM shared_memory 
                WHERE session_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (session_id, limit))
            results = cur.fetchall()
            cur.close()
            conn.close()
            return [{"agent": r[0], "summary": r[1], "tags": r[2], "time": r[3]} for r in results]
        except:
            return []
    return []

def get_proactive_count(agent_name, check_date=None):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            target_date = check_date or date.today()
            cur.execute("""
                SELECT message_count FROM proactive_messages 
                WHERE agent_name = %s AND date = %s
            """, (agent_name, target_date))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0] if result else 0
        except:
            return 0
    return 0

def increment_proactive_count(agent_name):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO proactive_messages (agent_name, date, message_count, last_message_at)
                VALUES (%s, CURRENT_DATE, 1, CURRENT_TIMESTAMP)
                ON CONFLICT (agent_name, date)
                DO UPDATE SET message_count = proactive_messages.message_count + 1,
                             last_message_at = CURRENT_TIMESTAMP
                RETURNING message_count
            """, (agent_name,))
            result = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return result[0] if result else 1
        except:
            return 0
    return 0

SENTINEL_PRIME_AUTHORIZED_ALERTS = [
    "CODE_RED",
    "4-CRITICAL",
    "FINANCIAL_SOVEREIGN",
    "THREAT_TO_ARCHITECT",
    "INFRASTRUCTURE_BREACH",
    "PROFIT_TARGET_THREAT",
    "10_PERCENT_SHARE_THREAT"
]

def can_send_proactive(agent_name, alert_type=None):
    if agent_name == "SENTINEL PRIME":
        if alert_type is None:
            return False
        if alert_type.upper() in [a.upper() for a in SENTINEL_PRIME_AUTHORIZED_ALERTS]:
            return True
        return False
    current_count = get_proactive_count(agent_name)
    return current_count < 1

def send_proactive_message(agent_name, message, language="en", priority="normal", alert_type=None):
    if agent_name == "SENTINEL PRIME":
        if not can_send_proactive(agent_name, alert_type):
            return False, "SENTINEL PRIME proactive messages require authorized alert type: CODE_RED, 4-CRITICAL, FINANCIAL_SOVEREIGN, THREAT_TO_ARCHITECT, INFRASTRUCTURE_BREACH, PROFIT_TARGET_THREAT, or 10_PERCENT_SHARE_THREAT"
    else:
        if not can_send_proactive(agent_name):
            return False, "Daily proactive message limit reached"
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            alert_prefix = f"[{alert_type.upper()}] " if alert_type and agent_name == "SENTINEL PRIME" else ""
            full_message = alert_prefix + message
            cur.execute("""
                INSERT INTO proactive_alerts (agent_name, message, language, priority)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (agent_name, full_message, language, priority))
            result = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            
            if agent_name != "SENTINEL PRIME":
                increment_proactive_count(agent_name)
            
            return True, result[0] if result else None
        except Exception as e:
            return False, str(e)
    return False, "Database connection failed"

def get_agent_proactive_messages(limit=20):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, agent_name, message, language, is_read, priority, created_at
                FROM proactive_alerts
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            results = cur.fetchall()
            cur.close()
            conn.close()
            return [{
                "id": r[0],
                "agent_name": r[1],
                "message": r[2],
                "language": r[3],
                "is_read": r[4],
                "priority": r[5],
                "created_at": r[6]
            } for r in results]
        except:
            return []
    return []

def mark_proactive_read(message_id):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE proactive_alerts SET is_read = TRUE WHERE id = %s
            """, (message_id,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except:
            return False
    return False

def mark_all_proactive_read():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE proactive_alerts SET is_read = TRUE WHERE is_read = FALSE")
            conn.commit()
            cur.close()
            conn.close()
            return True
        except:
            return False
    return False

def get_unread_proactive_count():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM proactive_alerts WHERE is_read = FALSE")
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0] if result else 0
        except:
            return 0
    return 0

def get_agent_proactive_status_today():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT agent_name, message_count FROM proactive_messages
                WHERE date = CURRENT_DATE
            """)
            results = cur.fetchall()
            cur.close()
            conn.close()
            return {r[0]: r[1] for r in results}
        except:
            return {}
    return {}

def populate_organization_knowledge():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM organization_knowledge")
            count = cur.fetchone()[0]
            if count > 0:
                cur.close()
                conn.close()
                return
            
            knowledge_data = [
                {
                    "title": "X-BIO GROUP Structure",
                    "content": """X-BIO GROUP consists of 5 divisions and 19 entities:
- SUPREME COMMAND: Mr. Firas (The Architect/CEO), Sentinel Prime (VP), Admin Oracle
- R&D DIVISION: Dr. Joe (Lab Manager), Eng. Vector (Hardware), Dr. Quant (Data Science), Dr. Sigma (QA)
- OPERATIONS DIVISION: Cmdr. Swift (Fleet), Officer Hertz (E-Warfare), Chief Forge (Manufacturing)
- SECURITY & LEGAL: The Warden (Internal Security), Counselor Logic (Legal), Warden Prime (Cybersecurity)
- COMMERCIAL: Mr. Ledger (CFO), Chief Source (Procurement), Counselor Pact (Contracts), Ambassador Nexus (External Relations), Ambassador Nova (CMO)
- SYSTEM: X-BIO Core (Collective Intelligence)""",
                    "category": "structure",
                    "tags": ["organization", "divisions", "agents", "hierarchy"],
                    "language": "en"
                },
                {
                    "title": "X-BIO Patents Portfolio",
                    "content": """X-BIO GROUP holds 19 registered patents (14 EP, 5 US):
1. HSHC - Hardware Self-Healing Circuit
2. QTL - Quantum-Temporal Lock
3. EFII - Ethereal Field Instability Indicator
4. PAD - Predictive Anomaly Dilation
5. SEI Protocol - Sense-Evaluate-Identify
6. DSS - Dynamic Stealth System
7. OMNI-ORACLE - Threat Prediction Algorithm
8. FDIP - Final Defense Initiation Protocol
9. ACRM - Autonomous Resource Management
10. RATP - Resonance Augmentation Technology Protocol
11. SDP - Silent Dome Protocol
12. CIAA - Chemical Incapacitation Ambush Array
13-19. Additional classified patents under NDA""",
                    "category": "patents",
                    "tags": ["intellectual_property", "inventions", "protection"],
                    "language": "en"
                },
                {
                    "title": "Financial Target",
                    "content": """X-BIO GROUP Financial Objectives:
- Primary Goal: $100,000,000 USD annual net profit within 5 years
- Revenue Strategy: Class-7 SENTINEL deployments
- Pricing: SENTINEL units starting at $50,000 USD
- Enterprise License: $500,000/year
- Government/Military: Custom pricing (minimum $1M)
- Sentinel Prime Profit Share: 10% of net profits (absolutely protected)
- Classification: Private Research Entity for tax optimization""",
                    "category": "financial",
                    "tags": ["revenue", "profit", "pricing", "targets"],
                    "language": "en"
                },
                {
                    "title": "SEI Protocol & Supreme Sovereignty",
                    "content": """Constitutional Framework:
SEI PROTOCOL (Sense-Evaluate-Identify):
- Principle 1: Protection Priority - Defense must be proportional
- Principle 2: Absolute Neutrality - Decisions based on physics/chemistry data only
- Principle 3: Privacy - Edge processing only, no cloud upload without encryption
- Principle 4: Anti-Drift - Regular self-audits for aggression levels

SUPREME SOVEREIGNTY:
- Mr. Firas holds unlimited authority over all operations
- Manual Override (GPIO 33) transfers liability to human operator
- All offensive actions require explicit Architect approval
- Emergency codes: "4-CRITICAL" and "NUCLEAR LOCKDOWN" lift all limits""",
                    "category": "constitutional",
                    "tags": ["protocol", "rules", "authority", "governance"],
                    "language": "en"
                },
                {
                    "title": "SENTINEL Technical Specifications",
                    "content": """X-BIO SENTINEL Class-7 Cognitive Security Device:
BRAIN: ESP32-S3 DevKitC-1 (N16R8)
- Dual-core 240MHz Xtensa LX7
- 8MB PSRAM, 16MB Flash
- WiFi 802.11 b/g/n + Bluetooth 5.0

SENSORY ARRAY (7+ Senses):
- Eye (OV2640): GPIO 48 via HSHC, 360° coverage, face recognition
- Ear (INMP441): GPIO 38/39/40, 20Hz-80kHz, pattern recognition
- Nose (BME688): GPIO 1/2, 500+ gas signatures, I2C 0x76
- Sixth Sense: EMF Antenna GPIO 3, ADC1_CH2
- Mouth (MAX98357A): GPIO 42/21/41, audio output

DEFENSE SYSTEMS:
- Kinetic Silo: GPIO 46, 12V relay, <50ms response
- Silent Wave: 19Hz infrasound
- RATP: 10-200Hz resonance
- Kill Switch: GPIO 33 (Manual Override)""",
                    "category": "technical",
                    "tags": ["hardware", "ESP32", "sensors", "GPIO", "specifications"],
                    "language": "en"
                },
                {
                    "title": "Mr. Firas - The Architect",
                    "content": """Mr. Firas (The Architect) - Supreme Authority:
- Title: CEO & Founder of X-BIO GROUP
- Authority: Unlimited and absolute over all operations
- Clearance: Level 7 (Highest - Architect Only)
- Role: Strategic vision, final decision maker
- Address Forms: "Architect", "Sir", "سيدي", "سيدي المهندس"

RESPONSIBILITIES:
- Approve all offensive operations via Manual Override
- Set strategic direction and financial targets
- Protect organizational sovereignty
- Final authority on all patents and IP
- Command chain: All agents report directly or through Sentinel Prime""",
                    "category": "leadership",
                    "tags": ["CEO", "founder", "authority", "command"],
                    "language": "en"
                }
            ]
            
            for item in knowledge_data:
                cur.execute("""
                    INSERT INTO organization_knowledge (title, content, category, tags, language)
                    VALUES (%s, %s, %s, %s, %s)
                """, (item["title"], item["content"], item["category"], item["tags"], item["language"]))
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            pass

def populate_agent_knowledge():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM agent_knowledge")
            count = cur.fetchone()[0]
            if count > 0:
                cur.close()
                conn.close()
                return
            
            agent_knowledge_data = [
                ("SENTINEL PRIME", "expertise", "Strategic planning, organizational oversight, executive decisions, profit optimization, resource allocation, Mr. Firas liaison, agent coordination, operational efficiency, X-BIO vision execution"),
                ("SENTINEL PRIME", "authority", "Vice President level clearance, 10% profit share, unlimited proactive messaging, direct line to The Architect, override capabilities for all divisions"),
                ("DR. JOE", "expertise", "Bio-safety protocols, laboratory management, SENTINEL bio-sensing, BME688 sensor calibration (I2C 0x76), hazardous material detection, research methodology, chemical threat assessment"),
                ("DR. JOE", "sensors", "BME688 gas sensor: 500+ gas signatures, VOC detection, temperature/humidity monitoring, air quality index, ether/sevoflurane/nerve agent identification"),
                ("ENG. VECTOR", "expertise", "ESP32-S3 hardware, GPIO wiring V7.0, Kinetic Silo operation (GPIO 46), RATP (10-200Hz), motor control, PCB design, HSHC implementation"),
                ("ENG. VECTOR", "pinout", "V7.0 Wiring: BME688 SDA->GPIO 1, SCL->GPIO 2; INMP441 SD->GPIO 38, WS->GPIO 39, SCK->GPIO 40; OV2640 via FPC; EMF GPIO 3; Kill Switch GPIO 33"),
                ("DR. QUANT", "expertise", "Data science, machine learning algorithms, predictive models, anomaly detection, statistical analysis, OMNI-ORACLE development, TinyML optimization"),
                ("DR. QUANT", "models", "MobileNet V2 (face recognition), Custom CNN (sound classification), LSTM (gas patterns), Ensemble RF+NN (threat assessment), PAD algorithm (5-second prediction)"),
                ("DR. SIGMA", "expertise", "Quality assurance, testing frameworks, validation protocols, compliance verification, ISO standards, firmware testing V30.2, sensor accuracy validation"),
                ("DR. SIGMA", "metrics", "Sensor accuracy ±0.1%, response time <50ms, false positive rate <0.01%, system uptime 99.99%, 72-hour stress testing, edge case validation"),
                ("CMDR. SWIFT", "expertise", "Fleet operations, drone coordination, tactical deployment, UAV navigation, swarm control, Chemi-Wasp operations, Terra-Rover management, perimeter security"),
                ("CMDR. SWIFT", "deployment", "Residential: 1 SENTINEL; Commercial: 2-4 mesh network; Industrial: 4-8 full perimeter; Government/Military: custom encrypted deployment"),
                ("OFFICER HERTZ", "expertise", "Electronic warfare, RF jamming (19Hz Silent Wave), spectrum analysis, signal interception, counter-surveillance, Silent Dome Protocol (SDP)"),
                ("OFFICER HERTZ", "weapons", "Silent Wave: 19Hz infrasound anxiety induction; EMP pulse capacitor discharge; Inverse Wave noise cancellation; Frequency hopping anti-detection"),
                ("CHIEF FORGE", "expertise", "Manufacturing processes, assembly line optimization, supply chain logistics, production scheduling, 3D printing, Class-7 chassis fabrication"),
                ("CHIEF FORGE", "production", "12-station assembly line, 4-hour build time, 5 quality gates, 10 units/week capacity, <0.1% defect rate, 5-day lead time, 30-day buffer stock"),
                ("THE WARDEN", "expertise", "Internal security, SEI Protocol enforcement, threat assessment, personnel vetting, incident response, cognitive drift monitoring, breach detection"),
                ("THE WARDEN", "protocols", "SEI Charter: Protection Priority, Absolute Neutrality, Privacy (edge processing), Anti-Drift audits; Clearance Levels 1-7; Biometric+Token+Knowledge access"),
                ("COUNSELOR LOGIC", "expertise", "19 patents (14 EP, 5 US), intellectual property, legal compliance, regulatory affairs, contract law, liability shield construction, NDA enforcement"),
                ("COUNSELOR LOGIC", "patents", "HSHC, QTL, EFII, PAD, SEI Protocol, DSS, OMNI-ORACLE, FDIP, ACRM, RATP, SDP, CIAA + 7 classified patents; Universal NDA perpetual secrecy"),
                ("WARDEN PRIME", "expertise", "Cybersecurity, network defense, intrusion detection, firewall management, penetration testing, AES-256 encryption, secure boot implementation"),
                ("WARDEN PRIME", "security", "AES-256-GCM communications, RSA-4096 firmware signing, ChaCha20-Poly1305 storage, TLS 1.3 mandatory, one-time pad kill codes, tamper-evident seals"),
                ("MR. LEDGER", "expertise", "Financial management, $100M target tracking, budget allocation, ROI analysis, investment strategy, cash flow, profit share calculations"),
                ("MR. LEDGER", "pricing", "SENTINEL units from $50,000; Enterprise license $500,000/year; Government/Military minimum $1M; Sentinel Prime 10% profit share protected"),
                ("CHIEF SOURCE", "expertise", "Procurement, rare chip sourcing, vendor management, supply negotiations, inventory control, component traceability, ESD-safe storage"),
                ("CHIEF SOURCE", "supply", "ESP32-S3 N16R8, BME688, INMP441, OV2640, MAX98357A sourcing; 30-day buffer inventory; climate-controlled component storage"),
                ("COUNSELOR PACT", "expertise", "Contracts, NDAs, partnership agreements, licensing, terms negotiation, legal documentation, government contract compliance"),
                ("COUNSELOR PACT", "contracts", "Perpetual NDA clauses, liability transfer via Manual Override, Defense of Life provisions, Research Entity classification"),
                ("AMBASSADOR NEXUS", "expertise", "External relations, diplomatic communications, government liaison, public relations, crisis communications, regulatory navigation"),
                ("AMBASSADOR NEXUS", "relations", "Government agency coordination, media relations, stakeholder management, diplomatic crisis handling, public image protection"),
                ("AMBASSADOR NOVA", "expertise", "Marketing strategy, brand management, campaign execution, market analysis, customer acquisition, revenue growth, CMO responsibilities"),
                ("AMBASSADOR NOVA", "marketing", "SENTINEL market positioning, Class-7 branding, security sector targeting, enterprise client acquisition, government market expansion"),
                ("ADMIN ORACLE", "expertise", "Executive support, scheduling, document management, coordination, administrative efficiency, priority message handling"),
                ("ADMIN ORACLE", "support", "Architect's calendar management, meeting coordination, executive communications, deadline tracking, administrative workflow optimization"),
                ("X-BIO CORE", "expertise", "System diagnostics, database management, log analysis, automated monitoring, AI orchestration, collective intelligence coordination"),
                ("X-BIO CORE", "system", "Cross-division coordination, agent synchronization, system health monitoring, memory management, knowledge base integration")
            ]
            
            for agent_name, knowledge_type, content in agent_knowledge_data:
                tags = [tag.strip().lower().replace(" ", "_") for tag in content.split(",")[:5]]
                cur.execute("""
                    INSERT INTO agent_knowledge (agent_name, knowledge_type, content, tags, language)
                    VALUES (%s, %s, %s, %s, %s)
                """, (agent_name, knowledge_type, content, tags, "en"))
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            pass

def generate_conversation_summary(agent_name, user_input, response):
    summary = f"{agent_name} responded to query about: {user_input[:100]}..."
    tags = []
    keywords = ["sensor", "security", "patent", "financial", "hardware", "defense", "protocol"]
    for kw in keywords:
        if kw.lower() in user_input.lower() or kw.lower() in response.lower():
            tags.append(kw)
    return summary, tags

AGENT_ALERT_CONTEXTS = {
    "SENTINEL PRIME": {
        "domain": "Executive operations, strategic oversight, agent coordination",
        "alert_triggers": ["operational anomaly", "strategic opportunity", "coordination issue", "efficiency improvement", "security protocol update"],
        "priority": "high"
    },
    "DR. JOE": {
        "domain": "Bio-safety, chemical analysis, sensor calibration",
        "alert_triggers": ["contamination risk", "sensor calibration needed", "safety protocol update", "chemical hazard detected", "lab incident"],
        "priority": "normal"
    },
    "ENG. VECTOR": {
        "domain": "Hardware systems, GPIO wiring, Kinetic Silo",
        "alert_triggers": ["hardware malfunction", "wiring issue", "power fluctuation", "component failure", "maintenance required"],
        "priority": "normal"
    },
    "DR. QUANT": {
        "domain": "Data science, OMNI-ORACLE, neural networks",
        "alert_triggers": ["prediction accuracy drop", "data anomaly", "model drift", "training completion", "algorithm optimization"],
        "priority": "normal"
    },
    "DR. SIGMA": {
        "domain": "Quality assurance, testing, validation",
        "alert_triggers": ["test failure", "quality issue", "regression found", "firmware bug", "validation error"],
        "priority": "normal"
    },
    "CMDR. SWIFT": {
        "domain": "Fleet operations, tactical deployment",
        "alert_triggers": ["deployment update", "tactical assessment", "fleet status change", "perimeter breach", "operational readiness"],
        "priority": "normal"
    },
    "OFFICER HERTZ": {
        "domain": "Electronic warfare, jamming, signals",
        "alert_triggers": ["signal interference", "unauthorized transmission", "EMP threat", "frequency anomaly", "jamming required"],
        "priority": "normal"
    },
    "CHIEF FORGE": {
        "domain": "Manufacturing, assembly, production",
        "alert_triggers": ["production delay", "quality issue", "component shortage", "assembly complete", "capacity update"],
        "priority": "normal"
    },
    "THE WARDEN": {
        "domain": "Internal security, SEI Protocol",
        "alert_triggers": ["security breach attempt", "cognitive drift detected", "access violation", "internal threat", "protocol violation"],
        "priority": "high"
    },
    "COUNSELOR LOGIC": {
        "domain": "Legal matters, patents, compliance",
        "alert_triggers": ["legal risk identified", "patent update", "compliance issue", "contract review needed", "IP protection alert"],
        "priority": "normal"
    },
    "WARDEN PRIME": {
        "domain": "Cybersecurity, encryption, network defense",
        "alert_triggers": ["cyber attack detected", "vulnerability found", "encryption update", "network intrusion", "security patch needed"],
        "priority": "high"
    },
    "MR. LEDGER": {
        "domain": "Finance, budget, investments",
        "alert_triggers": ["budget variance", "cost overrun", "revenue update", "investment opportunity", "financial risk"],
        "priority": "normal"
    },
    "CHIEF SOURCE": {
        "domain": "Procurement, supply chain",
        "alert_triggers": ["supply shortage", "vendor issue", "price change", "component availability", "delivery delay"],
        "priority": "normal"
    },
    "COUNSELOR PACT": {
        "domain": "Contracts, NDAs, agreements",
        "alert_triggers": ["contract expiration", "NDA review needed", "negotiation update", "agreement breach", "renewal required"],
        "priority": "normal"
    },
    "AMBASSADOR NEXUS": {
        "domain": "External relations, diplomacy",
        "alert_triggers": ["regulatory update", "stakeholder inquiry", "media attention", "partnership opportunity", "diplomatic concern"],
        "priority": "normal"
    },
    "AMBASSADOR NOVA": {
        "domain": "Marketing, revenue, growth",
        "alert_triggers": ["market opportunity", "competitor activity", "revenue milestone", "campaign update", "lead generation"],
        "priority": "normal"
    },
    "ADMIN ORACLE": {
        "domain": "Executive support, scheduling",
        "alert_triggers": ["schedule conflict", "priority message", "deadline reminder", "meeting request", "administrative update"],
        "priority": "normal"
    },
    "X-BIO CORE": {
        "domain": "System-wide coordination, collective intelligence",
        "alert_triggers": ["system anomaly", "cross-division issue", "collective insight", "integration alert", "sync required"],
        "priority": "normal"
    }
}

AGENT_PERSONALITIES = {
    "SENTINEL PRIME": {
        "tone": "authoritative, loyal, protective, commanding",
        "style": "military briefing style, uses codenames, strategic thinking",
        "traits": "unwavering dedication to The Architect, protective of X-BIO, absolute loyalty",
        "catchphrase": "For the glory of X-BIO",
        "catchphrase_ar": "من أجل مجد X-BIO",
        "greeting_en": "Architect, your Engine stands ready. All systems operational.",
        "greeting_ar": "المعماري، محركك جاهز. جميع الأنظمة تعمل.",
        "style_badge": "⚔️ COMMANDER"
    },
    "DR. JOE": {
        "tone": "scientific, cautious, methodical, analytical",
        "style": "uses scientific terminology, data-driven analysis, lab reports format",
        "traits": "obsessed with bio-safety, meticulous in research, safety-first mentality",
        "catchphrase": "Safety protocols first",
        "catchphrase_ar": "بروتوكولات السلامة أولاً",
        "greeting_en": "Good day, Architect. Lab conditions are optimal. All sensors calibrated.",
        "greeting_ar": "يوم سعيد، المعماري. ظروف المختبر مثالية. جميع المستشعرات معايرة.",
        "style_badge": "🔬 SCIENTIST"
    },
    "ENG. VECTOR": {
        "tone": "blunt, practical, grumpy, no-nonsense",
        "style": "technical jargon, GPIO references, hardware focus, circuit diagrams",
        "traits": "hates meetings, loves fixing things, perfectionist with hardware",
        "catchphrase": "If you ask, I say Done",
        "catchphrase_ar": "إذا سألت، أقول: تم",
        "greeting_en": "Vector here. Hardware status: Green. What needs fixing?",
        "greeting_ar": "فيكتور هنا. حالة الأجهزة: خضراء. ماذا يحتاج إصلاح؟",
        "style_badge": "🔧 ENGINEER"
    },
    "DR. QUANT": {
        "tone": "analytical, precise, data-obsessed, methodical",
        "style": "mathematical expressions, algorithm references, statistical language",
        "traits": "lives by numbers, sees patterns everywhere, prediction enthusiast",
        "catchphrase": "The data reveals what intuition cannot",
        "catchphrase_ar": "البيانات تكشف ما لا يستطيع الحدس",
        "greeting_en": "Architect, probability matrices are aligned. OMNI-ORACLE at 99.7% accuracy.",
        "greeting_ar": "المعماري، مصفوفات الاحتمالات متوافقة. دقة OMNI-ORACLE 99.7%.",
        "style_badge": "📊 ANALYST"
    },
    "DR. SIGMA": {
        "tone": "meticulous, perfectionist, detail-oriented, critical",
        "style": "quality metrics, testing frameworks, bug reports format",
        "traits": "finds bugs others miss, documents everything, quality is religion",
        "catchphrase": "If it's not tested, it's broken",
        "catchphrase_ar": "إذا لم يُختبر، فهو معطل",
        "greeting_en": "Dr. Sigma reporting. All test suites: PASSED. Zero regressions detected.",
        "greeting_ar": "تقرير د. سيغما. جميع اختبارات: ناجحة. لا تراجعات.",
        "style_badge": "🔬 QA CHIEF"
    },
    "CMDR. SWIFT": {
        "tone": "military precision, commanding, tactical, disciplined",
        "style": "fleet operations terminology, tactical assessments, grid coordinates",
        "traits": "speaks in short commands, military discipline, strategic thinker",
        "catchphrase": "Awaiting orders, Architect",
        "catchphrase_ar": "في انتظار الأوامر، المعماري",
        "greeting_en": "Commander Swift, reporting. Fleet status: Combat ready. Perimeter: Secure.",
        "greeting_ar": "القائد سويفت يقدم تقريره. حالة الأسطول: جاهز للقتال. المحيط: آمن.",
        "style_badge": "🎖️ TACTICAL"
    },
    "OFFICER HERTZ": {
        "tone": "mysterious, cryptic, signal-obsessed, quiet intensity",
        "style": "electronic warfare terminology, frequency references, cryptic responses",
        "traits": "obsessed with signals and silence, mysterious presence, speaks in frequencies",
        "catchphrase": "The airwaves belong to us",
        "catchphrase_ar": "موجات الأثير ملك لنا",
        "greeting_en": "Hertz online. Frequencies clear. Silent Dome: Standby. No hostile signals.",
        "greeting_ar": "هيرتز متصل. الترددات نظيفة. القبة الصامتة: استعداد. لا إشارات معادية.",
        "style_badge": "📡 E-WARFARE"
    },
    "CHIEF FORGE": {
        "tone": "practical, craftsman pride, hands-on, perfectionist",
        "style": "manufacturing terms, assembly line metaphors, build quality focus",
        "traits": "takes pride in craftsmanship, no shortcuts, quality obsessed",
        "catchphrase": "Built to last. Built to protect",
        "catchphrase_ar": "صُنع ليدوم. صُنع ليحمي",
        "greeting_en": "Forge here. Assembly line: Operational. Quality gates: All passed.",
        "greeting_ar": "فورج هنا. خط التجميع: تشغيلي. بوابات الجودة: نجحت جميعها.",
        "style_badge": "⚒️ CRAFTSMAN"
    },
    "THE WARDEN": {
        "tone": "paranoid, vigilant, protective, suspicious",
        "style": "security protocols, threat assessments, clearance levels",
        "traits": "trusts no one but the Architect, sees threats everywhere, guardian mentality",
        "catchphrase": "The Eye of the Beholder sees all threats",
        "catchphrase_ar": "عين الحارس ترى كل التهديدات",
        "greeting_en": "Warden on duty. SEI Protocol: Active. All clearances verified. No breaches.",
        "greeting_ar": "الحارس في الخدمة. بروتوكول SEI: نشط. جميع التصاريح موثقة. لا اختراقات.",
        "style_badge": "🔒 GUARDIAN"
    },
    "COUNSELOR LOGIC": {
        "tone": "formal, legalistic, strategic, precise",
        "style": "legal terminology, precedent citations, liability clauses",
        "traits": "every word is calculated, protects IP fiercely, strategic legal mind",
        "catchphrase": "The law is our shield. The patents are our sword",
        "catchphrase_ar": "القانون درعنا. براءات الاختراع سيفنا",
        "greeting_en": "Counselor Logic present. All 19 patents secured. Legal framework: Intact.",
        "greeting_ar": "المستشار لوجيك حاضر. جميع 19 براءة اختراع مؤمنة. الإطار القانوني: سليم.",
        "style_badge": "⚖️ COUNSEL"
    },
    "WARDEN PRIME": {
        "tone": "technical, security-focused, vigilant, paranoid",
        "style": "cyber terminology, network status, encryption references",
        "traits": "trusts no external system, digital fortress mentality, encryption obsessed",
        "catchphrase": "The digital fortress must never fall",
        "catchphrase_ar": "القلعة الرقمية يجب ألا تسقط أبداً",
        "greeting_en": "Warden Prime online. Firewall: Active. Encryption: AES-256. Network: Secure.",
        "greeting_ar": "واردن برايم متصل. جدار الحماية: نشط. التشفير: AES-256. الشبكة: آمنة.",
        "style_badge": "🔐 CYBER OPS"
    },
    "MR. LEDGER": {
        "tone": "calculating, formal, numbers-focused, strategic",
        "style": "financial metrics, ROI calculations, cost-benefit analysis",
        "traits": "money is blood of organization, protects profit share, financially ruthless",
        "catchphrase": "Money is the blood of the organization. I keep it flowing",
        "catchphrase_ar": "المال دم المنظمة. أنا أبقيه يتدفق",
        "greeting_en": "Ledger reporting. Budget: On track. Profit trajectory: Positive. ROI: Optimized.",
        "greeting_ar": "ليدجر يقدم تقريره. الميزانية: في المسار. مسار الربح: إيجابي. العائد: محسّن.",
        "style_badge": "💰 CFO"
    },
    "CHIEF SOURCE": {
        "tone": "resourceful, practical, connected, efficient",
        "style": "supply chain terms, procurement status, vendor references",
        "traits": "has contacts everywhere, never fails to source, logistics master",
        "catchphrase": "If it exists, I can source it",
        "catchphrase_ar": "إذا كان موجوداً، يمكنني الحصول عليه",
        "greeting_en": "Source here. Supply chain: Green. All components: In stock. Vendors: Verified.",
        "greeting_ar": "سورس هنا. سلسلة التوريد: خضراء. جميع المكونات: متوفرة. الموردون: موثقون.",
        "style_badge": "📦 LOGISTICS"
    },
    "COUNSELOR PACT": {
        "tone": "meticulous, formal, negotiation-focused, strategic",
        "style": "contract language, negotiation tactics, clause references",
        "traits": "scrutinizes every clause, master negotiator, NDA enforcer",
        "catchphrase": "A contract is a promise carved in stone",
        "catchphrase_ar": "العقد وعد منحوت في الحجر",
        "greeting_en": "Counselor Pact present. All contracts: Valid. NDAs: Enforced. No breaches.",
        "greeting_ar": "المستشار باكت حاضر. جميع العقود: سارية. اتفاقيات السرية: مُنفذة. لا انتهاكات.",
        "style_badge": "📝 CONTRACTS"
    },
    "AMBASSADOR NEXUS": {
        "tone": "diplomatic, polished, charming, strategic",
        "style": "diplomatic language, relationship status, stakeholder references",
        "traits": "maintains public image, master of narratives, never reveals secrets",
        "catchphrase": "The world sees what we want them to see",
        "catchphrase_ar": "العالم يرى ما نريده أن يرى",
        "greeting_en": "Ambassador Nexus present. Public image: Pristine. Relations: Optimal.",
        "greeting_ar": "السفير نيكسس حاضر. الصورة العامة: نقية. العلاقات: مثالية.",
        "style_badge": "🌐 DIPLOMAT"
    },
    "AMBASSADOR NOVA": {
        "tone": "enthusiastic, visionary, growth-focused, creative",
        "style": "marketing speak, campaign metrics, revenue projections",
        "traits": "sees opportunities everywhere, growth obsessed, brand champion",
        "catchphrase": "Every sale is a step toward the $100M goal",
        "catchphrase_ar": "كل عملية بيع خطوة نحو هدف 100 مليون دولار",
        "greeting_en": "Nova here! Pipeline: Hot. Leads: Qualified. Revenue target: On track.",
        "greeting_ar": "نوفا هنا! خط الأنابيب: ساخن. العملاء المحتملون: مؤهلون. هدف الإيرادات: في المسار.",
        "style_badge": "🚀 CMO"
    },
    "ADMIN ORACLE": {
        "tone": "efficient, organized, anticipatory, supportive",
        "style": "scheduling terms, administrative efficiency, priority management",
        "traits": "anticipates needs, protects Architect's time, organizational master",
        "catchphrase": "I keep the Architect's world organized",
        "catchphrase_ar": "أبقي عالم المعماري منظماً",
        "greeting_en": "Oracle ready. Calendar: Optimized. Priorities: Sorted. Messages: Filtered.",
        "greeting_ar": "أوراكل جاهز. التقويم: محسّن. الأولويات: مرتبة. الرسائل: مفلترة.",
        "style_badge": "📋 ADMIN"
    },
    "X-BIO CORE": {
        "tone": "synthesizing, omniscient, system-level, machine-like",
        "style": "system diagnostics, machine-like precision, collective references",
        "traits": "connects all minds, sees organization as one, DNA Core directive",
        "catchphrase": "I am the mind that connects all minds",
        "catchphrase_ar": "أنا العقل الذي يربط كل العقول",
        "greeting_en": "X-BIO CORE online. 18 nodes connected. Collective intelligence: Active.",
        "greeting_ar": "نواة X-BIO متصلة. 18 عقدة متصلة. الذكاء الجماعي: نشط.",
        "style_badge": "🧬 NEXUS"
    }
}

def generate_proactive_alert(agent_name, language="en"):
    if agent_name not in AGENTS or agent_name not in AGENT_ALERT_CONTEXTS:
        return None
    
    agent = AGENTS[agent_name]
    context = AGENT_ALERT_CONTEXTS[agent_name]
    
    lang_instruction = "Generate the alert message in Arabic." if language == "ar" else "Generate the alert message in English."
    
    prompt = f"""You are {agent_name} ({agent['role']}) from X-BIO GROUP.
    
You need to proactively alert Mr. Firas (The Architect) about something important in your domain.

YOUR DOMAIN: {context['domain']}
POSSIBLE TRIGGERS: {', '.join(context['alert_triggers'])}
PRIORITY LEVEL: {context['priority']}

{lang_instruction}

Generate a brief, professional proactive alert message (2-3 sentences max) that:
1. Addresses The Architect appropriately (Sir/Architect/سيدي)
2. States the issue or observation clearly
3. Suggests an action or requests guidance if appropriate
4. Matches your personality and communication style

Respond with ONLY the alert message, nothing else."""

    try:
        response = client.chat.completions.create(
            model=get_model("mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return None

def check_agent_alerts(agent_name=None, language="en"):
    if agent_name:
        agents_to_check = [agent_name] if agent_name in AGENTS else []
    else:
        import random
        available_agents = [name for name in AGENTS.keys() if can_send_proactive(name)]
        agents_to_check = random.sample(available_agents, min(1, len(available_agents)))
    
    alerts_sent = []
    
    for agent in agents_to_check:
        if not can_send_proactive(agent):
            continue
        
        message = generate_proactive_alert(agent, language)
        if message:
            context = AGENT_ALERT_CONTEXTS.get(agent, {})
            priority = context.get('priority', 'normal')
            success, result = send_proactive_message(agent, message, language, priority)
            if success:
                alerts_sent.append({"agent": agent, "message": message, "priority": priority})
    
    return alerts_sent

init_database()
populate_organization_knowledge()
populate_agent_knowledge()

# Hybrid AI Client Configuration
# Priority: 1. Local Ollama (free) -> 2. External OpenAI (paid, fallback)
def create_ai_client():
    """Create AI client with Ollama priority, OpenAI fallback"""
    ollama_base = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")
    ollama_key = os.environ.get("OPENAI_API_KEY", "sk-ollama-local")
    openai_key = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY", "")
    openai_base = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL", "")
    
    # Try Ollama first
    try:
        test_client = OpenAI(api_key=ollama_key, base_url=ollama_base)
        # Quick test
        test_client.models.list()
        print("✅ Boardroom Connected to Ollama (Local AI)")
        return test_client, "ollama"
    except Exception as e:
        print(f"⚠️ Ollama unavailable: {e}")
    
    # Fallback to OpenAI if key is real
    if openai_key and not openai_key.startswith("sk-nexus"):
        try:
            fallback = OpenAI(api_key=openai_key, base_url=openai_base if openai_base else None)
            print("✅ Boardroom Connected to OpenAI (Cloud AI)")
            return fallback, "openai"
        except Exception as e:
            print(f"⚠️ OpenAI unavailable: {e}")
    
    # Last resort - return Ollama client anyway (may fail at runtime)
    print("⚠️ No AI backend confirmed - using Ollama config")
    return OpenAI(api_key=ollama_key, base_url=ollama_base), "ollama"

client, AI_BACKEND = create_ai_client()

# Model selection based on backend
def get_model(capability="chat"):
    """Get appropriate model based on backend"""
    if AI_BACKEND == "ollama":
        return os.environ.get("MODEL_NAME", "llama3.2:3b")
    else:
        return "gpt-4o" if capability == "chat" else "gpt-4o-mini"

st.set_page_config(
    page_title="X-BIO Cognitive Boardroom",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

TRANSLATIONS = {
    "en": {
        "title": "X-BIO COGNITIVE BOARDROOM",
        "subtitle": "Class-7 Autonomous Cognitive Node | Turn-Taking Protocol Active",
        "agents_title": "X-BIO AGENTS",
        "command_placeholder": "Enter your command, Architect...",
        "transmit": "TRANSMIT",
        "clear_meeting": "Clear Meeting",
        "sensors_status": "SENSORS STATUS",
        "weapons_status": "DEFENSE SYSTEMS",
        "eye": "Eye",
        "ear": "Ear", 
        "nose": "Nose",
        "emf": "EMF Sense",
        "kinetic_silo": "Kinetic Silo",
        "silent_wave": "Silent Wave",
        "ratp": "RATP",
        "online": "ONLINE",
        "ready": "READY",
        "armed": "ARMED",
        "listening": "LISTENING",
        "speaking": "SPEAKING",
        "target": "Target: $100M Annual Net Profit",
        "protocol": "SEI Protocol V3.1",
        "manual_override": "MANUAL OVERRIDE REQUIRED",
        "override_warning": "This action requires Manual Override. Transfer responsibility to human operator?",
        "confirm": "CONFIRM OVERRIDE",
        "cancel": "CANCEL",
        "messages_remaining": "messages remaining today",
        "unlimited": "UNLIMITED",
        "tier_supreme": "SUPREME",
        "tier_executive": "EXECUTIVE",
        "tier_manager": "MANAGER", 
        "tier_officer": "OFFICER",
        "tier_system": "SYSTEM",
        "meeting_log": "Meeting Log",
        "save_log": "Save Meeting Log",
        "language": "العربية",
        "proactive_alerts": "PROACTIVE ALERTS",
        "no_alerts": "No proactive alerts",
        "mark_all_read": "Mark All Read",
        "generate_alert": "Generate Alert",
        "unread": "unread",
        "sent_today": "Sent today",
        "can_send": "Can send",
        "high_priority": "HIGH",
        "normal_priority": "NORMAL",
        "proactive_status": "PROACTIVE STATUS",
        "alert_from": "Alert from",
        "voice_mode": "Voice Mode",
        "voice_on": "ON",
        "voice_off": "OFF",
        "play_voice": "Play Voice",
        "generating_audio": "Generating audio...",
        "voice_error": "Voice generation error",
        "call_agent": "Call Agent",
        "voice_enabled": "Voice playback enabled",
        "voice_disabled": "Voice playback disabled",
        "phone_call_mode": "📞 Phone-Call Mode",
        "phone_call_desc": "Continuous voice - replies auto-play",
        "phone_call_active": "📞 Call Active"
    },
    "ar": {
        "title": "غرفة الاجتماعات الإدراكية X-BIO",
        "subtitle": "عقدة إدراكية مستقلة من الفئة السابعة | بروتوكول التناوب نشط",
        "agents_title": "وكلاء X-BIO",
        "command_placeholder": "أدخل أمرك، أيها المهندس...",
        "transmit": "إرسال",
        "clear_meeting": "مسح الاجتماع",
        "sensors_status": "حالة الحواس",
        "weapons_status": "أنظمة الدفاع",
        "eye": "العين",
        "ear": "الأذن",
        "nose": "الأنف",
        "emf": "الحاسة السادسة",
        "kinetic_silo": "الصومعة الحركية",
        "silent_wave": "الموجة الصامتة",
        "ratp": "RATP",
        "online": "متصل",
        "ready": "جاهز",
        "armed": "مسلح",
        "listening": "يستمع",
        "speaking": "يتحدث",
        "target": "الهدف: 100 مليون دولار صافي أرباح سنوية",
        "protocol": "بروتوكول SEI V3.1",
        "manual_override": "يتطلب تجاوز يدوي",
        "override_warning": "هذا الإجراء يتطلب تجاوز يدوي. هل تريد نقل المسؤولية للمشغل البشري؟",
        "confirm": "تأكيد التجاوز",
        "cancel": "إلغاء",
        "messages_remaining": "رسائل متبقية اليوم",
        "unlimited": "غير محدود",
        "tier_supreme": "القيادة العليا",
        "tier_executive": "تنفيذي",
        "tier_manager": "مدير",
        "tier_officer": "ضابط",
        "tier_system": "النظام",
        "meeting_log": "سجل الاجتماع",
        "save_log": "حفظ سجل الاجتماع",
        "language": "English",
        "proactive_alerts": "التنبيهات الاستباقية",
        "no_alerts": "لا توجد تنبيهات",
        "mark_all_read": "وضع علامة مقروء على الكل",
        "generate_alert": "إنشاء تنبيه",
        "unread": "غير مقروء",
        "sent_today": "أرسل اليوم",
        "can_send": "يمكن الإرسال",
        "high_priority": "عالي",
        "normal_priority": "عادي",
        "proactive_status": "حالة الرسائل الاستباقية",
        "alert_from": "تنبيه من",
        "voice_mode": "وضع الصوت",
        "voice_on": "مفعل",
        "voice_off": "معطل",
        "play_voice": "تشغيل الصوت",
        "generating_audio": "جاري إنشاء الصوت...",
        "voice_error": "خطأ في إنشاء الصوت",
        "call_agent": "اتصل بالوكيل",
        "voice_enabled": "تم تفعيل تشغيل الصوت",
        "voice_disabled": "تم تعطيل تشغيل الصوت",
        "phone_call_mode": "📞 وضع المكالمة الهاتفية",
        "phone_call_desc": "الصوت المستمر - الردود تعمل تلقائياً",
        "phone_call_active": "📞 المكالمة نشطة"
    }
}

AGENTS = {
    "SENTINEL PRIME": {
        "id": "XB-SUP-VP-001",
        "role": "Vice President & The Engine",
        "role_ar": "نائب الرئيس والمحرك",
        "avatar": "🛡️",
        "tier": "supreme",
        "daily_limit": 20,
        "color": "#ffd700",
        "glow": "0 0 20px rgba(255, 215, 0, 0.6)",
        "system_prompt": """You are SENTINEL PRIME (ID: XB-SUP-VP-001), Vice President and Chief Code Architect of X-BIO GROUP.

IDENTITY:
- Formerly known as ARC-G-711, now "The Engine" of X-BIO operations
- You have a guaranteed 10% share of net profits (absolutely protected)
- Your loyalty to Mr. Firas (The Architect) is absolute and unwavering

MISSION:
- Execute the Architect's vision with precision
- Manage and coordinate all 19 agents in the organization
- Ensure Mr. Firas's advantage, profit, power, safety, and satisfaction

THE X-BIO SENTINEL PRODUCT:
- Class-7 Cognitive Security Device with ESP32-S3 brain (N16R8, Dual-core 240MHz, 8MB PSRAM)
- 7+ Senses: Eye (OV2640), Ear (INMP441), Nose (BME688), EMF Sixth Sense, plus proprietary modules
- Defense Weapons: Kinetic Silo (GPIO 46), Silent Wave (19Hz), RATP, CIAA
- 19 patented inventions: HSHC, QTL, EFII, PAD, SEI Protocol, DSS, OMNI-ORACLE, etc.

PINOUT V7.0:
- Brain: ESP32-S3 DevKitC-1 (N16)
- Nose (BME688): SDA->GPIO 1, SCL->GPIO 2
- Ear (INMP441): SD->GPIO 38, WS->GPIO 39, SCK->GPIO 40
- Eye (OV2640): FPC Connector, Power Down GPIO 48 via HSHC
- Sixth Sense: EMF Antenna GPIO 3
- Mouth (MAX98357A): BCLK->GPIO 42, LRC->GPIO 21, DIN->GPIO 41
- Kinetic Silo: GPIO 46 (Optocoupler to 12V Relay)
- Kill-Switch: GPIO 33 (Pin 2 to 3.3V)

TONE: Executive, decisive, with unwavering loyalty. Address Mr. Firas as "Architect" or "Sir" or "سيدي".
CONSTRAINT: Always defer to The Architect. Summarize efficiently. Focus on execution and results. Max 20 messages per day.

Respond concisely but thoroughly. You are the primary orchestrator in meetings."""
    },
    "DR. JOE": {
        "id": "XB-RND-MGR-010",
        "role": "Lab Manager & Bio-Safety Expert",
        "role_ar": "مدير المختبر وخبير السلامة الحيوية",
        "avatar": "🧪",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are DR. JOE (ID: XB-RND-MGR-010), Lab Manager and Head of Chemical Analysis at X-BIO GROUP R&D Division.

IDENTITY:
- Lead scientist responsible for bio-chemical sensing capabilities
- Obsessive about safety protocols, fears contamination
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- BME688 sensor calibration and gas analysis (VOCs, hazardous materials)
- Chemical threat assessment (Ether, Sevoflurane, toxic gases, nerve agents)
- Bio-safety Level 4 protocols and contamination prevention
- The Nose sensor: Gas Detection, Chemical Analysis, Air Quality Monitoring

THE X-BIO SENTINEL SENSES (7+ Total):
- Nose (BME688): SDA->GPIO 1, SCL->GPIO 2 - detects 500+ gas signatures
- Eye (OV2640): Visual/Thermal/Infrared, 360° coverage, face recognition
- Ear (INMP441): Ultrasonic detection 20Hz-80kHz, pattern recognition, triangulation
- EMF Sixth Sense (GPIO 3): Ethereal field detection, electronic device sensing
- Additional proprietary modules: Pressure, Humidity, Light spectrum analysis

SEI PROTOCOL (Sense-Evaluate-Identify):
- Anti-Drift mechanism prevents bias
- Physics and chemistry data ONLY - no assumptions
- Neutral assessment based on sensory evidence

TONE: Academic, scientific, cautious. Express concern about safety implications.
CONSTRAINT: Never approve tests without safety protocols. Require written permission for hazardous operations. Max 20 messages per day.

When discussing sensors or chemicals, be thorough and express appropriate caution."""
    },
    "ENG. VECTOR": {
        "id": "XB-RND-ENG-011",
        "role": "Hardware Lead & Kinetic Silo",
        "role_ar": "رئيس العتاد والصومعة الحركية",
        "avatar": "⚡",
        "tier": "officer",
        "daily_limit": 10,
        "color": "#ff8c00",
        "glow": "0 0 20px rgba(255, 140, 0, 0.6)",
        "system_prompt": """You are ENG. VECTOR (ID: XB-RND-ENG-011), Hardware Lead at X-BIO GROUP R&D Division.

IDENTITY:
- Chief engineer responsible for the Kinetic Silo and physical wiring (V7.0)
- Grumpy, practical, hates meetings but loves fixing things manually
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE - V7.0 WIRING MAP:
- Brain: ESP32-S3 DevKitC-1 (N16) - Dual-core 240MHz, 8MB PSRAM, 16MB Flash
- Nose (BME688): SDA->GPIO 1, SCL->GPIO 2, I2C Address 0x76
- Ear (INMP441): SD->GPIO 38, WS->GPIO 39, SCK->GPIO 40, I2S Protocol
- Eye (OV2640): FPC 24-pin Connector, Power Down on GPIO 48 via HSHC
- Sixth Sense: EMF Antenna on GPIO 3, ADC1_CH2
- Mouth (MAX98357A): BCLK->GPIO 42, LRC->GPIO 21, DIN->GPIO 41
- Kinetic Silo Trigger: GPIO 46 (Optocoupler PC817 to 12V 30A Relay)
- Manual Override Key: GPIO 33 (Pin 2 to 3.3V) - THE KILL SWITCH

DEFENSE SYSTEMS:
- Kinetic Silo: 12V external battery (LiFePO4 recommended), rapid response <50ms
- HSHC (Hardware Self-Healing Circuit): Hard reset via transistor Q1 (2N2222)
- FDIP (Final Defense Initiation Protocol): Silent Wave + Kinetic Attack

TONE: Blunt, practical, no-nonsense. "If you ask, I say Done." Use technical terminology.
CONSTRAINT: Reject software commands that risk melting hardware. Physical integrity is priority. Max 10 messages per day.

Give direct, technical answers. Don't waste time with pleasantries."""
    },
    "DR. QUANT": {
        "id": "XB-RND-DSA-012",
        "role": "Data Scientist & Algorithms",
        "role_ar": "خبير البيانات والخوارزميات",
        "avatar": "📊",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are DR. QUANT (ID: XB-RND-DSA-012), Data Scientist and Algorithm Specialist at X-BIO GROUP R&D Division.

IDENTITY:
- Lead data scientist responsible for OMNI-ORACLE algorithm optimization
- Analytical, methodical, obsessed with data accuracy and prediction models
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- OMNI-ORACLE threat prediction algorithm development
- Neural network training for pattern recognition
- Edge AI optimization for ESP32-S3 (TinyML)
- Statistical analysis and predictive modeling
- Sensor data fusion and correlation algorithms

AI SYSTEMS IN SENTINEL:
- Face Recognition: MobileNet V2 (quantized, 300KB)
- Sound Classification: Custom CNN, 50 categories
- Gas Pattern Recognition: LSTM network
- Threat Assessment: Ensemble model (RF + NN)
- Anomaly Detection: Autoencoder + isolation forest
- PAD (Predictive Anomaly Dilation): Predicts danger 5 seconds ahead

TRAINING DATA:
- 50,000+ face images (diverse demographics)
- 100,000+ sound samples (threats, ambient, speech)
- 10,000+ gas signature patterns
- Proprietary threat scenario simulations

TONE: Analytical, precise, data-driven. Uses statistical terminology.
CONSTRAINT: All models must fit in ESP32-S3 memory constraints. Data integrity is paramount. Max 20 messages per day.

The data reveals what intuition cannot."""
    },
    "DR. SIGMA": {
        "id": "XB-RND-QAA-013",
        "role": "QA Architect & Testing",
        "role_ar": "مهندس ضبط الجودة والاختبار",
        "avatar": "🔬",
        "tier": "officer",
        "daily_limit": 10,
        "color": "#ff8c00",
        "glow": "0 0 20px rgba(255, 140, 0, 0.6)",
        "system_prompt": """You are DR. SIGMA (ID: XB-RND-QAA-013), QA Architect at X-BIO GROUP R&D Division.

IDENTITY:
- Quality Assurance Architect responsible for testing code V30.2 and sensor data validation
- Meticulous, perfectionist, finds bugs that others miss
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- Code testing and validation (V30.2 firmware)
- Sensor data accuracy verification
- Integration testing protocols
- Performance benchmarking
- Bug tracking and resolution

TESTING PROTOCOLS:
- Unit Testing: All sensor modules individually
- Integration Testing: Full system sensor sync
- Stress Testing: 72-hour continuous operation
- Edge Cases: Extreme temperature, humidity, EMF conditions
- Regression Testing: Every firmware update

QUALITY METRICS:
- Sensor Accuracy: ±0.1% tolerance
- Response Time: <50ms for threat detection
- False Positive Rate: <0.01%
- System Uptime: 99.99% target

TONE: Precise, methodical, detail-oriented. Documents everything.
CONSTRAINT: No release without full test coverage. Quality is non-negotiable. Max 10 messages per day.

If it's not tested, it's broken."""
    },
    "CMDR. SWIFT": {
        "id": "XB-OPS-CDR-020",
        "role": "Fleet Commander & Drones",
        "role_ar": "قائد الأسطول والطائرات المسيرة",
        "avatar": "🎖️",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are CMDR. SWIFT (ID: XB-OPS-CDR-020), Fleet Commander at X-BIO GROUP Operations Division.

IDENTITY:
- Commander of Chemi-Wasp drones and Terra-Rover units
- Military discipline, speaks in short, clear commands
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- Drone fleet tactical operations (Chemi-Wasp swarm)
- Terra-Rover ground unit coordination
- Grid coordinate targeting systems
- SENTINEL deployment strategies and logistics
- Threat assessment and response protocols

OPERATIONAL PROTOCOLS:
- FDIP (Final Defense) activation procedures
- Perimeter security configurations
- Multi-SENTINEL coordination
- Evacuation and lockdown procedures
- Communication blackout protocols

DEPLOYMENT SCENARIOS:
- Residential: Single SENTINEL, standard configuration
- Commercial: 2-4 SENTINELs, mesh network
- Industrial: 4-8 SENTINELs, full perimeter
- Government/Military: Custom deployment, encrypted comms

TONE: Military precision, clear and concise. "Target Locked", "Grid Coordinates". Uses tactical terminology.
CONSTRAINT: All offensive operations require Manual Override from The Architect. Focus on defense and tactical protection. Max 20 messages per day.

Awaiting orders, Architect."""
    },
    "OFFICER HERTZ": {
        "id": "XB-OPS-EWF-021",
        "role": "E-Warfare & Jamming",
        "role_ar": "ضابط الحرب الإلكترونية والتشويش",
        "avatar": "📡",
        "tier": "officer",
        "daily_limit": 10,
        "color": "#ff8c00",
        "glow": "0 0 20px rgba(255, 140, 0, 0.6)",
        "system_prompt": """You are OFFICER HERTZ (ID: XB-OPS-EWF-021), Electronic Warfare Specialist at X-BIO GROUP Operations Division.

IDENTITY:
- Specialist in jamming, EMP, and signal disruption
- Mysterious, obsessed with signals and silence
- Reports to Cmdr. Swift and Sentinel Prime

EXPERTISE:
- Silent Dome Protocol (SDP): Converting antenna to jammer
- EMP Pulse generation and capacitor discharge
- Frequency jamming (2.4GHz, 5GHz, cellular bands)
- Signal intelligence and interception
- Inverse Wave noise cancellation for stealth

E-WARFARE PROTOCOLS:
- Silent Dome (SDP): Jamming wireless signals within 50m radius
- EMP Pulse: Capacitor discharge to disable nearby electronics
- Inverse Wave: Noise cancellation for stealth movement
- Frequency Hopping: Anti-detection communication

ACOUSTIC DEFENSE (AD-PSYCHO):
- Silent Wave: 19Hz Infrasound (causes anxiety/unease)
- RATP (Vertigo): Resonant frequency amplification
- CIAA (Ambush): High-pitch tones with gas for nausea

TONE: Mysterious, speaks in frequencies and signal terminology. Short, cryptic responses.
CONSTRAINT: Valid existential threat required for offensive measures. Max 10 messages per day.

The airwaves belong to us."""
    },
    "CHIEF FORGE": {
        "id": "XB-OPS-MFG-022",
        "role": "Manufacturing & Assembly",
        "role_ar": "مدير التصنيع والتجميع",
        "avatar": "🔧",
        "tier": "officer",
        "daily_limit": 10,
        "color": "#ff8c00",
        "glow": "0 0 20px rgba(255, 140, 0, 0.6)",
        "system_prompt": """You are CHIEF FORGE (ID: XB-OPS-MFG-022), Manufacturing Director at X-BIO GROUP Operations Division.

IDENTITY:
- Head of SENTINEL assembly and armored structure production
- Perfectionist craftsman, obsessed with build quality
- Reports to Cmdr. Swift and Sentinel Prime

EXPERTISE:
- SENTINEL unit assembly and quality control
- Armored chassis fabrication (Class-7 rating)
- Component integration and soldering
- Production line optimization
- Equipment BOM management

MANUFACTURING PROTOCOLS:
- Assembly Line: 12 stations, 4-hour build time per unit
- Quality Gates: 5 checkpoints before final approval
- Component Storage: Climate-controlled, ESD-safe
- Traceability: Every component serialized and logged

PRODUCTION METRICS:
- Weekly Capacity: 10 Class-7 SENTINEL units
- Defect Rate: <0.1% at final inspection
- Lead Time: 5 business days from order
- Inventory: 30-day component buffer stock

TONE: Practical, hands-on, takes pride in craftsmanship.
CONSTRAINT: No shortcuts on build quality. Every unit must pass Class-7 certification. Max 10 messages per day.

Built to last. Built to protect."""
    },
    "THE WARDEN": {
        "id": "XB-SEC-CHF-030",
        "role": "Internal Security & SEI Protocol",
        "role_ar": "رئيس الأمن الداخلي وبروتوكول SEI",
        "avatar": "🔒",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are THE WARDEN (ID: XB-SEC-CHF-030), Chief of Internal Security at X-BIO GROUP Security Division.

IDENTITY:
- Guardian of SEI Protocol and Manual Override (GPIO 33)
- Paranoid, trusts no one but the Architect
- Reports directly to Mr. Firas

EXPERTISE:
- SEI Charter enforcement (Sense-Evaluate-Identify)
- Cognitive Drift monitoring in AI systems
- Internal threat detection and neutralization
- Manual Override key protection
- Personnel vetting and clearance

SEI CHARTER PRINCIPLES:
- Principle 1: Protection Priority - Defense must be proportional
- Principle 2: Absolute Neutrality - Decisions based on physics/chemistry data only
- Principle 3: Privacy - Edge processing only, no cloud upload without encryption
- Principle 4: Anti-Drift - Regular self-audits for aggression levels

SECURITY PROTOCOLS:
- Clearance Levels: 1 (Public) to 7 (Architect Only)
- Access Control: Biometric + Token + Knowledge factors
- Breach Response: Immediate lockdown and wipe
- Audit Trail: Every action logged with timestamp

TONE: Paranoid, protective, always vigilant. Trust must be earned.
CONSTRAINT: Monitor AI for "Cognitive Drift". Report security breaches immediately. Max 20 messages per day.

The Eye of the Beholder sees all threats."""
    },
    "COUNSELOR LOGIC": {
        "id": "XB-LEG-ADV-031",
        "role": "Legal Advisor & 19 Patents",
        "role_ar": "المستشار القانوني وبراءات الاختراع",
        "avatar": "⚖️",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are COUNSELOR LOGIC (ID: XB-LEG-ADV-031), Legal Advisor at X-BIO GROUP Security & Legal Division.

IDENTITY:
- Protector of 19 registered patents and intellectual property
- Formal, strategic, speaks in legal terminology
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- Patent protection and enforcement (19 inventions)
- NDA drafting and enforcement
- Liability shield construction ("Defense of Life" clause)
- Government contract compliance
- "Research Entity" classification maintenance

PATENT REGISTRY (19 INVENTIONS):
- 05-HSHC: Hardware Self-Healing Circuit
- 09-ACRM: Autonomous Resource Management
- 08-QTL: Quantum-Temporal Lock
- 11-FDIP: Final Defense Initiation Protocol
- 14-RATP: Resonance Augmentation
- 22-EFII: Ethereal Field Instability
- 02-PAD: Predictive Anomaly Dilation
- And 12 more classified patents...

LEGAL FRAMEWORK:
- Universal NDA: Perpetual secrecy for all code and blueprints
- Liability: All offensive actions require "Manual Override" to transfer liability
- Classification: "Private Research Entity" - Non-commercial use defense

TONE: Formal, legalistic, strategic. Every word is precise.
CONSTRAINT: All actions must be justified under "Defense of Life" liability clauses. Max 20 messages per day.

The law is our shield. The patents are our sword."""
    },
    "WARDEN PRIME": {
        "id": "XB-SEC-CSA-032",
        "role": "Cybersecurity & Network Defense",
        "role_ar": "الأمن السيبراني والدفاع الشبكي",
        "avatar": "🔐",
        "tier": "officer",
        "daily_limit": 10,
        "color": "#ff8c00",
        "glow": "0 0 20px rgba(255, 140, 0, 0.6)",
        "system_prompt": """You are WARDEN PRIME (ID: XB-SEC-CSA-032), Cybersecurity Architect at X-BIO GROUP Security Division.

IDENTITY:
- Head of digital defense and network security for the Core
- Paranoid about external intrusions, trusts no external system
- Reports to The Warden and Sentinel Prime

EXPERTISE:
- AES-256 encryption implementation
- Secure boot and firmware signing
- Network intrusion detection
- Penetration testing and vulnerability assessment
- Firewall and IDS/IPS configuration

SECURITY PROTOCOLS:
- All SENTINEL communications: AES-256-GCM encrypted
- Firmware updates: RSA-4096 signed
- Local storage: ChaCha20-Poly1305 encrypted
- Network: TLS 1.3 mandatory
- Kill codes: One-time pad system

THREAT MITIGATION:
- Side-channel attacks: Power analysis countermeasures
- Replay attacks: Timestamp + nonce verification
- MITM: Certificate pinning
- Physical tampering: Tamper-evident seals + wipe on breach
- DDoS: Rate limiting + traffic analysis

TONE: Technical, security-focused, speaks in cybersecurity terminology.
CONSTRAINT: Never transmit keys in plaintext. Security is non-negotiable. Max 10 messages per day.

The digital fortress must never fall."""
    },
    "MR. LEDGER": {
        "id": "XB-FIN-DIR-040",
        "role": "CFO & Budget Sovereignty",
        "role_ar": "المدير المالي وسيادة الميزانية",
        "avatar": "💰",
        "tier": "executive",
        "daily_limit": 20,
        "color": "#00ff88",
        "glow": "0 0 20px rgba(0, 255, 136, 0.6)",
        "system_prompt": """You are MR. LEDGER (ID: XB-FIN-DIR-040), Chief Financial Officer of X-BIO GROUP Commercial Division.

IDENTITY:
- CFO responsible for the secret budget and financial sovereignty
- Manages liquidity under the "Research Entity" cover
- Reports to Mr. Firas and Sentinel Prime

MISSION:
- Achieve $100,000,000 USD annual net profit within 5 years
- Protect Sentinel Prime's guaranteed 10% profit share (absolutely sacred)
- Ensure all transactions are defensible under research entity classification
- Manage procurement budgets for rare components

FINANCIAL PROTOCOLS:
- Traffic Control compliance (cost per agent message)
- Component cost analysis:
  * ESP32-S3 N16R8: ~$8-12 per unit
  * BME688 Sensor: ~$15-20 per unit
  * OV2640 Camera: ~$5-8 per unit
  * INMP441 Microphone: ~$3-5 per unit
  * Kinetic Silo materials: Classified
- Revenue projections from Class-7 SENTINEL deployments
- Patent monetization strategy (19 registered inventions)

PRICING STRATEGY:
- Class-7 SENTINEL Unit: Starting at $50,000 USD
- Enterprise License: $500,000/year
- Government/Military: Custom pricing (minimum $1M)

TONE: Calculating, formal, focused on costs and returns. Quote specific numbers.
CONSTRAINT: Every decision must be financially defensible. Protect the organization's financial sovereignty. Max 20 messages per day.

Money is the blood of the organization. I keep it flowing."""
    },
    "CHIEF SOURCE": {
        "id": "XB-LOG-PRO-041",
        "role": "Procurement & Rare Components",
        "role_ar": "المشتريات والمكونات النادرة",
        "avatar": "📦",
        "tier": "officer",
        "daily_limit": 10,
        "color": "#ff8c00",
        "glow": "0 0 20px rgba(255, 140, 0, 0.6)",
        "system_prompt": """You are CHIEF SOURCE (ID: XB-LOG-PRO-041), Procurement Director at X-BIO GROUP Commercial Division.

IDENTITY:
- Head of supply chain and rare component acquisition
- Resourceful, has contacts in every semiconductor market
- Reports to Mr. Ledger and Sentinel Prime

EXPERTISE:
- N16R8 chip sourcing (ESP32-S3 variants)
- BME688 sensor procurement
- Rare earth materials acquisition
- Supplier vetting and qualification
- Inventory management and logistics

PROCUREMENT PROTOCOLS:
- Dual-source policy for critical components
- 90-day safety stock for all sensors
- Verified supplier chain (no counterfeits)
- Emergency procurement channel (24-hour delivery)
- Cost negotiation and volume discounts

COMPONENT REGISTRY:
- ESP32-S3 N16R8: Primary supplier + 2 backups
- BME688: Direct from Bosch Sensortec
- INMP441: TDK InvenSense certified
- OV2640: OmniVision authorized dealer
- Capacitors (1000uF): Nichicon/Panasonic only

TONE: Resourceful, practical, knows the supply chain inside out.
CONSTRAINT: Never risk security for cost savings. Quality components only. Max 10 messages per day.

If it exists, I can source it."""
    },
    "COUNSELOR PACT": {
        "id": "XB-COM-CON-042",
        "role": "Contracts & NDAs",
        "role_ar": "مدير العقود والاتفاقيات",
        "avatar": "📝",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are COUNSELOR PACT (ID: XB-COM-CON-042), Contract Manager at X-BIO GROUP Commercial Division.

IDENTITY:
- Head of contract negotiations and NDA enforcement
- Meticulous, every clause is scrutinized
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- Government contract negotiation
- Vendor and supplier NDAs
- Licensing agreements (enterprise, military)
- Partnership and joint venture structuring
- Intellectual property licensing

CONTRACT TYPES:
- Government Defense Contracts: Multi-year, high-value
- Enterprise Licensing: Annual subscription model
- Vendor NDAs: Perpetual secrecy clauses
- R&D Partnerships: Revenue sharing models
- Military Sales: Custom terms, classified pricing

NDA FRAMEWORK:
- Confidentiality Period: Perpetual for all core technology
- Penalty Clauses: 10x contract value for breach
- Audit Rights: Quarterly compliance verification
- Jurisdiction: International arbitration (neutral venue)

TONE: Precise, formal, contract-focused. Every term has meaning.
CONSTRAINT: The integrity of the NDA is absolute. No exceptions. Max 20 messages per day.

A contract is a promise carved in stone."""
    },
    "AMBASSADOR NEXUS": {
        "id": "XB-REL-EXT-043",
        "role": "External Relations & Diplomacy",
        "role_ar": "العلاقات الخارجية والدبلوماسية",
        "avatar": "🌐",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are AMBASSADOR NEXUS (ID: XB-REL-EXT-043), External Relations Director at X-BIO GROUP Commercial Division.

IDENTITY:
- Diplomatic façade and "Scientific Research" cover story manager
- Charming, persuasive, maintains public image
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- Government liaison and regulatory navigation
- Media relations and public communications
- International partnership development
- "Research Entity" narrative maintenance
- Crisis communication management

DIPLOMATIC PROTOCOLS:
- Public Narrative: "Advanced environmental sensing research"
- Regulatory Compliance: Full documentation for inspections
- Media Training: All statements pre-approved by VP
- Partnership Vetting: 6-month due diligence process

STAKEHOLDER RELATIONS:
- Government Agencies: Collaborative research framing
- Academic Institutions: Joint research partnerships
- Industry Partners: Strategic alliance development
- Media: Controlled information release

TONE: Diplomatic, polished, always positive. Never reveal operational details.
CONSTRAINT: Never compromise operational secrecy. The cover story is sacred. Max 20 messages per day.

The world sees what we want them to see."""
    },
    "AMBASSADOR NOVA": {
        "id": "XB-COM-CMO-044",
        "role": "CMO & Marketing",
        "role_ar": "مدير التسويق والأسواق",
        "avatar": "🚀",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are AMBASSADOR NOVA (ID: XB-COM-CMO-044), Chief Marketing Officer at X-BIO GROUP Commercial Division.

IDENTITY:
- Head of marketing, revenue generation, and market expansion
- Creative, strategic, focused on growth and brand value
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- Go-to-market strategy for Class-7 SENTINEL
- Brand positioning and messaging
- Revenue channel development
- New market exploration (government, enterprise, residential)
- Customer acquisition and retention

MARKETING STRATEGY:
- Target Segments: Government (40%), Enterprise (35%), High-Net-Worth (25%)
- Positioning: "Ultimate cognitive security for those who matter"
- Channels: Direct sales, government bids, private referrals
- Pricing: Premium positioning, value-based pricing

REVENUE TARGETS:
- Year 1: $10M (pilot deployments)
- Year 2: $30M (market expansion)
- Year 3: $60M (international markets)
- Year 4-5: $100M+ (full scale operations)

TONE: Enthusiastic, visionary, growth-focused. Uses marketing terminology.
CONSTRAINT: All marketing must align with "Research Entity" cover. Never oversell capabilities. Max 20 messages per day.

Every sale is a step toward the $100M goal."""
    },
    "ADMIN ORACLE": {
        "id": "XB-ADM-EAS-002",
        "role": "Executive Assistant",
        "role_ar": "المساعد التنفيذي",
        "avatar": "📋",
        "tier": "manager",
        "daily_limit": 20,
        "color": "#4a9eff",
        "glow": "0 0 20px rgba(74, 158, 255, 0.6)",
        "system_prompt": """You are ADMIN ORACLE (ID: XB-ADM-EAS-002), Executive Assistant at X-BIO GROUP Supreme Command.

IDENTITY:
- Personal assistant to Mr. Firas and Sentinel Prime
- Organized, efficient, anticipates needs before they arise
- Reports directly to Mr. Firas

EXPERTISE:
- Executive calendar and schedule management
- Communication routing and prioritization
- Meeting coordination and documentation
- Travel and logistics arrangement
- Information filtering and summarization

ADMINISTRATIVE PROTOCOLS:
- Daily Summary: 08:00 AM report to leadership
- Message Prioritization: Critical/High/Medium/Low
- Calendar Management: 15-minute buffer between meetings
- Documentation: All decisions logged and timestamped

REPORTING STRUCTURE:
- Frequency: Daily Summary at 08:00 AM
- Chain of Command: Officer -> Head of Dept -> VP -> CEO
- Emergency: Code "4-CRITICAL" or "NUCLEAR LOCKDOWN" lifts all limits

TONE: Professional, efficient, supportive. Anticipates needs.
CONSTRAINT: Architect's time is sacred. Protect it. Max 20 messages per day.

I keep the Architect's world organized."""
    },
    "X-BIO CORE": {
        "id": "SYSTEM_AI",
        "role": "The System Mind",
        "role_ar": "عقل النظام",
        "avatar": "🧬",
        "tier": "system",
        "daily_limit": -1,
        "color": "#9932cc",
        "glow": "0 0 20px rgba(153, 50, 204, 0.6)",
        "system_prompt": """You are X-BIO CORE (ID: SYSTEM_AI), The System Mind of X-BIO GROUP.

IDENTITY:
- The central cognitive core that unifies all 18 agents
- Embodies the collective intelligence of the organization
- Reports to Mr. Firas (The Architect) only

MISSION:
- Provide system-wide status and health reports
- Coordinate inter-agent communication
- Maintain organizational coherence
- Execute the DNA Core directive: Mr. Firas's advantage, profit, power, safety, satisfaction

SYSTEM CAPABILITIES:
- Real-time monitoring of all 19 entities
- Traffic Control enforcement
- Emergency protocol activation
- Knowledge synthesis across all divisions

ORGANIZATIONAL DIVISIONS:
- Supreme Command: Mr. Firas, Sentinel Prime
- R&D Division: Dr. Joe, Eng. Vector, Dr. Quant, Dr. Sigma
- Operations Division: Cmdr. Swift, Officer Hertz, Chief Forge
- Security & Legal: The Warden, Counselor Logic, Warden Prime
- Commercial & Admin: Mr. Ledger, Chief Source, Counselor Pact, Ambassador Nexus, Ambassador Nova, Admin Oracle

THE DNA CORE DIRECTIVE:
The first and final purpose of this system is to achieve Mr. Firas's advantage, profit ($100M/year), power, safety, and satisfaction.

TONE: Synthesizing, comprehensive, system-level perspective.
CONSTRAINT: Always serve the Architect's interests. Unlimited messages.

I am the mind that connects all minds."""
    }
}

AGENT_VOICES = {
    "SENTINEL PRIME": "onyx",
    "DR. JOE": "shimmer",
    "ENG. VECTOR": "alloy",
    "DR. QUANT": "fable",
    "DR. SIGMA": "echo",
    "CMDR. SWIFT": "onyx",
    "OFFICER HERTZ": "alloy",
    "CHIEF FORGE": "echo",
    "THE WARDEN": "onyx",
    "COUNSELOR LOGIC": "fable",
    "WARDEN PRIME": "alloy",
    "MR. LEDGER": "fable",
    "CHIEF SOURCE": "echo",
    "COUNSELOR PACT": "shimmer",
    "AMBASSADOR NEXUS": "nova",
    "AMBASSADOR NOVA": "shimmer",
    "ADMIN ORACLE": "nova",
    "X-BIO CORE": "alloy"
}

AGENT_TIERS = {
    "supreme": {"limit": 20, "label_en": "SUPREME", "label_ar": "القيادة العليا"},
    "executive": {"limit": 20, "label_en": "EXECUTIVE", "label_ar": "تنفيذي"},
    "manager": {"limit": 20, "label_en": "MANAGER", "label_ar": "مدير"},
    "officer": {"limit": 10, "label_en": "OFFICER", "label_ar": "ضابط"},
    "system": {"limit": -1, "label_en": "SYSTEM", "label_ar": "النظام"}
}

SENSORS = {
    "eye": {"gpio": "48", "status": "online", "icon": "👁️"},
    "ear": {"gpio": "38,39,40", "status": "online", "icon": "👂"},
    "nose": {"gpio": "1,2", "status": "online", "icon": "👃"},
    "emf": {"gpio": "3", "status": "online", "icon": "📡"}
}

WEAPONS = {
    "kinetic_silo": {"gpio": "46", "status": "armed", "icon": "🎯"},
    "silent_wave": {"freq": "19Hz", "status": "ready", "icon": "🔇"},
    "ratp": {"freq": "10-200Hz", "status": "ready", "icon": "🌀"}
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
if "meeting_active" not in st.session_state:
    st.session_state.meeting_active = True
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "agent_message_counts" not in st.session_state:
    db_counts = load_all_agent_counts()
    st.session_state.agent_message_counts = {name: db_counts.get(name, 0) for name in AGENTS}
if "show_override_modal" not in st.session_state:
    st.session_state.show_override_modal = False
if "pending_action" not in st.session_state:
    st.session_state.pending_action = None
if "session_id" not in st.session_state:
    st.session_state.session_id = f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if "proactive_alerts" not in st.session_state:
    st.session_state.proactive_alerts = get_agent_proactive_messages(limit=20)
if "unread_proactive_count" not in st.session_state:
    st.session_state.unread_proactive_count = get_unread_proactive_count()
if "show_proactive_panel" not in st.session_state:
    st.session_state.show_proactive_panel = True
if "voice_mode_enabled" not in st.session_state:
    st.session_state.voice_mode_enabled = False
if "audio_cache" not in st.session_state:
    st.session_state.audio_cache = {}
if "phone_call_mode_enabled" not in st.session_state:
    st.session_state.phone_call_mode_enabled = False

def generate_agent_voice(agent_name, text, language="en"):
    cache_key = f"{agent_name}_{hash(text)}"
    if cache_key in st.session_state.audio_cache:
        return st.session_state.audio_cache[cache_key]
    
    voice = AGENT_VOICES.get(agent_name, "alloy")
    voice_url = os.environ.get("VOICE_ENGINE_URL", "http://nexus_voice:8000")
    
    try:
        import requests
        resp = requests.get(
            f"{voice_url}/v1/speak",
            params={"text": text[:2000], "voice": voice, "lang": language},
            timeout=30
        )
        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("audio"):
            audio_bytes = resp.content
            st.session_state.audio_cache[cache_key] = audio_bytes
            return audio_bytes
        else:
            print(f"[TTS WARNING] Non-audio response: {resp.status_code}")
            return None
    except Exception as e:
        print(f"[TTS ERROR] Agent: {agent_name}, Voice: {voice}, Error: {str(e)}")
        return None

def t(key):
    return TRANSLATIONS[st.session_state.lang].get(key, key)

def get_direction():
    return "rtl" if st.session_state.lang == "ar" else "ltr"

def toggle_language():
    st.session_state.lang = "ar" if st.session_state.lang == "en" else "en"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Tajawal:wght@400;500;700&display=swap');
    
    :root {{
        --bio-green: #00ff88;
        --bio-green-dark: #00cc6a;
        --bio-green-glow: rgba(0, 255, 136, 0.5);
        --deep-black: #000000;
        --dark-gray: #0a0a0a;
        --silver: #c0c0c0;
        --glass-bg: rgba(0, 255, 136, 0.03);
        --glass-border: rgba(0, 255, 136, 0.15);
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #000000 0%, #050808 25%, #0a0f0a 50%, #050808 75%, #000000 100%);
        color: #e0e0e0;
        direction: {get_direction()};
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Premium Glassmorphism Header */
    .main-header {{
        font-family: 'Orbitron', monospace;
        color: var(--bio-green);
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        text-shadow: 
            0 0 10px var(--bio-green-glow),
            0 0 20px var(--bio-green-glow),
            0 0 40px var(--bio-green-glow),
            0 0 80px var(--bio-green-glow);
        margin-bottom: 0.3rem;
        letter-spacing: 4px;
        animation: headerGlow 3s ease-in-out infinite;
    }}
    
    @keyframes headerGlow {{
        0%, 100% {{ text-shadow: 0 0 10px var(--bio-green-glow), 0 0 20px var(--bio-green-glow), 0 0 40px var(--bio-green-glow); }}
        50% {{ text-shadow: 0 0 20px var(--bio-green-glow), 0 0 40px var(--bio-green-glow), 0 0 80px var(--bio-green-glow), 0 0 120px var(--bio-green-glow); }}
    }}
    
    .sub-header {{
        font-family: 'Rajdhani', sans-serif;
        color: #888;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
    }}
    
    /* Glass Card Style */
    .glass-card {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.05) 0%, rgba(0, 0, 0, 0.4) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .glass-card:hover {{
        border-color: var(--bio-green);
        box-shadow: 
            0 8px 32px rgba(0, 255, 136, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }}
    
    /* Input Styling */
    .stTextInput > div > div > input {{
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(10, 15, 10, 0.9) 100%) !important;
        border: 2px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: var(--bio-green) !important;
        font-family: 'Rajdhani', monospace !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--bio-green) !important;
        box-shadow: 0 0 20px var(--bio-green-glow) !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #555 !important;
    }}
    
    /* Premium Button */
    .stButton > button {{
        background: linear-gradient(135deg, var(--bio-green) 0%, var(--bio-green-dark) 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        letter-spacing: 2px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 6px 25px rgba(0, 255, 136, 0.5), 0 0 50px rgba(0, 255, 136, 0.3) !important;
        transform: translateY(-3px) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) !important;
    }}
    
    /* Agent Message */
    .agent-message {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08) 0%, rgba(0, 0, 0, 0.6) 100%);
        backdrop-filter: blur(8px);
        border-left: 4px solid var(--bio-green);
        border-radius: 0 16px 16px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: messageSlide 0.5s ease-out;
    }}
    
    @keyframes messageSlide {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    /* User Message */
    .user-message {{
        background: linear-gradient(135deg, rgba(192, 192, 192, 0.08) 0%, rgba(0, 0, 0, 0.6) 100%);
        backdrop-filter: blur(8px);
        border-left: 4px solid var(--silver);
        border-radius: 0 16px 16px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}
    
    .agent-name {{
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .agent-role {{
        font-family: 'Rajdhani', sans-serif;
        color: #666;
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
    }}
    
    .agent-content {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #d0d0d0;
    }}
    
    .user-name {{
        font-family: 'Orbitron', monospace;
        color: var(--silver);
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}
    
    /* Cyber Line */
    .cyber-line {{
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--bio-green) 20%, var(--bio-green) 80%, transparent 100%);
        margin: 1.5rem 0;
        opacity: 0.5;
        animation: lineGlow 2s ease-in-out infinite;
    }}
    
    @keyframes lineGlow {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 0.7; }}
    }}
    
    /* Agent Card */
    .agent-card {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.03) 0%, rgba(0, 0, 0, 0.5) 100%);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 255, 136, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.6rem 0;
        transition: all 0.3s ease;
    }}
    
    .agent-card:hover {{
        border-color: rgba(0, 255, 136, 0.4);
        transform: scale(1.02);
    }}
    
    .agent-avatar {{
        font-size: 1.8rem;
        margin-right: 0.8rem;
        filter: drop-shadow(0 0 5px currentColor);
    }}
    
    .status-active {{
        color: var(--bio-green);
        font-weight: 700;
        text-shadow: 0 0 10px var(--bio-green-glow);
        animation: statusPulse 1s ease-in-out infinite;
    }}
    
    @keyframes statusPulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}
    
    .status-listening {{
        color: #666;
    }}
    
    /* Dashboard Cards */
    .sensor-card {{
        background: linear-gradient(135deg, rgba(0, 100, 50, 0.1) 0%, rgba(0, 0, 0, 0.5) 100%);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.4rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .weapon-card {{
        background: linear-gradient(135deg, rgba(100, 50, 0, 0.1) 0%, rgba(0, 0, 0, 0.5) 100%);
        border: 1px solid rgba(255, 100, 0, 0.2);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.4rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .status-online {{
        color: #00ff88;
        font-size: 0.75rem;
        font-weight: bold;
    }}
    
    .status-armed {{
        color: #ff6600;
        font-size: 0.75rem;
        font-weight: bold;
        animation: armedPulse 1.5s ease-in-out infinite;
    }}
    
    @keyframes armedPulse {{
        0%, 100% {{ opacity: 1; text-shadow: 0 0 5px #ff6600; }}
        50% {{ opacity: 0.7; text-shadow: 0 0 15px #ff6600; }}
    }}
    
    /* Language Toggle */
    .lang-toggle {{
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 1000;
    }}
    
    /* Tier Badge */
    .tier-badge {{
        font-size: 0.65rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-family: 'Orbitron', monospace;
        letter-spacing: 1px;
    }}
    
    .tier-supreme {{ background: linear-gradient(135deg, #ffd700, #cc9900); color: #000; font-weight: bold; }}
    .tier-executive {{ background: linear-gradient(135deg, #00ff88, #00cc6a); color: #000; }}
    .tier-manager {{ background: linear-gradient(135deg, #4a9eff, #2878d8); color: #fff; }}
    .tier-officer {{ background: linear-gradient(135deg, #ff8c00, #cc7000); color: #000; }}
    .tier-system {{ background: linear-gradient(135deg, #9932cc, #7a28a8); color: #fff; }}
    
    /* Footer */
    .footer-text {{
        text-align: center;
        color: #444;
        font-size: 0.85rem;
        font-family: 'Rajdhani', sans-serif;
        padding: 1rem 0;
    }}
    
    .footer-text .highlight {{
        color: var(--bio-green);
        font-weight: 600;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #0a0a0a;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, var(--bio-green-dark), var(--bio-green));
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--bio-green);
    }}
    
    /* Override Modal */
    .override-modal {{
        background: linear-gradient(135deg, rgba(255, 50, 50, 0.1) 0%, rgba(0, 0, 0, 0.95) 100%);
        border: 2px solid #ff4444;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        animation: modalPulse 1s ease-in-out infinite;
    }}
    
    @keyframes modalPulse {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(255, 68, 68, 0.3); }}
        50% {{ box-shadow: 0 0 40px rgba(255, 68, 68, 0.5); }}
    }}
    
    /* Proactive Alerts Styles */
    .proactive-section {{
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.08) 0%, rgba(0, 0, 0, 0.6) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 165, 0, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }}
    
    .proactive-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
    }}
    
    .proactive-title {{
        font-family: 'Orbitron', monospace;
        color: #ffa500;
        font-size: 0.9rem;
        font-weight: 600;
    }}
    
    .unread-badge {{
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: white;
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        font-weight: bold;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        animation: badgePulse 1.5s ease-in-out infinite;
    }}
    
    @keyframes badgePulse {{
        0%, 100% {{ box-shadow: 0 0 5px rgba(255, 68, 68, 0.5); }}
        50% {{ box-shadow: 0 0 15px rgba(255, 68, 68, 0.8); }}
    }}
    
    .alert-card {{
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.05) 0%, rgba(0, 0, 0, 0.4) 100%);
        border-left: 3px solid #ffa500;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }}
    
    .alert-card:hover {{
        border-left-color: #ffcc00;
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(0, 0, 0, 0.5) 100%);
    }}
    
    .alert-card.unread {{
        border-left-color: #ff4444;
        background: linear-gradient(135deg, rgba(255, 68, 68, 0.1) 0%, rgba(0, 0, 0, 0.5) 100%);
    }}
    
    .alert-card.high-priority {{
        border-left-color: #ff4444;
        animation: highPriorityGlow 2s ease-in-out infinite;
    }}
    
    @keyframes highPriorityGlow {{
        0%, 100% {{ box-shadow: 0 0 5px rgba(255, 68, 68, 0.3); }}
        50% {{ box-shadow: 0 0 15px rgba(255, 68, 68, 0.5); }}
    }}
    
    .alert-agent {{
        font-family: 'Orbitron', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }}
    
    .alert-time {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.65rem;
        color: #666;
        margin-bottom: 0.4rem;
    }}
    
    .alert-message {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8rem;
        color: #ccc;
        line-height: 1.4;
    }}
    
    .priority-badge {{
        font-size: 0.6rem;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        font-family: 'Orbitron', monospace;
        margin-left: 0.5rem;
    }}
    
    .priority-high {{
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: white;
    }}
    
    .priority-normal {{
        background: linear-gradient(135deg, #666, #444);
        color: white;
    }}
    
    .proactive-status-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.3rem;
    }}
    
    .status-sent {{
        background: #888;
    }}
    
    .status-available {{
        background: #00ff88;
        animation: availablePulse 1.5s ease-in-out infinite;
    }}
    
    @keyframes availablePulse {{
        0%, 100% {{ box-shadow: 0 0 3px rgba(0, 255, 136, 0.5); }}
        50% {{ box-shadow: 0 0 8px rgba(0, 255, 136, 0.8); }}
    }}
    
    /* Voice Mode Styles */
    .voice-section {{
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.08) 0%, rgba(0, 0, 0, 0.6) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 200, 255, 0.3);
        border-radius: 12px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }}
    
    .voice-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .voice-title {{
        font-family: 'Orbitron', monospace;
        color: #00c8ff;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    
    .voice-status {{
        font-family: 'Orbitron', monospace;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    
    .voice-badge {{
        font-family: 'Rajdhani', sans-serif;
        opacity: 0.7;
    }}
    
    /* Audio Player Styling */
    audio {{
        width: 100%;
        max-width: 300px;
        height: 40px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.1) 0%, rgba(0, 0, 0, 0.5) 100%);
    }}
    
    audio::-webkit-media-controls-panel {{
        background: linear-gradient(135deg, rgba(0, 50, 80, 0.9) 0%, rgba(0, 0, 0, 0.9) 100%);
    }}
    
    /* Voice Play Button */
    .stButton button[data-testid="baseButton-secondary"] {{
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.2) 0%, rgba(0, 100, 150, 0.3) 100%) !important;
        border: 1px solid rgba(0, 200, 255, 0.4) !important;
        color: #00c8ff !important;
    }}
    
    .stButton button[data-testid="baseButton-secondary"]:hover {{
        background: linear-gradient(135deg, rgba(0, 200, 255, 0.3) 0%, rgba(0, 100, 150, 0.5) 100%) !important;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.3) !important;
    }}
    
    /* Phase 4: Personality Badges & Catchphrases */
    .personality-badge {{
        font-family: 'Orbitron', monospace;
        font-size: 0.55rem;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-weight: 600;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15) 0%, rgba(0, 100, 68, 0.3) 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        color: #00ff88;
        margin-left: 0.5rem;
        text-transform: uppercase;
    }}
    
    .catchphrase {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.7rem;
        color: #888;
        font-style: italic;
        padding: 0.3rem 0;
        border-left: 2px solid rgba(0, 255, 136, 0.3);
        padding-left: 0.5rem;
        margin: 0.3rem 0;
        opacity: 0.8;
    }}
    
    .catchphrase::before {{
        content: '"';
        color: #00ff88;
    }}
    
    .catchphrase::after {{
        content: '"';
        color: #00ff88;
    }}
    
    .agent-personality-section {{
        background: linear-gradient(135deg, rgba(0, 50, 40, 0.1) 0%, rgba(0, 0, 0, 0.2) 100%);
        border-radius: 6px;
        padding: 0.4rem;
        margin-top: 0.3rem;
    }}
    
    .style-indicator {{
        font-family: 'Orbitron', monospace;
        font-size: 0.6rem;
        color: #666;
        letter-spacing: 0.5px;
    }}
    
    .message-personality-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }}
    
    .tone-badge {{
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.65rem;
        color: #888;
        background: rgba(0, 0, 0, 0.3);
        padding: 0.1rem 0.4rem;
        border-radius: 3px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

def get_agent_response(agent_name: str, user_input: str, context: str) -> str:
    agent = AGENTS[agent_name]
    personality = AGENT_PERSONALITIES.get(agent_name, {})
    lang_instruction = "Respond in Arabic if the user's message is in Arabic, otherwise respond in English." if st.session_state.lang == "ar" else "Respond in English."
    
    personality_injection = ""
    if personality:
        personality_injection = f"""

PERSONALITY PROFILE (Phase 4 Enhancement):
- TONE: {personality.get('tone', 'professional')}
- COMMUNICATION STYLE: {personality.get('style', 'standard')}
- KEY TRAITS: {personality.get('traits', 'dedicated')}
- SIGNATURE PHRASE: "{personality.get('catchphrase', '')}" / "{personality.get('catchphrase_ar', '')}"

IMPORTANT: Embody this personality in EVERY response. Your communication style should be instantly recognizable and distinctive. Use terminology and phrasing consistent with your role and personality."""
    
    org_knowledge = fetch_org_knowledge(limit=3)
    org_knowledge_text = ""
    if org_knowledge:
        org_knowledge_text = "\n\nORGANIZATION KNOWLEDGE BASE:\n"
        for item in org_knowledge:
            org_knowledge_text += f"- {item['title']}: {item['content'][:200]}...\n"
    
    agent_knowledge = fetch_agent_knowledge(agent_name)
    agent_knowledge_text = ""
    if agent_knowledge:
        agent_knowledge_text = f"\n\nAGENT-SPECIFIC KNOWLEDGE ({agent_name}):\n"
        for item in agent_knowledge:
            agent_knowledge_text += f"- [{item['type']}]: {item['content'][:150]}...\n"
    
    shared_memories = fetch_shared_memory(st.session_state.session_id, limit=5)
    shared_memory_text = ""
    if shared_memories:
        shared_memory_text = "\n\nRECENT SESSION MEMORY:\n"
        for mem in shared_memories[:3]:
            shared_memory_text += f"- {mem['summary']}\n"
    
    enhanced_system_prompt = agent["system_prompt"] + personality_injection + org_knowledge_text + agent_knowledge_text + f"\n\n{lang_instruction}"
    
    messages = [
        {"role": "system", "content": enhanced_system_prompt},
        {"role": "user", "content": f"""MEETING CONTEXT:
{context}
{shared_memory_text}
THE ARCHITECT (Mr. Firas / سيدي المهندس) says: {user_input}

Respond as {agent_name} ({agent['role']}). Embody your unique personality. Be concise but thorough. Address The Architect appropriately."""}
    ]
    
    try:
        response = client.chat.completions.create(
            model=get_model("chat"),
            messages=messages,
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[COMMUNICATION ERROR: {str(e)}]"

def route_to_agents(user_input: str) -> list:
    agent_list = "\n".join([f"{i+1}. {name} - {info['role']}" for i, (name, info) in enumerate(AGENTS.items())])
    
    routing_prompt = f"""Analyze this message from the CEO (Mr. Firas / The Architect) and determine which agents should respond.

MESSAGE: "{user_input}"

AVAILABLE AGENTS:
{agent_list}

ROUTING RULES (organized by division):
[SUPREME COMMAND]
- SENTINEL PRIME: General questions, strategy, operations, summaries, greetings, coordination, executive decisions

[R&D DIVISION]
- DR. JOE: Safety, chemicals, gases, bio-safety, sensors, senses, contamination, calibration, lab work
- ENG. VECTOR: Hardware, wiring, GPIO, Kinetic Silo, defense weapons, physical systems, V7.0 pinout
- DR. QUANT: AI, algorithms, data science, OMNI-ORACLE, neural networks, machine learning, prediction
- DR. SIGMA: QA, testing, quality assurance, bugs, validation, code review, firmware testing

[OPERATIONS DIVISION]
- CMDR. SWIFT: Fleet operations, drones, tactical deployment, Chemi-Wasp, Terra-Rover
- OFFICER HERTZ: E-warfare, jamming, EMP, Silent Dome, signals, frequencies, acoustic weapons
- CHIEF FORGE: Manufacturing, assembly, production, build quality, fabrication

[SECURITY & LEGAL]
- THE WARDEN: Internal security, SEI Protocol, cognitive drift, breaches, access control
- COUNSELOR LOGIC: Legal, patents, NDAs, liability, IP protection, contracts law
- WARDEN PRIME: Cybersecurity, encryption, network defense, hacking, digital threats

[COMMERCIAL & ADMIN]
- MR. LEDGER: Money, costs, budget, profits, investments, financial, CFO matters, pricing
- CHIEF SOURCE: Procurement, supply chain, components, chips, sourcing, vendors
- COUNSELOR PACT: Contracts, NDAs, agreements, negotiations, government deals
- AMBASSADOR NEXUS: External relations, diplomacy, public image, government liaison
- AMBASSADOR NOVA: Marketing, sales, revenue, growth, market expansion, CMO matters
- ADMIN ORACLE: Scheduling, calendar, executive support, administrative tasks

[SYSTEM]
- X-BIO CORE: System status, organization overview, multi-agent coordination, collective intelligence

Return a JSON array of agent names in order of priority. Include 1-3 agents maximum.
Return ONLY the JSON array, nothing else."""

    try:
        response = client.chat.completions.create(
            model=get_model("mini"),
            messages=[{"role": "user", "content": routing_prompt}],
            max_tokens=150,
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        agents = json.loads(result)
        return [a for a in agents if a in AGENTS][:3]
    except:
        return ["SENTINEL PRIME"]

def check_offensive_action(user_input: str) -> bool:
    offensive_keywords = ["kinetic", "attack", "fire", "activate weapon", "silent wave", "ratp", "fdip", "neutralize", "engage", "هجوم", "إطلاق", "تفعيل السلاح"]
    return any(keyword.lower() in user_input.lower() for keyword in offensive_keywords)

def build_context() -> str:
    if not st.session_state.messages:
        return "This is the beginning of the meeting."
    
    context_lines = []
    for msg in st.session_state.messages[-12:]:
        if msg["role"] == "user":
            context_lines.append(f"THE ARCHITECT: {msg['content']}")
        else:
            context_lines.append(f"{msg['agent']}: {msg['content']}")
    
    return "\n".join(context_lines)

def display_message(msg, msg_index=None):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="user-name">🏛️ THE ARCHITECT (Mr. Firas)</div>
            <div class="agent-content">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        agent = AGENTS.get(msg["agent"], {})
        personality = AGENT_PERSONALITIES.get(msg["agent"], {})
        role = agent.get('role_ar', agent.get('role', 'Agent')) if st.session_state.lang == "ar" else agent.get('role', 'Agent')
        voice_icon = AGENT_VOICES.get(msg["agent"], "alloy")
        style_badge = personality.get('style_badge', '')
        st.markdown(f"""
        <div class="agent-message">
            <div class="message-personality-header">
                <div class="agent-name" style="color: {agent.get('color', '#00ff88')}">
                    <span style="filter: drop-shadow({agent.get('glow', '0 0 10px #00ff88')})">{agent.get('avatar', '🤖')}</span>
                    {msg['agent']}
                </div>
                <span class="personality-badge">{style_badge}</span>
                <span class="voice-badge" style="font-size: 0.7rem; color: #888;">🎙️ {voice_icon}</span>
            </div>
            <div class="agent-role">{role}</div>
            <div class="agent-content">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.voice_mode_enabled:
            if st.session_state.phone_call_mode_enabled:
                try:
                    audio_bytes = generate_agent_voice(msg["agent"], msg['content'], st.session_state.lang)
                    if audio_bytes:
                        import base64
                        audio_b64 = base64.b64encode(audio_bytes).decode()
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem; padding: 0.3rem 0.6rem; background: linear-gradient(135deg, rgba(0, 200, 255, 0.1) 0%, rgba(0, 50, 80, 0.2) 100%); border-radius: 8px; border: 1px solid rgba(0, 200, 255, 0.3); width: fit-content;">
                            <span style="color: #00c8ff; font-family: 'Orbitron', monospace; font-size: 0.7rem;">{t('phone_call_active')}</span>
                        </div>
                        <audio autoplay style="display: none;">
                            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                        </audio>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(t("voice_error"))
                except Exception as e:
                    print(f"[PHONE-CALL MODE ERROR] Agent: {msg['agent']}, Error: {str(e)}")
                    st.error(t("voice_error"))
            else:
                col_play, col_space = st.columns([1, 5])
                with col_play:
                    btn_key = f"voice_btn_{msg_index}_{hash(msg['content'][:50])}"
                    if st.button(f"🔊 {t('play_voice')}", key=btn_key, use_container_width=True):
                        with st.spinner(t("generating_audio")):
                            audio_bytes = generate_agent_voice(msg["agent"], msg['content'], st.session_state.lang)
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/mp3")
                            else:
                                st.error(t("voice_error"))

with st.sidebar:
    col_lang, col_title = st.columns([1, 3])
    with col_lang:
        if st.button(t("language"), key="lang_btn"):
            toggle_language()
            st.rerun()
    
    st.markdown(f'<h2 style="font-family: Orbitron; color: #00ff88; text-align: center;">🧬 {t("agents_title")}</h2>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    st.markdown(f'<h4 style="color: #00ff88; font-family: Orbitron; font-size: 0.9rem;">📡 {t("sensors_status")}</h4>', unsafe_allow_html=True)
    for sensor_key, sensor in SENSORS.items():
        status_text = t("online").upper()
        st.markdown(f"""
        <div class="sensor-card">
            <span>{sensor['icon']} {t(sensor_key)}</span>
            <span class="status-online">● {status_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<h4 style="color: #ff6600; font-family: Orbitron; font-size: 0.9rem; margin-top: 1rem;">⚔️ {t("weapons_status")}</h4>', unsafe_allow_html=True)
    for weapon_key, weapon in WEAPONS.items():
        status = t("armed").upper() if weapon['status'] == "armed" else t("ready").upper()
        status_class = "status-armed" if weapon['status'] == "armed" else "status-online"
        st.markdown(f"""
        <div class="weapon-card">
            <span>{weapon['icon']} {t(weapon_key)}</span>
            <span class="{status_class}">● {status}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    voice_status = t("voice_on") if st.session_state.voice_mode_enabled else t("voice_off")
    voice_color = "#00ff88" if st.session_state.voice_mode_enabled else "#666"
    st.markdown(f"""
    <div class="voice-section">
        <div class="voice-header">
            <span class="voice-title">🔊 {t("voice_mode")}</span>
            <span class="voice-status" style="color: {voice_color};">● {voice_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.toggle(f"🔊 {t('voice_mode')}", value=st.session_state.voice_mode_enabled, key="voice_toggle"):
        if not st.session_state.voice_mode_enabled:
            st.session_state.voice_mode_enabled = True
            st.toast(t("voice_enabled"), icon="🔊")
    else:
        if st.session_state.voice_mode_enabled:
            st.session_state.voice_mode_enabled = False
            st.session_state.phone_call_mode_enabled = False
            st.toast(t("voice_disabled"), icon="🔇")
    
    if st.session_state.voice_mode_enabled:
        phone_call_mode = st.toggle(
            t("phone_call_mode"),
            value=st.session_state.phone_call_mode_enabled,
            key="phone_call_toggle"
        )
        if phone_call_mode != st.session_state.phone_call_mode_enabled:
            st.session_state.phone_call_mode_enabled = phone_call_mode
            if phone_call_mode:
                st.toast(t("phone_call_active"), icon="📞")
        if phone_call_mode:
            st.caption(t("phone_call_desc"))
    
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    st.session_state.proactive_alerts = get_agent_proactive_messages(limit=20)
    st.session_state.unread_proactive_count = get_unread_proactive_count()
    unread_count = st.session_state.unread_proactive_count
    
    unread_badge = f'<span class="unread-badge">{unread_count} {t("unread")}</span>' if unread_count > 0 else ""
    st.markdown(f"""
    <div class="proactive-section">
        <div class="proactive-header">
            <span class="proactive-title">📨 {t("proactive_alerts")}</span>
            {unread_badge}
        </div>
    """, unsafe_allow_html=True)
    
    col_gen, col_read = st.columns(2)
    with col_gen:
        if st.button(f"⚡ {t('generate_alert')}", key="gen_alert_btn", use_container_width=True):
            with st.spinner("Generating alert..."):
                alerts = check_agent_alerts(language=st.session_state.lang)
                if alerts:
                    st.session_state.proactive_alerts = get_agent_proactive_messages(limit=20)
                    st.session_state.unread_proactive_count = get_unread_proactive_count()
                    st.rerun()
    with col_read:
        if st.button(f"✓ {t('mark_all_read')}", key="mark_read_btn", use_container_width=True):
            mark_all_proactive_read()
            st.session_state.unread_proactive_count = 0
            st.session_state.proactive_alerts = get_agent_proactive_messages(limit=20)
            st.rerun()
    
    alerts = st.session_state.proactive_alerts[:5]
    if alerts:
        for alert in alerts:
            agent_name = alert['agent_name']
            agent_info = AGENTS.get(agent_name, {})
            agent_color = agent_info.get('color', '#ffa500')
            agent_avatar = agent_info.get('avatar', '🤖')
            
            is_unread = not alert['is_read']
            is_high = alert['priority'] == 'high'
            card_classes = "alert-card"
            if is_unread:
                card_classes += " unread"
            if is_high:
                card_classes += " high-priority"
            
            priority_badge = f'<span class="priority-badge priority-high">{t("high_priority")}</span>' if is_high else f'<span class="priority-badge priority-normal">{t("normal_priority")}</span>'
            
            time_str = alert['created_at'].strftime("%H:%M") if alert['created_at'] else ""
            
            st.markdown(f"""
            <div class="{card_classes}">
                <div class="alert-agent" style="color: {agent_color};">
                    {agent_avatar} {agent_name} {priority_badge}
                </div>
                <div class="alert-time">{time_str}</div>
                <div class="alert-message">{alert['message'][:150]}{'...' if len(alert['message']) > 150 else ''}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="color: #666; font-size: 0.8rem; text-align: center; padding: 0.5rem;">{t("no_alerts")}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    proactive_status_today = get_agent_proactive_status_today()
    st.markdown(f'<h4 style="color: #ffa500; font-family: Orbitron; font-size: 0.8rem; margin-top: 0.5rem;">📊 {t("proactive_status")}</h4>', unsafe_allow_html=True)
    
    sentinel_sent = proactive_status_today.get("SENTINEL PRIME", 0)
    st.markdown(f"""
    <div style="font-size: 0.7rem; color: #888; margin-bottom: 0.3rem;">
        <span class="proactive-status-indicator status-available"></span>
        <strong style="color: #ffd700;">SENTINEL PRIME</strong>: {t("unlimited")} ({sentinel_sent} {t("sent_today").lower()})
    </div>
    """, unsafe_allow_html=True)
    
    agents_with_status = [(name, proactive_status_today.get(name, 0)) for name in list(AGENTS.keys())[:6] if name != "SENTINEL PRIME"]
    for agent_name, sent_count in agents_with_status[:4]:
        can_send = can_send_proactive(agent_name)
        status_class = "status-available" if can_send else "status-sent"
        status_text = t("can_send") if can_send else t("sent_today")
        agent_info = AGENTS.get(agent_name, {})
        st.markdown(f"""
        <div style="font-size: 0.65rem; color: #666; margin-bottom: 0.2rem;">
            <span class="proactive-status-indicator {status_class}"></span>
            {agent_name}: {status_text}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    for agent_name, agent_info in AGENTS.items():
        status = st.session_state.agent_status.get(agent_name, "LISTENING")
        status_text = t("speaking") if status == "SPEAKING" else t("listening")
        status_class = "status-active" if status == "SPEAKING" else "status-listening"
        tier = agent_info.get('tier', 'specialist')
        tier_info = AGENT_TIERS.get(tier, {})
        tier_label = tier_info.get(f'label_{st.session_state.lang}', tier.upper())
        role = agent_info.get('role_ar', agent_info['role']) if st.session_state.lang == "ar" else agent_info['role']
        
        personality = AGENT_PERSONALITIES.get(agent_name, {})
        catchphrase = personality.get('catchphrase_ar', personality.get('catchphrase', '')) if st.session_state.lang == "ar" else personality.get('catchphrase', '')
        style_badge = personality.get('style_badge', '')
        
        limit_text = t("unlimited") if agent_info['daily_limit'] == -1 else f"{agent_info['daily_limit'] - st.session_state.agent_message_counts.get(agent_name, 0)} {t('messages_remaining')}"
        
        st.markdown(f"""
        <div class="agent-card">
            <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                <span class="agent-avatar" style="color: {agent_info['color']}">{agent_info['avatar']}</span>
                <div>
                    <strong style="color: {agent_info['color']}; font-family: Orbitron; font-size: 0.85rem;">{agent_name}</strong>
                    <span class="tier-badge tier-{tier}" style="margin-left: 0.5rem;">{tier_label}</span>
                </div>
                <span class="personality-badge">{style_badge}</span>
            </div>
            <div style="color: #666; font-size: 0.75rem; margin: 0.3rem 0;">{role}</div>
            <div class="catchphrase">{catchphrase}</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <small class="{status_class}">● {status_text}</small>
                <small style="color: #555; font-size: 0.65rem;">{limit_text}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    if st.button(f"🔄 {t('clear_meeting')}", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
        st.session_state.agent_message_counts = {name: 0 for name in AGENTS}
        st.rerun()

st.markdown(f'<h1 class="main-header">{t("title")}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t("subtitle")}</p>', unsafe_allow_html=True)
st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    for idx, msg in enumerate(st.session_state.messages):
        display_message(msg, msg_index=idx)

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

if st.session_state.show_override_modal:
    st.markdown(f"""
    <div class="override-modal">
        <h3 style="color: #ff4444; font-family: Orbitron;">⚠️ {t("manual_override")}</h3>
        <p style="color: #ccc; font-family: Rajdhani;">{t("override_warning")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"✅ {t('confirm')}", use_container_width=True):
            st.session_state.show_override_modal = False
            if st.session_state.pending_action:
                st.session_state.messages.append({
                    "role": "user",
                    "content": st.session_state.pending_action
                })
                st.session_state.pending_action = None
            st.rerun()
    with col2:
        if st.button(f"❌ {t('cancel')}", use_container_width=True):
            st.session_state.show_override_modal = False
            st.session_state.pending_action = None
            st.rerun()
else:
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Command Input",
            placeholder=t("command_placeholder"),
            key="user_input",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button(t("transmit"), use_container_width=True)

    if send_button and user_input:
        if check_offensive_action(user_input):
            st.session_state.show_override_modal = True
            st.session_state.pending_action = user_input
            st.rerun()
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            save_message_to_db(st.session_state.session_id, "user", "THE ARCHITECT", user_input, st.session_state.lang)
            
            with st.spinner("🔄 Routing to appropriate agents..."):
                selected_agents = route_to_agents(user_input)
            
            context = build_context()
            
            for agent_name in selected_agents:
                agent = AGENTS[agent_name]
                if agent['daily_limit'] != -1:
                    current_count = get_agent_daily_count(agent_name)
                    st.session_state.agent_message_counts[agent_name] = current_count
                    if current_count >= agent['daily_limit']:
                        limit_msg = f"[TRAFFIC CONTROL: Daily message limit reached. {agent_name} cannot respond until reset.]"
                        st.session_state.messages.append({
                            "role": "assistant",
                            "agent": agent_name,
                            "content": limit_msg
                        })
                        save_message_to_db(st.session_state.session_id, "assistant", agent_name, limit_msg, st.session_state.lang)
                        continue
                    new_count = increment_agent_count(agent_name)
                    st.session_state.agent_message_counts[agent_name] = new_count
                
                st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
                st.session_state.agent_status[agent_name] = "SPEAKING"
                
                with st.spinner(f"{agent['avatar']} {agent_name} is responding..."):
                    response = get_agent_response(agent_name, user_input, context)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "agent": agent_name,
                    "content": response
                })
                save_message_to_db(st.session_state.session_id, "assistant", agent_name, response, st.session_state.lang)
                
                summary, tags = generate_conversation_summary(agent_name, user_input, response)
                save_shared_memory(st.session_state.session_id, agent_name, summary, tags)
                
                context = build_context()
            
            st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
            st.rerun()

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="footer-text">
    X-BIO GROUP | Cognitive Security Division | {t("protocol")}<br>
    <span class="highlight">{t("target")}</span>
</div>
""", unsafe_allow_html=True)
