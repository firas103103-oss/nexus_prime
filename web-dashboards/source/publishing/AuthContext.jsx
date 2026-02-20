import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { supabase } from '@/api/supabaseClient'

const AuthContext = createContext(null)

const TOKEN_KEY = 'nexus_auth_token'
const USER_KEY = 'nexus_auth_user'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const savedToken = localStorage.getItem(TOKEN_KEY)
    const savedUser = localStorage.getItem(USER_KEY)
    
    if (savedToken && savedUser) {
      supabase.rpc('validate_session', { p_token: savedToken })
        .then(({ data, error }) => {
          if (!error && data && data.valid) {
            setUser(data.user)
            localStorage.setItem(USER_KEY, JSON.stringify(data.user))
          } else {
            localStorage.removeItem(TOKEN_KEY)
            localStorage.removeItem(USER_KEY)
            setUser(null)
          }
        })
        .catch(() => {
          try { setUser(JSON.parse(savedUser)) } catch { 
            localStorage.removeItem(TOKEN_KEY)
            localStorage.removeItem(USER_KEY)
          }
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = useCallback(async (email, password) => {
    try {
      const { data, error } = await supabase.rpc('login', { p_email: email, p_password: password })
      if (error) throw new Error(error.message)
      if (data.error) throw new Error(data.error)
      localStorage.setItem(TOKEN_KEY, data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      setUser(data.user)
      return { success: true, user: data.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }, [])

  const register = useCallback(async (email, password, fullName) => {
    try {
      const { data, error } = await supabase.rpc('register', { p_email: email, p_password: password, p_full_name: fullName || 'user' })
      if (error) throw new Error(error.message)
      if (data.error) throw new Error(data.error)
      localStorage.setItem(TOKEN_KEY, data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      setUser(data.user)
      return { success: true, user: data.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }, [])

  const logout = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token) { try { await supabase.rpc('logout', { p_token: token }) } catch {} }
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setUser(null)
  }, [])

  const updateProfile = useCallback(async (updates) => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) return { success: false, error: 'Not authenticated' }
    try {
      const { data, error } = await supabase.rpc('update_profile', { p_token: token, p_full_name: updates.full_name || null, p_avatar_url: updates.avatar_url || null })
      if (error) throw new Error(error.message)
      if (data.error) throw new Error(data.error)
      setUser(data.user)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      return { success: true, user: data.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }, [])

  const getToken = useCallback(() => localStorage.getItem(TOKEN_KEY), [])

  const value = { user, login, register, logout, updateProfile, getToken, loading, isAuthenticated: !!user, isAdmin: user?.role === 'admin' }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
