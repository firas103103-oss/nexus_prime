// Base44 API Client - منصة سيادي للنشر
// تكامل مع base44 backend API

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

class Base44Client {
  constructor() {
    this.baseURL = API_BASE_URL
    this.token = null
  }

  setToken(token) {
    this.token = token
    if (token) {
      localStorage.setItem('auth_token', token)
    } else {
      localStorage.removeItem('auth_token')
    }
  }

  getToken() {
    if (!this.token) {
      this.token = localStorage.getItem('auth_token')
    }
    return this.token
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const token = this.getToken()

    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'Unknown error' }))
        throw new Error(error.message || `HTTP ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // Authentication
  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })
  }

  async logout() {
    this.setToken(null)
    return Promise.resolve()
  }

  // Manuscripts
  async getManuscripts(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/manuscripts?${queryString}`)
  }

  async getManuscript(id) {
    return this.request(`/manuscripts/${id}`)
  }

  async createManuscript(data) {
    return this.request('/manuscripts', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateManuscript(id, data) {
    return this.request(`/manuscripts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteManuscript(id) {
    return this.request(`/manuscripts/${id}`, {
      method: 'DELETE',
    })
  }

  // File Upload
  async uploadFile(file, onProgress) {
    const formData = new FormData()
    formData.append('file', file)

    const token = this.getToken()
    const url = `${this.baseURL}/upload`

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable && onProgress) {
          const percentage = (e.loaded / e.total) * 100
          onProgress(percentage)
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText))
        } else {
          reject(new Error(`Upload failed: ${xhr.statusText}`))
        }
      })

      xhr.addEventListener('error', () => reject(new Error('Upload failed')))
      xhr.addEventListener('abort', () => reject(new Error('Upload cancelled')))

      xhr.open('POST', url)
      if (token) {
        xhr.setRequestHeader('Authorization', `Bearer ${token}`)
      }
      xhr.send(formData)
    })
  }

  // Processing Jobs
  async getProcessingJobs() {
    return this.request('/processing-jobs')
  }

  async getProcessingJob(id) {
    return this.request(`/processing-jobs/${id}`)
  }

  // LLM Integration
  async invokeLLM(prompt, options = {}) {
    return this.request('/llm/invoke', {
      method: 'POST',
      body: JSON.stringify({ prompt, ...options }),
    })
  }

  // Compliance
  async checkCompliance(manuscriptId) {
    return this.request(`/compliance/check/${manuscriptId}`)
  }

  async getComplianceRules() {
    return this.request('/compliance/rules')
  }

  // Cover Design
  async generateCover(manuscriptId, options = {}) {
    return this.request('/covers/generate', {
      method: 'POST',
      body: JSON.stringify({ manuscriptId, ...options }),
    })
  }

  async getCoverDesigns(manuscriptId) {
    return this.request(`/covers/${manuscriptId}`)
  }

  // Analytics
  async getDashboardStats() {
    return this.request('/analytics/dashboard')
  }
}

// Export singleton instance
const apiClient = new Base44Client()
export default apiClient
