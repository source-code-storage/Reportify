import { useState } from 'react'

interface Note {
  id: string
  filename: string
  file_type: string
  file_size: number
  status: 'pending' | 'processing' | 'completed' | 'error'
  uploaded_at: string
  processed_at?: string
  error_message?: string
}

interface NotesListProps {
  reportId: string
  onDeleteNote?: (noteId: string) => void
}

// Mock notes data
const mockNotes: Note[] = [
  {
    id: '1',
    filename: 'research_paper_ml.pdf',
    file_type: 'application/pdf',
    file_size: 2457600,
    status: 'completed',
    uploaded_at: '2024-01-08T10:30:00',
    processed_at: '2024-01-08T10:31:15'
  },
  {
    id: '2',
    filename: 'interview_notes.txt',
    file_type: 'text/plain',
    file_size: 15360,
    status: 'completed',
    uploaded_at: '2024-01-08T11:15:00',
    processed_at: '2024-01-08T11:15:30'
  },
  {
    id: '3',
    filename: 'diagram_architecture.png',
    file_type: 'image/png',
    file_size: 524288,
    status: 'processing',
    uploaded_at: '2024-01-08T14:20:00'
  }
]

export default function NotesList({ reportId, onDeleteNote }: NotesListProps) {
  const [notes] = useState<Note[]>(mockNotes)
  const [selectedNotes, setSelectedNotes] = useState<Set<string>>(new Set())

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const getFileIcon = (fileType: string) => {
    if (fileType.includes('pdf')) {
      return (
        <svg className="h-8 w-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
        </svg>
      )
    }
    if (fileType.includes('image')) {
      return (
        <svg className="h-8 w-8 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
        </svg>
      )
    }
    if (fileType.includes('text')) {
      return (
        <svg className="h-8 w-8 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
        </svg>
      )
    }
    return (
      <svg className="h-8 w-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
      </svg>
    )
  }

  const getStatusBadge = (status: Note['status']) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            <svg className="h-3 w-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            Processed
          </span>
        )
      case 'processing':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600 mr-1"></div>
            Processing
          </span>
        )
      case 'pending':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            Pending
          </span>
        )
      case 'error':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
            Error
          </span>
        )
    }
  }

  const toggleNoteSelection = (noteId: string) => {
    const newSelected = new Set(selectedNotes)
    if (newSelected.has(noteId)) {
      newSelected.delete(noteId)
    } else {
      newSelected.add(noteId)
    }
    setSelectedNotes(newSelected)
  }

  const handleDeleteSelected = () => {
    if (window.confirm(`Delete ${selectedNotes.size} selected note(s)?`)) {
      selectedNotes.forEach(noteId => {
        if (onDeleteNote) {
          onDeleteNote(noteId)
        }
      })
      setSelectedNotes(new Set())
    }
  }

  if (notes.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No notes uploaded</h3>
        <p className="mt-1 text-sm text-gray-500">Upload files above to get started</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header with actions */}
      {selectedNotes.size > 0 && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-indigo-900">
              {selectedNotes.size} note(s) selected
            </span>
            <button
              onClick={handleDeleteSelected}
              className="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Delete
            </button>
          </div>
        </div>
      )}

      {/* Notes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {notes.map(note => (
          <div
            key={note.id}
            className={`bg-white rounded-lg border-2 transition-all ${
              selectedNotes.has(note.id)
                ? 'border-indigo-500 shadow-md'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="p-4">
              <div className="flex items-start">
                {/* Checkbox */}
                <input
                  type="checkbox"
                  checked={selectedNotes.has(note.id)}
                  onChange={() => toggleNoteSelection(note.id)}
                  className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />

                {/* File Icon */}
                <div className="ml-3 flex-shrink-0">
                  {getFileIcon(note.file_type)}
                </div>

                {/* File Info */}
                <div className="ml-3 flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {note.filename}
                  </p>
                  <div className="mt-1 flex items-center space-x-2">
                    {getStatusBadge(note.status)}
                    <span className="text-xs text-gray-500">
                      {formatFileSize(note.file_size)}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    Uploaded {formatDate(note.uploaded_at)}
                  </p>
                  {note.error_message && (
                    <p className="mt-1 text-xs text-red-600">
                      {note.error_message}
                    </p>
                  )}
                </div>

                {/* Actions Menu */}
                <div className="ml-2 flex-shrink-0">
                  <button className="text-gray-400 hover:text-gray-500">
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
