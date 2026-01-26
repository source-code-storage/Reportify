import React from 'react';
import { AbsoluteFill } from 'remotion';
import { DemoVideoProps } from '../types';
import { FlowDiagram } from '../components/FlowDiagram';
import { AnimatedText } from '../components/AnimatedText';

/**
 * Workflow Scene - Shows the Reportify workflow as a flowing diagram
 */
export const WorkflowScene: React.FC<DemoVideoProps> = (props) => {
  const workflowSteps = [
    { title: 'Upload Template', icon: '📄' },
    { title: 'Extract Sections', icon: '✂️' },
    { title: 'Upload Notes', icon: '📚' },
    { title: 'Generate Embeddings', icon: '🧠' },
    { title: 'Search Content', icon: '🔍' },
    { title: 'Generate with AI', icon: '✨' },
    { title: 'Review & Edit', icon: '✏️' },
    { title: 'Export Report', icon: '📥' },
  ];
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        padding: 60,
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      <AnimatedText
        text="How Reportify Works"
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 40,
          position: 'absolute',
          top: 40,
          left: 0,
          right: 0,
        }}
      />
      
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100%',
          paddingTop: 120,
          position: 'relative',
        }}
      >
        {/* Connecting lines background */}
        <svg
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
          }}
        >
          {/* Horizontal lines connecting steps */}
          <line x1="25%" y1="35%" x2="75%" y2="35%" stroke={props.primaryColor} strokeWidth="3" opacity="0.3" strokeDasharray="10,5" />
          <line x1="25%" y1="65%" x2="75%" y2="65%" stroke={props.secondaryColor} strokeWidth="3" opacity="0.3" strokeDasharray="10,5" />
          
          {/* Vertical connecting lines */}
          <line x1="87%" y1="35%" x2="87%" y2="65%" stroke={props.accentColor} strokeWidth="3" opacity="0.3" strokeDasharray="10,5" />
        </svg>
        
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 40,
            maxWidth: 1600,
            position: 'relative',
            zIndex: 1,
          }}
        >
          {workflowSteps.map((step, index) => (
            <FlowStep
              key={index}
              number={index + 1}
              title={step.title}
              icon={step.icon}
              delay={index * 0.3}
              color={
                index % 3 === 0
                  ? props.primaryColor
                  : index % 3 === 1
                  ? props.secondaryColor
                  : props.accentColor
              }
            />
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Helper component for grid-based flow
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';

interface FlowStepProps {
  number: number;
  title: string;
  icon: string;
  delay: number;
  color: string;
}

const FlowStep: React.FC<FlowStepProps> = ({ number, title, icon, delay, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 200 },
  });
  
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 15,
        opacity: entrance,
        transform: `scale(${entrance}) translateY(${(1 - entrance) * 30}px)`,
      }}
    >
      {/* Step Circle */}
      <div
        style={{
          width: 140,
          height: 140,
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          border: `3px solid ${color}`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 8,
          position: 'relative',
        }}
      >
        {/* Step Number Badge */}
        <div
          style={{
            position: 'absolute',
            top: -12,
            right: -12,
            width: 36,
            height: 36,
            borderRadius: '50%',
            backgroundColor: color,
            color: '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 18,
            fontWeight: 'bold',
            border: '3px solid #0f172a',
          }}
        >
          {number}
        </div>
        
        {/* Icon */}
        <div style={{ fontSize: 50 }}>{icon}</div>
      </div>
      
      {/* Title */}
      <div
        style={{
          fontSize: 20,
          fontWeight: '600',
          color: '#f8fafc',
          textAlign: 'center',
          maxWidth: 140,
          lineHeight: 1.3,
        }}
      >
        {title}
      </div>
    </div>
  );
};
