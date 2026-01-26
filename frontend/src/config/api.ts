/**
 * API configuration
 */

export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  version: import.meta.env.VITE_API_VERSION || 'v1',
  timeout: 30000, // 30 seconds
} as const;

export const getApiUrl = (endpoint: string): string => {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_CONFIG.baseURL}/api/${API_CONFIG.version}/${cleanEndpoint}`;
};

export const API_ENDPOINTS = {
  // Auth
  auth: {
    register: '/auth/register',
    login: '/auth/login',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    me: '/auth/me',
  },
  // Reports
  reports: {
    list: '/reports',
    create: '/reports',
    get: (id: string) => `/reports/${id}`,
    update: (id: string) => `/reports/${id}`,
    delete: (id: string) => `/reports/${id}`,
    sections: (id: string) => `/reports/${id}/sections`,
    updateSection: (reportId: string, sectionId: string) => 
      `/reports/${reportId}/sections/${sectionId}`,
  },
  // Uploads
  uploads: {
    template: '/uploads/template',
    notes: '/uploads/notes',
    status: (id: string) => `/uploads/${id}/status`,
    delete: (id: string) => `/uploads/${id}`,
  },
  // Search
  search: {
    semantic: '/search',
    mapToSections: '/search/map-to-sections',
    sectionNotes: (sectionId: string) => `/search/section/${sectionId}/notes`,
  },
  // Content
  content: {
    generate: '/content/generate',
    regenerate: '/content/regenerate',
    improve: '/content/improve',
    expand: '/content/expand',
  },
  // Export
  export: {
    pdf: '/export/pdf',
    docx: '/export/docx',
    status: (id: string) => `/export/${id}/status`,
    download: (id: string) => `/export/${id}/download`,
  },
} as const;
