import { useState } from 'react'
import apiService from '../services/api'

interface SearchResult {
  id: string
  noteId: string
  noteName: string
  fileType: string
  excerpt: string
  relevanceScore: number
  uploadedAt: string
  highlightedExcerpt: string
}

interface NotesSearchProps {
  reportId: string
  onInsertExcerpt?: (excerpt: string, citation: string) => void
}

// Mock search results
const mockSearchResults: SearchResult[] = [
  {
    id: '1',
    noteId: '1',
    noteName: 'research_paper_ml.pdf',
    fileType: 'application/pdf',
    excerpt: 'Machine learning algorithms have shown significant improvements in natural language processing tasks. Recent studies demonstrate that transformer-based models achieve state-of-the-art results across multiple benchmarks.',
    relevanceScore: 0.95,
    uploadedAt: '2024-01-08T10:30:00',
    highlightedExcerpt: '<mark>Machine learning</mark> algorithms have shown significant improvements in natural language processing tasks. Recent studies demonstrate that transformer-based models achieve state-of-the-art results across multiple benchmarks.'
  },
  {
    id: '2',
    noteId: '1',
    noteName: 'research_paper_ml.pdf',
    fileType: 'application/pdf',
    excerpt: 'The implementation of deep learning techniques requires careful consideration of computational resources. GPU acceleration is essential for training large-scale models efficiently.',
    relevanceScore: 0.87,
    uploadedAt: '2024-01-08T10:30:00',
    highlightedExcerpt: 'The implementation of <mark>deep learning</mark> techniques requires careful consideration of computational resources. GPU acceleration is essential for training large-scale models efficiently.'
  },
  {
    id: '3',
    noteId: '2',
    noteName: 'interview_notes.txt',
    fileType: 'text/plain',
    excerpt: 'During the interview, the expert mentioned that machine learning adoption in industry has accelerated rapidly. Companies are investing heavily in AI infrastructure and talent acquisition.',
    relevanceScore: 0.82,
    uploadedAt: '2024-01-08T11:15:00',
    highlightedExcerpt: 'During the interview, the expert mentioned that <mark>machine learning</mark> adoption in industry has accelerated rapidly. Companies are investing heavily in AI infrastructure and talent acquisition.'
  }
]

export default function NotesSearch({ reportId, onInsertExcerpt }: NotesSearchProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [hasSearched, setHasSearched] = useState(false)
  
  // Filters
  const [selectedFileTypes, setSelectedFileTypes] = useState<string[]>([])
  const [dateRange, setDateRange] = useState<{ start: string; end: string }>({
    start: '',
    end: ''
  })

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setIsSearching(true)
    setHasSearched(true)

    try {
      // Call real API
      const response = await apiService.searchNotes(searchQuery, reportId, 10)
      
      console.log('Search API response:', response)
      
      // Transform API results to match our interface
      const transformedResults: SearchResult[] = response.results.map((result: any, index: number) => ({
        id: `${result.note_id}-${index}`,
        noteId: result.note_id.toString(),
        noteName: result.filename,
        fileType: result.file_type === 'txt' ? 'text/plain' : 'application/pdf',
        excerpt: result.chunk_text,
        relevanceScore: result.score,
        uploadedAt: new Date().toISOString(),
        highlightedExcerpt: result.chunk_text
      }))

      console.log('Transformed results:', transformedResults)
      setSearchResults(transformedResults)
    } catch (error) {
      console.error('Search failed:', error)
      alert('Search failed. Please try again.')
    } finally {
      setIsSearching(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const toggleFileType = (fileType: string) => {
    setSelectedFileTypes(prev =>
      prev.includes(fileType)
        ? prev.filter(t => t !== fileType)
        : [...prev, fileType]
    )
  }

  const handleInsert = (result: SearchResult) => {
    if (onInsertExcerpt) {
      const citation = `[Source: ${result.noteName}]`
      onInsertExcerpt(result.excerpt, citation)
    }
  }

  const getRelevanceColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600'
    if (score >= 0.8) return 'text-blue-600'
    if (score >= 0.7) return 'text-yellow-600'
    return 'text-gray-600'
  }

  const getFileTypeIcon = (fileType: string) => {
    if (fileType.includes('pdf')) {
      return (
        <svg className="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
        </svg>
      )
    }
    if (fileType.includes('image')) {
      return (
        <svg className="h-5 w-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
        </svg>
      )
    }
    return (
      <svg className="h-5 w-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
      </svg>
    )
  }

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex space-x-2">
          <div className="flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search your research notes..."
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={isSearching || !searchQuery.trim()}
            className="px-6 py-2 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed"
          >
            {isSearching ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Searching...
              </div>
            ) : (
              <div className="flex items-center">
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search
              </div>
            )}
          </button>
        </div>

        {/* Filters */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* File Type Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                File Type
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedFileTypes.includes('application/pdf')}
                    onChange={() => toggleFileType('application/pdf')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">PDF</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedFileTypes.includes('text/plain')}
                    onChange={() => toggleFileType('text/plain')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Text</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedFileTypes.includes('image/png')}
                    onChange={() => toggleFileType('image/png')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Images</span>
                </label>
              </div>
            </div>

            {/* Date Range Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date
              </label>
              <input
                type="date"
                value={dateRange.start}
                onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date
              </label>
              <input
                type="date"
                value={dateRange.end}
                onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          {/* Clear Filters */}
          {(selectedFileTypes.length > 0 || dateRange.start || dateRange.end) && (
            <button
              onClick={() => {
                setSelectedFileTypes([])
                setDateRange({ start: '', end: '' })
              }}
              className="mt-3 text-sm text-indigo-600 hover:text-indigo-700"
            >
              Clear all filters
            </button>
          )}
        </div>
      </div>

      {/* Search Results */}
      {hasSearched && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              {searchResults.length} {searchResults.length === 1 ? 'result' : 'results'} found
            </h3>
            {searchResults.length > 0 && (
              <span className="text-sm text-gray-600">
                Sorted by relevance
              </span>
            )}
          </div>

          {searchResults.length === 0 ? (
            <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No results found</h3>
              <p className="mt-1 text-sm text-gray-500">
                Try adjusting your search query or filters
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {searchResults.map((result) => (
                <div
                  key={result.id}
                  className="bg-white rounded-lg border border-gray-200 p-4 hover:border-indigo-300 hover:shadow-md transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      {/* Source Info */}
                      <div className="flex items-center space-x-2 mb-2">
                        {getFileTypeIcon(result.fileType)}
                        <span className="text-sm font-medium text-gray-900">
                          {result.noteName}
                        </span>
                        <span className={`text-sm font-medium ${getRelevanceColor(result.relevanceScore)}`}>
                          {Math.round(result.relevanceScore * 100)}% match
                        </span>
                      </div>

                      {/* Excerpt */}
                      <div
                        className="text-gray-700 leading-relaxed mb-3"
                        dangerouslySetInnerHTML={{ __html: result.highlightedExcerpt }}
                      />

                      {/* Metadata */}
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>
                          Uploaded {new Date(result.uploadedAt).toLocaleDateString()}
                        </span>
                      </div>
                    </div>

                    {/* Insert Button */}
                    <button
                      onClick={() => handleInsert(result)}
                      className="ml-4 flex-shrink-0 inline-flex items-center px-3 py-2 border border-indigo-300 text-sm font-medium rounded-md text-indigo-700 bg-indigo-50 hover:bg-indigo-100"
                    >
                      <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                      Insert
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
