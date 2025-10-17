"use client";

import React, { useEffect } from 'react';
import { useGLTF, useKTX2 } from '@react-three/drei';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';
import * as THREE from 'three';

export function Apartment(props: JSX.IntrinsicElements['group']) {
  // This is a placeholder component. 
  // You need to replace the paths with your actual assets.
  const { scene } = useGLTF('/models/apartment.glb');
  const lightmap = useKTX2('/textures/apartment_lightmap.ktx2');

  useEffect(() => {
    scene.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        // Apply lightmap
        child.material.lightMap = lightmap;
        child.material.lightMapIntensity = 1.5;
        child.material.needsUpdate = true;
      }
    });
  }, [scene, lightmap]);

  return <primitive object={scene} {...props} />;
}

// Configure loaders
useGLTF.preload('/models/apartment.glb', (loader: GLTFLoader) => {
  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath('/wasm/draco/');
  loader.setDRACOLoader(dracoLoader);

  const ktx2Loader = new KTX2Loader();
  ktx2Loader.setTranscoderPath('/wasm/draco/'); // Note: Draco's basis transcoder is often used
  loader.setKTX2Loader(ktx2Loader.detectSupport(new THREE.WebGLRenderer()));

  loader.setMeshoptDecoder(MeshoptDecoder);
});

useKTX2.preload('/textures/apartment_lightmap.ktx2');
