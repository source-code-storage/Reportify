import React from 'react';
import { AbsoluteFill } from 'remotion';
import { DemoVideoProps } from '../types';
import { AnimatedText } from '../components/AnimatedText';

/**
 * Generic Demo Scene Template
 * Can be used for Auth, Report Creation, Upload, Search, Generation, Export scenes
 */
interface DemoSceneProps extends DemoVideoProps {
  title: string;
  subtitle: string;
  icon: string;
}

export const DemoScene: React.FC<DemoSceneProps> = (props) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <div style={{ fontSize: 120, marginBottom: 40 }}>
        {props.icon}
      </div>
      
      <AnimatedText
        text={props.title}
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 30,
        }}
      />
      
      <AnimatedText
        text={props.subtitle}
        style={{
          fontSize: 32,
          color: props.secondaryColor,
          textAlign: 'center',
          maxWidth: 900,
        }}
        startFrame={15}
      />
    </AbsoluteFill>
  );
};

// Export specific scene variants
export const AuthScene: React.FC<DemoVideoProps> = (props) => (
  <DemoScene {...props} title="User Authentication" subtitle="Secure login and registration" icon="🔐" />
);

export const ReportCreationScene: React.FC<DemoVideoProps> = (props) => (
  <DemoScene {...props} title="Create Reports" subtitle="Upload templates and auto-extract sections" icon="📝" />
);

export const UploadScene: React.FC<DemoVideoProps> = (props) => (
  <DemoScene {...props} title="Upload Documents" subtitle="Process PDFs and generate embeddings" icon="📤" />
);

export const SearchScene: React.FC<DemoVideoProps> = (props) => (
  <DemoScene {...props} title="Semantic Search" subtitle="Find relevant content using AI" icon="🔍" />
);

export const GenerationScene: React.FC<DemoVideoProps> = (props) => (
  <DemoScene {...props} title="AI Content Generation" subtitle="Generate high-quality content with GPT-4" icon="✨" />
);

export const ExportScene: React.FC<DemoVideoProps> = (props) => (
  <DemoScene {...props} title="Export Reports" subtitle="Download as PDF or DOCX" icon="📥" />
);
