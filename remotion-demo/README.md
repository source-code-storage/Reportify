# Reportify Demo Video

Professional demo video for Reportify built with Remotion, following all best practices.

## 🎬 Features

- **10 Animated Scenes**: Introduction, Landing Page, Auth, Report Creation, Upload, Search, AI Generation, Export, Tech Stack, Conclusion
- **Smooth Transitions**: Fade and slide transitions between scenes
- **Spring Animations**: Natural motion using Remotion's spring physics
- **Fully Parametrized**: Customize text, colors, and durations via props
- **Type-Safe**: Built with TypeScript and Zod schema validation
- **Accessible**: High contrast text and proper font sizes

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
```

### Preview

```bash
# Start Remotion Studio
npm start
```

This will open the Remotion Studio at `http://localhost:3000` where you can preview and edit the video.

### Render

```bash
# Render the video
npm run build
```

The video will be rendered to `out/reportify-demo.mp4`.

## 📐 Video Specifications

- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 fps
- **Duration**: ~2-3 minutes (configurable)
- **Format**: MP4 (H.264 codec)

## 🎨 Customization

### Change Text Content

Edit the default props in `src/Root.tsx`:

```typescript
const defaultProps: DemoVideoProps = {
  appName: 'Your App Name',
  tagline: 'Your Tagline',
  liveUrl: 'https://your-url.com',
  // ... other props
};
```

### Change Colors

```typescript
const defaultProps: DemoVideoProps = {
  primaryColor: '#your-color',
  secondaryColor: '#your-color',
  accentColor: '#your-color',
  backgroundColor: '#your-color',
  textColor: '#your-color',
};
```

### Change Scene Durations

```typescript
const defaultProps: DemoVideoProps = {
  introDuration: 6, // seconds
  landingPageDuration: 10,
  // ... other durations
};
```

### Render with Custom Props

```bash
npx remotion render DemoVideo out/video.mp4 --props='{"appName":"Custom Name"}'
```

## 📁 Project Structure

```
remotion-demo/
├── src/
│   ├── components/          # Reusable components
│   │   ├── AnimatedText.tsx
│   │   ├── Logo.tsx
│   │   ├── Screenshot.tsx
│   │   ├── FeatureCard.tsx
│   │   ├── TechIcon.tsx
│   │   └── Caption.tsx
│   ├── scenes/              # Scene components
│   │   ├── IntroScene.tsx
│   │   ├── LandingPageScene.tsx
│   │   ├── TechStackScene.tsx
│   │   ├── ConclusionScene.tsx
│   │   └── DemoScene.tsx
│   ├── utils/               # Utility functions
│   │   ├── timing.ts
│   │   ├── animations.ts
│   │   └── colors.ts
│   ├── types/               # TypeScript types
│   │   └── index.ts
│   ├── DemoVideo.tsx        # Main composition
│   ├── Root.tsx             # Composition registry
│   └── index.ts             # Entry point
├── public/                  # Static assets
│   ├── images/
│   └── audio/
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

## 🎯 Remotion Best Practices Followed

✅ All animations driven by `useCurrentFrame()`  
✅ Time calculations use `fps` from `useVideoConfig()`  
✅ Spring animations for natural motion  
✅ Interpolations use `extrapolateRight: 'clamp'`  
✅ TransitionSeries for smooth scene transitions  
✅ Zod schema for props validation  
✅ TypeScript for type safety  
✅ Proper component organization  
✅ Memoization for performance  
✅ Accessibility considerations

## 📝 Notes

- No CSS animations or transitions (they don't render correctly in Remotion)
- All timing is frame-based, not time-based
- Sequences use `premountFor` for smooth loading
- Colors meet WCAG AA contrast requirements
- Font sizes are minimum 24px for readability

## 🔧 Advanced Usage

### Add Background Music

1. Place audio file in `public/audio/`
2. Update props:

```typescript
const defaultProps: DemoVideoProps = {
  backgroundMusicUrl: staticFile('audio/background.mp3'),
  musicVolume: 0.3,
};
```

### Render Different Quality

```bash
# High quality (larger file)
npx remotion render DemoVideo out/video.mp4 --quality=100

# Lower quality (smaller file)
npx remotion render DemoVideo out/video.mp4 --quality=70
```

### Render Specific Frame Range

```bash
# Render only first 10 seconds (300 frames at 30fps)
npx remotion render DemoVideo out/video.mp4 --frames=0-300
```

## 📚 Resources

- [Remotion Documentation](https://www.remotion.dev/docs)
- [Remotion Best Practices](https://www.remotion.dev/docs/best-practices)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Zod Documentation](https://zod.dev/)

## 📄 License

MIT

---

**Built with ❤️ using Remotion and Kiro CLI**
