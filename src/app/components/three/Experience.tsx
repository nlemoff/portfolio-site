'use client';

import React from 'react';
import { Apartment } from '@/app/components/three/Apartment';
import { CityBackdrop } from '@/app/components/three/CityBackdrop';
import { NeonTitle } from '@/app/components/three/NeonTitle';
import { Hotspots } from '@/app/components/three/Hotspots';
import { CameraRig } from '@/app/components/three/CameraRig';

export function Experience() {
  return (
    <>
      <CameraRig />
      <ambientLight intensity={0.1} />
      <pointLight position={[10, 10, 10]} intensity={0.5} color="#ff6ad5" />
      <pointLight position={[-10, 5, -10]} intensity={0.3} color="#54d6ff" />
      
      <CityBackdrop />
      <NeonTitle />
      <Apartment position={[0, 0, 0]} />
      <Hotspots />
    </>
  );
}