import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

interface CaptionProps {
  text: string;
  startFrame: number;
  endFrame: number;
}

/**
 * Caption component for accessibility
 * Positioned in lower third with fade in/out animations
 * Following Remotion best practice: all animations driven by useCurrentFrame()
 */
export const Caption: React.FC<CaptionProps> = ({ text, startFrame, endFrame }) => {
  const frame = useCurrentFrame();
  
  // Fade in at start
  const fadeInDuration = 10;
  const fadeOutDuration = 10;
  
  const opacity = interpolate(
    frame,
    [
      startFrame,
      startFrame + fadeInDuration,
      endFrame - fadeOutDuration,
      endFrame,
    ],
    [0, 1, 1, 0],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );
  
  // Only render if within time range
  if (frame < startFrame || frame > endFrame) {
    return null;
  }
  
  return (
    <div
      style={{
        position: 'absolute',
        bottom: 100,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '80%',
        maxWidth: 1200,
        opacity,
      }}
    >
      <div
        style={{
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: '15px 30px',
          borderRadius: 8,
          backdropFilter: 'blur(10px)',
        }}
      >
        <p
          style={{
            fontSize: 28,
            color: '#ffffff',
            margin: 0,
            textAlign: 'center',
            lineHeight: 1.4,
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};
