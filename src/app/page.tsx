'use client'

import { Button } from "@/components/ui/button"
import { Github, Linkedin, Mail } from "lucide-react"
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
            <Button variant="outline" className="border-vaporwave-pink/50 hover:bg-vaporwave-pink/10">
              Resume
            </Button>
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
                <p className="mx-auto max-w-[700px] text-gray-400 md:text-xl dark:text-gray-300">
                  Full Stack Developer, Data Scientist & Machine Learning Engineer based in the San Francisco Bay Area
                </p>
              </div>
              <div className="space-x-4">
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
                <Link href="mailto:nlemoff@gmail.com">
                  <Button
                    variant="outline"
                    size="icon"
                    className="border-vaporwave-teal/50 hover:bg-vaporwave-teal/10 hover:border-vaporwave-teal"
                  >
                    <Mail className="h-4 w-4" />
                    <span className="sr-only">Email</span>
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
                title="Audio Transcriber"
                description="A macOS application that captures both microphone and system audio while providing real-time transcription capabilities using Fast API and Docker."
                link="https://github.com/nlemoff/audio-transcriber"
                tags={["SwiftUI", "Docker", "Fast API", "GCP"]}
              />
              <ProjectCard
                title="Machine Learning Visualizer"
                description="A React-based web application for visualizing machine learning model predictions with interactive data visualization using Chart.js."
                link="https://github.com/nlemoff/ml-visualizer"
                tags={["React", "TypeScript", "Chart.js", "Tailwind CSS"]}
              />
              <ProjectCard
                title="POV Classification in Sentences"
                description="A BERT-based deep learning model for multi-class Point of View (POV) classification in literary texts, achieving 65% accuracy."
                link="https://github.com/nlemoff/pov-classification"
                tags={["BERT", "NLP", "Deep Learning", "Python"]}
              />
              <ProjectCard
                title="Titanic Survival Prediction"
                description="Led a UC Berkeley-hosted Kaggle competition team, focusing on predicting Titanic passenger survival with 80% accuracy."
                link="https://github.com/nlemoff/titanic-prediction"
                tags={["Kaggle", "Machine Learning", "Python", "Data Science"]}
              />
              <ProjectCard
                title="Earnings Predictions for College Graduates"
                description="Analyzed the interplay between college majors, gender, and earnings, to shed light on the gender wage gap's influence in early career stages."
                link="https://github.com/nlemoff/earnings-prediction"
                tags={["Data Analysis", "Prediction Models", "Python"]}
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
          <p className="text-xs text-gray-400 dark:text-gray-300">© 2024 Nick Lemoff. All rights reserved.</p>
          <nav className="sm:ml-auto flex gap-4 sm:gap-6">
            <Link className="text-xs hover:text-vaporwave-pink transition-colors" href="mailto:nlemoff@gmail.com">
              nlemoff@gmail.com
            </Link>
            <Link className="text-xs hover:text-vaporwave-pink transition-colors" href="tel:+13046852696">
              +1 (304) 685-2696
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  )
}

