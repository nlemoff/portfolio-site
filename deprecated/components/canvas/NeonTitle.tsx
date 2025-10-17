import React from 'react';
import { Text3D } from '@react-three/drei';

export function NeonTitle() {
  return (
    <group position={[-10, 5, -30]}>
      <Text3D
        font="/fonts/Inter_Bold.json" // Make sure to have this font file
        size={3}
        height={0.2}
        curveSegments={12}
        bevelEnabled
        bevelThickness={0.02}
        bevelSize={0.02}
        bevelOffset={0}
        bevelSegments={5}
      >
        nlemoff.com
        <meshStandardMaterial emissive="#00ffff" emissiveIntensity={2} toneMapped={false} />
      </Text3D>
    </group>
  );
}
