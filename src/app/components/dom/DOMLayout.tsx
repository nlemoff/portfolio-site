'use client';

import React from 'react';
import { Nav } from '@/app/components/dom/Nav';
import { Intro } from '@/app/components/dom/Intro';
import { About } from '@/app/components/dom/About';
import { Skills } from '@/app/components/dom/Skills';
import { Projects } from '@/app/components/dom/Projects';
import { Contact } from '@/app/components/dom/Contact';

interface DOMLayoutProps {
  children?: React.ReactNode;
}

export const DOMLayout = ({ children }: DOMLayoutProps) => {
  return (
    <div className="min-h-screen">
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