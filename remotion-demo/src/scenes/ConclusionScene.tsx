import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { DemoVideoProps } from '../types';
import { Logo } from '../components/Logo';
import { AnimatedText } from '../components/AnimatedText';

/**
 * Conclusion Scene
 * Shows summary, URLs, and call-to-action
 */
export const ConclusionScene: React.FC<DemoVideoProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const logoScale = spring({
    frame,
    fps,
    config: { damping: 200 },
  });
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <div style={{ transform: `scale(${logoScale * 0.8})`, marginBottom: 40 }}>
        <Logo size={150} color={props.primaryColor} />
      </div>
      
      <h1
        style={{
          fontSize: 64,
          fontWeight: 'bold',
          color: props.textColor,
          margin: 0,
          marginBottom: 30,
        }}
      >
        {props.appName}
      </h1>
      
      <AnimatedText
        text="Transform Your Report Writing with AI"
        style={{
          fontSize: 36,
          color: props.secondaryColor,
          textAlign: 'center',
          marginBottom: 60,
        }}
        startFrame={0.5 * fps}
      />
      
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 30,
          alignItems: 'center',
        }}
      >
        <div
          style={{
            fontSize: 48,
            color: props.textColor,
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            padding: '30px 60px',
            borderRadius: 20,
            border: `3px solid ${props.primaryColor}`,
            fontWeight: '600',
            textAlign: 'center',
          }}
        >
          Made for the Kiro Hackathon ❤️
        </div>
        
        <div
          style={{
            fontSize: 32,
            color: props.accentColor,
            marginTop: 20,
            fontWeight: '600',
            textAlign: 'center',
          }}
        >
          Built with Kiro CLI
        </div>
      </div>
    </AbsoluteFill>
  );
};
