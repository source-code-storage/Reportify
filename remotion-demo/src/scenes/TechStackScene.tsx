import React from 'react';
import { AbsoluteFill } from 'remotion';
import { DemoVideoProps } from '../types';
import { TechIcon } from '../components/TechIcon';
import { AnimatedText } from '../components/AnimatedText';

/**
 * Tech Stack Scene
 * Shows the technology stack used in Reportify
 */
export const TechStackScene: React.FC<DemoVideoProps> = (props) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        padding: 60,
        justifyContent: 'center',
      }}
    >
      <AnimatedText
        text="Powered by Modern Technology"
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 80,
        }}
      />
      
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 60,
          maxWidth: 1200,
          margin: '0 auto',
        }}
      >
        <TechIcon name="n8n" icon="🔗" delay={0.3} color={props.primaryColor} />
        <TechIcon name="React" icon="⚛️" delay={0.5} color={props.secondaryColor} />
        <TechIcon name="Node.js" icon="🟢" delay={0.7} color={props.accentColor} />
        <TechIcon name="MongoDB" icon="🍃" delay={0.9} color={props.primaryColor} />
        <TechIcon name="GPT-4" icon="🤖" delay={1.1} color={props.secondaryColor} />
        <TechIcon name="OpenAI" icon="✨" delay={1.3} color={props.accentColor} />
        <TechIcon name="Docker" icon="🐳" delay={1.5} color={props.primaryColor} />
        <TechIcon name="TypeScript" icon="📘" delay={1.7} color={props.secondaryColor} />
      </div>
    </AbsoluteFill>
  );
};
