import { useState, useEffect } from 'react'
import { useAuthStore } from '../stores/authStore'
import { useReportStore } from '../stores/reportStore'
import { useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Progress } from '../components/ui/progress'
import { Badge } from '../components/ui/badge'

export default function Dashboard() {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()
  
  const { reports, isLoading, error, fetchReports, createReport, clearError } = useReportStore()
  
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
  })
  const [templateFile, setTemplateFile] = useState<File | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    fetchReports()
  }, [])

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const handleCreateReport = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    try {
      const newReport = await createReport(
        formData.title,
        formData.description,
        templateFile || undefined
      )
      
      setShowCreateModal(false)
      setFormData({ title: '', description: '' })
      setTemplateFile(null)
      
      navigate(`/reports/${newReport.id}`)
    } catch (error) {
      console.error('Failed to create report:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setTemplateFile(e.target.files[0])
    }
  }

  const getStatusVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (status) {
      case 'completed':
        return 'default'
      case 'in_progress':
        return 'secondary'
      case 'draft':
        return 'outline'
      default:
        return 'outline'
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navigation Bar */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-gray-900">
                Report Writing Assistant
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-muted-foreground">
                {user?.name || user?.email}
              </span>
              <Button
                onClick={handleLogout}
                variant="outline"
                size="sm"
              >
                Logout
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="animate-fade-in">
          {/* Header */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              My Reports
            </h2>
            <p className="text-muted-foreground">
              Create and manage your report writing projects
            </p>
          </div>

          {/* Create New Report Button */}
          <div className="mb-6">
            <Button
              onClick={() => setShowCreateModal(true)}
              size="lg"
              className="shadow-lg"
            >
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Create New Report
            </Button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-lg relative">
              <span className="block sm:inline">{error}</span>
              <button
                onClick={clearError}
                className="absolute top-0 bottom-0 right-0 px-4 py-3"
              >
                <span className="text-2xl">&times;</span>
              </button>
            </div>
          )}

          {/* Loading State */}
          {isLoading && reports.length === 0 ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              <p className="mt-2 text-sm text-muted-foreground">Loading reports...</p>
            </div>
          ) : (
            <>
              {/* Reports Grid */}
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {reports.map((report) => (
                  <Card
                    key={report.id}
                    className="hover:shadow-lg transition-all cursor-pointer group animate-slide-in"
                    onClick={() => navigate(`/reports/${report.id}`)}
                  >
                    <CardHeader>
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant={getStatusVariant(report.status)}>
                          {report.status.replace('_', ' ')}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {formatDate(report.updated_at)}
                        </span>
                      </div>
                      <CardTitle className="group-hover:text-primary transition-colors">
                        {report.title}
                      </CardTitle>
                      <CardDescription className="line-clamp-2">
                        {report.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      {/* Progress Bar */}
                      <div className="mb-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-medium text-muted-foreground">Progress</span>
                          <span className="text-xs font-medium text-primary">{report.progress_percentage}%</span>
                        </div>
                        <Progress value={report.progress_percentage} className="h-2" />
                      </div>

                      {/* Stats */}
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span className="flex items-center">
                          <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          {report.total_word_count.toLocaleString()} words
                        </span>
                        <span>
                          {formatDate(report.created_at)}
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Empty State */}
              {reports.length === 0 && !isLoading && (
                <Card className="text-center py-12">
                  <CardContent className="pt-6">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                      <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-semibold mb-2">No reports yet</h3>
                    <p className="text-muted-foreground mb-6">Get started by creating your first report.</p>
                    <Button onClick={() => setShowCreateModal(true)} size="lg">
                      <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                      Create New Report
                    </Button>
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </div>
      </main>

      {/* Create Report Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 animate-fade-in">
          <Card className="max-w-lg w-full animate-slide-in">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Create New Report</CardTitle>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <CardDescription>
                Fill in the details to create your new report
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateReport} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Report Title *</Label>
                  <Input
                    id="title"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="e.g., Internship Final Report"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description *</Label>
                  <textarea
                    id="description"
                    required
                    rows={3}
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Brief description of your report"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="template">Template (Optional)</Label>
                  <div className="border-2 border-dashed border-input rounded-lg p-6 text-center hover:border-primary/50 transition-colors">
                    <svg
                      className="mx-auto h-12 w-12 text-muted-foreground"
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
                      <label
                        htmlFor="template"
                        className="cursor-pointer text-sm font-medium text-primary hover:text-primary/80"
                      >
                        Upload a file
                        <input
                          id="template"
                          name="template"
                          type="file"
                          className="sr-only"
                          accept=".pdf,.doc,.docx"
                          onChange={handleFileChange}
                        />
                      </label>
                      <span className="text-sm text-muted-foreground"> or drag and drop</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">PDF, DOC, DOCX up to 50MB</p>
                    {templateFile && (
                      <p className="text-sm text-primary font-medium mt-3">
                        ✓ {templateFile.name}
                      </p>
                    )}
                  </div>
                </div>

                <div className="flex space-x-3 pt-4">
                  <Button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    variant="outline"
                    className="flex-1"
                    disabled={isSubmitting}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={isSubmitting}
                    className="flex-1"
                  >
                    {isSubmitting ? 'Creating...' : 'Create Report'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
