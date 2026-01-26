import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

/**
 * RAGVisualization - Shows how RAG (Retrieval Augmented Generation) works
 * Animated data flow diagram
 */
export const RAGVisualization: React.FC<{ color?: string }> = ({ color = '#3b82f6' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Step 1: Document Upload (0-1s)
  const step1 = spring({
    frame: frame,
    fps,
    config: { damping: 200 },
  });
  
  // Step 2: Embedding Generation (1-2s)
  const step2 = spring({
    frame: frame - 1 * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Step 3: Vector Storage (2-3s)
  const step3 = spring({
    frame: frame - 2 * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Step 4: Query (3-4s)
  const step4 = spring({
    frame: frame - 3 * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Step 5: Retrieval (4-5s)
  const step5 = spring({
    frame: frame - 4 * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Step 6: Generation (5-6s)
  const step6 = spring({
    frame: frame - 5 * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Data flow animations
  const flow1 = interpolate(frame, [0.5 * fps, 1.5 * fps], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
  const flow2 = interpolate(frame, [1.5 * fps, 2.5 * fps], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
  const flow3 = interpolate(frame, [3.5 * fps, 4.5 * fps], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
  const flow4 = interpolate(frame, [4.5 * fps, 5.5 * fps], [0, 1], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
  
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative', padding: 60 }}>
      <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0 }}>
        {/* Flow lines */}
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill={color} />
          </marker>
        </defs>
        
        {/* Document to Embedding */}
        <line
          x1="20%" y1="25%" x2="50%" y2="25%"
          stroke={color}
          strokeWidth="3"
          strokeDasharray="10,5"
          strokeDashoffset={300 * (1 - flow1)}
          markerEnd="url(#arrowhead)"
          opacity={step2}
        />
        
        {/* Embedding to Vector DB */}
        <line
          x1="50%" y1="35%" x2="50%" y2="55%"
          stroke={color}
          strokeWidth="3"
          strokeDasharray="10,5"
          strokeDashoffset={200 * (1 - flow2)}
          markerEnd="url(#arrowhead)"
          opacity={step3}
        />
        
        {/* Query to Vector DB */}
        <line
          x1="20%" y1="75%" x2="40%" y2="65%"
          stroke={color}
          strokeWidth="3"
          strokeDasharray="10,5"
          strokeDashoffset={200 * (1 - flow3)}
          markerEnd="url(#arrowhead)"
          opacity={step5}
        />
        
        {/* Vector DB to GPT-4 */}
        <line
          x1="60%" y1="65%" x2="80%" y2="75%"
          stroke={color}
          strokeWidth="3"
          strokeDasharray="10,5"
          strokeDashoffset={200 * (1 - flow4)}
          markerEnd="url(#arrowhead)"
          opacity={step6}
        />
      </svg>
      
      {/* Step 1: Document Upload */}
      <RAGNode
        x="10%"
        y="20%"
        icon="📄"
        title="Your Documents"
        subtitle="PDFs, Notes, Research"
        opacity={step1}
        color={color}
      />
      
      {/* Step 2: Embedding Model */}
      <RAGNode
        x="50%"
        y="20%"
        icon="🧠"
        title="Embedding Model"
        subtitle="Sentence Transformers"
        opacity={step2}
        color={color}
      />
      
      {/* Step 3: Vector Database */}
      <RAGNode
        x="50%"
        y="60%"
        icon="🗄️"
        title="Vector Database"
        subtitle="Qdrant (768D vectors)"
        opacity={step3}
        color={color}
      />
      
      {/* Step 4: User Query */}
      <RAGNode
        x="10%"
        y="70%"
        icon="🔍"
        title="Your Query"
        subtitle="Search for content"
        opacity={step4}
        color="#8b5cf6"
      />
      
      {/* Step 5: Retrieved Context */}
      <RAGNode
        x="50%"
        y="80%"
        icon="📚"
        title="Retrieved Context"
        subtitle="Most relevant chunks"
        opacity={step5}
        color="#06b6d4"
      />
      
      {/* Step 6: GPT-4 Generation */}
      <RAGNode
        x="80%"
        y="70%"
        icon="✨"
        title="GPT-4 Generation"
        subtitle="Context-aware content"
        opacity={step6}
        color="#10b981"
      />
    </div>
  );
};

interface RAGNodeProps {
  x: string;
  y: string;
  icon: string;
  title: string;
  subtitle: string;
  opacity: number;
  color: string;
}

const RAGNode: React.FC<RAGNodeProps> = ({ x, y, icon, title, subtitle, opacity, color }) => {
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: 'translate(-50%, -50%)',
        opacity,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 10,
      }}
    >
      <div
        style={{
          width: 100,
          height: 100,
          borderRadius: '50%',
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          border: `3px solid ${color}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 40,
        }}
      >
        {icon}
      </div>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: 20, fontWeight: 'bold', color: '#f8fafc' }}>{title}</div>
        <div style={{ fontSize: 16, color: '#94a3b8' }}>{subtitle}</div>
      </div>
    </div>
  );
};
