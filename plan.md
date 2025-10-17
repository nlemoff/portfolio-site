Vision


- Narrative: First-person perspective inside a moody, neon-lit apartment overlooking a cyberpunk city. Landing view faces the window; the city skyline shows “nlemoff.com” in lights. Scrolling guides the camera smoothly through the apartment to reveal sections that map to your resume/portfolio.
- UX: Scroll to move; minimal UI hints; on reduced motion or low-power devices, a static cinematic layout with screenshots and CSS transitions.
Core Tech


- Next.js (App Router) + TypeScript
- Three.js via React Three Fiber (R3F) + @react-three/drei
- Postprocessing (postprocessing + drei)
- GSAP ScrollTrigger or Drei’s ScrollControls (prefer ScrollControls for tight R3F integration)
- Tailwind CSS for UI
- Asset pipeline: GLTF (DRACO + Meshopt), KTX2 textures, lightmap baking from Blender
- Optional: Lenis for scroll smoothing, Zustand for state, usehooks-ts for utilities
Experience Structure


- Intro (Hero): Camera at window, city skyline. Neon “nlemoff.com” text visible in sky. Subtle rain, distant traffic light flicker, parallax clouds/haze.
- About: Pan from window to desk area. Display About content on a holographic panel or diegetic screen.
- Skills: Rotate toward a wall with animated neon “skill nodes” or a desk terminal where hovering toggles skill groups.
- Projects: Move to a shelf or wall with “frames” that show project previews (video thumbnails or interactive mini-screens). Clicking opens modal/lightbox overlay.
- Resume/Contact: Final area near a door or desk terminal with download resume button, contact form as in-world terminal UI.
- Footer/CTA: Small UI overlay that’s always available for quick navigation.
Scene/Camera + Scroll Strategy


- Use <ScrollControls> from drei with pages ≈ number_of_sections + small buffer (e.g., 5–6).
- Create a camera rig that interpolates to “waypoints” per section based on scroll offset. Use easing and look-at targets per waypoint.
- For accessibility and reduced motion: provide a toggle to switch from 3D scroll to a standard vertical page; keep content mirrored in DOM sections.
Art and Asset Pipeline


- Apartment Base:
	- Option 1: Model in Blender (modular walls, floor, furniture). Optimize topology; generate UV2 for lightmaps.
	- Option 2: Start with a CC0/royalty-free apartment kit, customize and optimize.
- City Skyline:
	- Mid-distance skyline as low-poly instanced blocks with emissive windows texture. Background HDRI for reflections + fog for depth. Add billboard planes with animated shader for traffic streaks.
- Neon “nlemoff.com” in sky:
	- Option A: 3D text mesh with emissive material and slight bloom.
	- Option B: Transparent floating sign or drone billboard.
- Lighting:
	- Key: Baked indirect lighting for apartment interior (lightmaps).
	- Runtime: A few dynamic area/rect lights for accent, plus emissive materials.
- Textures:
	- Compress to KTX2 (BasisU). Keep atlases small. Use normal/roughness/metalness; limit 4K textures, favor 2K or 1K when possible.
- Effects:
	- Volumetric-ish look via fog and subtle GodRays from the window (if perf allows).
	- Rain streaks on window via screen-space quads or shader; sparing use of bloom and chromatic aberration.
Performance


- Target mobile first:
	- Adaptive DPR [1, 2], cap to 1.5–2 on mobile.
	- Progressive enhancement: simple shaders and reduced particle counts on low-end devices.
	- Lazy-load heavy models with Suspense; prioritize the window scene first.
- Use Meshopt + DRACO; KTX2 for textures; keep GPU memory in check.
- Postprocessing chain: SMAA/FXAA, light bloom with low threshold, optional color grading LUT.
Information Architecture Mapping


- In-world hotspots/props correspond to sections:
	- Window: Intro + tagline.
	- Desk screen: About.
	- Skill wall/terminal: Skills.
	- Project frames: Projects.
	- Door/terminal: Resume/Contact.
- Overlay UI mirrors content:
	- Sticky, minimal nav with section shortcuts.
	- Modals for project details; maintain accessible DOM structure.
Accessibility and Fallbacks


- prefers-reduced-motion:
	- Disable camera scroll rig and postprocessing; use static hero and DOM sections.
- No WebGL/WebGPU:
	- Serve a static hero image (screenshot of the window view) and standard sections.
- Keyboard navigation:
	- Provide skip links and section jump buttons. Focus management for modals.
SEO


- Standard Next.js metadata, Open Graph tags, title/description.
- JSON-LD for Person/Organization.
- Preload critical fonts with font-display: swap.
- Ensure actual text content exists in the DOM, even if also represented in 3D.
Analytics and Telemetry


- Track section visibility and project clicks via IntersectionObserver.
- Respect Do Not Track and privacy.
Milestones


1. Concept + Blockout (days 1–3)

- Greybox apartment in Blender or in-scene primitives.
- Implement ScrollControls, camera waypoints, section DOM overlays.
- Rough neon text and city backdrop.

1. Visual Foundation (days 4–7)

- Replace blockout with optimized GLTF.
- Add lightmaps; basic postprocessing.
- Implement window rain/fog and neon text polish.

1. Content Integration (days 8–10)

- Hook About, Skills, Projects, Resume/Contact to in-world UI and overlays.
- Modal gallery for projects.

1. Performance + A11y (days 11–12)

- KTX2, DRACO, Meshopt, adaptive DPR, reduced motion.
- Keyboard/focus, ARIA, semantic HTML, Lighthouse pass.

1. Polish + Launch (days 13–14)

- Micro-interactions, copy edits, analytics.
- Deploy to Vercel; set up previews and monitoring.
Risks and Mitigations


- Heavy assets → Strict budgets, compression, lazy-load.
- Scroll jank → Use ScrollControls or Lenis+ScrollTrigger with throttling; avoid layout thrash.
- A11y trade-offs → Always mirror content in HTML; provide non-3D path.