# استخدام Node.js 20
FROM node:20-alpine

# تحديد مجلد العمل
WORKDIR /app

# نسخ ملفات package أولاً للاستفادة من Docker layer caching
COPY package*.json ./

# تثبيت dependencies
RUN npm install --legacy-peer-deps

# نسخ باقي الملفات
COPY . .

# إنشاء environment.ts وبناء المشروع
RUN node scripts/set-env.cjs && npm run build

# فتح المنفذ
EXPOSE 8080

# تشغيل السيرفر
CMD ["node", "server.js"]
