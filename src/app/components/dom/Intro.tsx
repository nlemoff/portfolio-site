'use client';

import React from 'react';
import { Github, Linkedin, Twitter } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Intro() {
  return (
    <section 
      id="about" 
      className="relative py-12 md:py-24 lg:py-32 flex items-center justify-center min-h-screen"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-violet-900/20 to-cyan-900/20 pointer-events-none" />
      <div className="container px-4 md:px-6 relative z-10">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none gradient-text animate-gradient">
              Nick Lemoff
            </h1>
            <p className="mx-auto max-w-[700px] text-gray-400 md:text-xl dark:text-gray-300">
              Full Stack Developer, Data Scientist & Machine Learning Engineer based in the San Francisco Bay Area
            </p>
          </div>
          <div className="space-x-4">
            <a href="https://github.com/nlemoff" target="_blank" rel="noopener noreferrer">
              <Button
                variant="outline"
                size="icon"
                className="border-vaporwave-purple/50 hover:bg-vaporwave-purple/10 hover:border-vaporwave-purple"
              >
                <Github className="h-4 w-4" />
                <span className="sr-only">GitHub</span>
              </Button>
            </a>
            <a href="https://linkedin.com/in/nicklemoff/" target="_blank" rel="noopener noreferrer">
              <Button
                variant="outline"
                size="icon"
                className="border-vaporwave-blue/50 hover:bg-vaporwave-blue/10 hover:border-vaporwave-blue"
              >
                <Linkedin className="h-4 w-4" />
                <span className="sr-only">LinkedIn</span>
              </Button>
            </a>
            <a href="https://x.com/nlemoff" target="_blank" rel="noopener noreferrer">
              <Button
                variant="outline"
                size="icon"
                className="border-vaporwave-teal/50 hover:bg-vaporwave-teal/10 hover:border-vaporwave-teal"
              >
                <Twitter className="h-4 w-4" />
                <span className="sr-only">Twitter</span>
              </Button>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}