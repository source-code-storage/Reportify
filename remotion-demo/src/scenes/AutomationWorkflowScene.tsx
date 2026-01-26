import React from 'react';
import { AbsoluteFill } from 'remotion';
import { DemoVideoProps } from '../types';
import { AnimatedText } from '../components/AnimatedText';
import { AutomationFlow } from '../components/AutomationFlow';

/**
 * AutomationWorkflowScene - Shows n8n-style automation workflow
 */
export const AutomationWorkflowScene: React.FC<DemoVideoProps> = (props) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <AnimatedText
        text="Automated Client Acquisition"
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 20,
        }}
      />
      
      <AnimatedText
        text="From Lead to Proposal in Minutes"
        style={{
          fontSize: 28,
          color: props.primaryColor,
          textAlign: 'center',
          marginBottom: 60,
        }}
        startFrame={15}
      />
      
      <div style={{ flex: 1, position: 'relative' }}>
        <AutomationFlow color={props.primaryColor} />
      </div>
      
      {/* Bottom explanation */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-around',
          marginTop: 40,
        }}
      >
        <InfoBox
          icon="⚡"
          title="Instant"
          description="Respond to leads in seconds"
          color={props.primaryColor}
        />
        <InfoBox
          icon="🎯"
          title="Targeted"
          description="AI finds perfect matches"
          color={props.secondaryColor}
        />
        <InfoBox
          icon="📈"
          title="Scalable"
          description="Handle 100+ leads/day"
          color={props.accentColor}
        />
      </div>
    </AbsoluteFill>
  );
};

const InfoBox: React.FC<{
  icon: string;
  title: string;
  description: string;
  color: string;
}> = ({ icon, title, description, color }) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 10,
        padding: 20,
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: 12,
        border: `2px solid ${color}`,
        minWidth: 200,
      }}
    >
      <div style={{ fontSize: 40 }}>{icon}</div>
      <div style={{ fontSize: 24, fontWeight: 'bold', color: '#f8fafc' }}>{title}</div>
      <div style={{ fontSize: 16, color: '#94a3b8', textAlign: 'center' }}>{description}</div>
    </div>
  );
};
