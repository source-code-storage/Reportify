import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { DemoVideoProps } from '../types';
import { Logo } from '../components/Logo';
import { AnimatedText } from '../components/AnimatedText';

/**
 * Introduction Scene
 * Shows logo, tagline, and problem statement
 * Following Remotion best practice: all animations driven by useCurrentFrame()
 */
export const IntroScene: React.FC<DemoVideoProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Logo animation - spring entrance with smooth config
  const logoScale = spring({
    frame,
    fps,
    config: { damping: 200 }, // Smooth, no bounce
  });
  
  // Tagline animation - delayed fade in
  const taglineOpacity = interpolate(
    frame,
    [1 * fps, 2 * fps],
    [0, 1],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
    }
  );
  
  // Problem statement - further delayed
  const problemOpacity = interpolate(
    frame,
    [2.5 * fps, 3.5 * fps],
    [0, 1],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
    }
  );
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      {/* Logo */}
      <div style={{ transform: `scale(${logoScale})`, marginBottom: 40 }}>
        <Logo size={200} color={props.primaryColor} />
      </div>
      
      {/* App Name */}
      <h1
        style={{
          fontSize: 72,
          fontWeight: 'bold',
          color: props.textColor,
          opacity: taglineOpacity,
          margin: 0,
          marginBottom: 20,
        }}
      >
        {props.appName}
      </h1>
      
      {/* Tagline */}
      <AnimatedText
        text={props.tagline}
        style={{
          fontSize: 42,
          fontWeight: '600',
          color: props.secondaryColor,
          textAlign: 'center',
          marginBottom: 60,
        }}
        startFrame={1 * fps}
      />
      
      {/* Problem Statement */}
      <div
        style={{
          opacity: problemOpacity,
          maxWidth: 900,
          textAlign: 'center',
        }}
      >
        <p
          style={{
            fontSize: 32,
            color: props.textColor,
            margin: 0,
            lineHeight: 1.5,
          }}
        >
          Finding clients as an n8n freelancer is challenging.
        </p>
        <p
          style={{
            fontSize: 28,
            color: props.accentColor,
            margin: 0,
            marginTop: 20,
          }}
        >
          Let AI help you get more clients, automatically.
        </p>
      </div>
    </AbsoluteFill>
  );
};
