import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';

interface TechIconProps {
  name: string;
  icon: string; // Emoji or text representation
  delay?: number; // Delay in seconds
  color?: string;
}

/**
 * TechIcon component for displaying technology stack
 * Following Remotion best practice: use spring() for bouncy entrance
 */
export const TechIcon: React.FC<TechIconProps> = ({
  name,
  icon,
  delay = 0,
  color = '#3b82f6',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Bouncy entrance for playful feel
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 8 }, // Bouncy entrance
  });
  
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 10,
        transform: `scale(${entrance})`,
        opacity: entrance,
      }}
    >
      <div
        style={{
          width: 80,
          height: 80,
          borderRadius: 16,
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          border: `2px solid ${color}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 40,
        }}
      >
        {icon}
      </div>
      <span
        style={{
          fontSize: 18,
          color: '#f8fafc',
          fontWeight: '600',
          textAlign: 'center',
        }}
      >
        {name}
      </span>
    </div>
  );
};
