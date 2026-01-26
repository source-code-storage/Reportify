import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { DemoVideoProps } from '../types';
import { UIBrowser, ClickableButton, Tab } from '../components/UIBrowser';

/**
 * InteractiveDemoScene - Shows actual UI workflow with tab transitions
 * Simulates clicking through the app: Reports → Upload → Search → Generate → Export
 */
export const InteractiveDemoScene: React.FC<DemoVideoProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Determine which tab is active based on time
  const activeTab = Math.floor(frame / (3 * fps)); // Change tab every 3 seconds
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        padding: 40,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <UIBrowser title="reportify.app">
        {/* Navigation Tabs */}
        <div
          style={{
            display: 'flex',
            gap: 0,
            borderBottom: '1px solid #334155',
            padding: '0 30px',
          }}
        >
          <Tab label="📊 Reports" isActive={activeTab === 0} delay={0.2} />
          <Tab label="📤 Upload" isActive={activeTab === 1} delay={0.3} />
          <Tab label="🔍 Search" isActive={activeTab === 2} delay={0.4} />
          <Tab label="✨ Generate" isActive={activeTab === 3} delay={0.5} />
          <Tab label="📥 Export" isActive={activeTab === 4} delay={0.6} />
        </div>
        
        {/* Tab Content */}
        <div style={{ padding: 40 }}>
          {activeTab === 0 && <ReportsTab delay={0} color={props.primaryColor} />}
          {activeTab === 1 && <UploadTab delay={0} color={props.secondaryColor} />}
          {activeTab === 2 && <SearchTab delay={0} color={props.accentColor} />}
          {activeTab === 3 && <GenerateTab delay={0} color={props.primaryColor} />}
          {activeTab === 4 && <ExportTab delay={0} color={props.secondaryColor} />}
        </div>
      </UIBrowser>
    </AbsoluteFill>
  );
};

// Reports Tab
const ReportsTab: React.FC<{ delay: number; color: string }> = ({ delay, color }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 30 }}>
      <h2 style={{ fontSize: 36, color: '#f8fafc', margin: 0 }}>My Reports</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <ReportCard
          title="Research Paper"
          status="In Progress"
          progress={65}
          delay={delay + 0.3}
          color={color}
        />
        <ReportCard
          title="Project Proposal"
          status="Draft"
          progress={30}
          delay={delay + 0.5}
          color={color}
        />
      </div>
      
      <div style={{ marginTop: 20 }}>
        <ClickableButton text="Create New Report" icon="➕" delay={delay + 0.8} color={color} />
      </div>
    </div>
  );
};

// Upload Tab
const UploadTab: React.FC<{ delay: number; color: string }> = ({ delay, color }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 30, alignItems: 'center' }}>
      <h2 style={{ fontSize: 36, color: '#f8fafc', margin: 0 }}>Upload Documents</h2>
      
      <div
        style={{
          width: '100%',
          maxWidth: 600,
          height: 300,
          border: `3px dashed ${color}`,
          borderRadius: 20,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 20,
        }}
      >
        <div style={{ fontSize: 80 }}>📄</div>
        <div style={{ fontSize: 24, color: '#94a3b8' }}>Drop PDFs here or click to browse</div>
      </div>
      
      <ClickableButton text="Upload Files" icon="📤" delay={delay + 0.5} color={color} />
      
      <div style={{ fontSize: 18, color: '#94a3b8', marginTop: 20 }}>
        ✨ AI will automatically extract and index your content
      </div>
    </div>
  );
};

// Search Tab
const SearchTab: React.FC<{ delay: number; color: string }> = ({ delay, color }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 30 }}>
      <h2 style={{ fontSize: 36, color: '#f8fafc', margin: 0 }}>Semantic Search</h2>
      
      {/* Search Bar */}
      <div
        style={{
          width: '100%',
          height: 60,
          backgroundColor: '#1e293b',
          borderRadius: 12,
          border: `2px solid ${color}`,
          display: 'flex',
          alignItems: 'center',
          padding: '0 20px',
          gap: 15,
        }}
      >
        <span style={{ fontSize: 24 }}>🔍</span>
        <span style={{ fontSize: 20, color: '#94a3b8' }}>
          Search: "methodology for data analysis"
        </span>
      </div>
      
      {/* Search Results */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 15 }}>
        <SearchResult
          title="Research Methods Chapter"
          snippet="Our methodology employs quantitative analysis..."
          relevance={95}
          delay={delay + 0.5}
          color={color}
        />
        <SearchResult
          title="Data Analysis Framework"
          snippet="The framework for analyzing collected data..."
          relevance={87}
          delay={delay + 0.7}
          color={color}
        />
      </div>
    </div>
  );
};

// Generate Tab
const GenerateTab: React.FC<{ delay: number; color: string }> = ({ delay, color }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 30 }}>
      <h2 style={{ fontSize: 36, color: '#f8fafc', margin: 0 }}>AI Content Generation</h2>
      
      <div style={{ display: 'flex', gap: 20 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 20, color: '#94a3b8', marginBottom: 15 }}>Section:</div>
          <div
            style={{
              padding: 20,
              backgroundColor: '#1e293b',
              borderRadius: 12,
              border: `2px solid ${color}`,
            }}
          >
            <div style={{ fontSize: 24, color: '#f8fafc', fontWeight: 'bold' }}>
              3.2 Methodology
            </div>
          </div>
        </div>
        
        <div style={{ flex: 2 }}>
          <div style={{ fontSize: 20, color: '#94a3b8', marginBottom: 15 }}>Generated Content:</div>
          <div
            style={{
              padding: 20,
              backgroundColor: '#1e293b',
              borderRadius: 12,
              border: '2px solid #10b981',
              minHeight: 150,
            }}
          >
            <div style={{ fontSize: 18, color: '#f8fafc', lineHeight: 1.6 }}>
              Our research methodology employs a mixed-methods approach, combining quantitative data
              analysis with qualitative insights...
            </div>
          </div>
        </div>
      </div>
      
      <div style={{ display: 'flex', gap: 15 }}>
        <ClickableButton text="Generate" icon="✨" delay={delay + 0.5} color={color} />
        <ClickableButton text="Improve" icon="🔄" delay={delay + 0.7} color="#8b5cf6" />
        <ClickableButton text="Expand" icon="📝" delay={delay + 0.9} color="#06b6d4" />
      </div>
    </div>
  );
};

// Export Tab
const ExportTab: React.FC<{ delay: number; color: string }> = ({ delay, color }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 30, alignItems: 'center' }}>
      <h2 style={{ fontSize: 36, color: '#f8fafc', margin: 0 }}>Export Your Report</h2>
      
      <div style={{ display: 'flex', gap: 30, marginTop: 30 }}>
        <ExportOption
          icon="📄"
          format="PDF"
          description="Professional formatting"
          delay={delay + 0.3}
          color={color}
        />
        <ExportOption
          icon="📝"
          format="DOCX"
          description="Editable in Word"
          delay={delay + 0.5}
          color="#8b5cf6"
        />
      </div>
      
      <div style={{ marginTop: 30 }}>
        <ClickableButton text="Download Report" icon="📥" delay={delay + 0.8} color={color} />
      </div>
    </div>
  );
};

// Helper Components
const ReportCard: React.FC<{
  title: string;
  status: string;
  progress: number;
  delay: number;
  color: string;
}> = ({ title, status, progress, delay, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const entrance = interpolate(frame, [delay * fps, (delay + 0.5) * fps], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  
  return (
    <div
      style={{
        padding: 25,
        backgroundColor: '#1e293b',
        borderRadius: 12,
        border: `2px solid ${color}`,
        opacity: entrance,
        transform: `translateY(${(1 - entrance) * 20}px)`,
      }}
    >
      <h3 style={{ fontSize: 24, color: '#f8fafc', margin: '0 0 10px 0' }}>{title}</h3>
      <div style={{ fontSize: 16, color: '#94a3b8', marginBottom: 15 }}>{status}</div>
      <div style={{ width: '100%', height: 8, backgroundColor: '#334155', borderRadius: 4 }}>
        <div
          style={{
            width: `${progress}%`,
            height: '100%',
            backgroundColor: color,
            borderRadius: 4,
          }}
        />
      </div>
    </div>
  );
};

const SearchResult: React.FC<{
  title: string;
  snippet: string;
  relevance: number;
  delay: number;
  color: string;
}> = ({ title, snippet, relevance, delay, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const entrance = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  
  return (
    <div
      style={{
        padding: 20,
        backgroundColor: '#1e293b',
        borderRadius: 12,
        border: `2px solid ${color}`,
        opacity: entrance,
        transform: `translateX(${(1 - entrance) * -30}px)`,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
        <h4 style={{ fontSize: 20, color: '#f8fafc', margin: 0 }}>{title}</h4>
        <div
          style={{
            padding: '5px 15px',
            backgroundColor: color,
            borderRadius: 20,
            fontSize: 14,
            fontWeight: 'bold',
            color: '#ffffff',
          }}
        >
          {relevance}% match
        </div>
      </div>
      <p style={{ fontSize: 16, color: '#94a3b8', margin: 0, lineHeight: 1.5 }}>{snippet}</p>
    </div>
  );
};

const ExportOption: React.FC<{
  icon: string;
  format: string;
  description: string;
  delay: number;
  color: string;
}> = ({ icon, format, description, delay, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const entrance = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  
  return (
    <div
      style={{
        width: 200,
        padding: 30,
        backgroundColor: '#1e293b',
        borderRadius: 16,
        border: `3px solid ${color}`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 15,
        opacity: entrance,
        transform: `scale(${entrance})`,
        cursor: 'pointer',
      }}
    >
      <div style={{ fontSize: 60 }}>{icon}</div>
      <div style={{ fontSize: 28, fontWeight: 'bold', color: '#f8fafc' }}>{format}</div>
      <div style={{ fontSize: 16, color: '#94a3b8', textAlign: 'center' }}>{description}</div>
    </div>
  );
};
