import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface User {
  id: string
  email: string
  name: string
  created_at: string
  is_active: boolean
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshAccessToken: () => Promise<void>
  getCurrentUser: () => Promise<void>
  setTokens: (accessToken: string, refreshToken: string) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,

      setTokens: (accessToken: string, refreshToken: string) => {
        set({ accessToken, refreshToken, isAuthenticated: true })
      },

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await axios.post(`${API_URL}/auth/login`, {
            email,
            password,
          })

          const { access_token, refresh_token } = response.data
          set({
            accessToken: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          // Fetch user data after login
          await get().getCurrentUser()
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (name: string, email: string, password: string) => {
        set({ isLoading: true })
        try {
          // Register user
          await axios.post(`${API_URL}/auth/register`, {
            name,
            email,
            password,
          })

          // Auto-login after registration
          await get().login(email, password)
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: async () => {
        const { accessToken } = get()
        
        try {
          if (accessToken) {
            await axios.post(
              `${API_URL}/auth/logout`,
              {},
              {
                headers: {
                  Authorization: `Bearer ${accessToken}`,
                },
              }
            )
          }
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          // Clear state regardless of API call success
          set({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
          })
        }
      },

      refreshAccessToken: async () => {
        const { refreshToken } = get()
        
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })

          const { access_token, refresh_token: new_refresh_token } = response.data
          set({
            accessToken: access_token,
            refreshToken: new_refresh_token,
          })
        } catch (error) {
          // If refresh fails, logout user
          set({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
          })
          throw error
        }
      },

      getCurrentUser: async () => {
        const { accessToken } = get()
        
        if (!accessToken) {
          throw new Error('No access token available')
        }

        try {
          const response = await axios.get(`${API_URL}/auth/me`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          })

          set({ user: response.data })
        } catch (error) {
          throw error
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Axios interceptor for automatic token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        await useAuthStore.getState().refreshAccessToken()
        const { accessToken } = useAuthStore.getState()
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${accessToken}`
        return axios(originalRequest)
      } catch (refreshError) {
        // Refresh failed, logout user
        useAuthStore.getState().logout()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)
