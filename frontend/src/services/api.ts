/**
 * API Service
 * Centralized API calls to the backend
 */
import axios, { AxiosInstance } from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

class APIService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add request interceptor to include auth token
    this.client.interceptors.request.use(
      (config) => {
        const { accessToken } = useAuthStore.getState()
        if (accessToken) {
          config.headers.Authorization = `Bearer ${accessToken}`
        }
        
        // If the data is FormData, remove Content-Type to let browser set it with boundary
        if (config.data instanceof FormData) {
          delete config.headers['Content-Type']
        }
        
        return config
      },
      (error) => Promise.reject(error)
    )

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          const { logout } = useAuthStore.getState()
          logout()
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Reports API
  async getReports() {
    const response = await this.client.get('/reports')
    return response.data
  }

  async getReport(reportId: string) {
    const response = await this.client.get(`/reports/${reportId}`)
    return response.data
  }

  async createReport(data: { title: string; description: string }) {
    const response = await this.client.post('/reports', data)
    return response.data
  }

  async updateReport(reportId: string, data: any) {
    const response = await this.client.put(`/reports/${reportId}`, data)
    return response.data
  }

  async deleteReport(reportId: string) {
    await this.client.delete(`/reports/${reportId}`)
  }

  async createSection(reportId: string, data: { title: string; order: number }) {
    const response = await this.client.post(`/reports/${reportId}/sections`, null, {
      params: data
    })
    return response.data
  }

  async updateSection(reportId: string, sectionId: string, data: any) {
    const response = await this.client.put(`/reports/${reportId}/sections/${sectionId}`, data)
    return response.data
  }

  // Template Upload API
  async uploadTemplate(reportId: string, file: File) {
    const formData = new FormData()
    formData.append('report_id', reportId)
    formData.append('file', file)

    const response = await this.client.post('/uploads/template', formData)
    return response.data
  }

  // Notes API
  async uploadNote(reportId: string, file: File) {
    const formData = new FormData()
    formData.append('report_id', reportId)
    formData.append('file', file)

    const response = await this.client.post('/notes/upload', formData)
    return response.data
  }

  async getNotes(reportId: string) {
    const response = await this.client.get('/notes', {
      params: { report_id: reportId }
    })
    return response.data
  }

  async getNote(noteId: string) {
    const response = await this.client.get(`/notes/${noteId}`)
    return response.data
  }

  async deleteNote(noteId: string) {
    await this.client.delete(`/notes/${noteId}`)
  }

  // AI Content Generation API
  async generateContent(sectionId: string, sectionDescription?: string) {
    const response = await this.client.post('/content/generate', {
      section_id: parseInt(sectionId),
      section_description: sectionDescription || ''
    })
    return response.data
  }

  async improveContent(sectionId: string) {
    const response = await this.client.post('/content/improve', {
      section_id: parseInt(sectionId)
    })
    return response.data
  }

  async expandContent(sectionId: string) {
    const response = await this.client.post('/content/expand', {
      section_id: parseInt(sectionId)
    })
    return response.data
  }

  async searchNotes(query: string, reportId: string, limit: number = 5) {
    const response = await this.client.get('/content/search', {
      params: { query, report_id: reportId, limit }
    })
    return response.data
  }
}

export const apiService = new APIService()
export default apiService
