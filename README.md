# Cyberpunk Apartment Portfolio

This is a Next.js, React Three Fiber, and Tailwind CSS project that creates an immersive portfolio experience.

## Getting Started

### Prerequisites

- Node.js (v18 or later)
- npm, yarn, or pnpm

### 1. Install Dependencies

```bash
npm install
```

This will also trigger the `postinstall` script which downloads the necessary WebAssembly decoders for Draco and Meshopt into the `/public/wasm` directory.

### 2. Add 3D Assets (Manual Step)

This project requires a few 3D assets that cannot be included in the repository. You need to provide them yourself.

1.  **Apartment Model:**
    -   Find or create a low-poly apartment model.
    -   Optimize it using tools like glTF-Pipeline with Draco and Meshopt compression.
    -   Place it at `public/models/apartment.glb`.

2.  **Lightmap Texture:**
    -   Bake lighting in a 3D software like Blender.
    -   Export the texture and convert it to KTX2 format.
    -   Place it at `public/textures/apartment_lightmap.ktx2`.

3.  **Environment Map:**
    -   Find a suitable HDR image for the city skyline (e.g., from Poly Haven).
    -   Place it at `public/textures/city_hdr.hdr`.

For placeholder assets, you can search for CC0 (Creative Commons Zero) assets on sites like Sketchfab or Poly Haven.

### 3. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Building for Production

To create a production-ready build, run:

```bash
npm run build
```

This will create an optimized build in the `.next` directory.

To run the production build locally, use:

```bash
npm run start
```

## Deployment on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

This project includes a `.github/workflows/deploy.yml` file for continuous deployment. Push your code to a GitHub repository and link it to a Vercel project.