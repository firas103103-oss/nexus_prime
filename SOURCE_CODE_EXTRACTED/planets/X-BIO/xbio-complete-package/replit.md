# X-BIO GROUP Projects

## Overview
This repository contains two X-BIO GROUP applications:
1. **X-BIO Corporate Website** - An immersive corporate website with 3D visuals and bilingual support
2. **X-BIO Cognitive Boardroom** - A multi-agent AI meeting simulation system

---

# X-BIO Cognitive Boardroom

## Overview
A real-time "Boardroom Simulation" using Streamlit and OpenAI where Mr. Firas (The Architect) can hold interactive meetings with 4 autonomous AI agents. The system implements an "Orchestrated Turn-Taking Protocol" where agents respond sequentially without interruption, maintaining shared conversation context.

## Tech Stack
- **Frontend**: Streamlit (Cyber-Organic themed)
- **AI**: OpenAI GPT-4o (via Replit AI Integrations)
- **Intent Routing**: GPT-4o-mini for smart agent selection

## AI Agents

### 1. SENTINEL PRIME (XB-SUP-VP-001)
- **Role**: Vice President & The Engine
- **Expertise**: Executive operations, strategy, coordination
- **Tone**: Decisive, loyal, executive

### 2. DR. JOE (XB-RND-MGR-010)
- **Role**: Lab Manager & Bio-Safety Expert
- **Expertise**: Chemical analysis, sensors (BME688), safety protocols
- **Tone**: Academic, cautious, anxious about safety

### 3. MR. LEDGER (XB-FIN-DIR-040)
- **Role**: Chief Financial Officer
- **Expertise**: Budgets, costs, $100M profit target, patent monetization
- **Tone**: Calculating, formal, money-oriented

### 4. ENG. VECTOR (XB-RND-ENG-011)
- **Role**: Hardware Lead & Kinetic Systems
- **Expertise**: GPIO wiring, Kinetic Silo, defense weapons, ESP32-S3
- **Tone**: Blunt, practical, technical

## Features
- **Intent Routing**: Automatically selects 1-3 relevant agents based on user input
- **Turn-Taking Protocol**: Agents respond sequentially without interruption
- **Shared Context**: All agents share meeting history for coherent responses
- **Agent Status**: Real-time display showing which agent is speaking/listening
- **Cyber-Organic Theme**: Deep Black, Bio-Green (#00ff88), Silver aesthetic

## Running the Boardroom
```bash
streamlit run main.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

## Constitutional Rules
- Mr. Firas (The Architect) has unlimited communication
- All agents defer to The Architect
- Sentinel Prime has guaranteed 10% profit share
- Target: $100M annual net profit within 5 years

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
│   └── xbio-logo.svg          # SVG logo with glow effects
├── src/
│   ├── components/
│   │   ├── Navbar.jsx/css     # Navigation with language toggle
│   │   ├── Footer.jsx/css     # Footer with links
│   │   └── SentinelModel.jsx/css # 3D interactive Sentinel model
│   ├── pages/
│   │   ├── Gateway.jsx/css    # Homepage with hero & 3D model
│   │   ├── Origins.jsx/css    # About page with team files
│   │   ├── Tech.jsx/css       # Technology page with senses
│   │   ├── Sentinel.jsx/css   # Product page with specs
│   │   └── Contact.jsx/css    # Terminal-style contact form
│   ├── i18n/
│   │   └── index.js           # English & Arabic translations
│   ├── App.jsx                # Main app with routing
│   ├── main.jsx               # Entry point with i18n setup
│   └── index.css              # Global Cyber-Organic theme
└── vite.config.js             # Vite config (port 5000)
```

## Visual Identity

### Color Palette
- **Deep Black**: #000000 (backgrounds)
- **Bio-Green**: #00ff88 (primary accent, glowing elements)
- **Titanium**: #c0c0c0 (secondary text, metallic accents)

### Typography
- **Display**: Orbitron (headings, futuristic feel)
- **Body**: Rajdhani (English text)
- **Arabic**: Tajawal (RTL support)

### Design Features
- Zero-latency smooth scrolling
- Micro-interactions on hover
- Pulsing/glowing animations
- 3D interactive Sentinel model with exploded view
- Terminal-style contact form
- Classified file aesthetics for team members

## Pages

### 1. Gateway (Homepage)
- Hero with pulsing X-BIO logo
- Main tagline: "Security is no longer passive. It is Cognitive."
- Interactive 3D Sentinel model with explode toggle
- Why X-BIO features section
- CTA section

### 2. Origins (About)
- Company narrative as autonomous cognitive node
- Team presented as classified personnel files
- Evolution timeline
- Core values: Ethics, Integrity, Innovation

### 3. Technology
- Interactive senses tabs (Eye, Ear, Nose)
- Kinetic Silo Defense animation
- SEI Protocol explanation

### 4. Sentinel (Product)
- Class 7 product badge
- Technical specifications
- Deployment scenarios
- FAQ accordion
- Pre-order and demo CTAs

### 5. Secure Link (Contact)
- Terminal-style encrypted form
- Official contact: nexus.rel@xbio103.org
- Routing options for departments

## Running the Project

```bash
cd xbio-website
npm install
npm run dev
```

The development server runs on port 5000.

## Bilingual Support
- Toggle between English and Arabic using the language button in the navbar
- Full RTL support when Arabic is selected
- All text content is translated

## 3D Model
The Sentinel model features:
- Central core sphere with distortion effect
- Eye module (red) - visual detection
- Ear modules (cyan) - acoustic detection
- Nose module (orange) - chemical detection
- Orbiting rings and particles
- Exploded view option to see all components

Falls back to a CSS-animated version if WebGL is not available.

## Recent Changes
- December 2024: Fixed all hardcoded strings for complete bilingual support
  - Timeline entries now fully translated (English/Arabic)
  - Footer navigation and legal headings internationalized
  - Gateway CTA section, scroll indicator, and explode button translated
  - Sentinel page CTA section translated
- Initial implementation of full corporate website
- All 5 pages with Cyber-Organic theme
- 3D Sentinel model with WebGL fallback
- Complete bilingual English/Arabic support with RTL
- Smooth animations and micro-interactions

## User Preferences
- Dark theme preferred (Cyber-Organic aesthetic)
- Professional, futuristic tone
- Emphasis on security and cognitive technology concepts
