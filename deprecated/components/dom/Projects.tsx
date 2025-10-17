"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/app/components/ui/card";
import { Button } from "@/app/components/ui/button";
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogDescription, 
  DialogTrigger 
} from "@/app/components/ui/dialog";

const projects = [
  {
    title: "Project Alpha",
    description: "An immersive e-commerce experience using WebGL.",
    tags: ["Next.js", "React Three Fiber", "Stripe"],
    liveUrl: "#",
    githubUrl: "#",
    image: "/placeholder.svg"
  },
  {
    title: "Project Beta",
    description: "A data visualization platform for scientific research.",
    tags: ["React", "D3.js", "GraphQL"],
    liveUrl: "#",
    githubUrl: "#",
    image: "/placeholder.svg"
  },
  {
    title: "Project Gamma",
    description: "A real-time collaborative whiteboard application.",
    tags: ["SvelteKit", "WebSockets", "Tailwind CSS"],
    liveUrl: "#",
    githubUrl: "#",
    image: "/placeholder.svg"
  },
];

export const Projects = () => {
  return (
    <section id="projects" className="min-h-screen container mx-auto py-24 px-4">
      <h2 className="text-3xl font-bold mb-12 text-center">Projects</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {projects.map((project) => (
          <Dialog key={project.title}>
            <DialogTrigger asChild>
              <Card className="cursor-pointer hover:border-primary transition-colors">
                <CardHeader>
                  <CardTitle>{project.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{project.description}</p>
                </CardContent>
              </Card>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>{project.title}</DialogTitle>
                <DialogDescription>{project.description}</DialogDescription>
              </DialogHeader>
              <div className="py-4">
                <div className="flex flex-wrap gap-2 mb-4">
                    {project.tags.map(tag => (
                        <span key={tag} className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-primary-foreground bg-primary">
                            {tag}
                        </span>
                    ))}
                </div>
                {/* In a real project, you would have an image here */}
                {/* <img src={project.image} alt={project.title} className="w-full h-auto rounded-lg mb-4" /> */}
              </div>
              <div className="flex justify-end gap-4">
                <Button asChild variant="outline"><a href={project.githubUrl} target="_blank" rel="noopener noreferrer">GitHub</a></Button>
                <Button asChild><a href={project.liveUrl} target="_blank" rel="noopener noreferrer">Live Demo</a></Button>
              </div>
            </DialogContent>
          </Dialog>
        ))}
      </div>
    </section>
  );
};
