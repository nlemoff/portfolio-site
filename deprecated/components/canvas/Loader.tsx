import { Html, useProgress } from '@react-three/drei';

export function Loader() {
  const { active, progress, errors, item, loaded, total } = useProgress();
  return (
    <Html center>
      <div className="text-white">
        {progress.toFixed(2)} % loaded
      </div>
    </Html>
  );
}
