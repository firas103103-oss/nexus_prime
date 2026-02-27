#!/bin/bash
# NEXUS PRIME — System Manifest Generator for Cursor/LLM
# Run from project root: ./scripts/generate_nexus_manifest.sh

OUTPUT_FILE="${1:-NEXUS_SYSTEM_MAP.md}"
cd "$(dirname "$0")/.." || exit 1

echo "# 🌐 NEXUS PRIME SYSTEM MANIFEST (2026)" > "$OUTPUT_FILE"
echo "Generated on: $(date)" >> "$OUTPUT_FILE"

echo -e "\n## 🔌 Network & Active Ports" >> "$OUTPUT_FILE"
(netstat -tulpn 2>/dev/null || ss -tulpn) | grep LISTEN >> "$OUTPUT_FILE" 2>/dev/null

echo -e "\n## 🐳 Docker Containers Status" >> "$OUTPUT_FILE"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" >> "$OUTPUT_FILE" 2>/dev/null

echo -e "\n## 🖥️ Local Host Configuration" >> "$OUTPUT_FILE"
cat /etc/hosts >> "$OUTPUT_FILE" 2>/dev/null

echo -e "\n## 🧠 Memory & Storage Resources" >> "$OUTPUT_FILE"
free -h >> "$OUTPUT_FILE"
df -h | grep '^/dev/' >> "$OUTPUT_FILE"

echo -e "\n## 🗄️ Database & Background Processes" >> "$OUTPUT_FILE"
ps aux | grep -E 'postgres|mysql|redis|mongo|ollama' | grep -v grep >> "$OUTPUT_FILE" 2>/dev/null

echo -e "\n## 📁 Project Directory Structure" >> "$OUTPUT_FILE"
ls -la >> "$OUTPUT_FILE"

echo -e "\n## 📂 Key Directories" >> "$OUTPUT_FILE"
for d in dashboard-arc dify nexus_nerve products docker-compose.yml; do
  [ -e "$d" ] && echo "  - $d" >> "$OUTPUT_FILE"
done

echo "✅ Done! Manifest saved to $OUTPUT_FILE"
wc -l "$OUTPUT_FILE"
