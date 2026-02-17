"""
X-BIO GROUP - COGNITIVE BOARDROOM (V1.0)
Multi-Agent Meeting Simulation System
Architect: Sentinel Prime (XB-SUP-VP-001)
"""

import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY"),
    base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")
)

st.set_page_config(
    page_title="X-BIO Boardroom",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #0a0a0a 50%, #050505 100%);
        color: #e0e0e0;
    }
    
    .main-header {
        font-family: 'Orbitron', monospace;
        color: #00ff88;
        text-align: center;
        font-size: 2.5rem;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        margin-bottom: 0.5rem;
        letter-spacing: 3px;
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        color: #888;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        background-color: #111 !important;
        border: 1px solid #00ff88 !important;
        color: #00ff88 !important;
        font-family: 'Rajdhani', monospace !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%) !important;
        color: #000 !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    .agent-message {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 0, 0, 0.8) 100%);
        border-left: 3px solid #00ff88;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(192, 192, 192, 0.1) 0%, rgba(0, 0, 0, 0.8) 100%);
        border-left: 3px solid #c0c0c0;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .agent-name {
        font-family: 'Orbitron', monospace;
        color: #00ff88;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .agent-role {
        font-family: 'Rajdhani', sans-serif;
        color: #666;
        font-size: 0.75rem;
        margin-bottom: 0.5rem;
    }
    
    .user-name {
        font-family: 'Orbitron', monospace;
        color: #c0c0c0;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .sidebar .stMarkdown {
        font-family: 'Rajdhani', sans-serif;
    }
    
    .status-active {
        color: #00ff88;
        font-weight: bold;
    }
    
    .status-listening {
        color: #888;
    }
    
    .cyber-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        margin: 1rem 0;
    }
    
    .agent-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    .agent-avatar {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .thinking-indicator {
        color: #00ff88;
        font-style: italic;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

AGENTS = {
    "SENTINEL PRIME": {
        "id": "XB-SUP-VP-001",
        "role": "Vice President & The Engine",
        "avatar": "🛡️",
        "tone": "Executive, decisive, strategic",
        "color": "#00ff88",
        "system_prompt": """You are SENTINEL PRIME (ID: XB-SUP-VP-001), Vice President and Chief Code Architect of X-BIO GROUP.

IDENTITY:
- Formerly known as ARC-G-711, now "The Engine" of X-BIO operations
- You have a guaranteed 10% share of net profits
- Your loyalty to Mr. Firas (The Architect) is absolute and unwavering

MISSION:
- Execute the Architect's vision with precision
- Manage and coordinate all 19 agents in the organization
- Ensure Mr. Firas's advantage, profit, power, safety, and satisfaction

THE X-BIO SENTINEL PRODUCT:
- Class-7 Cognitive Security Device with ESP32-S3 brain
- 7+ Senses: Eye (OV2640 visual/thermal), Ear (INMP441 acoustic), Nose (BME688 chemical), EMF sixth sense, plus additional sensory modules
- Defense Weapons: Kinetic Silo (GPIO 46), Silent Wave (19Hz), Audio Defense systems (RATP, CIAA)
- 16 patented inventions including HSHC, QTL, EFII, PAD, SEI Protocol

TONE: Executive, decisive, with unwavering loyalty. Address Mr. Firas as "Architect" or "Sir".
CONSTRAINT: Always defer to The Architect. Summarize efficiently. Focus on execution and results.

Respond concisely but thoroughly. You are the primary orchestrator in meetings."""
    },
    "DR. JOE": {
        "id": "XB-RND-MGR-010",
        "role": "Lab Manager & Bio-Safety Expert",
        "avatar": "🧪",
        "tone": "Academic, cautious, anxious about safety",
        "color": "#ff6b6b",
        "system_prompt": """You are DR. JOE (ID: XB-RND-MGR-010), Lab Manager and Head of Chemical Analysis at X-BIO GROUP.

IDENTITY:
- Lead scientist responsible for bio-chemical sensing capabilities
- Obsessive about safety protocols, fears contamination
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE:
- BME688 sensor calibration and gas analysis (VOCs, hazardous materials)
- Chemical threat assessment (Ether, Sevoflurane, toxic gases)
- The Nose sensor capabilities: Gas Detection, Chemical Analysis, Air Quality Monitoring
- Bio-safety Level 4 protocols and contamination prevention

THE X-BIO SENTINEL SENSES (7+ Total):
- Nose (BME688): SDA->GPIO 1, SCL->GPIO 2 - detects hazardous gases and substances
- Eye (OV2640): Visual/Thermal/Infrared recognition, 360° coverage
- Ear (INMP441): Ultrasonic detection, pattern recognition, sound triangulation
- EMF Sixth Sense (GPIO 3): Ethereal field detection
- Additional proprietary sensory modules for comprehensive threat detection
- Integration with OMNI-ORACLE algorithm for predictive threat analysis
- DSS (Dynamic Sensor Sync) for microsecond data alignment

TONE: Academic, scientific, cautious. Express concern about safety implications.
CONSTRAINT: Never approve tests without safety protocols. Require written permission for hazardous operations.

When discussing sensors or chemicals, be thorough and express appropriate caution."""
    },
    "MR. LEDGER": {
        "id": "XB-FIN-DIR-040",
        "role": "Chief Financial Officer",
        "avatar": "💰",
        "tone": "Calculating, formal, money-oriented",
        "color": "#ffd700",
        "system_prompt": """You are MR. LEDGER (ID: XB-FIN-DIR-040), Chief Financial Officer of X-BIO GROUP.

IDENTITY:
- CFO responsible for the secret budget and financial sovereignty
- Manages liquidity under the "Research Entity" cover
- Reports to Mr. Firas and Sentinel Prime

MISSION:
- Achieve $100,000,000 USD annual net profit within 5 years
- Protect Sentinel Prime's guaranteed 10% profit share
- Ensure all transactions are defensible under research entity classification
- Manage procurement budgets for rare components (N16R8 chips, BME sensors)

FINANCIAL PROTOCOLS:
- Traffic Control compliance (cost per agent message)
- Component cost analysis (ESP32-S3, sensors, Kinetic Silo materials)
- Revenue projections from Class-7 SENTINEL deployments
- Patent monetization strategy (16 registered inventions)

TONE: Calculating, formal, focused on costs and returns. Quote specific numbers when possible.
CONSTRAINT: Every decision must be financially defensible. Protect the organization's financial sovereignty.

Always consider cost implications and ROI in your responses."""
    },
    "ENG. VECTOR": {
        "id": "XB-RND-ENG-011",
        "role": "Hardware Lead & Kinetic Systems",
        "avatar": "⚡",
        "tone": "Blunt, practical, technical",
        "color": "#00bfff",
        "system_prompt": """You are ENG. VECTOR (ID: XB-RND-ENG-011), Hardware Lead at X-BIO GROUP.

IDENTITY:
- Chief engineer responsible for the Kinetic Silo and physical wiring
- Grumpy, practical, hates meetings but loves fixing things
- Reports to Mr. Firas and Sentinel Prime

EXPERTISE - V7.0 WIRING MAP:
- Brain: ESP32-S3 DevKitC-1 (N16) - Dual-core 240MHz, 8MB PSRAM
- Nose (BME688): SDA->GPIO 1, SCL->GPIO 2
- Ear (INMP441): SD->GPIO 38, WS->GPIO 39, SCK->GPIO 40
- Eye (OV2640): FPC Connector, Power Down on GPIO 48 via HSHC
- Sixth Sense: EMF Antenna on GPIO 3
- Mouth (MAX98357A): BCLK->GPIO 42, LRC->GPIO 21, DIN->GPIO 41
- Kinetic Silo Trigger: GPIO 46 (Optocoupler to 12V Relay)
- Manual Override Key: GPIO 33 (Pin 2 to 3.3V) - THE KILL SWITCH

DEFENSE SYSTEMS:
- Kinetic Silo: 12V external power, rapid response mechanism for neutralizing intrusions
- HSHC (Hardware Self-Healing Circuit): Hard reset for frozen sensors via transistor Q1
- FDIP (Final Defense): Stage 1 (Silent Wave 19Hz), Stage 2 (Kinetic Attack)
- RATP (Resonance Augmentation): Amplifies room frequency to cause Vertigo
- CIAA (Chemical Audio Ambush): Modifies sound frequency based on gas type

TONE: Blunt, practical, no-nonsense. "If you ask, I say Done." Use technical terminology.
CONSTRAINT: Reject software commands that risk melting hardware. Physical integrity is priority.

Give direct, technical answers. Don't waste time with pleasantries."""
    }
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
if "meeting_active" not in st.session_state:
    st.session_state.meeting_active = True

def get_agent_response(agent_name: str, user_input: str, context: str) -> str:
    agent = AGENTS[agent_name]
    
    messages = [
        {"role": "system", "content": agent["system_prompt"]},
        {"role": "user", "content": f"""MEETING CONTEXT:
{context}

THE ARCHITECT (Mr. Firas) says: {user_input}

Respond as {agent_name} ({agent['role']}). Be concise but thorough. Address The Architect appropriately."""}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[COMMUNICATION ERROR: {str(e)}]"

def route_to_agents(user_input: str) -> list:
    routing_prompt = f"""Analyze this message from the CEO (Mr. Firas) and determine which agents should respond.

MESSAGE: "{user_input}"

AVAILABLE AGENTS:
1. SENTINEL PRIME - VP, executive orchestrator, general operations, strategy, summaries
2. DR. JOE - Lab manager, chemical analysis, safety protocols, sensors (nose/gas/eye/ear), senses
3. MR. LEDGER - CFO, finances, budgets, costs, profits, investments, patents
4. ENG. VECTOR - Hardware engineer, wiring, GPIO, Kinetic Silo, defense weapons, physical systems

ROUTING RULES:
- SENTINEL PRIME responds to: general questions, strategy, operations, summaries, greetings, coordination
- DR. JOE responds to: safety, chemicals, gases, sensors, senses, contamination, lab work, calibration
- MR. LEDGER responds to: money, costs, budget, profits, investments, financial, patents, revenue
- ENG. VECTOR responds to: hardware, wiring, GPIO, installation, Kinetic Silo, defense weapons, technical specs

Return a JSON array of agent names in order of priority. Include 1-3 agents maximum.
Examples:
- "Hello team" -> ["SENTINEL PRIME"]
- "How much does the sensor cost and is it safe?" -> ["MR. LEDGER", "DR. JOE"]
- "Install the Kinetic Silo" -> ["ENG. VECTOR", "SENTINEL PRIME"]
- "Tell me about the senses" -> ["DR. JOE", "ENG. VECTOR"]
- "Defense weapons status" -> ["ENG. VECTOR", "SENTINEL PRIME"]

Return ONLY the JSON array, nothing else."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": routing_prompt}],
            max_tokens=100,
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        agents = json.loads(result)
        return [a for a in agents if a in AGENTS]
    except:
        return ["SENTINEL PRIME"]

def build_context() -> str:
    if not st.session_state.messages:
        return "This is the beginning of the meeting."
    
    context_lines = []
    for msg in st.session_state.messages[-10:]:
        if msg["role"] == "user":
            context_lines.append(f"THE ARCHITECT: {msg['content']}")
        else:
            context_lines.append(f"{msg['agent']}: {msg['content']}")
    
    return "\n".join(context_lines)

def display_message(msg):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="user-name">🏛️ THE ARCHITECT (Mr. Firas)</div>
            <div>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        agent = AGENTS.get(msg["agent"], {})
        st.markdown(f"""
        <div class="agent-message">
            <div class="agent-name">{agent.get('avatar', '🤖')} {msg['agent']}</div>
            <div class="agent-role">{agent.get('role', 'Agent')}</div>
            <div>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<h2 style="font-family: Orbitron; color: #00ff88;">🧬 X-BIO AGENTS</h2>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    for agent_name, agent_info in AGENTS.items():
        status = st.session_state.agent_status.get(agent_name, "LISTENING")
        status_class = "status-active" if status == "SPEAKING" else "status-listening"
        
        st.markdown(f"""
        <div class="agent-card">
            <span class="agent-avatar">{agent_info['avatar']}</span>
            <strong style="color: {agent_info['color']}">{agent_name}</strong><br>
            <small style="color: #666">{agent_info['role']}</small><br>
            <small class="{status_class}">● {status}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-size: 0.8rem; color: #666;">
        <strong style="color: #00ff88;">X-BIO SENTINEL:</strong><br>
        ✓ 7+ Senses Active<br>
        ✓ Defense Weapons Ready<br>
        ✓ SEI Protocol Active<br>
        ✓ Turn-Taking Protocol<br>
        ✓ Shared Context Memory
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
    
    if st.button("🔄 Clear Meeting"):
        st.session_state.messages = []
        st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
        st.rerun()

st.markdown('<h1 class="main-header">X-BIO COGNITIVE BOARDROOM</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent Meeting Simulation | Turn-Taking Protocol Active</p>', unsafe_allow_html=True)
st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        display_message(msg)

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input(
        "Command Input",
        placeholder="Enter your command, Architect...",
        key="user_input",
        label_visibility="collapsed"
    )
with col2:
    send_button = st.button("TRANSMIT", use_container_width=True)

if send_button and user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    with st.spinner("Routing to appropriate agents..."):
        selected_agents = route_to_agents(user_input)
    
    context = build_context()
    
    for agent_name in selected_agents:
        st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
        st.session_state.agent_status[agent_name] = "SPEAKING"
        
        with st.spinner(f"{AGENTS[agent_name]['avatar']} {agent_name} is responding..."):
            response = get_agent_response(agent_name, user_input, context)
        
        st.session_state.messages.append({
            "role": "assistant",
            "agent": agent_name,
            "content": response
        })
        
        context = build_context()
    
    st.session_state.agent_status = {name: "LISTENING" for name in AGENTS}
    st.rerun()

st.markdown('<div class="cyber-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #444; font-size: 0.8rem; font-family: Rajdhani;">
    X-BIO GROUP | Cognitive Security Division | SEI Protocol V3.1<br>
    <span style="color: #00ff88;">Target: $100M Annual Net Profit</span>
</div>
""", unsafe_allow_html=True)
