"""
BOARDROOM BRIDGE — Nexus Prime
═══════════════════════════════
Connects the AI_HR_REGISTRY to the Boardroom and Nerve Center.
Reads profile.yaml (not dossier.yaml) with identity/operational_parameters keys.
"""

import os, yaml, json


class BoardroomBridge:
    def __init__(self, registry_path='/root/NEXUS_PRIME_UNIFIED/AI_HR_REGISTRY'):
        self.registry_path = registry_path
        self.agents_cache = self._build_directory()

    def _build_directory(self):
        """بناء خريطة سريعة لكل الوكلاء لتسريع الاستدعاء بدون البحث كل مرة"""
        directory = {}
        for root, dirs, files in os.walk(self.registry_path):
            if 'profile.yaml' in files:
                filepath = os.path.join(root, 'profile.yaml')
                with open(filepath, 'r') as f:
                    profile = yaml.safe_load(f)
                    agent_id = profile.get('identity', {}).get('id', '')
                    if agent_id:
                        directory[agent_id] = filepath
        return directory

    def list_agents(self):
        """قائمة بجميع الوكلاء المسجلين"""
        agents = []
        for agent_id, filepath in self.agents_cache.items():
            with open(filepath, 'r') as f:
                profile = yaml.safe_load(f)
            identity = profile.get('identity', {})
            agents.append({
                "id": agent_id,
                "name": identity.get('name', ''),
                "title": identity.get('title', ''),
                "department": profile.get('department', ''),
                "clearance": profile.get('clearance_level', ''),
            })
        return agents

    def summon_agent(self, agent_id):
        """استدعاء الوكيل لغرفة الاجتماعات مع كامل هويته وعدته"""
        if agent_id not in self.agents_cache:
            return {"error": f"Agent {agent_id} not found in HR Registry."}

        with open(self.agents_cache[agent_id], 'r') as f:
            profile = yaml.safe_load(f)

        identity = profile.get('identity', {})
        ops = profile.get('operational_parameters', {})
        department = profile.get('department', 'UNKNOWN')
        clearance = profile.get('clearance_level', '??')

        tools = ops.get('assigned_tools', [])
        apis = ops.get('api_access_rights', [])
        protocol = ops.get('communication_protocol', 'DEFAULT')
        specialization = ops.get('specialization', '')

        # هندسة البرومبت الديناميكي اللي رح ينبعث للـ AI
        system_prompt = f"""You are {identity.get('name')} (ID: {identity.get('id')}).
Role: {identity.get('title')} in the {department} department.
Clearance Level: {clearance}.

Core Directive:
{ops.get('system_prompt', 'Execute your assigned duties.')}

Specialization:
{specialization}

Authorized Tools & APIs at your disposal:
{', '.join(tools)}

System Access Endpoints:
{', '.join(apis)}

Communication Protocol: {protocol}
Respond exclusively in character. Address the user strictly as 'Mr. F'."""

        return {
            "status": "success",
            "agent_id": agent_id,
            "agent_name": identity.get('name'),
            "agent_title": identity.get('title'),
            "department": department,
            "clearance": clearance,
            "tools": tools,
            "apis": apis,
            "injected_prompt": system_prompt.strip()
        }

    def summon_department(self, department_name):
        """استدعاء كل وكلاء قسم معين"""
        results = []
        for agent_id in self.agents_cache:
            data = self.summon_agent(agent_id)
            if data.get('department', '').upper() == department_name.upper():
                results.append(data)
        return results

    def get_agent_count(self):
        return len(self.agents_cache)


# ═══════════════════════════════════════════════════════════════
# تجربة سريعة لاستدعاء وكيل لنشوف الانعكاس
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    bridge = BoardroomBridge()

    print(f"╔══════════════════════════════════════════════════════╗")
    print(f"║  BOARDROOM BRIDGE — {bridge.get_agent_count()} Agents Registered     ║")
    print(f"╚══════════════════════════════════════════════════════╝\n")

    # قائمة جميع الوكلاء
    print("━━━ ALL REGISTERED AGENTS ━━━")
    for a in bridge.list_agents():
        print(f"  [{a['clearance']}] {a['id']:20s} │ {a['name']:25s} │ {a['department']}")

    # استدعاء وكيل Shadow كمثال
    print("\n━━━ SUMMONING: socialMediaAgent ━━━")
    result = bridge.summon_agent("socialMediaAgent")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # استدعاء المؤسس
    print("\n━━━ SUMMONING: mrf (SOVEREIGN) ━━━")
    result = bridge.summon_agent("mrf")
    print(json.dumps(result, indent=4, ensure_ascii=False))
