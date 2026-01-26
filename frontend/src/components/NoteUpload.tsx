import { useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import NotesList from './NotesList'
import apiService from '../services/api'

interface UploadedFile {
  id: string
  file: File
  progress: number
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error'
  error?: string
}

interface NoteUploadProps {
  onUploadComplete?: () => void
}

export default function NoteUpload({ onUploadComplete }: NoteUploadProps) {
  const { reportId } = useParams<{ reportId: string }>()
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      handleFiles(files)
    }
  }

  const handleFiles = (files: File[]) => {
    // Validate file types
    const validTypes = [
      'application/pdf',
      'text/plain',
      'image/png',
      'image/jpeg',
      'image/jpg',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]

    const validFiles = files.filter(file => {
      if (!validTypes.includes(file.type)) {
        alert(`File type not supported: ${file.name}`)
        return false
      }
      if (file.size > 50 * 1024 * 1024) { // 50MB
        alert(`File too large: ${file.name} (max 50MB)`)
        return false
      }
      return true
    })

    // Add files to upload queue
    const newFiles: UploadedFile[] = validFiles.map(file => ({
      id: `${Date.now()}-${Math.random()}`,
      file,
      progress: 0,
      status: 'pending'
    }))

    setUploadedFiles(prev => [...prev, ...newFiles])

    // Start uploading
    newFiles.forEach(uploadFile)
  }

  const uploadFile = async (uploadedFile: UploadedFile) => {
    if (!reportId) return

    // Update status to uploading
    setUploadedFiles(prev =>
      prev.map(f => f.id === uploadedFile.id ? { ...f, status: 'uploading' } : f)
    )

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadedFiles(prev =>
          prev.map(f => {
            if (f.id === uploadedFile.id && f.progress < 90) {
              return { ...f, progress: f.progress + 10 }
            }
            return f
          })
        )
      }, 200)

      // Call real API to upload note
      const result = await apiService.uploadNote(reportId, uploadedFile.file)

      clearInterval(progressInterval)

      // Check if processing completed
      if (result.status === 'completed') {
        // Update to completed
        setUploadedFiles(prev =>
          prev.map(f =>
            f.id === uploadedFile.id
              ? { ...f, status: 'completed', progress: 100 }
              : f
          )
        )
        
        console.log('Note uploaded and processed successfully!')
        console.log(`Note ID: ${result.id}`)
        console.log(`Embeddings generated and stored in vector database`)
        
      } else if (result.status === 'processing') {
        // Still processing
        setUploadedFiles(prev =>
          prev.map(f =>
            f.id === uploadedFile.id
              ? { ...f, status: 'processing', progress: 100 }
              : f
          )
        )
        
        // Poll for completion (optional)
        setTimeout(() => checkNoteStatus(uploadedFile.id, result.id), 2000)
        
      } else if (result.status === 'failed') {
        // Processing failed
        setUploadedFiles(prev =>
          prev.map(f =>
            f.id === uploadedFile.id
              ? { ...f, status: 'error', progress: 0, error: result.processing_error || 'Processing failed' }
              : f
          )
        )
      }

      onUploadComplete()
    } catch (error: any) {
      console.error('Upload failed:', error)
      
      setUploadedFiles(prev =>
        prev.map(f =>
          f.id === uploadedFile.id
            ? { 
                ...f, 
                status: 'error', 
                progress: 0,
                error: error.response?.data?.detail || 'Upload failed. Please try again.'
              }
            : f
        )
      )
    }
  }

  const checkNoteStatus = async (uploadFileId: string, noteId: string) => {
    try {
      const note = await apiService.getNote(noteId)
      
      if (note.status === 'completed') {
        setUploadedFiles(prev =>
          prev.map(f =>
            f.id === uploadFileId
              ? { ...f, status: 'completed' }
              : f
          )
        )
      } else if (note.status === 'failed') {
        setUploadedFiles(prev =>
          prev.map(f =>
            f.id === uploadFileId
              ? { ...f, status: 'error', error: note.processing_error }
              : f
          )
        )
      } else {
        // Still processing, check again
        setTimeout(() => checkNoteStatus(uploadFileId, noteId), 2000)
      }
    } catch (error) {
      console.error('Failed to check note status:', error)
    }
  }

  const removeFile = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const retryUpload = (fileId: string) => {
    const file = uploadedFiles.find(f => f.id === fileId)
    if (file) {
      setUploadedFiles(prev =>
        prev.map(f =>
          f.id === fileId ? { ...f, status: 'pending', progress: 0, error: undefined } : f
        )
      )
      uploadFile(file)
    }
  }

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'pending':
        return (
          <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )
      case 'uploading':
        return (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600"></div>
        )
      case 'processing':
        return (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        )
      case 'completed':
        return (
          <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        )
      case 'error':
        return (
          <svg className="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        )
    }
  }

  const getStatusText = (status: UploadedFile['status']) => {
    switch (status) {
      case 'pending':
        return 'Pending'
      case 'uploading':
        return 'Uploading...'
      case 'processing':
        return 'Processing...'
      case 'completed':
        return 'Completed'
      case 'error':
        return 'Failed'
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 hover:border-indigo-400'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.txt,.png,.jpg,.jpeg,.doc,.docx"
          onChange={handleFileSelect}
          className="hidden"
        />

        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>

        <div className="mt-4">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Select Files
          </button>
          <p className="mt-2 text-sm text-gray-600">or drag and drop files here</p>
        </div>

        <p className="mt-2 text-xs text-gray-500">
          PDF, TXT, PNG, JPG, DOC, DOCX up to 50MB each
        </p>
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-medium text-gray-900">
              Uploaded Files ({uploadedFiles.length})
            </h3>
          </div>
          <div className="divide-y divide-gray-200">
            {uploadedFiles.map(file => (
              <div key={file.id} className="px-4 py-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center flex-1 min-w-0">
                    {getStatusIcon(file.status)}
                    <div className="ml-3 flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {file.file.name}
                      </p>
                      <div className="flex items-center space-x-2 text-xs text-gray-500">
                        <span>{formatFileSize(file.file.size)}</span>
                        <span>•</span>
                        <span>{getStatusText(file.status)}</span>
                      </div>
                      {file.error && (
                        <p className="text-xs text-red-600 mt-1">{file.error}</p>
                      )}
                    </div>
                  </div>

                  <div className="ml-4 flex items-center space-x-2">
                    {file.status === 'error' && (
                      <button
                        onClick={() => retryUpload(file.id)}
                        className="text-sm text-indigo-600 hover:text-indigo-700"
                      >
                        Retry
                      </button>
                    )}
                    {(file.status === 'pending' || file.status === 'error' || file.status === 'completed') && (
                      <button
                        onClick={() => removeFile(file.id)}
                        className="text-gray-400 hover:text-gray-500"
                      >
                        <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                        </svg>
                      </button>
                    )}
                  </div>
                </div>

                {/* Progress Bar */}
                {(file.status === 'uploading' || file.status === 'processing') && (
                  <div className="mt-2">
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div
                        className="bg-indigo-600 h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${file.progress}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Existing Notes List */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Uploaded Notes</h3>
        <NotesList 
          reportId={reportId || ''} 
          onDeleteNote={(noteId) => {
            console.log('Delete note:', noteId)
          }} 
        />
      </div>
    </div>
  )
}
