import { DemoVideoProps, SceneTiming } from '../types';

/**
 * Convert seconds to frames
 * Following Remotion best practice: always multiply seconds by fps
 */
export const toFrames = (seconds: number, fps: number): number => {
  return Math.round(seconds * fps);
};

/**
 * Calculate scene timings with transitions
 * Transitions overlap adjacent scenes, so total duration is shorter than sum of scenes
 */
export const calculateSceneTimings = (
  props: DemoVideoProps,
  fps: number
): SceneTiming[] => {
  const transitionFrames = toFrames(props.transitionDuration, fps);
  const scenes: SceneTiming[] = [];
  let currentFrame = 0;
  
  const addScene = (name: string, durationInSeconds: number) => {
    const durationInFrames = toFrames(durationInSeconds, fps);
    scenes.push({
      name,
      startFrame: currentFrame,
      durationInFrames,
      endFrame: currentFrame + durationInFrames,
    });
    // Subtract transition duration for overlap (except for first scene)
    currentFrame += durationInFrames - (scenes.length > 1 ? transitionFrames : 0);
  };
  
  // Add all scenes in order
  addScene('intro', props.introDuration);
  addScene('landingPage', props.landingPageDuration);
  addScene('auth', props.authDuration);
  addScene('reportCreation', props.reportCreationDuration);
  addScene('upload', props.uploadDuration);
  addScene('search', props.searchDuration);
  addScene('generation', props.generationDuration);
  addScene('export', props.exportDuration);
  addScene('techStack', props.techStackDuration);
  addScene('conclusion', props.conclusionDuration);
  
  return scenes;
};

/**
 * Get total duration in frames from scene timings
 */
export const getTotalDuration = (timings: SceneTiming[]): number => {
  if (timings.length === 0) return 0;
  return timings[timings.length - 1].endFrame;
};

/**
 * Get total duration in seconds
 */
export const getTotalDurationInSeconds = (timings: SceneTiming[], fps: number): number => {
  return getTotalDuration(timings) / fps;
};
