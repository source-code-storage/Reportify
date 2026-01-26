import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

interface UIBrowserProps {
  title: string;
  children: React.ReactNode;
  delay?: number;
}

/**
 * UIBrowser component - simulates a browser window
 * Perfect for showing UI mockups and interactions
 */
export const UIBrowser: React.FC<UIBrowserProps> = ({ title, children, delay = 0 }) => {
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
        width: '100%',
        maxWidth: 1400,
        backgroundColor: '#1e293b',
        borderRadius: 16,
        overflow: 'hidden',
        boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
        transform: `scale(${entrance})`,
        opacity: entrance,
      }}
    >
      {/* Browser Header */}
      <div
        style={{
          height: 50,
          backgroundColor: '#0f172a',
          display: 'flex',
          alignItems: 'center',
          padding: '0 20px',
          gap: 10,
          borderBottom: '1px solid #334155',
        }}
      >
        {/* Browser Dots */}
        <div style={{ display: 'flex', gap: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#ef4444' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#f59e0b' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#10b981' }} />
        </div>
        
        {/* URL Bar */}
        <div
          style={{
            flex: 1,
            height: 32,
            backgroundColor: '#1e293b',
            borderRadius: 8,
            display: 'flex',
            alignItems: 'center',
            padding: '0 15px',
            fontSize: 14,
            color: '#94a3b8',
          }}
        >
          🔒 {title}
        </div>
      </div>
      
      {/* Browser Content */}
      <div style={{ backgroundColor: '#0f172a', minHeight: 600 }}>
        {children}
      </div>
    </div>
  );
};

interface ClickableButtonProps {
  text: string;
  onClick?: () => void;
  delay?: number;
  color?: string;
  icon?: string;
}

/**
 * ClickableButton - animated button with click effect
 */
export const ClickableButton: React.FC<ClickableButtonProps> = ({
  text,
  delay = 0,
  color = '#3b82f6',
  icon,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Button appears
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 200 },
  });
  
  // Click animation - happens 1 second after entrance
  const clickFrame = delay * fps + 30;
  const clickScale = spring({
    frame: frame - clickFrame,
    fps,
    config: { damping: 15, stiffness: 300 },
    durationInFrames: 20,
  });
  
  // Pulse effect during click
  const pulse = interpolate(
    frame,
    [clickFrame, clickFrame + 10, clickFrame + 20],
    [1, 1.1, 1],
    { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' }
  );
  
  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 10,
        padding: '15px 30px',
        backgroundColor: color,
        color: '#ffffff',
        borderRadius: 12,
        fontSize: 20,
        fontWeight: '600',
        cursor: 'pointer',
        opacity: entrance,
        transform: `scale(${entrance * pulse})`,
        boxShadow: frame > clickFrame ? '0 10px 30px rgba(59, 130, 246, 0.5)' : 'none',
      }}
    >
      {icon && <span style={{ fontSize: 24 }}>{icon}</span>}
      {text}
    </div>
  );
};

interface TabProps {
  label: string;
  isActive: boolean;
  delay?: number;
}

/**
 * Tab component for navigation
 */
export const Tab: React.FC<TabProps> = ({ label, isActive, delay = 0 }) => {
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
        padding: '15px 30px',
        fontSize: 18,
        fontWeight: '600',
        color: isActive ? '#3b82f6' : '#94a3b8',
        borderBottom: isActive ? '3px solid #3b82f6' : '3px solid transparent',
        cursor: 'pointer',
        opacity: entrance,
        transform: `translateY(${(1 - entrance) * -20}px)`,
      }}
    >
      {label}
    </div>
  );
};
