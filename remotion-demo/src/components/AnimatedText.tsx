import React, { CSSProperties } from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

interface AnimatedTextProps {
  text: string;
  style?: CSSProperties;
  staggerDelay?: number; // Delay between each character in frames
  startFrame?: number; // When to start the animation
}

/**
 * AnimatedText component with optional staggered character animation
 * Following Remotion best practice: all animations driven by useCurrentFrame()
 */
export const AnimatedText: React.FC<AnimatedTextProps> = ({
  text,
  style,
  staggerDelay = 0,
  startFrame = 0,
}) => {
  const frame = useCurrentFrame();
  
  if (staggerDelay === 0) {
    // Simple text without stagger - just fade in
    const opacity = interpolate(
      frame,
      [startFrame, startFrame + 20],
      [0, 1],
      {
        extrapolateRight: 'clamp',
        extrapolateLeft: 'clamp',
      }
    );
    
    return <div style={{ ...style, opacity }}>{text}</div>;
  }
  
  // Staggered character animation
  return (
    <div style={{ ...style, display: 'inline-block' }}>
      {text.split('').map((char, index) => {
        const charOpacity = interpolate(
          frame,
          [startFrame + index * staggerDelay, startFrame + index * staggerDelay + 10],
          [0, 1],
          {
            extrapolateRight: 'clamp',
            extrapolateLeft: 'clamp',
          }
        );
        
        return (
          <span key={index} style={{ opacity: charOpacity }}>
            {char === ' ' ? '\u00A0' : char}
          </span>
        );
      })}
    </div>
  );
};
