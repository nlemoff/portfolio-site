import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useScroll } from '@react-three/drei';
import * as THREE from 'three';

export function CameraRig() {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const scroll = useScroll();

  // Define camera waypoints for each section
  // These are illustrative and will need fine-tuning based on your apartment model
  const waypoints = [
    { position: new THREE.Vector3(0, 2, 10), lookAt: new THREE.Vector3(0, 2, 0) }, // Intro (window view)
    { position: new THREE.Vector3(-5, 2, 0), lookAt: new THREE.Vector3(0, 2, 0) }, // About (desk area)
    { position: new THREE.Vector3(0, 3, -5), lookAt: new THREE.Vector3(0, 2, -10) }, // Skills (wall/terminal)
    { position: new THREE.Vector3(5, 2, 0), lookAt: new THREE.Vector3(0, 2, 0) }, // Projects (shelf/wall)
    { position: new THREE.Vector3(0, 1, -10), lookAt: new THREE.Vector3(0, 1, -15) }, // Contact (door/terminal)
  ];

  useFrame(() => {
    if (cameraRef.current) {
      const offset = scroll.offset; // 0 to 1
      const numSections = waypoints.length - 1;
      const sectionIndex = Math.min(Math.floor(offset * numSections), numSections - 1);
      const sectionProgress = (offset * numSections) % 1;

      const currentWaypoint = waypoints[sectionIndex];
      const nextWaypoint = waypoints[Math.min(sectionIndex + 1, numSections)];

      // Interpolate position
      cameraRef.current.position.lerpVectors(
        currentWaypoint.position,
        nextWaypoint.position,
        sectionProgress
      );

      // Interpolate lookAt target
      const lookAtTarget = new THREE.Vector3().lerpVectors(
        currentWaypoint.lookAt,
        nextWaypoint.lookAt,
        sectionProgress
      );
      cameraRef.current.lookAt(lookAtTarget);

      cameraRef.current.updateProjectionMatrix();
    }
  });

  return <perspectiveCamera makeDefault ref={cameraRef} fov={75} near={0.1} far={1000} />;
}
