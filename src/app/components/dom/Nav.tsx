'use client';

import React from 'react';
import { ThemeToggle } from '@/app/components/dom/ThemeToggle';

export function Nav() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-vaporwave-pink/20 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <a className="mr-6 flex items-center space-x-2" href="/">
            <span className="hidden font-bold sm:inline-block gradient-text">Nick Lemoff</span>
          </a>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <a 
              href="#about" 
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              About
            </a>
            <a 
              href="#skills" 
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Skills
            </a>
            <a 
              href="#projects" 
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Projects
            </a>
            <a 
              href="#contact" 
              className="transition-colors hover:text-foreground/80 text-foreground"
            >
              Contact
            </a>
          </nav>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}