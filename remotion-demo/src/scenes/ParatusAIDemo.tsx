import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Img, staticFile } from 'remotion';
import { DemoVideoProps } from '../types';
import { AnimatedText } from '../components/AnimatedText';

/**
 * ParatusAIDemo - Shows actual app screenshots with smooth transitions
 */
export const ParatusAIDemo: React.FC<DemoVideoProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Determine which screenshot to show based on time
  // Each screenshot shows for 5 seconds
  const screenshotIndex = Math.floor(frame / (5 * fps));
  
  const screenshots = [
    {
      src: staticFile('images/paratusaia login.png'),
      title: 'Secure Login',
      description: 'Access your AI-powered client acquisition dashboard'
    },
    {
      src: staticFile('images/main app page paratusai.png'),
      title: 'Main Dashboard',
      description: 'Manage leads, projects, and automation workflows'
    },
    {
      src: staticFile('images/paratusai app.png'),
      title: 'Lead Management',
      description: 'Track and organize potential clients'
    },
    {
      src: staticFile('images/paratusai app 1.png'),
      title: 'Workflow Builder',
      description: 'Create custom automation flows for client acquisition'
    },
    {
      src: staticFile('images/paratusai breifing generation .png'),
      title: 'AI Briefing Generation',
      description: 'Generate professional project briefs automatically'
    },
  ];
  
  const currentScreenshot = screenshots[Math.min(screenshotIndex, screenshots.length - 1)];
  
  // Fade transition between screenshots
  const fadeProgress = (frame % (5 * fps)) / fps;
  const fadeOpacity = fadeProgress < 0.5 ? 1 : interpolate(fadeProgress, [4.5, 5], [1, 0], {
    extrapolateRight: 'clamp',
    extrapolateLeft: 'clamp',
  });
  
  // Scale animation for screenshot
  const scale = interpolate(
    frame % (5 * fps),
    [0, 0.5 * fps],
    [0.95, 1],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
    }
  );
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {/* Title */}
      <AnimatedText
        text={currentScreenshot.title}
        style={{
          fontSize: 48,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 20,
        }}
        key={screenshotIndex}
      />
      
      {/* Description */}
      <div
        style={{
          fontSize: 28,
          color: props.primaryColor,
          textAlign: 'center',
          marginBottom: 40,
          opacity: fadeOpacity,
        }}
      >
        {currentScreenshot.description}
      </div>
      
      {/* Screenshot with browser frame */}
      <div
        style={{
          width: '90%',
          maxWidth: 1400,
          backgroundColor: '#1e293b',
          borderRadius: 16,
          overflow: 'hidden',
          boxShadow: `0 25px 50px ${props.primaryColor}40`,
          opacity: fadeOpacity,
          transform: `scale(${scale})`,
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
            🔒 paratusai.com
          </div>
        </div>
        
        {/* Screenshot */}
        <div style={{ position: 'relative', width: '100%', height: 700, overflow: 'hidden' }}>
          <Img
            src={currentScreenshot.src}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
          />
        </div>
      </div>
      
      {/* Progress indicator */}
      <div style={{ display: 'flex', gap: 10, marginTop: 30 }}>
        {screenshots.map((_, index) => (
          <div
            key={index}
            style={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              backgroundColor: index === screenshotIndex ? props.primaryColor : '#334155',
              transition: 'background-color 0.3s',
            }}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};
