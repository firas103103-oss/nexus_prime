// API Client for Backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8085/api';

interface APIOptions {
  method?: string;
  body?: any;
  headers?: Record<string, string>;
  token?: string;
}

class APIClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    // Load token from localStorage
    this.token = localStorage.getItem('auth_token');
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  private async request(endpoint: string, options: APIOptions = {}) {
    const { method = 'GET', body, headers = {}, token } = options;

    const config: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };

    // Add auth token
    const authToken = token || this.token;
    if (authToken) {
      config.headers = {
        ...config.headers,
        'Authorization': `Bearer ${authToken}`,
      };
    }

    // Add body for non-GET requests
    if (body && method !== 'GET') {
      config.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Request failed');
      }

      return await response.json();
    } catch (error: any) {
      console.error(`API Error [${method} ${endpoint}]:`, error);
      throw error;
    }
  }

  // Gemini API Proxy
  async validateText(text: string, language: string) {
    return this.request('/gemini/validate', {
      method: 'POST',
      body: { text, language },
    });
  }

  async analyzeManuscript(text: string, metadata: any) {
    return this.request('/gemini/analyze', {
      method: 'POST',
      body: { text, metadata },
    });
  }

  async editText(text: string, instructions: string, metadata: any) {
    return this.request('/gemini/edit', {
      method: 'POST',
      body: { text, instructions, metadata },
    });
  }

  async generateCover(description: string, metadata: any) {
    return this.request('/gemini/generate-cover', {
      method: 'POST',
      body: { description, metadata },
    });
  }

  // Manuscripts API
  async getManuscripts(userId?: string) {
    const headers: Record<string, string> = {};
    if (userId) {
      headers['x-user-id'] = userId;
    }
    return this.request('/manuscripts', { headers });
  }

  async getManuscript(id: string) {
    return this.request(`/manuscripts/${id}`);
  }

  async createManuscript(data: {
    title: string;
    author?: string;
    genre?: string;
    language?: string;
    originalText: string;
    wordCount?: number;
    metadata?: any;
  }) {
    const userId = localStorage.getItem('user_id') || 'anonymous';
    return this.request('/manuscripts', {
      method: 'POST',
      body: data,
      headers: { 'x-user-id': userId },
    });
  }

  async updateManuscript(id: string, updates: any) {
    const userId = localStorage.getItem('user_id');
    return this.request(`/manuscripts/${id}`, {
      method: 'PATCH',
      body: updates,
      headers: userId ? { 'x-user-id': userId } : {},
    });
  }

  async startProcessing(id: string, step: string, options?: any) {
    const userId = localStorage.getItem('user_id') || 'anonymous';
    return this.request(`/manuscripts/${id}/process`, {
      method: 'POST',
      body: { step, options },
      headers: { 'x-user-id': userId },
    });
  }

  // Auth API
  async signup(email: string, password: string, name?: string) {
    const response = await this.request('/auth/signup', {
      method: 'POST',
      body: { email, password, name },
    });
    
    if (response.session?.access_token) {
      this.setToken(response.session.access_token);
      if (response.user?.id) {
        localStorage.setItem('user_id', response.user.id);
      }
    }
    
    return response;
  }

  async login(email: string, password: string) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: { email, password },
    });
    
    if (response.session?.access_token) {
      this.setToken(response.session.access_token);
      if (response.user?.id) {
        localStorage.setItem('user_id', response.user.id);
      }
    }
    
    return response;
  }

  async logout() {
    const response = await this.request('/auth/logout', {
      method: 'POST',
    });
    
    this.setToken(null);
    localStorage.removeItem('user_id');
    
    return response;
  }

  async getCurrentUser() {
    return this.request('/auth/user');
  }

  async refreshToken(refreshToken: string) {
    const response = await this.request('/auth/refresh', {
      method: 'POST',
      body: { refresh_token: refreshToken },
    });
    
    if (response.session?.access_token) {
      this.setToken(response.session.access_token);
    }
    
    return response;
  }
}

// Export singleton instance
export const apiClient = new APIClient(API_BASE_URL);

export default apiClient;
