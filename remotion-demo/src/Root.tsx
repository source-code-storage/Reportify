import { Composition, staticFile } from 'remotion';
import { DemoVideo } from './DemoVideo';
import { DemoVideoPropsSchema, DemoVideoProps } from './types';
import { calculateSceneTimings, getTotalDuration } from './utils/timing';

/**
 * Root component - registers all compositions
 * Following Remotion best practice: use Zod schema for props validation
 */
export const RemotionRoot: React.FC = () => {
  // Default props with Reportify branding and background music
  const defaultProps: DemoVideoProps = DemoVideoPropsSchema.parse({
    backgroundMusicUrl: staticFile('audio/2 Minute Timer with Relaxing LoFi Music for Classroom.mp3'),
    musicVolume: 0.25, // 25% volume for background music
  });
  
  // Calculate total duration dynamically
  const fps = 30;
  const timings = calculateSceneTimings(defaultProps, fps);
  const totalDurationInFrames = getTotalDuration(timings);
  
  return (
    <>
      <Composition
        id="DemoVideo"
        component={DemoVideo}
        durationInFrames={totalDurationInFrames}
        fps={fps}
        width={1920}
        height={1080}
        defaultProps={defaultProps}
        schema={DemoVideoPropsSchema}
      />
    </>
  );
};
