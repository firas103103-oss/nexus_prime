# Railway Deployment Configuration

## 🚀 Live URL
https://777-production-a3a7.up.railway.app

## ⚙️ Configuration Status

### ✅ Completed
- [x] GitHub repository connected
- [x] Railway deployment successful
- [x] Port configured to 8080
- [x] Express server ready
- [x] Build scripts configured

### 🔧 Required: Supabase Configuration

**CRITICAL: Update Supabase Auth URLs**

Go to [Supabase Dashboard](https://app.supabase.com) and update:

1. **Project Settings** > **Authentication** > **URL Configuration**

2. Add these URLs:

   **Site URL:**
   ```
   https://777-production-a3a7.up.railway.app
   ```

   **Redirect URLs (Add to list):**
   ```
   https://777-production-a3a7.up.railway.app
   https://777-production-a3a7.up.railway.app/**
   ```

3. **Save Changes**

### 📋 Railway Environment Variables

Ensure these are set in Railway Dashboard > Variables:

```env
SUPABASE_URL=https://udcwitnnogxrvoxefrge.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVkY3dpdG5ub2d4cnZveGVmcmdlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzMTUwNTcsImV4cCI6MjA4MDg5MTA1N30.SfPkepVomW4bwFSi1lhS81d-nSlNgYQ3jhjtHri8hhg
GEMINI_API_KEY=AIzaSyCyHegfv5nzDNx-CaxZ2mI3daAukizoYUo
PORT=8080
```

## 🧪 Testing

1. Open: https://777-production-a3a7.up.railway.app
2. You should see the login page
3. Enter your email
4. Check email for Magic Link
5. Click link to authenticate

## 🔒 Security Notes

- ✅ `.env` file excluded from git
- ✅ Environment variables injected at build time
- ✅ Supabase keys properly configured
- ✅ No service role key exposed in frontend

## 📊 Deployment Info

- **Platform:** Railway
- **Port:** 8080
- **Build Command:** `npm run build`
- **Start Command:** `npm start`
- **Node Version:** Auto-detected
- **Framework:** Angular 21 + Express

---

**Status:** 🟡 Waiting for Supabase URL configuration
**Next Step:** Update Supabase Dashboard with Railway URL
