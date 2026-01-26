import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

/**
 * AutomationFlow - Shows n8n-style automation workflow
 * Animated nodes with data flowing through connections
 */
export const AutomationFlow: React.FC<{ color?: string }> = ({ color = '#10b981' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Node animations - staggered entrance
  const node1 = spring({
    frame: frame,
    fps,
    config: { damping: 200 },
  });
  
  const node2 = spring({
    frame: frame - 0.5 * fps,
    fps,
    config: { damping: 200 },
  });
  
  const node3 = spring({
    frame: frame - 1 * fps,
    fps,
    config: { damping: 200 },
  });
  
  const node4 = spring({
    frame: frame - 1.5 * fps,
    fps,
    config: { damping: 200 },
  });
  
  const node5 = spring({
    frame: frame - 2 * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Data flow animations - particles moving through connections
  const flow1 = interpolate(frame, [0.5 * fps, 2 * fps], [0, 1], { 
    extrapolateRight: 'clamp', 
    extrapolateLeft: 'clamp' 
  });
  
  const flow2 = interpolate(frame, [1 * fps, 2.5 * fps], [0, 1], { 
    extrapolateRight: 'clamp', 
    extrapolateLeft: 'clamp' 
  });
  
  const flow3 = interpolate(frame, [1.5 * fps, 3 * fps], [0, 1], { 
    extrapolateRight: 'clamp', 
    extrapolateLeft: 'clamp' 
  });
  
  const flow4 = interpolate(frame, [2 * fps, 3.5 * fps], [0, 1], { 
    extrapolateRight: 'clamp', 
    extrapolateLeft: 'clamp' 
  });
  
  // Pulsing effect for active nodes
  const pulse = Math.sin(frame / 10) * 0.1 + 1;
  
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative', padding: 80 }}>
      <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0 }}>
        <defs>
          {/* Arrow marker */}
          <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill={color} />
          </marker>
          
          {/* Gradient for flow effect */}
          <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={color} stopOpacity="0" />
            <stop offset="50%" stopColor={color} stopOpacity="1" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </linearGradient>
        </defs>
        
        {/* Connection lines */}
        <line
          x1="20%" y1="30%" x2="40%" y2="30%"
          stroke="#334155"
          strokeWidth="3"
          opacity={node2}
        />
        <line
          x1="50%" y1="30%" x2="70%" y2="30%"
          stroke="#334155"
          strokeWidth="3"
          opacity={node3}
        />
        <line
          x1="40%" y1="40%" x2="40%" y2="60%"
          stroke="#334155"
          strokeWidth="3"
          opacity={node4}
        />
        <line
          x1="50%" y1="70%" x2="70%" y2="70%"
          stroke="#334155"
          strokeWidth="3"
          opacity={node5}
        />
        
        {/* Animated data flow particles */}
        {node2 > 0.5 && (
          <circle
            cx={`${20 + (flow1 * 20)}%`}
            cy="30%"
            r="6"
            fill={color}
            opacity={flow1 * (1 - flow1) * 4}
          />
        )}
        
        {node3 > 0.5 && (
          <circle
            cx={`${40 + (flow2 * 20)}%`}
            cy="30%"
            r="6"
            fill={color}
            opacity={flow2 * (1 - flow2) * 4}
          />
        )}
        
        {node4 > 0.5 && (
          <circle
            cx="40%"
            cy={`${40 + (flow3 * 20)}%`}
            r="6"
            fill={color}
            opacity={flow3 * (1 - flow3) * 4}
          />
        )}
        
        {node5 > 0.5 && (
          <circle
            cx={`${50 + (flow4 * 20)}%`}
            cy="70%"
            r="6"
            fill={color}
            opacity={flow4 * (1 - flow4) * 4}
          />
        )}
      </svg>
      
      {/* Node 1: Trigger */}
      <AutomationNode
        x="10%"
        y="25%"
        icon="⚡"
        title="Trigger"
        subtitle="New Lead Detected"
        opacity={node1}
        color={color}
        scale={pulse}
      />
      
      {/* Node 2: AI Analysis */}
      <AutomationNode
        x="40%"
        y="25%"
        icon="🧠"
        title="AI Analysis"
        subtitle="Analyze Requirements"
        opacity={node2}
        color="#3b82f6"
        scale={1}
      />
      
      {/* Node 3: Generate Brief */}
      <AutomationNode
        x="70%"
        y="25%"
        icon="📝"
        title="Generate"
        subtitle="Create Project Brief"
        opacity={node3}
        color="#8b5cf6"
        scale={1}
      />
      
      {/* Node 4: Enrich Data */}
      <AutomationNode
        x="40%"
        y="65%"
        icon="🔍"
        title="Enrich"
        subtitle="Find Contact Info"
        opacity={node4}
        color="#06b6d4"
        scale={1}
      />
      
      {/* Node 5: Send Proposal */}
      <AutomationNode
        x="70%"
        y="65%"
        icon="📧"
        title="Send"
        subtitle="Email Proposal"
        opacity={node5}
        color={color}
        scale={1}
      />
    </div>
  );
};

interface AutomationNodeProps {
  x: string;
  y: string;
  icon: string;
  title: string;
  subtitle: string;
  opacity: number;
  color: string;
  scale: number;
}

const AutomationNode: React.FC<AutomationNodeProps> = ({ 
  x, 
  y, 
  icon, 
  title, 
  subtitle, 
  opacity, 
  color,
  scale 
}) => {
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: `translate(-50%, -50%) scale(${opacity * scale})`,
        opacity,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 10,
      }}
    >
      {/* Node circle */}
      <div
        style={{
          width: 120,
          height: 120,
          borderRadius: '50%',
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          border: `4px solid ${color}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 48,
          boxShadow: `0 0 30px ${color}40`,
        }}
      >
        {icon}
      </div>
      
      {/* Node label */}
      <div style={{ textAlign: 'center', minWidth: 150 }}>
        <div style={{ fontSize: 22, fontWeight: 'bold', color: '#f8fafc' }}>{title}</div>
        <div style={{ fontSize: 16, color: '#94a3b8' }}>{subtitle}</div>
      </div>
    </div>
  );
};
