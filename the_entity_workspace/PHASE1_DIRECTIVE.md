# Phase 1 Directive — Sovereign Autonomous Entity

**Issue this directive to OpenHands at http://localhost:3010**

---

## Directive: Map NEXUS PRIME Directory Structure

Execute the following tasks in `/workspace` (which is NEXUS_PRIME_UNIFIED):

1. **Map the directory tree** (max depth 4):
   ```bash
   find /workspace -type d -maxdepth 4 | head -150
   ```

2. **Catalog the 11 Planets** — List each sub-system with its main entry point:
   - dashboard-arc
   - nexus_nerve
   - neural_spine
   - dify
   - products/xbio-sentinel
   - products/alsultan-intelligence (SULTAN)
   - sovereign_gateway
   - shadow-seven-publisher
   - (others as discovered)

3. **Identify key files**:
   - ENTERPRISE_CODEX.yaml
   - docker-compose.yml
   - Main entry points (main.py, routes.ts, etc.)

4. **Output**: Write results to `the_entity_workspace/DIRECTORY_MAP.json` with structure:
   ```json
   {
     "planets": [...],
     "entry_points": [...],
     "key_configs": [...]
   }
   ```

---

## Phase 2 Preview (Next Directive)

After Phase 1 complete: Extract cross-relations between X-BIO, SULTAN, and Codex. Grep for shared references.
