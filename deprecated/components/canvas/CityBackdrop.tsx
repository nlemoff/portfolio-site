import React from 'react';
import { Environment, Sky } from '@react-three/drei';

export function CityBackdrop() {
  return (
    <>
      {/* You can use a procedural sky or an HDR environment map */}
      {/* <Sky distance={450000} sunPosition={[0, 1, 0]} inclination={0} azimuth={0.25} /> */}
      
      {/* Replace with your actual HDR file */}
      <Environment files="/textures/city_hdr.hdr" background />

      {/* Add some fog for atmosphere */}
      <fog attach="fog" args={['#050505', 10, 50]} />
    </>
  );
}
