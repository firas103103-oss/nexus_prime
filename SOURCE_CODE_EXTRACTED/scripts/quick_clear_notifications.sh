#!/bin/bash
# 🧹 مسح سريع لكل إشعارات GitHub

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔔 GitHub Notifications Cleaner"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# التحقق من gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI غير مثبت"
    echo "   نفذ: sudo apt install gh -y"
    exit 1
fi

# التحقق من تسجيل الدخول
if ! gh auth status &> /dev/null; then
    echo "⚠️  غير مسجل دخول في GitHub CLI"
    echo ""
    echo "📝 خطوات تسجيل الدخول:"
    echo "   1. نفذ: gh auth login"
    echo "   2. اختر: GitHub.com"
    echo "   3. اختر: HTTPS"
    echo "   4. اختر: Login with a web browser"
    echo "   5. انسخ الكود وافتح الرابط"
    echo ""
    read -p "❓ هل تريد تسجيل الدخول الآن؟ (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh auth login
    else
        echo "❌ إلغاء العملية"
        exit 1
    fi
fi

echo ""
echo "🔍 فحص عدد الإشعارات الحالية..."
CURRENT=$(gh api /notifications --jq 'length' 2>/dev/null || echo "???")
echo "   📊 الإشعارات الحالية: $CURRENT"
echo ""

if [ "$CURRENT" == "0" ]; then
    echo "✅ لا توجد إشعارات! كل شي نظيف."
    exit 0
fi

echo "🧹 مسح كل الإشعارات..."
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# مسح كل الإشعارات
gh api -X PUT /notifications \
  -f last_read_at="$TIMESTAMP" &> /dev/null

echo "   ✓ تم مسح الإشعارات العامة"

# مسح إشعارات nexus_prime خصيصاً
gh api -X PUT /repos/firas103103-oss/nexus_prime/notifications \
  -f last_read_at="$TIMESTAMP" &> /dev/null

echo "   ✓ تم مسح إشعارات nexus_prime"

echo ""
echo "⏳ التحقق من النتيجة..."
sleep 2

REMAINING=$(gh api /notifications --jq 'length' 2>/dev/null || echo "???")
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 النتائج:"
echo "   قبل: $CURRENT إشعار"
echo "   بعد: $REMAINING إشعار"
echo ""

if [ "$REMAINING" == "0" ]; then
    echo "✅ نجح! جميع الإشعارات تم مسحها!"
else
    echo "⚠️  لا يزال هناك $REMAINING إشعار"
    echo ""
    echo "💡 للمسح اليدوي:"
    echo "   افتح: https://github.com/notifications"
    echo "   اضغط: Shift + a (تحديد الكل)"
    echo "   اضغط: Shift + i (تحديد كمقروء)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
