#!/bin/bash
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TARGET_DIR="/root/NEXUS_PRIME_UNIFIED/dashboard-arc"
REPORT_FILE="/root/NEXUS_PRIME_UNIFIED/DASHBOARD_BLUEPRINT.md"

echo -e "${BLUE}--- [ NEXUS DASHBOARD: CODE ANATOMY REPORT ] ---${NC}" > $REPORT_FILE

echo -e "\n## 🖥️ 1. الواجهة الأمامية (Frontend - React/Vite)" >> $REPORT_FILE
echo "المسار: client/src/" >> $REPORT_FILE
echo "### الصفحات (Pages):" >> $REPORT_FILE
ls -1 $TARGET_DIR/client/src/pages/*.tsx 2>/dev/null | xargs -n 1 basename >> $REPORT_FILE
echo -e "\n### المكونات (Components):" >> $REPORT_FILE
ls -1 $TARGET_DIR/client/src/components/*.tsx 2>/dev/null | xargs -n 1 basename >> $REPORT_FILE

echo -e "\n## ⚙️ 2. النظام الخلفي (Backend - Express/Node)" >> $REPORT_FILE
echo "المسار: server/" >> $REPORT_FILE
echo "### المسارات (Routes & API):" >> $REPORT_FILE
ls -1 $TARGET_DIR/server/routes.ts >> $REPORT_FILE
ls -1 $TARGET_DIR/server/routes/*.ts 2>/dev/null | xargs -n 1 basename >> $REPORT_FILE
echo -e "\n### المنطق (Modules & Services):" >> $REPORT_FILE
ls -1 $TARGET_DIR/server/modules/*.ts 2>/dev/null | xargs -n 1 basename >> $REPORT_FILE

echo -e "\n## 🗄️ 3. قاعدة البيانات (Database Schema)" >> $REPORT_FILE
echo "المسار: shared/" >> $REPORT_FILE
ls -1 $TARGET_DIR/shared/schema.ts >> $REPORT_FILE

echo -e "${GREEN}✅ BLUEPRINT GENERATED: $REPORT_FILE${NC}"
cat $REPORT_FILE
