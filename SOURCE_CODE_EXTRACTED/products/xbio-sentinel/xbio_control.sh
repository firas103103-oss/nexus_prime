#!/bin/bash

# مصفوفة الخدمات
SERVICES=("xbio_core.py" "sentinel_monitor.py" "xbio_watchdog.py")

case "$1" in
    start)
        echo "🚀 [X-BIO] جاري تشغيل المنظومة بالكامل..."
        nohup python3 xbio_core.py > core.log 2>&1 &
        nohup python3 -m streamlit run sentinel_monitor.py --server.port 8502 --server.address 0.0.0.0 > monitor.log 2>&1 &
        nohup python3 xbio_watchdog.py > watchdog.log 2>&1 &
        echo "✅ المنظومة حية الآن."
        ;;
    stop)
        echo "🛑 [X-BIO] جاري إيقاف كافة العمليات لتوفير الموارد..."
        pkill -f xbio_core.py
        pkill -f sentinel_monitor.py
        pkill -f xbio_watchdog.py
        echo "✅ تم الإيقاف بأمان."
        ;;
    status)
        echo "📊 [X-BIO] تقرير الحالة الحالية:"
        for s in "${SERVICES[@]}"; do
            pgrep -f $s > /dev/null && echo "🟢 $s: ACTIVE" || echo "🔴 $s: INACTIVE"
        done
        ;;
    clean)
        echo "🧹 [X-BIO] تنظيف السجلات والملفات المؤقتة..."
        rm -f *.log
        echo "✅ السجلات نظيفة."
        ;;
esac
