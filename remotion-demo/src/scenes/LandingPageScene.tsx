import React from 'react';
import { AbsoluteFill, useVideoConfig } from 'remotion';
import { DemoVideoProps } from '../types';
import { FeatureCard } from '../components/FeatureCard';
import { AnimatedText } from '../components/AnimatedText';

/**
 * Landing Page Scene
 * Shows key features of Reportify
 */
export const LandingPageScene: React.FC<DemoVideoProps> = (props) => {
  const { fps } = useVideoConfig();
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        padding: 60,
        justifyContent: 'center',
      }}
    >
      <AnimatedText
        text="How ParatusAI Helps You"
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 60,
        }}
      />
      
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 40,
          maxWidth: 1400,
          margin: '0 auto',
        }}
      >
        <FeatureCard
          icon="🎯"
          title="AI Lead Generation"
          description="Automatically find potential clients who need automation"
          delay={0.5}
          color={props.primaryColor}
        />
        <FeatureCard
          icon="📝"
          title="Smart Briefing Creation"
          description="Generate professional project briefs in seconds"
          delay={0.8}
          color={props.secondaryColor}
        />
        <FeatureCard
          icon="🤖"
          title="Workflow Automation"
          description="Automate your client acquisition process end-to-end"
          delay={1.1}
          color={props.accentColor}
        />
        <FeatureCard
          icon="📊"
          title="Client Management"
          description="Track leads, proposals, and projects in one place"
          delay={1.4}
          color={props.primaryColor}
        />
      </div>
    </AbsoluteFill>
  );
};
