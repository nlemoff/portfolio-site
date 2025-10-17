'use client';

import React, { useState } from 'react';
import { useThree } from '@react-three/fiber';

interface HotspotProps {
  position: [number, number, number];
  section: string;
  onClick: () => void;
}

const Hotspot = ({ position, section, onClick }: HotspotProps) => {
  const [hovered, setHover] = useState(false);
  const { camera } = useThree();
  
  // Calculate scale based on distance from camera for consistent sizing
  const distance = camera.position.distanceTo(new THREE.Vector3(...position));
  const scale = Math.max(0.5, distance * 0.05);

  return (
    <mesh
      position={position}
      scale={hovered ? scale * 1.2 : scale}
      onPointerOver={() => setHover(true)}
      onPointerOut={() => setHover(false)}
      onClick={onClick}
      visible={false} // Hide in 3D view, show in DOM
    >
      <sphereGeometry args={[0.5, 16, 16]} />
      <meshStandardMaterial 
        color={hovered ? '#ff6ad5' : '#54d6ff'} 
        emissive={hovered ? '#ff6ad5' : '#54d6ff'}
        emissiveIntensity={hovered ? 1 : 0.5}
        transparent
        opacity={0.7}
      />
    </mesh>
  );
};

export function Hotspots() {
  const handleHotspotClick = (section: string) => {
    // Scroll to the section
    const element = document.getElementById(section);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <group>
      <Hotspot 
        position={[0, 2, -9]} 
        section="about" 
        onClick={() => handleHotspotClick('about')} 
      />
      <Hotspot 
        position={[-5, 2, 0]} 
        section="skills" 
        onClick={() => handleHotspotClick('skills')} 
      />
      <Hotspot 
        position={[5, 2, 0]} 
        section="projects" 
        onClick={() => handleHotspotClick('projects')} 
      />
      <Hotspot 
        position={[0, 1, -15]} 
        section="contact" 
        onClick={() => handleHotspotClick('contact')} 
      />
    </group>
  );
}