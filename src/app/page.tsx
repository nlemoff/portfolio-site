'use client'

import { Button } from "@/components/ui/button"
import { FileText, Github, Linkedin, Twitter } from "lucide-react"
import Link from "next/link"
import ContactForm from "./components/contact-form"
import ProjectCard from "./components/project-card"
import TechStack from "./components/tech-stack"
import Experience from "./components/experience"
import Education from "./components/education"
import { ThemeToggle } from "@/components/theme-toggle"
import NavLink from "./components/nav-link"

export default function Home() {
  return (
    <div className="min-h-screen bg-background retro-grid">
      <div className="fixed inset-0 bg-vaporwave-gradient opacity-5 pointer-events-none"></div>

      <header className="sticky top-0 z-50 w-full border-b border-vaporwave-pink/20 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <div className="mr-4 hidden md:flex">
            <Link className="mr-6 flex items-center space-x-2" href="/">
              <span className="hidden font-bold sm:inline-block gradient-text">Nick Lemoff</span>
            </Link>
            <nav className="flex items-center space-x-6 text-sm font-medium">
              <NavLink href="#about">About</NavLink>
              <NavLink href="#education">Education</NavLink>
              <NavLink href="#experience">Experience</NavLink>
              <NavLink href="#projects">Projects</NavLink>
              <NavLink href="#skills">Skills</NavLink>
              <NavLink href="#contact">Contact</NavLink>
            </nav>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="container px-4 md:px-6">
        <section id="about" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none gradient-text animate-gradient">
                  Nick Lemoff
                </h1>
                <p className="mx-auto max-w-[760px] text-slate-700 md:text-xl dark:text-gray-300">
                  Founding engineer focused on applied AI research and full-stack product engineering. I turn papers, open-source systems, and fast prototypes into production agents, retrieval systems, eval harnesses, and user-facing software.
                </p>
              </div>
              <div className="flex flex-wrap justify-center gap-3">
                <Link href="/resume.pdf" target="_blank">
                  <Button className="bg-vaporwave-pink text-vaporwave-dark hover:bg-vaporwave-pink/90">
                    <FileText className="mr-2 h-4 w-4" />
                    Resume
                  </Button>
                </Link>
                <Link href="https://github.com/nlemoff" target="_blank">
                  <Button
                    variant="outline"
                    size="icon"
                    className="border-vaporwave-purple/50 hover:bg-vaporwave-purple/10 hover:border-vaporwave-purple"
                  >
                    <Github className="h-4 w-4" />
                    <span className="sr-only">GitHub</span>
                  </Button>
                </Link>
                <Link href="https://linkedin.com/in/nicklemoff/" target="_blank">
                  <Button
                    variant="outline"
                    size="icon"
                    className="border-vaporwave-blue/50 hover:bg-vaporwave-blue/10 hover:border-vaporwave-blue"
                  >
                    <Linkedin className="h-4 w-4" />
                    <span className="sr-only">LinkedIn</span>
                  </Button>
                </Link>
                <Link href="https://x.com/nlemoff" target="_blank">
                  <Button
                    variant="outline"
                    size="icon"
                    className="border-vaporwave-teal/50 hover:bg-vaporwave-teal/10 hover:border-vaporwave-teal"
                  >
                    <Twitter className="h-4 w-4" />
                    <span className="sr-only">Twitter</span>
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        <section id="education" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
              Education
            </h2>
            <Education />
          </div>
        </section>

        <section id="experience" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
              Professional Experience
            </h2>
            <Experience />
          </div>
        </section>

        <section id="projects" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
              Projects
            </h2>
            <div className="max-w-4xl mx-auto space-y-6">
              <ProjectCard
                title="Evie — Full Proof's real-time deposition agent"
                description="Architected the production AI agent system described in my resume: a GCP-backed real-time agent with FastAPI streaming endpoints, hybrid RAG over case documents, agent memory, live transcript orchestration, citation-grounded outputs, and replay/eval infrastructure."
                tags={["Real-time agents", "Hybrid RAG", "FastAPI", "React", "TypeScript", "PostgreSQL", "Redis", "Google Cloud"]}
              />
              <ProjectCard
                title="SfRB — Straightforward Resume Builder"
                description="Local-first TypeScript resume design tool with an installable Node CLI, Vite browser editor, canonical JSON document model, Zod validation, template system, shared print/PDF export surface, overflow checks, and optional AI layout repair proposals behind explicit user acceptance."
                link="https://github.com/nlemoff/SfRB"
                tags={["TypeScript", "Node CLI", "Vite", "Zod", "Playwright", "PDF export", "Local-first"]}
              />
              <ProjectCard
                title="FEBSim — Formula Electric Berkeley lap simulation"
                description="Formula Electric Berkeley's lap simulation project for racecar performance modeling. Led simulations work around lap-time modeling, vehicle dynamics, CAN/simulation analysis, Dockerized contributor workflows, and team engineering practices."
                link="https://github.com/Formula-Electric-Berkeley/FEBSim"
                tags={["Simulation", "Vehicle dynamics", "Python", "Docker", "Data analysis"]}
              />
              <ProjectCard
                title="Personal Portfolio Website"
                description="A responsive portfolio website built with Next.js, TypeScript, and Tailwind CSS. Current version is a clean content refresh before a larger interactive 3D redesign."
                link="https://github.com/nlemoff/portfolio-site"
                tags={["Next.js", "TypeScript", "Tailwind CSS", "shadcn/ui"]}
              />
              <ProjectCard
                title="Audio Transcriber"
                description="A macOS application that captures both microphone and system audio while providing real-time transcription capabilities using Fast API and Docker."
                link="https://github.com/nlemoff/audio-transcriber"
                tags={["SwiftUI", "Docker", "Fast API", "GCP"]}
              />
            </div>
          </div>
        </section>

        <section id="skills" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
              Skills
            </h2>
            <TechStack />
          </div>
        </section>

        <section id="contact" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto max-w-2xl">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
                Get in Touch
              </h2>
              <ContactForm />
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-vaporwave-pink/20">
        <div className="container flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6">
          <p className="text-xs text-slate-600 dark:text-gray-300">© 2026 Nick Lemoff. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

