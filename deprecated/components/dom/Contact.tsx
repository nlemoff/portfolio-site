"use client";

import React from 'react';
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Textarea } from "@/app/components/ui/textarea";
import { Label } from "@/app/components/ui/label";

export const Contact = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission logic here
    alert("Form submitted! (This is a placeholder)");
  };

  return (
    <section id="contact" className="min-h-screen container mx-auto py-24 px-4 flex flex-col justify-center">
      <h2 className="text-3xl font-bold mb-12 text-center">Contact</h2>
      <div className="max-w-xl mx-auto w-full">
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid w-full items-center gap-1.5">
            <Label htmlFor="name">Name</Label>
            <Input type="text" id="name" placeholder="Your Name" required />
          </div>
          <div className="grid w-full items-center gap-1.5">
            <Label htmlFor="email">Email</Label>
            <Input type="email" id="email" placeholder="your.email@example.com" required />
          </div>
          <div className="grid w-full items-center gap-1.5">
            <Label htmlFor="message">Message</Label>
            <Textarea id="message" placeholder="Your message..." required />
          </div>
          <div className="flex justify-between items-center">
            <Button type="submit">Send Message</Button>
            <Button variant="outline" asChild>
                <a href="/resume.pdf" download>Download Resume</a>
            </Button>
          </div>
        </form>
      </div>
    </section>
  );
};
