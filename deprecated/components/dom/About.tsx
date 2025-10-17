import React from 'react';

export const About = () => {
  return (
    <section id="about" className="min-h-screen container mx-auto py-24 px-4">
      <h2 className="text-3xl font-bold mb-8 text-center">About Me</h2>
      <div className="max-w-3xl mx-auto text-lg text-center text-muted-foreground">
        <p>
          I am a creative developer with a passion for building immersive and interactive web experiences. 
          With a background in both design and development, I strive to bridge the gap between aesthetics and functionality.
        </p>
        <p className="mt-4">
          This portfolio is a reflection of my love for cyberpunk aesthetics and my skills in modern web technologies like Next.js, React Three Fiber, and Tailwind CSS.
        </p>
      </div>
    </section>
  );
};
