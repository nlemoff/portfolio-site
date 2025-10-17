'use client';

import { Html, useProgress } from '@react-three/drei';

export function Loader() {
  const { active, progress, errors, item, loaded, total } = useProgress();
  
  return (
    <Html center className="text-white">
      <div className="text-center">
        <div className="mb-2">Loading cyberpunk apartment...</div>
        <div className="w-48 h-2 bg-gray-700 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-cyan-400 to-pink-500 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="mt-2 text-sm">{Math.round(progress)}% loaded</div>
      </div>
    </Html>
  );
}