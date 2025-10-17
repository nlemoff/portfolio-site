import React, { useState } from 'react';
import { Box } from '@react-three/drei';

const Hotspot = ({ position, ...props }) => {
  const [hovered, setHover] = useState(false);
  return (
    <Box 
      position={position} 
      onPointerOver={() => setHover(true)} 
      onPointerOut={() => setHover(false)}
      {...props}
    >
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </Box>
  );
};

export function Hotspots() {
  return (
    <group>
      {/* Placeholder hotspots. Positions should match features in the apartment model. */}
      <Hotspot position={[0, 1, -3]} /> {/* About Me hotspot */}
      <Hotspot position={[-4, 1.5, 0]} /> {/* Skills hotspot */}
      <Hotspot position={[4, 1.5, 0]} /> {/* Projects hotspot */}
    </group>
  );
}
