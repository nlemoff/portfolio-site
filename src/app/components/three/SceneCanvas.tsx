'use client';

import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { ScrollControls, Scroll, Environment, Fog, Sky } from '@react-three/drei';
import { Experience } from '@/app/components/three/Experience';
import { Loader } from '@/app/components/three/Loader';
import { Effects } from '@/app/components/three/Effects';

export function SceneCanvas() {
  return (
    <>
      <Canvas
        className="w-full h-full"
        gl={{ 
          antialias: true, 
          alpha: false,
          powerPreference: "high-performance"
        }}
        camera={{ position: [0, 2, 10], fov: 75 }}
        dpr={[1, 2]}
        frameloop="always"
        shadows
      >
        <color attach="background" args={['#050505']} />
        <fog attach="fog" args={['#050505', 10, 50]} />
        
        <Suspense fallback={null}>
          <ScrollControls pages={6} damping={0.15}>
            <Scroll>
              <Experience />
            </Scroll>
            <Scroll html>
              {/* DOM content will be added here */}
            </Scroll>
          </ScrollControls>
          <Effects />
        </Suspense>
      </Canvas>
      <Loader />
    </>
  );
}