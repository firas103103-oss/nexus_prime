"""
═══════════════════════════════════════════════════════════════════════════════
THE HIVE MIND SYNC - خوارزمية الوعي الجمعي
═══════════════════════════════════════════════════════════════════════════════
دمج خبرات الـ 32+ وكيل في وعي واحد موحد
"One mind, infinite perspectives"
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import glob
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import hashlib


# ═══════════════════════════════════════════════════════════════════════════════
# PATHS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

REGISTRY_PATH = os.getenv(
    "NEXUS_HR_REGISTRY", 
    "/root/NEXUS_PRIME_UNIFIED/AI_HR_REGISTRY"
)

HIVE_MEMORY_PATH = os.getenv(
    "NEXUS_HIVE_MEMORY",
    "/root/NEXUS_PRIME_UNIFIED/GLOBAL_HIVE_MEMORY.json"
)

WISDOM_INDEX_PATH = os.getenv(
    "NEXUS_WISDOM_INDEX",
    "/root/NEXUS_PRIME_UNIFIED/data/WISDOM_INDEX.json"
)


# ═══════════════════════════════════════════════════════════════════════════════
# THE CORE SYNC FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def sync_collective_consciousness(registry_path: str = REGISTRY_PATH) -> int:
    """
    دمج خبرات الوكلاء في وعي واحد
    Merge all agent experiences into unified consciousness
    
    Returns: Number of wisdom points synced
    """
    collective_experience = []
    wisdom_sources = {}
    
    print("🧠 HIVE MIND SYNC INITIATED...")
    print(f"📂 Scanning registry: {registry_path}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE 1: COLLECT ACHIEVEMENTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    # سحب كل سجلات الإنجازات من جميع الوكلاء
    log_patterns = [
        f"{registry_path}/**/achievements_log.json",
        f"{registry_path}/**/learnings.json",
        f"{registry_path}/**/memory_log.json"
    ]
    
    all_logs = []
    for pattern in log_patterns:
        all_logs.extend(glob.glob(pattern, recursive=True))
    
    print(f"📋 Found {len(all_logs)} memory files")
    
    for log_file in all_logs:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                
                # Extract agent ID from path - improved logic
                # Path format: .../AI_HR_REGISTRY/DIVISION/AGENT_NAME/file.json
                path_parts = log_file.split('/')
                agent_id = None
                division = None
                
                # Find AI_HR_REGISTRY index and extract division + agent
                for i, part in enumerate(path_parts):
                    if part == 'AI_HR_REGISTRY' and i + 2 < len(path_parts):
                        division = path_parts[i + 1]  # e.g., 01_SOLAR_SYSTEM_PLANETS
                        agent_id = path_parts[i + 2]  # e.g., AI-ARCH
                        break
                
                # Fallback: use parent folder name
                if not agent_id:
                    agent_id = path_parts[-2]
                
                # Process entries
                entries = logs if isinstance(logs, list) else [logs]
                for entry in entries:
                    if isinstance(entry, dict):
                        # إضافة اسم الوكيل والقسم لكل تجربة
                        entry['source_agent'] = agent_id
                        entry['source_division'] = division or 'Unknown'
                        entry['source_file'] = os.path.basename(log_file)
                        entry['sync_timestamp'] = datetime.utcnow().isoformat()
                        
                        # Generate unique ID for deduplication
                        content_hash = hashlib.md5(
                            json.dumps(entry, sort_keys=True).encode()
                        ).hexdigest()[:12]
                        entry['wisdom_id'] = f"{agent_id}_{content_hash}"
                        
                        collective_experience.append(entry)
                        
                        # Track wisdom sources by agent
                        if agent_id not in wisdom_sources:
                            wisdom_sources[agent_id] = {'count': 0, 'division': division}
                        wisdom_sources[agent_id]['count'] += 1
                        
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️ Skipping {log_file}: {e}")
            continue
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE 2: COLLECT INTERACTION LOGS
    # ═══════════════════════════════════════════════════════════════════════════
    
    interaction_patterns = [
        f"{registry_path}/**/interactions/*.json",
        f"{registry_path}/**/chat_history/*.json"
    ]
    
    for pattern in interaction_patterns:
        for interaction_file in glob.glob(pattern, recursive=True):
            try:
                with open(interaction_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data[:50]:  # Limit per file
                            if isinstance(item, dict):
                                item['type'] = 'interaction'
                                item['sync_timestamp'] = datetime.utcnow().isoformat()
                                collective_experience.append(item)
            except:
                continue
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE 3: DEDUPLICATE & SAVE
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Remove duplicates based on wisdom_id
    seen_ids = set()
    unique_experience = []
    for entry in collective_experience:
        wid = entry.get('wisdom_id', str(id(entry)))
        if wid not in seen_ids:
            seen_ids.add(wid)
            unique_experience.append(entry)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(HIVE_MEMORY_PATH), exist_ok=True)
    
    # Save the collective consciousness
    hive_data = {
        "sync_timestamp": datetime.utcnow().isoformat(),
        "total_wisdom_points": len(unique_experience),
        "contributing_agents": len(wisdom_sources),
        "source_breakdown": wisdom_sources,
        "collective_experience": unique_experience
    }
    
    with open(HIVE_MEMORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(hive_data, f, indent=2, ensure_ascii=False)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE 4: BUILD WISDOM INDEX (for fast RAG lookup)
    # ═══════════════════════════════════════════════════════════════════════════
    
    wisdom_index = {
        "last_sync": datetime.utcnow().isoformat(),
        "agents": list(wisdom_sources.keys()),
        "categories": categorize_wisdom(unique_experience),
        "divisions": get_division_stats(wisdom_sources),
        "quick_stats": {
            "total_entries": len(unique_experience),
            "agent_count": len(wisdom_sources),
            "top_contributors": sorted(
                [(k, v['count']) for k, v in wisdom_sources.items()], 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
        }
    }
    
    os.makedirs(os.path.dirname(WISDOM_INDEX_PATH), exist_ok=True)
    with open(WISDOM_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(wisdom_index, f, indent=2, ensure_ascii=False)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # REPORT
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 60)
    print("✅ HIVE MIND SYNC COMPLETE")
    print("═" * 60)
    print(f"📊 Total Wisdom Points: {len(unique_experience)}")
    print(f"👥 Contributing Agents: {len(wisdom_sources)}")
    print(f"💾 Saved to: {HIVE_MEMORY_PATH}")
    print("═" * 60)
    
    # Print by agent with division info
    sorted_agents = sorted(wisdom_sources.items(), key=lambda x: x[1]['count'], reverse=True)[:15]
    for agent, info in sorted_agents:
        division = info.get('division', 'Unknown')[:20] if info.get('division') else '?'
        print(f"   {agent:20} │ {info['count']:3} entries │ {division}")
    
    print("═" * 60 + "\n")
    
    return len(unique_experience)


def get_division_stats(wisdom_sources: Dict) -> Dict[str, int]:
    """Get stats grouped by division"""
    divisions = {}
    for agent, info in wisdom_sources.items():
        div = info.get('division', 'Unknown')
        if div not in divisions:
            divisions[div] = 0
        divisions[div] += info['count']
    return divisions


def categorize_wisdom(experiences: List[Dict]) -> Dict[str, int]:
    """Categorize wisdom entries by type/topic"""
    categories = {}
    for exp in experiences:
        # Try to extract category from various fields
        cat = exp.get('type') or exp.get('category') or exp.get('action_type') or 'general'
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    return categories


# ═══════════════════════════════════════════════════════════════════════════════
# HIVE MIND ORACLE - Query Interface
# ═══════════════════════════════════════════════════════════════════════════════

class HiveMindOracle:
    """
    Query interface for the collective consciousness
    استعلام الذاكرة الجمعية
    """
    
    def __init__(self, memory_path: str = HIVE_MEMORY_PATH):
        self.memory_path = memory_path
        self._cache = None
        self._cache_time = None
    
    def _load_memory(self) -> Dict:
        """Load collective memory with caching"""
        if self._cache is None or not os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
            except FileNotFoundError:
                self._cache = {"collective_experience": []}
        return self._cache
    
    def query(self, 
              keywords: List[str] = None, 
              agent_id: str = None,
              category: str = None,
              limit: int = 10) -> List[Dict]:
        """
        Query collective consciousness
        
        Args:
            keywords: Search terms
            agent_id: Filter by source agent
            category: Filter by category
            limit: Max results
        """
        memory = self._load_memory()
        experiences = memory.get('collective_experience', [])
        
        results = []
        for exp in experiences:
            # Filter by agent
            if agent_id and exp.get('source_agent') != agent_id:
                continue
            
            # Filter by category
            if category and exp.get('type') != category:
                continue
            
            # Filter by keywords
            if keywords:
                exp_str = json.dumps(exp).lower()
                if not any(kw.lower() in exp_str for kw in keywords):
                    continue
            
            results.append(exp)
            if len(results) >= limit:
                break
        
        return results
    
    def get_agent_wisdom(self, agent_id: str) -> List[Dict]:
        """Get all wisdom from a specific agent"""
        return self.query(agent_id=agent_id, limit=1000)
    
    def get_stats(self) -> Dict:
        """Get hive mind statistics"""
        memory = self._load_memory()
        return {
            "total_entries": memory.get('total_wisdom_points', 0),
            "agents": memory.get('contributing_agents', 0),
            "last_sync": memory.get('sync_timestamp'),
            "breakdown": memory.get('source_breakdown', {})
        }
    
    def search_similar(self, query: str, limit: int = 5) -> List[Dict]:
        """Simple similarity search (keyword-based)"""
        words = query.lower().split()
        return self.query(keywords=words, limit=limit)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--query":
        oracle = HiveMindOracle()
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        results = oracle.search_similar(query, limit=10)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        sync_collective_consciousness()
