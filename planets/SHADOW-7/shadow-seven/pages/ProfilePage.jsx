import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth } from '@/api/postgresClient'
import apiClient from '@/api'
import { Button } from '@/Components/ui/button'
import { Input } from '@/Components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/Components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/Components/ui/tabs'
import { Alert, AlertDescription } from '@/Components/ui/alert'
import { Loader2, AlertCircle, CheckCircle2, LogOut } from 'lucide-react'
import PageContainer from '@/Components/PageContainer'

const PROFILE_KEY = 'shadow7_profile'
const SETTINGS_KEY = 'shadow7_settings'

export default function ProfilePage() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [profileForm, setProfileForm] = useState({
    full_name: '',
    bio: '',
    avatar_url: ''
  })

  const [settingsForm, setSettingsForm] = useState({
    language: 'ar',
    theme: 'dark',
    notifications_enabled: true,
    email_notifications: true,
    marketing_emails: false
  })

  useEffect(() => {
    const load = async () => {
      try {
        const u = await auth.getUser()
        if (!u) {
          navigate('/login')
          return
        }
        setUser(u)
        const p = JSON.parse(localStorage.getItem(PROFILE_KEY) || '{}')
        setProfileForm({ full_name: p.full_name || '', bio: p.bio || '', avatar_url: p.avatar_url || '' })
        const s = JSON.parse(localStorage.getItem(SETTINGS_KEY) || '{}')
        setSettingsForm({ ...settingsForm, ...s })
      } catch (_) {
        navigate('/login')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [navigate])

  const handleProfileUpdate = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      localStorage.setItem(PROFILE_KEY, JSON.stringify(profileForm))
      await auth.updateUser(profileForm)
      setSuccess('تم تحديث الملف الشخصي بنجاح')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleSettingsUpdate = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(settingsForm))
      setSuccess('تم تحديث الإعدادات بنجاح')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleLogout = async () => {
    await apiClient.logout()
    navigate('/login')
  }

  if (loading) {
    return (
      <PageContainer className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </PageContainer>
    )
  }

  return (
    <PageContainer className="py-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">الملف الشخصي</h1>
            <p className="text-slate-400 mt-2">إدارة حسابك والإعدادات — محلي</p>
          </div>
          <Button onClick={handleLogout} variant="destructive" className="flex items-center gap-2">
            <LogOut size={18} />
            تسجيل الخروج
          </Button>
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

        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="bg-slate-800 border border-slate-700">
            <TabsTrigger value="profile">الملف الشخصي</TabsTrigger>
            <TabsTrigger value="settings">الإعدادات</TabsTrigger>
          </TabsList>

          <TabsContent value="profile">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">معلومات الملف الشخصي</CardTitle>
                <CardDescription>تحديث معلومات حسابك (محفوظة محلياً)</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleProfileUpdate} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">البريد الإلكتروني</label>
                    <Input
                      type="email"
                      value={user?.email || ''}
                      disabled
                      className="bg-slate-700 border-slate-600 text-slate-400"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">الاسم الكامل</label>
                    <Input
                      type="text"
                      value={profileForm.full_name}
                      onChange={(e) => setProfileForm({ ...profileForm, full_name: e.target.value })}
                      className="bg-slate-700 border-slate-600 text-white"
                      disabled={saving}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">السيرة الذاتية</label>
                    <textarea
                      value={profileForm.bio}
                      onChange={(e) => setProfileForm({ ...profileForm, bio: e.target.value })}
                      className="w-full bg-slate-700 border border-slate-600 text-white rounded-md p-3"
                      rows="4"
                      disabled={saving}
                    />
                  </div>
                  <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={saving}>
                    {saving ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />جاري الحفظ...</> : 'حفظ التغييرات'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">الإعدادات</CardTitle>
                <CardDescription>تخصيص تجربتك</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSettingsUpdate} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">اللغة</label>
                    <select
                      value={settingsForm.language}
                      onChange={(e) => setSettingsForm({ ...settingsForm, language: e.target.value })}
                      className="w-full bg-slate-700 border border-slate-600 text-white rounded-md p-2"
                      disabled={saving}
                    >
                      <option value="ar">العربية</option>
                      <option value="en">English</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">المظهر</label>
                    <select
                      value={settingsForm.theme}
                      onChange={(e) => setSettingsForm({ ...settingsForm, theme: e.target.value })}
                      className="w-full bg-slate-700 border border-slate-600 text-white rounded-md p-2"
                      disabled={saving}
                    >
                      <option value="light">فاتح</option>
                      <option value="dark">غامق</option>
                      <option value="auto">تلقائي</option>
                    </select>
                  </div>
                  <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={saving}>
                    {saving ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />جاري الحفظ...</> : 'حفظ الإعدادات'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </PageContainer>
  )
}
