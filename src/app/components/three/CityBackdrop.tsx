'use client';

import React, { useMemo } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

export function CityBackdrop() {
  // Create a simple cityscape with instanced meshes for performance
  const buildingGeometry = useMemo(() => {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    geometry.translate(0, 0.5, 0); // Move pivot to bottom
    return geometry;
  }, []);

  const buildingMaterial = useMemo(() => {
    return new THREE.MeshStandardMaterial({
      color: '#1a1a1a',
      emissive: '#ff6ad5',
      emissiveIntensity: 0.2,
      roughness: 0.9,
      metalness: 0.1
    });
  }, []);

  // Create instanced buildings
  const buildingCount = 100;
  const buildings = useMemo(() => {
    const positions = [];
    const scales = [];
    
    for (let i = 0; i < buildingCount; i++) {
      // Position buildings in a grid with some randomness
      const x = (i % 10 - 5) * 8 + (Math.random() - 0.5) * 4;
      const z = Math.floor(i / 10) * 8 + 20 + (Math.random() - 0.5) * 4;
      const height = 2 + Math.random() * 8;
      
      positions.push([x, 0, z]);
      scales.push([1, height, 1]);
    }
    
    return { positions, scales };
  }, []);

  return (
    <>
      {/* Background buildings */}
      <instancedMesh 
        args={[buildingGeometry, buildingMaterial, buildingCount]} 
        position={[0, 0, -50]}
      >
        {buildings.positions.map((pos, i) => (
          <group key={i} position={pos as [number, number, number]}>
            <mesh scale={buildings.scales[i] as [number, number, number]} />
          </group>
        ))}
      </instancedMesh>

      {/* Neon sign in the sky */}
      <mesh position={[0, 15, -100]}>
        <boxGeometry args={[20, 4, 0.5]} />
        <meshStandardMaterial 
          color="#ff6ad5" 
          emissive="#ff6ad5" 
          emissiveIntensity={2}
          toneMapped={false}
        />
      </mesh>
      
      {/* Fog for atmosphere */}
      <fog attach="fog" args={['#050505', 30, 100]} />
    </>
  );
}