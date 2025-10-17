'use client';

import React, { useMemo } from 'react';
import { Text } from '@react-three/drei';
import * as THREE from 'three';

export function NeonTitle() {
  const neonMaterial = useMemo(() => {
    return new THREE.MeshStandardMaterial({
      color: '#00ffff',
      emissive: '#00ffff',
      emissiveIntensity: 2,
      toneMapped: false,
      roughness: 0.2,
      metalness: 0.8
    });
  }, []);

  return (
    <group position={[0, 10, -50]}>
      <Text
        font="/fonts/Inter_Bold.json"
        fontSize={3}
        maxWidth={100}
        lineHeight={1}
        letterSpacing={0.02}
        textAlign="center"
        color="#00ffff"
        outlineWidth={0.05}
        outlineColor="#00ffff"
      >
        nlemoff.com
        <meshStandardMaterial
          color="#00ffff"
          emissive="#00ffff"
          emissiveIntensity={2}
          toneMapped={false}
        />
      </Text>
    </group>
  );
}