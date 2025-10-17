'use client';

import React, { useEffect, useMemo } from 'react';
import { useGLTF, useKTX2 } from '@react-three/drei';
import * as THREE from 'three';

export function Apartment(props: JSX.IntrinsicElements['group']) {
  // For now, we'll create a simple apartment blockout
  // In the final version, this will load the actual GLB model
  const { scene } = useGLTF('/models/apartment.glb', '/wasm/draco/');
  const lightmap = useKTX2('/textures/apartment_lightmap.ktx2');

  useEffect(() => {
    scene.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        // Apply lightmap if available
        if (lightmap) {
          child.material.lightMap = lightmap;
          child.material.lightMapIntensity = 1.5;
        }
        child.material.needsUpdate = true;
      }
    });
  }, [scene, lightmap]);

  return <primitive object={scene} {...props} />;
}

// For now, let's create a simple blockout version
export function ApartmentBlockout(props: JSX.IntrinsicElements['group']) {
  const materials = useMemo(() => ({
    floor: new THREE.MeshStandardMaterial({ 
      color: '#2a2a2a',
      roughness: 0.8,
      metalness: 0.2
    }),
    wall: new THREE.MeshStandardMaterial({ 
      color: '#1a1a1a',
      roughness: 0.9,
      metalness: 0.1
    }),
    window: new THREE.MeshStandardMaterial({ 
      color: '#54d6ff',
      emissive: '#54d6ff',
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.7
    }),
    furniture: new THREE.MeshStandardMaterial({ 
      color: '#c774e8',
      roughness: 0.6,
      metalness: 0.3
    })
  }), []);

  return (
    <group {...props}>
      {/* Floor */}
      <mesh position={[0, 0, 0]} material={materials.floor}>
        <boxGeometry args={[20, 0.2, 20]} />
      </mesh>
      
      {/* Walls */}
      <mesh position={[0, 2.5, -10]} material={materials.wall}>
        <boxGeometry args={[20, 5, 0.2]} />
      </mesh>
      <mesh position={[10, 2.5, 0]} rotation={[0, Math.PI/2, 0]} material={materials.wall}>
        <boxGeometry args={[20, 5, 0.2]} />
      </mesh>
      <mesh position={[-10, 2.5, 0]} rotation={[0, Math.PI/2, 0]} material={materials.wall}>
        <boxGeometry args={[20, 5, 0.2]} />
      </mesh>
      
      {/* Window */}
      <mesh position={[0, 3, -9.9]} material={materials.window}>
        <boxGeometry args={[8, 4, 0.1]} />
      </mesh>
      
      {/* Furniture */}
      <mesh position={[-5, 1, 0]} material={materials.furniture}>
        <boxGeometry args={[2, 1, 1]} />
      </mesh>
      <mesh position={[-5, 0.5, 0]} material={materials.furniture}>
        <boxGeometry args={[2.5, 0.1, 1.5]} />
      </mesh>
      
      {/* Desk screen */}
      <mesh position={[-5, 2, 0]} material={materials.window}>
        <boxGeometry args={[1.5, 1, 0.1]} />
      </mesh>
    </group>
  );
}