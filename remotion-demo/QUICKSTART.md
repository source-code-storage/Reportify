# 🚀 Quick Start Guide

## Start the Remotion Studio

```bash
cd remotion-demo
npm start
```

This will open the Remotion Studio in your browser at `http://localhost:3000`.

## What You'll See

The Remotion Studio will show:
- **Preview Player**: Watch your video in real-time
- **Timeline**: See all scenes and transitions
- **Props Editor**: Customize text, colors, and durations
- **Render Button**: Export the final video

## Customize the Video

### In the Studio

1. Click the "Props" tab in the right sidebar
2. Edit any property (app name, colors, durations, etc.)
3. See changes instantly in the preview

### In Code

Edit `src/Root.tsx` to change default props:

```typescript
const defaultProps: DemoVideoProps = {
  appName: 'Your App Name',
  tagline: 'Your Custom Tagline',
  primaryColor: '#your-color',
  // ... more props
};
```

## Render the Video

### From the Studio

1. Click the "Render" button in the top right
2. Choose quality and codec settings
3. Click "Render" to export

### From Command Line

```bash
npm run build
```

The video will be saved to `out/reportify-demo.mp4`.

## Tips

- **Preview is fast**: Changes appear instantly
- **Scrub the timeline**: Click and drag to see any frame
- **Keyboard shortcuts**: Space to play/pause, arrow keys to step through frames
- **Props are live**: Edit props and see changes without restarting

## Troubleshooting

### Port 3000 already in use

```bash
# Use a different port
npx remotion studio --port=3001
```

### Slow preview

- Close other applications
- Reduce preview quality in settings
- Disable some animations temporarily

## Next Steps

1. **Add screenshots**: Place images in `public/images/`
2. **Add music**: Place audio in `public/audio/`
3. **Customize scenes**: Edit files in `src/scenes/`
4. **Add new scenes**: Create new scene components

## Need Help?

- Check `README.md` for full documentation
- Visit [Remotion Docs](https://www.remotion.dev/docs)
- Review the code - it's well-commented!

---

**Happy video making! 🎬**
