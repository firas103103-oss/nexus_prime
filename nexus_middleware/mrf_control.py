#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
🔱 MR. F SOVEREIGN TERMINAL - GOD MODE INTERFACE
═══════════════════════════════════════════════════════════════════════════════
"When the Architect speaks, the Empire listens"

محطة التحكم العليا - السيطرة الكاملة على إمبراطورية NEXUS
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add middleware to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_middleware.connector import NexusMasterConnector, get_connector
from nexus_middleware.hive_mind import sync_collective_consciousness, HiveMindOracle


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL COLORS & FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    GOLD = '\033[33m'


def banner():
    """Display sovereign terminal banner"""
    print(f"""
{Colors.GOLD}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗    ██████╗ ██████╗ ██╗███╗   ███╗║
║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔══██╗██╔══██╗██║████╗ ████║║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ██████╔╝██████╔╝██║██╔████╔██║║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██╔═══╝ ██╔══██╗██║██║╚██╔╝██║║
║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ██║     ██║  ██║██║██║ ╚═╝ ██║║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝║
║                                                                              ║
║             🔱 S O V E R E I G N   T E R M I N A L — GOD MODE 🔱             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.END}
""")
    print(f"{Colors.CYAN}Welcome back, Mr. F — The Architect{Colors.END}")
    print(f"{Colors.GREEN}System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.BLUE}Type 'help' for commands. Type 'exit' to leave.{Colors.END}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

class SovereignCommands:
    """All sovereign commands handler"""
    
    def __init__(self):
        self.connector = get_connector()
        self.oracle = HiveMindOracle()
    
    def help(self):
        """Display all available commands"""
        print(f"""
{Colors.GOLD}═══════════════════════════════════════════════════════════════════════════════
                          📖 SOVEREIGN COMMANDS
═══════════════════════════════════════════════════════════════════════════════{Colors.END}

{Colors.CYAN}🔧 SYSTEM COMMANDS:{Colors.END}
  {Colors.GREEN}pulse{Colors.END}              - Check empire's vital signs
  {Colors.GREEN}status{Colors.END}             - Full system status report
  {Colors.GREEN}agents{Colors.END}             - List all registered agents

{Colors.CYAN}💣 BOMB COMMANDS:{Colors.END}
  {Colors.RED}deploy bombs{Colors.END}        - 🚨 DEPLOY ALL 5 ATOMIC BOMBS
  {Colors.RED}bomb <1-5>{Colors.END}          - Check specific bomb status

{Colors.CYAN}🧠 HIVE MIND COMMANDS:{Colors.END}
  {Colors.GREEN}sync hive{Colors.END}          - Synchronize collective consciousness
  {Colors.GREEN}hive stats{Colors.END}         - Show hive mind statistics
  {Colors.GREEN}query <text>{Colors.END}       - Search collective memory

{Colors.CYAN}👥 AGENT COMMANDS:{Colors.END}
  {Colors.GREEN}summon <id>{Colors.END}        - Summon agent to boardroom
  {Colors.GREEN}chat <id> <msg>{Colors.END}    - Chat with specific agent
  {Colors.GREEN}council <ids>{Colors.END}      - Summon multiple agents for council
  {Colors.GREEN}broadcast <msg>{Colors.END}    - Broadcast message to all agents

{Colors.CYAN}📊 INTEL COMMANDS:{Colors.END}
  {Colors.GREEN}wisdom <id>{Colors.END}        - Get agent's accumulated wisdom
  {Colors.GREEN}profile <id>{Colors.END}       - Get agent's HR profile

{Colors.CYAN}🔧 UTILITY:{Colors.END}
  {Colors.GREEN}clear{Colors.END}              - Clear screen
  {Colors.GREEN}exit / quit{Colors.END}        - Exit terminal

{Colors.GOLD}═══════════════════════════════════════════════════════════════════════════════{Colors.END}
""")

    async def pulse(self):
        """Check system pulse"""
        print(f"\n{Colors.CYAN}📡 Reading Empire's Pulse...{Colors.END}")
        result = await self.connector.get_system_pulse()
        self._print_result(result)

    async def status(self):
        """Full system status"""
        print(f"\n{Colors.CYAN}📊 Generating Full System Report...{Colors.END}")
        
        # Get pulse
        pulse = await self.connector.get_system_pulse()
        
        # Get local hive stats
        hive_stats = self.oracle.get_stats()
        
        print(f"""
{Colors.GOLD}═══════════════════════════════════════════════════════════════════════════════
                          📊 NEXUS PRIME STATUS REPORT
═══════════════════════════════════════════════════════════════════════════════{Colors.END}

{Colors.CYAN}🌐 API Status:{Colors.END}
{json.dumps(pulse, indent=2) if isinstance(pulse, dict) else pulse}

{Colors.CYAN}🧠 Hive Mind Status:{Colors.END}
   Total Wisdom Points: {hive_stats.get('total_entries', 'N/A')}
   Contributing Agents: {hive_stats.get('agents', 'N/A')}
   Last Sync: {hive_stats.get('last_sync', 'Never')}

{Colors.GOLD}═══════════════════════════════════════════════════════════════════════════════{Colors.END}
""")

    async def agents(self):
        """List all agents"""
        print(f"\n{Colors.CYAN}👥 Fetching Agent Registry...{Colors.END}")
        result = await self.connector.get_all_agents()
        self._print_result(result)

    async def deploy_bombs(self):
        """Deploy all atomic bombs"""
        print(f"\n{Colors.RED}💣💣💣 INITIATING ATOMIC BOMB DEPLOYMENT 💣💣💣{Colors.END}")
        print(f"{Colors.WARNING}⚠️  This will trigger full autopilot mode!{Colors.END}")
        
        confirm = input(f"{Colors.RED}Type 'CONFIRM' to proceed: {Colors.END}")
        if confirm != "CONFIRM":
            print(f"{Colors.WARNING}Aborted.{Colors.END}")
            return
        
        print(f"\n{Colors.GREEN}🚀 Deploying all bombs...{Colors.END}")
        result = await self.connector.deploy_bombs()
        self._print_result(result)

    def sync_hive(self):
        """Synchronize collective consciousness"""
        print(f"\n{Colors.CYAN}🧠 Initiating Hive Mind Sync...{Colors.END}\n")
        count = sync_collective_consciousness()
        print(f"\n{Colors.GREEN}✅ Synced {count} wisdom points!{Colors.END}")

    def hive_stats(self):
        """Show hive mind statistics"""
        stats = self.oracle.get_stats()
        print(f"""
{Colors.GOLD}═══════════════════════════════════════════════════════════════════════════════
                          🧠 HIVE MIND STATISTICS
═══════════════════════════════════════════════════════════════════════════════{Colors.END}

{Colors.CYAN}📊 Overview:{Colors.END}
   Total Wisdom Points: {stats.get('total_entries', 0)}
   Contributing Agents: {stats.get('agents', 0)}
   Last Sync: {stats.get('last_sync', 'Never')}

{Colors.CYAN}📈 Agent Contributions:{Colors.END}""")
        
        breakdown = stats.get('breakdown', {})
        for agent, count in sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = '█' * min(count // 5, 20)
            print(f"   {agent:20} │ {bar} ({count})")
        
        print(f"\n{Colors.GOLD}═══════════════════════════════════════════════════════════════════════════════{Colors.END}")

    def query(self, text):
        """Query collective memory"""
        print(f"\n{Colors.CYAN}🔍 Searching Collective Memory for: '{text}'...{Colors.END}\n")
        results = self.oracle.search_similar(text, limit=5)
        
        if not results:
            print(f"{Colors.WARNING}No results found.{Colors.END}")
            return
        
        for i, r in enumerate(results, 1):
            print(f"{Colors.GREEN}━━━ Result {i} ━━━{Colors.END}")
            agent = r.get('source_agent', 'Unknown')
            print(f"   Agent: {Colors.CYAN}{agent}{Colors.END}")
            # Print relevant fields
            for key in ['action', 'result', 'learning', 'content', 'message']:
                if key in r:
                    print(f"   {key.title()}: {r[key][:100]}...")
                    break
            print()

    async def summon(self, agent_id):
        """Summon agent to boardroom"""
        print(f"\n{Colors.CYAN}📢 Summoning {agent_id} to Boardroom...{Colors.END}")
        result = await self.connector.summon_to_boardroom(agent_id)
        self._print_result(result)

    async def chat(self, agent_id, message):
        """Chat with agent"""
        print(f"\n{Colors.CYAN}💬 Initiating chat with {agent_id}...{Colors.END}")
        result = await self.connector.collective_chat(agent_id, message)
        self._print_result(result)

    async def council(self, agent_ids):
        """Summon council"""
        print(f"\n{Colors.CYAN}🏛️ Summoning Council: {agent_ids}...{Colors.END}")
        topic = input("Council Topic: ")
        result = await self.connector.multi_agent_council(agent_ids.split(','), topic)
        self._print_result(result)

    async def broadcast(self, message):
        """Broadcast to all agents"""
        print(f"\n{Colors.CYAN}📡 Broadcasting to all agents...{Colors.END}")
        result = await self.connector.broadcast_directive(message, priority="high")
        self._print_result(result)

    def wisdom(self, agent_id):
        """Get agent wisdom"""
        print(f"\n{Colors.CYAN}📚 Retrieving wisdom from {agent_id}...{Colors.END}\n")
        results = self.oracle.get_agent_wisdom(agent_id)
        
        if not results:
            print(f"{Colors.WARNING}No wisdom found for {agent_id}.{Colors.END}")
            return
        
        print(f"Found {len(results)} wisdom entries:")
        for r in results[:10]:
            print(f"  • {json.dumps(r, ensure_ascii=False)[:100]}...")

    async def profile(self, agent_id):
        """Get agent profile"""
        print(f"\n{Colors.CYAN}👤 Fetching profile for {agent_id}...{Colors.END}")
        result = await self.connector.get_agent_profile(agent_id)
        self._print_result(result)

    async def bomb_status(self, bomb_id):
        """Get bomb status"""
        print(f"\n{Colors.CYAN}💣 Checking Bomb {bomb_id} status...{Colors.END}")
        result = await self.connector.get_bomb_status(int(bomb_id))
        self._print_result(result)

    def clear(self):
        """Clear screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
        banner()

    def _print_result(self, result):
        """Pretty print a result"""
        if isinstance(result, dict):
            if 'error' in result:
                print(f"{Colors.RED}❌ Error: {result.get('error')}{Colors.END}")
            else:
                print(f"{Colors.GREEN}{json.dumps(result, indent=2, ensure_ascii=False)}{Colors.END}")
        else:
            print(result)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN REPL LOOP
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    """Main REPL loop"""
    os.system('clear' if os.name != 'nt' else 'cls')
    banner()
    
    cmds = SovereignCommands()
    
    while True:
        try:
            cmd = input(f"{Colors.GOLD}NEXUS🔱> {Colors.END}").strip()
            
            if not cmd:
                continue
            
            cmd_lower = cmd.lower()
            parts = cmd.split(maxsplit=1)
            base_cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Exit commands
            if cmd_lower in ['exit', 'quit', 'q']:
                print(f"\n{Colors.GOLD}System Standby. Long live the Architect. 🔱{Colors.END}\n")
                break
            
            # Help
            elif cmd_lower == 'help':
                cmds.help()
            
            # System commands
            elif cmd_lower == 'pulse':
                await cmds.pulse()
            elif cmd_lower == 'status':
                await cmds.status()
            elif cmd_lower == 'agents':
                await cmds.agents()
            elif cmd_lower == 'clear':
                cmds.clear()
            
            # Bomb commands
            elif cmd_lower == 'deploy bombs':
                await cmds.deploy_bombs()
            elif base_cmd == 'bomb' and args:
                await cmds.bomb_status(args)
            
            # Hive mind commands
            elif cmd_lower == 'sync hive':
                cmds.sync_hive()
            elif cmd_lower == 'hive stats':
                cmds.hive_stats()
            elif base_cmd == 'query' and args:
                cmds.query(args)
            
            # Agent commands
            elif base_cmd == 'summon' and args:
                await cmds.summon(args)
            elif base_cmd == 'chat' and args:
                chat_parts = args.split(maxsplit=1)
                if len(chat_parts) >= 2:
                    await cmds.chat(chat_parts[0], chat_parts[1])
                else:
                    print(f"{Colors.WARNING}Usage: chat <agent_id> <message>{Colors.END}")
            elif base_cmd == 'council' and args:
                await cmds.council(args)
            elif base_cmd == 'broadcast' and args:
                await cmds.broadcast(args)
            elif base_cmd == 'wisdom' and args:
                cmds.wisdom(args)
            elif base_cmd == 'profile' and args:
                await cmds.profile(args)
            
            # Unknown command
            else:
                print(f"{Colors.WARNING}Unknown command: '{cmd}'. Type 'help' for available commands.{Colors.END}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Use 'exit' to quit.{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())
