import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  FileText, 
  Sparkles, 
  Search, 
  Zap, 
  CheckCircle2, 
  ArrowRight,
  Upload,
  Brain,
  Download
} from 'lucide-react'

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="relative">
                <FileText className="h-8 w-8 text-blue-600" />
                <Sparkles className="h-4 w-4 text-purple-500 absolute -top-1 -right-1" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Reportify
              </span>
            </div>
            
            {/* Navigation Links */}
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link to="/register">
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-8">
              <Sparkles className="h-4 w-4" />
              <span>AI-Powered Report Writing</span>
            </div>
            
            {/* Main Heading */}
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 mb-6">
              Transform Your
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Report Writing
              </span>
            </h1>
            
            {/* Subheading */}
            <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
              Reportify uses AI to help you create professional reports faster. 
              Upload documents, search intelligently, and generate content with GPT-4.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/register">
                <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8 py-6">
                  Start Writing Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link to="/login">
                <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                  Sign In
                </Button>
              </Link>
            </div>
            
            {/* Social Proof */}
            <div className="mt-12 flex items-center justify-center space-x-8 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>No credit card required</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>Free to use</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>AI-powered</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Write Better Reports
            </h2>
            <p className="text-xl text-gray-600">
              Powerful features that make report writing effortless
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-blue-100 hover:shadow-xl transition-shadow">
              <div className="h-12 w-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
                <Upload className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Smart Document Processing
              </h3>
              <p className="text-gray-600">
                Upload PDFs and templates. Our AI automatically extracts sections and structures your report.
              </p>
            </div>
            
            {/* Feature 2 */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-purple-100 hover:shadow-xl transition-shadow">
              <div className="h-12 w-12 bg-purple-600 rounded-lg flex items-center justify-center mb-4">
                <Search className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Semantic Search
              </h3>
              <p className="text-gray-600">
                Find relevant information instantly with AI-powered semantic search. Not just keywords, but meaning.
              </p>
            </div>
            
            {/* Feature 3 */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-pink-50 to-pink-100 hover:shadow-xl transition-shadow">
              <div className="h-12 w-12 bg-pink-600 rounded-lg flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                AI Content Generation
              </h3>
              <p className="text-gray-600">
                Generate high-quality content with GPT-4. Context-aware and citation-ready.
              </p>
            </div>
            
            {/* Feature 4 */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-green-50 to-green-100 hover:shadow-xl transition-shadow">
              <div className="h-12 w-12 bg-green-600 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Lightning Fast
              </h3>
              <p className="text-gray-600">
                Async processing ensures your documents are ready in seconds, not minutes.
              </p>
            </div>
            
            {/* Feature 5 */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-yellow-50 to-yellow-100 hover:shadow-xl transition-shadow">
              <div className="h-12 w-12 bg-yellow-600 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Professional Templates
              </h3>
              <p className="text-gray-600">
                Use your own templates or start from scratch. Full support for academic and business reports.
              </p>
            </div>
            
            {/* Feature 6 */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-indigo-50 to-indigo-100 hover:shadow-xl transition-shadow">
              <div className="h-12 w-12 bg-indigo-600 rounded-lg flex items-center justify-center mb-4">
                <Download className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Export Anywhere
              </h3>
              <p className="text-gray-600">
                Export to PDF or DOCX with professional formatting. Ready to submit or share.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Get started in minutes with our simple workflow
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                Create Report
              </h3>
              <p className="text-gray-600">
                Start a new report and optionally upload a template
              </p>
            </div>
            
            {/* Step 2 */}
            <div className="text-center">
              <div className="h-16 w-16 bg-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                Upload Notes
              </h3>
              <p className="text-gray-600">
                Add your reference documents and research materials
              </p>
            </div>
            
            {/* Step 3 */}
            <div className="text-center">
              <div className="h-16 w-16 bg-pink-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                Generate Content
              </h3>
              <p className="text-gray-600">
                Let AI write sections based on your notes
              </p>
            </div>
            
            {/* Step 4 */}
            <div className="text-center">
              <div className="h-16 w-16 bg-green-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                Export & Share
              </h3>
              <p className="text-gray-600">
                Download as PDF or DOCX and submit
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Transform Your Report Writing?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join students and professionals who are writing better reports with AI
          </p>
          <Link to="/register">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-6">
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <FileText className="h-6 w-6 text-blue-500" />
              <span className="text-xl font-bold text-white">Reportify</span>
            </div>
            <div className="text-sm">
              © 2026 Reportify. Built for the Dynamous Kiro Hackathon.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
