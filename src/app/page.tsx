'use client';

import { useState, useEffect } from 'react';
import { usePrefersReducedMotion, useWebGLSupport } from '@/lib/hooks';
import { SceneCanvas } from '@/app/components/three/SceneCanvas';
import { StaticFallback } from '@/app/components/StaticFallback';

export default function Home() {
  const prefersReducedMotion = usePrefersReducedMotion();
  const isWebGLSupported = useWebGLSupport();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  // Use fallback for reduced motion or no WebGL support
  if (!isClient || prefersReducedMotion || !isWebGLSupported) {
    return <StaticFallback />;
  }

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <SceneCanvas />
    </div>
  );
}