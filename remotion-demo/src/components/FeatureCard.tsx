import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';

interface FeatureCardProps {
  icon: string; // Emoji or icon
  title: string;
  description: string;
  delay?: number; // Delay in seconds
  color?: string;
}

/**
 * FeatureCard component for highlighting key features
 * Following Remotion best practice: use spring() for entrance animations
 */
export const FeatureCard: React.FC<FeatureCardProps> = ({
  icon,
  title,
  description,
  delay = 0,
  color = '#3b82f6',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Spring entrance with snappy config
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 20, stiffness: 200 }, // Snappy, minimal bounce
  });
  
  return (
    <div
      style={{
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: 16,
        padding: 30,
        transform: `scale(${entrance}) translateY(${(1 - entrance) * 50}px)`,
        opacity: entrance,
        border: `2px solid ${color}`,
        backdropFilter: 'blur(10px)',
      }}
    >
      <div
        style={{
          fontSize: 48,
          marginBottom: 15,
        }}
      >
        {icon}
      </div>
      <h3
        style={{
          fontSize: 28,
          fontWeight: 'bold',
          color: '#f8fafc',
          marginBottom: 10,
          margin: 0,
        }}
      >
        {title}
      </h3>
      <p
        style={{
          fontSize: 20,
          color: '#cbd5e1',
          margin: 0,
          lineHeight: 1.5,
        }}
      >
        {description}
      </p>
    </div>
  );
};
