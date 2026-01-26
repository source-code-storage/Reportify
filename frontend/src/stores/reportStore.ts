import { create } from 'zustand'
import axios from 'axios'
import { useAuthStore } from './authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Report {
  id: string
  title: string
  description: string
  created_at: string
  updated_at: string
  progress_percentage: number
  total_word_count: number
  status: 'draft' | 'in_progress' | 'completed'
  user_id: string
}

export interface ReportSection {
  id: string
  report_id: string
  title: string
  content: string
  order: number
  word_count: number
  is_completed: boolean
}

interface ReportState {
  reports: Report[]
  currentReport: Report | null
  currentSections: ReportSection[]
  isLoading: boolean
  error: string | null

  // Actions
  fetchReports: () => Promise<void>
  fetchReportById: (reportId: string) => Promise<void>
  createReport: (title: string, description: string, templateFile?: File) => Promise<Report>
  updateReport: (reportId: string, data: Partial<Report>) => Promise<void>
  deleteReport: (reportId: string) => Promise<void>
  updateSection: (sectionId: string, content: string) => Promise<void>
  clearError: () => void
}

export const useReportStore = create<ReportState>((set, get) => ({
  reports: [],
  currentReport: null,
  currentSections: [],
  isLoading: false,
  error: null,

  clearError: () => set({ error: null }),

  fetchReports: async () => {
    set({ isLoading: true, error: null })
    try {
      const { accessToken } = useAuthStore.getState()
      const response = await axios.get(`${API_URL}/reports`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      set({ reports: response.data, isLoading: false })
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch reports',
        isLoading: false 
      })
    }
  },

  fetchReportById: async (reportId: string) => {
    set({ isLoading: true, error: null })
    try {
      const { accessToken } = useAuthStore.getState()
      const response = await axios.get(`${API_URL}/reports/${reportId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      set({ 
        currentReport: response.data,
        currentSections: response.data.sections || [],
        isLoading: false 
      })
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch report',
        isLoading: false 
      })
    }
  },

  createReport: async (title: string, description: string, templateFile?: File) => {
    set({ isLoading: true, error: null })
    try {
      const { accessToken } = useAuthStore.getState()
      
      console.log('Creating report...', { title, description, hasTemplate: !!templateFile })
      
      // Create report first
      const response = await axios.post(`${API_URL}/reports`, 
        {
          title,
          description
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        }
      )

      const newReport = response.data
      console.log('Report created:', newReport)
      
      set(state => ({ 
        reports: [newReport, ...state.reports],
        isLoading: false 
      }))
      
      // Upload template if provided
      if (templateFile) {
        console.log('Uploading template file:', templateFile.name)
        try {
          const formData = new FormData()
          formData.append('report_id', newReport.id.toString())
          formData.append('file', templateFile)
          
          const uploadResponse = await axios.post(`${API_URL}/uploads/template`, formData, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          })
          
          console.log('Template uploaded successfully!', uploadResponse.data)
        } catch (uploadError: any) {
          console.error('Failed to upload template:', uploadError)
          console.error('Upload error details:', uploadError.response?.data)
          // Don't fail the whole operation if template upload fails
          set({ 
            error: 'Report created but template upload failed: ' + (uploadError.response?.data?.detail || uploadError.message)
          })
        }
      }
      
      return newReport
    } catch (error: any) {
      console.error('Failed to create report:', error)
      set({ 
        error: error.response?.data?.detail || 'Failed to create report',
        isLoading: false 
      })
      throw error
    }
  },

  updateReport: async (reportId: string, data: Partial<Report>) => {
    set({ isLoading: true, error: null })
    try {
      const { accessToken } = useAuthStore.getState()
      const response = await axios.put(`${API_URL}/reports/${reportId}`, data, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })

      set(state => ({
        reports: state.reports.map(r => r.id === reportId ? response.data : r),
        currentReport: state.currentReport?.id === reportId ? response.data : state.currentReport,
        isLoading: false
      }))
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to update report',
        isLoading: false 
      })
    }
  },

  deleteReport: async (reportId: string) => {
    set({ isLoading: true, error: null })
    try {
      const { accessToken } = useAuthStore.getState()
      await axios.delete(`${API_URL}/reports/${reportId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })

      set(state => ({
        reports: state.reports.filter(r => r.id !== reportId),
        isLoading: false
      }))
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to delete report',
        isLoading: false 
      })
    }
  },

  updateSection: async (sectionId: string, content: string) => {
    try {
      const { accessToken } = useAuthStore.getState()
      const { currentReport } = get()
      
      if (!currentReport) return

      const response = await axios.put(
        `${API_URL}/reports/${currentReport.id}/sections/${sectionId}`,
        { content },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )

      set(state => ({
        currentSections: state.currentSections.map(s => 
          s.id === sectionId ? response.data : s
        )
      }))
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to update section'
      })
    }
  },
}))
