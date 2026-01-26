import React from 'react';
import { Img, useCurrentFrame, useVideoConfig, spring } from 'remotion';

interface ScreenshotProps {
  src: string;
  alt: string;
  delay?: number; // Delay in seconds
  scale?: number;
  borderRadius?: number;
  style?: React.CSSProperties;
}

/**
 * Screenshot component with spring entrance animation
 * Following Remotion best practice: use spring() for natural motion
 */
export const Screenshot: React.FC<ScreenshotProps> = ({
  src,
  alt,
  delay = 0,
  scale = 1,
  borderRadius = 12,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Spring entrance animation with smooth config
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 200 }, // Smooth, no bounce
  });
  
  return (
    <Img
      src={src}
      alt={alt}
      style={{
        width: '100%',
        height: 'auto',
        borderRadius,
        transform: `scale(${entrance * scale})`,
        opacity: entrance,
        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
        ...style,
      }}
    />
  );
};
