import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

interface FlowStepProps {
  number: number;
  title: string;
  icon: string;
  delay?: number;
  color?: string;
  isLast?: boolean;
}

/**
 * FlowStep component for diagram-style visualization
 * Shows a step in the workflow with connecting arrows
 */
export const FlowStep: React.FC<FlowStepProps> = ({
  number,
  title,
  icon,
  delay = 0,
  color = '#3b82f6',
  isLast = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Spring entrance for the step
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Arrow animation - grows after step appears
  const arrowProgress = interpolate(
    frame,
    [delay * fps + 15, delay * fps + 30],
    [0, 1],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
    }
  );
  
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 20,
        opacity: entrance,
        transform: `scale(${entrance})`,
      }}
    >
      {/* Step Circle */}
      <div
        style={{
          width: 180,
          height: 180,
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          border: `4px solid ${color}`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 10,
          position: 'relative',
        }}
      >
        {/* Step Number */}
        <div
          style={{
            position: 'absolute',
            top: -15,
            left: -15,
            width: 40,
            height: 40,
            borderRadius: '50%',
            backgroundColor: color,
            color: '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 20,
            fontWeight: 'bold',
          }}
        >
          {number}
        </div>
        
        {/* Icon */}
        <div style={{ fontSize: 60 }}>{icon}</div>
        
        {/* Title */}
        <div
          style={{
            fontSize: 18,
            fontWeight: '600',
            color: '#f8fafc',
            textAlign: 'center',
            padding: '0 15px',
          }}
        >
          {title}
        </div>
      </div>
      
      {/* Connecting Arrow (if not last) */}
      {!isLast && (
        <div
          style={{
            width: 4,
            height: 60,
            backgroundColor: color,
            position: 'relative',
            transformOrigin: 'top',
            transform: `scaleY(${arrowProgress})`,
          }}
        >
          {/* Arrow head */}
          <div
            style={{
              position: 'absolute',
              bottom: -10,
              left: '50%',
              transform: 'translateX(-50%)',
              width: 0,
              height: 0,
              borderLeft: '10px solid transparent',
              borderRight: '10px solid transparent',
              borderTop: `15px solid ${color}`,
              opacity: arrowProgress,
            }}
          />
        </div>
      )}
    </div>
  );
};

interface FlowDiagramProps {
  steps: Array<{
    title: string;
    icon: string;
  }>;
  color?: string;
  title?: string;
}

/**
 * FlowDiagram component - displays a vertical flow of steps
 */
export const FlowDiagram: React.FC<FlowDiagramProps> = ({
  steps,
  color = '#3b82f6',
  title,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 0,
      }}
    >
      {title && (
        <h2
          style={{
            fontSize: 48,
            fontWeight: 'bold',
            color: '#f8fafc',
            marginBottom: 60,
            textAlign: 'center',
          }}
        >
          {title}
        </h2>
      )}
      
      {steps.map((step, index) => (
        <FlowStep
          key={index}
          number={index + 1}
          title={step.title}
          icon={step.icon}
          delay={index * 0.4}
          color={color}
          isLast={index === steps.length - 1}
        />
      ))}
    </div>
  );
};
