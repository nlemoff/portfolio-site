"use client";

import React from 'react';
import { Button } from "@/app/components/ui/button";
import { ThemeToggle } from "@/app/components/ThemeToggle";

const navLinks = [
  { name: "About", href: "#about" },
  { name: "Skills", href: "#skills" },
  { name: "Projects", href: "#projects" },
  { name: "Contact", href: "#contact" },
];

export const Nav = () => {
  const scrollTo = (selector: string) => {
    const element = document.querySelector(selector);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 p-4 bg-background/80 backdrop-blur-sm">
      <div className="container mx-auto flex justify-between items-center">
        <a href="#intro" onClick={(e) => { e.preventDefault(); scrollTo('#intro'); }} className="font-bold text-lg cursor-pointer">
          nlemoff.com
        </a>
        <div className="hidden md:flex items-center gap-4">
          {navLinks.map((link) => (
            <Button variant="ghost" key={link.name} onClick={() => scrollTo(link.href)}>
              {link.name}
            </Button>
          ))}
        </div>
        <ThemeToggle />
      </div>
    </nav>
  );
};
