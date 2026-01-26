import React from 'react';

interface LogoProps {
  size?: number;
  color?: string;
}

/**
 * Reportify Logo component
 * Simple SVG logo with customizable size and color
 */
export const Logo: React.FC<LogoProps> = ({ size = 100, color = '#3b82f6' }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Document icon with AI sparkle */}
      <rect
        x="20"
        y="10"
        width="60"
        height="80"
        rx="4"
        fill={color}
        opacity="0.2"
      />
      <rect
        x="20"
        y="10"
        width="60"
        height="80"
        rx="4"
        stroke={color}
        strokeWidth="3"
        fill="none"
      />
      
      {/* Document lines */}
      <line x1="30" y1="25" x2="70" y2="25" stroke={color} strokeWidth="2" strokeLinecap="round" />
      <line x1="30" y1="35" x2="70" y2="35" stroke={color} strokeWidth="2" strokeLinecap="round" />
      <line x1="30" y1="45" x2="60" y2="45" stroke={color} strokeWidth="2" strokeLinecap="round" />
      
      {/* AI Sparkle */}
      <circle cx="70" cy="70" r="15" fill={color} />
      <path
        d="M70 60 L72 68 L80 70 L72 72 L70 80 L68 72 L60 70 L68 68 Z"
        fill="white"
      />
    </svg>
  );
};
