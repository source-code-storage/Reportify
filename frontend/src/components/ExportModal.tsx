import { useState, useEffect } from 'react'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface ExportModalProps {
  isOpen: boolean
  onClose: () => void
  reportId: string
  reportTitle: string
}

type ExportFormat = 'pdf' | 'docx'
type ExportStatus = 'idle' | 'preparing' | 'exporting' | 'completed' | 'error'

export default function ExportModal({ isOpen, onClose, reportId, reportTitle }: ExportModalProps) {
  const [selectedFormat, setSelectedFormat] = useState<ExportFormat>('pdf')
  const [exportStatus, setExportStatus] = useState<ExportStatus>('idle')
  const [progress, setProgress] = useState(0)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [fileBlob, setFileBlob] = useState<Blob | null>(null)
  
  // Get token from auth store
  const accessToken = useAuthStore((state) => state.accessToken)

  useEffect(() => {
    if (!isOpen) {
      // Reset state when modal closes
      setExportStatus('idle')
      setProgress(0)
      setDownloadUrl(null)
      setErrorMessage(null)
      setFileBlob(null)
    }
  }, [isOpen])

  const handleExport = async () => {
    setExportStatus('preparing')
    setProgress(10)
    setErrorMessage(null)

    try {
      // Check if user is authenticated
      if (!accessToken) {
        throw new Error('Not authenticated')
      }

      console.log('Starting export:', { reportId, selectedFormat, token: accessToken.substring(0, 20) + '...' })

      setProgress(30)
      setExportStatus('exporting')

      // Call the backend API to export
      const url = `${API_URL}/export/${selectedFormat}`
      console.log('Export URL:', url)
      console.log('Report ID:', reportId)

      const response = await axios.post(
        url,
        null,
        {
          params: { report_id: reportId },
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
          responseType: 'blob', // Important for file download
          onDownloadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
              setProgress(30 + (percentCompleted * 0.6)) // 30% to 90%
            }
          }
        }
      )

      console.log('Export response received:', response.status, response.headers['content-type'])
      setProgress(100)

      // Create blob URL for download
      const blob = new Blob([response.data], {
        type: selectedFormat === 'pdf' 
          ? 'application/pdf' 
          : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      })
      
      setFileBlob(blob)
      const blobUrl = window.URL.createObjectURL(blob)
      setDownloadUrl(blobUrl)
      setExportStatus('completed')

      console.log('Export completed successfully')
      
    } catch (error: any) {
      console.error('Export error details:', error)
      console.error('Error response:', error.response?.data)
      console.error('Error status:', error.response?.status)
      
      setExportStatus('error')
      const errorMsg = error.response?.data?.detail || error.message || 'Export failed. Please try again.'
      setErrorMessage(errorMsg)
      console.error('Export error:', error)
    }
  }

  const handleDownload = () => {
    if (!downloadUrl || !fileBlob) {
      console.error('No download URL or file blob available')
      return
    }

    // Create a temporary anchor element and trigger download
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = `${reportTitle}.${selectedFormat}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // Clean up the blob URL after download
    setTimeout(() => {
      window.URL.revokeObjectURL(downloadUrl)
    }, 100)
  }

  const handleClose = () => {
    if (exportStatus === 'preparing' || exportStatus === 'exporting') {
      if (window.confirm('Export is in progress. Are you sure you want to cancel?')) {
        onClose()
      }
    } else {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">
              Export Report
            </h3>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-500"
              disabled={exportStatus === 'preparing' || exportStatus === 'exporting'}
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          {exportStatus === 'idle' && (
            <>
              <p className="text-sm text-gray-600 mb-4">
                Export "{reportTitle}" to your preferred format
              </p>

              {/* Format Selection */}
              <div className="space-y-3 mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Format
                </label>
                
                <button
                  onClick={() => setSelectedFormat('pdf')}
                  className={`w-full flex items-center p-4 border-2 rounded-lg transition-all ${
                    selectedFormat === 'pdf'
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex-shrink-0">
                    <svg className="h-8 w-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-4 text-left flex-1">
                    <p className="text-sm font-medium text-gray-900">PDF Document</p>
                    <p className="text-xs text-gray-500">Best for sharing and printing</p>
                  </div>
                  {selectedFormat === 'pdf' && (
                    <svg className="h-5 w-5 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>

                <button
                  onClick={() => setSelectedFormat('docx')}
                  className={`w-full flex items-center p-4 border-2 rounded-lg transition-all ${
                    selectedFormat === 'docx'
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex-shrink-0">
                    <svg className="h-8 w-8 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-4 text-left flex-1">
                    <p className="text-sm font-medium text-gray-900">Word Document</p>
                    <p className="text-xs text-gray-500">Best for further editing</p>
                  </div>
                  {selectedFormat === 'docx' && (
                    <svg className="h-5 w-5 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              </div>
            </>
          )}

          {(exportStatus === 'preparing' || exportStatus === 'exporting') && (
            <div className="py-6">
              <div className="text-center mb-4">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-4">
                  <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
                </div>
                <h4 className="text-lg font-medium text-gray-900 mb-2">
                  {exportStatus === 'preparing' ? 'Preparing Export...' : 'Exporting...'}
                </h4>
                <p className="text-sm text-gray-600">
                  {exportStatus === 'preparing' 
                    ? 'Gathering report content and formatting'
                    : `Creating ${selectedFormat.toUpperCase()} file`
                  }
                </p>
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Progress</span>
                  <span className="text-sm font-medium text-gray-700">{Math.round(progress)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {exportStatus === 'completed' && (
            <div className="py-6 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <svg className="h-10 w-10 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <h4 className="text-lg font-medium text-gray-900 mb-2">
                Export Complete!
              </h4>
              <p className="text-sm text-gray-600 mb-4">
                Your report is ready to download
              </p>
              <p className="text-xs text-gray-500 mb-6">
                {reportTitle}.{selectedFormat}
              </p>
            </div>
          )}

          {exportStatus === 'error' && (
            <div className="py-6 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
                <svg className="h-10 w-10 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <h4 className="text-lg font-medium text-gray-900 mb-2">
                Export Failed
              </h4>
              <p className="text-sm text-red-600 mb-4">
                {errorMessage}
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
          <div className="flex space-x-3">
            {exportStatus === 'idle' && (
              <>
                <button
                  onClick={handleClose}
                  className="flex-1 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleExport}
                  className="flex-1 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Export {selectedFormat.toUpperCase()}
                </button>
              </>
            )}

            {exportStatus === 'completed' && (
              <>
                <button
                  onClick={handleClose}
                  className="flex-1 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Close
                </button>
                <button
                  onClick={handleDownload}
                  className="flex-1 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                >
                  <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Download
                </button>
              </>
            )}

            {exportStatus === 'error' && (
              <>
                <button
                  onClick={handleClose}
                  className="flex-1 px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Close
                </button>
                <button
                  onClick={handleExport}
                  className="flex-1 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Try Again
                </button>
              </>
            )}

            {(exportStatus === 'preparing' || exportStatus === 'exporting') && (
              <button
                disabled
                className="w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-400 cursor-not-allowed"
              >
                Exporting...
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
