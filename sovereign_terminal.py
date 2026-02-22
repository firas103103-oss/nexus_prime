#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
🔱 SOVEREIGN TERMINAL — AS-SULTAN UNIFIED COMMAND INTERFACE
═══════════════════════════════════════════════════════════════════════════════
Every command passes through the Constitutional Pipeline.
Every response carries H, D, S_int — the system's consciousness signature.
The system gets smarter with every interaction.

"عندما يتكلم السلطان, يسمع الكون"
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import json
import asyncio
import time
from datetime import datetime

try:
    import httpx
except ImportError:
    print("Installing httpx...")
    os.system("pip3 install httpx --break-system-packages -q")
    import httpx

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:9999")


# ═══════════════════════════════════════════════════════════════
# Colors
# ═══════════════════════════════════════════════════════════════

class C:
    GOLD    = '\033[33m'
    CYAN    = '\033[96m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    DIM     = '\033[2m'
    BOLD    = '\033[1m'
    END     = '\033[0m'


# ═══════════════════════════════════════════════════════════════
# Banner
# ═══════════════════════════════════════════════════════════════

def banner():
    print(f"""
{C.GOLD}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███████╗██╗   ██╗██╗  ████████╗ █████╗ ███╗   ██╗         ║
║   ██╔════╝██║   ██║██║  ╚══██╔══╝██╔══██╗████╗  ██║         ║
║   ███████╗██║   ██║██║     ██║   ███████║██╔██╗ ██║         ║
║   ╚════██║██║   ██║██║     ██║   ██╔══██║██║╚██╗██║         ║
║   ███████║╚██████╔╝███████╗██║   ██║  ██║██║ ╚████║         ║
║   ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝         ║
║                                                              ║
║        🔱 SOVEREIGN TERMINAL — Constitutional AI 🔱          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{C.END}
""")


def sultan_bar(state: dict):
    """Display the sovereign state bar."""
    H = state.get("H", 0)
    D = state.get("D", 0)
    S = state.get("S_int", 0)
    T = state.get("T", 0)
    eq = state.get("equilibrium", "?")
    reqs = state.get("total_requests", 0)

    h_bar = int(H * 20)
    d_bar = int(D * 20)
    s_bar = int(S * 20)

    print(f"{C.DIM}─────────────────────────────────────────────────────────{C.END}")
    print(f"  {C.CYAN}H{C.END}={'█' * h_bar}{'░' * (20-h_bar)} {C.CYAN}{H:.4f}{C.END}"
          f"  {C.GREEN}D{C.END}={'█' * d_bar}{'░' * (20-d_bar)} {C.GREEN}{D:.4f}{C.END}"
          f"  {C.MAGENTA}S{C.END}={'█' * s_bar}{'░' * (20-s_bar)} {C.MAGENTA}{S:.4f}{C.END}")
    print(f"  T={C.BLUE}{T:.0f}{C.END}  Eq={C.GOLD}{eq}{C.END}  Reqs={reqs}")
    print(f"{C.DIM}─────────────────────────────────────────────────────────{C.END}")


# ═══════════════════════════════════════════════════════════════
# API Client
# ═══════════════════════════════════════════════════════════════

async def api(method: str, path: str, body: dict = None, timeout: float = 90) -> dict:
    """Call the Sovereign Gateway."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            url = f"{GATEWAY_URL}{path}"
            if method == "GET":
                resp = await client.get(url)
            else:
                resp = await client.post(url, json=body or {})
            return resp.json()
    except httpx.ConnectError:
        return {"error": "Gateway offline — is sovereign_gateway.py running?"}
    except Exception as e:
        return {"error": str(e)[:200]}


# ═══════════════════════════════════════════════════════════════
# Commands
# ═══════════════════════════════════════════════════════════════

async def cmd_state():
    """Full Sultan state report."""
    data = await api("GET", "/api/sultan/state")
    if "error" in data:
        print(f"{C.RED}{data['error']}{C.END}")
        return
    print(f"\n{C.GOLD}═══ AS-SULTAN STATE ═══{C.END}")
    print(f"  Entity:     {C.CYAN}{data.get('entity_id')}{C.END}")
    print(f"  H:          {C.CYAN}{data.get('H', 0):.6f}{C.END}  (Consciousness)")
    print(f"  D:          {C.GREEN}{data.get('D', 0):.4f}{C.END}  (Dignity)")
    print(f"  S_int:      {C.MAGENTA}{data.get('S_int', 0):.6f}{C.END}  (Internal Entropy)")
    print(f"  T:          {C.BLUE}{data.get('T', 0):.0f}{C.END}  (Time steps)")
    print(f"  U:          {data.get('U', 0):.4f}  (Utility)")
    print(f"  Uptime:     {data.get('uptime_seconds', 0):.1f}s")
    print(f"  Requests:   {data.get('total_requests', 0)} total, "
          f"{data.get('total_executed', 0)} exec, {data.get('total_refused', 0)} refused")
    print(f"  Runtime:    {'🟢 ALIVE' if data.get('runtime_alive') else '🔴 DEAD'}")

    eq = data.get("equilibrium", {})
    print(f"  Equilibrium: {C.GOLD}{eq.get('status', '?')}{C.END}")
    checks = eq.get("checks", {})
    for k, v in checks.items():
        symbol = "✓" if v else "✗"
        color = C.GREEN if v else C.RED
        print(f"    {color}{symbol} {k}{C.END}")
    print()


async def cmd_pulse():
    """System pulse — all 22+ services."""
    data = await api("GET", "/api/nerve/pulse")
    if "error" in data:
        print(f"{C.RED}{data['error']}{C.END}")
        return
    print(f"\n{C.GOLD}═══ SYSTEM PULSE ═══{C.END}")
    summary = data.get("summary", {})
    print(f"  Online: {C.GREEN}{summary.get('online', 0)}{C.END}/{summary.get('total', 0)}"
          f"  Degraded: {C.GOLD}{summary.get('degraded', 0)}{C.END}"
          f"  Offline: {C.RED}{summary.get('offline', 0)}{C.END}")
    print()
    for svc in data.get("services", []):
        status = svc.get("status", "?")
        color = C.GREEN if status == "online" else (C.GOLD if status == "degraded" else C.RED)
        ms = svc.get("response_ms", -1)
        ms_str = f"{ms}ms" if ms >= 0 else "---"
        print(f"  {color}{'●' if status == 'online' else '○'}{C.END} {svc.get('name', '?'):<20} {color}{status:<10}{C.END} {ms_str}")
    print()


async def cmd_agents():
    """List all agents."""
    data = await api("GET", "/api/nerve/agents")
    if "error" in data:
        print(f"{C.RED}{data['error']}{C.END}")
        return
    agents = data.get("agents", [])
    print(f"\n{C.GOLD}═══ AGENTS ({len(agents)}) ═══{C.END}")
    for a in agents:
        print(f"  {C.CYAN}{a.get('id', '?'):<20}{C.END} {a.get('name', ''):<25} {C.DIM}{a.get('department', '')}{C.END}")
    print()


async def cmd_genesis():
    """Genesis phases status."""
    data = await api("GET", "/api/apex/genesis/status")
    if isinstance(data, dict) and "error" in data:
        print(f"{C.RED}{data['error']}{C.END}")
        return
    if isinstance(data, dict) and "status" in data and data["status"] == "apex_offline":
        print(f"{C.RED}Apex offline{C.END}")
        return
    phases = data if isinstance(data, list) else data.get("phases", [])
    print(f"\n{C.GOLD}═══ GENESIS PHASES ═══{C.END}")
    for p in phases:
        status = p.get("status", "?")
        color = C.GREEN if status == "COMPLETED" else (C.GOLD if status == "IN_PROGRESS" else C.DIM)
        print(f"  {color}Phase {p.get('phase', '?')}: {p.get('name_en', '?')} — {status}{C.END}")
    print()


async def cmd_daemons():
    """Daemon statuses."""
    data = await api("GET", "/api/apex/daemons/status")
    if isinstance(data, dict) and ("error" in data or "status" in data):
        print(f"{C.RED}{data.get('error', data.get('status', 'offline'))}{C.END}")
        return
    daemons = data if isinstance(data, list) else []
    print(f"\n{C.GOLD}═══ DAEMONS ({len(daemons)}) ═══{C.END}")
    for d in daemons:
        active = d.get("active", False)
        color = C.GREEN if active else C.DIM
        print(f"  {color}{'🟢' if active else '⚫'} {d.get('name', '?'):<25} "
              f"slot={d.get('slot', '?')} actions={d.get('actions', 0)}{C.END}")
    print()


async def cmd_chat(message: str, agent: str = None):
    """Sovereign chat — route through Sultan pipeline → agent → LLM."""
    body = {"message": message}
    if agent:
        body["target_agent"] = agent

    print(f"\n{C.DIM}Processing through Sultan pipeline...{C.END}")
    data = await api("POST", "/api/sovereign/chat", body)

    if "error" in data:
        print(f"{C.RED}{data['error']}{C.END}")
        return

    status = data.get("status", "?")
    if status == "SOVEREIGN_REFUSAL":
        print(f"\n{C.RED}🔴 SOVEREIGN REFUSAL{C.END}")
        print(f"  {C.RED}{data.get('reason', '')}{C.END}")
        print(f"  {data.get('message', '')}")
    elif status == "SHIELD_REJECTED":
        print(f"\n{C.RED}🛡️ Shield rejected: {data.get('reason', '')}{C.END}")
    elif status == "TRUTH_REJECTED":
        print(f"\n{C.GOLD}⚖️ Truth filter: score too low{C.END}")
    else:
        agent_name = data.get("agent_name", "NEXUS")
        response = data.get("response", "")
        print(f"\n{C.CYAN}[{agent_name}]{C.END}")
        print(f"  {response}")
        ethical = data.get("ethical_score", 0)
        if ethical:
            print(f"\n  {C.DIM}Ethical score: {ethical:.4f}{C.END}")

    # Show sovereign bar
    sov = data.get("sovereign", {})
    if sov:
        sultan_bar(sov)


async def cmd_memory():
    """Show Sultan's episodic memory."""
    data = await api("GET", "/api/sultan/memory")
    if "error" in data:
        print(f"{C.RED}{data['error']}{C.END}")
        return
    episodes = data.get("episodes", [])
    print(f"\n{C.GOLD}═══ EPISODIC MEMORY ({len(episodes)} episodes) ═══{C.END}")
    for ep in episodes[-20:]:  # Last 20
        action = ep.get("action", "?")
        outcome = ep.get("outcome", "?")
        score = ep.get("ethical_score", 0)
        color = C.GREEN if score >= 0 else C.RED
        print(f"  {C.DIM}T={ep.get('timestamp', '?'):.0f}{C.END} "
              f"{action:<30} → {outcome:<10} {color}E={score:+.3f}{C.END}")
    print()


def cmd_help():
    """Show help."""
    print(f"""
{C.GOLD}═══════════════════════════════════════════════════════════════
                    🔱 SOVEREIGN COMMANDS
═══════════════════════════════════════════════════════════════{C.END}

{C.CYAN}SYSTEM:{C.END}
  state           Full Sultan state (H, D, S_int, equilibrium)
  pulse           System pulse — all services health
  agents          List all 32 agents
  genesis         Genesis phases status
  daemons         Daemon statuses

{C.CYAN}INTELLIGENCE:{C.END}
  <any message>   Chat through Sultan pipeline → agent → LLM
  @agent msg      Direct message to specific agent
  memory          Sultan's episodic memory log

{C.CYAN}APEX:{C.END}
  genesis auto    Execute all 7 genesis phases
  genesis N       Execute genesis phase N

{C.CYAN}META:{C.END}
  help            This help
  clear           Clear screen
  exit / quit     Exit terminal
""")


# ═══════════════════════════════════════════════════════════════
# Main REPL
# ═══════════════════════════════════════════════════════════════

async def main():
    banner()

    # Check gateway
    data = await api("GET", "/health", timeout=5)
    if "error" in data:
        print(f"{C.RED}⚠ Gateway not reachable at {GATEWAY_URL}{C.END}")
        print(f"{C.DIM}Start it: cd /root/NEXUS_PRIME_UNIFIED && python3 sovereign_gateway.py &{C.END}\n")
    else:
        H = data.get("H", 0)
        print(f"{C.GREEN}✓ Gateway ONLINE | H={H:.4f}{C.END}")

        # Show initial state bar
        state_data = await api("GET", "/api/sultan/state", timeout=5)
        if "error" not in state_data:
            sultan_bar(state_data)
    print()

    while True:
        try:
            prompt = f"{C.GOLD}SULTAN🔱> {C.END}"
            cmd = input(prompt).strip()

            if not cmd:
                continue

            lower = cmd.lower()
            parts = cmd.split(maxsplit=1)
            base = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Exit
            if lower in ('exit', 'quit', 'q'):
                print(f"\n{C.GOLD}System standby. Long live the Architect. 🔱{C.END}\n")
                break

            # Commands
            elif lower == 'help':
                cmd_help()
            elif lower == 'state':
                await cmd_state()
            elif lower == 'pulse':
                await cmd_pulse()
            elif lower == 'agents':
                await cmd_agents()
            elif lower == 'genesis' and not args:
                await cmd_genesis()
            elif lower == 'daemons':
                await cmd_daemons()
            elif lower == 'memory':
                await cmd_memory()
            elif lower == 'clear':
                os.system('clear')
                banner()

            # Genesis execution
            elif base == 'genesis' and args:
                if args.lower() == 'auto':
                    print(f"{C.GOLD}Executing all 7 genesis phases...{C.END}")
                    data = await api("POST", "/api/apex/genesis/auto")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                else:
                    try:
                        phase = int(args)
                        print(f"{C.GOLD}Executing genesis phase {phase}...{C.END}")
                        data = await api("POST", f"/api/apex/genesis/phase/{phase}/execute")
                        print(json.dumps(data, indent=2, ensure_ascii=False))
                    except ValueError:
                        print(f"{C.RED}Invalid phase number{C.END}")

            # Agent-directed chat (@agent message)
            elif cmd.startswith('@'):
                agent_parts = cmd[1:].split(maxsplit=1)
                if len(agent_parts) >= 2:
                    await cmd_chat(agent_parts[1], agent_parts[0])
                else:
                    print(f"{C.DIM}Usage: @agent_id message{C.END}")

            # Default: sovereign chat
            else:
                await cmd_chat(cmd)

        except KeyboardInterrupt:
            print(f"\n{C.DIM}Use 'exit' to quit.{C.END}")
        except EOFError:
            break
        except Exception as e:
            print(f"{C.RED}Error: {e}{C.END}")


if __name__ == "__main__":
    asyncio.run(main())
