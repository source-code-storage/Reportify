import { z } from 'zod';

// Zod schema for DemoVideo props with validation and defaults
export const DemoVideoPropsSchema = z.object({
  // Branding
  appName: z.string().default('ParatusAI'),
  tagline: z.string().default('AI-Powered Client Acquisition for Automation Freelancers'),
  logoUrl: z.string().optional(),
  
  // Colors (ParatusAI brand colors - automation theme)
  primaryColor: z.string().default('#10b981'), // green-500 (automation/flow)
  secondaryColor: z.string().default('#3b82f6'), // blue-500 (tech)
  accentColor: z.string().default('#8b5cf6'), // violet-500 (AI)
  backgroundColor: z.string().default('#0f172a'), // slate-900
  textColor: z.string().default('#f8fafc'), // slate-50
  
  // Scene durations (in seconds)
  introDuration: z.number().min(5).max(8).default(6),
  landingPageDuration: z.number().min(8).max(12).default(10),
  authDuration: z.number().min(6).max(10).default(8),
  reportCreationDuration: z.number().min(12).max(18).default(15),
  uploadDuration: z.number().min(10).max(15).default(12),
  searchDuration: z.number().min(15).max(20).default(17),
  generationDuration: z.number().min(18).max(25).default(20),
  exportDuration: z.number().min(8).max(12).default(10),
  techStackDuration: z.number().min(8).max(12).default(10),
  conclusionDuration: z.number().min(8).max(12).default(10),
  
  // Transition duration
  transitionDuration: z.number().min(0.3).max(1.0).default(0.5),
  
  // Audio
  backgroundMusicUrl: z.string().optional(),
  musicVolume: z.number().min(0).max(1).default(0.3),
});

// TypeScript type inferred from Zod schema
export type DemoVideoProps = z.infer<typeof DemoVideoPropsSchema>;

// Scene timing interface
export interface SceneTiming {
  name: string;
  startFrame: number;
  durationInFrames: number;
  endFrame: number;
}
