// ═══════════════════════════════════════════════════════════════════════════
// 🚀 NEXUS PRIME - LLM Stress Testing Script (K6)
// ═══════════════════════════════════════════════════════════════════════════
// Purpose: اختبار ضغط على محرك Ollama/LiteLLM لقياس القدرة الفعلية
// Target: http://localhost:4000 (LiteLLM) و http://localhost:9000 (Memory Keeper)
// Metrics: RPS, Latency, Error Rate, Queuing Time
// ═══════════════════════════════════════════════════════════════════════════

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// ═══════════════════════════════════════════════════════════════════════════
// 📊 Custom Metrics
// ═══════════════════════════════════════════════════════════════════════════
const errorRate = new Rate('errors');
const llmResponseTime = new Trend('llm_response_time');
const queuedRequests = new Counter('queued_requests');
const successfulRequests = new Counter('successful_requests');

// ═══════════════════════════════════════════════════════════════════════════
// ⚙️ Test Configuration
// ═══════════════════════════════════════════════════════════════════════════
export const options = {
    scenarios: {
        // 1️⃣ Warm-up Phase (تسخين تدريجي)
        warmup: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '30s', target: 5 },   // 5 users for 30s
                { duration: '30s', target: 10 },  // 10 users for 30s
            ],
            gracefulRampDown: '10s',
        },
        
        // 2️⃣ Load Testing (اختبار الحمل الطبيعي)
        load_test: {
            executor: 'constant-vus',
            vus: 20,
            duration: '3m',
            startTime: '1m10s', // يبدأ بعد الـ warm-up
        },
        
        // 3️⃣ Spike Testing (اختبار الذروة المفاجئة)
        spike_test: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '10s', target: 50 },  // قفزة مفاجئة إلى 50 user
                { duration: '1m', target: 50 },   // استمرار لمدة دقيقة
                { duration: '10s', target: 0 },   // تراجع سريع
            ],
            startTime: '4m10s', // يبدأ بعد الـ load test
        },
        
        // 4️⃣ Stress Testing (اختبار حد الانهيار)
        stress_test: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '1m', target: 100 },  // تدريجياً إلى 100
                { duration: '2m', target: 100 },  // ثبات عند 100
                { duration: '1m', target: 0 },    // تنازل تدريجي
            ],
            startTime: '5m30s', // يبدأ بعد الـ spike test
        },
    },
    
    thresholds: {
        'http_req_duration': ['p(95)<30000'],     // 95% of requests < 30s
        'http_req_failed': ['rate<0.1'],          // Error rate < 10%
        'llm_response_time': ['p(90)<25000'],     // 90% < 25s
    },
};

// ═══════════════════════════════════════════════════════════════════════════
// 🧪 Test Scenarios
// ═══════════════════════════════════════════════════════════════════════════

const LITELLM_URL = 'http://localhost:4000';
const MEMORY_KEEPER_URL = 'http://localhost:9000';

// نماذج الأسئلة (متنوعة الطول والتعقيد)
const questions = [
    'ما هو عدد الوكلاء النشطين الآن؟',
    'أعطني تقريراً مختصراً عن صحة النظام',
    'اشرح لي بنية NEXUS PRIME بالتفصيل مع جميع المكونات والخدمات والعلاقات بينها',
    'ما هي أهم 5 أحداث حصلت اليوم في النظام؟',
    'حلل لي أداء قاعدة البيانات واعطني توصيات للتحسين',
];

export default function () {
    const question = questions[Math.floor(Math.random() * questions.length)];
    
    // ═══════════════════════════════════════════════════════════════════════════
    // Test 1: Memory Keeper Conversation (الاختبار الأساسي)
    // ═══════════════════════════════════════════════════════════════════════════
    const memoryKeeperPayload = JSON.stringify({
        user_name: `LoadTest_User_${__VU}`,
        message: question,
    });
    
    const memoryKeeperParams = {
        headers: { 'Content-Type': 'application/json' },
        timeout: '60s',
    };
    
    const startTime = Date.now();
    const memoryKeeperResponse = http.post(
        `${MEMORY_KEEPER_URL}/conversation`,
        memoryKeeperPayload,
        memoryKeeperParams
    );
    const responseTime = Date.now() - startTime;
    
    // Record metrics
    llmResponseTime.add(responseTime);
    errorRate.add(memoryKeeperResponse.status !== 200);
    
    const memoryKeeperCheck = check(memoryKeeperResponse, {
        'Memory Keeper: status is 200': (r) => r.status === 200,
        'Memory Keeper: has response': (r) => {
            try {
                const body = JSON.parse(r.body);
                return body.response !== null && body.response !== undefined;
            } catch (e) {
                return false;
            }
        },
        'Memory Keeper: response time < 30s': (r) => responseTime < 30000,
    });
    
    if (memoryKeeperCheck) {
        successfulRequests.add(1);
    } else {
        if (memoryKeeperResponse.status === 429) {
            queuedRequests.add(1);
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════════════
    // Test 2: Direct LiteLLM Call (اختبار مباشر)
    // ═══════════════════════════════════════════════════════════════════════════
    const litellmPayload = JSON.stringify({
        model: 'mrf_brain',
        messages: [
            { role: 'system', content: 'أنت مساعد ذكي لنظام NEXUS PRIME' },
            { role: 'user', content: question }
        ],
        max_tokens: 500,
    });
    
    const litellmParams = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sk-nexus-sovereign-mrf',
        },
        timeout: '60s',
    };
    
    const litellmResponse = http.post(
        `${LITELLM_URL}/v1/chat/completions`,
        litellmPayload,
        litellmParams
    );
    
    check(litellmResponse, {
        'LiteLLM: status is 200': (r) => r.status === 200,
        'LiteLLM: has choices': (r) => {
            try {
                const body = JSON.parse(r.body);
                return body.choices && body.choices.length > 0;
            } catch (e) {
                return false;
            }
        },
    });
    
    // Controlled pacing (تباعد الطلبات)
    sleep(Math.random() * 2 + 1); // 1-3 seconds between requests
}

// ═══════════════════════════════════════════════════════════════════════════
// 📈 Summary Handler
// ═══════════════════════════════════════════════════════════════════════════
export function handleSummary(data) {
    return {
        'stdout': textSummary(data, { indent: ' ', enableColors: true }),
        '/tmp/k6_llm_stress_report.json': JSON.stringify(data, null, 2),
        '/tmp/k6_llm_stress_report.html': htmlReport(data),
    };
}

// Helper للـ Text Summary
function textSummary(data, opts) {
    const { indent = '', enableColors = false } = opts || {};
    let output = '\n';
    
    output += `${indent}✅ عدد الطلبات الناجحة: ${data.metrics.successful_requests?.values?.count || 0}\n`;
    output += `${indent}⏳ عدد الطلبات المتأخرة: ${data.metrics.queued_requests?.values?.count || 0}\n`;
    output += `${indent}❌ معدل الأخطاء: ${((data.metrics.errors?.values?.rate || 0) * 100).toFixed(2)}%\n`;
    output += `${indent}⏱️  متوسط وقت الاستجابة: ${(data.metrics.llm_response_time?.values?.avg || 0).toFixed(0)}ms\n`;
    output += `${indent}📊 الحد الأقصى: ${(data.metrics.llm_response_time?.values?.max || 0).toFixed(0)}ms\n`;
    output += `${indent}📉 الحد الأدنى: ${(data.metrics.llm_response_time?.values?.min || 0).toFixed(0)}ms\n`;
    
    return output;
}

// Helper للـ HTML Report
function htmlReport(data) {
    return `<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>NEXUS PRIME - LLM Stress Test Report</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0e27; color: #00ff9f; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #00ff9f; padding-bottom: 20px; }
        .metric { background: #1a1f3a; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #00ff9f; }
        .metric h3 { margin: 0 0 10px 0; color: #00d4ff; }
        .metric p { margin: 5px 0; font-size: 18px; }
        .success { color: #00ff9f; }
        .warning { color: #ffa500; }
        .error { color: #ff4444; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 NEXUS PRIME - LLM Stress Test Report</h1>
        <p>Generated: ${new Date().toLocaleString('ar-EG')}</p>
    </div>
    <div class="metric">
        <h3>✅ الطلبات الناجحة</h3>
        <p class="success">${data.metrics.successful_requests?.values?.count || 0} طلب</p>
    </div>
    <div class="metric">
        <h3>⏳ الطلبات المتأخرة (Queued)</h3>
        <p class="warning">${data.metrics.queued_requests?.values?.count || 0} طلب</p>
    </div>
    <div class="metric">
        <h3>❌ معدل الأخطاء</h3>
        <p class="error">${((data.metrics.errors?.values?.rate || 0) * 100).toFixed(2)}%</p>
    </div>
    <div class="metric">
        <h3>⏱️ أوقات الاستجابة</h3>
        <p>متوسط: ${(data.metrics.llm_response_time?.values?.avg || 0).toFixed(0)}ms</p>
        <p>الحد الأقصى: ${(data.metrics.llm_response_time?.values?.max || 0).toFixed(0)}ms</p>
        <p>الحد الأدنى: ${(data.metrics.llm_response_time?.values?.min || 0).toFixed(0)}ms</p>
        <p>P95: ${(data.metrics.llm_response_time?.values?.['p(95)'] || 0).toFixed(0)}ms</p>
    </div>
    <div class="metric">
        <h3>📊 إجمالي الطلبات</h3>
        <p>${data.metrics.http_reqs?.values?.count || 0} طلب HTTP</p>
    </div>
</body>
</html>`;
}
