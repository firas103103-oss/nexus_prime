import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth } from '@/api/postgresClient'
import apiClient from '@/api'
import { Button } from '@/Components/ui/button'
import { Input } from '@/Components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/Components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/Components/ui/tabs'
import { Alert, AlertDescription } from '@/Components/ui/alert'
import { Loader2, AlertCircle, CheckCircle2, Eye, EyeOff } from 'lucide-react'
import PageContainer from '@/Components/PageContainer'

/**
 * Authentication Page — Local Postgres / Demo Mode
 * No Supabase. Uses localStorage guest session.
 */
export default function AuthPage() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('login')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const [loginData, setLoginData] = useState({
    email: '',
    password: '',
    rememberMe: false
  })

  const [signupData, setSignupData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    acceptTerms: false
  })

  useEffect(() => {
    const checkUser = async () => {
      const user = await auth.getUser()
      if (user) navigate('/')
    }
    checkUser()
  }, [navigate])

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)
    try {
      if (!loginData.email || !loginData.password) {
        throw new Error('يرجى ملء جميع الحقول')
      }
      await apiClient.login({ email: loginData.email, password: loginData.password })
      setSuccess('تم تسجيل الدخول بنجاح!')
      setTimeout(() => navigate('/'), 800)
    } catch (err) {
      setError(err.message || 'فشل تسجيل الدخول')
    } finally {
      setLoading(false)
    }
  }

  const handleSignup = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)
    try {
      if (!signupData.email || !signupData.password || !signupData.fullName) {
        throw new Error('يرجى ملء جميع الحقول')
      }
      if (signupData.password !== signupData.confirmPassword) {
        throw new Error('كلمات المرور غير متطابقة')
      }
      if (signupData.password.length < 6) {
        throw new Error('يجب أن تكون كلمة المرور 6 أحرف على الأقل')
      }
      if (!signupData.acceptTerms) {
        throw new Error('يجب قبول الشروط والأحكام')
      }
      await apiClient.login({ email: signupData.email, password: signupData.password })
      setSuccess('تم إنشاء الحساب بنجاح!')
      setSignupData({ email: '', password: '', confirmPassword: '', fullName: '', acceptTerms: false })
      setTimeout(() => setActiveTab('login'), 1500)
    } catch (err) {
      setError(err.message || 'فشل إنشاء الحساب')
    } finally {
      setLoading(false)
    }
  }

  const handleGuest = async () => {
    try {
      await apiClient.login({ email: 'guest@local', password: 'guest' })
      navigate('/')
    } catch (_) {}
  }

  return (
    <PageContainer className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Shadow Seven</h1>
          <p className="text-slate-400">منصة النشر الذكية — محليّ</p>
        </div>

        {error && (
          <Alert className="mb-4 bg-red-500/10 border-red-500/50">
            <AlertCircle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-500">{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="mb-4 bg-green-500/10 border-green-500/50">
            <CheckCircle2 className="h-4 w-4 text-green-500" />
            <AlertDescription className="text-green-500">{success}</AlertDescription>
          </Alert>
        )}

        <Card className="bg-slate-800 border-slate-700">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 bg-slate-900 border-b border-slate-700">
              <TabsTrigger value="login" className="data-[state=active]:bg-slate-700">دخول</TabsTrigger>
              <TabsTrigger value="signup" className="data-[state=active]:bg-slate-700">إنشاء حساب</TabsTrigger>
              <TabsTrigger value="recovery" className="data-[state=active]:bg-slate-700">استرجاع</TabsTrigger>
            </TabsList>

            <TabsContent value="login" className="space-y-4 p-6">
              <CardHeader className="px-0 pt-0">
                <CardTitle className="text-white">تسجيل الدخول</CardTitle>
                <CardDescription>أدخل بيانات حسابك أو استمر كضيف</CardDescription>
              </CardHeader>

              <Button
                onClick={handleGuest}
                variant="outline"
                className="w-full mb-4 border-slate-600 text-slate-300 hover:bg-slate-700"
              >
                دخول كضيف (بدون حساب)
              </Button>

              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">البريد الإلكتروني</label>
                  <Input
                    type="email"
                    placeholder="your@email.com"
                    value={loginData.email}
                    onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                    disabled={loading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">كلمة المرور</label>
                  <div className="relative">
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      placeholder="••••••••"
                      value={loginData.password}
                      onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                      className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                      disabled={loading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>
                <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white" disabled={loading}>
                  {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />جاري التسجيل...</> : 'دخول'}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="signup" className="space-y-4 p-6">
              <CardHeader className="px-0 pt-0">
                <CardTitle className="text-white">إنشاء حساب جديد</CardTitle>
                <CardDescription>انضم إلى منصة النشر الذكية</CardDescription>
              </CardHeader>

              <form onSubmit={handleSignup} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">الاسم الكامل</label>
                  <Input
                    type="text"
                    placeholder="أحمد محمد"
                    value={signupData.fullName}
                    onChange={(e) => setSignupData({ ...signupData, fullName: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                    disabled={loading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">البريد الإلكتروني</label>
                  <Input
                    type="email"
                    placeholder="your@email.com"
                    value={signupData.email}
                    onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                    disabled={loading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">كلمة المرور</label>
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    value={signupData.password}
                    onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                    disabled={loading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">تأكيد كلمة المرور</label>
                  <Input
                    type={showConfirmPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    value={signupData.confirmPassword}
                    onChange={(e) => setSignupData({ ...signupData, confirmPassword: e.target.value })}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                    disabled={loading}
                  />
                </div>
                <div className="flex items-start">
                  <input
                    type="checkbox"
                    id="acceptTerms"
                    checked={signupData.acceptTerms}
                    onChange={(e) => setSignupData({ ...signupData, acceptTerms: e.target.checked })}
                    className="rounded border-slate-600 mt-1"
                    disabled={loading}
                  />
                  <label htmlFor="acceptTerms" className="ml-2 text-sm text-slate-400">أوافق على الشروط والأحكام</label>
                </div>
                <Button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white" disabled={loading}>
                  {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />جاري الإنشاء...</> : 'إنشاء حساب'}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="recovery" className="space-y-4 p-6">
              <CardHeader className="px-0 pt-0">
                <CardTitle className="text-white">استرجاع كلمة المرور</CardTitle>
                <CardDescription>وضع التشغيل المحلي: أنشئ حساباً جديداً أو استخدم دخول كضيف</CardDescription>
              </CardHeader>
              <Button onClick={() => setActiveTab('signup')} className="w-full">
                إنشاء حساب جديد
              </Button>
            </TabsContent>
          </Tabs>
        </Card>

        <p className="text-center text-slate-400 text-sm mt-6">© 2026 Shadow Seven — MRF103</p>
      </div>
    </PageContainer>
  )
}
