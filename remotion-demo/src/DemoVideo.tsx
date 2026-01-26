import React from 'react';
import { AbsoluteFill, Audio, useVideoConfig } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { DemoVideoProps } from './types';
import { IntroScene } from './scenes/IntroScene';
import { LandingPageScene } from './scenes/LandingPageScene';
import { TechStackScene } from './scenes/TechStackScene';
import { ConclusionScene } from './scenes/ConclusionScene';
import { AutomationWorkflowScene } from './scenes/AutomationWorkflowScene';
import { ComparisonScene } from './scenes/ComparisonScene';
import { ParatusAIDemo } from './scenes/ParatusAIDemo';

/**
 * Main DemoVideo Composition for ParatusAI
 * Following Remotion best practices:
 * - Use TransitionSeries for smooth scene transitions
 * - Convert seconds to frames using fps
 * - Use premountFor to load scenes before they appear
 */
export const DemoVideo: React.FC<DemoVideoProps> = (props) => {
  const { fps } = useVideoConfig();
  
  // Convert seconds to frames
  // Following Remotion best practice: always multiply seconds by fps
  const toFrames = (seconds: number) => Math.round(seconds * fps);
  const transitionFrames = toFrames(props.transitionDuration);
  
  return (
    <AbsoluteFill style={{ backgroundColor: props.backgroundColor }}>
      {/* Background music (if provided) */}
      {props.backgroundMusicUrl && (
        <Audio src={props.backgroundMusicUrl} volume={props.musicVolume} />
      )}
      
      {/* Scene transitions using TransitionSeries */}
      <TransitionSeries>
        {/* Introduction Scene */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.introDuration)}>
          <IntroScene {...props} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: transitionFrames })}
        />
        
        {/* Landing Page Scene - Key Features */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.landingPageDuration)}>
          <LandingPageScene {...props} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition
          presentation={slide({ direction: 'from-right' })}
          timing={linearTiming({ durationInFrames: transitionFrames })}
        />
        
        {/* Automation Workflow Scene - Shows the automation flow */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.authDuration + props.reportCreationDuration)}>
          <AutomationWorkflowScene {...props} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: transitionFrames })}
        />
        
        {/* ParatusAI Demo - Shows actual app screenshots */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.uploadDuration + props.searchDuration + props.generationDuration)}>
          <ParatusAIDemo {...props} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition
          presentation={slide({ direction: 'from-right' })}
          timing={linearTiming({ durationInFrames: transitionFrames })}
        />
        
        {/* Comparison - Why ParatusAI vs Traditional Methods */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.exportDuration)}>
          <ComparisonScene {...props} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: transitionFrames })}
        />
        
        {/* Tech Stack Scene */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.techStackDuration)}>
          <TechStackScene {...props} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: transitionFrames })}
        />
        
        {/* Conclusion Scene */}
        <TransitionSeries.Sequence durationInFrames={toFrames(props.conclusionDuration)}>
          <ConclusionScene {...props} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
