import React from 'react';
import { Nav } from './Nav';
import { Intro } from './Intro';
import { About } from './About';
import { Skills } from './Skills';
import { Projects } from './Projects';
import { Contact } from './Contact';

interface DOMLayoutProps {
  children?: React.ReactNode;
}

export const DOMLayout = ({ children }: DOMLayoutProps) => {
  return (
    <div>
      <Nav />
      <main>
        <Intro />
        <About />
        <Skills />
        <Projects />
        <Contact />
      </main>
      {children}
    </div>
  );
};
