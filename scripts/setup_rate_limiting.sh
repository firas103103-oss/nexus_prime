#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🔧 NEXUS PRIME - Rate Limiting Setup Script
# ═══════════════════════════════════════════════════════════════════════════

set -e

echo "🚀 NEXUS PRIME - إعداد Rate Limiting على API Gateway"
echo "════════════════════════════════════════════════════════════════"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════
# 1️⃣ إضافة Rate Limiting Middleware إلى Cortex
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}1️⃣ إضافة Rate Limiting إلى Cortex...${NC}"

cat > /root/NEXUS_PRIME_UNIFIED/ecosystem-api/middleware/rateLimiter.js << 'EOF'
// ═══════════════════════════════════════════════════════════════════════════
// 🛡️ NEXUS PRIME - Rate Limiting Middleware
// ═══════════════════════════════════════════════════════════════════════════
// Purpose: حماية API من الإساءة والاستهلاك الزائد
// Strategy: Token Bucket Algorithm مع Redis للتوزيع
// ═══════════════════════════════════════════════════════════════════════════

const Redis = require('ioredis');
const redis = new Redis({
    host: process.env.REDIS_HOST || 'nexus_redis',
    port: process.env.REDIS_PORT || 6379,
    db: 1, // Database منفصل للـ rate limiting
});

// ═══════════════════════════════════════════════════════════════════════════
// ⚙️ Rate Limit Tiers (مستويات التحديد)
// ═══════════════════════════════════════════════════════════════════════════
const RATE_LIMITS = {
    // Anonymous users
    anonymous: {
        points: 100,        // 100 request
        duration: 60,       // per minute
        blockDuration: 300, // block for 5 minutes
    },
    
    // Authenticated users
    authenticated: {
        points: 500,
        duration: 60,
        blockDuration: 180,
    },
    
    // Premium users
    premium: {
        points: 2000,
        duration: 60,
        blockDuration: 60,
    },
    
    // AI endpoints (خاص بالذكاء الاصطناعي)
    ai_endpoints: {
        points: 20,         // 20 AI requests
        duration: 60,       // per minute
        blockDuration: 300,
    },
};

// ═══════════════════════════════════════════════════════════════════════════
// 🔍 Identify User Tier
// ═══════════════════════════════════════════════════════════════════════════
function getUserTier(req) {
    // للذكاء الاصطناعي
    if (req.path.includes('/ai/') || req.path.includes('/conversation')) {
        return 'ai_endpoints';
    }
    
    // للمستخدمين المميزين
    if (req.user && req.user.subscription === 'premium') {
        return 'premium';
    }
    
    // للمستخدمين المسجلين
    if (req.user) {
        return 'authenticated';
    }
    
    // الزوار
    return 'anonymous';
}

// ═══════════════════════════════════════════════════════════════════════════
// 🔐 Get Client Identifier
// ═══════════════════════════════════════════════════════════════════════════
function getClientId(req) {
    // إذا في user مسجل، استخدم الـ user_id
    if (req.user && req.user.id) {
        return `user:${req.user.id}`;
    }
    
    // استخدم الـ IP address
    const ip = req.headers['x-forwarded-for'] || 
               req.headers['x-real-ip'] || 
               req.connection.remoteAddress ||
               req.ip;
    
    return `ip:${ip}`;
}

// ═══════════════════════════════════════════════════════════════════════════
// 🛡️ Rate Limiter Middleware
// ═══════════════════════════════════════════════════════════════════════════
async function rateLimiter(req, res, next) {
    try {
        const clientId = getClientId(req);
        const tier = getUserTier(req);
        const limit = RATE_LIMITS[tier];
        
        const key = `ratelimit:${tier}:${clientId}`;
        
        // Get current count from Redis
        const current = await redis.get(key);
        
        // Check if blocked
        const blockKey = `blocked:${clientId}`;
        const isBlocked = await redis.get(blockKey);
        
        if (isBlocked) {
            const ttl = await redis.ttl(blockKey);
            return res.status(429).json({
                error: 'Too Many Requests',
                message: `تم حظرك مؤقتاً بسبب تجاوز الحد المسموح. انتظر ${ttl} ثانية.`,
                retry_after: ttl,
                limit: limit.points,
                tier: tier,
            });
        }
        
        // Increment and check
        let count = current ? parseInt(current) : 0;
        count++;
        
        if (count > limit.points) {
            // Block the user
            await redis.setex(blockKey, limit.blockDuration, '1');
            
            // Log to Memory Keeper
            await fetch('http://nexus_memory_keeper:9000/incidents/report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    incident_type: 'rate_limit_exceeded',
                    severity: 'medium',
                    agent_name: 'cortex',
                    description: `Rate limit exceeded for ${clientId} (${tier})`,
                    metadata: {
                        client_id: clientId,
                        tier: tier,
                        count: count,
                        limit: limit.points,
                    },
                }),
            }).catch(() => {});
            
            return res.status(429).json({
                error: 'Too Many Requests',
                message: `تجاوزت الحد الأقصى (${limit.points} طلب/${limit.duration}ث). تم حظرك لمدة ${limit.blockDuration} ثانية.`,
                limit: limit.points,
                tier: tier,
                blocked_for: limit.blockDuration,
            });
        }
        
        // Update counter
        if (count === 1) {
            await redis.setex(key, limit.duration, count);
        } else {
            await redis.set(key, count, 'KEEPTTL');
        }
        
        const remaining = limit.points - count;
        const ttl = await redis.ttl(key);
        
        // Add headers
        res.setHeader('X-RateLimit-Limit', limit.points);
        res.setHeader('X-RateLimit-Remaining', remaining);
        res.setHeader('X-RateLimit-Reset', Math.floor(Date.now() / 1000) + ttl);
        res.setHeader('X-RateLimit-Tier', tier);
        
        next();
    } catch (error) {
        console.error('[RATE LIMITER ERROR]', error);
        // Fail open (لا نمنع الطلب عند وجود خطأ في Redis)
        next();
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// 📊 Rate Limit Stats (إحصائيات)
// ═══════════════════════════════════════════════════════════════════════════
async function getRateLimitStats() {
    const keys = await redis.keys('ratelimit:*');
    const blocked = await redis.keys('blocked:*');
    
    return {
        active_limiters: keys.length,
        blocked_clients: blocked.length,
        tiers: RATE_LIMITS,
    };
}

module.exports = { rateLimiter, getRateLimitStats };
EOF

echo -e "${GREEN}✅ تم إنشاء Rate Limiting Middleware${NC}"

# ═══════════════════════════════════════════════════════════════════════════
# 2️⃣ تعديل Cortex لاستخدام الـ Middleware
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}2️⃣ تحديث Cortex لاستخدام Rate Limiting...${NC}"

echo -e "${YELLOW}ℹ️  يجب إضافة السطور التالية يدوياً إلى cortex/index.js:${NC}"
echo ""
echo "const { rateLimiter, getRateLimitStats } = require('./middleware/rateLimiter');"
echo ""
echo "// Apply to all routes"
echo "app.use(rateLimiter);"
echo ""
echo "// Stats endpoint"
echo "app.get('/rate-limit-stats', async (req, res) => {"
echo "    const stats = await getRateLimitStats();"
echo "    res.json(stats);"
echo "});"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 3️⃣ إنشاء NGINX Rate Limiting Config (طبقة إضافية)
# ═══════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}3️⃣ إضافة NGINX Rate Limiting (Layer 2)...${NC}"

mkdir -p /root/NEXUS_PRIME_UNIFIED/nginx/conf.d

cat > /root/NEXUS_PRIME_UNIFIED/nginx/conf.d/rate_limit.conf << 'EOF'
# ═══════════════════════════════════════════════════════════════════════════
# 🛡️ NEXUS PRIME - NGINX Rate Limiting Configuration
# ═══════════════════════════════════════════════════════════════════════════

# Define rate limit zones
limit_req_zone $binary_remote_addr zone=general:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=200r/m;
limit_req_zone $binary_remote_addr zone=ai:10m rate=20r/m;
limit_req_zone $binary_remote_addr zone=auth:10m rate=50r/m;

# Connection limits
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

# Apply to AI endpoints
location /ai/ {
    limit_req zone=ai burst=5 nodelay;
    limit_conn conn_limit 5;
    proxy_pass http://nexus_cortex:8005;
}

# Apply to API endpoints
location /api/ {
    limit_req zone=api burst=20 nodelay;
    limit_conn conn_limit 10;
    proxy_pass http://nexus_cortex:8005;
}

# Apply to Auth endpoints
location /auth/ {
    limit_req zone=auth burst=10 nodelay;
    limit_conn conn_limit 3;
    proxy_pass http://nexus_cortex:8005;
}
EOF

echo -e "${GREEN}✅ تم إنشاء NGINX Rate Limiting Config${NC}"

# ═══════════════════════════════════════════════════════════════════════════
# ✅ Summary
# ═══════════════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ تم إعداد Rate Limiting بنجاح!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📊 المستويات المطبقة:"
echo "   • Anonymous: 100 req/min"
echo "   • Authenticated: 500 req/min"
echo "   • Premium: 2000 req/min"
echo "   • AI Endpoints: 20 req/min"
echo ""
echo "🔄 الخطوات التالية:"
echo "   1. إضافة الـ Middleware يدوياً إلى cortex/index.js"
echo "   2. إعادة تشغيل Cortex: docker compose restart nexus_cortex"
echo "   3. اختبار: curl -I http://localhost:8005/api/health"
echo ""
