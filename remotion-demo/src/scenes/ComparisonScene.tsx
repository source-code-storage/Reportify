import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { DemoVideoProps } from '../types';
import { AnimatedText } from '../components/AnimatedText';

/**
 * ComparisonScene - Shows why Reportify is better than Overleaf
 */
export const ComparisonScene: React.FC<DemoVideoProps> = (props) => {
  const frame = useCurrentFrame();
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
        text="Why Choose ParatusAI?"
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: props.textColor,
          textAlign: 'center',
          marginBottom: 80,
        }}
      />
      
      <div style={{ display: 'flex', gap: 60, maxWidth: 1600, margin: '0 auto' }}>
        {/* Traditional Column */}
        <div style={{ flex: 1 }}>
          <ComparisonCard
            title="Traditional Methods"
            subtitle="(Cold Emails, Upwork)"
            icon="📧"
            delay={0.3}
            color="#64748b"
            items={[
              { text: 'Manual lead research', icon: '🔍', negative: true },
              { text: 'Generic proposals', icon: '📄', negative: true },
              { text: 'Low response rates', icon: '📉', negative: true },
              { text: 'Time-consuming', icon: '⏰', negative: true },
              { text: 'Inconsistent results', icon: '❌', negative: true },
            ]}
          />
        </div>
        
        {/* VS Divider */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <VSBadge delay={0.6} />
        </div>
        
        {/* ParatusAI Column */}
        <div style={{ flex: 1 }}>
          <ComparisonCard
            title="ParatusAI"
            subtitle="AI-Powered Automation"
            icon="🤖"
            delay={0.9}
            color={props.primaryColor}
            items={[
              { text: 'AI finds perfect leads', icon: '🎯', negative: false },
              { text: 'Custom briefs per client', icon: '📝', negative: false },
              { text: '10x higher response rate', icon: '📈', negative: false },
              { text: 'Fully automated', icon: '⚡', negative: false },
              { text: 'Consistent pipeline', icon: '✅', negative: false },
            ]}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

interface ComparisonCardProps {
  title: string;
  subtitle: string;
  icon: string;
  delay: number;
  color: string;
  items: Array<{ text: string; icon: string; negative: boolean }>;
}

const ComparisonCard: React.FC<ComparisonCardProps> = ({
  title,
  subtitle,
  icon,
  delay,
  color,
  items,
}) => {
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
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: 20,
        padding: 40,
        border: `3px solid ${color}`,
        opacity: entrance,
        transform: `scale(${entrance}) translateY(${(1 - entrance) * 50}px)`,
      }}
    >
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <div style={{ fontSize: 60, marginBottom: 15 }}>{icon}</div>
        <h3 style={{ fontSize: 32, fontWeight: 'bold', color: '#f8fafc', margin: 0 }}>
          {title}
        </h3>
        <p style={{ fontSize: 20, color: '#94a3b8', margin: '10px 0 0 0' }}>{subtitle}</p>
      </div>
      
      {/* Features List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        {items.map((item, index) => (
          <ComparisonItem
            key={index}
            text={item.text}
            icon={item.icon}
            negative={item.negative}
            delay={delay + 0.2 + index * 0.1}
          />
        ))}
      </div>
    </div>
  );
};

interface ComparisonItemProps {
  text: string;
  icon: string;
  negative: boolean;
  delay: number;
}

const ComparisonItem: React.FC<ComparisonItemProps> = ({ text, icon, negative, delay }) => {
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
        display: 'flex',
        alignItems: 'center',
        gap: 15,
        padding: '15px 20px',
        backgroundColor: negative
          ? 'rgba(239, 68, 68, 0.1)'
          : 'rgba(16, 185, 129, 0.1)',
        borderRadius: 12,
        border: negative ? '2px solid #ef4444' : '2px solid #10b981',
        opacity: entrance,
        transform: `translateX(${(1 - entrance) * (negative ? -30 : 30)}px)`,
      }}
    >
      <span style={{ fontSize: 28 }}>{icon}</span>
      <span
        style={{
          fontSize: 20,
          color: '#f8fafc',
          fontWeight: '500',
        }}
      >
        {text}
      </span>
    </div>
  );
};

const VSBadge: React.FC<{ delay: number }> = ({ delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const entrance = spring({
    frame: frame - delay * fps,
    fps,
    config: { damping: 8 }, // Bouncy
  });
  
  return (
    <div
      style={{
        width: 100,
        height: 100,
        borderRadius: '50%',
        backgroundColor: '#8b5cf6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 36,
        fontWeight: 'bold',
        color: '#ffffff',
        transform: `scale(${entrance}) rotate(${entrance * 360}deg)`,
        boxShadow: '0 10px 40px rgba(139, 92, 246, 0.5)',
      }}
    >
      VS
    </div>
  );
};
