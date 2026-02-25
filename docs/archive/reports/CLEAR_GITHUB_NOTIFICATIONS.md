# 🔔 حل مشكلة الإشعارات المتراكمة على GitHub (1000+)

> **المشكلة:** أكثر من 1000 إشعار عالق على GitHub
> **الحل:** دليل شامل لمسح كل الإشعارات

---

## 🚀 الطريقة السريعة (3 دقائق)

### الخطوة 1: مسح كل الإشعارات دفعة واحدة

**افتح هذا الرابط مباشرة:**
```
https://github.com/notifications
```

**ثم اضغط على:**
1. ✅ **Select all** (أعلى القائمة)
2. ✅ **Mark as done** (زر أزرق)

**أو استخدم اختصارات لوحة المفاتيح:**
- اضغط `Shift + a` → لتحديد الكل
- اضغط `Shift + i` → لتحديد كلهم كـ "مقروء"
- اضغط `y` → لـ mark as done

---

## 🔧 الطريقة المتقدمة (API Script)

إذا ما نفعت الطريقة السريعة، استخدم هذا السكريبت:

### تثبيت GitHub CLI وتسجيل الدخول:
```bash
# التحقق من التثبيت
gh --version

# تسجيل الدخول
gh auth login
# اختر: GitHub.com
# اختر: HTTPS
# اختر: Login with a web browser
# انسخ الكود وافتح الرابط
```

### مسح كل الإشعارات:
```bash
# مسح كل الإشعارات دفعة واحدة
gh api -X PUT /notifications \
  -f last_read_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# التحقق من العدد المتبقي
gh api /notifications --jq 'length'
```

---

## 🎯 الطريقة الشاملة (مسح حسب Repository)

### مسح إشعارات repository محدد:
```bash
# مسح إشعارات nexus_prime
gh api -X PUT /repos/firas103103-oss/nexus_prime/notifications \
  -f last_read_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### مسح كل الإشعارات لكل الـ repositories:
```bash
#!/bin/bash
# احفظ هذا في ملف: clear_all_notifications.sh

echo "🧹 مسح كل إشعارات GitHub..."

# الحصول على قائمة كل الـ repos
REPOS=$(gh repo list --limit 100 --json nameWithOwner -q '.[].nameWithOwner')

# مسح إشعارات كل repo
for repo in $REPOS; do
  echo "  ✓ مسح إشعارات: $repo"
  gh api -X PUT "/repos/$repo/notifications" \
    -f last_read_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null
done

# مسح كل الإشعارات العامة
echo "  ✓ مسح كل الإشعارات المتبقية..."
gh api -X PUT /notifications \
  -f last_read_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# التحقق
REMAINING=$(gh api /notifications --jq 'length')
echo "✅ تم! الإشعارات المتبقية: $REMAINING"
```

**تشغيله:**
```bash
chmod +x clear_all_notifications.sh
./clear_all_notifications.sh
```

---

## 🔐 الطريقة اليدوية (Personal Access Token)

إذا ما اشتغل GitHub CLI:

### 1. إنشاء Token:
- افتح: https://github.com/settings/tokens
- اضغط **Generate new token (classic)**
- حدد الصلاحيات: `notifications` (فقط)
- انسخ الـ Token

### 2. استخدم cURL:
```bash
# احفظ الـ Token في متغير
export GITHUB_TOKEN="ghp_your_token_here"

# مسح كل الإشعارات
curl -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"last_read_at":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' \
  https://api.github.com/notifications

# التحقق من الباقي
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/notifications | jq 'length'
```

---

## ⚙️ إعدادات لمنع التراكم مستقبلاً

### تعطيل الإشعارات غير المهمة:

**افتح الإعدادات:**
```
https://github.com/settings/notifications
```

**الإعدادات الموصى بها:**

✅ **Watching:**
- ❌ Automatically watch repositories (أوقفها)
- ❌ Automatically watch teams (أوقفها)

✅ **Participating and @mentions:**
- ✅ On GitHub (فقط)
- ❌ Email (أوقفها إذا مو محتاجها)

✅ **Custom routing:**
- اختر `Notification settings` لكل repo مهم فقط

### مسح الإشعارات تلقائياً:

**أضف هذا لـ `.bashrc` أو `.zshrc`:**
```bash
alias gh-clear="gh api -X PUT /notifications -f last_read_at=\"\$(date -u +%Y-%m-%dT%H:%M:%SZ)\" && echo '✅ تم مسح كل الإشعارات'"
```

**استخدمه:**
```bash
gh-clear
```

---

## 🎯 حل سريع (من المتصفح فقط)

### Chrome/Firefox Extension:
استخدم هذا الامتداد لمسح الإشعارات بضغطة واحدة:
- **Octotree** → يضيف زر "Mark all as read"
- **Refined GitHub** → يحسن واجهة الإشعارات

### JavaScript في Console:
إذا كنت على صفحة الإشعارات:
```javascript
// افتح Developer Console (F12)
// الصق هذا الكود:

fetch('/notifications/mark', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
  }
}).then(() => location.reload())
```

---

## 📊 التحقق من النتائج

### فحص عدد الإشعارات:
```bash
# باستخدام gh
gh api /notifications --jq 'length'

# باستخدام curl (مع token)
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/notifications | jq 'length'

# يجب أن يرجع: 0
```

### فحص آخر نشاط:
```bash
gh api /notifications --jq '.[] | {repo: .repository.full_name, reason: .reason, updated: .updated_at}' | head -20
```

---

## ❓ الأسئلة المتوقعة

### "ليش الإشعارات تتراكم؟"
**الأسباب:**
1. **Commits كثيرة** → كل commit يولد إشعار
2. **Watching repos كثيرة** → تستقبل إشعار لكل نشاط
3. **Team mentions** → ذكرك في discussions كثيرة
4. **GitHub Actions** → كل workflow يرسل إشعار

### "هل مسح الإشعارات آمن؟"
✅ **نعم!** مسح الإشعارات لا يحذف:
- ❌ Commits
- ❌ Issues
- ❌ Pull Requests
- ❌ Code

فقط يمسح **علامة "غير مقروء"** من الإشعارات.

### "كيف أمنع التراكم مستقبلاً؟"
**توصيات:**
1. ✅ **Unwatch** الـ repos غير المهمة
2. ✅ مسح الإشعارات يومياً (استخدم alias)
3. ✅ استخدم Filters في صفحة الإشعارات
4. ✅ شغل Email فقط للمهم (Participating)

---

## 🎉 الملخص السريع

### لمسح 1000+ إشعار الآن:

**الطريقة الأسرع (30 ثانية):**
```bash
# سجل دخول مرة واحدة
gh auth login

# امسح كل شي
gh api -X PUT /notifications -f last_read_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# تحقق
gh api /notifications --jq 'length'
# النتيجة: 0
```

**من المتصفح (دقيقة واحدة):**
1. افتح: https://github.com/notifications
2. اضغط `Shift + a` (تحديد الكل)
3. اضغط `Shift + i` (تحديد كمقروء)
4. اضغط على **Done** أو `y`

---

## 🔄 Next Steps (الخطوات التالية)

بعد مسح الإشعارات:

✅ **ضبط الإعدادات:**
```
https://github.com/settings/notifications
```

✅ **Unwatch الـ repos غير المهمة:**
```bash
gh repo list --limit 100 | while read repo _; do
  gh api -X DELETE "/repos/$repo/subscription"
done
```

✅ **إنشاء Cron Job للمسح التلقائي:**
```bash
# أضف لـ crontab
crontab -e

# امسح الإشعارات كل يوم الساعة 8 صباحاً
0 8 * * * /usr/bin/gh api -X PUT /notifications -f last_read_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

---

**Generated:** 2026-02-20  
**Problem:** 1000+ GitHub notifications stuck  
**Status:** ✅ Solutions provided (4 methods)  
**Time to fix:** 30 seconds - 3 minutes
