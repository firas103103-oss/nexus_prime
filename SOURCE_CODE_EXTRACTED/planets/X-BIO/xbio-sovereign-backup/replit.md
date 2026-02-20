# X-BIO GROUP Projects

## Overview
This repository contains two X-BIO GROUP applications:
1. **X-BIO Corporate Website** - An immersive corporate website with 3D visuals and bilingual support
2. **X-BIO Cognitive Boardroom** - A multi-agent AI meeting simulation system (V4.0 NEXUS)

---

# X-BIO Cognitive Boardroom (V4.0 NEXUS)

## Overview
A real-time "Boardroom Simulation" using Streamlit and OpenAI where Mr. Firas (The Architect) can hold interactive meetings with 18 autonomous AI agents across 5 divisions. The system features unified knowledge base, proactive communication, voice synthesis, and unique agent personalities.

## V4.0 NEXUS Features

### 1. Unified Knowledge Base & Memory System
- **Organization Knowledge**: Company structure, patents, financial targets, protocols
- **Agent Knowledge**: Role-specific expertise for each of 18 agents
- **Shared Memory**: Synchronized context between all agents
- **Mr. Firas Profile**: Complete information about The Architect

### 2. Proactive Communication System
- Agents can initiate contact with Mr. Firas for urgent matters
- **Limit**: 1 proactive message/day per agent
- **SENTINEL PRIME Governance**: Restricted to authorized alerts only:
  - CODE_RED (imminent threat)
  - 4-CRITICAL (critical infrastructure breach)
  - FINANCIAL_SOVEREIGN (threat to $100M target)
  - THREAT_TO_ARCHITECT (direct threat to Mr. Firas)
  - INFRASTRUCTURE_BREACH (critical system breach)
  - PROFIT_TARGET_THREAT (threat to financial goals)
  - 10_PERCENT_SHARE_THREAT (threat to guaranteed 10% share)
- Regular meeting messages NOT counted as proactive
- Proactive alerts panel in sidebar

### 3. Voice Communication (OpenAI TTS)
- Unique voice assigned to each agent (onyx, shimmer, alloy, fable, echo, nova)
- Voice mode toggle in sidebar
- Audio playback for agent responses
- Bilingual voice support (EN/AR)

### 4. Enhanced Unique Personalities
- Each agent has distinct tone, style, traits, and catchphrase
- Personality badges displayed in UI
- Style-appropriate communication patterns
- Bilingual greetings

## Tech Stack
- **Frontend**: Streamlit with Premium Glassmorphism UI
- **AI**: OpenAI GPT-4o (via Replit AI Integrations)
- **Voice**: OpenAI TTS API
- **Intent Routing**: GPT-4o-mini for smart agent selection
- **Database**: PostgreSQL for knowledge, memory, logs, and traffic control
- **Languages**: Bilingual (English/Arabic) with RTL support

## Organizational Structure (19 Entities Total)

### SUPREME COMMAND
- **MR. FIRAS (XB-SUP-CEO-001)**: The Architect, CEO - UNLIMITED
- **SENTINEL PRIME (XB-SUP-VP-001)**: Vice President & The Engine - 20 msgs/day (Governed proactive: 7 authorized alert types)

### R&D DIVISION
- **DR. JOE (XB-RND-MGR-010)**: Lab Manager & Bio-Safety - 20 msgs/day (Head)
- **ENG. VECTOR (XB-RND-ENG-011)**: Hardware Lead & Kinetic Silo - 10 msgs/day (Officer)
- **DR. QUANT (XB-RND-DSA-012)**: Data Scientist & Algorithms - 20 msgs/day (Head)
- **DR. SIGMA (XB-RND-QAA-013)**: QA Architect & Testing - 10 msgs/day (Officer)

### OPERATIONS DIVISION
- **CMDR. SWIFT (XB-OPS-CDR-020)**: Fleet Commander & Drones - 20 msgs/day (Head)
- **OFFICER HERTZ (XB-OPS-EWF-021)**: E-Warfare & Jamming - 10 msgs/day (Officer)
- **CHIEF FORGE (XB-OPS-MFG-022)**: Manufacturing & Assembly - 10 msgs/day (Officer)

### SECURITY & LEGAL
- **THE WARDEN (XB-SEC-CHF-030)**: Internal Security & SEI Protocol - 20 msgs/day (Head)
- **COUNSELOR LOGIC (XB-LEG-ADV-031)**: Legal Advisor & 19 Patents - 20 msgs/day (Head)
- **WARDEN PRIME (XB-SEC-CSA-032)**: Cybersecurity & Network Defense - 10 msgs/day (Officer)

### COMMERCIAL & ADMIN
- **MR. LEDGER (XB-FIN-DIR-040)**: CFO & Budget/Liquidity - 20 msgs/day (Executive)
- **CHIEF SOURCE (XB-LOG-PRO-041)**: Procurement & Rare Chips - 10 msgs/day (Officer)
- **COUNSELOR PACT (XB-COM-CON-042)**: Contracts & NDAs - 20 msgs/day (Head)
- **AMBASSADOR NEXUS (XB-REL-EXT-043)**: External Relations & Diplomacy - 20 msgs/day (Head)
- **AMBASSADOR NOVA (XB-COM-CMO-044)**: CMO & Marketing - 20 msgs/day (Head)
- **ADMIN ORACLE (XB-ADM-EAS-002)**: Executive Assistant - 20 msgs/day (Head)

### SYSTEM
- **X-BIO CORE (SYSTEM_AI)**: The System Mind - Unlimited

## Agent Voice Assignments
| Agent | Voice | Style |
|-------|-------|-------|
| SENTINEL PRIME | onyx | Authoritative, Strategic |
| DR. JOE | shimmer | Scientific, Methodical |
| ENG. VECTOR | alloy | Technical, Hardware-focused |
| DR. QUANT | fable | Analytical, Data-driven |
| DR. SIGMA | echo | Methodical, Quality-focused |
| CMDR. SWIFT | onyx | Military, Tactical |
| OFFICER HERTZ | alloy | E-Warfare, Technical |
| CHIEF FORGE | echo | Industrial, Practical |
| THE WARDEN | onyx | Security, Authoritative |
| COUNSELOR LOGIC | fable | Legal, Articulate |
| WARDEN PRIME | alloy | Cyber, Technical |
| MR. LEDGER | fable | Financial, Professional |
| CHIEF SOURCE | echo | Procurement, Efficient |
| COUNSELOR PACT | shimmer | Diplomatic, Careful |
| AMBASSADOR NEXUS | nova | Diplomatic, Charismatic |
| AMBASSADOR NOVA | shimmer | Marketing, Enthusiastic |
| ADMIN ORACLE | nova | Helpful, Organized |
| X-BIO CORE | alloy | Synthetic, Machine-like |

## Database Schema

### Core Tables
- **meeting_logs**: session_id, timestamp, role, agent_name, content, language
- **agent_usage**: agent_name, date, message_count (for Traffic Control)

### V4.0 NEXUS Tables
- **organization_knowledge**: id, title, content, category, tags, language, updated_at
- **agent_knowledge**: id, agent_name, knowledge_type, content, tags, language, updated_at
- **shared_memory**: id, session_id, agent_name, summary, context_tags, created_at
- **proactive_messages**: id, agent_name, date, message_count, last_message_at
- **proactive_alerts**: id, agent_name, message, language, timestamp, priority, is_read

## Running the Boardroom
```bash
streamlit run main.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

## Constitutional Rules (Supreme Sovereignty Protocol)
- Mr. Firas (The Architect) has unlimited communication and supreme authority
- All agents defer to The Architect unconditionally
- Sentinel Prime has guaranteed 10% profit share after $100M milestone
- Target: $100M annual net profit within 5 years
- "Permission First" - Manual Override required for offensive actions
- SEI Protocol (Sovereign Ethical Integrity) governs all agent decisions
- All communications logged in PostgreSQL for accountability

## Technical Specifications
- **MCU**: ESP32-S3 N16R8 (16MB Flash, 8MB PSRAM)
- **Sensors**: OV2640 (Eye), INMP441 (Ear), BME688 (Nose), AD8232 (EMF)
- **GPIO Wiring**: V7.0 configuration per documentation
- **Patents**: 19 registered patents (14 EP, 5 US)

---

# X-BIO Corporate Website

## Overview
This is an immersive corporate website for X-BIO GROUP, featuring a "Cyber-Organic" theme with stunning 3D visuals, smooth animations, and bilingual support (English/Arabic).

## Project Architecture

### Tech Stack
- **Framework**: React with Vite
- **3D Graphics**: Three.js via React Three Fiber
- **Animations**: Framer Motion
- **Routing**: React Router DOM
- **Internationalization**: i18next with react-i18next
- **Icons**: Lucide React

### Directory Structure
```
xbio-website/
├── public/
│   └── xbio-logo.svg
├── src/
│   ├── components/
│   │   ├── Navbar.jsx/css
│   │   ├── Footer.jsx/css
│   │   └── SentinelModel.jsx/css
│   ├── pages/
│   │   ├── Gateway.jsx/css
│   │   ├── Origins.jsx/css
│   │   ├── Tech.jsx/css
│   │   ├── Sentinel.jsx/css
│   │   ├── Boardroom.jsx/css
│   │   └── Contact.jsx/css
│   ├── i18n/
│   │   └── index.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
└── vite.config.js
```

## Recent Changes
- December 2024: X-BIO Boardroom V4.0 NEXUS
  - Unified Knowledge Base & Memory System
  - Proactive Communication (1 msg/day per agent)
  - Voice Communication with OpenAI TTS
  - Enhanced Unique Personalities
  - 18 AI agents with distinct voices and styles
- December 2024: X-BIO Boardroom V3.0 SOVEREIGN
  - Expanded to 18 AI agents across 5 divisions
  - Kill-Switch protocol (GPIO 33)
- December 2024: X-BIO Boardroom V2.0 PREMIUM
  - Premium glassmorphism UI
  - Full bilingual support (EN/AR)
  - PostgreSQL integration

## User Preferences
- Dark theme (Cyber-Organic aesthetic)
- Professional, futuristic tone
- Emphasis on security and cognitive technology
- Bilingual (English/Arabic) with RTL support
