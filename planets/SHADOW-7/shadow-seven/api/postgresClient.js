/**
 * Local Postgres API Client — replaces Supabase
 * Uses shadow7_api (/api/shadow7/) and PostgREST (/api/) for all data operations.
 */

const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '') || ''

function apiUrl(path) {
  const base = API_BASE || ''
  const p = path.startsWith('/') ? path : `/${path}`
  return base ? `${base}${p}` : p
}

async function fetchJson(url, opts = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || err.message || res.statusText)
  }
  return res.json()
}

// Database Helpers — via shadow7_api
export const db = {
  manuscripts: {
    list: async (orderBy = '-created_at', limit) => {
      const params = new URLSearchParams({ order_by: orderBy })
      if (limit) params.set('limit', limit)
      const url = apiUrl(`/api/shadow7/manuscripts?${params}`)
      return fetchJson(url)
    },

    get: async (id) => {
      const url = apiUrl(`/api/shadow7/manuscripts/${id}`)
      return fetchJson(url)
    },

    filter: async (filters) => {
      const data = await fetchJson(apiUrl('/api/shadow7/manuscripts'))
      if (!filters || !Object.keys(filters).length) return data
      return data.filter(m => Object.entries(filters).every(([k, v]) => m[k] === v))
    },

    create: async (data) => {
      if (data.file) {
        const form = new FormData()
        form.append('file', data.file)
        form.append('title', data.title || 'Untitled')
        form.append('content', data.content || '')
        form.append('word_count', String(data.word_count || 0))
        form.append('metadata', JSON.stringify(data.metadata || {}))
        const res = await fetch(apiUrl('/api/shadow7/manuscripts/upload'), { method: 'POST', body: form })
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw new Error(err.detail || res.statusText)
        }
        return res.json()
      }
      return fetchJson(apiUrl('/api/shadow7/manuscripts'), {
        method: 'POST',
        body: JSON.stringify(data)
      })
    },

    update: async (id, data) => {
      const url = apiUrl(`/api/shadow7/manuscripts/${id}`)
      return fetchJson(url, { method: 'PATCH', body: JSON.stringify(data) })
    },

    delete: async (id) => {
      const url = apiUrl(`/api/shadow7/manuscripts/${id}`)
      await fetch(url, { method: 'DELETE' })
      return { success: true }
    }
  },

  complianceRules: {
    list: async () => [],
    create: async () => ({}),
    update: async () => ({}),
    delete: async () => ({ success: true })
  },

  coverDesigns: {
    create: async (data) => ({ ...data, id: crypto.randomUUID() })
  },

  processingJobs: {
    filter: async () => []
  }
}

// Auth — demo mode: no real auth, localStorage guest session
const GUEST_KEY = 'shadow7_guest_user'

export const auth = {
  getUser: async () => {
    const stored = localStorage.getItem(GUEST_KEY)
    if (stored) {
      try {
        return JSON.parse(stored)
      } catch (_) {}
    }
    return null
  },

  signIn: async (email, password) => {
    // Demo mode: accept any email, store as guest
    const user = { id: crypto.randomUUID(), email: email || 'guest@local', user_metadata: {} }
    localStorage.setItem(GUEST_KEY, JSON.stringify(user))
    return { user, session: {} }
  },

  signUp: async (email, password, metadata = {}) => {
    const user = { id: crypto.randomUUID(), email: email || 'guest@local', user_metadata: metadata }
    localStorage.setItem(GUEST_KEY, JSON.stringify(user))
    return { user, session: {} }
  },

  signOut: async () => {
    localStorage.removeItem(GUEST_KEY)
  },

  updateUser: async (updates) => {
    const stored = localStorage.getItem(GUEST_KEY)
    if (!stored) return null
    const user = JSON.parse(stored)
    Object.assign(user, updates)
    localStorage.setItem(GUEST_KEY, JSON.stringify(user))
    return { data: user }
  }
}

// Storage — via shadow7_api upload (no Supabase buckets)
export const storage = {
  uploadFile: async (bucket, path, file) => {
    const form = new FormData()
    form.append('file', file)
    form.append('title', file.name || 'upload')
    form.append('content', '')
    form.append('word_count', '0')
    form.append('metadata', '{}')
    const url = apiUrl('/api/shadow7/manuscripts/upload')
    const res = await fetch(url, { method: 'POST', body: form })
    if (!res.ok) throw new Error('فشل رفع الملف')
    const data = await res.json()
    return { file_url: data.file_path || path, path: data.file_path || path }
  },

  deleteFile: async () => {},
  getPublicUrl: (bucket, path) => path
}

// No supabase instance — for components that check supabase
export const supabase = null

export default { db, auth, storage, supabase }
