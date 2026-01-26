import { useState, useEffect, useRef } from 'react'

interface RichTextEditorProps {
  content: string
  onChange: (content: string) => void
  onSave: () => void
  isSaving: boolean
  wordCount: number
  onGenerateContent?: () => void
  onImproveContent?: () => void
  onExpandContent?: () => void
  isGenerating?: boolean
}

export default function RichTextEditor({
  content,
  onChange,
  onSave,
  isSaving,
  wordCount,
  onGenerateContent,
  onImproveContent,
  onExpandContent,
  isGenerating = false
}: RichTextEditorProps) {
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const editorRef = useRef<HTMLDivElement>(null)
  const autoSaveTimerRef = useRef<NodeJS.Timeout>()

  // Auto-save functionality
  useEffect(() => {
    if (hasUnsavedChanges) {
      // Clear existing timer
      if (autoSaveTimerRef.current) {
        clearTimeout(autoSaveTimerRef.current)
      }

      // Set new timer for 3 seconds (simulating 30 seconds for demo)
      autoSaveTimerRef.current = setTimeout(() => {
        handleSave()
      }, 3000)
    }

    return () => {
      if (autoSaveTimerRef.current) {
        clearTimeout(autoSaveTimerRef.current)
      }
    }
  }, [content, hasUnsavedChanges])

  const handleSave = () => {
    onSave()
    setLastSaved(new Date())
    setHasUnsavedChanges(false)
  }

  const handleContentChange = (e: React.FormEvent<HTMLDivElement>) => {
    const newContent = e.currentTarget.textContent || ''
    onChange(newContent)
    setHasUnsavedChanges(true)
  }

  const applyFormat = (command: string, value?: string) => {
    document.execCommand(command, false, value)
    editorRef.current?.focus()
  }

  const formatLastSaved = () => {
    if (!lastSaved) return ''
    const now = new Date()
    const diff = Math.floor((now.getTime() - lastSaved.getTime()) / 1000)
    
    if (diff < 60) return 'just now'
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
    return `${Math.floor(diff / 3600)}h ago`
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Toolbar */}
      <div className="border-b border-gray-200 p-3">
        <div className="flex items-center justify-between">
          {/* Formatting Tools */}
          <div className="flex items-center space-x-1">
            <button
              onClick={() => applyFormat('bold')}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Bold (Ctrl+B)"
            >
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3H6a1 1 0 000 2h5a3 3 0 010 6H6a1 1 0 100 2h5a5 5 0 000-10z" />
              </svg>
            </button>
            <button
              onClick={() => applyFormat('italic')}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Italic (Ctrl+I)"
            >
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1z" transform="skewX(-15)" />
              </svg>
            </button>
            <button
              onClick={() => applyFormat('underline')}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Underline (Ctrl+U)"
            >
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a1 1 0 011 1v8a3 3 0 11-6 0V3a1 1 0 112 0v8a1 1 0 102 0V3a1 1 0 011-1zM4 16a1 1 0 100 2h12a1 1 0 100-2H4z" />
              </svg>
            </button>

            <div className="w-px h-6 bg-gray-300 mx-2" />

            <button
              onClick={() => applyFormat('insertUnorderedList')}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Bullet List"
            >
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            </button>
            <button
              onClick={() => applyFormat('insertOrderedList')}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Numbered List"
            >
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            </button>

            <div className="w-px h-6 bg-gray-300 mx-2" />

            <select
              onChange={(e) => applyFormat('formatBlock', e.target.value)}
              className="text-sm border-gray-300 rounded px-2 py-1"
              defaultValue="p"
            >
              <option value="p">Normal</option>
              <option value="h1">Heading 1</option>
              <option value="h2">Heading 2</option>
              <option value="h3">Heading 3</option>
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-2">
            {onGenerateContent && (
              <button
                onClick={onGenerateContent}
                disabled={isGenerating}
                className="inline-flex items-center px-3 py-1.5 border border-purple-300 text-sm font-medium rounded-md text-purple-700 bg-purple-50 hover:bg-purple-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-700 mr-2"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Generate
                  </>
                )}
              </button>
            )}
            
            <button
              onClick={handleSave}
              disabled={isSaving || !hasUnsavedChanges}
              className="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>
      </div>

      {/* Editor Area */}
      <div
        ref={editorRef}
        contentEditable
        onInput={handleContentChange}
        className="p-6 min-h-[500px] focus:outline-none font-serif text-gray-900 prose prose-lg max-w-none"
        suppressContentEditableWarning
        dangerouslySetInnerHTML={{ __html: content }}
      />

      {/* Status Bar */}
      <div className="border-t border-gray-200 px-6 py-3 bg-gray-50">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">
              {wordCount} {wordCount === 1 ? 'word' : 'words'}
            </span>
            {hasUnsavedChanges && (
              <span className="text-yellow-600 flex items-center">
                <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
                Auto-saving...
              </span>
            )}
            {!hasUnsavedChanges && lastSaved && (
              <span className="text-green-600 flex items-center">
                <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Saved {formatLastSaved()}
              </span>
            )}
          </div>

          {/* Content Improvement Tools */}
          {(onImproveContent || onExpandContent) && (
            <div className="flex items-center space-x-2">
              {onImproveContent && (
                <button
                  onClick={onImproveContent}
                  className="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
                >
                  Improve
                </button>
              )}
              {onExpandContent && (
                <button
                  onClick={onExpandContent}
                  className="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
                >
                  Expand
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
