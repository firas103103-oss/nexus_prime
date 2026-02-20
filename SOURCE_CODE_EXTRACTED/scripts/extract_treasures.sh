#!/bin/bash
# 🔍 NEXUS PRIME — سكريبت فك ضغط الكنوز
# Automatic Archive Extraction Script

TEMP_AUDIT_DIR="/tmp/NEXUS_AUDIT_EXTRACT"
REPORT_FILE="/tmp/NEXUS_EXTRACTION_REPORT.txt"

# Create extraction directory
mkdir -p "$TEMP_AUDIT_DIR"

# Initialize report
echo "🔍 === NEXUS TREASURE EXTRACTION REPORT ===" > "$REPORT_FILE"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "🔍 جاري البحث عن ملفات الكنوز المضغوطة..."
echo "📁 Searching for compressed treasures..." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Count files
zip_count=$(find /root -name "*.zip" -not -path "*/node_modules/*" -not -path "*/\.git/*" 2>/dev/null | wc -l)
tar_count=$(find /root -name "*.tar.gz" -not -path "*/node_modules/*" -not -path "*/\.git/*" 2>/dev/null | wc -l)

echo "📊 Found: $zip_count ZIP files, $tar_count TAR.GZ files"
echo "📊 Statistics:" >> "$REPORT_FILE"
echo "  - ZIP files: $zip_count" >> "$REPORT_FILE"
echo "  - TAR.GZ files: $tar_count" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Extract ZIP files
echo "" >> "$REPORT_FILE"
echo "📦 === EXTRACTING ZIP FILES ===" >> "$REPORT_FILE"
echo "📦 فك ضغط ملفات ZIP..."

find /root -name "*.zip" -not -path "*/node_modules/*" -not -path "*/\.git/*" 2>/dev/null | while read -r zipfile; do
    folder_name=$(basename "$zipfile" .zip)
    size=$(du -h "$zipfile" | awk '{print $1}')
    
    echo "  📦 فك ضغط: $folder_name ($size)"
    echo "  - $folder_name ($size) from: $zipfile" >> "$REPORT_FILE"
    
    # Create extraction folder
    extract_dir="$TEMP_AUDIT_DIR/zip_$folder_name"
    mkdir -p "$extract_dir"
    
    # Extract with progress
    unzip -q -o "$zipfile" -d "$extract_dir" 2>&1 | head -5
    
    if [ $? -eq 0 ]; then
        files_count=$(find "$extract_dir" -type f | wc -l)
        echo "    ✅ Extracted: $files_count files" >> "$REPORT_FILE"
    else
        echo "    ❌ FAILED" >> "$REPORT_FILE"
    fi
done

# Extract TAR.GZ files
echo "" >> "$REPORT_FILE"
echo "📦 === EXTRACTING TAR.GZ FILES ===" >> "$REPORT_FILE"
echo "📦 فك ضغط ملفات TAR.GZ..."

find /root -name "*.tar.gz" -not -path "*/node_modules/*" -not -path "*/\.git/*" 2>/dev/null | while read -r tarfile; do
    folder_name=$(basename "$tarfile" .tar.gz)
    size=$(du -h "$tarfile" | awk '{print $1}')
    
    echo "  📦 فك ضغط (Tarball): $folder_name ($size)"
    echo "  - $folder_name ($size) from: $tarfile" >> "$REPORT_FILE"
    
    ##  Create extraction folder
    extract_dir="$TEMP_AUDIT_DIR/tar_$folder_name"
    mkdir -p "$extract_dir"
    
    # Extract with progress
    tar -xzf "$tarfile" -C "$extract_dir" 2>&1 | head -5
    
    if [ $? -eq 0 ]; then
        files_count=$(find "$extract_dir" -type f | wc -l)
        echo "    ✅ Extracted: $files_count files" >> "$REPORT_FILE"
    else
        echo "    ❌ FAILED" >> "$REPORT_FILE"
    fi
done

# Generate summary
echo "" >> "$REPORT_FILE"
echo "📊 === EXTRACTION SUMMARY ===" >> "$REPORT_FILE"

total_extracted=$(find "$TEMP_AUDIT_DIR" -type d -mindepth 1 -maxdepth 1 | wc -l)
total_files=$(find "$TEMP_AUDIT_DIR" -type f | wc -l)
total_size=$(du -sh "$TEMP_AUDIT_DIR" 2>/dev/null | awk '{print $1}')

echo "  ✅ Total extracted directories: $total_extracted" >> "$REPORT_FILE"
echo "  ✅ Total files extracted: $total_files" >> "$REPORT_FILE"
echo "  ✅ Total size: $total_size" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# List extracted directories
echo "📁 === EXTRACTED DIRECTORIES ===" >> "$REPORT_FILE"
find "$TEMP_AUDIT_DIR" -type d -mindepth 1 -maxdepth 1 -exec basename {} \; | sort >> "$REPORT_FILE"

echo ""
echo "✅ تم فك جميع 'الصناديق'. جاهزون للفحص الجراحي."
echo ""
echo "📋 Report saved to: $REPORT_FILE"
echo "📁 Extracted files location: $TEMP_AUDIT_DIR"
echo ""
echo "🔍 Quick inventory:"
echo "  - Directories: $total_extracted"
echo "  - Files: $total_files"
echo "  - Total size: $total_size"
