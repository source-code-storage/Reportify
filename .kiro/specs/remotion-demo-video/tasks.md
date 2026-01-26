# Implementation Plan: Remotion Demo Video

## Overview

This implementation plan breaks down the creation of the Reportify demo video into discrete, manageable tasks. Each task builds on previous work, with testing integrated throughout to ensure correctness. The plan follows a logical progression: setup → core infrastructure → scenes → polish → testing.

## Tasks

- [x] 1. Project Setup and Configuration
  - Initialize Remotion project with TypeScript
  - Install dependencies (@remotion/cli, @remotion/transitions, zod, tailwindcss)
  - Configure remotion.config.ts with video settings
  - Set up TypeScript configuration
  - Create project folder structure (scenes/, components/, utils/, types/)
  - _Requirements: 1.2, 1.3, 20.1_

- [x] 2. Define Type System and Props Schema
  - [x] 2.1 Create DemoVideoPropsSchema with Zod
    - Define all prop fields (branding, URLs, colors, durations, audio)
    - Set default values for all props
    - Add validation rules (min/max for durations, color formats)
    - Export TypeScript type from schema
    - _Requirements: 17.1, 17.2, 17.3, 17.4_

  - [ ]* 2.2 Write property test for props validation
    - **Property 10: Props Validation**
    - **Validates: Requirements 17.1**
    - Generate random valid and invalid props
    - Test that valid props pass validation
    - Test that invalid props throw ZodError
    - _Requirements: 17.1_

- [x] 3. Create Utility Functions
  - [x] 3.1 Implement timing utilities
    - Create calculateSceneTimings function
    - Create getTotalDuration function
    - Create toFrames helper function
    - _Requirements: 1.1, 1.4_

  - [x] 3.2 Implement animation utilities
    - Create fadeIn, fadeOut, slideIn functions
    - Define ANIMATION_CONFIGS presets (smooth, snappy, bouncy, heavy)
    - Define EASING_PRESETS
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 20.3_

  - [x] 3.3 Create color utilities
    - Create function to calculate contrast ratio
    - Create function to validate color format
    - _Requirements: 13.4_

  - [ ]* 3.4 Write property tests for utility functions
    - **Property 14: Scene Timing Calculation**
    - **Property 15: Animation Utility Functions**
    - **Validates: Requirements 1.4, 20.3**
    - Test fadeIn/fadeOut return values in [0, 1]
    - Test slideIn returns appropriate position values
    - Test scene timing calculations with various durations
    - _Requirements: 1.4, 20.3_

- [x] 4. Build Reusable Components
  - [x] 4.1 Create AnimatedText component
    - Implement basic text rendering
    - Add staggered character animation support
    - Add opacity animation
    - _Requirements: 2.4, 12.5_

  - [x] 4.2 Create Logo component
    - Design or import Reportify logo SVG
    - Add size and color props
    - Add animation support
    - _Requirements: 2.1, 15.2_

  - [x] 4.3 Create Screenshot component
    - Implement image loading with Img from Remotion
    - Add entrance animation with spring
    - Add error handling with fallback
    - Add border radius and shadow styling
    - _Requirements: 3.1, 3.4_

  - [x] 4.4 Create FeatureCard component
    - Design card layout for feature highlights
    - Add icon support
    - Add title and description text
    - Add entrance animation
    - _Requirements: 3.2_

  - [x] 4.5 Create TechIcon component
    - Create icon component for technology logos
    - Add animation support
    - Add label text
    - _Requirements: 10.5_

  - [x] 4.6 Create Caption component
    - Implement caption text rendering
    - Add background for contrast
    - Position in lower third
    - Add fade in/out animations
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

  - [ ]* 4.7 Write unit tests for components
    - Test AnimatedText renders text correctly
    - Test Logo accepts size and color props
    - Test Screenshot handles error states
    - Test Caption positioning and styling
    - _Requirements: 2.1, 2.4, 18.3_

- [ ] 5. Checkpoint - Verify Core Infrastructure
  - Ensure all utility functions work correctly
  - Ensure all reusable components render
  - Run unit tests
  - Ask the user if questions arise

- [x] 6. Implement Scene Components
  - [x] 6.1 Create IntroScene
    - Add Logo with spring scale animation
    - Add tagline with fade-in animation
    - Add problem statement with delayed fade-in
    - Use brand colors from props
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 6.2 Create LandingPageScene
    - Add screenshot of landing page
    - Add feature highlights with animations
    - Add zoom/spotlight effects for features
    - Add "Get Started" button highlight
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 6.3 Create AuthScene
    - Add registration form screenshot
    - Add login form screenshot
    - Add dashboard transition
    - Use slide-in animations
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 6.4 Create ReportCreationScene
    - Add "Create New Report" button interaction
    - Add report creation form
    - Add template upload visualization
    - Add section extraction animation
    - Animate each section appearing
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [x] 6.5 Create UploadScene
    - Add "Upload Notes" button interaction
    - Add file selection visualization
    - Add processing indicators with progress
    - Add embedding generation visualization
    - Add success confirmation
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

  - [x] 6.6 Create SearchScene
    - Add search interface with sample query
    - Add search results with relevance scores
    - Add semantic understanding callout
    - Add result snippets with context
    - Use staggered fade-in for results
    - Add "Semantic vs Keyword" comparison
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

  - [x] 6.7 Create GenerationScene
    - Add section selection in editor
    - Add "Generate Content" button interaction
    - Add loading animation during generation
    - Add typing effect for generated content
    - Add GPT-4 badge/indicator
    - Highlight key phrases
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7_

  - [x] 6.8 Create ExportScene
    - Add export button and dropdown
    - Show PDF and DOCX options
    - Add document preview
    - Show professional formatting
    - Add download confirmation
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_

  - [x] 6.9 Create TechStackScene
    - Display technology stack in grid layout
    - Show backend technologies with icons
    - Show frontend technologies with icons
    - Show AI technologies with icons
    - Animate icons appearing
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [x] 6.10 Create ConclusionScene
    - Display summary of key benefits
    - Show live demo URL
    - Show GitHub repository URL
    - Add "Built with Kiro CLI" badge
    - Add contact information
    - Add QR codes for URLs
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

  - [ ]* 6.11 Write unit tests for scenes
    - Test IntroScene renders logo and tagline
    - Test each scene accepts DemoVideoProps
    - Test scenes use brand colors from props
    - Test scenes render expected content
    - _Requirements: 2.1, 2.2, 2.5_

- [ ] 7. Checkpoint - Verify All Scenes
  - Preview each scene individually
  - Verify animations work correctly
  - Verify text is readable
  - Verify colors match brand
  - Ask the user if questions arise

- [x] 8. Compose Main Video
  - [x] 8.1 Create DemoVideo composition
    - Set up TransitionSeries structure
    - Add all 10 scenes in order
    - Add transitions between scenes (fade, slide)
    - Configure transition durations
    - Add background music support
    - Calculate total duration dynamically
    - _Requirements: 1.1, 1.4, 1.5, 1.6, 12.2, 12.3, 14.1_

  - [x] 8.2 Register composition in Root.tsx
    - Import DemoVideo component
    - Create Composition with correct dimensions (1920x1080)
    - Set fps to 30
    - Calculate durationInFrames from scene timings
    - Add defaultProps with Reportify branding
    - Add calculateMetadata for dynamic duration
    - _Requirements: 1.2, 1.3, 17.1_

  - [ ]* 8.3 Write property tests for composition
    - **Property 1: Total Duration Bounds**
    - **Property 2: Scene Structure Consistency**
    - **Property 3: Animation Timing Consistency**
    - **Validates: Requirements 1.1, 1.4, 12.6**
    - Test total duration is between 120-180 seconds
    - Test video contains 10 scenes and 9 transitions
    - Test all animations use fps from useVideoConfig
    - _Requirements: 1.1, 1.4, 12.6_

- [ ] 9. Add Captions and Accessibility
  - [ ] 9.1 Create caption data structure
    - Define caption timing for each scene
    - Write caption text for all narration
    - _Requirements: 18.1, 18.2_

  - [ ] 9.2 Integrate captions into scenes
    - Add Caption component to each scene
    - Synchronize caption timing with animations
    - Ensure captions are readable
    - _Requirements: 18.2, 18.3, 18.4, 18.5_

  - [ ]* 9.3 Write property tests for accessibility
    - **Property 8: Minimum Font Size**
    - **Property 9: Text Color Contrast**
    - **Validates: Requirements 13.3, 13.4**
    - Test all fontSize values >= 24px
    - Test all text has contrast ratio >= 4.5:1
    - _Requirements: 13.3, 13.4_

- [ ] 10. Implement Parametrization
  - [ ] 10.1 Verify all scenes use props
    - Ensure all text comes from props
    - Ensure all colors come from props
    - Ensure all durations come from props
    - _Requirements: 17.2, 17.3, 17.4_

  - [ ]* 10.2 Write property tests for parametrization
    - **Property 11: Text Parametrization**
    - **Property 12: Color Parametrization**
    - **Property 13: Duration Parametrization**
    - **Validates: Requirements 17.2, 17.3, 17.4**
    - Test changing text props changes rendered text
    - Test changing color props changes rendered colors
    - Test changing duration props changes scene timings
    - _Requirements: 17.2, 17.3, 17.4, 17.6_

- [ ] 11. Optimize Performance
  - [ ] 11.1 Add memoization
    - Use useMemo for expensive calculations
    - Use React.memo for components that don't need frequent updates
    - _Requirements: 19.2, 19.3_

  - [ ] 11.2 Optimize assets
    - Compress images to WebP format
    - Optimize audio file size
    - Use appropriate image dimensions
    - _Requirements: 19.1, 19.4_

  - [ ]* 11.3 Write unit tests for optimization
    - Test that expensive calculations are memoized
    - Test that components use React.memo where appropriate
    - _Requirements: 19.2, 19.3_

- [ ] 12. Add Audio and Sound Design
  - [ ] 12.1 Select background music
    - Find royalty-free background music
    - Ensure music fits video tone
    - Trim music to video duration
    - _Requirements: 14.1_

  - [ ] 12.2 Add sound effects
    - Add transition sound effects
    - Add button click sounds
    - Add success/completion sounds
    - _Requirements: 14.2, 14.3_

  - [ ] 12.3 Mix audio levels
    - Set background music volume to 30%
    - Ensure audio levels between -12dB and -6dB
    - Add fade in/out for music
    - _Requirements: 14.4, 14.5, 14.6_

- [ ] 13. Gather and Prepare Assets
  - [ ] 13.1 Take screenshots of Reportify
    - Screenshot landing page
    - Screenshot dashboard
    - Screenshot report editor
    - Screenshot search interface
    - Screenshot export options
    - _Requirements: 3.1, 5.1, 7.1, 9.1_

  - [ ] 13.2 Create or source brand assets
    - Export Reportify logo as SVG
    - Export favicon
    - Gather technology logos (FastAPI, React, GPT-4, etc.)
    - _Requirements: 2.1, 10.5, 15.2_

  - [ ] 13.3 Prepare fonts
    - Select professional sans-serif font
    - Select bold font for headings
    - Select monospace font for code
    - Load fonts using @remotion/google-fonts or local files
    - _Requirements: 13.1, 13.2, 13.5_

- [ ] 14. Final Polish and Testing
  - [ ] 14.1 Review all animations
    - Ensure smooth transitions
    - Verify spring animations feel natural
    - Check timing consistency
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.6_

  - [ ] 14.2 Review typography
    - Verify all text is readable
    - Check font sizes meet minimum
    - Verify text doesn't exceed 2-3 lines
    - _Requirements: 13.1, 13.2, 13.3, 13.6_

  - [ ] 14.3 Review branding
    - Verify brand colors are consistent
    - Check logo placement
    - Verify spacing and layout
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

  - [ ]* 14.4 Run all property tests
    - **Property 4: Spring Animation Usage**
    - **Property 5: Fade-In Animation Behavior**
    - **Property 6: Staggered Text Animation**
    - **Property 7: Brand Color Consistency**
    - **Validates: Requirements 12.1, 2.4, 12.5, 2.5, 15.1**
    - Run full property test suite (100+ iterations each)
    - Verify all properties pass
    - Fix any failing tests
    - _Requirements: 12.1, 2.4, 12.5, 2.5, 15.1_

- [ ] 15. Checkpoint - Final Review
  - Preview entire video from start to finish
  - Verify total duration is within bounds (120-180 seconds)
  - Check all scenes flow smoothly
  - Verify audio levels are appropriate
  - Ensure all text is readable
  - Ask the user for final approval

- [ ] 16. Render Final Video
  - [ ] 16.1 Render high-quality version
    - Run: `npx remotion render DemoVideo out/reportify-demo.mp4 --quality=90`
    - Verify output file size < 100MB
    - Verify video plays correctly
    - _Requirements: 16.2, 16.5_

  - [ ] 16.2 Create alternative versions (optional)
    - Render 60-second version for social media
    - Render with different props for A/B testing
    - Export captions as SRT file
    - _Requirements: 16.6, 18.6_

  - [ ] 16.3 Test rendered video
    - Play video in multiple players (VLC, browser, etc.)
    - Verify audio sync
    - Check for any rendering artifacts
    - Verify file format and codec
    - _Requirements: 16.2_

- [ ] 17. Documentation and Deployment
  - [ ] 17.1 Write README for video project
    - Document how to preview video
    - Document how to render video
    - Document how to customize props
    - List all dependencies
    - _Requirements: 20.4_

  - [ ] 17.2 Create usage examples
    - Show how to change text content
    - Show how to change colors
    - Show how to adjust scene durations
    - Show how to add new scenes
    - _Requirements: 17.2, 17.3, 17.4_

  - [ ] 17.3 Set up CI/CD (optional)
    - Create GitHub Actions workflow
    - Automate video rendering on push
    - Upload rendered video as artifact
    - _Requirements: 16.2_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation follows Remotion best practices throughout
- All animations are driven by useCurrentFrame(), not CSS
- All timing calculations use fps from useVideoConfig()
- All interpolations use extrapolateRight: 'clamp'
- All sequences use premountFor for smooth loading
