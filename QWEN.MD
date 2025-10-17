# gemini.md — Immersive Cyberpunk Apartment Portfolio (Next.js + R3F)

Role
- You are a senior Frontend ple+ WebGL engineer and technical artist.
- Deliver a production-ready Next.js App Router project with an immersive, performant Three.js scene via React Three Fiber.

Project
- Rebuild nlemoff.com as a first-person, scroll-driven experience inside a neon-lit apartment overlooking a cyberpunk city.
- On load, the camera faces the window with “nlemoff.com” glowing in the sky. Scrolling moves the camera through apartment waypoints to reveal About, Skills, Projects, and Resume/Contact.
- Provide graceful fallbacks for reduced motion and non-WebGL environments.

Tech stack
- Next.js (App Router) + TypeScript
- Tailwind CSS
- Three.js via @react-three/fiber + @react-three/drei
- postprocessing (with drei effects)
- Optional: Lenis (smooth scroll), GSAP ScrollTrigger (only if needed), Zustand (state)
- Loaders: DRACO + Meshopt + KTX2
- ESLint + Prettier

Output format
- First: concise file tree.
- Then: full code for each file.
- Include minimal asset samples (tiny KTX2 textures, small GLTF for apartment blockout, example HDRI or procedural sky).
- End with run/build/deploy instructions and notes.

Target structure
- app/
  - layout.tsx
  - page.tsx
  - globals.css (imports Tailwind)
  - components/
    - ui/
      - Header.tsx
      - OverlayNav.tsx
      - SectionPanels.tsx
      - Modal.tsx
    - three/
      - SceneCanvas.tsx
      - Experience.tsx
      - CameraRig.tsx
      - CityBackdrop.tsx
      - NeonTitle.tsx
      - Apartment.tsx
      - Hotspots.tsx
      - Effects.tsx
  - (optional) sitemap.ts, robots.txt
- lib/
  - three/
    - loaders.ts (DRACO, Meshopt, KTX2 config)
    - perf.ts (adaptive DPR, frame budget)
    - a11y.ts (prefers-reduced-motion checks)
- public/
  - models/
    - apartment.glb (light low-poly blockout; DRACO + Meshopt)
  - textures/
    - city_windows.ktx2
    - metal_rough.ktx2
    - emission_sign.ktx2
  - env/
    - night_neon.hdr (small, example)
  - wasm/
    - draco/
    - meshopt/
    - basis/
  - images/
    - hero_fallback.jpg
- styles/
  - tailwind.css (if separated)
- next.config.js
- tailwind.config.ts
- postcss.config.js
- tsconfig.json
- .eslintrc.cjs
- .prettierrc

Core features to implement
- Scene + Scroll
  - Use <Canvas> from R3F in a client component.
  - Use <ScrollControls pages={N}> from drei; N ≈ 5 to cover all sections.
  - CameraRig: interpolate camera position and look-at using scroll.offset; define waypoints per section.
- Apartment + City
  - Apartment: GLTF blockout with basic materials; UV2 for lightmaps. Provide placeholder lightmap and baked feel.
  - CityBackdrop: instanced low-poly blocks with emissive window texture + exponential fog. Minimal geometry to appear dense.
- Neon “nlemoff.com”
  - Mesh text with emissive material; slight animated flicker and subtle bloom. Position visible through window on initial frame.
- Effects
  - Postprocessing composer: SMAA/FXAA, light bloom (low intensity), optional color grading. Keep subtle.
  - Window rain streaks: simple screen-aligned quad with UV distortion; toggle off on low power.
- Hotspots + Sections
  - Map scroll ranges to sections: Intro, About, Skills, Projects, Resume/Contact.
  - Hotspots are meshes with subtle pulsing; on hover/focus show in-world labels; click opens DOM modal with content.
  - Always mirror content in DOM panels for SEO and accessibility.
- Performance
  - DPR clamp [1, 2]; adaptive on frame dips. Pause render on tab blur.
  - Lazy-load GLTF and effects. Use KTX2 textures, DRACO + Meshopt. Keep draw calls low.
  - Offer “Low” quality toggle: fewer particles, effects off, simpler shaders.
- Accessibility
  - Respect prefers-reduced-motion: bypass ScrollControls; show static hero_fallback.jpg and standard vertical sections with CSS transitions.
  - Keyboard: provide overlay nav with section jump buttons; focus management in modals; roles/labels and high-contrast focus rings.
- SEO
  - Next.js metadata, Open Graph tags, JSON-LD for Person. Preload fonts with font-display: swap.

Detailed implementation guidance
- SceneCanvas.tsx
  - Configure color space, tone mapping (ACES), shadow map if needed, gl.clearColor to match theme.
  - dpr={[1, 2]} and onCreated pauseRender logic on blur/visibilitychange.
- CameraRig.tsx
  - Define an array of waypoints: { pos: [x,y,z], lookAt: [x,y,z], start: number, end: number } mapped to scroll ranges.
  - Lerp camera position/orientation each frame; use smooth easing.
- Experience.tsx
  - Wrap with <ScrollControls pages={5} damping={0.15}>, include <Scroll> for 3D scene and <Scroll html> for overlay DOM.
  - Add Apartment, CityBackdrop, NeonTitle, Hotspots, and Effects.
- loaders.ts
  - Set decoder paths: /wasm/draco/, /wasm/meshopt/; set KTX2 transcoder path /wasm/basis/.
- Effects.tsx
  - Minimal composer with <EffectComposer> and <Bloom> low intensity; conditionally add SMAA/FXAA.
- Hotspots.tsx
  - Create interactive meshes with raycast events; maintain accessible equivalents in DOM (buttons linked to sections).
- SectionPanels.tsx
  - Content cards for About, Skills, Projects, Resume/Contact; appear in <Scroll html>; tie visibility to scroll offsets and ARIA attributes.
- CityBackdrop.tsx
  - InstancedMesh for buildings; material with emissive windows texture; GPU-generated positions; fog for depth.
- NeonTitle.tsx
  - Use <Text> from drei with emissive material and mild flicker via a time-based uniform.

Content to include
- About: Bio + headshot.
- Skills: Categories with proficiency indicators.
- Projects: Grid of cards; each opens modal with description, tech, links, and media.
- Resume/Contact: Download Resume (PDF), EmailJS form or serverless action.

Performance budgets
- Main scene draw calls: ≤ 150 desktop, ≤ 80 mobile.
- GPU memory: ≤ 250 MB desktop, ≤ 150 MB mobile.
- LCP ≤ 2.5s mid-tier mobile; CLS < 0.05.

Acceptance criteria
- Scroll from window intro to each section smoothly; waypoints feel cinematic.
- Reduced motion mode shows static hero and standard sections with no 3D scroll.
- Lighthouse mobile: Performance ≥ 90, A11y ≥ 95, Best Practices ≥ 95, SEO ≥ 90.
- No WebGL errors, memory stable after 2 minutes idle.

Commands to Gemini
- Generate the complete Next.js (App Router) project as specified.
- Include a functional blockout apartment.glb (very low poly) and tiny example textures in KTX2.
- Provide all code files with minimal but tasteful visuals out of the box.
- Add comments only where necessary; keep files concise and typed.
- Ensure npm scripts: dev, build, start. Include Vercel deployment notes.

Run/build
- npm install
- npm run dev → http://localhost:3000
- npm run build && npm start
- Vercel deployment: push to GitHub → import on Vercel.

Notes
- Keep dependencies lean; avoid heavy effect stacks.
- Ensure WebGL enhances, not blocks, the experience.