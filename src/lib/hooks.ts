import { useState, useEffect } from 'react';

const QUERY = '(prefers-reduced-motion: no-preference)';

export const usePrefersReducedMotion = () => {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(true);

  useEffect(() => {
    const mediaQuery = window.matchMedia(QUERY);
    setPrefersReducedMotion(!mediaQuery.matches);

    const listener = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(!event.matches);
    };

    mediaQuery.addEventListener('change', listener);
    return () => {
      mediaQuery.removeEventListener('change', listener);
    };
  }, []);

  return prefersReducedMotion;
};

export const useWebGLSupport = () => {
    const [isSupported, setIsSupported] = useState(true);

    useEffect(() => {
        try {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            setIsSupported(!!context);
        } catch (e) {
            setIsSupported(false);
        }
    }, []);

    return isSupported;
}