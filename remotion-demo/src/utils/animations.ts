import { interpolate, Easing, SpringConfig } from 'remotion';

/**
 * Animation configuration presets
 * Following Remotion best practice: use spring animations for natural motion
 */
export const ANIMATION_CONFIGS = {
  smooth: { damping: 200 } as SpringConfig, // Smooth, no bounce (subtle reveals)
  snappy: { damping: 20, stiffness: 200 } as SpringConfig, // Snappy, minimal bounce (UI elements)
  bouncy: { damping: 8 } as SpringConfig, // Bouncy entrance (playful animations)
  heavy: { damping: 15, stiffness: 80, mass: 2 } as SpringConfig, // Heavy, slow, small bounce
};

/**
 * Easing presets for interpolations
 */
export const EASING_PRESETS = {
  easeInOut: Easing.inOut(Easing.quad),
  easeOut: Easing.out(Easing.quad),
  easeIn: Easing.in(Easing.quad),
  easeInOutSin: Easing.inOut(Easing.sin),
};

/**
 * Fade in animation
 * Following Remotion best practice: always use extrapolateRight: 'clamp'
 */
export const fadeIn = (
  frame: number,
  startFrame: number,
  duration: number
): number => {
  return interpolate(
    frame,
    [startFrame, startFrame + duration],
    [0, 1],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
    }
  );
};

/**
 * Fade out animation
 */
export const fadeOut = (
  frame: number,
  startFrame: number,
  duration: number
): number => {
  return interpolate(
    frame,
    [startFrame, startFrame + duration],
    [1, 0],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
    }
  );
};

/**
 * Slide in animation
 * Returns position offset (use with transform: translateX or translateY)
 */
export const slideIn = (
  frame: number,
  startFrame: number,
  duration: number,
  distance: number
): number => {
  return interpolate(
    frame,
    [startFrame, startFrame + duration],
    [distance, 0],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
      easing: EASING_PRESETS.easeOut,
    }
  );
};

/**
 * Slide out animation
 */
export const slideOut = (
  frame: number,
  startFrame: number,
  duration: number,
  distance: number
): number => {
  return interpolate(
    frame,
    [startFrame, startFrame + duration],
    [0, distance],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
      easing: EASING_PRESETS.easeIn,
    }
  );
};

/**
 * Scale animation
 */
export const scaleAnimation = (
  frame: number,
  startFrame: number,
  duration: number,
  fromScale: number = 0,
  toScale: number = 1
): number => {
  return interpolate(
    frame,
    [startFrame, startFrame + duration],
    [fromScale, toScale],
    {
      extrapolateRight: 'clamp',
      extrapolateLeft: 'clamp',
      easing: EASING_PRESETS.easeOut,
    }
  );
};
