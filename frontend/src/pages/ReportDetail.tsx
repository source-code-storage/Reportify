import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useReportStore } from '../stores/reportStore'
import { useAuthStore } from '../stores/authStore'
import NoteUpload from '../components/NoteUpload'
import RichTextEditor from '../components/RichTextEditor'
import NotesSearch from '../components/NotesSearch'
import ExportModal from '../components/ExportModal'
import apiService from '../services/api'

export default function ReportDetail() {
  const { reportId } = useParams<{ reportId: string }>()
  const navigate = useNavigate()
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)
  
  const { 
    currentReport, 
    currentSections, 
    isLoading, 
    error, 
    fetchReportById,
    updateSection,
    clearError 
  } = useReportStore()

  const [selectedSectionId, setSelectedSectionId] = useState<string | null>(null)
  const [editingContent, setEditingContent] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [activeTab, setActiveTab] = useState<'editor' | 'notes' | 'search'>('editor')
  const [showExportModal, setShowExportModal] = useState(false)

  useEffect(() => {
    if (reportId) {
      fetchReportById(reportId)
    }
  }, [reportId])

  useEffect(() => {
    if (currentSections.length > 0 && !selectedSectionId) {
      setSelectedSectionId(currentSections[0].id)
      setEditingContent(currentSections[0].content)
    }
  }, [currentSections])

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const handleSectionSelect = (sectionId: string) => {
    const section = currentSections.find(s => s.id === sectionId)
    if (section) {
      setSelectedSectionId(sectionId)
      setEditingContent(section.content)
    }
  }

  const handleSaveSection = async () => {
    if (!selectedSectionId) return
    
    setIsSaving(true)
    try {
      await updateSection(selectedSectionId, editingContent)
    } catch (error) {
      console.error('Failed to save section:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleGenerateContent = async () => {
    if (!selectedSection) return
    
    setIsGenerating(true)
    try {
      // Call real API for AI content generation
      const result = await apiService.generateContent(
        selectedSection.id,
        selectedSection.title
      )
      
      // Set the generated content
      setEditingContent(result.content)
      
      // Show success message with metadata
      console.log('Content generated successfully!')
      console.log(`Model: ${result.metadata.model}`)
      console.log(`Tokens: ${result.metadata.total_tokens}`)
      console.log(`Cost: $${result.metadata.estimated_cost}`)
      console.log(`Sources: ${result.sources.length}`)
      
    } catch (error: any) {
      console.error('Failed to generate content:', error)
      
      // Show user-friendly error message
      if (error.response?.status === 503) {
        alert('AI service is not available. Please check if OpenAI API key is configured.')
      } else if (error.response?.status === 404) {
        alert('No research notes found. Please upload some notes first.')
      } else {
        alert('Failed to generate content. Please try again.')
      }
    } finally {
      setIsGenerating(false)
    }
  }

  const handleImproveContent = async () => {
    if (!editingContent || !selectedSection) return
    
    setIsGenerating(true)
    try {
      // Call real API for content improvement
      const result = await apiService.improveContent(selectedSection.id)
      
      // Set the improved content
      setEditingContent(result.content)
      
      console.log('Content improved successfully!')
      console.log(`Cost: $${result.metadata.estimated_cost}`)
      
    } catch (error: any) {
      console.error('Failed to improve content:', error)
      alert('Failed to improve content. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleExpandContent = async () => {
    if (!editingContent || !selectedSection) return
    
    setIsGenerating(true)
    try {
      // Call real API for content expansion
      const result = await apiService.expandContent(selectedSection.id)
      
      // Set the expanded content
      setEditingContent(result.content)
      
      console.log('Content expanded successfully!')
      console.log(`Cost: $${result.metadata.estimated_cost}`)
      
    } catch (error: any) {
      console.error('Failed to expand content:', error)
      alert('Failed to expand content. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const calculateWordCount = (html: string) => {
    const text = html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()
    return text ? text.split(' ').length : 0
  }

  const handleInsertExcerpt = (excerpt: string, citation: string) => {
    // Insert excerpt with citation into the editor
    const insertText = `\n\n<p>${excerpt}</p>\n<p><em>${citation}</em></p>\n\n`
    setEditingContent(prev => prev + insertText)
    
    // Switch to editor tab to show the inserted content
    setActiveTab('editor')
    
    // Show success message (you could add a toast notification here)
    console.log('Excerpt inserted successfully')
  }

  const selectedSection = currentSections.find(s => s.id === selectedSectionId)

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
        return 'bg-blue-100 text-blue-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500'
    if (progress >= 50) return 'bg-blue-500'
    if (progress >= 25) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  if (isLoading && !currentReport) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
          <p className="mt-2 text-sm text-gray-600">Loading report...</p>
        </div>
      </div>
    )
  }

  if (!currentReport) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Report not found</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="mt-4 text-indigo-600 hover:text-indigo-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-gray-600 hover:text-gray-900"
              >
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <h1 className="text-xl font-bold text-gray-900">
                {currentReport.title}
              </h1>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(currentReport.status)}`}>
                {currentReport.status.replace('_', ' ')}
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">{user?.name}</span>
              <button
                onClick={() => setShowExportModal(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Export
              </button>
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex h-[calc(100vh-4rem)]">
        {/* Sidebar - Sections List */}
        <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
          <div className="p-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Sections</h2>
            
            {/* Progress Overview */}
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Overall Progress</span>
                <span className="text-sm font-medium text-gray-700">{currentReport.progress_percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                <div
                  className={`h-2 rounded-full transition-all ${getProgressColor(currentReport.progress_percentage)}`}
                  style={{ width: `${currentReport.progress_percentage}%` }}
                />
              </div>
              <div className="flex items-center justify-between text-xs text-gray-600">
                <span>{currentReport.total_word_count.toLocaleString()} words</span>
                <span>{currentSections.filter(s => s.is_completed).length}/{currentSections.length} completed</span>
              </div>
            </div>

            {/* Sections List */}
            <div className="space-y-2">
              {currentSections.length === 0 ? (
                <p className="text-sm text-gray-500 text-center py-4">
                  No sections yet. Upload a template to get started.
                </p>
              ) : (
                currentSections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => handleSectionSelect(section.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedSectionId === section.id
                        ? 'bg-indigo-50 border-2 border-indigo-500'
                        : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-sm font-medium text-gray-900 mb-1">
                          {section.title}
                        </h3>
                        <p className="text-xs text-gray-600">
                          {section.word_count} words
                        </p>
                      </div>
                      {section.is_completed && (
                        <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto">
          {error && (
            <div className="m-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
              <span className="block sm:inline">{error}</span>
              <button
                onClick={clearError}
                className="absolute top-0 bottom-0 right-0 px-4 py-3"
              >
                <span className="text-2xl">&times;</span>
              </button>
            </div>
          )}

          {/* Tabs */}
          <div className="border-b border-gray-200 bg-white">
            <nav className="flex space-x-8 px-6" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('editor')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'editor'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center">
                  <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Editor
                </div>
              </button>
              <button
                onClick={() => setActiveTab('search')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'search'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center">
                  <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Search Notes
                </div>
              </button>
              <button
                onClick={() => setActiveTab('notes')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'notes'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center">
                  <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  Notes & Files
                </div>
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          {activeTab === 'editor' && selectedSection ? (
            <div className="p-6">
              <div className="max-w-5xl mx-auto">
                {/* Section Header */}
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    {selectedSection.title}
                  </h2>
                  <p className="text-sm text-gray-600">
                    Section {currentSections.findIndex(s => s.id === selectedSectionId) + 1} of {currentSections.length}
                  </p>
                </div>

                {/* Rich Text Editor */}
                <RichTextEditor
                  content={editingContent}
                  onChange={setEditingContent}
                  onSave={handleSaveSection}
                  isSaving={isSaving}
                  wordCount={calculateWordCount(editingContent)}
                  onGenerateContent={handleGenerateContent}
                  onImproveContent={handleImproveContent}
                  onExpandContent={handleExpandContent}
                  isGenerating={isGenerating}
                />
              </div>
            </div>
          ) : activeTab === 'editor' ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center text-gray-500">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="mt-2">Select a section to start editing</p>
              </div>
            </div>
          ) : null}

          {/* Search Tab Content */}
          {activeTab === 'search' && (
            <div className="p-6">
              <div className="max-w-5xl mx-auto">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Search Research Notes
                  </h2>
                  <p className="text-sm text-gray-600">
                    Find relevant content from your uploaded notes and insert it into your report
                  </p>
                </div>

                <NotesSearch 
                  reportId={reportId || ''} 
                  onInsertExcerpt={handleInsertExcerpt}
                />
              </div>
            </div>
          )}

          {/* Notes Tab Content */}
          {activeTab === 'notes' && (
            <div className="p-6">
              <div className="max-w-4xl mx-auto">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Research Notes & Files
                  </h2>
                  <p className="text-sm text-gray-600">
                    Upload your research materials, notes, and reference documents
                  </p>
                </div>

                <NoteUpload onUploadComplete={() => {
                  // Refresh notes list when upload completes
                  console.log('Upload completed')
                }} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Export Modal */}
      <ExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
        reportId={reportId || ''}
        reportTitle={currentReport?.title || ''}
      />
    </div>
  )
}
